# -*- coding: utf-8 -*-
"""
WR-LAB · check_patch.py — vigilante de parches + win rates (v1.11).
Detecta: (1) cambios de CONTENIDO en la página oficial 7.3 (hash de texto normalizado,
inmune al ruido dinámico del CMS/nav), (2) publicación de páginas 7.3a/7.3b/7.4,
(3) nuevas entradas de change-history en wr-meta para campeones centinela,
(4) ACTUALIZA LAS WIN RATES DEL ROSTER (wr-meta, bloque "Meta Overview", bucket
    Diamond+ por defecto) en el MISMO proceso: escribe data/estructurada/
    champion_winrates.csv/.md (fuente de verdad de los callouts meta de los reportes)
    y alerta cuando un campeón se mueve ≥ UMBRAL_WINRATE_PTS puntos.
Estado persistente en data/raw/.watch_state.json. Exit 1 si hay cambios (útil para CI/cron).

Historia: hasta v1.5 hasheaba el HTML crudo → falsos positivos por el listados de
"artículos relacionados" y tokens del CMS (29-sep-2026: md5 distinto con contenido idéntico).
Desde v1.6 el hash es del TEXTO del artículo, cortado antes del pie dinámico.
Desde v1.11 las win rates viajan en el mismo ciclo del vigía (petición del autor:
"dato vital siempre actualizado, fundamental para los reportes").

Uso:  python3 model/check_patch.py [--quiet] [--winrates-only] [--roster full]
      --roster full     refresco masivo de TODO el roster conocido (manual)
      --winrates-only   solo el paso 4 (refresco manual: wrlab.py winrates)
"""
import csv, datetime, hashlib, html as htmllib, io, json, os, re, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "data", "raw", ".watch_state.json")
OFFICIAL = "https://wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-{slug}/"
CANDIDATES = ["7-3b", "7-3c", "7-4", "7-4a", "7-5", "7-3b-hotfix"]
WATCH_PAGES = ["7-3", "7-3a"]        # páginas activas: vigilar cambios de CONTENIDO
WRMETA_SENTINELS = {"jinx": "39-jinx", "caitlyn": "317-caitlyn", "hwei": "505-hwei",
                    "yuumi": "321-yuumi", "kalista": "349-kalista", "malphite": "47-malphite"}
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0"}

# ---------------------------------------------------------------- win rates (paso 4, v1.11)
WRMETA_PAGE = "https://wr-meta.com/{pid}-{slug}.html"
WRMETA_SITEMAP = "https://wr-meta.com/sitemap.xml"
WINRATES_CSV = os.path.join(ROOT, "data", "estructurada", "champion_winrates.csv")
WINRATES_MD = os.path.join(ROOT, "data", "estructurada", "champion_winrates.md")
UMBRAL_WINRATE_PTS = 2.0     # |Δ win rate| en puntos que merece alerta (el ruido diario es menor)
PAUSA_ENTRE_PETICIONES = 0.35  # s — cortesía con wr-meta

# Roster vigilado: campeones de los 16 reportes del vault + los 13 specs del lab
# (el registro de reportes añade automáticamente cualquier campeón nuevo).
WINRATE_ROSTER = ["ahri", "caitlyn", "chogath", "diana", "heimerdinger", "jinx", "kalista",
                  "karma", "malphite", "mordekaiser", "nocturne", "norra", "orianna",
                  "rammus", "seraphine", "shyvana", "sivir", "syndra", "volibear",
                  "yunara", "yuumi"]

