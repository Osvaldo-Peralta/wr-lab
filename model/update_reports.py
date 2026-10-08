# -*- coding: utf-8 -*-
"""
WR-LAB · update_reports.py — triador/actualizador de reportes publicados (v1.6)
================================================================================
Cuando sale un hotfix (7.3a, 7.3b, 7.4…), los reportes publicados NO se regeneran
a ciegas: este módulo TRIA el impacto de cada cambio sobre cada reporte y decide:

    ✅ SIN_IMPACTO  el parche no toca nada del reporte → sello de verificación.
    ✅ ANOTAR       impacto medido < 2 % en métricas clave → la build y los veredictos
                    SIGUEN VIGENTES; se anota el bloque de verificación (nunca se regenera).
    ⚠️ REVISAR      Δ 2–5 %, o ítem de la build/variantes cambió, o cambio directo sin
                    hook cuantitativo → revisión manual acotada (matriz del último slot,
                    motivo de rechazados), sin regenerar la build completa.
    ❌ REGENERAR    Δ ≥ 5 % o cambio directo a inputs del spec (AD/AS growth, bases…)
                    → regeneración manual completa por el flujo del FRAMEWORK (10 pasos).

Principio rector (petición del autor, 29-sep-2026): **una build publicada y aprobada es
definitiva; el hotfix se ANOTA con su impacto medido, no se re-deriva la build** salvo
que la matemática demuestre que cambió (umbral ❌).

Flujo típico tras aplicar datos nuevos (FRAMEWORK §E pasos 1-5):
    python3 model/update_reports.py triage   --patch 7.3a   # tabla de impacto/veredicto
    python3 model/update_reports.py annotate --patch 7.3a --apply   # inserta bloques ✅
    python3 model/update_reports.py check                       # CI: drift + pendientes

Comandos:
    baseline   (re)construye data/estructurada/reportes_registry.json desde los reportes
               + estado actual del motor (métricas golden por reporte).
    triage     cuantifica el impacto de un parche sobre cada reporte (tabla + detalle).
    annotate   genera el bloque de verificación; --apply lo inserta en el reporte
               (idempotente, delimitado por marcadores HTML) y sella el registro.
    check      modo CI: falla (exit 1) si hay drift motor↔registro o reportes sin triar
               contra el último parche con diff estructurado.

Cero dependencias (stdlib). Texto plano = fuente de verdad; el registro JSON es índice derivado.
"""
import argparse, contextlib, datetime, io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTES = os.path.join(ROOT, "reportes")
ESTRUCTURADA = os.path.join(ROOT, "data", "estructurada")
REGISTRY = os.path.join(ESTRUCTURADA, "reportes_registry.json")
sys.path.insert(0, os.path.join(ROOT, "model"))

import dps_model as M                                  # noqa: E402
with contextlib.redirect_stdout(io.StringIO()):         # batch2 imprime tablas al importar
    import analysis_batch2 as B2                        # noqa: E402

# ---------------------------------------------------------------- umbrales (documentados en FRAMEWORK §E)
UMBRAL_ANOTAR = 2.0       # |Δ| < 2 %  → ✅ ANOTAR (impacto despreciable)
UMBRAL_REGENERAR = 5.0    # |Δ| >= 5 % → ❌ REGENERAR

VEREDICTOS = {
    "SIN_IMPACTO": "✅ SIN IMPACTO",
    "ANOTAR":      "✅ ANOTAR",
    "AL_DIA":      "⏩ AL DÍA",
    "REVISAR":     "⚠️ REVISAR",
    "REGENERAR":   "❌ REGENERAR",
}

# keywords que indican que un cambio directo toca INPUTS DEL SPEC (AD/AS/defensas base…)
SPEC_INPUT_KEYWORDS = [
    "growth", "ad base", "base ad", "attack speed", "as base", "base bonus", "as ratio",
    "ratio/base", "vida base", "hp base", "hp growth", "armadura base", "armor base",
    "mr base", "mr growth", "resistencia mágica base", "rango de ataque", "daño crítico",
    "crit ratio", "armadura y mr", "armor growth",
]

# ---------------------------------------------------------------- modelos por campeón (hooks cuantitativos)
# Cada hook devuelve métricas clave con el motor ACTUAL; params permite reconstruir el "pre-parche".
MODELOS = {
    "jinx":    dict(tipo="autos",    hook="hook_jinx"),
    "kalista": dict(tipo="onhit",    hook="hook_kalista"),
    "diana":   dict(tipo="rotacion", hook="hook_diana"),
    "yuumi":   dict(tipo="aliado",   hook="hook_yuumi"),
    "karma":   dict(tipo="aliado",   hook=None,
                    motivo="Imperial Mandate no está parametrizado en analysis_batch2.karma()"),
}

# nombre visible en Tabla A → clave del modelo correspondiente
SINONIMOS = {
    "berserker's greaves":       {"autos": "Berserker's"},
    "gunmetal greaves":          {"autos": "Gunmetal", "onhit": "Gunmetal"},
    "hexoptics c44":             {"autos": "C44"},
    "runaan's hurricane":        {"autos": "Runaan's", "onhit": "Runaan"},
    "infinity edge":             {"autos": "IE"},
    "lord dominik's regards":    {"autos": "LDR"},
    "kraken slayer":             {"autos": "Kraken"},
    "guinsoo's rageblade":       {"autos": "Guinsoo", "onhit": "Guinsoo"},
    "wit's end":                 {"autos": "WE", "onhit": "WitsEnd"},
    "terminus":                  {"autos": "Terminus", "onhit": "Terminus"},
    "blade of the ruined king":  {"autos": "BotRK", "onhit": "BotRK"},
    "spellslinger's shoes":      {"rotacion": "Spellslinger"},
    "boots of mana":             {"rotacion": "boots_mana"},
    "dusk and dawn":             {"rotacion": "DuskDawn"},
    "nashor's tooth":            {"rotacion": "Nashor"},
    "rabadon's deathcap":        {"rotacion": "Rabadon"},
    "zhonya's hourglass":        {"rotacion": "Zhonyas"},
    "cryptbloom":                {"rotacion": "Cryptbloom"},
    "void staff":                {"rotacion": "VoidStaff"},
    "ionian boots":              {"aliado": "ionian"},
    "crimson lucidity":          {"aliado": "Crimson"},
    "black mist scythe":         {"aliado": "Scythe"},
    "ardent censer":             {"aliado": "Censer"},
    "echoes of helia":           {"aliado": "Echoes"},
    "staff of flowing waters":   {"aliado": "Staff"},
    "redemption":                {"aliado": "Redemption"},
    "imperial mandate":          {"aliado": "Mandate"},
    "mikael's blessing":         {"aliado": "Mikael"},
    "shurelya's requiem":        {"aliado": "Shurelya"},
    "zeke's convergence":        {"aliado": "Zeke"},
    "locket of the iron solari": {"aliado": "Locket"},
    "diadem of songs":           {"aliado": "Diadem"},
    "crown of songs":            {"aliado": "Diadem"},
    # formas cortas / alias de paréntesis frecuentes en reportes del vault
    "botrk":                     {"onhit": "BotRK", "autos": "botrk"},
    "blade of the ruined king (botrk)": {"onhit": "BotRK"},
    "bloodthirster":             {"autos": "bt"},
    "gunmetal":                  {"autos": "Gunmetal", "onhit": "Gunmetal"},
    "guinsoo":                   {"autos": "Guinsoo", "onhit": "Guinsoo"},
    "statikk":                   {"autos": "statikk", "onhit": "Statikk"},
    "infinity orb":              {"rotacion": "InfinityOrb"},
    "luden's echo":              {"rotacion": "Luden"},
    "liandry's anguish":         {"rotacion": "Liandry", "aliado": "Liandry"},
    "morellonomicon":            {"rotacion": "Morello"},
    "zhonyas":                   {"rotacion": "Zhonyas"},
    "nashor":                    {"rotacion": "Nashor"},
    "rabadon":                   {"rotacion": "Rabadon"},
    "censer":                    {"aliado": "Censer"},
    "stormsurge":                {"aliado": "Stormsurge", "rotacion": "Stormsurge"},
    "harmonic echo":             {"aliado": "HarmonicEcho"},
    "morellonomicon":            {"aliado": "Morello", "rotacion": "Morello"},
    "rylai's crystal scepter":   {"aliado": "Rylai", "rotacion": "Rylai"},
    "horizon focus":             {"aliado": "HorizonFocus", "rotacion": "HorizonFocus"},
    "liandry's torment":         {"aliado": "Liandry", "rotacion": "Liandry"},
}

