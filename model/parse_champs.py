# -*- coding: utf-8 -*-
"""Parser de fichas de campeón (wr-meta) -> data/estructurada/campeones/{slug}.md + champion_base_stats.json"""
import re, html as H, json, csv, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAWC = os.path.join(ROOT, "data", "raw", "campeones")
OUTC = os.path.join(ROOT, "data", "estructurada", "campeones")
os.makedirs(OUTC, exist_ok=True)

NAMES = {"yuumi":"Yuumi","yunara":"Yunara","mordekaiser":"Mordekaiser","kalista":"Kalista",
         "diana":"Diana","karma":"Karma","heimerdinger":"Heimerdinger","volibear":"Volibear",
         "seraphine":"Seraphine","shyvana":"Shyvana","chogath":"Cho'Gath",
         # v1.15: nuevos campeones solicitados por el autor (IDs vía sitemap.xml, 04/10)
         "orianna":"Orianna","ahri":"Ahri","nocturne":"Nocturne","syndra":"Syndra"}

# AS oficial 7.3 (apéndice de las notas)
as_official = {}
with open(os.path.join(ROOT,"data","estructurada","champion_attack_speed_7.3.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        as_official[r["champion"].lower().replace("'","")] = r
dur_official = {}
with open(os.path.join(ROOT,"data","estructurada","champion_durability_7.3.csv"), encoding="utf-8") as f:
    for r in csv.DictReader(f):
        dur_official[r["champion"].lower().replace("'","")] = r

def parse(slug):
    raw = open(os.path.join(RAWC, slug+".html"), encoding="utf-8", errors="ignore").read()
    name = NAMES[slug]
    # --- stats base ---
    stats = {}
    sb = raw.find('<div class="stats-block">'); se = raw.find('</table>', sb)
    block = raw[sb:se]
    for m in re.finditer(r'alt="([a-z]+)"[^>]*>(?:<!--/smile-->)?\s*([^<]*)', block):
        val = m.group(2).strip()
        if val: stats[m.group(1)] = val
    # --- habilidades ---
    ab = raw.find('<div class="ability-block">')
    ae = raw.find("Change history", ab)
    if ae < 0: ae = raw.find("Meta Overview", ab)
    hab_html = raw[ab:ae]
    txt = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>', ' ', hab_html)
    txt = re.sub(r'</(div|p|br|li|td)>', '\n', txt, flags=re.I)
    txt = H.unescape(re.sub(r'<[^>]+>', ' ', txt))
    txt = re.sub(r'[ \t]+', ' ', txt)
    txt = re.sub(r'\n\s*\n+', '\n', txt).strip()
    # --- change history ---
    ch = raw.find("Change history")
    ch_txt = ""
    if ch >= 0:
        ce = raw.find("Comments", ch)
        t2 = re.sub(r'<[^>]+>', '\n', raw[ch:ce if ce>0 else ch+15000])
        t2 = H.unescape(t2); t2 = re.sub(r'\n{2,}', '\n', t2).strip()
        ch_txt = t2[:5000]
    # --- popular build/runes (referencia) ---
    meta = ""
    mo = raw.find("Runes BUILD")
    if mo > 0:
        t3 = H.unescape(re.sub(r'<[^>]+>', '\n', raw[mo:mo+3000]))
        meta = re.sub(r'\n{2,}', '\n', t3).strip()[:900]
    return name, stats, txt, ch_txt, meta

results = {}
for slug in NAMES:
    name, stats, abilities, history, meta = parse(slug)
    key = slug.replace("'","")
    off = as_official.get(key) or as_official.get(name.lower().replace("'",""))
    dur = dur_official.get(name.lower().replace("'",""))
    results[slug] = dict(name=name, stats=stats, as_official_73=off, durability_73=dur)
    md = [f"# {name} — Ficha de datos (Wild Rift 7.3)", "",
          f"> wr-meta.com (24-sep-2026) + apéndice oficial 7.3. Crudo: data/raw/campeones/{slug}.html", "",
          "## Stats base (nivel 1, growth entre paréntesis)", ""]
    for k, v in stats.items(): md.append(f"- **{k}**: {v}")
    md += ["", "## AS oficial 7.3 (apéndice de las notas — fuente primaria para el modelo)", ""]
    if off:
        for k, v in off.items(): md.append(f"- {k}: {v}")
    else: md.append("- (no encontrado en el apéndice — verificar)")
    if dur:
        md += ["", "## Ajustes de durabilidad 7.3", ""]
        for k, v in dur.items():
            if k != "champion": md.append(f"- {k}: {v}")
    md += ["", "## Habilidades (texto completo con valores actuales)", "", "```", abilities[:9000], "```", "",
           "## Change history (cambios recientes)", "", "```", history[:4000], "```", "",
           "## Build/runas populares (referencia comunitaria, NO conclusión)", "", "```", meta, "```"]
    open(os.path.join(OUTC, slug+".md"), "w", encoding="utf-8").write("\n".join(md))
    print(f"ok {name:<12} stats={len(stats)} as_official={'SI' if off else 'NO'} hab={len(abilities)}")

json.dump(results, open(os.path.join(ROOT,"data","estructurada","champion_base_stats.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("JSON guardado")
