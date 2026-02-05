#! /bin/bash

uv tool uninstall tserj
rm -r build dist *.egg-info
uv build
uv tool install --no-cache .
