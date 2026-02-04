#! /bin/bash

uv tool uninstall streameast
rm -r build dist *.egg-info
uv build
uv tool install --no-cache .