# IDs de página wr-meta conocidos (FUENTES.md + verificados en vivo el 01/10/2026).
# Lo que falte se descubre con el sitemap y se persiste en state["wrmeta_ids"].
# v1.15.3: mapa COMPLETO del roster de wr-meta (sitemap 09/10). Antes solo los
# campeones estudiados: una guía nueva de un campeón ajeno al lab no tenía
# win rates ni id (fricción real al crear Xayah). Con el mapa completo,
# `wrlab.py winrates --roster full` puebla el CSV de todo el roster y el
# vigía sigue vigilando solo el subconjunto de WINRATE_ROSTER + registro.
WRMETA_IDS = {
              "aatrox": "332", "ahri": "1", "akali": "2", "akshan": "311", "alistar": "42", "ambessa": "528",
              "amumu": "46", "ancient-coin": "435", "anivia": "333", "annie": "45", "aphelios": "334", "ashe": "41",
              "aurelion-sol": "24", "aurora": "526", "azir": "335", "bard": "336", "belveth": "337", "berserkers-greaves": "431",
              "blitzcrank": "43", "boots-of-dynamism": "433", "boots-of-mana": "432", "brand": "313", "braum": "44", "briar": "497",
              "caitlyn": "317", "camille": "18", "cassiopeia": "338", "chempunk-chainsword": "421", "chogath": "339", "corki": "57",
              "darius": "49", "diana": "216", "dr-mundo": "17", "draven": "51", "duskblade-of-draktharr": "66", "ekko": "328",
              "elise": "340", "evelynn": "10", "ezreal": "40", "fiddlesticks": "341", "fiora": "9", "fizz": "8",
              "galio": "238", "gangplank": "342", "garen": "13", "gnar": "343", "gragas": "26", "graves": "14",
              "gwen": "344", "heartsteel": "504", "hecarim": "345", "heimerdinger": "346", "horizon-focus": "420", "hwei": "505",
              "ignite": "493", "illaoi": "347", "irelia": "282", "ivern": "348", "janna": "28", "jarvan-iv": "16",
              "jax": "15", "jayce": "316", "jhin": "27", "jinx": "39", "kaisa": "5", "kalista": "349",
              "karma": "323", "karthus": "350", "kassadin": "329", "katarina": "211", "kayle": "319", "kayn": "351",
              "kennen": "58", "kha-zix": "253", "kindred": "352", "kled": "353", "kogmaw": "354", "ksante": "419",
              "leblanc": "355", "lee-sin": "6", "leona": "215", "lillia": "356", "lissandra": "357", "locke": "577",
              "lucian": "295", "lulu": "56", "lux": "30", "malphite": "47", "malzahar": "361", "maokai": "364",
              "master-yi": "7", "mejais-soulstealer": "499", "mel": "536", "milio": "426", "miss-fortune": "31", "mordekaiser": "365",
              "morgana": "318", "naafiri": "488", "nami": "32", "nashors-talon": "429", "nasus": "20", "nautilus": "327",
              "neeko": "366", "nidalee": "367", "nilah": "368", "nocturne": "382", "noonquiver": "430", "norra": "552",
              "nunu-amp-willump": "314", "olaf": "21", "orianna": "33", "ornn": "383", "pantheon": "217", "poppy": "384",
              "pyke": "326", "qiyana": "385", "quinn": "386", "rakan": "166", "rammus": "242", "reksai": "387",
              "rell": "388", "renata-glasc": "389", "renekton": "264", "rengar": "252", "riven": "283", "rumble": "390",
              "runaans-hurricane": "64", "ryze": "391", "samira": "330", "sejuani": "392", "senna": "296", "seraphine": "34",
              "sett": "320", "shaco": "393", "shen": "322", "shimmering-spark": "437", "shyvana": "23", "singed": "35",
              "sion": "331", "sivir": "394", "skarner": "395", "smolder": "506", "sona": "36", "soraka": "37",
              "swain": "396", "sylas": "397", "syndra": "398", "tahm-kench": "399", "talisman-of-ascension": "436", "taliyah": "400",
              "talon": "401", "taric": "402", "teemo": "59", "the-collector": "428", "thresh": "312", "tristana": "55",
              "trundle": "403", "tryndamere": "22", "twisted-fate": "38", "twitch": "404", "udyr": "405", "urgot": "406",
              "varus": "25", "vayne": "3", "vejgar": "315", "velkoz": "407", "vex": "381", "vi": "12",
              "viego": "408", "viktor": "409", "vladimir": "410", "volibear": "411", "vukong": "50", "warwick": "362",
              "xayah": "165", "xerath": "412", "xin-zhao": "19", "yasuo": "11", "yone": "363", "yorick": "413",
              "yunara": "545", "yuumi": "321", "zaahen": "551", "zac": "414", "zed": "4", "zeri": "415",
              "ziggs": "29", "zilean": "416", "zoe": "417", "zyra": "418"}

