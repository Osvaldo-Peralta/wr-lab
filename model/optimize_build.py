# -*- coding: utf-8 -*-
"""
WR-LAB · optimize_build.py — optimizador exhaustivo de builds (v2: 4 motores)
=============================================================================
Busca la build ÓPTIMA de 6 slots (Ley 0) maximizando un objetivo ponderado
NORMALIZADO por escenario (cada escenario aporta en proporción, no en magnitud),
sujeto a presupuesto de oro y —en el motor de autos— a las Leyes 1 y 2 como podas.

MOTORES (adapters sobre los modelos del lab; el motor declara ítems, botas, escenarios y pesos):
    autos     dps_model.eval_build    → Jinx, Yunara, Sivir, Caitlyn… (crítico/on-hit del engine)
    onhit     analysis_batch2.kalista → Kalista (E Rend + Guinsoo doble on-hit)
    rotacion  analysis_batch2.diana   → Diana (y magos de rotación AP; keystone configurable)
    aliado    analysis_batch2.yuumi   → Yuumi/Karma (valor-aliado: escudo/cura/DPS-al-carry;
                                        slot de quest fijo + botas Crimson)

USO
    python3 model/optimize_build.py jinx                        # motor autos (default del campeón)
    python3 model/optimize_build.py jinx --crit-min 100 --pen-min 30 --validar
    python3 model/optimize_build.py kalista --validar           # ¿redescubre K2 BotRK?
    python3 model/optimize_build.py diana --keystone lt --validar
    python3 model/optimize_build.py yuumi --oro 13000 --validar
    python3 model/optimize_build.py jinx --motor autos --oro 15000 --top 5
    python3 model/optimize_build.py jinx --incluir "Gunmetal,C44,Runaan's,IE,LDR,Kraken,BT" --excluir ga

VALIDACIÓN CRUZADA (ROADMAP): con pesos default debe redescubrir la build C de Jinx
(pool del reporte), K2 de Kalista, D2-LT de Diana e Y1 de Yuumi — ver tests/test_optimize_build.py.

Búsqueda: DFS podado (oro; en autos también AS-cap y crit≤100 como podas estructurales,
y --crit-min/--pen-min como restricciones duras de hoja) + embudo re-puntuado con el
objetivo ponderado completo. Cero dependencias.
"""
import argparse, heapq, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "model"))
import dps_model as M
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import analysis_batch2 as B2

EPS_AS = 0.02          # tolerancia del tope de AS (Ley 2)

# ---------------------------------------------------------------- defensa y utilidad (v1.9)
# Fuentes: items_7.3.csv (valores oficiales) + comentarios del motor. Uptimes declarados:
# escudos condicionales (Lifeline/Ichorshield/Noxian) cuentan al 50-70 % (no están siempre).
ESCUDOS_FIS = {"bt": 255 * 0.5, "shieldbow": 425 * 0.5, "armored_adv": 75 * 0.7}
ESCUDOS_MAG = {"chainlaced": 75 * 0.7}      # Maw: valor recortado en la fuente → solo su MR cuenta
UTIL_FLAGS = {"ga": 300, "Zhonyas": 300, "scimitar": 150, "gale": 100,
              "immortal_treads": 100, "Redemption": 200, "Mikael": 200, "Locket": 150,
              "Shurelya": 100, "Zeke": 100}
BASE_DEF_FALLBACK = (650.0, 45.0, 35.0)     # hp/armor/mr nivel 1 (si no está en champion_base_stats.json)


def cargar_base_def(champ, nivel=15):
    """(hp, armor, mr) a nivel `nivel` desde data/estructurada/champion_base_stats.json.
    Formato fuente: '570 (104)' = base (crecimiento por nivel). Fallback genérico declarado."""
    import json, re as _re
    ruta = os.path.join(ROOT, "data", "estructurada", "champion_base_stats.json")
    try:
        with open(ruta, encoding="utf-8") as fh:
            db = json.load(fh)
        st = db[champ]["stats"]
        def num(clave):
            m = _re.match(r"([\d.]+)\s*\(([\d.]+)\)", st.get(clave, "").replace("\xa0", " "))
            if not m:
                return None
            return float(m.group(1)) + float(m.group(2)) * (nivel - 1)
        hp, ar, mr = num("heal"), num("armor"), num("magicresistance")   # 'heal' = Health (errata del scrape)
        if None in (hp, ar, mr):
            raise ValueError
        return hp, ar, mr
    except Exception:
        b = BASE_DEF_FALLBACK
        return (b[0] + 90 * (nivel - 1), b[1] + 3.5 * (nivel - 1), b[2] + 1.2 * (nivel - 1))


