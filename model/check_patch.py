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

Uso:  python3 model/check_patch.py [--quiet] [--winrates-only]
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
WRMETA_IDS = {"jinx": "39", "yuumi": "321", "yunara": "545", "mordekaiser": "365",
              "kalista": "349", "diana": "216", "karma": "323", "heimerdinger": "346",
              "volibear": "411", "seraphine": "34", "shyvana": "23", "chogath": "339",
              "malphite": "47", "caitlyn": "317", "sivir": "394", "norra": "552",
              "rammus": "242",
              # v1.15: nuevos campeones (IDs vía sitemap.xml, confirmados con fetch 04/10)
              "orianna": "33", "ahri": "1", "nocturne": "382", "syndra": "398"}

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


def actualizar_winrates(state, findings, quiet=False):
    """Paso 4 del vigía. Devuelve (n_champs_ok, n_filas). Falla suave: si wr-meta no
    responde, conserva los valores previos y NO rompe los pasos 1-3."""
    ids = dict(WRMETA_IDS)
    ids.update(state.get("wrmeta_ids", {}))
    roster = roster_winrates()
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
    # drift contra el estado previo (antes de sobrescribirlo)
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
    state = load_state()
    findings = []

    if not solo_wr:
        chequear_parches(state, findings)          # pasos 1-3
    n_ch, n_filas = actualizar_winrates(state, findings, quiet)   # paso 4 (mismo proceso)

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
