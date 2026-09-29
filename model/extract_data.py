# -*- coding: utf-8 -*-
"""
WR-LAB · Extractor de datos estructurados
Convierte los archivos crudos (data/raw/) en bases reutilizables (data/estructurada/).
Fuentes: notas oficiales 7.3 (21-sep-2026), notas 7.2 (08-jul-2026), wr-meta.com (24-sep-2026).
Ejecutar: python3 model/extract_data.py   (desde la raiz de wr-lab)
"""
import re, html as H, csv, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
OUT = os.path.join(ROOT, "data", "estructurada")
os.makedirs(OUT, exist_ok=True)

def read(p): return open(os.path.join(RAW, p), encoding="utf-8", errors="ignore").read()

notes = read("patch73.txt")
items_html = read("wrmeta_items.html")

def clean(s):
    s = H.unescape(re.sub(r'<[^>]+>', '\n', s))
    s = s.replace('\u2019', "'").replace('\u2018', "'").replace('\u201c','"').replace('\u201d','"')
    s = re.sub(r'\n{2,}', '\n', s).strip()
    return s

# ============ 1) SECCIONES DE LAS NOTAS OFICIALES 7.3 ============
def section(text, start_marker, end_marker):
    i = text.find(start_marker); j = text.find(end_marker, i+1)
    return text[i:j if j>0 else len(text)].strip()

sec_champs = section(notes, "Marksman Systematic Adjustments", "Champion Durability Adjustments")
sec_items  = section(notes, "Item Adjustments", "RUNE ADJUSTMENTS")
sec_runes  = section(notes, "RUNE ADJUSTMENTS", "BATTLEFIELD ADJUSTMENTS")
sec_field  = section(notes, "Jungle Adjustments", "OTHER IN-GAME ADJUSTMENTS")
sec_min    = section(notes, "Lifesteal\nWe're introducing", "OTHER IN-GAME ADJUSTMENTS")
sec_asmech = section(notes, "In Patch 7.3, we made fairly major changes to Attack Speed", "Garen\nBase Stats")

def save(name, content):
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(content)
    print("ok:", name, len(content), "chars")

save("cambios_campeones_7.3.md",
"# Cambios a campeones - Wild Rift 7.3 (notas oficiales 21-sep-2026)\n\n"
"> Ajustes sistemicos de marksman + cambios individuales. Fuente: wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-7-3/\n\n"
+ sec_champs)
save("cambios_items_7.3.md",
"# Cambios a items - Wild Rift 7.3 (notas oficiales)\n\n> Incluye items nuevos (C44, Yun Tal, Fiendhunter, Stormrazor, Shieldbow), removidos (Magnetic Blaster, Cloak of Agility, Soul Transfer, Nashor's Talon) y componentes.\n\n"
+ sec_items)
save("cambios_runas_7.3.md",
"# Cambios a runas - Wild Rift 7.3 (notas oficiales)\n\n> Lethal Tempo rehecho, Legend: Haste reemplaza a Legend: Tenacity, Ingenious Hunter removida, Conqueror/Demolish ajustados.\n\n"
+ sec_runes)
save("sistemas_campo_7.3.md",
"# Sistemas de campo - Wild Rift 7.3 (notas oficiales)\n\n> Jungla/smite, torretas (7000 HP, placas permanentes, Crystalline Overgrowth), minions, Hand of Baron, Lifesteal nuevo stat.\n\n"
+ sec_field + "\n\n## LIFESTEAL (nuevo stat)\n\n" + sec_min)
save("mecanica_attack_speed_7.3.md",
"# Mecanica de Attack Speed 7.3 (explicacion oficial)\n\n" + sec_asmech)

# ============ 2) TABLAS DEL APENDICE (todos los campeones) ============
apendice = notes[notes.find("Champion Durability Adjustments Detailed List"):]
apendice = apendice[:apendice.find("Wild Rift Game Design Team") if "Wild Rift Game Design Team" in apendice else len(apendice)]

lines = [l.rstrip() for l in apendice.split("\n")]
dur_rows, as_rows = [], []
i = 0
while i < len(lines):
    l = lines[i].strip()
    if l and i+1 < len(lines) and lines[i+1].strip() == "Base Stats":
        name = l
        stats = []
        j = i+2
        while j < len(lines) and lines[j].strip().startswith("- "):
            stats.append(lines[j].strip()[2:]); j += 1
        if any("Attack Speed Ratio" in s for s in stats):
            row = {"champion": name}
            for s in stats:
                k, _, v = s.partition(":")
                row[k.strip()] = v.strip()
            as_rows.append(row)
        elif stats:
            row = {"champion": name}
            for s in stats:
                k, _, v = s.partition(":")
                row[k.strip()] = v.strip()
            dur_rows.append(row)
        i = j; continue
    i += 1

# ⚠️ Overrides del HOTFIX 7.3a (29-sep-2026) — la página oficial 7.3 aún trae el apéndice viejo.
# Si regeneras desde raw, estos overrides se re-aplican automáticamente (fuente: cambios_7.3a.md).
OVERRIDES_73A = {
  "Caitlyn": {"Attack Speed per Level": "0.025 (7.3a: era 0.04)"},
  "Senna": {"Attack Speed Ratio": "0.3 (7.3a)", "Base Attack Speed": "0.3 (7.3a)",
            "Base Bonus Attack Speed": "1.1 (7.3a)", "Attack Speed per Level": "0.025 (7.3a)"},
}

