import asyncio
import os
import time
from typing import Any, Dict, List, Optional

from comfykit.comfyui.base_executor import MEDIA_UPLOAD_NODE_TYPES, ComfyUIExecutor
from comfykit.comfyui.models import ExecuteResult
from comfykit.comfyui.runninghub_client import RunningHubClient
from comfykit.logger import logger
from comfykit.utils.file_util import download_files


class RunningHubExecutor(ComfyUIExecutor):
    """RunningHub executor for executing workflows on RunningHub cloud platform"""

    def __init__(self, base_url: str = None, api_key: str = None, timeout: int = 300, retry_count: int = 3):
        """Initialize RunningHub executor
        
        Args:
            base_url: RunningHub API base URL (optional)
            api_key: RunningHub API key (optional)
            timeout: Task timeout in seconds (default: 300)
            retry_count: API retry count (default: 3)
        """
        # For RunningHub, base_url is the API base URL
        super().__init__(base_url or "https://www.runninghub.ai", api_key=api_key)
        self.timeout = timeout
        self.retry_count = retry_count
        self.client = RunningHubClient(api_key=api_key, base_url=base_url, timeout=timeout, retry_count=retry_count)

    async def execute_by_id(self, workflow_id: str, params: Dict[str, Any] = None) -> ExecuteResult:
        """Execute workflow on RunningHub platform by workflow ID directly
        
        Supports unified simple parameter format like local ComfyUI!
        Automatically fetches workflow definition and does parameter mapping.
        
        Args:
            workflow_id: RunningHub workflow ID (numeric string)
            params: Workflow parameters in SIMPLE format (same as local ComfyUI)
                   Example: {"prompt": "a cat", "seed": 42}
                   
        Returns:
            Execution result
        """
        try:
            start_time = asyncio.get_event_loop().time()

            logger.info(f"Starting RunningHub workflow execution: workflow_id={workflow_id}")

            # Fetch workflow definition from RunningHub API
            logger.info(f"Fetching workflow definition for workflow_id={workflow_id}")
            workflow_json = await self.client.get_workflow_json(workflow_id)
            
            # Apply seed randomization (consistent with local ComfyUI behavior)
            workflow_json, seed_changes = self._randomize_seed_in_workflow(workflow_json)
            
            # Parse workflow to get metadata for parameter mapping
            from comfykit.comfyui.workflow_parser import WorkflowParser
            parser = WorkflowParser()
            metadata = parser.parse_workflow(workflow_json, f"workflow_{workflow_id}")
            
            if not metadata:
                return ExecuteResult(status="error", msg="Failed to parse workflow metadata")
            
            # Store workflow_id in metadata
            metadata.workflow_id = workflow_id
            metadata.is_runninghub = True
            
            logger.info(f"Workflow parsed successfully: {len(metadata.params)} parameters found")

            # Convert simple parameters to RunningHub nodeInfoList format using metadata
            node_info_list = await self._convert_params_to_node_info_list(metadata, params or {}, seed_changes)
            
            # Extract output node information from metadata
            output_id_2_var = self._extract_output_nodes(metadata)

            # Create task on RunningHub
            task_data = await self.client.create_task(workflow_id, node_info_list if node_info_list else None)
            task_id = task_data.get('taskId')

            if not task_id:
                return ExecuteResult(status="error", msg="Failed to create RunningHub task")

            logger.info(f"RunningHub task created: {task_id}")

            # Wait for task completion with output mapping
            result = await self._wait_for_task_completion(task_id, output_id_2_var)

            # Calculate execution time
            end_time = asyncio.get_event_loop().time()
            duration = end_time - start_time
            result.duration = duration

            return result

        except Exception as e:
            logger.error(f"RunningHub workflow execution failed: {e}", exc_info=True)
            return ExecuteResult(status="error", msg=f"RunningHub execution failed: {str(e)}")

    async def execute_workflow(self, workflow_file: str, params: Dict[str, Any] = None) -> ExecuteResult:
        """Execute workflow on RunningHub platform
        
        Args:
            workflow_file: Local workflow file path (for RunningHub, this contains workflow_id)
            params: Workflow parameters
            
        Returns:
            Execution result
        """
        try:
            start_time = asyncio.get_event_loop().time()

            if not os.path.exists(workflow_file):
                logger.error(f"Workflow file does not exist: {workflow_file}")
                return ExecuteResult(status="error", msg=f"Workflow file does not exist: {workflow_file}")

            # Load workflow JSON and apply seed randomization
            import json
            with open(workflow_file, 'r', encoding='utf-8') as f:
                workflow_json = json.load(f)
            
            # Apply seed randomization (consistent with local ComfyUI behavior)
            workflow_json, seed_changes = self._randomize_seed_in_workflow(workflow_json)
            
            # Parse workflow to get metadata
            from pathlib import Path
            from comfykit.comfyui.workflow_parser import WorkflowParser
            parser = WorkflowParser()
            metadata = parser.parse_workflow(workflow_json, Path(workflow_file).stem)
            
            if not metadata:
                return ExecuteResult(status="error", msg="Cannot parse workflow metadata")

            # For RunningHub workflows, get the workflow_id from metadata
            workflow_id = metadata.workflow_id
            if not workflow_id:
                return ExecuteResult(status="error", msg="RunningHub workflow_id not found in metadata")

            logger.info(f"Starting RunningHub workflow execution: workflow_id={workflow_id}")

            # Convert parameters to RunningHub nodeInfoList format
            node_info_list = await self._convert_params_to_node_info_list(metadata, params or {}, seed_changes)

            # Create task on RunningHub
            task_data = await self.client.create_task(workflow_id, node_info_list if node_info_list else None)
            task_id = task_data.get('taskId')

            if not task_id:
                return ExecuteResult(status="error", msg="Failed to create RunningHub task")

            logger.info(f"RunningHub task created: {task_id}")

            # Extract output node information from metadata
            output_id_2_var = self._extract_output_nodes(metadata)

            # Wait for task completion
            result = await self._wait_for_task_completion(task_id, output_id_2_var)

            # Calculate execution time
            end_time = asyncio.get_event_loop().time()
            duration = end_time - start_time
            result.duration = duration

            return result

        except Exception as e:
            logger.error(f"RunningHub workflow execution failed: {e}", exc_info=True)
            return ExecuteResult(status="error", msg=f"RunningHub execution failed: {str(e)}")


    async def _convert_params_to_node_info_list(self, metadata, params: dict, seed_changes: Dict[str, int] = None) -> List[dict]:
        """Convert parameters to RunningHub nodeInfoList format
        
        Upload handling logic:
        - Check need_upload flag (from DSL ~marker)
        - Check node_class_type in MEDIA_UPLOAD_NODE_TYPES (backward compatibility)
        
        Seed handling:
        - Randomized seeds (from seed=0) are passed via seed_changes
        """
        node_info_list = []
        seed_changes = seed_changes or {}

        # Process parameter mappings from metadata
        for param_mapping in metadata.mapping_info.param_mappings:
            param_name = param_mapping.param_name

            if param_name in params:
                param_value = params[param_name]
                node_class_type = param_mapping.node_class_type
                need_upload = param_mapping.need_upload

                # Follow the same upload logic as base_executor
                # Priority 1: Check DSL upload marker (~)
                if need_upload:
                    param_value = await self._handle_runninghub_media_upload(param_value)
                # Priority 2: Check if node type needs special media upload handling (backward compatibility)
                elif node_class_type in MEDIA_UPLOAD_NODE_TYPES:
                    param_value = await self._handle_runninghub_media_upload(param_value)

                # Create nodeInfo entry
                node_info = {
                    "nodeId": param_mapping.node_id,
                    "fieldName": param_mapping.input_field,
                    "fieldValue": param_value
                }
                node_info_list.append(node_info)
                logger.debug(f"Added nodeInfo: {node_info}")
        
        # Add randomized seeds that weren't overridden by user params
        # This ensures seed=0 randomization works for RunningHub
        for node_id, seed_value in seed_changes.items():
            # Check if this seed was already set by user params
            already_set = any(
                ni["nodeId"] == node_id and ni["fieldName"] == "seed" 
                for ni in node_info_list
            )
            if not already_set:
                node_info = {
                    "nodeId": node_id,
                    "fieldName": "seed",
                    "fieldValue": seed_value
                }
                node_info_list.append(node_info)
                logger.debug(f"Added randomized seed: node {node_id} = {seed_value}")

        return node_info_list

    async def _handle_runninghub_media_upload(self, param_value: Any) -> Any:
        """Handle media upload for RunningHub"""
        if isinstance(param_value, str):
            # Handle URL
            if param_value.startswith(('http://', 'https://')):
                try:
                    media_value = await self._upload_media_from_url(param_value)
                    logger.info(f"Media upload successful (URL): {media_value}")
                    return media_value
                except Exception as e:
                    logger.error(f"Media upload failed: {str(e)}")
                    raise Exception(f"Media upload failed: {str(e)}")
            # Handle local file path
            elif os.path.exists(param_value):
                try:
                    uploaded_filename = await self.client.upload_file(param_value)
                    logger.info(f"Media upload successful (local file): {uploaded_filename}")
                    return uploaded_filename
                except Exception as e:
                    logger.error(f"Failed to upload local file {param_value}: {str(e)}")
                    raise Exception(f"Failed to upload local file: {str(e)}")

        # Other cases (already a fileName or doesn't need upload)
        return param_value

    async def _upload_media_from_url(self, media_url: str) -> str:
        """Upload media from URL to RunningHub"""
        try:
            # Download the file first
            async with download_files(media_url) as temp_file_path:
                # Upload to RunningHub and get fileName
                result = await self.client.upload_file(temp_file_path)
                return result
        except Exception as e:
            logger.error(f"Failed to upload media from URL {media_url}: {e}")
            raise

    async def _download_text_from_url(self, text_url: str) -> str:
        """Download text content from URL"""
        try:
            async with self.get_comfyui_session() as session:
                async with session.get(text_url) as response:
                    if response.status != 200:
                        raise Exception(f"Download text failed: HTTP {response.status}")

                    # Get text content
                    text_content = await response.text()
                    return text_content.strip()

        except Exception as e:
            logger.error(f"Failed to download text from URL {text_url}: {e}")
            raise


    async def _wait_for_task_completion(self, task_id: str, output_id_2_var: Optional[Dict[str, str]] = None, max_wait_time: int = None) -> ExecuteResult:
        """Wait for RunningHub task completion and return results"""
        max_wait_time = max_wait_time or self.timeout
        check_interval = 2
        start_time = time.time()

        logger.info(f"Waiting for RunningHub task completion: {task_id}")

        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time >= max_wait_time:
                break

            try:
                # Query task status
                task_status = await self.client.query_task_status(task_id)
                logger.debug(f"Task {task_id} status: {task_status}")

                # RunningHub API only returns: ["QUEUED","RUNNING","FAILED","SUCCESS"]
                if task_status == 'SUCCESS':
                    # Task completed - get results
                    result_data = await self.client.query_task_result(task_id)
                    return await self._process_task_result(task_id, result_data, output_id_2_var)

                elif task_status == 'FAILED':
                    # Task failed
                    return ExecuteResult(
                        status="error",
                        prompt_id=task_id,
                        msg="RunningHub task failed"
                    )

                elif task_status in ['QUEUED', 'RUNNING']:
                    # Task still in progress - wait and check again
                    logger.info(f"Task {task_id} status: {task_status}, waiting...")
                    await asyncio.sleep(check_interval)
                    continue

            except Exception as e:
                logger.error(f"Error checking task status {task_id}: {e}")
                await asyncio.sleep(check_interval)
                continue

        # Timeout
        return ExecuteResult(
            status="error",
            prompt_id=task_id,
            msg=f"RunningHub task timeout after {max_wait_time} seconds"
        )

    async def _process_task_result(self, task_id: str, result_data: List[Dict[str, Any]], output_id_2_var: Optional[Dict[str, str]] = None) -> ExecuteResult:
        """Process RunningHub task result and convert to ExecuteResult format"""
        try:
            # Initialize result
            result = ExecuteResult(
                status="completed",
                prompt_id=task_id
            )

            # Handle different result_data formats
            logger.debug(f"Processing result_data type: {type(result_data)}, data: {result_data}")

            # Collect all images, videos, audios and texts outputs by node_id (simulated)
            # For RunningHub, we don't have actual node_id info, so we'll use indices or default keys
            output_id_2_images = {}
            output_id_2_videos = {}
            output_id_2_audios = {}
            output_id_2_texts = {}

            # RunningHub API may return result_data as a list or dict
            # If it's a list, process each item
            for idx, item in enumerate(result_data):
                if isinstance(item, dict):
                    file_url = item.get('fileUrl')
                    file_type = item.get('fileType', '').lower()

                    # Use node_id from item if available, otherwise use index as fallback
                    node_id = item.get('nodeId', str(idx))

                    if file_url:
                        if file_type in ['png', 'jpg', 'jpeg', 'gif', 'webp'] or 'image' in file_type:
                            if node_id not in output_id_2_images:
                                output_id_2_images[node_id] = []
                            output_id_2_images[node_id].append(file_url)
                        elif file_type in ['mp4', 'avi', 'mov', 'mkv'] or 'video' in file_type:
                            if node_id not in output_id_2_videos:
                                output_id_2_videos[node_id] = []
                            output_id_2_videos[node_id].append(file_url)
                        elif file_type in ['mp3', 'wav', 'flac'] or 'audio' in file_type:
                            if node_id not in output_id_2_audios:
                                output_id_2_audios[node_id] = []
                            output_id_2_audios[node_id].append(file_url)
                        elif file_type in ['txt', 'text', 'json', 'xml'] or 'text' in file_type:
                            # For text files, we need to download the content instead of storing the URL
                            try:
                                text_content = await self._download_text_from_url(file_url)
                                if node_id not in output_id_2_texts:
                                    output_id_2_texts[node_id] = []
                                output_id_2_texts[node_id].append(text_content)
                            except Exception as e:
                                logger.error(f"Failed to download text from URL {file_url}: {e}")
                                # Skip this text output if download fails
                                continue
                        else:
                            # Log warning for unknown file types instead of defaulting to images
                            logger.warning(f"Unknown file type '{file_type}' for URL {file_url} from node {node_id}. Skipping this output.")

            # If there is a mapping, map by variable name (following HTTP executor pattern)
            if output_id_2_images:
                result.images_by_var = self._map_outputs_by_var(output_id_2_var or {}, output_id_2_images)
                result.images = self._extend_flat_list_from_dict(result.images_by_var)

            if output_id_2_videos:
                result.videos_by_var = self._map_outputs_by_var(output_id_2_var or {}, output_id_2_videos)
                result.videos = self._extend_flat_list_from_dict(result.videos_by_var)

            if output_id_2_audios:
                result.audios_by_var = self._map_outputs_by_var(output_id_2_var or {}, output_id_2_audios)
                result.audios = self._extend_flat_list_from_dict(result.audios_by_var)

            # Process texts/texts_by_var
            if output_id_2_texts:
                result.texts_by_var = self._map_outputs_by_var(output_id_2_var or {}, output_id_2_texts)
                result.texts = self._extend_flat_list_from_dict(result.texts_by_var)

            # Store raw data for debugging
            result.outputs = {
                "raw_data": result_data
            }

            logger.info(f"RunningHub task {task_id} completed successfully: {len(result.images)} images, {len(result.videos)} videos, {len(result.audios)} audios, {len(result.texts)} texts")

            return result

        except Exception as e:
            logger.error(f"Failed to process RunningHub task result {task_id}: {e}")
            return ExecuteResult(
                status="error",
                prompt_id=task_id,
                msg=f"Failed to process task result: {str(e)}"
            )
