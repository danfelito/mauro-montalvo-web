#!/usr/bin/env bash
set -euo pipefail

rm -rf dist
mkdir -p dist/assets

# Usar directamente el sitio del repositorio. No reconstruir HTML ni assets desde source/.
cp index.html dist/index.html
cp -R assets/. dist/assets/

# Aplicar solo los cambios de marca y rutas sobre la copia que Render publicará.
python3 transform_site.py dist/index.html

# Validación estricta: Render no publica si falta cualquiera de los dos recursos.
test -s dist/assets/logo-gestion-administrativa.webp
test -s dist/assets/mauro-montalvo-traje.webp
grep -q '/assets/logo-gestion-administrativa.webp?v=4' dist/index.html
grep -q '/assets/mauro-montalvo-traje.webp?v=4' dist/index.html

printf 'OK: dist contiene HTML, logo y foto de Mauro.\n'
