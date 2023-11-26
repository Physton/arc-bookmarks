#!/bin/bash
./venv/bin/pyinstaller main.py -F -n arc-bookmarks
chmod +x dist/arc-bookmarks