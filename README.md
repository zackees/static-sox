# static-sox

[![Linting](../../actions/workflows/lint.yml/badge.svg)](../../actions/workflows/lint.yml)

[![MacOS_Tests](../../actions/workflows/push_macos.yml/badge.svg)](../../actions/workflows/push_macos.yml)
[![Ubuntu_Tests](../../actions/workflows/push_ubuntu.yml/badge.svg)](../../actions/workflows/push_ubuntu.yml)
[![Win_Tests](../../actions/workflows/push_win.yml/badge.svg)](../../actions/workflows/push_win.yml)

Installs sox binaries and allows you to use them in your python code.

# Usage

```bash
> pip install static-sox
> static_sox --help
```

```python
import static_sox
import os
static_sox.add_paths(weak=True)  # Only install if sox is not available.
os.system("sox --help")
```

# Without this library...

Your sox tool would have to rely on the user to install sox, with the right build settings to ensure your tool functions correctly. This is a major pain for sox based tools and this library solves this problem.

As of now, binaries are available for:

# Development

To develop software, run `. ./activate.sh`

# Windows

This environment requires you to use `git-bash`.

# Linting

Run `./lint.sh` to find linting errors using `pylint`, `flake8` and `mypy`.

# Release

  * 1.0.0: Initial release. All builds pass.
