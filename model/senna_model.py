# -*- coding: utf-8 -*-
"""
WR-LAB · SENNA — modelo por medida (7.3 + hotfix 7.3a) · añadidura al framework (batch3)
========================================================================================
Senna NO es representable por el motor "autos" puro ni por el motor "aliado" puro:
  - Daño propio = autos (crit mod 0.9) + Relic Cannon on-hit + Living Extraction + Q + W
    (rotación con CD reducido por autos) → híbrido autos/rotación.
  - Support = además valor-aliado (cura Q, escudo R, procs de enchanter) → motor mixto.

FUENTES DE NÚMEROS (jerarquía lab):
  1. Notas oficiales 7.3 y 7.3a (data/raw/patch73*.txt; §3/§3b del bundle):
     AS 0.3/0.3/1.1/0.025 (7.3a) · crit 90 % · niebla: crit/20 = 10 % · Living Extraction 1-10 %
     · Q base 50/80/110/140 (+60 % bAD) · R 250/400/550 + 120 % bAD + 70 % AP · escudo R
     120/160/200 + 50 % AP + 2×Niebla · HP base 600→570.
  2. Wiki oficial (WR:Senna): rango 625 · +15 rango/20 niebla (cap +400) · exceso crit→35 % vamp
     · Relic Cannon on-hit 20 % AD + robo MS · Q/W mecánicas (Q -1 s CD por auto; W root al morir
     el objetivo) · R recoge wraiths globales.
  3. wr-meta/wildriftfire/wildriftcore (fichas vivas 29-sep/11-oct-2026): valores de tooltip,
     builds y runas meta.

SUPUESTOS DECLARADOS (todos auditables en §10 del reporte):
  - AD base 54 (wiki V6.2c; wr-meta muestra 50 → discrepancia D1; 54 = techo conservador-alto,
    50 el piso; Δ en DPS < 2 %).
  - Relic Cannon on-hit = 20 % AD (wiki). Sensibilidad con "+10 plano" (wr-meta) → ver --sens.
  - Niebla por checkpoint (mediana de guías wildriftcore + reglas de drop; VERIFICAR EN JUEGO):
      support: L9=50, L12=90, L15=140 · duo: L9=35, L12=65, L15=110 · late (22 min): 180-200.
  - Q/W NO critican (sin mención oficial; conservador). Q aplica on-hit (wiki) → sí proca
    on-hit plano de ítems y BotRK (declarado).
  - Q en 3v3 impacta a 2 objetivos (línea 1 300×280; conservador vs 3).
  - Living Extraction: 1 golpe cada 6 s por objetivo a vida COMPLETA (convención engine BotRK).
  - Black Cleaver: 5 stacks (30 % reducción de armadura) en escenarios sostenidos (tarda ~4 s;
    convención de uptime pleno como BotRK-enemy_hp).
  - Navori "Deft Strikes": CD efectivo ×0.75 de Q/W/E (convención D8 del reporte Xayah).
  - Energized: proc cada 7 autos (convención engine M.eval_build); Statikk "5 stacks extra" NO
    modelado (conservador, como Flurry de Yun Tal en Xayah).
  - Scythe (quest): 0 g, +10 AH; Soulcast/adaptativos NO modelados (convención Yuumi/Karma).
  - Revitalize OFF (runas meta = Bone Plating); variante +5 HSP disponible.
  - Censer uptime = min(1, 6 s / q_cd) sobre un ADC 2.6 AS × 330 dmg/golpe (convención Yuumi).
  - R fuera del DPS sostenido (CD 75-85 s): se reporta como burst/valor-aliado aparte.
  - Keystone baseline: Fleet Footwork (sin DPS directo; sustain anotado) + Legend: Alacrity
    (21 %) + Cut Down (+6.57 % vsTanque, +3.29 % resto — convención optimize_runes).
    Variantes LT / First Strike en --sens.
"""
import os, sys, math, time, heapq, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dps_model as M
from dps_model import ChampSpec, resolve, as_total, lvl_as_bonus, lt_bullet, validate_slots, \
    CRIT_DMG_BASE, CRIT_DMG_IE, AS_CAP, LT_RANGED_STACK, ALACRITY_FULL

