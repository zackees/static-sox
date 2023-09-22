# static-sox

[![MacOS_Tests](../../actions/workflows/push_macos.yml/badge.svg)](../../actions/workflows/push_macos.yml)
[![Ubuntu_Tests](../../actions/workflows/push_ubuntu.yml/badge.svg)](../../actions/workflows/push_ubuntu.yml)
[![Win_Tests](../../actions/workflows/push_win.yml/badge.svg)](../../actions/workflows/push_win.yml)
[![Linting](../../actions/workflows/lint.yml/badge.svg)](../../actions/workflows/lint.yml)

Installs sox binaries and allows you to use them in your python code.

# Usage

Outside of python, static_sox can be used to access the library.

```bash
> pip install static-sox
> static_sox  # static_sox will pass all args to sox
```

Inside python, you can just add the paths (which will trigger a download) then use sox as you
normally would.

```python
import static_sox
import os
static_sox.add_paths(weak=True)  # Only install if sox is not available.
# static_sox.add_paths()  # Sox is installed unconditionally.
os.system("sox --help")
```

# Why

Deploying binaries is a pain. This library makes it not-your-problem. Now you can make a tool that uses sox backend and distribute it easily.

As of now, binaries are available for:

# Development

To develop software, run `. ./activate.sh`

# Windows

This environment requires you to use `git-bash`.

# Linting

Run `./lint.sh` to find linting errors using `pylint`, `flake8` and `mypy`.

# Release

  * 1.0.1: Improve readme.
  * 1.0.0: Initial release. All builds pass.