# relevancia de cambios sistémicos por rol (para notas cualitativas)
SISTEMAS_POR_ROL = [
    (("jungla", "jungle"), ("jungla", "smite", "monstruo", "clear")),
    (("adc", "dragon", "marksman", "siege", "tirador"), ("placa", "torreta", "nexus", "siege", "minion", "barón", "baron")),
    (("support", "soporte"), ("support", "soporte", "quest", "relic", "oro de")),
]

STOP_WORDS = {"of", "the", "and", "de", "la", "el", "los", "las", "vs", "con", "por"}

# roster conocido para derivar el campeón del nombre de archivo (los reportes del vault
# no siempre llevan 'champion:' en el frontmatter)
ROSTER = ["heimerdinger", "mordekaiser", "seraphine", "chogath", "cho'gath", "kalista",
          "volibear", "shyvana", "caitlyn", "corki", "ezreal", "graves", "janna",
          "diana", "jinx", "karma", "lulu", "nami", "norra", "rammus", "senna",
          "sivir", "soraka", "thresh", "tristana", "vayne", "veigar", "vi", "viego",
          "yasuo", "yone", "yunara", "yuumi", "zed", "zoe", "zyra", "malphite", "warwick"]
ALIAS_ARCHIVO = {"yunana": "yunara"}   # errata de nombre de archivo confirmada en el contenido


