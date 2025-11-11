import copy
import json
import mimetypes
import os
import random
import tempfile
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Dict, List, Optional, Tuple
from urllib.parse import urlparse

import aiohttp

from comfykit.comfyui.models import ExecuteResult
from comfykit.comfyui.workflow_parser import WorkflowMetadata, WorkflowParser
from comfykit.logger import logger
from comfykit.utils.os_util import get_data_path

# Node types that need special media upload handling
MEDIA_UPLOAD_NODE_TYPES = {
    'LoadImage',
    'LoadAudio',
    'LoadVideo',
    'VHS_LoadAudioUpload',
    'VHS_LoadVideo',
}

class ComfyUIExecutor(ABC):
    """ComfyUI executor abstract base class"""

    def __init__(self, base_url: str = None, api_key: str = None, cookies: str = None):
        """Initialize executor
        
        Args:
            base_url: ComfyUI base URL (optional)
            api_key: API key for authentication (optional)
            cookies: Cookies for authentication (optional)
        """
        self.base_url = (base_url or "http://127.0.0.1:8188").rstrip('/')
        self.api_key = api_key
        self.cookies = cookies

    @abstractmethod
    async def execute_workflow(self, workflow_file: str, params: Dict[str, Any] = None) -> ExecuteResult:
        """Abstract method to execute a workflow"""
        pass

    async def _parse_comfyui_cookies(self) -> Optional[Dict[str, str]]:
        """Parse COMFYUI_COOKIES configuration and return cookies dictionary
        Supports three formats:
        1. HTTP URL - Access cookies from a URL
        2. JSON string format - directly parse
        3. Key-value string format - parse to dictionary
        """
        if not self.cookies:
            return None

        try:
            content = self.cookies.strip()

            # Check if it is an HTTP URL
            if content.startswith(('http://', 'https://')):
                async with aiohttp.ClientSession() as session:
                    async with session.get(content) as response:
                        if response.status != 200:
                            raise Exception(f"Failed to get cookies from URL: HTTP {response.status}")
                        content = await response.text()
                        content = content.strip()
                        logger.info(f"Successfully got cookies from URL: {content}")

            # Parse cookies content
            if content.startswith('{'):
                return json.loads(content)
            else:
                cookies = {}
                for pair in content.split(';'):
                    if '=' in pair:
                        k, v = pair.strip().split('=', 1)
                        cookies[k.strip()] = v.strip()
                return cookies
        except Exception as e:
            logger.warning(f"Failed to parse COMFYUI_COOKIES: {e}")
            return None

    @asynccontextmanager
    async def get_comfyui_session(self) -> AsyncGenerator[aiohttp.ClientSession, None]:
        """Create aiohttp session with authentication"""
        headers = {}
        
        # Add API key if configured
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        
        # Parse cookies
        cookies = await self._parse_comfyui_cookies()
        
        # Create session with auth
        async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
            yield session


    def _generate_63bit_seed(self) -> int:
        """Generate a 63-bit random integer seed.

        Using SystemRandom to avoid global RNG side-effects in multi-threaded or
        multi-tenant environments.
        """
        return random.SystemRandom().randint(0, (1 << 63) - 1)

    def _randomize_seed_in_workflow(self, workflow_data: Dict[str, Any]) -> tuple[Dict[str, Any], Dict[str, int]]:
        """Replace any node inputs.seed == 0 (int or string "0") with a new random seed.

        Returns a tuple of (modified_workflow, seed_changes) where seed_changes maps
        node_id (as string) to the new seed value.
        """
        changed: Dict[str, int] = {}
        for node_id, node in workflow_data.items():
            if not isinstance(node, dict):
                continue
            inputs = node.get("inputs")
            if not isinstance(inputs, dict):
                continue
            if "seed" in inputs:
                val = inputs.get("seed")
                is_zero = (isinstance(val, int) and val == 0) or (isinstance(val, str) and str(val).strip() == "0")
                if is_zero:
                    new_seed = self._generate_63bit_seed()
                    inputs["seed"] = new_seed
                    changed[str(node_id)] = new_seed
        if changed:
            logger.info(f"Randomized seeds for {len(changed)} node(s): {changed}")
        return workflow_data, changed

    async def _apply_param_mapping(self, workflow_data: Dict[str, Any], mapping: Any, param_value: Any):
        """Apply single parameter based on parameter mapping"""
        node_id = mapping.node_id
        input_field = mapping.input_field
        node_class_type = mapping.node_class_type
        need_upload = mapping.need_upload  # Check if upload is needed (from DSL ~marker)

        # Check if node exists
        if node_id not in workflow_data:
            logger.warning(f"Node {node_id} does not exist in workflow")
            return

        node_data = workflow_data[node_id]

        # Ensure inputs exist
        if "inputs" not in node_data:
            node_data["inputs"] = {}

        # Priority 1: Check DSL upload marker (~)
        if need_upload:
            await self._handle_media_upload(node_data, input_field, param_value)
        # Priority 2: Check if node type needs special media upload handling (backward compatibility)
        elif node_class_type in MEDIA_UPLOAD_NODE_TYPES:
            await self._handle_media_upload(node_data, input_field, param_value)
        else:
            # Regular parameter setting
            await self._set_node_param(node_data, input_field, param_value)

    async def _handle_media_upload(self, node_data: Dict[str, Any], input_field: str, param_value: Any):
        """Handle media upload"""
        # Ensure inputs exist
        if "inputs" not in node_data:
            node_data["inputs"] = {}

        # If parameter value is a URL starting with http, upload media first
        if isinstance(param_value, str):
            if param_value.startswith(('http://', 'https://')):
                try:
                    # Upload media and get uploaded media name
                    media_value = await self._upload_media_from_source(param_value)
                    # Use uploaded media name as node input value
                    await self._set_node_param(node_data, input_field, media_value)
                    logger.info(f"Media upload successful: {media_value}")
                except Exception as e:
                    logger.error(f"Media upload failed: {str(e)}")
                    raise Exception(f"Media upload failed: {str(e)}")
            # Handle local file path
            elif os.path.exists(param_value):
                try:
                    uploaded_filename = await self._upload_media(param_value)
                    await self._set_node_param(node_data, input_field, uploaded_filename)
                    logger.info(f"Media upload successful (local file): {uploaded_filename}")
                except Exception as e:
                    logger.error(f"Failed to upload local file {param_value}: {str(e)}")
                    raise Exception(f"Failed to upload local file: {str(e)}")
        else:
            # Use parameter value as media name
            await self._set_node_param(node_data, input_field, param_value)

    async def _set_node_param(self, node_data: Dict[str, Any], input_field: str, param_value: Any):
        """Set node parameter"""
        # Ensure inputs exist
        if "inputs" not in node_data:
            node_data["inputs"] = {}
        # Set parameter value
        node_data["inputs"][input_field] = param_value

    async def _upload_media_from_source(self, media_url: str) -> str:
        """Upload media from URL"""
        async with self.get_comfyui_session() as session:
            async with session.get(media_url) as response:
                if response.status != 200:
                    raise Exception(f"Download media failed: HTTP {response.status}")

                # Extract filename from URL
                parsed_url = urlparse(media_url)
                filename = os.path.basename(parsed_url.path)
                if not filename:
                    filename = f"temp_media_{hash(media_url)}.jpg"

                # Get media data
                media_data = await response.read()

                # Save to temporary file
                suffix = os.path.splitext(filename)[1] or ".jpg"
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(media_data)
                    temp_path = tmp.name

        try:
            # Upload temporary file to ComfyUI
            return await self._upload_media(temp_path)
        finally:
            # Delete temporary file
            os.unlink(temp_path)

    async def _upload_media(self, media_path: str) -> str:
        """Upload media to ComfyUI"""
        # Read media data
        with open(media_path, 'rb') as f:
            media_data = f.read()

        # Extract filename
        filename = os.path.basename(media_path)

        # Automatically detect file MIME type
        mime_type = mimetypes.guess_type(filename)[0]
        if mime_type is None:
            mime_type = 'application/octet-stream'

        # Prepare form data
        data = aiohttp.FormData()
        data.add_field('image', media_data,
                       filename=filename,
                       content_type=mime_type)

        # Upload media
        upload_url = f"{self.base_url}/upload/image"
        async with self.get_comfyui_session() as session:
            async with session.post(upload_url, data=data) as response:
                if response.status != 200:
                    raise Exception(f"Upload media failed: HTTP {response.status}")

                # Get upload result
                result = await response.json()
                return result.get('name', '')

    async def _apply_params_to_workflow(self, workflow_data: Dict[str, Any], metadata: WorkflowMetadata, params: Dict[str, Any]) -> Dict[str, Any]:
        """Apply parameters to workflow using new parser"""
        workflow_data = copy.deepcopy(workflow_data)

        # Iterate through all parameter mappings
        for mapping in metadata.mapping_info.param_mappings:
            param_name = mapping.param_name

            # Check if parameter exists
            if param_name in params:
                param_value = params[param_name]
                await self._apply_param_mapping(workflow_data, mapping, param_value)
            else:
                # Use default value (if exists)
                if param_name in metadata.params:
                    param_info = metadata.params[param_name]
                    if param_info.default is not None:
                        await self._apply_param_mapping(workflow_data, mapping, param_info.default)
                    elif param_info.required:
                        raise Exception(f"Required parameter '{param_name}' is missing")

        return workflow_data

    def _extract_output_nodes(self, metadata: WorkflowMetadata) -> Dict[str, str]:
        """Extract output nodes and their output variable names from metadata"""
        output_id_2_var = {}

        for output_mapping in metadata.mapping_info.output_mappings:
            output_id_2_var[output_mapping.node_id] = output_mapping.output_var

        return output_id_2_var

    def get_workflow_metadata(self, workflow_file: str) -> Optional[WorkflowMetadata]:
        """Get workflow metadata (using new parser)"""
        parser = WorkflowParser()
        return parser.parse_workflow_file(workflow_file)

    def _split_media_by_suffix(self, node_output: Dict[str, Any], base_url: str) -> Tuple[List[str], List[str], List[str]]:
        """Split media by file extension into images/videos/audios"""
        image_exts = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff'}
        video_exts = {'.mp4', '.mov', '.avi', '.webm', '.gif'}
        audio_exts = {'.mp3', '.wav', '.flac', '.ogg', '.aac', '.m4a', '.wma', '.opus'}

        images = []
        videos = []
        audios = []

        for media_key in ("images", "gifs", "audio"):
            for media_data in node_output.get(media_key, []):
                filename = media_data.get("filename")
                subfolder = media_data.get("subfolder", "")
                media_type = media_data.get("type", "output")

                url = f"{base_url}/view?filename={filename}"
                if subfolder:
                    url += f"&subfolder={subfolder}"
                if media_type:
                    url += f"&type={media_type}"

                ext = os.path.splitext(filename)[1].lower()
                if ext in image_exts:
                    images.append(url)
                elif ext in video_exts:
                    videos.append(url)
                elif ext in audio_exts:
                    audios.append(url)

        return images, videos, audios

    def _map_outputs_by_var(self, output_id_2_var: Dict[str, str], output_id_2_media: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """Map outputs by variable name"""
        result = {}
        for node_id, media_data in output_id_2_media.items():
            # If there is an explicit variable name, use it, otherwise use node_id
            var_name = output_id_2_var.get(node_id, str(node_id))
            result[var_name] = media_data
        return result

    def _extend_flat_list_from_dict(self, media_dict: Dict[str, List[str]]) -> List[str]:
        """Flatten all lists in the dictionary into a single list"""
        flat = []
        for items in media_dict.values():
            flat.extend(items)
        return flat
