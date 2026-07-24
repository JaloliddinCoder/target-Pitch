import re
import subprocess
import os

html_path = "/Users/macstore.uz/Desktop/target_pitch/index.html"
handbook_path = "/Users/macstore.uz/Desktop/target_pitch/handbook.html"
pdf_path = "/Users/macstore.uz/Desktop/target_pitch/Target_Dual_Talim_Tizimi_Qollanma.pdf"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extract style definitions
style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
styles = style_match.group(1) if style_match else ""

# Extract all section.slide elements
slides = re.findall(r'<section class="slide.*?">(.*?)</section>', content, re.DOTALL)

# Build a continuous handbook HTML
handbook_css = """
:root{
  --base:#0F1533;
  --base2:#161E42;
  --surface:#1B2450;
  --surface2:#212B5C;
  --line:rgba(255,255,255,.12);
  --line2:rgba(255,255,255,.22);
  --text:#EEF1FA;
  --muted:#96A0CC;
  --turq:#3BC9C0;
  --saffron:#F0B23C;
  --madder:#E4645A;
  --disp:"Bricolage Grotesque",-apple-system,sans-serif;
  --body:"Manrope",-apple-system,sans-serif;
  --mono:"JetBrains Mono",ui-monospace,monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
body{
  background:var(--base);
  color:var(--text);
  font-family:var(--body);
  padding:30px 40px;
  -webkit-print-color-adjust: exact !important;
  print-color-adjust: exact !important;
}
@page {
  size: A4 portrait;
  margin: 12mm 15mm;
}
.page-section {
  page-break-inside: avoid;
  break-inside: avoid;
  margin-bottom: 30px;
  padding: 24px 28px;
  background: var(--base2);
  border: 1px solid var(--line);
  border-radius: 16px;
  position: relative;
}
.eyebrow {
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--turq);
  margin-bottom: 10px;
}
h1 { font-family: var(--disp); font-size: 38px; line-height: 1.1; margin-bottom: 14px; color: var(--text); }
h2 { font-family: var(--disp); font-size: 26px; line-height: 1.2; margin-bottom: 12px; color: var(--text); }
h3 { font-family: var(--disp); font-size: 19px; font-weight: 700; margin-bottom: 6px; }
p, .sub, .lede { font-size: 15px; line-height: 1.5; color: var(--muted); margin-bottom: 12px; }
.sub { font-size: 16px; color: var(--text); }
.lede { font-size: 17px; font-weight: 500; color: var(--text); }
.g2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 12px; }
.g3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 12px; }
.g4 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; margin-top: 12px; }
.g5, .g6 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; margin-top: 12px; }
.card, .stat, .kase {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 16px 18px;
}
.stat .n { font-family: var(--disp); font-size: 42px; font-weight: 800; color: var(--saffron); line-height: 1; }
.stat .n.t { color: var(--turq); }
.stat .l { font-size: 14px; color: var(--muted); margin-top: 4px; }
.kase .sinf { font-family: var(--disp); font-size: 24px; font-weight: 800; color: var(--turq); }
.kase .nm { font-family: var(--disp); font-size: 17px; font-weight: 700; margin-top: 4px; }
.kase .yo { font-family: var(--mono); font-size: 10px; color: var(--muted); margin-top: 2px; }
.kase .ish { font-size: 14px; margin-top: 8px; color: var(--text); }
.kase .res { font-size: 17px; font-weight: 800; color: var(--saffron); margin-top: 8px; border-top: 1px solid var(--line); padding-top: 6px; }
.person { display: flex; gap: 14px; align-items: center; background: var(--surface); padding: 12px 14px; border-radius: 12px; border: 1px solid var(--line); }
.person .photo { width: 56px; height: 56px; border-radius: 10px; overflow: hidden; flex: none; }
.person .photo img { width: 100%; height: 100%; object-fit: cover; }
.person .nm { font-size: 16px; font-weight: 700; }
.person .rl { font-size: 12.5px; color: var(--turq); }
.person .yr, .person .pf { font-size: 11px; color: var(--muted); word-break: break-all; }
.steps { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin-top: 12px; }
.step { background: var(--surface); border-radius: 12px; padding: 14px; border-top: 3px solid var(--turq); }
.cmp { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.cmp .col { padding: 16px; border-radius: 12px; border: 1px solid var(--line); }
.cmp .old { background: rgba(255,255,255,.02); }
.cmp .new { background: rgba(59,201,192,.08); border-color: rgba(59,201,192,.3); }
.flow { list-style: none; display: flex; flex-direction: column; gap: 8px; }
.flow li { font-size: 14.5px; display: flex; gap: 8px; }
.ask .row { display: flex; flex-direction: column; gap: 4px; padding: 10px 0; border-bottom: 1px solid var(--line); }
.ask .t { font-size: 16.5px; font-weight: 700; color: var(--text); }
.ask .d { font-size: 14px; color: var(--muted); }
.tmeta { display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 14px; margin-top: 16px; border-top: 1px solid var(--line); padding-top: 14px; }
.tmeta .k { font-family: var(--mono); font-size: 10px; letter-spacing: 0.14em; color: var(--muted); text-transform: uppercase; }
.tmeta .v { font-size: 14.5px; font-weight: 700; }
.logo-full { width: 240px; height: auto; margin-bottom: 16px; }
.tail { margin-top: 16px; padding-top: 12px; border-top: 1px solid var(--line); font-size: 14px; color: var(--muted); }
.big-quote { font-family: var(--disp); font-size: 28px; font-weight: 700; line-height: 1.2; }
.big-quote em { color: var(--saffron); font-style: normal; }
"""

