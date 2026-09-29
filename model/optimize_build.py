# -*- coding: utf-8 -*-
"""
WR-LAB · optimize_build.py — optimizador exhaustivo de builds (ROADMAP módulo 2)
================================================================================
Busca la build ÓPTIMA de 6 slots (Ley 0: 1 botas T3 + 5 ítems) para cualquier
ChampSpec del arquetipo de autos (dps_model), maximizando un objetivo ponderado
de escenarios, sujeto a:
    · presupuesto de oro            (--oro, default 18 000)
    · Ley 1: crítico total ≤ 100 %  (poda estructural)
    · Ley 2: AS cruda ≤ tope 3.0+ε  (poda estructural; pasivas tipo Get Excited quedan fuera)
    · Ley 0: 1 botas + 5 ítems      (estructural: la botas se eligen en el lazo externo)

Motor = dps_model.eval_build (fuente de verdad). Búsqueda en dos pasadas:
    1) DFS podado sobre el pool (oro/AS/crit monótonos) puntuado con el escenario
       de mayor peso → se conservan los mejores --embudo (default 400).
    2) Re-puntuación EXACTA del embudo con el objetivo ponderado completo.

USO
    python3 model/optimize_build.py jinx                     # top 10 por defecto
    python3 model/optimize_build.py jinx --oro 15000 --top 5 # presupuesto early/mid
    python3 model/optimize_build.py jinx --validar           # ¿redescubre la build publicada?
    python3 model/optimize_build.py yunara --pesos 1v1:0.5,3v3:0.5
    python3 model/optimize_build.py jinx --excluir ga,maw    # sin defensivos

VALIDACIÓN CRUZADA (obligatoria tras tocar datos): con pesos por defecto debe
redescubrir la build C de Jinx (Gunmetal+C44+Runaan's+IE+LDR+Kraken, 17 350 g).

Alcance v1: arquetipo de AUTOS (crítico/on-hit del motor dps_model). Kalista/Diana/
soportes usan los modelos de analysis_batch2 (optimizador propio = ROADMAP).
"""
import argparse, heapq, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "model"))
import dps_model as M

EPS_AS = 0.02          # tolerancia del tope de AS (Ley 2)
ESCENARIOS = {          # nombre → (kwargs de eval_build, métrica)
    "1v1":     (dict(),                                   "dps1"),
    "3v3":     (dict(targets=3),                          "dpsN"),
    "vs120":   (dict(armor=120),                          "dps1"),
    "vsTanque": (dict(armor=220, tank=True, enemy_hp=4500), "dps1"),
}
PESOS_DEFAULT = {"1v1": 0.30, "3v3": 0.30, "vs120": 0.20, "vsTanque": 0.20}


def pool_items(excluir=(), incluir=None):
    ex = {x.lower() for x in excluir}
    pool = [k for k in M.ITEMS if k not in M.BOOTS_ALL and k.lower() not in ex
            and k != "boots_speed"]
    if incluir:
        inc = {M.resolve(x).key for x in incluir}
        pool = [k for k in pool if k in inc]
    return pool


def pool_botas(solo=None):
    t3 = list(M.BOOT_UPGRADES.keys())          # solo Tier 3 (build final, min 10:00)
    if solo:
        wanted = {M.resolve(x).key for x in solo.split(",")}
        t3 = [b for b in t3 if b in wanted]
    return t3