def write_csv(name, rows, cols):
    p = os.path.join(OUT, name)
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader()
        for r in rows: w.writerow(r)
    print("ok:", name, len(rows), "filas")

as_cols = ["champion","Attack Speed Ratio","Base Attack Speed","Base Bonus Attack Speed","Attack Speed per Level"]
for _r in as_rows:
    _r.update(OVERRIDES_73A.get(_r["champion"], {}))
write_csv("champion_attack_speed_7.3.csv", as_rows, as_cols)

dur_cols = ["champion"]
for r in dur_rows:
    for k in r:
        if k not in dur_cols: dur_cols.append(k)
write_csv("champion_durability_7.3.csv", dur_rows, dur_cols)

# ============ 3) BASE DE ITEMS (wr-meta 24-sep-2026) ============
SECTIONS = ["FIGHTER ITEMS","ASSASSIN ITEMS","MARKSMAN ITEMS","MAGIC ITEMS","DEFENSE ITEMS","SUPPORT ITEMS",
            "Boots tier 2","Boots tier 3","Mid Tier Items","Basic Items"]
marks = []
for s in SECTIONS:
    idx = items_html.find(">"+s+"<")
    if idx<0: idx = items_html.find(s)
    marks.append((idx, s))
marks = sorted([m for m in marks if m[0]>=0])
def section_of(pos):
    cur = "?"
    for idx, s in marks:
        if idx <= pos: cur = s
    return cur

positions = [m.start() for m in re.finditer(r'<div class="bild-img-short">', items_html)]
positions.append(len(items_html))
items, seen = [], {}
for bi in range(len(positions)-1):
    b = items_html[positions[bi]:positions[bi+1]]
    m = re.search(r'<b class="iname">(.*?)</b>', b, re.S)
    if not m: continue
    name = clean(m.group(1)).replace("\n","")
    gold = re.search(r'<b class="goldt">([^<]+)</b>', b)
    gold = gold.group(1).strip() if gold else ""
    stats = [clean(s).replace("\n"," ") for s in re.findall(r'<b class="istats">(.*?)</b>', b, re.S)]
    full = clean(b).split("TIPS:")[0]
    sec = section_of(positions[bi])
    if name in seen:
        if sec not in seen[name]["sections"]: seen[name]["sections"] += "; "+sec
        if len(full) > len(seen[name]["full"]): seen[name]["full"] = full
        continue
    rec = dict(name=name, price=gold, stats=" | ".join(stats), sections=sec, full=full)
    seen[name] = rec; items.append(rec)

with open(os.path.join(OUT,"items_7.3.csv"),"w",newline="",encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["item","precio_oro","stats","categorias","detalle_completo"])
    for r in items: w.writerow([r["name"], r["price"], r["stats"], r["sections"], r["full"].replace("\n"," ~ ")])
print("ok: items_7.3.csv", len(items), "items unicos")

with open(os.path.join(OUT,"items_7.3.md"),"w",encoding="utf-8") as f:
    f.write("# Base de items Wild Rift 7.3 (estado 24-sep-2026)\n\n")
    f.write("> Fuente: wr-meta.com/items (BD sincronizada con 7.3), cross-verificada contra las notas oficiales 7.3/7.2.\n")
    f.write("> Diffs exactos del parche (antes -> despues): cambios_items_7.3.md. Un item puede aparecer en varias categorias.\n"
            "> \u26a0\ufe0f REGLA DE SLOTS (Ley 0): Wild Rift tiene 6 slots TOTALES y las botas ocupan UNO. Las 'Boots tier 3'\n"
            "> (Gunmetal, Chainlaced, Armored Advance, Crimson Lucidity, Spellslinger's, Armorcrusher, Immortal Treads)\n"
            "> son la MEJORA EN EL MISMO SLOT de su tier 2 (disponible desde el minuto 10:00), NO un item adicional.\n"
            "> Una build final = 1 botas (T3 tras el min 10) + 5 items. Ver FRAMEWORK.md Ley 0 y dps_model.validate_slots().\n\n")
    cur = None
    for r in items:
        s = r["sections"].split(";")[0]
        if s != cur: f.write(f"\n## {s}\n\n"); cur = s
        f.write(f"### {r['name']} — {r['price']}g\n")
        if r["stats"]: f.write(f"**Stats:** {r['stats']}\n")
        det = r["full"]
        det = det.replace(r["name"],"",1).strip("\n ")
        f.write("```\n"+det[:900]+"\n```\n")
print("ok: items_7.3.md")

# ============ 4) RUNAS (wr-meta) ============
i0 = items_html.find("KEYSTONE")
i_sorc = items_html.find("SORCERY", i0)
i1 = items_html.find("Spells", i_sorc)
runes_html = items_html[i0:i1 if i1>0 else len(items_html)]
txt = clean(runes_html)
txt = re.sub(r'\n\s*\n+', '\n', txt)
save("runas_7.3.md",
"# Runas Wild Rift - estado 7.3\n\n"
"> Fuente: wr-meta.com (24-sep-2026). OJO: Ingenious Hunter fue REMOVIDA en 7.3 y Legend: Tenacity -> Legend: Haste (ver cambios_runas_7.3.md).\n"
"> Lethal Tempo: usar valores oficiales 7.3 (6.4%/stack ranged, bala 6-24, +0.67% por 1% AS bonus), NO el texto de abajo que puede estar desactualizado.\n\n"+txt)

print("\nTodo extraido en", OUT)
