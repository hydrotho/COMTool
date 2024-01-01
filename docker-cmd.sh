#!/usr/bin/env bash

pip install .

NUITKA_CACHE_DIR=".nuitka_cache" python -m nuitka --onefile --output-filename=COMTool src/comtool/__main__.py
