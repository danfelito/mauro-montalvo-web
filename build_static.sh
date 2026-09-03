#!/usr/bin/env bash
set -euo pipefail

rm -rf dist
mkdir -p dist/assets

cp index.html dist/index.html
cp compartir.html dist/compartir.html
cp -R assets/. dist/assets/

python3 transform_site.py dist/index.html

test -s dist/assets/logo-gestion-administrativa.webp
test -s dist/assets/mauro-montalvo-traje.webp
test -s dist/assets/whatsapp-montalvo.png
test -s dist/compartir.html
grep -q '/assets/logo-gestion-administrativa.webp?v=6' dist/index.html
grep -q '/assets/mauro-montalvo-traje.webp?v=7' dist/index.html
grep -q 'assets/whatsapp-montalvo.png' dist/compartir.html

printf 'OK: dist contiene el portal, compartir.html y la vista previa de WhatsApp.\n'