DISPLAY = {"chogath": "Cho'Gath"}    # el resto: title()

CSV_COLS = ["champion", "role", "tier", "win_pct", "pick_pct", "ban_pct",
            "trend", "confidence", "bucket", "updated_utc", "actualizado"]


def get(url, t=25):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=t) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return f"ERR:{type(e).__name__}", b""

def content_md5(body):
    """Hash del CONTENIDO de la nota: sin scripts/estilos/etiquetas, cortado en
    'Related Articles' (carrusel dinámico) y sin líneas de fecha ISO (metadata que
    rota por visita). Verificado estable entre descargas consecutivas (29-sep-2026)."""
    t = body.decode("utf-8", "ignore")
    t = re.sub(r"<script[^>]*>.*?</script>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<style[^>]*>.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", "\n", t)
    t = htmllib.unescape(t)
    lines = [re.sub(r"\s+", " ", l).strip() for l in t.split("\n")]
    lines = [l for l in lines if l]
    for i, l in enumerate(lines):
        if l == "Related Articles":
            lines = lines[:i]
            break
    lines = [l for l in lines if not re.match(r"^\d{4}-\d{2}-\d{2}T", l)]
    return hashlib.md5("\n".join(lines).encode()).hexdigest()

def load_state():
    if os.path.exists(STATE):
        st = json.load(open(STATE))
        st.setdefault("official_73_content_md5", None)
        st.setdefault("winrates", {})
        st.setdefault("wrmeta_ids", {})
        return st
    return {"official_73_md5": None, "official_73_content_md5": None,
            "new_pages": [], "changelog_dates": {}, "last_check": None,
            "winrates": {}, "wrmeta_ids": {}}


# ---------------------------------------------------------------- pasos 1-3: parches
def chequear_parches(state, findings):
    # 1) ¿el CONTENIDO de las páginas oficiales activas cambió? (7-3 y 7-3a)
    for slug in WATCH_PAGES:
        st, body = get(OFFICIAL.format(slug=slug))
        if st != 200:
            continue
        cmd5 = content_md5(body)
        key = f"content_{slug}"
        prev_c = state.get(key)
        if prev_c and cmd5 != prev_c:
            findings.append(f"CONTENIDO de la página oficial {slug} MODIFICADO (content-md5 {prev_c[:8]} → {cmd5[:8]})")
        state[key] = cmd5
        if slug == "7-3":
            state["official_73_md5"] = hashlib.md5(body).hexdigest()   # informativo

    # 2) ¿se publicó alguna página nueva de parche?
    for slug in CANDIDATES:
        st2, _ = get(OFFICIAL.format(slug=slug), t=15)
        if st2 == 200 and slug not in state["new_pages"]:
            state["new_pages"].append(slug)
            findings.append(f"NUEVA página oficial de notas: {slug} → descargar y correr protocolo FRAMEWORK §E")
    # las páginas ya vigiladas no deben re-alertarse como "nuevas"
    state["new_pages"] = sorted(set(state["new_pages"]) | set(WATCH_PAGES))

    # 3) change-history de centinelas en wr-meta
    for champ, pageid in WRMETA_SENTINELS.items():
        if not pageid: continue
        st3, body3 = get(f"https://wr-meta.com/{pageid}.html", t=20)
        if st3 != 200: continue
        t = body3.decode("utf-8", "ignore")
        dates = re.findall(r'(\d{1,2}\s+\w{3}\s+2026)\s+\(PATCH\s+([^)]+)\)', t)
        latest = dates[0] if dates else None
        prev = state["changelog_dates"].get(champ)
        if latest and (prev is None or latest[0] != prev[0] or latest[1] != prev[1]):
            if prev is not None:
                findings.append(f"wr-meta {champ}: nuevo change-history {latest} (antes {prev})")
            state["changelog_dates"][champ] = list(latest)