def ehp_y_util(keys_resueltas, base_def, heal_s):
    """EHP mixto (50 % físico / 50 % mágico, escudos condicionales ponderados) y utilidad
    (heal/s + banderas de activas). hechizo heurístico declarado: GA/Zhonyas 300, QSS 150…"""
    hp, armor, mr = base_def
    esc_f = esc_m = util = 0.0
    for k in keys_resueltas:
        it = M.ITEMS.get(k)
        if it is not None:
            hp += it.hp; armor += it.armor; mr += it.mr
        esc_f += ESCUDOS_FIS.get(k, 0.0)
        esc_m += ESCUDOS_MAG.get(k, 0.0)
        util += UTIL_FLAGS.get(k, 0.0)
    ehp = 0.5 * ((hp + esc_f) * (1 + armor / 100.0) + (hp + esc_m) * (1 + mr / 100.0))
    # heal/s se pondera ×0.25 para que no aplaste a las activas (heurístico declarado v1.9)
    return ehp, util + 0.25 * heal_s

# ---------------------------------------------------------------- motores
ESC_AUTOS = {
    "1v1":      (dict(),                                     "dps1"),
    "3v3":      (dict(targets=3),                            "dpsN"),
    "vs120":    (dict(armor=120),                            "dps1"),
    "vsTanque": (dict(armor=220, tank=True, enemy_hp=4500),  "dps1"),
}
PESOS_AUTOS = {"1v1": 0.30, "3v3": 0.30, "vs120": 0.20, "vsTanque": 0.20}

ESC_ONHIT = {
    "1v1":      (dict(), "single"),
    "3v3":      (dict(targets=3), "multi"),
    "vsTanque": (dict(armor=220, mr=150, ehp=4500), "single"),
}
PESOS_ONHIT = {"1v1": 0.35, "3v3": 0.45, "vsTanque": 0.20}

ESC_ROT = {
    "dps10s":  (dict(), "dps"),
    "burst":   (dict(), "burst"),
    "vs180mr": (dict(mr=180), "dps"),
}
PESOS_ROT = {"dps10s": 0.50, "burst": 0.30, "vs180mr": 0.20}

ESC_ALIADO = {
    "e_shield": (dict(), "e_shield"),
    "r_heal":   (dict(), "r_heal"),
    "adc_dps":  (dict(), "adc_dps_add"),
}
PESOS_ALIADO = {"e_shield": 0.35, "r_heal": 0.30, "adc_dps": 0.35}

# IE fuera del pool on-hit: batch2.kalista() NO modela críticos (la E Rend no critica y los
# autos critables no están en la fórmula) → IE aparecería como "AD barato" y su 25 % de crit
# valdría 0 en el score. En la realidad ese crit SÍ vale: excluirlo es la postura conservadora.
_K_NO_BOOT = [k for k in B2.K_ITEMS if k not in ("Gunmetal", "IE")]
_D_NO_BOOT = [k for k in B2.D_ITEMS if k not in ("Spellslinger", "Crimson")]
_Y_NO_BOOT = [k for k in B2.Y_ITEMS if k not in ("Crimson", "Scythe", "ionian")]

