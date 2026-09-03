#!/usr/bin/env bash
set -euo pipefail

rm -rf dist
mkdir -p dist/assets

cp index.html dist/index.html
cp -R assets/. dist/assets/

python3 transform_site.py dist/index.html

test -s dist/assets/logo-gestion-administrativa.webp
test -s dist/assets/mauro-montalvo-traje.webp
grep -q '/assets/logo-gestion-administrativa.webp?v=6' dist/index.html
grep -q '/assets/mauro-montalvo-traje.webp?v=7' dist/index.html

printf 'OK: dist contiene el logo y la única fotografía de Mauro, con traje.\n'
