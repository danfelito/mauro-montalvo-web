from pathlib import Path

path = Path("dist/index.html")
html = path.read_text(encoding="utf-8")

old_mark = '<div class="w-10 h-10 rounded-lg bg-gold flex items-center justify-center font-serif font-bold text-navy-950 text-xl">M</div>'
new_logo = '<img src="assets/logo-gestion.webp" alt="Gestión Administrativa en El Puerto de Veracruz" class="w-12 h-12 rounded-full object-contain bg-white/95 p-0.5 shadow-sm flex-shrink-0">'

solution_old = 'https://image.qwenlm.ai/public_source/215c317f-9eac-48d7-88a5-901add41d64d/1af5d26b1-b565-4604-a34a-93dac1048264.png'
solution_new = 'assets/mauro-traje.webp'

mark_count = html.count(old_mark)
solution_count = html.count(solution_old)

if mark_count != 2:
    raise SystemExit(f"Expected 2 logo placeholders, found {mark_count}")
if solution_count != 1:
    raise SystemExit(f"Expected 1 solution image, found {solution_count}")

html = html.replace(old_mark, new_logo)
html = html.replace(solution_old, solution_new)

path.write_text(html, encoding="utf-8")

# Final guard: fail the deploy instead of silently publishing an incomplete change.
verified = path.read_text(encoding="utf-8")
if verified.count('assets/logo-gestion.webp') != 2:
    raise SystemExit("Logo replacement verification failed")
if verified.count('assets/mauro-traje.webp') != 1:
    raise SystemExit("Mauro suit image replacement verification failed")
