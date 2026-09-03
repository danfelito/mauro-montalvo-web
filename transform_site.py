from pathlib import Path
import sys

path = Path(sys.argv[1] if len(sys.argv) > 1 else "dist/index.html")
s = path.read_text(encoding="utf-8")

LOGO = "/assets/logo-gestion-administrativa.webp?v=6"
MAURO_TRAJE = "/assets/mauro-montalvo-traje.webp?v=7"

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

    # Voz institucional y textos comerciales
    "Mauro realiza visita, recopila información y entrega reporte con evidencias.": "Realizamos visita, recopilamos la información requerida y entregamos un reporte detallado con evidencias.",
    "Decisión informada sin desplazar personal propio a El Puerto de Veracruz.": "Recibe un reporte completo y preciso para que pueda tomar decisiones informadas, sin desplazar personal propio al Puerto de Veracruz.",
    "Cada empresa accede a un portal privado donde ve expedientes, avances, documentos, evidencias, tareas e informes. Ya no contratan simplemente a Mauro: contratan un <strong class=\"text-gold\">servicio profesional de representación con trazabilidad</strong>.": "Cada empresa cuenta con acceso a un portal privado donde puede consultar en tiempo real su expediente, avances, documentos, evidencias e informes, manteniendo toda la información organizada y disponible en un solo lugar.<br><br>Ofrecemos un <strong class=\"text-gold\">servicio profesional de representación con transparencia, trazabilidad y respaldo en cada etapa</strong>.",
    "Solicite su orientación inicial gratuita.": "Solicita tu orientación inicial gratuita.",
    "Videollamada de 15 minutos para entender su necesidad. Mauro recibe toda la información antes de la llamada.": "Agenda una videollamada de 15 minutos para conocer tu situación y entender tus necesidades. Antes de la llamada, nosotros recibiremos la información que nos proporciones.",
    "<h3 class=\"font-serif text-2xl font-bold text-navy-900 mb-2\">Solicitar orientación inicial</h3>": "<h3 class=\"font-serif text-2xl font-bold text-navy-900 mb-2\">¿Necesitas orientación? Contáctanos</h3>",
    "Cuéntenos lo que sepa. Todos los campos son opcionales y puede enviar el formulario incompleto.": "Puedes enviar la información aunque no completes todos los campos. La información proporcionada nos ayudará a brindarte una mejor orientación.",
    "Al responder, Mauro podrá proporcionarle un consejo inicial claro y práctico relacionado con su trámite o problema.": "Nuestro equipo analizará la información que compartas para ofrecerte una guía inicial precisa y orientada a tu caso o trámite.",
    "Cerramos y documentamos": "Cierre y documentación final",
    "Hola Mauro, solicito orientación inicial para una gestión en El Puerto de Veracruz.": "Hola, solicito orientación inicial para una gestión en El Puerto de Veracruz.",
    "Agradecería un consejo inicial claro y práctico relacionado con este trámite o problema.": "Agradecería una guía inicial clara y práctica relacionada con este trámite o problema.",
}
for old, new in replacements.items():
    s = s.replace(old, new)

header_old = '''    <a href="#hero" class="nav-logo flex items-center gap-3 text-white transition-colors">
      <div class="w-10 h-10 rounded-lg bg-gold flex items-center justify-center font-serif font-bold text-navy-950 text-xl">M</div>
      <div class="leading-tight">
        <div class="font-serif font-bold text-lg tracking-wide">Mauro J. Montalvo</div>
        <div class="text-xs tracking-[0.2em] uppercase opacity-80">Representación Empresarial · El Puerto de Veracruz</div>
      </div>
    </a>'''
header_new = f'''    <a href="#hero" class="nav-logo flex items-center gap-3 text-white transition-colors min-w-0">
      <img src="{LOGO}" alt="Gestión Administrativa en El Puerto de Veracruz" class="w-20 h-20 lg:w-24 lg:h-24 object-contain flex-shrink-0 drop-shadow-xl" />
      <div class="leading-tight hidden xl:block">
        <div class="font-serif font-bold text-lg tracking-wide">Mauro J. Montalvo</div>
        <div class="text-xs tracking-[0.18em] uppercase opacity-80">Gestión Administrativa · El Puerto de Veracruz</div>
      </div>
    </a>'''
if header_old not in s:
    raise SystemExit("No se encontró el bloque original del logotipo en el encabezado")
s = s.replace(header_old, header_new, 1)
s = s.replace('class="max-w-7xl mx-auto px-6 lg:px-10 py-5 flex items-center justify-between"', 'class="max-w-7xl mx-auto px-6 lg:px-10 py-2 flex items-center justify-between"', 1)
s = s.replace('class="hidden lg:flex items-center gap-8"', 'class="hidden lg:flex items-center gap-5 xl:gap-7"', 1)

footer_mark = '<div class="w-10 h-10 rounded-lg bg-gold flex items-center justify-center font-serif font-bold text-navy-950 text-xl">M</div>'
s = s.replace(footer_mark, f'<img src="{LOGO}" alt="Gestión Administrativa en El Puerto de Veracruz" class="w-16 h-16 object-contain flex-shrink-0" />')
s = s.replace('Representación Empresarial El Puerto de Veracruz', 'Gestión Administrativa · El Puerto de Veracruz')

path.write_text(s, encoding="utf-8")

verified = path.read_text(encoding="utf-8")
if verified.count(LOGO) < 2:
    raise SystemExit("Verificación del logotipo falló")
if verified.count(MAURO_TRAJE) < 1:
    raise SystemExit("Verificación de la imagen de Mauro con traje falló")
print("OK: branding y textos institucionales actualizados.")
