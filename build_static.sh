#!/usr/bin/env bash
set -euo pipefail

rm -rf dist
mkdir -p dist

base64 -d source/index.html.gz.b64 | gzip -dc > dist/index.html
cp -R assets dist/assets

printf 'Static site built from the original uploaded index.html\n'
