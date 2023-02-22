# static-sox

[![Linting](../../actions/workflows/lint.yml/badge.svg)](../../actions/workflows/lint.yml)

[![MacOS_Tests](../../actions/workflows/push_macos.yml/badge.svg)](../../actions/workflows/push_macos.yml)
[![Ubuntu_Tests](../../actions/workflows/push_ubuntu.yml/badge.svg)](../../actions/workflows/push_ubuntu.yml)
[![Win_Tests](../../actions/workflows/push_win.yml/badge.svg)](../../actions/workflows/push_win.yml)

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

# About

Installs sox binaries and allows you to use them in your python code.

# Development

To develop software, run `. ./activate.sh`

# Windows

This environment requires you to use `git-bash`.

# Linting

Run `./lint.sh` to find linting errors using `pylint`, `flake8` and `mypy`.
