# -*- coding: utf-8 -*-
"""
WR-LAB · optimize_runes.py — buscador de runas (ROADMAP módulo 3)
=================================================================
Puntúa combinaciones KEYSTONE × SECUNDARIA sobre una build dada, con el mismo
esquema del optimizador de builds: escenario por escenario, puntuación ponderada
NORMALIZADA y valor marginal contra el baseline del lab (Lethal Tempo + Alacrity).

Motores soportados (v1):
    autos      (dps_model.eval_build)     → Jinx, Yunara, Sivir, Caitlyn…
    rotacion   (analysis_batch2.diana)    → Diana y magos de rotación (keystones empower/lt/conq)
    onhit/aliado: PENDIENTES (los modelos batch no parametrizan suficientes runas — ver ROADMAP)

FUENTE DE VALORES: data/estructurada/runas_7.3.md (scrape de wr-meta; las notas oficiales
7.3 mandan para Lethal Tempo, ya dentro del motor). SUPUESTOS DECLARADOS (auditables):
    · Conqueror: 5 AD × 6 stacks = 30 AD con uptime 85 % en pelea sostenida (→ 25.5 efectivo)
      + 5 % omnivamp ranged a stacks llenos (va a la columna de sustain, no al DPS).
    · First Strike: +7 % verdadero 3 s cada 25 s → +0.84 % efectivo sostenido (+oro no modelado).
    · Electrocute: 210 (nivel 15) + 10 % AD por proc; **CD 25 s ASUMIDO** (la fuente está cortada
      en "Cooldown:") → verificar en juego antes de publicar conclusiones finas.
    · Coup de Grace: +8 % sobre el 25 % del tiempo de pelea con el objetivo <40 % HP → +2 %.
    · Cut Down: +6.57 % vs >60 % HP → completo en vsTanque, mitad en el resto.
    · Last Stand: 5-11 % bajo 60 % HP → promedio 5 % × ventana 50 % → +2.5 %.
    · Triumph / Legend: Bloodline: sustain/utilidad (columna propia, NO puntúan DPS).
    · Brutal / Sudden Impact / Battle Zeal / Gathering Storm: EXCLUIDOS del modelo v1
      (fuente rasgada sin números fiables / requieren flags por campeón / amplifican
      habilidades fuera del modelo de autos). Motivo registrado en EXCLUIDAS.

USO
    python3 model/optimize_runes.py jinx                       # build publicada del registro
    python3 model/optimize_runes.py jinx --build "Gunmetal,C44,Runaan's,IE,LDR,Kraken"
    python3 model/optimize_runes.py diana --build "Spellslinger,DuskDawn,Nashor,Rabadon,Zhonyas,Cryptbloom"
    python3 model/optimize_runes.py jinx --top 8

VALIDACIÓN: para Jinx debe ganar Lethal Tempo + Legend: Alacrity (conclusión del reporte);
para Diana (rotación), keystone LT (reporte: +30 % DPS sostenido vs Empowerment).
"""
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "model"))
import dps_model as M
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import analysis_batch2 as B2
from optimize_build import ENGINES, PESOS_AUTOS, motor_para   # reutiliza motores/normalización

# ---------------------------------------------------------------- catálogo de runas (autos)
KEYSTONES_AUTOS = {
    "Lethal Tempo": dict(lt=True,
        notas="6.4 %/stack ranged + bala 6-24 · valores oficiales 7.3 YA en el motor"),
    "Conqueror": dict(ad_extra=25.5, omnivamp=0.05,
        notas="30 AD a 6 stacks × uptime 85 % = 25.5 · +5 % omnivamp (sustain)"),
    "First Strike": dict(true_amp=0.0084,
        notas="+7 % verdadero 3 s / CD 25 s = +0.84 % sostenido · +oro no modelado"),
    "Electrocute": dict(burst_ad_ratio=0.10, burst_flat=210, burst_cd=25,
        notas="210 + 10 % AD por proc · CD 25 s ASUMIDO (fuente cortada)"),
}
SECONDARIES_AUTOS = {
    "Legend: Alacrity": dict(alacrity=0.21, notas="+21 % AS (3+18 a full stacks) — motor oficial"),
    "Legend: Bloodline": dict(omnivamp=0.08, notas="+8 % omnivamp — sustain, no DPS"),
    "Coup de Grace": dict(cond_amp=0.08, ventana=0.25, notas="+8 % vs <40 % HP × ventana 25 %"),
    "Cut Down": dict(tank_amp=0.0657, otros_amp=0.0329, notas="+6.57 % vs >60 % HP (mitad fuera de vsTanque)"),
    "Last Stand": dict(cond_amp=0.05, ventana=0.50, notas="5-11 % bajo 60 % HP → 5 % × 50 %"),
    "Triumph": dict(utility=True, notas="10 % vida perdida por takedown + 35 MS — utilidad pura"),
}
EXCLUIDAS = {
    "Brutal": "fuente rasgada sin números fiables (verificar en juego)",
    "Sudden Impact": "requiere flag de dash por campeón (no está en ChampSpec)",
    "Battle Zeal": "amplifica habilidades — fuera del modelo de autos",
    "Legend: Haste": "AH de habilidades — solo aplica al motor rotación",
    "Grasp of the Undying": "sustain de melee — fuera del arquetipo autos ranged",
    "Summon Aery / Arcane Comet / Phase Rush / Ice Overlord": "keystones de mago/utilidad — fuera de autos",
}