# ---------------------------------------------------------------- spec oficial (apéndice 7.3 + override 7.3a)
M.CHAMPS["senna"] = ChampSpec(
    name="Senna", base_ad=54, ad_growth=0.0,            # wiki V6.2c (D1: wr-meta muestra 50)
    base_as=0.3, as_ratio=0.3, base_bonus_as=1.1, as_per_lvl=0.025,   # 7.3a OFICIAL
    ranged=True, attack_range=625,
    self_as_buff=0.0, aa_mult=1.0, aa_aoe=False,
    crit_dmg_mod=0.9,            # 7.3: críticos al 90 % del daño crítico normal
    uses_magnification=True,     # siempre ataca a >=550 (rango base 625 + niebla)
    notes=("Niebla: +1.25 AD/stack, +15 rango y +10 % crit/20 stacks (cap +400 rango/100 % crit); "
           "exceso crit → 35 % physical vamp. Relic Cannon on-hit 20 % AD (wiki) + robo MS. "
           "Q 50/80/110/140+60 % bAD (CD -1 s/auto), W 90/155/220/285+70 % bAD, "
           "R 250/400/550+120 % bAD+70 % AP, escudo 120/160/200+50 % AP+2×niebla."),
)
SPEC = M.CHAMPS["senna"]

# ---------------------------------------------------------------- ítems fuera de M.ITEMS (stats oficiales §8/§15)
def S(g, **kw):
    d = dict(g=g, ad=0, ap=0, a_s=0, crit=0, pen=0, ls=0, mr=0, armor=0, hp=0, ah=0, ms=0, hsp=0)
    d.update(kw)
    return d
SUP = {
 "scythe":      S(0,    ah=10, nombre="Black Mist Scythe (quest)"),
 "cleaver":     S(3000, ad=40, hp=400, ah=20, carve=0.30, nombre="Black Cleaver"),
 "serpent":     S(2800, ad=50, ah=10, shieldreaver=1, nombre="Serpent's Fang"),
 "censer":      S(2400, ap=50, hsp=8, ms=4, censer=1, nombre="Ardent Censer"),
 "staff":       S(2400, ap=50, hsp=8, ah=10, nombre="Staff of Flowing Waters"),
 "echoes":      S(2400, ap=40, hp=200, ah=20, echo=1, nombre="Echoes of Helia"),
 "redemption":  S(2450, ap=40, hsp=8, ah=10, redempt=1, nombre="Redemption"),
 "mandate":     S(2600, ap=60, ah=20, mandate=1, nombre="Imperial Mandate"),
 "harmonic":    S(2500, ap=40, hp=200, ah=20, harmonic=1, nombre="Harmonic Echo"),
 "mikael":      S(2500, hp=300, hsp=9, ah=15, cleanse=1, nombre="Mikael's Blessing"),
 "shurelya":    S(2500, ap=55, ah=20, ms=4, nombre="Shurelya's Battlesong"),
 "zeke":        S(2400, hp=300, armor=25, mr=25, ah=10, nombre="Zeke's Convergence"),
 "locket":      S(2600, hp=200, armor=30, mr=30, ah=10, nombre="Locket of the Iron Solari"),
 "morello":     S(2650, ap=75, hp=300, ah=15, gw=1, nombre="Morellonomicon"),
 "horizon":     S(2700, ap=80, ah=25, nombre="Horizon Focus"),
 "duskdawn":    S(3100, hp=300, a_s=20, ap=60, ah=20, nombre="Dusk and Dawn"),
 "liandry":     S(3000, ap=70, hp=300, nombre="Liandry's Torment"),
 "youmuu":      S(3000, ad=55, ah=15, ms=4, nombre="Youmuu's Ghostblade"),   # +15 pen PLANA no modelada (conservador)
 "trinity":     S(3333, hp=333, ad=36, a_s=30, ah=15, nombre="Trinity Force"),  # spellblade de base AD (54) → débil en ella
}
SUP_KEYS = set(SUP)