# ---------------------------------------------------------------- paso 4: win rates
def display(champ):
    return DISPLAY.get(champ, champ.title())


def descubrir_ids():
    """{slug: id} desde el sitemap de wr-meta (1 petición). Falla suave: {}."""
    st, body = get(WRMETA_SITEMAP, t=20)
    if st != 200:
        return {}
    t = body.decode("utf-8", "ignore")
    return {name: num for num, name in re.findall(r"(\d+)-([a-z0-9-]+)\.html", t)}


def roster_winrates():
    """WINRATE_ROSTER + campeones del registro de reportes (si existe)."""
    roster = set(WINRATE_ROSTER)
    reg = os.path.join(ROOT, "data", "estructurada", "reportes_registry.json")
    if os.path.exists(reg):
        try:
            datos = json.load(open(reg, encoding="utf-8")).get("reportes", {})
            roster |= {e.get("champion") for e in datos.values() if e.get("champion")}
        except Exception:
            pass
    return sorted(roster)


def parsear_winrates(champ, body):
    """[{role, tier, win_pct, pick_pct, ban_pct, trend, confidence, bucket, updated_utc}]
    del bloque 'Meta Overview' (widget wrCnFsSnapWrap) de una ficha wr-meta.
    Un registro por rol (SOLO/JUNGLE/MID/DUO/SUPPORT). Lista vacía si no está el bloque."""
    t = body.decode("utf-8", "ignore")
    i = t.find("wrCnFsSnapWrap")
    if i < 0:
        return []
    seg = t[i:i + 40000]                       # el widget completo cabe de sobra

    def _uno(pat, chunk, d=""):
        m = re.search(pat, chunk)
        return htmllib.unescape(m.group(1)).strip() if m else d

    bucket = _uno(r'<option value="\d+" selected>([^<]+)</option>', seg, "Diamond +")
    updated = _uno(r"Updated: <b>([^<]+)</b>", seg)
    out, vistos = [], set()
    # cada slide = un rol; el primer trozo es la cabecera del widget
    for chunk in re.split(r"<div class='wr-cn-fs-slide'>", seg)[1:]:
        role = _uno(r"wr-cn-fs-role'><i[^>]*></i><span>([^<]+)</span>", chunk).upper()
        win = _uno(r"<span class='k'>Win:</span>\s*<span class='v[^']*'>([\d.]+)%", chunk)
        if not role or not win or role in vistos:
            continue
        vistos.add(role)
        out.append({
            "champion": display(champ),
            "role": role,
            "tier": _uno(r'wr-tier-ico"[^>]*alt="([^"]*)"', chunk),
            "win_pct": win,
            "pick_pct": _uno(r"<span class='k'>Pick:</span>\s*<span class='v[^']*'>([\d.]+)%", chunk),
            "ban_pct": _uno(r"<span class='k'>Ban:</span>\s*<span class='v[^']*'>([\d.]+)%", chunk),
            "trend": _uno(r"wr-cn-trend[^']*'>([^<]+)<", chunk),
            "confidence": _uno(r"wr-badge wr-conf-[^']*'>([^<]+)<", chunk),
            "bucket": bucket,
            "updated_utc": updated,
        })
    return out


def winrates_csv_text(filas):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=CSV_COLS, lineterminator="\r\n")
    w.writeheader()
    for f in filas:
        w.writerow({k: f.get(k, "") for k in CSV_COLS})
    return buf.getvalue()


