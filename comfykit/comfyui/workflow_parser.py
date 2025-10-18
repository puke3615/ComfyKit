import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from comfykit.logger import logger


class WorkflowParam(BaseModel):
    name: str
    type: str = Field(default="str")
    required: bool = True
    default: Optional[Any] = None
    need_upload: bool = False

class WorkflowParamMapping(BaseModel):
    """Parameter mapping information"""
    param_name: str
    node_id: str
    input_field: str
    node_class_type: str
    need_upload: bool = False

class WorkflowOutputMapping(BaseModel):
    """Output mapping information"""
    node_id: str
    output_var: str

class WorkflowMappingInfo(BaseModel):
    """Workflow mapping information"""
    param_mappings: List[WorkflowParamMapping]
    output_mappings: List[WorkflowOutputMapping]

class WorkflowMetadata(BaseModel):
    title: str
    params: Dict[str, WorkflowParam]
    mapping_info: WorkflowMappingInfo
    workflow_id: Optional[str] = None  # RunningHub workflow ID
    is_runninghub: bool = False  # Whether this is a RunningHub workflow

class WorkflowParser:
    """Workflow parser - ComfyKit DSL
    
    DSL Syntax:
    - Basic: $param_name.field_name
    - Shorthand: $param_name (auto-maps to same field name)
    - Upload: $~param or $param.~field (needs media upload)
    - Required: $param! or $param.field!
    - Multiple: Display Text, $param1!, $param2
    
    Examples:
    - "Load Image, $~image!" → param 'image', needs upload, required
    - "Size, $width!, $height!" → two required params
    - "$prompt.text!" → param 'prompt' maps to field 'text', required
    """

    def __init__(self):
        pass

    def parse_title(self, title: str) -> List[str]:
        """Extract parameter markers from title
        
        Title format: "Display Text, $param1, $param2"
        
        Args:
            title: Node title string
            
        Returns:
            List of parameter markers (starting with $)
        """
        if not title:
            return []
        
        parts = [p.strip() for p in title.split(',')]
        return [p for p in parts if p.startswith('$')]

    def parse_param_marker(self, marker: str) -> Optional[Dict[str, Any]]:
        """Parse single parameter marker
        
        Syntax: $[~]param_name[.field_name][!][:description]
        
        Note: :description is for backward compatibility and will be ignored
        
        Examples:
        - $width → {name: 'width', field: 'width', upload: False, required: False}
        - $width! → {name: 'width', field: 'width', upload: False, required: True}
        - $~image → {name: 'image', field: 'image', upload: True, required: False}
        - $~image! → {name: 'image', field: 'image', upload: True, required: True}
        - $prompt.text! → {name: 'prompt', field: 'text', upload: False, required: True}
        - $image.~image! → {name: 'image', field: 'image', upload: True, required: True}
        - $prompt.text!:desc → same as $prompt.text! (desc ignored for backward compat)
        
        Returns:
            Dict with: name, field, upload, required
        """
        if not marker or not marker.startswith('$'):
            return None
        
        # Remove leading $
        marker = marker[1:]
        
        # Remove description part (backward compatibility)
        if ':' in marker:
            marker = marker.split(':', 1)[0]
        
        # Extract required flag
        required = marker.endswith('!')
        if required:
            marker = marker[:-1]
        
        # Extract upload flag at param level
        upload = marker.startswith('~')
        if upload:
            marker = marker[1:]
        
        # Split param and field
        if '.' in marker:
            param_name, field_part = marker.split('.', 1)
            
            # Check field-level upload flag
            if field_part.startswith('~'):
                upload = True
                field_name = field_part[1:]
            else:
                field_name = field_part
        else:
            # Shorthand: $param → $param.param
            param_name = marker
            field_name = marker
        
        return {
            'name': param_name,
            'field': field_name,
            'upload': upload,
            'required': required
        }

    def infer_type_from_value(self, value: Any) -> str:
        """Infer type from value"""
        if isinstance(value, bool):
            return "bool"
        elif isinstance(value, int):
            return "int"
        elif isinstance(value, float):
            return "float"
        else:
            return "str"

    def extract_field_value(self, node_data: Dict[str, Any], field_name: str) -> Any:
        """Extract value from the specified field of the node
        
        Returns None if:
        - Field doesn't exist
        - Field is a node connection (list format)
        """
        inputs = node_data.get("inputs", {})

        # Check if the specified field exists and is not a node connection
        if field_name in inputs and not isinstance(inputs[field_name], list):
            return inputs[field_name]

        return None

    def parse_output_marker(self, title: str) -> Optional[str]:
        """Parse output marker
        
        Format: $output.name
        """
        if not title.startswith('$output.'):
            return None

        output_var = title[8:]  # Remove '$output.'
        return output_var if output_var else None

    def is_known_output_node(self, class_type: str) -> bool:
        """Check if it is a known output node type"""
        known_output_types = {
            'SaveImage',
            'SaveVideo',
            'SaveAudio',
            'VHS_SaveVideo',
            'VHS_SaveAudio'
        }
        return class_type in known_output_types

    def parse_node(self, node_id: str, node_data: Dict[str, Any]) -> tuple[List[WorkflowParam], List[WorkflowParamMapping], Optional[WorkflowOutputMapping]]:
        """Parse parameters or outputs from the node
        
        Returns:
            (params_list, mappings_list, output_mapping)
            
        Note: Now supports multiple params per node!
        """
        # Check if the node is valid
        if not isinstance(node_data, dict) or "_meta" not in node_data:
            return [], [], None

        title = node_data["_meta"].get("title", "")
        class_type = node_data.get("class_type", "")

        # 1. Check if it is an output marker
        output_var = self.parse_output_marker(title)
        if output_var:
            output_mapping = WorkflowOutputMapping(
                node_id=node_id,
                output_var=output_var
            )
            return [], [], output_mapping

        # 2. Check if it is a known output node
        if self.is_known_output_node(class_type):
            # Use node_id as default output variable name
            output_mapping = WorkflowOutputMapping(
                node_id=node_id,
                output_var=node_id
            )
            return [], [], output_mapping

        # 3. Parse parameter markers from title
        param_markers = self.parse_title(title)
        if not param_markers:
            return [], [], None

        params = []
        mappings = []

        # 4. Parse each parameter marker
        for marker in param_markers:
            param_info = self.parse_param_marker(marker)
            if not param_info:
                logger.warning(f"Failed to parse parameter marker: {marker}")
                continue

            param_name = param_info['name']
            field_name = param_info['field']
            is_required = param_info['required']
            need_upload = param_info['upload']

            # 5. Extract default value and infer type
            default_value = self.extract_field_value(node_data, field_name)
            param_type = self.infer_type_from_value(default_value) if default_value is not None else "str"

            # 6. Verify required logic
            if not is_required and default_value is None:
                message = f"Parameter `{param_name}` has no default value but not marked as required (node {node_id})"
                logger.error(message)
                raise Exception(message)

            # 7. Create parameter object
            param = WorkflowParam(
                name=param_name,
                type=param_type,
                required=is_required,
                default=None if is_required else default_value,
                need_upload=need_upload
            )

            # 8. Create parameter mapping
            param_mapping = WorkflowParamMapping(
                param_name=param_name,
                node_id=node_id,
                input_field=field_name,
                node_class_type=class_type,
                need_upload=need_upload
            )

            params.append(param)
            mappings.append(param_mapping)

        return params, mappings, None

    def parse_workflow(self, workflow_data: Dict[str, Any], title: str) -> Optional[WorkflowMetadata]:
        """Parse complete workflow using ComfyKit DSL
        
        Scans all nodes and extracts parameter/output mappings based on DSL markers.
        """
        # Scan all nodes, collect parameter and mapping information
        params = {}
        param_mappings = []
        output_mappings = []

        for node_id, node_data in workflow_data.items():
            params_list, mappings_list, output_mapping = self.parse_node(node_id, node_data)

            # Add all parameters from this node
            for param in params_list:
                if param.name in params:
                    logger.warning(f"Duplicate parameter name: {param.name} (node {node_id})")
                params[param.name] = param

            # Add all mappings from this node
            param_mappings.extend(mappings_list)

            # Add output mapping if exists
            if output_mapping:
                output_mappings.append(output_mapping)

        # Build mapping_info
        mapping_info = WorkflowMappingInfo(
            param_mappings=param_mappings,
            output_mappings=output_mappings
        )

        # Build metadata
        metadata = WorkflowMetadata(
            title=title,
            params=params,
            mapping_info=mapping_info
        )

        return metadata

    def parse_workflow_file(self, file_path: str, tool_name: Optional[str] = None) -> Optional[WorkflowMetadata]:
        """Parse workflow file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            workflow_data = json.load(f)

        # Extract title from file name (remove suffix)
        title = tool_name or Path(file_path).stem

        return self.parse_workflow(workflow_data, title)