ENGINES = {
    "autos": dict(
        items=[k for k in M.ITEMS if k not in M.BOOTS_ALL and k != "boots_speed"],
        boots=list(M.BOOT_UPGRADES.keys()), fixed=[], n_elegir=5, oro_default=18000,
        escenarios=ESC_AUTOS, pesos=PESOS_AUTOS, podas_autos=True,
        eval_fn=lambda champ, combo, kw, opts: M.eval_build(M.CHAMPS[champ], combo, validate=False, **kw),
        base_fn=lambda champ, combo, opts: M.eval_build(M.CHAMPS[champ], combo, validate=False),
        gold_fn=lambda k: M.ITEMS[k].gold,
        requiere_spec=True,
    ),
    "onhit": dict(
        items=_K_NO_BOOT, boots=["Gunmetal"], fixed=[], n_elegir=5, oro_default=18000,
        escenarios=ESC_ONHIT, pesos=PESOS_ONHIT, podas_autos=False,
        eval_fn=lambda champ, combo, kw, opts: B2.kalista(combo, **kw),
        base_fn=lambda champ, combo, opts: B2.kalista(combo),
        gold_fn=lambda k: B2.K_ITEMS[k]["g"],
        requiere_spec=False,
    ),
    "rotacion": dict(
        items=_D_NO_BOOT, boots=["Spellslinger", "Crimson"], fixed=[], n_elegir=5, oro_default=18500,
        escenarios=ESC_ROT, pesos=PESOS_ROT, podas_autos=False,
        eval_fn=lambda champ, combo, kw, opts: B2.diana(combo, keystone=opts.get("keystone", "lt"), **kw),
        base_fn=lambda champ, combo, opts: B2.diana(combo, keystone=opts.get("keystone", "lt")),
        gold_fn=lambda k: B2.D_ITEMS[k]["g"],
        requiere_spec=False,
    ),
    "aliado": dict(
        items=_Y_NO_BOOT, boots=["Crimson"], fixed=["Scythe"], n_elegir=4, oro_default=13000,
        escenarios=ESC_ALIADO, pesos=PESOS_ALIADO, podas_autos=False,
        eval_fn=lambda champ, combo, kw, opts: B2.yuumi(combo, **kw),
        base_fn=lambda champ, combo, opts: B2.yuumi(combo),
        gold_fn=lambda k: B2.Y_ITEMS[k]["g"],
        requiere_spec=False,
    ),
}

MOTOR_POR_CAMPEON = {"kalista": "onhit", "diana": "rotacion", "yuumi": "aliado", "karma": "aliado"}

# Campeones cuyo arquetipo NO es representable por ningún motor del lab: optimizarlos
# con el motor de autos produce BASURA (bug reportado 29-sep: chogath "como ADC").
SIN_MOTOR = {
    "chogath":     "tanque AP (Feast) — el motor de autos no tiene sentido; ver metodologia/ESCALADO_DE_TAMANIO.md y el modelo de rotación (pendiente en batch2)",
    "mordekaiser": "juggernaut AP — requiere modelo de rotación + R (pendiente en batch2)",
    "heimerdinger": "mago de zona (torretas) — requiere modelo de DPS de torretas (pendiente)",
    "seraphine":   "enchanter-mage — modelo de valor-aliado/rotación (pendiente)",
    "malphite":    "tanque de escalado de armadura — ver ESCALADO_DE_TAMANIO.md",
}
# Campeones donde el motor elegido es una APROXIMACIÓN (aviso, no bloqueo)
MOTOR_AVISOS = {
    "yunara":   "motor autos NO modela su spread de Q ni la interacción de R con crítico — resultados aproximados",
    "shyvana":  "motor autos NO modela su Q doble golpe ni la forma dragón — resultados aproximados",
    "volibear": "motor autos NO modela su W ejecutor ni stacks de AS; ad_growth sin verificar (FUENTES.md) — resultados aproximados",
}


def motor_para(champ, override=None, quiet=False):
    if override:
        if champ in SIN_MOTOR and not quiet:
            print(f"⚠️ MOTOR FORZADO para {champ}: {SIN_MOTOR[champ]}.\n"
                  f"   Los resultados NO son válidos para publicar — solo exploración bajo tu responsabilidad.")
        return override
    if champ in SIN_MOTOR:
        sys.exit(f"❌ '{champ}' no tiene motor de optimización: {SIN_MOTOR[champ]}.\n"
                 f"   (Puedes forzar uno con --motor, bajo tu responsabilidad; o analizarlo a mano "
                 f"con el bundle completo en un chat externo.)")
    if champ in MOTOR_AVISOS and not quiet:
        print(f"⚠️ {champ}: {MOTOR_AVISOS[champ]}")
    return MOTOR_POR_CAMPEON.get(champ, "autos")


# ---------------------------------------------------------------- búsqueda
PRESETS = {"balanceado": (0.15, 0.15), "ofensivo": (0.0, 0.0), "defensivo": (0.30, 0.15)}