sections_html = []
for idx, s in enumerate(slides, 1):
    # Remove anim classes for clean static document
    clean_s = s.replace(" anim", "")
    sections_html.append(f'<div class="page-section" id="section-{idx}">\n<div class="eyebrow">BO\'LIM {idx:02d} / {len(slides):02d}</div>\n{clean_s}\n</div>')

full_handbook = f"""<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="utf-8">
<title>Target International School — Dual Ta'lim Tizimi Qo'llanmasi</title>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,300..800&family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>
{handbook_css}
</style>
</head>
<body>
<div style="text-align:center;padding:40px 20px 60px;background:var(--base2);border:1px solid var(--line);border-radius:20px;margin-bottom:30px">
  <div style="font-family:var(--mono);font-size:12px;color:var(--turq);letter-spacing:.2em;text-transform:uppercase;margin-bottom:12px">Rasmiy Qo'llanma va Taqdimot Hujjati</div>
  <h1 style="font-size:44px;margin-bottom:16px">Target International School<br><span style="color:var(--saffron)">Dual Ta'lim Tizimi</span></h1>
  <p style="font-size:18px;max-width:700px;margin:0 auto 24px;color:var(--muted)">Maktab darsligi asosida IT kadrlar tayyorlash va o'quvchilarni real daromadga olib chiqish modelining to'liq qo'llanmasi</p>
  <div style="display:inline-flex;gap:24px;font-family:var(--mono);font-size:13px;color:var(--muted);border-top:1px solid var(--line);padding-top:16px">
    <span><b>O'quv yili:</b> 2026 – 2027</span>
    <span><b>Sana:</b> 24.07.2026</span>
    <span><b>Bo'limlar:</b> 20 ta</span>
  </div>
</div>

{''.join(sections_html)}

</body>
</html>
"""

with open(handbook_path, "w", encoding="utf-8") as f:
    f.write(full_handbook)

print("handbook.html written successfully.")

# Run Chrome CLI to generate A4 PDF Handbook
chrome_cmd = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    f"file://{handbook_path}"
]

res = subprocess.run(chrome_cmd, capture_output=True, text=True)
print("Chrome output:", res.stdout, res.stderr)
