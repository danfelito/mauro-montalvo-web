#!/usr/bin/env bash
set -euo pipefail

rm -rf dist
mkdir -p dist/assets

# Usar directamente el sitio del repositorio.
cp index.html dist/index.html
cp -R assets/. dist/assets/

# Aplicar solo branding y rutas sobre la copia que Render publicará.
python3 transform_site.py dist/index.html

# Validación estricta: Render no publica si falta cualquiera de los recursos.
test -s dist/assets/logo-gestion-administrativa.webp
test -s dist/assets/mauro-montalvo-traje.png
grep -q '/assets/logo-gestion-administrativa.webp?v=5' dist/index.html
grep -q '/assets/mauro-montalvo-traje.png?v=5' dist/index.html

printf 'OK: dist contiene HTML, logo y foto PNG de Mauro.\n'
