"""
add_paths() Adds sox to the path, overriding any system sox.
remove_paths() Removes sox from the path.
"""

import os
import shutil

from .run import get_or_fetch_platform_executables_else_raise


def _has(name: str) -> bool:
    """Check if the path has the name"""
    return shutil.which(name) is not None


def add_paths(weak=False) -> bool:
    """Add the sox executable to the path"""
    if weak and _has("sox"):
        return False
    sox_exe = get_or_fetch_platform_executables_else_raise()
    os.environ["PATH"] = os.pathsep.join([os.path.dirname(sox_exe), os.environ["PATH"]])
    return True


def remove_paths() -> None:
    """Remove the sox executable from the path"""
    sox_exe = get_or_fetch_platform_executables_else_raise()
    install_dir = os.path.dirname(sox_exe)
    os.environ["PATH"] = os.pathsep.join(
        [x for x in os.environ["PATH"].split(os.pathsep) if x != install_dir]
    )
    # NOTE in addition to adding sox to the PATH variable, add_paths()
    # also sets the LD_PRELOAD variable to include all the dependencies
    # of the sox executable. We remove these dependencies from the
    # LD_PRELOAD variable below.
    deps = [
        "libbz2.so.1.0",
        "libgomp.so.1",
        "libgsm.so.1",
        "libltdl.so.7",
        "liblzma.so.5",
        "libm.so.6",
        "libmagic.so.1",
        "libpng16.so.16",
        "libpthread.so.0",
        "libsox.so.3",
        "libz.so.1",
    ]
    os.environ["LD_PRELOAD"] = os.pathsep.join(
        [x for x in os.environ.get("LD_PRELOAD", "").split(os.pathsep) if x not in deps]
    )
