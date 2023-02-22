"""
    Entry point for running the ffmpeg executable.
"""

import os
import stat
import subprocess
import sys
import zipfile
from datetime import datetime

import requests  # type: ignore
from filelock import FileLock, Timeout

TIMEOUT = 10 * 60  # Wait upto 10 minutes to validate install
# otherwise break the lock and install anyway.

SELF_DIR = os.path.abspath(os.path.dirname(__file__))
LOCK_FILE = os.path.join(SELF_DIR, "lock.file")


PLATFORM_ZIP_FILES = {
    "win32": "https://github.com/zackees/static-sox/raw/main/bin/sox-14.4.2-win32.zip",
    "darwin": "https://github.com/zackees/static-sox/raw/main/bin/sox-14.4.2-darwin.zip",
    "linux": "https://github.com/zackees/static-sox/raw/main/bin/sox-14.4.2-linux.zip",
}


def check_system():
    """Friendly error if there's a problem with the system configuration."""
    if sys.platform not in PLATFORM_ZIP_FILES:
        raise OSError(f"Please implement static-sox for {sys.platform}")


def get_platform_http_zip():
    """Return the download link for the current platform"""
    check_system()
    return PLATFORM_ZIP_FILES[sys.platform]


def get_bin_dir():
    """Either get the executable or raise an error"""
    check_system()
    return os.path.join(SELF_DIR, "bin")


def download_file(url, local_path):
    """Downloads a file to the give path."""
    # NOTE the stream=True parameter below
    print(f"Downloading {url} -> {local_path}")
    with requests.get(url, stream=True, timeout=60) as req:
        req.raise_for_status()
        with open(local_path, "wb") as file_d:
            for chunk in req.iter_content(chunk_size=8192 * 16):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                sys.stdout.write(".")
                file_d.write(chunk)
            sys.stdout.write(f"\nDownload of {url} -> {local_path} completed.\n")
    return local_path


def get_or_fetch_platform_executables_else_raise(
    fix_permissions=True,
) -> str:
    """Either get the executable or raise an error"""
    lock = FileLock(LOCK_FILE, timeout=TIMEOUT)  # pylint: disable=E0110
    try:
        with lock.acquire():
            return _get_or_fetch_platform_executables_else_raise_no_lock(
                fix_permissions=fix_permissions
            )
    except Timeout:
        sys.stderr.write(f"{__file__}: Warning, could not acquire lock at {LOCK_FILE}\n")
        return _get_or_fetch_platform_executables_else_raise_no_lock(
            fix_permissions=fix_permissions
        )


def _get_or_fetch_platform_executables_else_raise_no_lock(  # pylint: disable=too-many-locals
    fix_permissions=True,
) -> str:
    """Either get the executable or raise an error, internal api"""
    bin_dir = get_bin_dir()
    installed_crumb = os.path.join(bin_dir, "installed.crumb")
    if not os.path.exists(installed_crumb):
        # All zip files store their platform executables in a folder
        # like "win32" or "darwin" or "linux" inside the executable. So root
        # the install one level up from that same directory.
        os.makedirs(bin_dir, exist_ok=True)
        url = get_platform_http_zip()
        local_zip = os.path.join(bin_dir, sys.platform + ".zip")
        download_file(url, local_zip)
        print(f"Extracting {local_zip} -> {bin_dir}")
        with zipfile.ZipFile(local_zip, mode="r") as zipf:
            zipf.extractall(bin_dir)
        try:
            os.remove(local_zip)
        except OSError as err:
            print(f"{__file__}: Error could not remove {local_zip} because of {err}")
        with open(installed_crumb, "wt") as filed:  # pylint: disable=W1514
            filed.write(f"installed from {url} on {str(datetime.now())}")
    if sys.platform == "win32":
        sox_exe = os.path.join(bin_dir, "sox-14.4.2-win32", "sox.exe")
    elif sys.platform == "darwin":
        sox_exe = os.path.join(bin_dir, "sox-14.4.2-darwin", "sox")
    elif sys.platform == "linux":
        sox_exe = os.path.join(bin_dir, "sox-14.4.2-linux", "sox")
    else:
        raise OSError(f"Please implement static-sox for {sys.platform}")
    assert os.path.exists(sox_exe), f"Could not find sox executable at {sox_exe}"
    if (
        fix_permissions
        and sys.platform != "win32"
        and (not os.access(sox_exe, os.X_OK) or not os.access(sox_exe, os.R_OK))
    ):
        # Set bits for execution and read for all users.
        exe_bits = stat.S_IXOTH | stat.S_IXUSR | stat.S_IXGRP
        read_bits = stat.S_IRUSR | stat.S_IRGRP | stat.S_IXGRP
        os.chmod(sox_exe, exe_bits | read_bits)
        assert os.access(sox_exe, os.X_OK), f"Could not execute {sox_exe}"
        assert os.access(sox_exe, os.R_OK), f"Could not get read bits of {sox_exe}"
    if "linux" in sys.platform:
        # On linux, we need to set LD_PRELOAD to the directory
        # where the ffmpeg libraries are stored.
        prev_ld_library_path = os.environ.get("LD_PRELOAD", "")
        install_dir = os.path.dirname(sox_exe)
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
        ld_paths = [prev_ld_library_path]
        for dep in deps:
            ld_path = os.path.join(install_dir, dep)
            ld_paths.append(ld_path)
        ld_paths = [x for x in ld_paths if x]
        os.environ["LD_PRELOAD"] = os.pathsep.join(ld_paths)
    return sox_exe


def main_static_sox() -> None:
    """Entry point for running static_ffmpeg, which delegates to ffmpeg."""
    sox_exe = get_or_fetch_platform_executables_else_raise()
    rtn: int = subprocess.call([sox_exe] + sys.argv[1:])
    sys.exit(rtn)


def main_print_paths() -> None:
    """Entry point for printing ffmpeg paths"""
    sox_exe = get_or_fetch_platform_executables_else_raise()
    print(f"SOX={sox_exe}")
    sys.exit(0)


if __name__ == "__main__":
    sys.platform = "linux"
    get_or_fetch_platform_executables_else_raise()