def optimizar(champ, motor=None, oro=None, top=10, pesos=None, excluir=(), incluir=None,
              solo_botas=None, embudo=400, nivel=15, verbose=True, crit_min=0, pen_min=0,
              keystone="lt", defensa=0.0, utilidad=0.0, preset=None):
    champ = champ.lower()
    motor = motor_para(champ, motor, quiet=not verbose)
    eng = ENGINES[motor]
    if preset:
        defensa, utilidad = PRESETS[preset]
    if motor == "aliado" and (defensa or utilidad):
        print("[aviso] motor aliado: la defensa propia no aplica (Yuumi attachada es intargeteable) "
              "— pesos de defensa/utilidad ignorados")
        defensa = utilidad = 0.0
    if eng["requiere_spec"] and champ not in M.CHAMPS:
        sys.exit(f"'{champ}' no tiene ChampSpec en dps_model.CHAMPS (motor autos). "
                 f"Especs: {sorted(M.CHAMPS)}")
    opts = {"keystone": keystone}
    oro = oro or eng["oro_default"]
    pesos = pesos or dict(eng["pesos"])
    escenarios = eng["escenarios"]
    falta = set(pesos) - set(escenarios)
    if falta:
        sys.exit(f"escenarios desconocidos para motor {motor}: {falta} (válidos: {list(escenarios)})")

    def resolver(x):
        """alias/nombre visible → clave del pool del motor."""
        x = x.strip()
        if eng is ENGINES["autos"]:
            try:
                return M.resolve(x).key
            except KeyError:
                return x.lower()
        for k in eng["items"] + eng["boots"] + eng["fixed"]:
            if k.lower() == x.lower():
                return k
        try:                                  # nombres visibles del vault ("Runaan's Hurricane")
            import update_reports as U
            for k in eng["items"] + eng["boots"] + eng["fixed"]:
                if U.resolver_clave(x, motor) == k:
                    return k
        except Exception:
            pass
        return x.lower()

    ex_keys = {resolver(x) for x in excluir if x}
    pool = [k for k in eng["items"] if k not in ex_keys]
    if incluir:
        inc = {resolver(x) for x in incluir if x.strip()}
        pool = [k for k in pool if k in inc]
    botas = list(eng["boots"])
    if solo_botas:
        wanted = {x.strip().lower() for x in solo_botas.split(",")}
        botas = [b for b in botas if b.lower() in wanted]
    if not botas:
        sys.exit("sin botas candidatas")
    fixed = list(eng["fixed"])
    n_elegir = eng["n_elegir"]

    gold = eng["gold_fn"]
    esc1 = max(pesos, key=pesos.get)
    kw1, met1 = escenarios[esc1]

    # podas estructurales del motor de autos (Ley 1/2 como cotas monótonas)
    if eng["podas_autos"]:
        spec = M.CHAMPS[champ]
        lt_as = (M.LT_RANGED_STACK if spec.ranged else M.LT_MELEE_STACK) * 6
        const_raw = spec.base_as + spec.as_ratio * (
            spec.base_bonus_as + M.lvl_as_bonus(spec, nivel) + lt_as + M.ALACRITY_FULL + spec.self_as_buff)
        as_por_item = {k: M.ITEMS[k].a_s / 100.0 for k in pool}
        crit_item = {k: M.ITEMS[k].crit for k in pool}
    oro_item = {k: gold(k) for k in pool}
    oro_min = min(oro_item.values()) if oro_item else 0
    orden = sorted(pool, key=lambda k: oro_item[k])
    idx = {k: i for i, k in enumerate(orden)}

    t0 = time.time()
    hojas = 0
    heap = []                                   # min-heap (score1, -oro, combo)
    eval_fn = eng["eval_fn"]

    def dfs(start, elegidos, g):
        nonlocal hojas
        faltan = n_elegir - len(elegidos)
        if g + faltan * oro_min > oro - oro_fijo:
            return
        if eng["podas_autos"]:
            if sum(crit_item[k] for k in elegidos) > 100:
                return
            ai = sum(as_por_item[k] for k in elegidos)
            if const_raw + spec.as_ratio * ai > M.AS_CAP + EPS_AS:
                return
        if faltan == 0:
            combo = ctx_botas + fixed + elegidos
            base = eng["base_fn"](champ, combo, opts)
            if eng["podas_autos"]:
                if base["crit"] < crit_min or base["pen"] < pen_min:
                    return
            hojas += 1
            r = eval_fn(champ, combo, kw1, opts) if kw1 else base
            s = r[met1]
            if len(heap) < embudo:
                heapq.heappush(heap, (s, -g, combo))
            elif s > heap[0][0]:
                heapq.heapreplace(heap, (s, -g, combo))
            return
        for k in orden[start:]:
            dfs(idx[k] + 1, elegidos + [k], g + oro_item[k])

    oro_fijo = sum(gold(k) for k in fixed)
    candidatos = []
    for b in botas:
        ctx_botas = [b]
        oro_save, oro = oro, oro - gold(b)
        dfs(0, [], 0)
        oro = oro_save
        candidatos.extend(heap)
        heap = []

    # pasada 2: objetivo ponderado NORMALIZADO por escenario (+ defensa/utilidad opcionales)
    base_def = cargar_base_def(champ, nivel) if (defensa or utilidad) else None
    brutos = []
    for s1, neg_g, combo in candidatos:
        det = {e: eval_fn(champ, combo, kw, opts)[m] for e, (kw, m) in escenarios.items()}
        base = eng["base_fn"](champ, combo, opts)
        ehp = util = 0.0
        if base_def is not None:
            keys = [M.resolve(c).key for c in combo] if eng is ENGINES["autos"] else list(combo)
            heal_s = base.get("heal", 0.0) if isinstance(base, dict) else 0.0
            ehp, util = ehp_y_util(keys, base_def, heal_s)
        brutos.append((combo, det, base, ehp, util))
    max_e = {e: max((d[e] for _, d, _, _, _ in brutos), default=1.0) or 1.0 for e in escenarios}
    max_ehp = max((x[3] for x in brutos), default=1.0) or 1.0
    max_util = max((x[4] for x in brutos), default=1.0) or 1.0
    finales = []
    for combo, det, base, ehp, util in brutos:
        off = sum(pesos.get(e, 0.0) * (det[e] / max_e[e]) for e in escenarios)
        score = (1 - defensa - utilidad) * off + defensa * (ehp / max_ehp) + utilidad * (util / max_util)
        finales.append((score, combo, det, base, ehp, util))
    finales.sort(key=lambda x: (-x[0], sum(gold(k) for k in x[1])))
    if verbose:
        print(f"[{champ}·{motor}] hojas legales: {hojas:,} · embudo: {len(candidatos)} · "
              f"{time.time()-t0:.1f}s · ≤{oro:,} g · nivel {nivel}")
    return finales[:top], hojas


