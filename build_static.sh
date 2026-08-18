#!/usr/bin/env bash
set -euo pipefail

rm -rf dist
mkdir -p dist

cat source/index.parts/part*.b64 | base64 -d | gzip -dc > dist/index.html

EXPECTED_SHA256="1d16cc8392222c60b3da946eb199885516cedff640776967fa5c86220cb9356f"
ACTUAL_SHA256="$(sha256sum dist/index.html | awk '{print $1}')"
if [[ "$ACTUAL_SHA256" != "$EXPECTED_SHA256" ]]; then
  echo "ERROR: reconstructed index.html does not match the reviewed source" >&2
  exit 1
fi

cp -R assets dist/assets
printf 'Static site built from the verified original uploaded index.html\n'