def winrates_md_text(filas):
    """Documento legible (el que viaja en el bundle §7b). Misma fuente que el CSV."""
    if not filas:
        return ""
    updated = filas[0].get("updated_utc", "")
    bucket = filas[0].get("bucket", "Diamond +")
    hoy = datetime.date.today().strftime("%d/%m/%Y")
    L = ["# Win rates del roster — wr-meta (Meta Overview)",
         "",
         f"> Bucket: **{bucket}** · Datos wr-meta: **Updated {updated}** · Refrescado por el vigía: {hoy}",
         "> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía",
         "> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día",
         "> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).",
         "> **Los callouts \"Estado Meta Actual\" de los reportes se toman de aquí** (TEMPLATE §A.1);",
         "> alerta del vigía si un campeón se mueve ≥ "
         f"{UMBRAL_WINRATE_PTS:.0f} pts de win rate.",
         "",
         "| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |",
         "|---|---|---|---|---|---|---|---|"]
    for f in filas:
        L.append(f"| {f['champion']} | {f['role']} | {f.get('tier','')} | {f['win_pct']} "
                 f"| {f.get('pick_pct','')} | {f.get('ban_pct','')} | {f.get('trend','')} "
                 f"| {f.get('confidence','')} |")
    L += ["",
          "Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.",
          "Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).",
          "Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento",
          "coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).", ""]
    return "\n".join(L)


def _escribir_si_cambia(ruta, texto):
    """Escribe solo si el contenido cambia (evita commits/fechas parásitos en el vigía)."""
    nuevo = texto.encode("utf-8")
    if os.path.exists(ruta) and open(ruta, "rb").read() == nuevo:
        return False
    with open(ruta, "wb") as fh:
        fh.write(nuevo)
    return True


def deltas_winrate(filas, prev):
    """Findings de drift |Δwin| ≥ umbral contra el estado previo. Nuevo campeón no alerta."""
    findings = []
    for f in filas:
        clave = f"{f['champion']}|{f['role']}"
        try:
            nuevo = float(f["win_pct"])
        except ValueError:
            continue
        anterior = prev.get(clave)
        if anterior is None:
            continue
        d = nuevo - float(anterior)
        if abs(d) >= UMBRAL_WINRATE_PTS:
            findings.append(f"WIN RATE {f['champion']} ({f['role']}, {f['bucket']}): "
                            f"{float(anterior):.2f} → {nuevo:.2f} % ({d:+.2f} pts) — "
                            "re-verificar el callout meta de sus reportes")
    return findings