def optimizar(spec_key, oro=18000, top=10, pesos=None, excluir=(), solo_botas=None,
              embudo=400, nivel=15, verbose=True, crit_min=0, pen_min=0, incluir=None):
    spec = M.CHAMPS[spec_key]
    pesos = pesos or dict(PESOS_DEFAULT)
    falta = set(pesos) - set(ESCENARIOS)
    if falta:
        sys.exit(f"escenarios desconocidos: {falta} (válidos: {list(ESCENARIOS)})")

    items = pool_items(excluir, incluir)
    botas = pool_botas(solo_botas)
    if not botas:
        sys.exit("sin botas candidatas")

    # escenario de la pasada 1 = el de mayor peso
    esc1 = max(pesos, key=pesos.get)
    kw1, met1 = ESCENARIOS[esc1]

    # constantes de AS para la poda (as_total: raw = base_as + as_ratio·B)
    lt_as = (M.LT_RANGED_STACK if spec.ranged else M.LT_MELEE_STACK) * 6
    const_B = (spec.base_bonus_as + M.lvl_as_bonus(spec, nivel) + lt_as
               + M.ALACRITY_FULL + spec.self_as_buff)
    const_raw = spec.base_as + spec.as_ratio * const_B
    as_por_item = {k: M.ITEMS[k].a_s / 100.0 for k in items}
    oro_item = {k: M.ITEMS[k].gold for k in items}
    crit_item = {k: M.ITEMS[k].crit for k in items}
    oro_min = min(oro_item.values())

    # pool ordenado por oro ascendente → poda de presupuesto más efectiva
    orden = sorted(items, key=lambda k: oro_item[k])
    idx = {k: i for i, k in enumerate(orden)}

    t0 = time.time()
    candidatos = []            # heap de (score1, oro_total,组合)
    hojas = 0
    heap = []                  # min-heap con los mejores `embudo` por score1

    def dfs(start, elegidos, g, crit_p, as_p):
        nonlocal hojas
        faltan = 5 - len(elegidos)
        if g + faltan * oro_min > oro:
            return                                    # ni con lo más barato cabe
        if crit_p > 100:
            return                                    # Ley 1: crítico desperdiciado
        if const_raw + spec.as_ratio * as_p > M.AS_CAP + EPS_AS:
            return                                    # Ley 2: AS cruda pasmada
        if faltan == 0:
            combo = botas_ctx + elegidos
            r0 = M.eval_build(spec, combo, level=nivel, validate=False)
            if r0["crit"] < crit_min or r0["pen"] < pen_min:
                return                                  # Ley 1 / Ley 3 como restricción dura
            hojas += 1
            r = M.eval_build(spec, combo, level=nivel, validate=False, **kw1) if kw1 else r0
            s = r[met1] if kw1 else r0[met1]
            if len(heap) < embudo:
                heapq.heappush(heap, (s, -g, combo))
            elif s > heap[0][0]:
                heapq.heapreplace(heap, (s, -g, combo))
            return
        for k in orden[start:]:
            dfs(idx[k] + 1, elegidos + [k], g + oro_item[k],
                crit_p + crit_item[k], as_p + as_por_item[k])

    for b in botas:
        botas_ctx = [b]
        presupuesto = oro - M.ITEMS[b].gold
        oro_save, oro = oro, presupuesto       # el DFS trabaja sobre el resto
        dfs(0, [], 0, 0.0, 0.0)
        oro = oro_save
        candidatos.extend(heap)
        heap = []

    # pasada 2: objetivo ponderado NORMALIZADO (cada escenario aporta en proporción,
    # no en magnitud absoluta: 3v3 ~10k no aplasta a vsTanque ~1.3k)
    brutos = []
    for s1, neg_g, combo in candidatos:
        detalle = {}
        for esc in ESCENARIOS:
            kw, met = ESCENARIOS[esc]
            detalle[esc] = M.eval_build(spec, combo, level=nivel, validate=False, **kw)[met]
        base = M.eval_build(spec, combo, level=nivel, validate=False)
        brutos.append((combo, detalle, base))
    max_e = {esc: max((d[esc] for _, d, _ in brutos), default=1.0) or 1.0 for esc in ESCENARIOS}
    finales = []
    for combo, detalle, base in brutos:
        score = sum(pesos.get(esc, 0.0) * (detalle[esc] / max_e[esc]) for esc in ESCENARIOS)
        finales.append((score, combo, detalle, base))
    finales.sort(key=lambda x: (-x[0], x[3]["gold"]))
    if verbose:
        print(f"[{spec.name}] hojas legales exploradas: {hojas:,} · embudo: {len(candidatos)} "
              f"· {time.time()-t0:.1f}s · presupuesto {oro:,} g · nivel {nivel}")
    return finales[:top], hojas


def imprimir(finales, spec, pesos, oro):
    nombres = lambda combo: "+".join(combo)
    w = " · ".join(f"{e}:{p:g}" for e, p in sorted(pesos.items(), key=lambda x: -x[1]))
    print(f"\n=== TOP builds · {spec.name} · objetivo [{w}] · ≤{oro:,} g ===")
    tot_w = sum(pesos.values()) or 1.0
    hdr = (f"{'#':>2} {'EFIC':>6} {'ORO':>6} {'AD':>4} {'AS':>5} {'crit':>4} {'pen':>4} "
           + " ".join(f"{e:>7}" for e in ESCENARIOS) + "  BUILD")
    print(hdr)
    for i, (score, combo, det, base) in enumerate(finales, 1):
        as_s = f"{base['AS']:.2f}" + ("*" if base["overcap"] else "")
        print(f"{i:>2} {score/tot_w*100:>5.1f}% {base['gold']:>6} {base['AD']:>4.0f} {as_s:>5} "
              f"{base['crit']:>4.0f} {base['pen']:>4.0f} "
              + " ".join(f"{det[e]:>7.0f}" for e in ESCENARIOS)
              + f"  {nombres(combo)}")
    print("(* = AS cruda excede el tope; el exceso viene de pasivas, no de ítems)")


