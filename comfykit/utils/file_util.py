import mimetypes
import os
import tempfile
from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator, List, Union, overload
from urllib.parse import urlparse

import aiohttp

from comfykit.logger import logger
from comfykit.utils.os_util import get_data_path


@overload
async def download_files(file_urls: str, suffix: str = None, auto_cleanup: bool = True, cookies: dict = None) -> AsyncGenerator[str, None]:
    ...


@overload
async def download_files(file_urls: List[str], suffix: str = None, auto_cleanup: bool = True, cookies: dict = None) -> AsyncGenerator[List[str], None]:
    ...


@asynccontextmanager
async def download_files(file_urls: Union[str, List[str]], suffix: str = None, auto_cleanup: bool = True, cookies: dict = None) -> AsyncGenerator[Union[str, List[str]], None]:
    """
    Download files from URLs to temporary files.
    
    Args:
        file_urls: Single URL string or URL list
        suffix: Temporary file suffix, if not specified, try to infer from URL
        auto_cleanup: Whether to automatically clean up temporary files, default is True
        cookies: Cookies used when requesting
        
    Yields:
        str: If input is str, return temporary file path
        List[str]: If input is List[str], return temporary file path list
        
    Automatically clean up all temporary files
    """
    is_single_url = isinstance(file_urls, str)
    url_list = [file_urls] if is_single_url else file_urls

    temp_file_paths = []
    try:
        for url in url_list:
            logger.info(f"Downloading file from URL: {url}")

            # Download external file using asynchronous HTTP client
            parsed_url = urlparse(url)
            file_content, content_type = await _download_external_file(url, cookies)

            # Determine file suffix
            file_suffix = suffix
            if not file_suffix:
                # Try to infer suffix from URL
                filename = os.path.basename(parsed_url.path)
                if filename and '.' in filename:
                    file_suffix = '.' + filename.split('.')[-1]
                else:
                    # If the extension cannot be obtained from the URL path, try to get it from the response header
                    file_suffix = get_ext_from_content_type(content_type or '')
                    if not file_suffix:
                        file_suffix = '.tmp'  # Default suffix

            with tempfile.NamedTemporaryFile(delete=False, suffix=file_suffix) as temp_file:
                temp_file.write(file_content)
                temp_file.flush()
                os.fsync(temp_file.fileno())
                temp_file_paths.append(temp_file.name)

        logger.info(f"Downloaded {len(temp_file_paths)} files to temporary files")

        # Return corresponding type based on input type
        if is_single_url:
            yield temp_file_paths[0]
        else:
            yield temp_file_paths

    except aiohttp.ClientError as e:
        logger.error(f"Download file failed: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error occurred while processing files: {str(e)}")
        raise
    finally:
        if auto_cleanup:
            cleanup_temp_files(temp_file_paths)


def get_ext_from_content_type(content_type: str) -> str:
    """Get file extension from Content-Type response header"""
    if not content_type:
        return ""

    # Parse Content-Type, remove parameters
    mime_type = content_type.split(';')[0].strip()

    # Use standard library's mimetypes.guess_extension
    ext = mimetypes.guess_extension(mime_type)

    # Optimize some common extensions (mimetypes sometimes returns uncommon ones)
    if ext:
        # Optimize JPEG extension
        if mime_type == 'image/jpeg' and ext in ['.jpe', '.jpeg']:
            ext = '.jpg'
        # Optimize TIFF extension
        elif mime_type == 'image/tiff' and ext == '.tiff':
            ext = '.tif'

        logger.debug(f"Get extension from Content-Type '{content_type}': {ext}")
        return ext
    else:
        logger.debug(f"Unknown Content-Type: {content_type}")
        return ""


async def _download_external_file(url: str, cookies: dict = None) -> tuple[bytes, str]:
    """Download external file using asynchronous HTTP client"""
    async with aiohttp.ClientSession(cookies=cookies, timeout=aiohttp.ClientTimeout(total=30)) as session:
        async with session.get(url) as response:
            response.raise_for_status()
            content = await response.read()
            content_type = response.headers.get('Content-Type', '')
            return content, content_type


def cleanup_temp_files(file_paths: Union[str, List[str]]) -> None:
    """
    Clean up temporary files.
    
    Args:
        file_paths: Single file path or file path list
    """
    if isinstance(file_paths, str):
        file_paths = [file_paths]

    for file_path in file_paths:
        if os.path.exists(file_path):
            try:
                os.unlink(file_path)
                logger.debug(f"Cleaned up temporary file: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary file {file_path}: {str(e)}")
