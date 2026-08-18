#!/usr/bin/env bash
set -euo pipefail

rm -rf dist
mkdir -p dist/assets

# Restore the reviewed original page.
cat source/index.parts/part*.b64 | base64 -d | gzip -dc > dist/index.html
EXPECTED_SHA256="1d16cc8392222c60b3da946eb199885516cedff640776967fa5c86220cb9356f"
ACTUAL_SHA256="$(sha256sum dist/index.html | awk '{print $1}')"
if [[ "$ACTUAL_SHA256" != "$EXPECTED_SHA256" ]]; then
  echo "ERROR: reconstructed index.html does not match the reviewed source" >&2
  exit 1
fi

# Existing website assets.
cp -R assets/. dist/assets/

# Rebuild the approved branding assets committed as text-safe base64 chunks.
cat source/assets/logo/part*.b64 | base64 -d > dist/assets/logo-gestion.webp
cat source/assets/mauro2/part*.b64 | base64 -d > dist/assets/mauro-traje.webp

# Apply and verify the requested logo + Mauro suit-image substitutions.
python3 apply_branding.py

printf 'Static site built with verified logo and Mauro suit image\n'