# registrar los añadidos en el registry del motor (resolve/validate_slots/ALIAS funcionen)
for _k, _d in SUP.items():
    if _k not in M.ITEMS:
        M.ITEMS[_k] = M.Item(key=_k, gold=_d["g"], ad=_d.get("ad",0), ap=_d.get("ap",0),
                             a_s=_d.get("a_s",0), crit=_d.get("crit",0), pen=_d.get("pen",0),
                             ls=_d.get("ls",0), mr=_d.get("mr",0), armor=_d.get("armor",0),
                             hp=_d.get("hp",0), ah=_d.get("ah",0), ms=_d.get("ms",0),
                             comment="SENNA-SUP: " + _d.get("nombre", _k))
    if _d.get("nombre"):
        M.ALIAS.setdefault(_d["nombre"], _k)

def it(key):
    """Accesor unificado: M.ITEMS (motor) o SUP (añadidos)."""
    if key in SUP_KEYS:
        d = SUP[key]
        return dict(g=d["g"], ad=d.get("ad",0), ap=d.get("ap",0), a_s=d.get("a_s",0),
                    crit=d.get("crit",0), pen=d.get("pen",0), ls=d.get("ls",0),
                    mr=d.get("mr",0), armor=d.get("armor",0), hp=d.get("hp",0),
                    ah=d.get("ah",0), ms=d.get("ms",0), hsp=d.get("hsp",0),
                    ie=False, kraken=False, magnification=False, runaan=False,
                    energized=0, onhit_flat=0, onhit_pct_current=0, spellblade=0,
                    giant_slayer=0, execute_pct=0,
                    carve=d.get("carve",0), censer=d.get("censer",0), echo=d.get("echo",0),
                    nombre=d.get("nombre", key))
    x = resolve(key)
    return dict(g=x.gold, ad=x.ad, ap=x.ap, a_s=x.a_s, crit=x.crit, pen=x.pen, ls=x.ls,
                mr=x.mr, armor=x.armor, hp=x.hp, ah=x.ah, ms=x.ms, hsp=0,
                ie=x.ie, kraken=x.kraken, magnification=x.magnification, runaan=x.runaan,
                energized=x.energized, onhit_flat=x.onhit_flat,
                onhit_pct_current=x.onhit_pct_current, spellblade=x.spellblade,
                giant_slayer=x.giant_slayer, execute_pct=x.execute_pct,
                carve=0, censer=0, echo=0, nombre=key)

NOMBRE = {}
def nombre(key):
    if key not in NOMBRE:
        if key in SUP_KEYS: NOMBRE[key] = SUP[key].get("nombre", key)
        else:
            for alias, k in M.ALIAS.items():
                if k == resolve(key).key and len(alias) > len(NOMBRE.get(key,"")):
                    NOMBRE[key] = alias
            NOMBRE.setdefault(key, resolve(key).key)
    return NOMBRE[key]

# ---------------------------------------------------------------- parámetros por rol/checkpoint
MIST = {("support",9):50, ("support",12):90, ("support",15):140,
        ("duo",9):35,     ("duo",12):65,     ("duo",15):110}
PRESUPUESTO = {"support":13000, "duo":17500}
CHECK_BUDGET = {("support",9):4500, ("support",12):7500, ("support",15):13000,
                ("duo",9):7500, ("duo",12):11500, ("duo",15):17500}

