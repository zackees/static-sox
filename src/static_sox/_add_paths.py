"""
add_paths() Adds ffmpeg and ffprobe to the path, overriding any system ffmpeg/ffprobe.
"""

import os
import shutil

from .run import get_or_fetch_platform_executables_else_raise


def _has(name: str) -> bool:
    """Check if the path has the name"""
    return shutil.which(name) is not None


def add_paths(weak=False) -> bool:
    """Add the ffmpeg executable to the path"""
    if weak:
        has_sox = _has("sox") is not None
        if has_sox:
            return False
    sox_exe = get_or_fetch_platform_executables_else_raise()
    os.environ["PATH"] = os.pathsep.join([os.path.dirname(sox_exe), os.environ["PATH"]])
    return True
