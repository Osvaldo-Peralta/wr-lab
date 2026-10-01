# -*- coding: utf-8 -*-
"""
WR-LAB · build_db.py — construye data/wrlab.db (SQLite) desde las fuentes de texto del lab.
Tablas: meta, champions, champion_as_official, items, patches, changes, reports, sources,
winrates (champion_winrates.csv — las refresca el vigía 2×/día, check_patch.py paso 4).
Uso:  python3 model/build_db.py        (idempotente: recrea la BD desde cero)
Diseño: los .md/.csv siguen siendo la fuente de verdad editable; la BD es la capa de
consulta/respaldo (y lo que consume un futuro frontend/CLI).
"""
import csv, os, re, sqlite3, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = os.path.join(ROOT, "data", "estructurada")
DB = os.path.join(ROOT, "data", "wrlab.db")

def connect_fresh():
    if os.path.exists(DB): os.remove(DB)
    con = sqlite3.connect(DB)
    con.executescript("""
    CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT);
    CREATE TABLE champions(key TEXT PRIMARY KEY, name TEXT, roles TEXT, archetype TEXT,
        base_ad REAL, ad_growth REAL, base_as REAL, as_ratio REAL, base_bonus_as REAL,
        as_per_lvl REAL, ranged INT, notes TEXT, report TEXT);
    CREATE TABLE champion_as_official(champion TEXT PRIMARY KEY, patch TEXT,
        as_ratio TEXT, base_as TEXT, base_bonus TEXT, as_per_lvl TEXT);
    CREATE TABLE items(name TEXT PRIMARY KEY, gold TEXT, stats TEXT, categories TEXT, passives TEXT);
    CREATE TABLE patches(id TEXT PRIMARY KEY, release_date TEXT, status TEXT, raw_path TEXT, diff_path TEXT);
    CREATE TABLE changes(patch TEXT, entity_type TEXT, entity TEXT, change TEXT);
    CREATE TABLE reports(champion TEXT, path TEXT PRIMARY KEY, version TEXT, status TEXT, patch TEXT, tags TEXT);
    CREATE TABLE sources(name TEXT, url TEXT, accessed TEXT, role TEXT);
    CREATE TABLE winrates(champion TEXT, role TEXT, tier TEXT, win_pct REAL, pick_pct REAL,
        ban_pct REAL, trend TEXT, confidence TEXT, bucket TEXT, updated_utc TEXT,
        actualizado TEXT, PRIMARY KEY(champion, role));
    """)
    return con

def load_specs():
    sys.path.insert(0, os.path.join(ROOT, "model"))
    from champspecs import SPECS
    import dataclasses
    import dps_model
    out = dict(SPECS)
    if "jinx" not in out:
        j = dps_model.CHAMPS["jinx"]
        out["jinx"] = {f.name: getattr(j, f.name) for f in dataclasses.fields(j)}
        out["jinx"]["roles"] = ["ADC (Dragon)"]
        out["jinx"]["archetype"] = "crit-aoe"
    return out

def parse_change_rows(md_path, patch_id):
    """Extrae filas de las tablas markdown de un archivo de cambios (| a | b | c |)."""
    rows = []
    if not os.path.exists(md_path): return rows
    for line in open(md_path, encoding="utf-8"):
        line = line.strip()
        if not line.startswith("|") or set(line) <= set("|-: "): continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 3 and cells[0] and not cells[0].lower().startswith(("champ","ítem","item","sistema","fuente","tema","---")):
            rows.append((patch_id, "tabla", cells[0], " · ".join(cells[1:])))
    return rows