def actualizar_winrates(state, findings, quiet=False, roster_full=False):
    """Paso 4 del vigía. Devuelve (n_champs_ok, n_filas). Falla suave: si wr-meta no
    responde, conserva los valores previos y NO rompe los pasos 1-3."""
    ids = dict(WRMETA_IDS)
    ids.update(state.get("wrmeta_ids", {}))
    # v1.15.3: modo full = refrescar TODO el roster conocido (poblado inicial,
    # onboarding de campeones nuevos); vigilado = el subset de siempre.
    roster = sorted(ids) if roster_full else roster_winrates()
    faltan = [c for c in roster if c not in ids]
    if faltan:
        descubiertos = descubrir_ids()
        if descubiertos:
            for c in faltan:
                if c in descubiertos:
                    ids[c] = descubiertos[c]
            state["wrmeta_ids"] = {k: v for k, v in ids.items() if k not in WRMETA_IDS}
            faltan = [c for c in roster if c not in ids]

    filas, fallos = [], []
    for n, champ in enumerate(roster):
        pid = ids.get(champ)
        if not pid:
            fallos.append(f"{champ} (sin id wr-meta)")
            continue
        if n:
            time.sleep(PAUSA_ENTRE_PETICIONES)
        st, body = get(WRMETA_PAGE.format(pid=pid, slug=champ), t=20)
        if st != 200:
            fallos.append(f"{champ} (HTTP {st})")
            continue
        rows = parsear_winrates(champ, body)
        if not rows:
            fallos.append(f"{champ} (sin bloque Meta Overview)")
            continue
        filas += rows

    if not filas:
        msg = ("⚠️ win rates: sin datos frescos (wr-meta inaccesible o estructura cambiada) "
               "— se conservan los valores previos" + (f": {', '.join(fallos)}" if fallos else ""))
        print(msg)
        return 0, 0

    hoy = datetime.date.today().isoformat()
    for f in filas:
        f["actualizado"] = hoy
    # drift contra el estado previo (antes de sobrescribirlo).
    # En modo full NO se generan findings: es un refresco masivo manual,
    # no una señal de vigilia (evita 100+ alertas de una vez).
    if not roster_full:
        findings.extend(deltas_winrate(filas, state.get("winrates", {})))
    # escribe CSV + MD solo si los VALORES cambian (la columna 'actualizado' no cuenta:
    # así el vigía no genera commits/fechas parásitos cuando wr-meta no ha movido datos)
    csv_txt = winrates_csv_text(filas)
    anterior = open(WINRATES_CSV, "rb").read().decode("utf-8") if os.path.exists(WINRATES_CSV) else None
    sin_fecha = lambda t: [l.rsplit(",", 1)[0] for l in t.splitlines()]
    if anterior is None or sin_fecha(anterior) != sin_fecha(csv_txt):
        _escribir_si_cambia(WINRATES_CSV, csv_txt)
        _escribir_si_cambia(WINRATES_MD, winrates_md_text(filas))
        if not quiet:
            print(f"✍️  win rates actualizadas: {os.path.relpath(WINRATES_CSV, ROOT)} ({len(filas)} filas)")
    state["winrates"] = {f"{f['champion']}|{f['role']}": float(f["win_pct"]) for f in filas}
    state["winrates_meta"] = {"bucket": filas[0]["bucket"], "updated_utc": filas[0]["updated_utc"],
                              "n_champs": len({f["champion"] for f in filas}), "n_filas": len(filas)}
    state["winrates_checked"] = datetime.datetime.now().isoformat(timespec="seconds")
    if fallos and not quiet:
        print("⚠️  win rates sin refrescar:", ", ".join(fallos))
    return len({f["champion"] for f in filas}), len(filas)


def main():
    quiet = "--quiet" in sys.argv
    solo_wr = "--winrates-only" in sys.argv
    argv = sys.argv[1:]
    roster_full = "--roster" in argv and argv.index("--roster") + 1 < len(argv) \
        and argv[argv.index("--roster") + 1] == "full"
    state = load_state()
    findings = []

    if not solo_wr:
        chequear_parches(state, findings)          # pasos 1-3
    n_ch, n_filas = actualizar_winrates(state, findings, quiet, roster_full)  # paso 4

    state["last_check"] = datetime.datetime.now().isoformat(timespec="seconds")
    json.dump(state, open(STATE, "w"), indent=1)

    if solo_wr:
        if findings:
            print("🔔 WIN RATES — MOVIMIENTOS ≥ umbral:")
            for f in findings: print("  -", f)
        if not n_filas:
            sys.exit(1)
        if not quiet:
            print(f"✅ Win rates al día: {n_ch} campeones · {n_filas} filas (champion_winrates.csv)")
        sys.exit(1 if findings else 0)

    if findings:
        print("🔔 CAMBIOS DETECTADOS:")
        for f in findings: print("  -", f)
        print("→ Ejecutar protocolo de actualización (FRAMEWORK §E) y regenerar BD/bundles.")
        sys.exit(1)
    if not quiet:
        print("✅ Sin cambios desde el último chequeo.", state["last_check"],
              f"· win rates: {n_ch} campeones refrescados")
    sys.exit(0)

if __name__ == "__main__":
    main()
