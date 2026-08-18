from pathlib import Path
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else "dist/index.html")
s = path.read_text(encoding="utf-8")

# Paleta tomada del logotipo: azul marino, azul/cian, turquesa y naranja.
replacements = {
    "navy: { 50:'#f0f4fa', 100:'#dbe4f2', 200:'#b7c9e5', 300:'#8baad3', 400:'#5f89b8', 500:'#3d6a9a', 600:'#2d5280', 700:'#1a3a5c', 800:'#0f2744', 900:'#0a1f38', 950:'#061428' },": "navy: { 50:'#edf7ff', 100:'#d8efff', 200:'#b6e2ff', 300:'#7bcfff', 400:'#2fafe7', 500:'#0b88c9', 600:'#066ca8', 700:'#045083', 800:'#063b68', 900:'#032f57', 950:'#02255d' },",
    "steel: { 50:'#f8fafc', 100:'#f1f5f9', 200:'#e2e8f0', 300:'#cbd5e1', 400:'#94a3b8', 500:'#64748b', 600:'#475569', 700:'#334155', 800:'#1e293b', 900:'#0f172a' },": "steel: { 50:'#f4fbfc', 100:'#e5f5f7', 200:'#c9e8ec', 300:'#9bd3da', 400:'#60b4c1', 500:'#2e8e9c', 600:'#146d7b', 700:'#0b5865', 800:'#084652', 900:'#063943' },",
    "gold: '#c9a961'": "gold: '#ff6b00'",
    "#0f172a": "#063943",
    "#061428": "#02255d",
    "#c9a961": "#ff6b00",
    "#e0c07a": "#ff8a2a",
    "rgba(201,169,97,0.35)": "rgba(255,107,0,0.32)",
    "rgba(201,169,97,0.15)": "rgba(255,107,0,0.16)",
    "#0f2744": "#063b68",
    "#1a3a5c": "#045083",
    "#f0f4fa": "#edf7ff",
    "#f1f5f9": "#e5f5f7",
    "rgba(6,20,40,0.92)": "rgba(2,37,93,0.94)",
    "rgba(10,31,56,0.75)": "rgba(3,59,104,0.80)",
    "rgba(10,31,56,0.35)": "rgba(0,165,250,0.30)",
    "rgba(6,20,40,0.7)": "rgba(2,37,93,0.74)",
    "rgba(10,31,56,0.08)": "rgba(0,74,128,0.10)",
    "rgba(10,31,56,0.12)": "rgba(0,74,128,0.14)",
}
for old, new in replacements.items():
    s = s.replace(old, new)

header_old = '''    <a href="#hero" class="nav-logo flex items-center gap-3 text-white transition-colors">
      <div class="w-10 h-10 rounded-lg bg-gold flex items-center justify-center font-serif font-bold text-navy-950 text-xl">M</div>
      <div class="leading-tight">
        <div class="font-serif font-bold text-lg tracking-wide">Mauro J. Montalvo</div>
        <div class="text-xs tracking-[0.2em] uppercase opacity-80">Representación Empresarial · Veracruz</div>
      </div>
    </a>'''
header_new = '''    <a href="#hero" class="nav-logo flex items-center gap-3 text-white transition-colors min-w-0">
      <img src="assets/logo-gestion-administrativa.webp" alt="Gestión Administrativa Veracruz" class="w-24 h-24 lg:w-28 lg:h-28 object-contain flex-shrink-0 drop-shadow-xl" />
      <div class="leading-tight hidden xl:block">
        <div class="font-serif font-bold text-lg tracking-wide">Mauro J. Montalvo</div>
        <div class="text-xs tracking-[0.18em] uppercase opacity-80">Gestión Administrativa · Veracruz</div>
      </div>
    </a>'''
if header_old not in s:
    raise SystemExit("No se encontró el bloque original del logotipo en el encabezado")
s = s.replace(header_old, header_new, 1)
s = s.replace('class="max-w-7xl mx-auto px-6 lg:px-10 py-5 flex items-center justify-between"', 'class="max-w-7xl mx-auto px-6 lg:px-10 py-1 flex items-center justify-between"', 1)
s = s.replace('class="hidden lg:flex items-center gap-8"', 'class="hidden lg:flex items-center gap-5 xl:gap-7"', 1)

# Sustituir tanto la foto de perfil como la imagen corporativa del señor con traje.
profile_old = 'src="assets/mauro-1.webp" class="rounded-2xl shadow-2xl w-full h-[550px] object-cover"'
profile_new = 'src="assets/mauro-montalvo-traje.webp" alt="Mauro J. Montalvo" class="rounded-2xl shadow-2xl w-full h-[550px] object-cover object-center"'
if profile_old not in s:
    raise SystemExit("No se encontró la imagen original de perfil")
s = s.replace(profile_old, profile_new, 1)

solution_old = 'https://image.qwenlm.ai/public_source/215c317f-9eac-48d7-88a5-901add41d64d/1af5d26b1-b565-4604-a34a-93dac1048264.png'
if solution_old not in s:
    raise SystemExit("No se encontró la imagen corporativa original")
s = s.replace(solution_old, 'assets/mauro-montalvo-traje.webp', 1)

footer_mark = '<div class="w-10 h-10 rounded-lg bg-gold flex items-center justify-center font-serif font-bold text-navy-950 text-xl">M</div>'
s = s.replace(footer_mark, '<img src="assets/logo-gestion-administrativa.webp" alt="Gestión Administrativa Veracruz" class="w-20 h-20 object-contain flex-shrink-0" />')
s = s.replace('Representación Empresarial Veracruz', 'Gestión Administrativa Veracruz')

path.write_text(s, encoding="utf-8")

verified = path.read_text(encoding="utf-8")
if verified.count('assets/logo-gestion-administrativa.webp') < 2:
    raise SystemExit("Verificación del logotipo falló")
if verified.count('assets/mauro-montalvo-traje.webp') < 2:
    raise SystemExit("Verificación de la imagen de Mauro falló")
if "gold: '#ff6b00'" not in verified or "950:'#02255d'" not in verified:
    raise SystemExit("Verificación de paleta de colores falló")
print("Aplicados y verificados: logo grande, paleta del logotipo y foto real de Mauro.")