def main():
    con = connect_fresh(); cur = con.cursor()
    hoy = datetime.date.today().isoformat()
    cur.executemany("INSERT INTO meta VALUES(?,?)", [
        ("lab_version", "1.11"), ("patch_base", "7.3"), ("hotfix", "7.3a"),
        ("db_built", hoy), ("champions_total", ""), ("items_total", "")])

    # champions (specs del equipo)
    reps = {}
    rdir = os.path.join(ROOT, "reportes")
    for f in os.listdir(rdir):
        m = re.match(r"([A-Za-z']+)_WR_", f)
        if m: reps[m.group(1).lower()] = os.path.join("reportes", f)
    n = 0
    for key, sp in load_specs().items():
        cur.execute("INSERT OR REPLACE INTO champions VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            key, sp["name"], ";".join(sp.get("roles", [])), sp.get("archetype", ""),
            sp.get("base_ad"), sp.get("ad_growth"), sp.get("base_as"), sp.get("as_ratio"),
            sp.get("base_bonus_as"), sp.get("as_per_lvl"), int(sp.get("ranged", 0)),
            sp.get("notes", ""), reps.get(key, "")))
        n += 1
    cur.execute("UPDATE meta SET value=? WHERE key='champions_total'", (str(n),))

    # AS oficial 140 campeones
    with open(os.path.join(E, "champion_attack_speed_7.3.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cur.execute("INSERT OR REPLACE INTO champion_as_official VALUES(?,?,?,?,?,?)", (
                r["champion"], "7.3+7.3a", r["Attack Speed Ratio"], r["Base Attack Speed"],
                r["Base Bonus Attack Speed"], r["Attack Speed per Level"]))

    # items (tolerante a nombres de columna entre versiones del extractor)
    with open(os.path.join(E, "items_7.3.csv"), encoding="utf-8") as f:
        rd = csv.DictReader(f)
        det_col = "pasivos_y_detalle" if "pasivos_y_detalle" in rd.fieldnames else "detalle_completo"
        rows = [(r["item"], r["precio_oro"], r["stats"], r["categorias"], r.get(det_col, "")) for r in rd]
    cur.executemany("INSERT OR REPLACE INTO items VALUES(?,?,?,?,?)", rows)
    cur.execute("UPDATE meta SET value=? WHERE key='items_total'", (str(len(rows)),))

    # win rates del roster (si el vigía ya las sembró; si no, la tabla queda vacía)
    wr_csv = os.path.join(E, "champion_winrates.csv")
    n_wr = 0
    if os.path.exists(wr_csv):
        with open(wr_csv, encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                try:
                    cur.execute("INSERT OR REPLACE INTO winrates VALUES(?,?,?,?,?,?,?,?,?,?,?)", (
                        r["champion"], r["role"], r.get("tier", ""),
                        float(r["win_pct"]), float(r.get("pick_pct") or 0), float(r.get("ban_pct") or 0),
                        r.get("trend", ""), r.get("confidence", ""), r.get("bucket", ""),
                        r.get("updated_utc", ""), r.get("actualizado", "")))
                    n_wr += 1
                except (KeyError, ValueError):
                    continue

    # patches + changes
    cur.execute("INSERT INTO patches VALUES(?,?,?,?,?)",
                ("7.3", "2026-09-21", "live", "data/raw/patch73.txt", "data/estructurada/cambios_items_7.3.md"))
    cur.execute("INSERT INTO patches VALUES(?,?,?,?,?)",
                ("7.3a", "2026-09-29", "programado (CN confirmado; EN pendiente)", "data/raw/patch73a_cn_en.txt", "data/estructurada/cambios_7.3a.md"))
    for row in parse_change_rows(os.path.join(E, "cambios_7.3a.md"), "7.3a"):
        cur.execute("INSERT INTO changes VALUES(?,?,?,?)", row)

    # reports (frontmatter; champion con fallback al nombre de archivo — formato vault)
    import contextlib, io as _io
    with contextlib.redirect_stdout(_io.StringIO()):
        import update_reports as U
    for f in sorted(os.listdir(rdir)):
        if not f.endswith(".md"): continue
        t = open(os.path.join(rdir, f), encoding="utf-8").read()
        fm = re.search(r'^---\n(.*?)\n---', t, re.S)
        champ = ver = stat = pat = tags = ""
        fm_dict = {}
        if fm:
            for k, v in re.findall(r'^(\w+):\s*(.+)$', fm.group(1), flags=re.M):
                fm_dict[k] = v
                if k == "champion": champ = v
                if k == "version": ver = v
                if k == "Status": stat = v
                if k == "patch": pat = v.strip('"')
            tags = ",".join(re.findall(r'^\s+-\s+(.+)$', fm.group(1), flags=re.M))
        if not champ:
            champ = U.champ_desde_archivo(f, fm_dict, t)
        if not pat:
            pat = U.parche_declarado(fm_dict, t) or ""
        if champ:
            cur.execute("INSERT OR REPLACE INTO reports VALUES(?,?,?,?,?,?)",
                        (champ, os.path.join("reportes", f), ver, stat, pat, tags))

    # sources
    for s in [("Notas oficiales 7.3", "wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-7-3/", "2026-09-25", "primaria"),
              ("Notas oficiales 7.2", "wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-7-2/", "2026-09-25", "primaria"),
              ("7.3a CN vía Arctic Shift", "lolm.qq.com docid 15413436308828016227 (reddit 1wskk84)", "2026-09-28", "primaria-traducida"),
              ("wr-meta items", "wr-meta.com/items/", "2026-09-25", "secundaria"),
              ("wr-meta campeones", "wr-meta.com/{id}-{champ}.html", "2026-09-25/28", "secundaria"),
              ("wr-meta Meta Overview (win rates)", "wr-meta.com/{id}-{champ}.html · sitemap.xml", "vigía 2×/día (check_patch.py)", "secundaria-contexto")]:
        cur.execute("INSERT INTO sources VALUES(?,?,?,?)", s)

    con.commit(); con.close()
    print(f"BD construida: {DB} ({os.path.getsize(DB)//1024} KB)")
    con = sqlite3.connect(DB)
    for q in ["SELECT COUNT(*) FROM champions","SELECT COUNT(*) FROM champion_as_official",
              "SELECT COUNT(*) FROM items","SELECT COUNT(*) FROM changes","SELECT COUNT(*) FROM reports",
              "SELECT COUNT(*) FROM winrates"]:
        print(" ", q.replace("SELECT COUNT(*) FROM ",""), "=", con.execute(q).fetchone()[0])
    con.close()

if __name__ == "__main__":
    main()