ESC_AUTOS = ENGINES["autos"]["escenarios"]

# ---------------------------------------------------------------- catálogo (rotación)
KEYSTONES_ROT = {
    "Lethal Tempo": dict(ks="lt", notas="motor batch2: bala adaptativa + AS 38.4 %"),
    "Empowerment": dict(ks="empower", notas="motor batch2: proc 165 + amp 8 %, ICD 4 s"),
    "Conqueror": dict(ks="conq", notas="motor batch2: ~30 adaptivo uptime 60 % + omnivamp"),
}
SECONDARIES_ROT = {
    "Legend: Haste": dict(pen_note="Legend: Haste", notas="+15 AH (tope) — entra en diana()"),
    "— (sin secundaria modelada)": dict(pen_note=None, notas="baseline"),
}


def build_desde_registro(champ):
    reg_path = os.path.join(ROOT, "data", "estructurada", "reportes_registry.json")
    if not os.path.exists(reg_path):
        return None
    with open(reg_path, encoding="utf-8") as fh:
        reg = json.load(fh)
    for f, e in sorted(reg["reportes"].items()):
        if e["champion"] == champ and e.get("build_keys"):
            return e["build_keys"], f
    return None


def eval_par_autos(spec, build, ks, sec, esc_kw, met, nivel=15):
    """Valor del par (keystone, secundaria) para la métrica del escenario + sustain."""
    k, s = KEYSTONES_AUTOS[ks], SECONDARIES_AUTOS[sec]
    r = M.eval_build(spec, build, level=nivel, validate=False,
                     lt=k.get("lt", False), alacrity=s.get("alacrity", 0.0),
                     ad_extra=k.get("ad_extra", 0.0), **esc_kw)
    dps = r[met]
    armor = esc_kw.get("armor", 0.0)
    if k.get("true_amp"):                                   # First Strike: verdadero post-mitigación
        dps *= (1 + k["true_amp"])
    if k.get("burst_flat"):                                 # Electrocute: burst single-target mitigado / CD
        mit = 100 / (100 + armor * (1 - r["pen"] / 100)) if armor > 0 else 1.0
        dps += (k["burst_flat"] + k["burst_ad_ratio"] * r["AD"]) * mit / k["burst_cd"]
    if s.get("cond_amp"):                                   # CdG / Last Stand: ventana declarada
        dps *= (1 + s["cond_amp"] * s["ventana"])
    if s.get("tank_amp"):                                   # Cut Down
        dps *= (1 + (s["tank_amp"] if esc_kw.get("tank") else s["otros_amp"]))
    sustain = r["heal"] + r["dps1"] * (k.get("omnivamp", 0) + s.get("omnivamp", 0))
    return dps, sustain