def _norm_champ(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def champ_desde_archivo(archivo, fm, txt):
    """champion del frontmatter → si no, desde el nombre de archivo (roster + alias)."""
    if fm.get("champion"):
        return fm["champion"].strip()
    base = re.sub(r"\.md$", "", archivo).split(" - ")[0].strip().lower()
    if base in ALIAS_ARCHIVO:
        base = ALIAS_ARCHIVO[base]
    nb = _norm_champ(base)
    display_special = {"chogath": "Cho'Gath"}
    for r in ROSTER:
        nr = _norm_champ(r)
        if nb.startswith(nr):
            return display_special.get(nr, r.title())
    return base.title()


def parche_declarado(fm, txt):
    """Parche máximo que el reporte declara cubrir (frontmatter 'patch:' o línea **Parche:**)."""
    fuentes = [fm.get("patch", "")]
    m = re.search(r"\*\*Parche:\*\*\s*([^\n]+)", txt)
    if m:
        fuentes.append(m.group(1))
    tokens = []
    for s in fuentes:
        tokens += re.findall(r"\d+\.\d+[a-z]?", s)
    return max(tokens, key=patch_key) if tokens else None


# ================================================================ parches y diffs
def patch_key(p):
    """'7.3'→(7,3,0) · '7.3a'→(7,3,1) · '7.4'→(7,4,0) — para ordenar parches."""
    m = re.match(r"(\d+)\.(\d+)([a-z]?)", p.strip())
    if not m:
        return (0, 0, 0)
    return (int(m.group(1)), int(m.group(2)), (ord(m.group(3)) - 96) if m.group(3) else 0)


def _max_patch(s):
    """De '7.3+7.3a' (o cualquier texto) extrae el token de parche máximo."""
    if not s:
        return None
    tokens = re.findall(r"\d+\.\d+[a-z]?", s)
    return max(tokens, key=patch_key) if tokens else None


def cambios_archivos():
    """[(patch, ruta, kind)] de los diffs estructurados en data/estructurada/.
    kind='hotfix' para cambios_<patch>.md; kind='tema' para cambios_<tema>_<patch>.md."""
    out = []
    for f in sorted(os.listdir(ESTRUCTURADA)):
        m = re.match(r"^cambios_(?:(\w+?)_)?(\d+\.\d+[a-z]?)\.md$", f)
        if m:
            kind = "hotfix" if not m.group(1) else "tema"
            out.append((m.group(2), os.path.join(ESTRUCTURADA, f), kind))
    return out


def ultimo_parche_hotfix():
    hf = [(p, r) for p, r, k in cambios_archivos() if k == "hotfix"]
    if not hf:
        return None, None
    p, r = max(hf, key=lambda x: patch_key(x[0]))
    return p, r


def parse_cambios(ruta):
    """Parsea un diff estructurado (formato cambios_7.3a.md):
    tablas bajo '## CAMPEONES', '## ÍTEMS', '## MAPA Y SISTEMAS' e
    '## IMPACTO EN REPORTES/SPECS DEL LAB'."""
    with open(ruta, encoding="utf-8") as fh:
        txt = fh.read()
    seccion = None
    cs = {"champions": {}, "items": {}, "sistemas": [], "lab_notes": {}, "raw": ruta}
    for linea in txt.splitlines():
        h = re.match(r"^##\s+(.*)", linea)
        if h:
            t = h.group(1).upper()
            if t.startswith("CAMPEONES"): seccion = "champ"
            elif t.startswith("ÍTEMS") or t.startswith("ITEMS"): seccion = "items"
            elif "SISTEMAS" in t: seccion = "sist"
            elif "IMPACTO" in t: seccion = "lab"
            else: seccion = None
            continue
        if not linea.strip().startswith("|") or seccion is None:
            continue
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if len(celdas) < 2 or set(celdas[0]) <= set("-: "):
            continue
        nombre_m = re.search(r"\*\*(.+?)\*\*", celdas[0])
        if seccion == "lab":
            if celdas[0].lower().startswith(("archivo", "---")):
                continue
            cs["lab_notes"][celdas[0]] = " → ".join(celdas[1:]).strip()
            continue
        if not nombre_m or nombre_m.group(1).lower() in ("campeón", "champion", "ítem", "item", "sistema"):
            continue
        nombre = nombre_m.group(1).strip()
        if seccion == "champ":
            cs["champions"][nombre] = {"tipo": celdas[1] if len(celdas) > 1 else "",
                                       "detalles": celdas[2] if len(celdas) > 2 else ""}
        elif seccion == "items":
            cs["items"][nombre] = {"tipo": celdas[1] if len(celdas) > 1 else "",
                                   "detalles": celdas[2] if len(celdas) > 2 else ""}
        elif seccion == "sist":
            cs["sistemas"].append({"sistema": nombre,
                                   "cambio": celdas[1] if len(celdas) > 1 else "",
                                   "impacto": celdas[2] if len(celdas) > 2 else ""})
    return cs


def expandir_nombre_item(nombre):
    """'Crown/Diadem of Songs' → ['Crown of Songs','Diadem of Songs']."""
    m = re.match(r"^([\w']+)/([\w'']+)(.*)$", nombre)
    if m:
        return [m.group(1) + m.group(3), m.group(2) + m.group(3)]
    return [nombre]


# ================================================================ parseo de reportes
def parse_frontmatter(txt):
    fm = {}
    m = re.search(r"^---\n(.*?)\n---", txt, re.S)
    if m:
        for k, v in re.findall(r"^(\w+):\s*(.+)$", m.group(1), flags=re.M):
            fm[k] = v.strip().strip('"')
    return fm


def parse_rol(txt):
    m = re.search(r"\*\*Rol principal:\*\*\s*(.+)", txt)
    if m:
        return m.group(1).strip()
    fm = re.search(r"^---\n(.*?)\n---", txt, re.S)          # fallback: tags del frontmatter
    if fm:
        tags = re.findall(r"^\s+-\s+(.+)$", fm.group(1), flags=re.M)
        return " ".join(t.strip() for t in tags)
    return ""


def _limpiar_nombre(s):
    s = s.replace("⬆️", "").strip()
    s = re.sub(r"\s*\(.*?\)\s*$", "", s).strip()   # "(default)" / "(jungla)" finales
    return s.strip()


# ---------------------------------------------------------------- extracción de la build publicada
SLOT_HEADERS = ("slot", "ranura", "#", "nº", "no.", "posición")

def _es_fila_sep(celdas):
    return all(set(c) <= set("-: ") and c for c in celdas)

def _header_slot_like(celdas):
    h = celdas[0].lower().strip(" *")
    return any(h.startswith(s) for s in SLOT_HEADERS)

def _header_es_ruta(celdas):
    return any(("minuto" in c.lower() or "momento" in c.lower()) for c in celdas)

def _nombre_de_celda(celda):
    """Ítem visible de una celda: primer bold (T3 si hay '→' dentro), o texto plano
    si no hay bold (alias en paréntesis se resuelve después en resolver_clave)."""
    c = celda.split("<br>")[0].strip()
    bolds = re.findall(r"\*\*(.+?)\*\*", c)
    if bolds:
        b = bolds[0]
        if "→" in b or "->" in b:
            b = re.split(r"→|->", b)[-1]
        nombre = b
    else:
        base = re.sub(r"\*\*|⬆️|\*", "", c)
        paren = re.findall(r"\(([^)]+)\)", base)
        alias = None
        for p in paren:                       # alias inglés entre paréntesis tiene prioridad
            pp = re.split(r"→|->", p.strip())[-1].strip()
            if _nombre_conocido(pp):
                alias = pp
                break
        if alias:
            nombre = alias
        else:
            if "→" in base or "->" in base:
                base = re.split(r"→|->", base)[-1]
            nombre = base.split("(")[0]
    nombre = nombre.replace("⬆️", "").strip()
    nombre = re.sub(r"\s*\((default|jungla|mid|t3|solo[^)]*|min[^)]*)\)\s*$", "", nombre, flags=re.I)
    return nombre.strip(" ·*")

def _nombre_conocido(x):
    xl = x.lower().strip()
    if xl in SINONIMOS or xl in M.ITEMS or x in M.ALIAS or xl in {a.lower() for a in M.ALIAS}:
        return True
    for dic in (B2.K_ITEMS, B2.D_ITEMS, B2.Y_ITEMS):
        if x in dic or xl in {k.lower() for k in dic}:
            return True
    return False

def _tablas_candidatas(txt):
    """[(prioridad, posición, filas)] de las tablas markdown del documento."""
    out = []
    lines = txt.splitlines()
    heading = ""
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith("#"):
            heading = lines[i].lstrip("# ").strip()
        if lines[i].strip().startswith("|"):
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                j += 1
            out.append((heading, i, lines[i:j]))
            i = j
            continue
        i += 1
    cands = []
    for pos, (heading, start, filas) in enumerate(out):
        celdas_hdr = [c.strip() for c in filas[0].strip().strip("|").split("|")]
        if len(celdas_hdr) < 2 or not _header_slot_like(celdas_hdr):
            continue
        if _header_es_ruta(celdas_hdr):
            continue
        cuerpo = [f for f in filas[2:] if not _es_fila_sep([c.strip() for c in f.strip().strip("|").split("|")])]
        if len(cuerpo) < 6:
            continue
        h = heading.lower()
        prio = 0 if "tabla a" in h else (1 if ("build final" in h or "ranura por ranura" in h) else 2)
        cands.append((prio, start, heading, cuerpo))
    cands.sort(key=lambda x: (x[0], x[1]))
    return cands

def extraer_build(txt):
    """(nombres_visibles, fuente) de la build final publicada. fuente = heading de la tabla."""
    # prioridad 1: sección "### Tabla A ... ### Tabla B" (estándar v1.4)
    m = re.search(r"###\s+Tabla A(.*?)(?:###\s+Tabla B|\n## )", txt, re.S)
    if m:
        filas = [l for l in m.group(1).splitlines()
                 if l.strip().startswith("|") and not _es_fila_sep([c.strip() for c in l.strip().strip("|").split("|")])]
        filas = [l for l in filas if not re.match(r"^\|\s*slot\s*\|", l.strip(), re.I)]
        nombres = []
        for l in filas[:6]:
            celdas = [c.strip() for c in l.strip().strip("|").split("|")]
            if len(celdas) >= 2 and celdas[0]:
                n = _nombre_de_celda(celdas[1])
                if n:
                    nombres.append(n)
        if len(nombres) == 6:
            return nombres, "Tabla A"
    # prioridad 2/3: otras tablas con header de slot (BUILD FINAL, §0, etc.)
    for prio, start, heading, cuerpo in _tablas_candidatas(txt):
        nombres = []
        for l in cuerpo[:6]:
            celdas = [c.strip() for c in l.strip().strip("|").split("|")]
            n = _nombre_de_celda(celdas[1]) if len(celdas) >= 2 else ""
            if n:
                nombres.append(n)
        if len(nombres) == 6:
            return nombres, heading or f"tabla@línea{start}"
    return [], None


def parse_resumen_publico(txt):
    m = re.search(r"###\s+Tabla A.*?\n(>\s+\*\*Oro total.+)", txt, re.S)
    return m.group(1).strip() if m else ""


def resolver_clave(display, tipo_modelo):
    """display ('Lord Dominik's Regards' / 'Bloodthirster (BotRK)') → clave del modelo.
    Prueba: nombre completo → alias entre paréntesis → nombre sin paréntesis."""
    d = display.strip()
    cands = [(d, d.lower())]
    m = re.search(r"\(([^)]+)\)", d)
    if m:
        cands.append((m.group(1).strip(), m.group(1).strip().lower()))
    base = re.sub(r"\s*\([^)]*\)\s*", " ", d).strip()
    if base != d:
        cands.append((base, base.lower()))
    dic_por_tipo = {"onhit": B2.K_ITEMS, "rotacion": B2.D_ITEMS, "aliado": B2.Y_ITEMS}
    for orig, low in cands:
        if low in SINONIMOS and tipo_modelo in SINONIMOS[low]:
            return SINONIMOS[low][tipo_modelo]
    if tipo_modelo == "autos":
        for orig, low in cands:
            if orig in M.ALIAS:
                return M.ALIAS[orig]
            for a, k in M.ALIAS.items():
                if a.lower() == low:
                    return k
            if low in M.ITEMS:
                return low
    d2 = dic_por_tipo.get(tipo_modelo)
    if d2:
        for orig, low in cands:
            if orig in d2:
                return orig
            for k in d2:
                if k.lower() == low:
                    return k
    return None


# ================================================================ hooks cuantitativos
def hook_jinx(build_keys, params=None):
    spec = M.CHAMPS["jinx"]
    r1 = M.eval_build(spec, build_keys, level=15)
    r3 = M.eval_build(spec, build_keys, level=15, targets=3)
    ra = M.eval_build(spec, build_keys, level=15, armor=120)
    rt = M.eval_build(spec, build_keys, level=15, armor=220, tank=True, enemy_hp=4500)
    return {"oro": r1["gold"], "AD": r1["AD"], "AS": r1["AS"], "crit": r1["crit"],
            "dps1": r1["dps1"], "dps3": r3["dpsN"], "vs120": ra["dps1"],
            "vsTanque": rt["dps1"], "heal": r1["heal"]}


def hook_kalista(build_keys, params=None):
    r = B2.kalista(build_keys)
    r3 = B2.kalista(build_keys, targets=3)
    rt = B2.kalista(build_keys, armor=220, mr=150, ehp=4500)
    return {"oro": r["gold"], "AD": r["AD"], "AS": r["AS"], "pen": r["pen"],
            "dps1": r["single"], "dps3": r3["multi"], "vsTanque": rt["single"],
            "e_hit": r["e_hit"], "heal": r["heal"]}


def hook_diana(build_keys, params=None):
    kw = dict(keystone=(params or {}).get("keystone", "lt"))
    r = B2.diana(build_keys, **kw)
    rt = B2.diana(build_keys, mr=180, **kw)
    return {"oro": r["gold"], "AP": r["AP"], "AS": r["AS"], "dps10s": r["dps"],
            "burst": r["burst"], "vs180mr": rt["dps"]}


def hook_yuumi(build_keys, params=None):
    p = params or {}
    kw = {}
    if "w_flat" in p: kw["w_flat"] = p["w_flat"]
    if "w_ap_pct" in p: kw["w_ap_pct"] = p["w_ap_pct"]
    r = B2.yuumi(build_keys, **kw)
    return {"oro": r["gold"], "AP": r["AP"], "HSP": r["HSP"], "haste": r["haste"],
            "e_shield": r["e_shield"], "e_cd": r["e_cd"], "r_heal": r["r_heal"],
            "adc_dps_add": r["adc_dps_add"], "shield_per_min": r["shield_per_min"]}


HOOKS = {"hook_jinx": hook_jinx, "hook_kalista": hook_kalista,
         "hook_diana": hook_diana, "hook_yuumi": hook_yuumi}

# Métricas de RESULTADO (las que sostienen los veredictos del reporte). Los stats-input
# (HSP, AP, AD, AS, oro, haste…) se muestran en el triage pero NO deciden el veredicto:
# un nerf de input puede diluirse en el resultado (caso Yuumi 7.3a: HSP −5 % → E-shield −1.4 %).
RESULT_KEYS = {
    "hook_jinx":    ("dps1", "dps3", "vs120", "vsTanque", "heal"),
    "hook_kalista": ("dps1", "dps3", "vsTanque", "e_hit", "heal"),
    "hook_diana":   ("dps10s", "burst", "vs180mr"),
    "hook_yuumi":   ("e_shield", "r_heal", "adc_dps_add", "shield_per_min"),
}


# ---- parsers de parámetros pre/post por campeón (extender con cada hotfix) ----
def params_yuumi(detalles, patch):
    """Del texto 'W Best Friend HSP: 8/9/10/11 % + 0.02 % AP → 6/7/8/9 % + 0.01 % AP'
    extrae (pre, post, post_conservador). Convención del baseline publicado: pre = solo flat
    (rank 5), que es la que reproduce los golden numbers del reporte (E=339)."""
    ms = re.findall(r"(\d+)\s*/\s*(\d+)\s*/\s*(\d+)\s*/\s*(\d+)\s*%\s*\+\s*([\d.]+)\s*%\s*AP", detalles)
    if len(ms) < 2:
        return None
    pre = {"w_flat": int(ms[0][3]), "w_ap_pct": 0.0}
    post = {"w_flat": int(ms[1][3]), "w_ap_pct": float(ms[1][4])}
    post_cons = {"w_flat": int(ms[1][3]), "w_ap_pct": 0.0}   # conservador: ignora término AP
    return pre, post, post_cons


CHAMP_PARAMS = {"yuumi": params_yuumi}


# ================================================================ registro (índice derivado)
def construir_registro(hoy=None):
    hoy = hoy or datetime.date.today().isoformat()
    reg = {"version_schema": 1, "generado": hoy,
           "parche_motor": "7.3+7.3a", "reportes": {}}
    for f in sorted(os.listdir(REPORTES)):
        if not f.endswith(".md"):
            continue
        with open(os.path.join(REPORTES, f), encoding="utf-8") as fh:
            txt = fh.read()
        fm = parse_frontmatter(txt)
        champ = champ_desde_archivo(f, fm, txt)
        clave = _norm_champ(champ)
        modelo = MODELOS.get(clave, dict(tipo="desconocido", hook=None,
                                         motivo="sin modelo cuantitativo para este campeón/arquetipo"))
        build_disp, build_fuente = extraer_build(txt)
        build_keys, sin_resolver = [], []
        for d in build_disp:
            k = resolver_clave(d, modelo["tipo"])
            (build_keys if k else sin_resolver).append(k or d)
        entry = {
            "champion": clave, "champion_display": champ,
            "rol": parse_rol(txt), "modelo": modelo["tipo"],
            "hook": modelo.get("hook"), "hook_motivo": modelo.get("motivo", ""),
            "build_display": build_disp, "build_keys": build_keys,
            "build_fuente": build_fuente, "sin_resolver": sin_resolver,
            "parche_declarado": parche_declarado(fm, txt),
            "resumen_publico": parse_resumen_publico(txt),
            "metricas": None, "ultima_verificacion": None,
        }
        # v1.15.2: la verificación se DERIVA del frontmatter (verification +
        # verified_patch) para que `baseline` no destruya el sellado de
        # `annotate` según el orden en que se corran (incidente CI 08/10).
        if fm.get("verification") not in (None, "", "pending") and fm.get("verified_patch"):
            entry["ultima_verificacion"] = {
                "patch": fm["verified_patch"],
                "fecha": str(fm.get("updated_at") or fm.get("published_at") or hoy),
                "veredicto": fm["verification"],
                "delta_max_pct": None,
            }
        if not build_disp:
            if modelo.get("hook"):
                entry["hook"] = None
                entry["hook_motivo"] = "build final no extraíble automáticamente (formato del vault)"
        elif modelo.get("hook") and not sin_resolver and len(build_keys) == 6:
            try:
                entry["metricas"] = _redondear(HOOKS[modelo["hook"]](build_keys))
            except ValueError as exc:          # p.ej. exclusividad violada en la build publicada
                entry["hook"] = None
                entry["hook_motivo"] = f"build rechazada por el validador: {str(exc).splitlines()[-1][:120]}"
        elif modelo.get("hook"):
            entry["hook"] = None
            entry["hook_motivo"] = ("ítems sin resolver en el modelo: " + ", ".join(sin_resolver)) \
                if sin_resolver else entry["hook_motivo"]
        reg["reportes"][f] = entry
    return reg


def _redondear(d):
    return {k: (round(v, 1) if isinstance(v, float) else v) for k, v in d.items()}


def guardar_registro(reg):
    with open(REGISTRY, "w", encoding="utf-8") as fh:
        json.dump(reg, fh, indent=1, ensure_ascii=False)
    print(f"Registro guardado: {os.path.relpath(REGISTRY, ROOT)} "
          f"({len(reg['reportes'])} reportes, motor {reg['parche_motor']})")


def cargar_registro():
    if not os.path.exists(REGISTRY):
        sys.exit("No existe reportes_registry.json — correr primero: python3 model/update_reports.py baseline")
    with open(REGISTRY, encoding="utf-8") as fh:
        return json.load(fh)


# ================================================================ triage
def _norm(s):
    return re.sub(r"[^a-z0-9' ]", "", s.lower()).strip()


def _mencionado(texto_lower, nombre_item):
    """¿El ítem cambiado aparece en el texto del reporte (variantes/rechazados/apéndices)?
    Palabras distintivas con límite de palabra (\b) para evitar falsos positivos
    del tipo 'death' ⊂ 'Deathcap'."""
    variantes = [nombre_item] + expandir_nombre_item(nombre_item)
    for v in variantes:
        nv = _norm(v).replace("'", "")
        if nv in texto_lower.replace("'", ""):
            return v
        palabras = [w for w in re.split(r"[\s']+", _norm(v)) if len(w) >= 5 and w not in STOP_WORDS]
        if palabras and any(re.search(rf"\b{re.escape(w)}\b", texto_lower) for w in palabras):
            return v
    return None


def sistemas_relevantes(rol, cs):
    notas = []
    roles = (rol or "").lower()
    for s in cs["sistemas"]:
        texto = _norm(f"{s['sistema']} {s['cambio']} {s['impacto']}")
        for roles_clave, kws in SISTEMAS_POR_ROL:
            if any(r in roles for r in roles_clave) and any(k in texto for k in kws):
                notas.append(f"{s['sistema']}: {s['cambio']} → {s['impacto']}")
                break
    return notas


def lab_note_para(archivo, cs):
    for patron, nota in cs["lab_notes"].items():
        p = patron.strip().strip("`").replace("reportes/", "")
        p = re.sub(r"[_*\s]+$", "", p)          # 'Jinx_*' → 'Jinx' (match por prefijo de archivo)
        if p and archivo.startswith(p):
            return nota
    return None


def triage_reporte(archivo, entry, cs, patch):
    """Devuelve dict de triage para un reporte contra un ChangeSet."""
    with open(os.path.join(REPORTES, archivo), encoding="utf-8") as fh:
        txt = fh.read()
    tl = _norm(txt)
    out = {"archivo": archivo, "champion": entry["champion_display"], "patch": patch,
           "directo": None, "delta": {}, "delta_max": None, "delta_cons": None,
           "items_build": [], "items_variantes": [], "sistemas": [], "lab_note": None,
           "build_display": entry.get("build_display", []), "cuantificado": False,
           "hook_motivo": entry.get("hook_motivo", ""),
           "veredicto": "SIN_IMPACTO", "razones": [], "hook": entry.get("hook")}

    # 0) ¿el reporte ya declara cubrir este parche (o uno posterior)?
    pd = _max_patch(entry.get("parche_declarado"))
    if pd and patch_key(pd) >= patch_key(patch):
        out["veredicto"] = "AL_DIA"
        out["razones"].append(f"el reporte ya declara datos {pd} ≥ {patch}")
        return out

    # 1) cambio directo al campeón
    for nombre, c in cs["champions"].items():
        if _norm(nombre) == _norm(entry["champion_display"]):
            out["directo"] = {"nombre": nombre, **c}
            break

    # 2) ítems cambiados ∩ build final / ∩ texto (variantes, rechazados, apéndices)
    build_norm = {_norm(b) for b in entry["build_display"]}
    for nombre in cs["items"]:
        variantes = [nombre] + expandir_nombre_item(nombre)
        en_build = any(_norm(v) in build_norm for v in variantes)
        if en_build:
            out["items_build"].append(nombre)
        else:
            m = _mencionado(tl, nombre)
            if m:
                out["items_variantes"].append(f"{nombre} ({cs['items'][nombre]['tipo']})")

    # 3) sistemas relevantes al rol + nota humana del diff
    out["sistemas"] = sistemas_relevantes(entry.get("rol", ""), cs)
    out["lab_note"] = lab_note_para(archivo, cs)

    # 4) cuantificación
    toca_spec = bool(out["directo"] and any(k in _norm(out["directo"]["detalles"]) for k in SPEC_INPUT_KEYWORDS))
    if entry.get("hook") and not entry.get("sin_resolver"):
        hook = HOOKS[entry["hook"]]
        actual = _redondear(hook(entry["build_keys"]))
        parser = CHAMP_PARAMS.get(entry["champion"])
        if out["directo"] and parser:
            pp = parser(out["directo"]["detalles"], patch)
            if pp:
                pre, post, post_cons = pp
                m_pre = hook(entry["build_keys"], params=pre)
                m_post = hook(entry["build_keys"], params=post)
                m_cons = hook(entry["build_keys"], params=post_cons)
                for k in m_pre:
                    if isinstance(m_pre[k], (int, float)) and m_pre[k]:
                        out["delta"][k] = round((m_cons[k] - m_pre[k]) / abs(m_pre[k]) * 100, 2)
                out["pre"], out["post"], out["post_cons"] = _redondear(m_pre), _redondear(m_post), _redondear(m_cons)
                res_keys = RESULT_KEYS.get(entry["hook"], tuple(out["delta"]))
                out["delta_resultado"] = {k: v for k, v in out["delta"].items() if k in res_keys}
                out["delta_input"] = {k: v for k, v in out["delta"].items() if k not in res_keys}
                out["delta_max"] = max((abs(v) for v in out["delta_resultado"].values()), default=0.0)
                out["delta_cons"] = out["delta_max"]     # el conservador YA es el del dict
                out["cuantificado"] = True
        elif not out["directo"] and not out["items_build"]:
            out["delta_max"] = 0.0
        out["metricas_actuales"] = actual

    # 5) veredicto (rúbrica determinista)
    d = out["delta_max"]
    if toca_spec:
        out["veredicto"] = "REGENERAR"
        out["razones"].append("cambio directo a inputs del spec (AD/AS/defensas base o growth)")
    elif d is not None and d >= UMBRAL_REGENERAR:
        out["veredicto"] = "REGENERAR"
        out["razones"].append(f"Δ de resultado {d:.1f} % ≥ umbral {UMBRAL_REGENERAR:.0f} %")
    elif out["items_build"]:
        out["veredicto"] = "REVISAR"
        out["razones"].append("ítem(s) de la build final cambiados: " + ", ".join(out["items_build"]))
    elif out["directo"] and (not entry.get("hook") or not out["cuantificado"]):
        out["veredicto"] = "REVISAR"
        out["razones"].append("cambio directo sin cuantificación automática "
                              f"({entry.get('hook_motivo') or 'sin parser de parámetros pre/post para este cambio'})")
    elif d is not None and d >= UMBRAL_ANOTAR:
        out["veredicto"] = "REVISAR"
        out["razones"].append(f"Δ de resultado {d:.1f} % ≥ umbral {UMBRAL_ANOTAR:.0f} %")
    elif out["directo"] or d or out["items_variantes"] or out["sistemas"]:
        out["veredicto"] = "ANOTAR"
        if out["directo"]:
            out["razones"].append(f"cambio directo ({out['directo']['tipo']}) con impacto medido "
                                  f"{d if d is not None else '—'} % < umbral {UMBRAL_ANOTAR:.0f} %")
        if out["items_variantes"]:
            out["razones"].append("ítems de variantes/rechazados cambiados (nota informativa)")
        if out["sistemas"]:
            out["razones"].append("cambios sistémicos relevantes al rol (cualitativos, refuerzan o no cambian la build)")
    else:
        out["veredicto"] = "SIN_IMPACTO"
        out["razones"].append("el parche no toca champion, build, ni sistemas del rol")
    return out


def triage_todos(reg, patch=None, ruta=None):
    rutas = {p: r for p, r, k in cambios_archivos()}
    patch = patch or ultimo_parche_hotfix()[0]
    if not patch or patch not in rutas:
        sys.exit(f"No hay diff estructurado (cambios_<patch>.md) para el parche {patch!r}. "
                 f"Disponibles: {sorted(rutas)}")
    cs = parse_cambios(ruta or rutas[patch])
    return patch, cs, [triage_reporte(f, e, cs, patch) for f, e in sorted(reg["reportes"].items())]


# ================================================================ anotación
def bloque_verificacion(t, fecha=None):
    """Bloque markdown idempotente (marcadores HTML) con el resultado del triage."""
    fecha = fecha or datetime.date.today().strftime("%d/%m/%Y")
    v = t["veredicto"]
    icono = VEREDICTOS[v]
    regen = v in ("REGENERAR",)
    revisar = v == "REVISAR"
    titulo = (f"❌ REQUIERE REGENERACIÓN — hotfix {t['patch']}" if regen else
              f"⚠️ REQUIERE REVISIÓN ACOTADA — hotfix {t['patch']}" if revisar else
              f"NO requiere regeneración — hotfix {t['patch']}")
    L = [f"<!-- WRLAB-VERIF:{t['patch']}:START — generado por model/update_reports.py · no editar a mano -->",
         f"> [!NOTE] {icono} Verificación automática ({fecha}) — **{titulo}**"]
    if t["directo"]:
        L.append(f"> **Cambio directo:** {t['directo']['tipo']} — {t['directo']['detalles'][:220]}.")
    else:
        L.append(f"> **Cambios directos a {t['champion']}:** ninguno en {t['patch']}.")
    if t.get("delta"):
        pares = []
        for k, dv in sorted(t.get("delta_resultado", {}).items(), key=lambda x: -abs(x[1]))[:5]:
            if abs(dv) >= 0.05:
                pares.append(f"{k} {t['pre'][k]:g}→{t['post_cons'][k]:g} ({dv:+.1f} %)")
        inp = [f"{k} ({dv:+.1f} %)" for k, dv in t.get("delta_input", {}).items() if abs(dv) >= 0.05]
        if pares:
            L.append(f"> **Δ de resultado (conservador):** {' · '.join(pares)}. "
                     f"Δ máx **{t['delta_max']:.1f} %** (umbrales: anotar {UMBRAL_ANOTAR:.0f} %, regenerar {UMBRAL_REGENERAR:.0f} %).")
            dif_full = {k: (t['pre'][k], t['post'][k]) for k in t.get("delta_resultado", {})
                        if abs(t['post'][k] - t['post_cons'][k]) > 0.05}
            if dif_full:
                extra = " · ".join(f"{k} {a:g}→{b:g}" for k, (a, b) in list(dif_full.items())[:3])
                L.append(f"> **Con la fórmula completa post-parche:** {extra} (el veredicto usa el caso conservador).")
        else:
            L.append("> **Δ de resultado:** 0 % en todas las métricas clave del reporte.")
        if inp:
            L.append(f"> **Δ de stats-input (no decide veredicto):** {', '.join(inp[:4])}.")
    elif t.get("hook"):
        L.append("> **Δ del modelo:** 0 % — ningún input del campeón/build cambió en el motor.")
    else:
        motivo = t.get("hook_motivo") or "modelo no conectado para este campeón"
        L.append(f"> **Modelo:** sin hook cuantitativo ({motivo}) → triage por intersección "
                 f"(champion/ítems/sistemas). Métricas publicadas sin cambios medibles.")
    if t.get("build_display"):
        slots = " + ".join(t["build_display"][:6])
        L.append(f"> **Build publicada (6 slots, Ley 0):** {slots} — **sin cambios**.")
    else:
        L.append("> **Build publicada:** no extraíble automáticamente del formato del vault → "
                 "triage cualitativo (intersección champion/ítems/sistemas).")
    if t["items_variantes"]:
        L.append(f"> **Ítems cambiados fuera de la build final:** {', '.join(t['items_variantes'])} "
                 f"— verificar variantes/rechazados del reporte.")
    for s in t["sistemas"][:3]:
        L.append(f"> **Sistema ({t['patch']}):** {s[:240]}")
    if t["lab_note"]:
        L.append(f"> **Nota del lab (diff {t['patch']}):** {t['lab_note'][:260]}")
    cierre = ("regenerar por el flujo FRAMEWORK (10 pasos, con apoyo de model/optimize_build.py "
              "para re-derivar la build óptima) y re-baselinar." if regen else
              "revisión manual acotada (matriz último slot / rechazados); la build NO se re-deriva." if revisar else
              "build, ruta de compra y veredictos siguen vigentes; este bloque es la constancia de verificación.")
    L.append(f"> **Veredicto:** {icono} — {cierre}")
    L.append(f"<!-- WRLAB-VERIF:{t['patch']}:END -->")
    return "\n".join(L)




def insertar_bloque(txt, bloque, patch):
    """Idempotente a nivel de bytes:
    - si ya existe el bloque del mismo parche → lo reemplaza in-place (normaliza espacios previos);
    - si existen bloques de otros parches → inserta después del último;
    - si no → inserta tras el bloque de metadatos (antes del primer callout '> [!' o '## ')."""
    pat = re.compile(rf"\n*<!-- WRLAB-VERIF:{re.escape(patch)}:START.*?<!-- WRLAB-VERIF:{re.escape(patch)}:END -->", re.S)
    if pat.search(txt):
        return pat.sub(lambda _m: "\n\n" + bloque, txt, count=1)
    ends = list(re.finditer(r"<!-- WRLAB-VERIF:[^:>]+:END -->", txt))
    if ends:
        i = ends[-1].end()
        return txt[:i] + "\n\n" + bloque + "\n\n" + txt[i:].lstrip("\n")
    m = re.search(r"^> \[!", txt, flags=re.M) or re.search(r"^## ", txt, flags=re.M)
    if not m:
        return txt.rstrip() + "\n\n" + bloque + "\n"
    i = m.start()
    return txt[:i].rstrip("\n") + "\n\n" + bloque + "\n\n" + txt[i:]


# ================================================================ refresh (aplicar números nuevos)
def variantes_num(pre, post):
    """Pares (cadena_pre, cadena_post) con los formatos de número del estándar v1.4
    (entero, entero con espacio de miles, 1 decimal) para reemplazo 1:1."""
    pares = []
    rp, rq = round(pre), round(post)
    if rp != rq:
        pares.append((str(rp), str(rq)))
        f = lambda n: f"{n:,}".replace(",", " ")
        if rp >= 1000:
            pares.append((f(rp), f(rq)))
    for dec in (1, 2):
        a, b = f"{pre:.{dec}f}", f"{post:.{dec}f}"
        if a != b:
            pares.append((a, b))
    return pares


def refresh_texto(txt, delta, pre, post_cons, max_hits=3):
    """Actualiza los números reproducibles DENTRO de la sección '### Resultado del modelo'
    (y su cita titular). Devuelve (nuevo_txt, cambios). Si la sección no existe o ningún
    número publicado coincide 1:1 con el modelo, no toca nada (honestidad: la anotación
    WRLAB-VERIF sigue siendo la constancia del Δ)."""
    m = re.search(r"(###\s+Resultado del modelo.*?)(?=\n---|\n## )", txt, re.S)
    if not m:
        return txt, []
    seccion = m.group(1)
    nueva = seccion
    cambios = []
    for k, dv in sorted(delta.items(), key=lambda x: -abs(x[1])):
        if abs(dv) < 0.05 or k not in pre or k not in post_cons:
            continue
        for pre_s, post_s in variantes_num(pre[k], post_cons[k]):
            hits = len(re.findall(rf"(?<![\d.,]){re.escape(pre_s)}(?![\d])", nueva))
            if 0 < hits <= max_hits:
                nueva = re.sub(rf"(?<![\d.,]){re.escape(pre_s)}(?![\d])", post_s, nueva)
                cambios.append((k, pre_s, post_s, hits))
    if cambios:
        txt = txt[:m.start(1)] + nueva + txt[m.end(1):]
    return txt, cambios


def cmd_refresh(args):
    reg = cargar_registro()
    patch, cs, resultados = triage_todos(reg, patch=args.patch)
    solo = set(args.solo.split(",")) if args.solo else None
    for t in resultados:
        if solo and t["archivo"] not in solo:
            continue
        ruta = os.path.join(REPORTES, t["archivo"])
        if t["veredicto"] == "REGENERAR":
            print(f"❌ {t['archivo']}: veredicto REGENERAR — refresh NO aplica "
                  f"(usa 'borrador' y el flujo FRAMEWORK)")
            continue
        if not t.get("delta") or not any(abs(v) >= 0.05 for v in t["delta"].values()):
            motivo = ("sin modelo cuantitativo (triage cualitativo)" if not t.get("hook")
                      else "Δ 0 % — nada que refrescar")
            print(f"=  {t['archivo']}: {motivo}")
            continue
        with open(ruta, encoding="utf-8") as fh:
            txt = fh.read()
        nuevo, cambios = refresh_texto(txt, t["delta"], t["pre"], t["post_cons"])
        if not cambios:
            print(f"⚠️  {t['archivo']}: Δ {t['delta_max']:.1f} % medido, pero sus números publicados "
                  f"no son reproducibles 1:1 por el motor — sin auto-refresh (la anotación "
                  f"WRLAB-VERIF documenta el Δ)")
            continue
        desc = ", ".join(f"{k}: {a}→{b} (×{n})" for k, a, b, n in cambios)
        if args.apply:
            with open(ruta, "w", encoding="utf-8") as fh:
                fh.write(nuevo)
            print(f"✍️  {t['archivo']}: números actualizados — {desc}")
        else:
            print(f"── {t['archivo']} (dry-run): {desc}")
    if args.apply:
        print("\nRecuerda: python3 model/build_bundles.py && python3 -m unittest discover -s tests")


# ================================================================ borrador (para ❌ REGENERAR)
def _fila_csv(rel, champ):
    import csv as _csv
    with open(os.path.join(ROOT, *rel.split("/")), encoding="utf-8", newline="") as fh:
        for fila in _csv.reader(fh):
            if fila and fila[0].strip().lower() == champ.lower():
                return fila
    return None


def _esqueleto_template():
    tpl = leer_md(os.path.join(ROOT, "metodologia", "TEMPLATE_REPORTE.md"))
    m = re.search(r"## B\. ESQUELETO CANÓNICO.*?```markdown\n(.*?)```", tpl, re.S)
    return m.group(1).rstrip() if m else "(copiar el esqueleto de metodologia/TEMPLATE_REPORTE.md §B)"


def leer_md(ruta):
    with open(ruta, encoding="utf-8") as fh:
        return fh.read()


def cmd_borrador(args):
    reg = cargar_registro()
    patch, cs, resultados = triage_todos(reg, patch=args.patch)
    outdir = os.path.join(REPORTES, "_borradores")
    os.makedirs(outdir, exist_ok=True)
    hoy = datetime.date.today().strftime("%d/%m/%Y")
    generados = 0
    for t in resultados:
        if t["veredicto"] != "REGENERAR":
            continue
        entry = reg["reportes"][t["archivo"]]
        champ = t["champion"]
        stem = re.sub(r"\.md$", "", t["archivo"]).replace(" ", "_")
        partes = [f"""---
tags:
  - BORRADOR
version: 0.1
Status: Borrador
champion: {champ}
patch: "{patch}"
---
# ⚠️ BORRADOR DE REGENERACIÓN — {champ} ({patch}) · generado {hoy} por update_reports.py

> [!DANGER] Por qué existe este borrador
> El reporte publicado `{t['archivo']}` recibió veredicto **❌ REGENERAR** contra {patch}:
> {'; '.join(t['razones'])}.
> **Cambio directo:** {t['directo']['detalles'] if t['directo'] else '—'}

## 1. DATOS NUEVOS DEL PARCHE (fuente: data/estructurada/cambios_{patch}.md)

| Entidad | Tipo | Cambio |
|---|---|---|"""]
        if t["directo"]:
            partes.append(f"| **{champ}** | {t['directo']['tipo']} | {t['directo']['detalles']} |")
        for it in t["items_build"] + [v.split(" (")[0] for v in t["items_variantes"]]:
            if it in cs["items"]:
                partes.append(f"| {it} | {cs['items'][it]['tipo']} | {cs['items'][it]['detalles'][:160]} |")
        for srow in t["sistemas"]:
            partes.append(f"| (sistema) | — | {srow[:200]} |")
        partes.append("")
        as_row = _fila_csv("data/estructurada/champion_attack_speed_7.3.csv", champ)
        dur_row = _fila_csv("data/estructurada/champion_durability_7.3.csv", champ)
        partes.append("## 2. FICHA BASE (datos del lab)")
        if as_row:
            partes.append("- **AS oficial (7.3, overrides " + patch + " marcados):** `" + ", ".join(as_row) + "`")
        if dur_row:
            partes.append("- **Durabilidad (cambios 7.3):** `" + ", ".join(dur_row) + "`")
        spec = M.CHAMPS.get(entry["champion"])
        if spec:
            partes.append(f"- **ChampSpec precargado:** AD {spec.base_ad}+{spec.ad_growth}/nv · "
                          f"AS ratio {spec.as_ratio} · bonus base {spec.base_bonus_as} · "
                          f"AS/nv {spec.as_per_lvl} — ⚠️ revisar contra el diff de arriba antes de regenerar")
        else:
            partes.append("- **ChampSpec:** NO existe en `model/champspecs.py` — crearlo desde el "
                          "apéndice AS de las notas oficiales + wiki (FRAMEWORK §A paso 2)")
        partes.append(f"""
## 3. CÓMO REGENERAR (flujo FRAMEWORK §A de 10 pasos)

1. Actualizar el spec/datos con los valores de §1 (fuente primaria: notas oficiales {patch}).
2. Re-derivar candidatos: {'`python3 model/optimize_build.py ' + entry['champion'] + ' --validar --top 8`' if spec else 'crear primero el ChampSpec (paso 2 de FRAMEWORK §A) y luego `python3 model/optimize_build.py ' + entry['champion'] + ' --validar --top 8`; si el arquetipo no es de autos, comparar candidatas con analysis_batch2'}.
   Verificar también a mano contra las candidatas del reporte original (§8).
3. Rellenar el esqueleto TEMPLATE (§B) abajo, o generar el reporte completo en un chat
   externo con el bundle `WR-LAB_completo.md`.
4. Sustituir `reportes/{t['archivo']}` por la versión nueva (o decidir mantenerla con el
   bloque ❌ visible), luego:
   `python3 model/update_reports.py baseline && python3 model/update_reports.py annotate --patch {patch} --apply`
5. `python3 model/build_bundles.py && python3 -m unittest discover -s tests` y commit.

## 4. ESQUELETO DEL REPORTE NUEVO (TEMPLATE v1.4 §B)

```markdown
{_esqueleto_template().replace("{champion}", champ).replace("{patch}", patch)}
```
""")
        destino = os.path.join(outdir, f"{stem}_{patch}_REGENERAR.md")
        with open(destino, "w", encoding="utf-8") as fh:
            fh.write("\n".join(partes))
        generados += 1
        print(f"📝 {os.path.relpath(destino, ROOT)}")
    if not generados:
        print(f"Ningún reporte con veredicto ❌ REGENERAR contra {patch} — nada que borrador.")



# ================================================================ comandos
def cmd_baseline(args):
    reg = construir_registro()
    # conservar sellos previos si el registro ya existía
    if os.path.exists(REGISTRY) and not args.force:
        with open(REGISTRY, encoding="utf-8") as fh:
            viejo = json.load(fh)
        for f, e in reg["reportes"].items():
            if f in viejo.get("reportes", {}):
                # v1.15.2: el sello DERIVADO del frontmatter (construir_registro)
                # manda; el registry viejo solo es fallback si el frontmatter
                # no lo declara. Antes el preserve pisaba al derivado y el
                # orden baseline-después-de-annotate dejaba el vault "sin
                # verificar" (incidente CI 08/10).
                e["ultima_verificacion"] = (
                    e.get("ultima_verificacion")
                    or viejo["reportes"][f].get("ultima_verificacion")
                )
    guardar_registro(reg)
    for f, e in sorted(reg["reportes"].items()):
        mets = e["metricas"]
        s = " · ".join(f"{k}={v:g}" for k, v in list(mets.items())[:6]) if mets else f"SIN HOOK ({e['hook_motivo'][:60]})"
        print(f"  {f:<44} {e['champion_display']:<8} {e['modelo']:<9} {s}")


def cmd_triage(args):
    reg = cargar_registro()
    patch, cs, resultados = triage_todos(reg, patch=args.patch)
    print(f"\n=== TRIAGE hotfix {patch} ({os.path.basename(cs['raw'])}) sobre {len(resultados)} reportes ===")
    print(f"{'REPORTE':<44}{'CHAMP':<9}{'DIRECTO':<9}{'Δmax':>7}  {'ÍTEMS BUILD':<12}{'VEREDICTO'}")
    for t in resultados:
        dmax = f"{t['delta_max']:.1f} %" if t["delta_max"] is not None else "—"
        directo = t["directo"]["tipo"][:8] if t["directo"] else "—"
        ib = ",".join(t["items_build"])[:11] or "—"
        print(f"{t['archivo']:<44}{t['champion']:<9}{directo:<9}{dmax:>7}  {ib:<12}{VEREDICTOS[t['veredicto']]}")
        for r in t["razones"]:
            print(f"    └─ {r}")
    n_reg = sum(1 for t in resultados if t["veredicto"] == "REGENERAR")
    n_rev = sum(1 for t in resultados if t["veredicto"] == "REVISAR")
    print(f"\nResumen: {len(resultados) - n_reg - n_rev} reportes NO requieren regeneración · "
          f"{n_rev} revisión acotada · {n_reg} regeneración completa.")
    return resultados


def cmd_annotate(args):
    reg = cargar_registro()
    patch, cs, resultados = triage_todos(reg, patch=args.patch)
    solo = set(args.solo.split(",")) if args.solo else None
    fecha = args.fecha or datetime.date.today().strftime("%d/%m/%Y")
    for t in resultados:
        if solo and t["archivo"] not in solo:
            continue
        if t["veredicto"] == "AL_DIA":
            print(f"⏩ {t['archivo']}: ya declara datos {t['patch']} o posteriores — sin bloque")
            reg["reportes"][t["archivo"]]["ultima_verificacion"] = {
                "patch": t["patch"], "fecha": fecha, "veredicto": "AL_DIA", "delta_max_pct": None}
            continue
        bloque = bloque_verificacion(t, fecha)
        ruta = os.path.join(REPORTES, t["archivo"])
        if args.apply:
            with open(ruta, encoding="utf-8") as fh:
                txt = fh.read()
            nuevo = insertar_bloque(txt, bloque, patch)
            if nuevo != txt:
                with open(ruta, "w", encoding="utf-8") as fh:
                    fh.write(nuevo)
                print(f"✍️  {t['archivo']}: bloque {patch} insertado/actualizado ({VEREDICTOS[t['veredicto']]})")
            else:
                print(f"=  {t['archivo']}: sin cambios (bloque ya vigente)")
            reg["reportes"][t["archivo"]]["ultima_verificacion"] = {
                "patch": patch, "fecha": fecha, "veredicto": t["veredicto"],
                "delta_max_pct": t["delta_max"]}
        else:
            print(f"\n────── {t['archivo']} ({VEREDICTOS[t['veredicto']]}) — dry-run ──────")
            print(bloque)
    if args.apply:
        guardar_registro(reg)
        print("\nRegistro sellado. Corre 'python3 -m unittest discover -s tests' y commitea reportes+registro.")


def cmd_check(args):
    reg = cargar_registro()
    fallos = []
    # 1) drift motor ↔ registro
    for f, e in sorted(reg["reportes"].items()):
        if not e.get("hook") or e.get("sin_resolver") or not e.get("metricas"):
            continue
        act = _redondear(HOOKS[e["hook"]](e["build_keys"]))
        for k, v in e["metricas"].items():
            if isinstance(v, (int, float)) and v and k in act:
                drift = abs(act[k] - v) / abs(v) * 100
                if drift > 0.5:
                    fallos.append(f"{f}: drift en {k} ({v:g} → {act[k]:g}, {drift:.1f} %) — "
                                  f"¿datos del motor cambiaron? Documenta y corre 'baseline'.")
    # 2) reportes sin triar contra el último hotfix
    patch, _ = ultimo_parche_hotfix()
    if patch:
        for f, e in sorted(reg["reportes"].items()):
            pd = _max_patch(e.get("parche_declarado"))
            if pd and patch_key(pd) >= patch_key(patch):
                continue                      # el reporte ya cubre el parche
            uv = e.get("ultima_verificacion")
            if not uv or patch_key(uv["patch"]) < patch_key(patch):
                fallos.append(f"{f}: sin verificar contra {patch} — corre "
                              f"'update_reports.py triage/annotate --patch {patch} --apply'.")
    if fallos:
        print("❌ CHECK FALLÓ:")
        for x in fallos:
            print("  -", x)
        sys.exit(1)
    print(f"✅ check OK: {len(reg['reportes'])} reportes sin drift y verificados contra {patch}.")


def main():
    ap = argparse.ArgumentParser(description="WR-LAB · triador/actualizador de reportes publicados")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("baseline", help="(re)construir el registro de reportes+golden metrics")
    b.add_argument("--force", action="store_true", help="no conservar sellos de verificación previos")
    t = sub.add_parser("triage", help="cuantificar impacto de un parche sobre los reportes")
    t.add_argument("--patch", default=None)
    a = sub.add_parser("annotate", help="generar/insertar bloques de verificación")
    a.add_argument("--patch", default=None)
    a.add_argument("--apply", action="store_true", help="escribir en los reportes (default: dry-run)")
    a.add_argument("--solo", default=None, help="solo estos archivos (coma-separados)")
    a.add_argument("--fecha", default=None, help="fecha del sello (dd/mm/aaaa)")
    rf = sub.add_parser("refresh", help="aplicar los números post-parche dentro de los reportes (solo si el motor los reproduce 1:1)")
    rf.add_argument("--patch", default=None)
    rf.add_argument("--apply", action="store_true")
    rf.add_argument("--solo", default=None)
    bo = sub.add_parser("borrador", help="generar esqueletos de regeneración en reportes/_borradores/ (veredictos ❌)")
    bo.add_argument("--patch", default=None)
    sub.add_parser("check", help="modo CI: drift + verificaciones pendientes")
    args = ap.parse_args()
    {"baseline": cmd_baseline, "triage": cmd_triage, "annotate": cmd_annotate,
     "refresh": cmd_refresh, "borrador": cmd_borrador, "check": cmd_check}[args.cmd](args)


if __name__ == "__main__":
    main()