Q_BASE = [50,80,110,140]; W_BASE = [90,155,220,285]; R_BASE = [250,400,550]
def q_rank(l): return min(4, (l+2)//3)
def w_rank(l): return min(4, max(1, 1+(l-2)//3))
def r_rank(l): return min(3, max(1, 1+(l-5)//4))

def mist_stats(mist):
    brackets = mist//20
    return dict(ad=1.25*mist, crit=10*brackets, rango=625+15*brackets, brackets=brackets)

# ---------------------------------------------------------------- evaluación principal
def eval_senna(items, mist=140, level=15, targets=1, armor=0.0, tank=False, enemy_hp=2200,
               keystone="fleet", alacrity=True, relic="wiki", navori=0.75,
               cleaver_full=True, cutdown=True, role="support", validate=False, ad_extra=0.0):
    if validate:
        validate_slots(items, final=(len(items)==6))
    its = [it(k) for k in items]
    gold = sum(i["g"] for i in its)
    ms_ = mist_stats(mist)

    ad_total = SPEC.base_ad + ms_["ad"] + sum(i["ad"] for i in its) + ad_extra
    bonus_ad = ms_["ad"] + sum(i["ad"] for i in its) + ad_extra     # base 54 NO es bonus (ratios bAD)
    ap       = sum(i["ap"] for i in its)
    ah       = sum(i["ah"] for i in its)
    hsp      = sum(i["hsp"] for i in its)
    ls       = sum(i["ls"] for i in its)
    pen_pct  = min(sum(i["pen"] for i in its), 100)
    crit_items = sum(i["crit"] for i in its)
    crit_total = crit_items + ms_["crit"]
    crit_eff   = min(crit_total, 100)/100.0
    excess     = max(0.0, crit_total-100)
    vamp_exc   = 0.35*excess                       # physical vamp del exceso (35 %)

    # --- attack speed (fórmula oficial 7.3; keystone LT opcional)
    lt = (keystone == "lt")
    ai = sum(i["a_s"] for i in its)/100.0
    lt_as = LT_RANGED_STACK*6 if lt else 0.0
    alac = ALACRITY_FULL if alacrity else 0.0   # WR: LT y Legend: Alacrity COEXISTEN (baseline del lab, ver Jinx)
    B = SPEC.base_bonus_as + lvl_as_bonus(SPEC, level) + ai + lt_as + alac
    AS = min(SPEC.base_as + SPEC.as_ratio*B, AS_CAP)
    raw_AS = SPEC.base_as + SPEC.as_ratio*B

    # --- multiplicadores
    cdmg = (CRIT_DMG_IE if any(i["ie"] for i in its) else CRIT_DMG_BASE) * SPEC.crit_dmg_mod
    cmult = 1 + crit_eff*(cdmg-1)
    magn = 1.10 if any(i["magnification"] for i in its) else 1.0    # siempre >=550 de rango
    amp  = 1 + (sum(i["giant_slayer"] for i in its)/100.0 if tank else 0)
    amp_cd = 1.0
    if cutdown:
        amp_cd = 1.0657 if tank else 1.0329                          # convención optimize_runes

    # --- mitigación (Black Cleaver: reducción de armadura ANTES de pen %)
    carve = 0.30 if (cleaver_full and any(i["carve"] for i in its)) else 0.0
    armor_eff = armor*(1-carve)
    mit = 100/(100+armor_eff*(1-pen_pct/100)) if armor > 0 else 1.0

    # --- autos + Relic Cannon + Living Extraction
    hit = ad_total*cmult*magn*amp*amp_cd
    d = AS*hit
    relic_per_hit = 0.20*ad_total if relic == "wiki" else 10.0       # D2: wiki 20 % AD vs wr-meta +10 plano
    d += AS*relic_per_hit*amp*amp_cd
    extract_pct = 0.01 + 0.09*(level-1)/14
    d += extract_pct*enemy_hp/6.0*amp_cd                              # 1 proc/6 s (vida completa, convención)

    # --- ítems procs (convenciones engine)
    for i in its:
        if i["kraken"]:
            d += AS/3*(168*(level/15))*(1+0.0075*50)*amp_cd           # missing 50 % default
        if i["energized"]:
            d += AS/7*i["energized"]                                   # mágico (aprox física, conservador)
        if i["onhit_flat"]:
            d += AS*i["onhit_flat"]
        if i["onhit_pct_current"]:
            d += AS*max(15, i["onhit_pct_current"]/100*enemy_hp)
        if i["spellblade"]:
            d += (1/1.5)*(1.35*SPEC.base_ad + 80*crit_eff)             # base AD 54 fijo → ER flojo (correcto)
    if lt:
        d += AS*lt_bullet(SPEC, level, B)

    # --- Q / W en rotación (CD por haste; Q además -1 s por auto; Navori ×0.75)
    nav = navori if any(resolve(k).key == "navori" for k in items if k not in SUP_KEYS) else 1.0
    haste_mult = 100/(100+ah)
    q_cd = 15*haste_mult*nav/(1+AS)          # -1 s de CD por autoataque (uptime pleno en pelea)
    w_cd = 11*haste_mult*nav
    q_dmg = Q_BASE[q_rank(level)-1] + 0.60*bonus_ad
    w_dmg = W_BASE[w_rank(level)-1] + 0.70*bonus_ad
    # on-hit de Q (wiki): proca on-hit plano y %-vida de ítems, 1 vez por cast
    q_onhit = sum(i["onhit_flat"] for i in its) + sum(max(15, i["onhit_pct_current"]/100*enemy_hp) for i in its)
    q_dps = (q_dmg*amp*amp_cd + q_onhit)/q_cd
    w_dps = w_dmg*amp*amp_cd/w_cd
    d += q_dps + w_dps

    # --- AoE
    aoe = 0.0
    if targets > 1:
        aoe += q_dps*(min(targets,2)-1)                               # línea de Q (2 objetivos, conservador)
        if any(i["runaan"] for i in its):
            aoe += AS*0.55*ad_total*cmult*amp*amp_cd*min(2, targets-1)

    dps1 = d*mit
    dpsN = (d+aoe)*mit

    # --- sustain
    heal = dps1*(ls+vamp_exc)/100
    keys = {resolve(k).key for k in items if k not in SUP_KEYS}
    if "gunmetal" in keys: heal += 12*AS
    q_heal_base = (130 + 0.40*bonus_ad + 0.25*ap)                    # rank 4
    q_self_hps = q_heal_base*(1+hsp/100)/q_cd                         # se autocura en 1v1
    if keystone == "firststrike":
        dps1 *= 1.0084; dpsN *= 1.0084                                # +0.84 % efectivo (convención lab)

    # --- burst R (fuera de DPS sostenido)
    r_dmg = R_BASE[r_rank(level)-1] + 1.20*bonus_ad + 0.70*ap
    r_shield_ally = (120 if level < 9 else (160 if level < 13 else 200)) + 0.50*ap + 2*mist
    r_shield_ally *= (1+hsp/100)
    r_cd = (85 if level < 9 else (80 if level < 13 else 75))*haste_mult

    # --- valor aliado (support)
    censer_uptime = min(1.0, 6.0/q_cd) if any(i["censer"] for i in its) else 0.0
    adc_dps_add = censer_uptime*(0.115*2.6*330 + 2.6*25)              # convención yuumi() del lab
    echo_val = 0.30*q_heal_base*(1+hsp/100)/q_cd if any(i["echo"] for i in its) else 0.0
    q_heal_hps = q_heal_base*(1+hsp/100)/q_cd + echo_val
    r_shield_min_team = r_shield_ally*3*60/r_cd                       # 3 aliados, conservador

    return dict(gold=gold, AD=ad_total, bAD=bonus_ad, AP=ap, AH=ah, AS=AS, raw_AS=raw_AS,
                crit=crit_total, crit_eff=crit_eff*100, excess=excess, vamp=vamp_exc,
                pen=pen_pct, HSP=hsp, rango=ms_["rango"], mist=mist,
                dps1=dps1, dpsN=dpsN, heal=heal+q_self_hps, q_heal_hps=q_heal_hps,
                r_shield=r_shield_ally, r_shield_min=r_shield_min_team, r_dmg=r_dmg,
                adc_dps_add=adc_dps_add, q_cd=q_cd, w_cd=w_cd, overcap=raw_AS > AS_CAP,
                q_dmg=q_dmg, w_dmg=w_dmg, q_slow=15+10*bonus_ad/100+6*ap/100)

ESC_OFF = {"1v1": dict(), "3v3": dict(targets=3),
           "vs120": dict(armor=120), "vsTanque": dict(armor=220, tank=True, enemy_hp=4500)}
PESOS_OFF = {"1v1":0.30, "3v3":0.30, "vs120":0.20, "vsTanque":0.20}

def score_build(items, mist, level, role, budget, w_off=None, w_ally=None, **kw):
    """Score normalizado por escenario (convención optimize_build pasada 2)."""
    if role == "duo":
        w_off, w_ally = 1.0, 0.0
    else:
        w_off  = 0.55 if w_off  is None else w_off
        w_ally = 0.45 if w_ally is None else w_ally
    det = {}
    base = None
    for e, k in ESC_OFF.items():
        r = eval_senna(items, mist=mist, level=level, role=role, **k, **kw)
        det[e] = r["dpsN"] if e == "3v3" else r["dps1"]
        if base is None: base = r
    ally = {"q_hps": base["q_heal_hps"], "r_shield_min": base["r_shield_min"],
            "adc_dps": base["adc_dps_add"]}
    return base, det, ally

# ---------------------------------------------------------------- pools
BOOT_POOL = ["gunmetal", "crimson", "chainlaced", "armored_adv", "armorcrusher", "immortal_treads"]
DUO_POOL = ["statikk", "rfc", "ie", "mortal", "ldr", "c44", "gale", "collector", "bt", "storm",
            "navori", "yuntal", "kraken", "runaan", "er", "pd", "cleaver", "serpent", "manamune",
            "guinsoo", "botrk", "terminus", "witsend", "duskdawn", "ga", "shieldbow", "scimitar",
            "deathsdance", "maw", "trinity"]
SUP_POOL = ["statikk", "rfc", "ie", "mortal", "ldr", "c44", "gale", "collector", "bt", "storm",
            "navori", "yuntal", "cleaver", "serpent", "youmuu", "censer", "staff", "echoes",
            "redemption", "mandate", "harmonic", "mikael", "shurelya", "zeke", "locket",
            "morello", "horizon", "duskdawn", "ga", "shieldbow", "scimitar", "maw", "er", "runaan"]
GRUPO_PEN = {"ldr", "mortal", "terminus"}   # Ley 3b (items_exclusivos.csv)

def legales(combo):
    if len(set(GRUPO_PEN) & set(combo)) > 1: return False
    return True

def optimizar_senna(role, nivel=15, mist=None, oro=None, top=8, embudo=300, **kw):
    mist = mist if mist is not None else MIST[(role, nivel)]
    oro  = oro  if oro  is not None else CHECK_BUDGET[(role, nivel)]
    eval_kw = {k: v for k, v in kw.items() if k not in ("w_off", "w_ally")}
    pool = DUO_POOL if role == "duo" else SUP_POOL
    n_elegir = 5 if role == "duo" else 4
    fixed = [] if role == "duo" else ["scythe"]
    oro_fijo = sum(it(k)["g"] for k in fixed)
    oro_item = {k: it(k)["g"] for k in pool}
    orden = sorted(pool, key=lambda k: oro_item[k])
    oro_min = min(oro_item.values())
    idx = {k:i for i,k in enumerate(orden)}
    resultados, hojas = [], 0
    t0 = time.time()
    for b in BOOT_POOL:
        gb = it(b)["g"]
        heap = []
        def dfs(start, elegidos, g):
            nonlocal hojas
            faltan = n_elegir - len(elegidos)
            if g + faltan*oro_min > oro - oro_fijo - gb: return
            if faltan == 0:
                combo = [b] + fixed + list(elegidos)
                if not legales(combo): return
                hojas += 1
                # pasada 1 (embudo barato): 1v1 + heurística de valor aliado en support
                base = eval_senna(combo, mist=mist, level=nivel, role=role, **eval_kw)
                s = base["dps1"] + (base["q_heal_hps"]*2 + base["adc_dps_add"] if role == "support" else 0.0)
                if len(heap) < embudo: heapq.heappush(heap, (s, -g, combo))
                elif s > heap[0][0]:   heapq.heapreplace(heap, (s, -g, combo))
                return
            for k in orden[start:]:
                dfs(idx[k]+1, elegidos+[k], g+oro_item[k])
        dfs(0, [], 0)
        resultados.extend(heap)
    # pasada 2: score ponderado normalizado
    brutos = []
    for s1, neg_g, combo in resultados:
        base, det, ally = score_build(combo, mist, nivel, role, oro, **eval_kw)
        brutos.append((combo, det, ally, base))
    max_off  = {e: max((d[e] for _,d,_,_ in brutos), default=1.0) or 1.0 for e in ESC_OFF}
    max_ally = {e: max((a[e] for _,_,a,_ in brutos), default=1.0) or 1.0 for e in ("q_hps","r_shield_min","adc_dps")}
    w_off, w_ally = (1.0, 0.0) if role == "duo" else (kw.get("w_off",0.55), kw.get("w_ally",0.45))
    finales = []
    for combo, det, ally, base in brutos:
        off  = sum(PESOS_OFF[e]*(det[e]/max_off[e]) for e in ESC_OFF)
        al   = (0.35*ally["q_hps"]/max_ally["q_hps"] + 0.30*ally["r_shield_min"]/max_ally["r_shield_min"]
                + 0.35*ally["adc_dps"]/max_ally["adc_dps"]) if role == "support" else 0.0
        score = w_off*off + w_ally*al
        finales.append((score, combo, det, ally, base))
    finales.sort(key=lambda x: (-x[0], x[4]["gold"]))
    return finales[:top], hojas, time.time()-t0

# ---------------------------------------------------------------- CLI
def fmt_combo(combo):
    return "+".join(nombre(k) for k in combo)

def tabla(finales, titulo):
    print(f"\n=== {titulo} ===")
    print(f"{'score':>6} {'oro':>6} {'AD':>5} {'AS':>5} {'crit':>5} {'pen':>4} {'1v1':>6} {'3v3':>6} "
          f"{'vs120':>6} {'vsTq':>6} {'Q-h/s':>6} {'R-sh':>5} {'ADC+':>5}  BUILD")
    for sc, combo, det, ally, base in finales:
        print(f"{sc:6.3f} {base['gold']:6d} {base['AD']:5.0f} {base['AS']:5.2f} {base['crit']:5.0f} "
              f"{base['pen']:4.0f} {det['1v1']:6.0f} {det['3v3']:6.0f} {det['vs120']:6.0f} "
              f"{det['vsTanque']:6.0f} {ally['q_hps']:6.0f} {base['r_shield']:5.0f} "
              f"{ally['adc_dps']:5.0f}  {fmt_combo(combo)}")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("rol", nargs="?", default="ambos", choices=["support","duo","ambos"])
    ap.add_argument("--nivel", type=int, default=15)
    ap.add_argument("--mist", type=int, default=None)
    ap.add_argument("--oro", type=int, default=None)
    ap.add_argument("--top", type=int, default=8)
    ap.add_argument("--w-off", type=float, default=None)
    args = ap.parse_args()
    roles = ["support","duo"] if args.rol == "ambos" else [args.rol]
    kw = {}
    if args.w_off is not None: kw = dict(w_off=args.w_off, w_ally=round(1-args.w_off,2))
    for role in roles:
        fin, hojas, t = optimizar_senna(role, nivel=args.nivel, mist=args.mist, oro=args.oro,
                                        top=args.top, **kw)
        mist = args.mist if args.mist is not None else MIST[(role,args.nivel)]
        print(f"\n[{role}] hojas legales: {hojas:,} · {t:.1f}s · nivel {args.nivel} · niebla {mist} "
              f"· oro ≤ {args.oro or CHECK_BUDGET[(role,args.nivel)]}")
        tabla(fin, f"SENNA {role.upper()} — top {args.top} (nivel {args.nivel}, niebla {mist})")
