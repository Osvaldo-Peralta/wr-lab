# -*- coding: utf-8 -*-
"""
WR-LAB · check_patch.py — vigilante de parches.
Detecta: (1) cambios en la página oficial 7.3, (2) publicación de páginas 7.3a/7.3b/7.4,
(3) nuevas entradas de change-history en wr-meta para campeones centinela.
Estado persistente en data/raw/.watch_state.json. Exit 1 si hay cambios (útil para CI/cron).

Uso:  python3 model/check_patch.py [--quiet]
"""
import hashlib, json, os, re, sys, datetime, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "data", "raw", ".watch_state.json")
OFFICIAL = "https://wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-{slug}/"
CANDIDATES = ["7-3a", "7-3-a", "7-3b", "7-4", "7-3b-hotfix"]
WRMETA_SENTINELS = {"jinx": "39-jinx", "caitlyn": None, "hwei": None, "yuumi": "321-yuumi",
                    "kalista": "349-kalista", "malphite": "47-malphite"}
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/126.0"}

def get(url, t=25):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=t) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return f"ERR:{type(e).__name__}", b""

def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE))
    return {"official_73_md5": None, "new_pages": [], "changelog_dates": {}, "last_check": None}

def main():
    quiet = "--quiet" in sys.argv
    state = load_state()
    findings = []

    # 1) ¿la página oficial 7.3 cambió?
    st, body = get(OFFICIAL.format(slug="7-3"))
    if st == 200:
        md5 = hashlib.md5(body).hexdigest()
        if state["official_73_md5"] and md5 != state["official_73_md5"]:
            findings.append(f"Página oficial 7.3 MODIFICADA (md5 {state['official_73_md5'][:8]} → {md5[:8]})")
        state["official_73_md5"] = md5

    # 2) ¿se publicó alguna página nueva de parche?
    for slug in CANDIDATES:
        st2, _ = get(OFFICIAL.format(slug=slug), t=15)
        if st2 == 200 and slug not in state["new_pages"]:
            state["new_pages"].append(slug)
            findings.append(f"NUEVA página oficial de notas: {slug} → descargar y correr protocolo FRAMEWORK §E")

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

    state["last_check"] = datetime.datetime.now().isoformat(timespec="seconds")
    json.dump(state, open(STATE, "w"), indent=1)

    if findings:
        print("🔔 CAMBIOS DETECTADOS:")
        for f in findings: print("  -", f)
        print("→ Ejecutar protocolo de actualización (FRAMEWORK §E) y regenerar BD/bundles.")
        sys.exit(1)
    if not quiet:
        print("✅ Sin cambios desde el último chequeo.", state["last_check"])
    sys.exit(0)

if __name__ == "__main__":
    main()