def imprimir(finales, champ, motor, pesos, oro, con_def=False):
    eng = ENGINES[motor]
    gold = eng["gold_fn"]
    w = " · ".join(f"{e}:{p:g}" for e, p in sorted(pesos.items(), key=lambda x: -x[1]))
    print(f"\n=== TOP builds · {champ} ({motor}) · objetivo [{w}] · ≤{oro:,} g ===")
    cols = list(eng["escenarios"])
    print(f"{'#':>2} {'EFIC':>6} {'ORO':>6} " + " ".join(f"{c:>8}" for c in cols) + "  BUILD")
    tot_w = sum(pesos.values()) or 1.0
    if con_def:
        print(f"(columnas EHP/UTIL activas — pesos defensa/utilidad incluidos en EFIC)")
    for i, fila in enumerate(finales, 1):
        score, combo, det, base = fila[0], fila[1], fila[2], fila[3]
        ehp, util = (fila[4], fila[5]) if con_def else (0, 0)
        og = sum(gold(k) for k in combo)
        extra = f" {ehp/1000:>6.1f}k {util:>6.0f}" if con_def else ""
        print(f"{i:>2} {score/tot_w*100:>5.1f}% {og:>6} "
              + " ".join(f"{det[c]:>8.0f}" for c in cols)
              + extra + f"  {'+'.join(combo)}")


