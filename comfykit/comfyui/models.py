from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ExecuteResult(BaseModel):
    """Execution result model"""
    status: str = Field(description="Execution status")
    prompt_id: Optional[str] = Field(None, description="Prompt ID")
    duration: Optional[float] = Field(None, description="Execution duration (in seconds)")
    images: List[str] = Field(default_factory=list, description="List of image URLs")
    images_by_var: Dict[str, List[str]] = Field(default_factory=dict, description="Images grouped by variable name")
    audios: List[str] = Field(default_factory=list, description="List of audio URLs")
    audios_by_var: Dict[str, List[str]] = Field(default_factory=dict, description="Audios grouped by variable name")
    videos: List[str] = Field(default_factory=list, description="List of video URLs")
    videos_by_var: Dict[str, List[str]] = Field(default_factory=dict, description="Videos grouped by variable name")
    texts: List[str] = Field(default_factory=list, description="List of texts")
    texts_by_var: Dict[str, List[str]] = Field(default_factory=dict, description="Texts grouped by variable name")
    outputs: Optional[Dict[str, Any]] = Field(None, description="Raw outputs")
    msg: Optional[str] = Field(None, description="Message")