def validar(finales, spec_key):
    """Compara el top-1 contra la build publicada en el registro (si existe)."""
    reg_path = os.path.join(ROOT, "data", "estructurada", "reportes_registry.json")
    if not os.path.exists(reg_path):
        print("⚠️ sin reportes_registry.json — corre update_reports.py baseline")
        return None
    import json
    reg = json.load(open(reg_path, encoding="utf-8"))
    pubs = []
    for f, e in reg["reportes"].items():
        if e["champion"] == spec_key and e.get("build_keys") and e.get("hook"):
            pubs.append((f, e["build_keys"]))
    if not pubs:
        print("⚠️ el registro no tiene build cuantitativa publicada para", spec_key)
        return None
    top1 = finales[0][1]
    top1_keys = sorted(M.resolve(x).key for x in top1)
    ok_global = False
    for f, bk in pubs:
        pub_keys = sorted(M.resolve(x).key for x in bk)
        r = M.eval_build(M.CHAMPS[spec_key], bk, validate=False)
        rank = next((i for i, (_, c, _, _) in enumerate(finales, 1)
                     if sorted(M.resolve(x).key for x in c) == pub_keys), None)
        mismo = pub_keys == top1_keys
        ok_global |= mismo
        print(f"{'✅ REDISCUBIERTA' if mismo else '≠ DIVERGE'} · {f}: "
              f"top-1 del optimizador {'==' if mismo else '≠'} publicada"
              + (f" (la publicada rankea #{rank} del top-{len(finales)})" if rank and not mismo else "")
              + f" · dps1 publicada {r['dps1']:.0f} vs óptima {finales[0][3]['dps1']:.0f}")
    return ok_global


def parse_pesos(s):
    out = {}
    for par in s.split(","):
        k, v = par.split(":")
        out[k.strip()] = float(v)
    return out


def main():
    ap = argparse.ArgumentParser(description="WR-LAB · optimizador exhaustivo de builds (motor dps_model)")
    ap.add_argument("champion", help="clave en CHAMPS (jinx, yunara, shyvana…)")
    ap.add_argument("--oro", type=int, default=18000, help="presupuesto total (default 18000)")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--nivel", type=int, default=15)
    ap.add_argument("--pesos", default=None, help="p.ej. 1v1:0.5,3v3:0.5 (default 0.3/0.3/0.2/0.2)")
    ap.add_argument("--excluir", default="", help="claves de ítem a excluir (coma-separadas)")
    ap.add_argument("--incluir", default=None,
                    help="restringir el pool a estos ítems (alias, coma-separados) — útil para "
                         "validación cruzada contra el pool de candidatos de un reporte")
    ap.add_argument("--botas", default=None, help="restringir botas T3 (coma-separadas, alias ok)")
    ap.add_argument("--embudo", type=int, default=400)
    ap.add_argument("--crit-min", type=float, default=0,
                    help="Ley 1 como restricción dura (p.ej. 100 = crítico exacto)")
    ap.add_argument("--pen-min", type=float, default=0,
                    help="Ley 3 como restricción dura (p.ej. 30 = pen %% mínima)")
    ap.add_argument("--validar", action="store_true", help="comparar contra la build publicada del registro")
    ap.add_argument("--contra", default=None, help="build de referencia extra (alias separados por coma)")
    args = ap.parse_args()

    ck = args.champion.lower()
    if ck not in M.CHAMPS:
        sys.exit(f"'{ck}' no está en CHAMPS. Especs: {sorted(M.CHAMPS)}")
    pesos = parse_pesos(args.pesos) if args.pesos else dict(PESOS_DEFAULT)
    excluir = tuple(x for x in args.excluir.split(",") if x)

    finales, hojas = optimizar(ck, oro=args.oro, top=args.top, pesos=pesos,
                               excluir=excluir, solo_botas=args.botas,
                               embudo=args.embudo, nivel=args.nivel,
                               crit_min=args.crit_min, pen_min=args.pen_min,
                               incluir=[x for x in args.incluir.split(",")] if args.incluir else None)
    if args.contra:
        ref = [x.strip() for x in args.contra.split(",")]
        M.validate_slots(ref)
        det = {e: M.eval_build(M.CHAMPS[ck], ref, level=args.nivel, validate=False, **kw)[met]
               for e, (kw, met) in ESCENARIOS.items()}
        base = M.eval_build(M.CHAMPS[ck], ref, level=args.nivel, validate=False)
        # re-normalizar incluyendo la referencia
        max_e = {e: max([det[e]] + [d[e] for _, _, d, _ in finales]) for e in ESCENARIOS}
        def score_norm(d):
            tot = sum(pesos.values()) or 1.0
            return sum(pesos.get(e, 0.0) * (d[e] / (max_e[e] or 1.0)) for e in ESCENARIOS)
        finales = [(score_norm(d), c, d, b) for _, c, d, b in finales]
        finales.append((score_norm(det), ref, det, base))
        finales.sort(key=lambda x: (-x[0], x[3]["gold"]))
        finales = finales[:args.top + 1]
    imprimir(finales, M.CHAMPS[ck], pesos, args.oro)
    if args.validar:
        print()
        ok = validar(finales, ck)
        if ok is False:
            sys.exit(2)


if __name__ == "__main__":
    main()