def buscar_autos(champ, build, top=10, nivel=15, pesos=None):
    spec = M.CHAMPS[champ]
    pesos = pesos or dict(PESOS_AUTOS)
    grid = []
    for ks in KEYSTONES_AUTOS:
        for sec in SECONDARIES_AUTOS:
            det, sustains = {}, []
            for e, (kw, met) in ESC_AUTOS.items():
                d, sus = eval_par_autos(spec, build, ks, sec, kw, met, nivel)
                det[e] = d
                sustains.append(sus)
            grid.append({"ks": ks, "sec": sec, "det": det, "sustain": max(sustains)})
    max_e = {e: max(g["det"][e] for g in grid) or 1.0 for e in ESC_AUTOS}
    for g in grid:
        g["score"] = sum(pesos.get(e, 0) * (g["det"][e] / max_e[e]) for e in ESC_AUTOS)
    base = next(g for g in grid if g["ks"] == "Lethal Tempo" and g["sec"] == "Legend: Alacrity")
    for g in grid:
        g["marginal"] = (g["score"] / base["score"] - 1) * 100 if base["score"] else 0.0
    grid.sort(key=lambda g: (-g["score"], g["ks"]))
    return grid[:top], base


def buscar_rotacion(champ, build, top=10, keystone_build_kw=None):
    grid = []
    for ks_name, ks in KEYSTONES_ROT.items():
        for sec_name, sec in SECONDARIES_ROT.items():
            kw = {"keystone": ks["ks"]}
            if sec.get("pen_note"):
                kw["pen_note"] = sec["pen_note"]
            r = B2.diana(build, **kw)
            rt = B2.diana(build, mr=180, **kw)
            grid.append({"ks": ks_name, "sec": sec_name,
                         "det": {"dps10s": r["dps"], "burst": r["burst"], "vs180mr": rt["dps"]},
                         "sustain": 0.0})
    from optimize_build import PESOS_ROT
    max_e = {e: max(g["det"][e] for g in grid) or 1.0 for e in ("dps10s", "burst", "vs180mr")}
    for g in grid:
        g["score"] = sum(PESOS_ROT[e] * (g["det"][e] / max_e[e]) for e in max_e)
    base = next(g for g in grid if g["ks"] == "Lethal Tempo" and "sin secundaria" in g["sec"])
    for g in grid:
        g["marginal"] = (g["score"] / base["score"] - 1) * 100 if base["score"] else 0.0
    grid.sort(key=lambda g: -g["score"])
    return grid[:top], base


def main():
    ap = argparse.ArgumentParser(description="WR-LAB · buscador de runas (keystone × secundaria)")
    ap.add_argument("champion")
    ap.add_argument("--build", default=None, help="ítems coma-separados (default: publicada en el registro)")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--nivel", type=int, default=15)
    args = ap.parse_args()
    champ = args.champion.lower()
    motor = motor_para(champ)
    if motor not in ("autos", "rotacion"):
        sys.exit(f"motor '{motor}' aún sin soporte de runas (v1: autos y rotacion). Ver ROADMAP.")

    if args.build:
        build = [x.strip() for x in args.build.split(",")]
        origen = "CLI"
    else:
        reg = build_desde_registro(champ)
        if not reg:
            sys.exit("sin build publicada en el registro — pasa --build explícita")
        build, origen = reg
    if motor == "autos":
        build = [M.ALIAS.get(b, b) if b in M.ALIAS else b for b in build]
        M.validate_slots(build)
        grid, base = buscar_autos(champ, build, args.top, args.nivel)
        cols = list(ESC_AUTOS)
    else:
        grid, base = buscar_rotacion(champ, build, args.top)
        cols = ["dps10s", "burst", "vs180mr"]

    base_lbl = "vs baseline" if motor == "rotacion" else "vs LT+Alac"
    print(f"=== RUNAS · {champ} ({motor}) · build: {'+'.join(build)}  [{origen}] ===")
    print(f"{'#':>2} {'SCORE':>6} {base_lbl:>10} {'sustain':>8} " +
          " ".join(f"{c:>8}" for c in cols) + "  KEYSTONE × SECUNDARIA")
    for i, g in enumerate(grid, 1):
        print(f"{i:>2} {g['score']*100:>5.1f}% {g['marginal']:>+9.1f}% {g['sustain']:>8.0f} " +
              " ".join(f"{g['det'][c]:>8.0f}" for c in cols) +
              f"  {g['ks']} × {g['sec']}")
    lbl = ("Lethal Tempo × — (sin secundaria modelada)" if motor == "rotacion"
           else "Lethal Tempo × Legend: Alacrity")
    print(f"\nBaseline del lab: {lbl} = 0.0 % (columna '{base_lbl}' = valor marginal).")
    print("Supuestos declarados en el docstring del módulo; runas excluidas:")
    for r, mot in EXCLUIDAS.items():
        print(f"  · {r}: {mot}")


if __name__ == "__main__":
    main()
