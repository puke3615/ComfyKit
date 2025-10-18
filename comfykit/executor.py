"""ComfyKit - Unified API for executing ComfyUI workflows"""

import os
import re
import tempfile
from pathlib import Path
from typing import Any, Dict, Literal, Optional, Union

from comfykit.comfyui.http_executor import HttpExecutor
from comfykit.comfyui.models import ExecuteResult
from comfykit.comfyui.runninghub_executor import RunningHubExecutor
from comfykit.comfyui.websocket_executor import WebSocketExecutor
from comfykit.logger import logger
from comfykit.utils.file_util import download_files
from comfykit.utils.runninghub_util import is_runninghub_workflow


class ComfyKit:
    """ComfyUI Workflow Executor - Intelligent execution for any workflow source
    
    Automatically handles:
    - Local ComfyUI workflows (file paths)
    - RunningHub workflows (workflow IDs)
    - Remote workflows (URLs - downloads and executes)
    
    Examples:
        >>> kit = ComfyKit()
        >>> 
        >>> # Local workflow file
        >>> result = await kit.execute("workflow.json", {"prompt": "a cat"})
        >>> 
        >>> # RunningHub workflow ID
        >>> result = await kit.execute("12345", {"prompt": "a cat"})
        >>> 
        >>> # Remote workflow URL
        >>> result = await kit.execute("https://example.com/workflow.json")
    """

    def __init__(
        self,
        # ComfyUI configuration (local execution)
        comfyui_url: Optional[str] = None,
        executor_type: Literal["http", "websocket"] = "http",
        api_key: Optional[str] = None,
        cookies: Optional[str] = None,
        # RunningHub configuration (cloud execution)
        runninghub_url: Optional[str] = None,
        runninghub_api_key: Optional[str] = None,
        runninghub_timeout: int = 300,
        runninghub_retry_count: int = 3,
    ):
        """Initialize ComfyKit with flexible configuration
        
        ComfyKit supports two execution modes:
        1. Local ComfyUI - Execute on your local ComfyUI server
        2. RunningHub Cloud - Execute on RunningHub cloud platform
        
        Configuration Priority:
            Constructor parameters > Environment variables > Default values
        
        Args:
            # Local ComfyUI Settings
            comfyui_url: ComfyUI server base URL
                        Default: "http://127.0.0.1:8188"
                        Env var: COMFYUI_BASE_URL
                        Example: "http://my-server:8188"
            
            executor_type: Execution mode for local ComfyUI
                          Options: "http" (recommended) or "websocket"
                          Default: "http"
                          Env var: COMFYUI_EXECUTOR_TYPE
            
            api_key: API key for ComfyUI authentication (if required)
                    Default: None
                    Env var: COMFYUI_API_KEY
                    Note: Also used as RunningHub API key if runninghub_api_key is not set
            
            cookies: ComfyUI cookies for authentication
                    Default: None
                    Env var: COMFYUI_COOKIES
                    Formats supported:
                      - JSON string: '{"key": "value"}'
                      - Key-value pairs: "key1=value1; key2=value2"
                      - URL to fetch cookies from
            
            # RunningHub Cloud Settings
            runninghub_url: RunningHub API base URL
                           Default: "https://www.runninghub.ai"
                           Env var: RUNNINGHUB_BASE_URL
            
            runninghub_api_key: RunningHub API key for cloud execution
                               Default: None (falls back to api_key parameter)
                               Env var: RUNNINGHUB_API_KEY
                               Required for RunningHub workflow execution
            
            runninghub_timeout: Timeout for RunningHub task execution (seconds)
                               Default: 300 (5 minutes)
                               Env var: RUNNINGHUB_TIMEOUT
            
            runninghub_retry_count: Number of retries for RunningHub API requests
                                   Default: 3
                                   Env var: RUNNINGHUB_RETRY_COUNT
        
        Examples:
            # Example 1: Default configuration (local ComfyUI)
            >>> kit = ComfyKit()
            >>> # Connects to http://127.0.0.1:8188
            
            # Example 2: Custom ComfyUI server
            >>> kit = ComfyKit(comfyui_url="http://my-server:8188")
            
            # Example 3: With authentication
            >>> kit = ComfyKit(
            ...     comfyui_url="http://my-server:8188",
            ...     api_key="my-api-key",
            ...     cookies="session=abc123"
            ... )
            
            # Example 4: WebSocket mode
            >>> kit = ComfyKit(executor_type="websocket")
            
            # Example 5: RunningHub cloud execution
            >>> kit = ComfyKit(runninghub_api_key="rh-key-xxx")
            >>> # Can execute both local and cloud workflows
            
            # Example 6: Environment variables (recommended for production)
            >>> # Set in shell: export COMFYUI_BASE_URL="http://server:8188"
            >>> kit = ComfyKit()
            >>> # Automatically reads from environment
        """
        # ComfyUI configuration (priority: param > env > default)
        self.comfyui_url = comfyui_url or os.getenv("COMFYUI_BASE_URL", "http://127.0.0.1:8188")
        self.executor_type = executor_type or os.getenv("COMFYUI_EXECUTOR_TYPE", "http")
        self.api_key = api_key or os.getenv("COMFYUI_API_KEY")
        self.cookies = cookies or os.getenv("COMFYUI_COOKIES")
        
        # RunningHub configuration (priority: param > env > default)
        self.runninghub_url = runninghub_url or os.getenv("RUNNINGHUB_BASE_URL", "https://www.runninghub.ai")
        # If runninghub_api_key not set, fall back to api_key (for convenience)
        self.runninghub_api_key = runninghub_api_key or os.getenv("RUNNINGHUB_API_KEY") or self.api_key
        self.runninghub_timeout = runninghub_timeout if runninghub_timeout != 300 else int(os.getenv("RUNNINGHUB_TIMEOUT", "300"))
        self.runninghub_retry_count = runninghub_retry_count if runninghub_retry_count != 3 else int(os.getenv("RUNNINGHUB_RETRY_COUNT", "3"))
        
        # Normalize executor type
        self.executor_type = self.executor_type.lower()
        
        # Lazy initialization of executors
        self._http_executor = None
        self._websocket_executor = None
        self._runninghub_executor = None

    def _get_http_executor(self) -> HttpExecutor:
        """Get or create HTTP executor"""
        if self._http_executor is None:
            self._http_executor = HttpExecutor(
                base_url=self.comfyui_url,
                api_key=self.api_key,
                cookies=self.cookies
            )
        return self._http_executor

    def _get_websocket_executor(self) -> WebSocketExecutor:
        """Get or create WebSocket executor"""
        if self._websocket_executor is None:
            self._websocket_executor = WebSocketExecutor(
                base_url=self.comfyui_url,
                api_key=self.api_key,
                cookies=self.cookies
            )
        return self._websocket_executor

    def _get_runninghub_executor(self) -> RunningHubExecutor:
        """Get or create RunningHub executor"""
        if self._runninghub_executor is None:
            self._runninghub_executor = RunningHubExecutor(
                base_url=self.runninghub_url,
                api_key=self.runninghub_api_key,
                timeout=self.runninghub_timeout,
                retry_count=self.runninghub_retry_count
            )
        return self._runninghub_executor

    def _get_local_executor(self):
        """Get local ComfyUI executor based on executor_type"""
        if self.executor_type == "websocket":
            return self._get_websocket_executor()
        else:
            return self._get_http_executor()

    def _is_runninghub_workflow_id(self, workflow: str) -> bool:
        """Check if workflow is a RunningHub workflow ID
        
        RunningHub workflow IDs are numeric strings (e.g. "12345")
        """
        return workflow.isdigit()

    def _is_url(self, workflow: str) -> bool:
        """Check if workflow is a URL"""
        return workflow.startswith(('http://', 'https://'))

    def _is_file_path(self, workflow: str) -> bool:
        """Check if workflow is a file path"""
        return os.path.exists(workflow) or '/' in workflow or '\\' in workflow

    async def execute(
        self,
        workflow: Union[str, Path],
        params: Optional[Dict[str, Any]] = None,
    ) -> ExecuteResult:
        """Execute a ComfyUI workflow - intelligently handles any workflow source
        
        This method automatically detects the workflow type and uses the appropriate executor:
        - RunningHub workflow ID (numeric string like "12345")
        - Local file path (e.g. "workflow.json" or Path("workflow.json"))
        - Remote URL (e.g. "https://example.com/workflow.json")
        - RunningHub workflow file (contains _source: "runninghub")
        
        Args:
            workflow: Workflow source, can be:
                     - str: workflow_id (numeric) | file_path | url
                     - Path: file path object
            params: Workflow parameters in UNIFIED SIMPLE format (works for ALL workflow types!)
                   Example: {"prompt": "a cat", "seed": 42, "steps": 20}
                   
                   ComfyKit automatically handles parameter mapping:
                   - For local ComfyUI: applies params directly to workflow nodes
                   - For RunningHub: converts to nodeInfoList format internally
        
        Returns:
            ExecuteResult: Structured execution result
        
        Examples:
            >>> kit = ComfyKit()
            >>> 
            >>> # Example 1: Local workflow file
            >>> result = await kit.execute("workflow.json", {"prompt": "a cat"})
            >>> 
            >>> # Example 2: RunningHub workflow ID (same param format!)
            >>> result = await kit.execute("12345", {"prompt": "a cat", "seed": 42})
            >>> 
            >>> # Example 3: Remote workflow URL
            >>> result = await kit.execute(
            ...     "https://example.com/workflow.json",
            ...     {"prompt": "a cat"}
            ... )
            >>> 
            >>> # Example 4: Path object
            >>> from pathlib import Path
            >>> result = await kit.execute(Path("workflow.json"))
        """
        workflow_str = str(workflow)
        
        # Case 1: RunningHub workflow ID (numeric string)
        if self._is_runninghub_workflow_id(workflow_str):
            logger.info(f"Detected RunningHub workflow ID: {workflow_str}")
            executor = self._get_runninghub_executor()
            return await executor.execute_by_id(workflow_str, params or {})
        
        # Case 2: URL - download and execute as local workflow
        elif self._is_url(workflow_str):
            logger.info(f"Detected workflow URL: {workflow_str}")
            async with download_files(workflow_str) as temp_file_path:
                executor = self._get_local_executor()
                return await executor.execute_workflow(temp_file_path, params or {})
        
        # Case 3: File path (local or RunningHub workflow file)
        elif self._is_file_path(workflow_str):
            # Check if it's a RunningHub workflow file
            if os.path.exists(workflow_str) and is_runninghub_workflow(workflow_str):
                logger.info(f"Detected RunningHub workflow file: {workflow_str}")
                executor = self._get_runninghub_executor()
                return await executor.execute_workflow(workflow_str, params or {})
            else:
                # Local ComfyUI workflow
                logger.info(f"Detected local workflow file: {workflow_str}")
                executor = self._get_local_executor()
                return await executor.execute_workflow(workflow_str, params or {})
        
        # Case 4: Unknown format - try as file path
        else:
            logger.warning(f"Unknown workflow format: {workflow_str}, treating as file path")
            executor = self._get_local_executor()
            return await executor.execute_workflow(workflow_str, params or {})

    async def execute_json(
        self,
        workflow_json: Dict[str, Any],
        params: Optional[Dict[str, Any]] = None,
    ) -> ExecuteResult:
        """Execute a ComfyUI workflow from a JSON dict
        
        Args:
            workflow_json: Workflow definition as a dictionary
            params: Optional parameters to inject into the workflow
        
        Returns:
            ExecuteResult: Structured execution result
        
        Example:
            >>> workflow = {"nodes": [...], "edges": [...]}
            >>> result = await kit.execute_json(workflow, {"prompt": "a cat"})
        """
        import json
        import tempfile

        # Save to temp file and execute
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False
        ) as f:
            json.dump(workflow_json, f)
            temp_path = f.name

        try:
            result = await self.execute(temp_path, params)
        finally:
            # Clean up temp file
            Path(temp_path).unlink(missing_ok=True)

        return result