def validar(finales, champ, motor):
    """Compara el top-1 contra las builds publicadas del registro (mismo campeón)."""
    eng = ENGINES[motor]
    reg_path = os.path.join(ROOT, "data", "estructurada", "reportes_registry.json")
    if not os.path.exists(reg_path):
        print("⚠️ sin reportes_registry.json — corre update_reports.py baseline")
        return None
    import json
    with open(reg_path, encoding="utf-8") as fh:
        reg = json.load(fh)
    keys_pool = set(eng["items"]) | set(eng["boots"]) | set(eng["fixed"])

    def norm_keys(bk):
        out = []
        for k in bk:
            if k in keys_pool:
                out.append(k)
            elif eng is ENGINES["autos"]:
                try:
                    out.append(M.resolve(k).key)
                except KeyError:
                    out.append(k)
            else:
                hit = next((p for p in keys_pool if p.lower() == k.lower()), None)
                out.append(hit or k)
        return out

    pubs = []
    for f, e in reg["reportes"].items():
        if e["champion"] != champ or not e.get("build_keys"):
            continue
        bk = norm_keys(e["build_keys"])
        if all(k in keys_pool for k in bk):
            pubs.append((f, bk))
    if not pubs:
        print(f"⚠️ el registro no tiene build publicada compatible con el motor '{motor}' para {champ}")
        return None
    top1 = finales[0][1]
    ok_global = False
    for f, bk in pubs:
        mismo = sorted(bk) == sorted(top1)
        rank = next((i for i, f in enumerate(finales, 1) if sorted(f[1]) == sorted(bk)), None)
        ok_global |= mismo
        print(f"{'✅ REDISCUBIERTA' if mismo else '≠ DIVERGE'} · {f}: "
              f"top-1 {'==' if mismo else '≠'} publicada"
              + ("" if mismo else f" (publicada rankea #{rank} del top-{len(finales)} mostrado)"
                 if rank else " (publicada fuera del top mostrado — corre con --top mayor)")
              + f" · publicada: {'+'.join(bk)}")
    return ok_global


def parse_pesos(s):
    return {par.split(":")[0].strip(): float(par.split(":")[1]) for par in s.split(",")}


def main():
    ap = argparse.ArgumentParser(description="WR-LAB · optimizador exhaustivo de builds (4 motores)")
    ap.add_argument("champion")
    ap.add_argument("--motor", default=None, choices=list(ENGINES),
                    help="default: por campeón (kalista→onhit, diana→rotacion, yuumi/karma→aliado, resto→autos)")
    ap.add_argument("--oro", type=int, default=None, help="presupuesto (default por motor)")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--nivel", type=int, default=15)
    ap.add_argument("--pesos", default=None, help="p.ej. 1v1:0.5,3v3:0.5")
    ap.add_argument("--excluir", default="")
    ap.add_argument("--incluir", default=None)
    ap.add_argument("--botas", default=None)
    ap.add_argument("--keystone", default="lt", help="motor rotacion: lt|empower|conq")
    ap.add_argument("--embudo", type=int, default=400)
    ap.add_argument("--crit-min", type=float, default=0, help="Ley 1 dura (motor autos)")
    ap.add_argument("--pen-min", type=float, default=0, help="Ley 3 dura (motor autos)")
    ap.add_argument("--validar", action="store_true")
    ap.add_argument("--defensa", type=float, default=0.0, help="peso de EHP en el score (0-0.5)")
    ap.add_argument("--utilidad", type=float, default=0.0, help="peso de heal/activas en el score (0-0.5)")
    ap.add_argument("--preset", default=None, choices=list(PRESETS),
                    help="balanceado=70/15/15 ofensivo/defensivo (ver PRESETS)")
    args = ap.parse_args()

    ck = args.champion.lower()
    motor = motor_para(ck, args.motor)
    eng = ENGINES[motor]
    pesos = parse_pesos(args.pesos) if args.pesos else dict(eng["pesos"])
    oro = args.oro or eng["oro_default"]
    finales, hojas = optimizar(ck, motor=motor, oro=oro, top=args.top, pesos=pesos,
                               excluir=tuple(x for x in args.excluir.split(",") if x),
                               incluir=args.incluir.split(",") if args.incluir else None,
                               solo_botas=args.botas, embudo=args.embudo, nivel=args.nivel,
                               crit_min=args.crit_min, pen_min=args.pen_min,
                               keystone=args.keystone, defensa=args.defensa,
                               utilidad=args.utilidad, preset=args.preset)
    imprimir(finales, ck, motor, pesos, oro,
             con_def=bool(args.preset in ("balanceado", "defensivo") or args.defensa or args.utilidad))
    if args.validar:
        print()
        ok = validar(finales, ck, motor)
        if ok is False:
            sys.exit(2)


if __name__ == "__main__":
    main()
