import base64
import os
from pathlib import Path

import comfykit

# Package installation path (for accessing package resources)
SRC_PATH = Path(comfykit.__file__).parent

def get_comfykit_root_path() -> str:
    """Get ComfyKit root path - current working directory"""
    return str(Path.cwd())

def get_root_path(*paths: str) -> str:
    """Get path relative to ComfyKit root path"""
    root_path = get_comfykit_root_path()
    if paths:
        return os.path.join(root_path, *paths)
    return root_path

def get_data_path(*paths: str) -> str:
    """Get path relative to ComfyKit root path data folder"""
    if paths:
        return get_root_path("data", *paths)
    return get_root_path("data")

def get_src_path(*paths: str) -> str:
    """Get path relative to package source (for accessing package resources)"""
    if paths:
        return os.path.join(SRC_PATH, *paths)
    return str(SRC_PATH)

def save_base64_to_file(base64_str, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(base64.b64decode(base64_str))
