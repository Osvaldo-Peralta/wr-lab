# -*- coding: utf-8 -*-
"""
WR-LAB · model/chogath_model.py — MOTOR ROTACIÓN-TANQUE (batch4, 12/10/2026)
=============================================================================
El motor que el lab tenía PENDIENTE para Cho'Gath (SIN_MOTOR: "tanque AP (Feast) —
el motor de autos no tiene sentido; ver ESCALADO_DE_TAMANIO.md y el modelo de
rotación (pendiente en batch2)"). Implementa el protocolo §1b.6 del apéndice de
TAMAÑO:
  1. Ventanas de supervivencia por build (Gargoyle/Twinguard/Mantle/botas/Kaenic…).
  2. EHP efectivo EN VENTANA (no solo estático).
  3. Curva de stacks de Feast por minuto + execute de R por punto de la partida.
  4. Reglas de compra de ítems de tamaño verificadas con números.

Métricas del arquetipo Tanque (TEMPLATE §A.5): EHP + ventanas + execute R + daño
de utilidad (rotación Q/W/E + pasivas de ítems) + sustain. DPS de autos NO es la
métrica principal (AS 0.87 a nivel 15 — Ley 2 muerta; crítico/AD — Ley 4 muertos).

FUENTES (todo desde WR-LAB v1.15 bundle 11/10/2026):
  - Ficha Cho'Gath wr-meta 24/09: stats base + Q/W/E/R valores 7.3 (buff 7.2c incluido).
  - Apéndice AS oficial 7.3: ratio 0.625 / base 0.625 / BBA 0.28 / growth 0.008.
  - items_7.3.csv (186 ítems) + diff oficial de ítems 7.3 (Mantle/Twinguard/FoN/
    Sunfire/Frozen Heart/Abyssal/Winter's reworks) + apéndice ESCALADO_DE_TAMAÑO.
  - Runas 7.3 (runas_7.3.md): Grasp 3.3 %/1.3 %/+10 HP, Demolish 85+28 %,
    Overgrowth +3/3 minions y +3 % a 30 stacks, Transcendence +5/+5 AH,
    Axiom Arcanist +10 % daño de R y −7 % CD por takedown.
  - Smite 7.3/7.3a (upgrades 600→1000→1400), torretas 7 000 HP,
    Crystalline Overgrowth 3.3–18.9 %.

SUPUESTOS DECLARADOS (ver §9 de la ficha):
  A1  Feast retroactivo al subir R (80→120→160/stack aplica a stacks existentes,
      comportamiento PC). Sensibilidad: si NO retroactivo, −480 HP a 22 stacks;
      rankings sin cambio.
  A2  Twinguard Endurance = ×1.3 a armadura/MR TOTALES en combate (convención del
      código de ESCALADO_DE_TAMAÑO; el texto de intención 7.3 dice "bonus" → D2).
  A3  Axiom Arcanist amplifica el daño VERDADERO de R (+10 %). Sensibilidad D4.
  A4  Heartsteel: 1 proc por ventana de 10 s (carga de 2.5 s completada al entrar).
  A5  Runas acumuladas por minuto: Grasp +10 HP × ~2 procs/min (cap 400 a min 20);
      Overgrowth +3 HP por 3 unidades (~6/min, cap 100 planos) y +3 % HP máx desde
      ~min 13 (30 stacks).
  A6  E (cono): objetivos promedio en teamfight = min(3, 1.5 + 1.5×(size−1)/1.55)
      (la anchura escala con tamaño; el juego no publica la fórmula → heurística).
  A7  Ítems condicionales (Kaenic, Mantle, Sterak's, Randuin's, Frozen Heart,
      Thornmail thorns) puntúan al 50 % de su valor teórico (uptime parcial).
  A8  Block de botas Plated/Armored cubre el 70 % del DPS físico entrante (autos).
  A9  Escudos con decaimiento (Gargoyle 2.5 s) cuentan al 75 % en la ventana de 5 s.
  A10 Exclusividad "immolate": Sunfire Aegis y Hollow Radiance NO stackean
      (misma pasiva Immolate) — extensión de Ley 3b declarada.
  A11 Madness (Liandry's) y Void Corruption (Riftmaker) amplifican solo daño
      MÁGICO propio; promedio 10 s: ×1.051 y ×1.054.
  A12 Torment uptime 100 % en pelea (E cada ~1.2 s refresca el burn de 3 s).
  A13 Heartsteel growth: +15 % del daño de cada proc como HP permanente. Snapshot
      estático no lo captura → término explícito: ~0.9 procs/min desde min 9.5
      × ~45 HP/proc (media entre +34 a 2 500 HP y +58 a 7 000, apéndice TAMAÑO).
      A min 20: ≈ +425 HP; min 24: ≈ +590 HP.
  A14 Smite upgrade por minuto (aprox): 600 (<8'), 1 000 (8–14'), 1 400 (≥14').
"""
import itertools, json

# ══════════════════════════════ BASE CHAMP (crecimientos spec 7.3) ══════════════════════════════
def base(level):
    return dict(hp=690+128*(level-1), armor=46+4.5*(level-1), mr=40+2*(level-1),
                ad=62+4*(level-1), mana=380+50*(level-1), regen5=8+0.86*(level-1),
                AS=0.625*(1+0.28+0.008*(level-1)))
ATT_RANGE = 125

# ══════════════════════════════ ÍTEMS (items_7.3.csv + diff 7.3) ══════════════════════════════
BOOTS = {
 'ArmoredAdvance': dict(g=2200, hp=150, armor=30, block=0.10,
    shield_phys=lambda HP: (75 + 0.08*HP)*0.42),          # Noxian Endurance CD12 en ventana 5s
 'Chainlaced':     dict(g=2200, hp=150, mr=30, ten=30,
    shield_mag=lambda HP: (65 + 0.05*HP)*0.42),            # Noxian Persistence
 'ImmortalTreads': dict(g=2000, ap=20, omnivamp=0.05),     # Gluttonous T3 (adaptive→AP)
}
BOOTS_T2 = {
 'Plated':  dict(g=1200, hp=150, armor=20, block=0.10),
 'Mercurys':dict(g=1200, hp=150, mr=25, ten=30),
 'Gluttonous': dict(g=1000, ap=20, omnivamp=0.05),
}

ITEMS = {
 'Heartsteel':   dict(g=3000, hp=700, ah=20, hpregen=1.5, hs_proc=1),
 'HollowRadiance':dict(g=2800, hp=400, mr=40, ah=15, immolate=('hollow',)),
 'Sunfire':      dict(g=2900, hp=350, armor=40, ah=15, immolate=('sunfire',)),
 'Liandry':      dict(g=3000, hp=300, ap=70, torment=1, madness=1),
 'Riftmaker':    dict(g=3100, hp=350, ap=70, ah=15, voidcorr=1, omnivamp=0.10, hp2ap=0.02),
 'RodOfAges':    dict(g=2700, hp=500, ap=90, mana=700, eternity=1),   # Veteran 10 stacks incluido
 'Rylai':        dict(g=2700, hp=350, ap=65, slow=1),
 'Morello':      dict(g=2650, hp=300, ap=75, ah=15, gw=1),
 'Cryptbloom':   dict(g=3000, ap=75, pen_p=30, ah=20),
 'Abyssal':      dict(g=2400, hp=350, mr=45, ah=10, unmake=1),
 'Zeke':         dict(g=2400, hp=300, armor=25, mr=25, ah=10, ult_haste=10, zeke=1),
 'FrozenHeart':  dict(g=2550, armor=80, mana=400, ah=20, as_slow=1),
 'Thornmail':    dict(g=2700, hp=200, armor=75, thorns=1, gw=1),
 'Randuin':      dict(g=2800, hp=400, armor=75, anticrit=1),
 'DeadMans':     dict(g=2800, hp=350, armor=70, ms=4),
 'ForceOfNature':dict(g=2800, hp=400, mr=60, ms=5, absorb=1),          # 7.3: sin % dmg reduction
 'KaicRookern':  dict(g=2800, hp=350, mr=85, hpregen=1.0, kaenic=1),
 'Warmog':       dict(g=2850, hp=700, ah=20, hpregen=1.0, warmog=1, blessed=0.30),
 'Gargoyle':     dict(g=2900, hp=200, armor=45, mr=45, ah=10, garg=1),
 'UnendingDespair':dict(g=3000, hp=300, armor=40, mr=40, ah=10, anguish=1),
 'Iceborn':      dict(g=3000, hp=300, armor=50, mana=250, ah=30, spellblade=1, slow=1),
 'Mantle':       dict(g=2550, hp=600, ah=20, mantle=1),
 'Twinguard':    dict(g=3200, hp=300, armor=50, mr=50, tw=1),
 'TitanicHydra': dict(g=3000, hp=450, ad=40, titanic=1),
 'Fimbulwinter': dict(g=2600, hp=500, mana=1200, ah=15, awe=0.15, colossus=1),
 'OverlordBlood':dict(g=3200, hp=450, ad=30, tyranny=0.025),   # control Ley 4 (AD muerto)
 'Sterak':       dict(g=3200, hp=400, ten=20, sterak=1),       # control (AD base muerto)
 'BlackCleaver': dict(g=3000, hp=400, ad=40, ah=20, sunder=1), # control (físico muerto)
 'Zhonyas':      dict(g=3300, ap=110, armor=40, stasis=1),     # pool AP comparativo
 'Rabadon':      dict(g=3400, ap=130),
 'Stormsurge':   dict(g=2800, ap=90, pen_f=15, ms=6),
}
TANK_POOL = [k for k in ITEMS if k not in
    ('OverlordBlood','Sterak','BlackCleaver','Zhonyas','Rabadon','Stormsurge','TitanicHydra')]
EXCLUSIVOS = [('immolate', {'Sunfire','HollowRadiance'})]     # A10

def exclusivo_ok(keys):
    for _, grupo in EXCLUSIVOS:
        if len(grupo & set(keys)) > 1: return False
    return True

# ══════════════════════════════ ENEMIGOS PROXY (estándares del lab) ══════════════════════════════
ENEMIES = {
  'squishy': dict(hp=2200, armor=60,  mr=40),
  'fighter': dict(hp=3200, armor=120, mr=80),
  'tank':    dict(hp=4500, armor=220, mr=150),   # estándar lab vsTanque
}

def mit_phys(armor): return 100.0/(100.0+armor)
def mit_magic(mr, pen_p=0.0, pen_f=0.0):
    return 100.0/(100.0+max(0.0, mr*(1-pen_p/100.0) - pen_f))

def feast(S, r_rank):
    hp_per = {1:80, 2:120, 3:160}[r_rank]
    return dict(hp=hp_per*S, size=min(0.06*S, 1.35), rng=min(7.7*S, 75),
                rrange=min(2.5*S, 25))

# ══════════════════════════════ EVALUADOR ══════════════════════════════
def evaluate(boot_key, item_keys, S=15, r_rank=3, fight=10.0, window=5.0,
             tw_mode='total', axiom=True, hearts_proc=1.0, level=15, minute=20.0,
             smite=None, e_rank=4):
    bs = base(level)
    B = BOOTS.get(boot_key) or BOOTS_T2[boot_key]
    its = [ITEMS[k] for k in item_keys] + [B]
    gold = B['g'] + sum(ITEMS[k]['g'] for k in item_keys)
    has = lambda f: any(f in i for i in its)

    # ── stats planos ──
    hp_i   = sum(i.get('hp',0) for i in its)
    armor  = bs['armor'] + sum(i.get('armor',0) for i in its)
    mr     = bs['mr'] + sum(i.get('mr',0) for i in its)
    ap     = sum(i.get('ap',0) for i in its)
    ah     = sum(i.get('ah',0) for i in its) + (10 if level >= 5 else 5)  # Transcendence
    ad     = bs['ad'] + sum(i.get('ad',0) for i in its)
    mana   = bs['mana'] + sum(i.get('mana',0) for i in its)
    ms     = sum(i.get('ms',0) for i in its)
    ten    = sum(i.get('ten',0) for i in its)

    if has('absorb'):                       # FoN Absorb: +70 MR +6 % MS a max stacks (×0.75 A7)
        mr += 70*0.75; ms += 6
    awe_hp = 0.15*mana if has('awe') else 0.0        # Fimbulwinter Awe

    # A5/A13: acumulaciones dependientes del minuto
    gflat = 10*min(40, minute*2)
    oflat = min(100, minute*6)
    opct  = 0.03 if minute >= 13 else 0.0
    hs_growth = 0.9*max(0.0, minute-9.5)*45 if has('hs_proc') else 0.0

    F = feast(S, r_rank)
    bonusHP = hp_i + F['hp'] + gflat + oflat + awe_hp + hs_growth
    if has('hp2ap'): ap += 0.02*bonusHP              # Riftmaker Void Infusion
    maxHP = (bs['hp'] + bonusHP) * (1 + opct)
    bonusHP = maxHP - bs['hp']
    cdr = ah/(100.0+ah)

    size = 1.0 + F['size'] + (0.20 if has('tw') else 0.0)
    atk_range = ATT_RANGE + F['rng']

    pen_p = max([i.get('pen_p',0) for i in its], default=0)
    pen_f = sum(i.get('pen_f',0) for i in its)

    # ── amplificaciones de daño mágico propio ──
    amp = 1.0
    if has('madness'):  amp *= 1.051                 # A11
    if has('voidcorr'): amp *= 1.054
    if has('unmake'):   amp *= 1.12
    bless = 1.0 + (0.30 if has('blessed') else 0.0)  # Warmog's Blessed

    # ── ROTACIÓN (Q4/W4/E4 al nivel del checkpoint; R va aparte: CD 50 s) ──
    n_q = fight/(6.0*(1-cdr)); n_w = fight/(9.0*(1-cdr)); n_e_cast = fight/(4.0*(1-cdr))
    n_spikes = min(3*n_e_cast, bs['AS']*fight)       # limitado por AS
    # E rank: se maxea PRIMERO (nivel ~7 en adelante rank 4) — 3.5 % + 0.6 %/stack (7.2c)
    E_BASE = {1:20, 2:45, 3:70, 4:95}[e_rank]
    e_pct  = (0.023+0.004*(e_rank-1)) + 0.006*S

    def dps_vs(en, aoe_targets=1.0, torments=1.0):
        m_f = mit_magic(en['mr'], pen_p, pen_f); p_f = mit_phys(en['armor'])
        d_mag = (n_q*(245+1.0*ap) + n_w*(230+0.7*ap))*aoe_targets \
              + n_spikes*(95+0.3*ap)*aoe_targets + n_spikes*e_pct*en['hp']*aoe_targets
        if has('immolate'):
            kind = next(i['immolate'][0] for i in its if 'immolate' in i)
            imm = (25 + 0.01*bonusHP) if kind=='hollow' else (20 + 0.015*bonusHP)
            d_mag += imm*fight*aoe_targets
        if has('torment'): d_mag += 0.02*en['hp']*fight*torments        # A12
        if has('anguish'): d_mag += 0.03*maxHP*(fight/4.0)*aoe_targets
        d_mag += (fight/3.0)*(0.033*maxHP)                               # Grasp
        if has('zeke'):    d_mag += 150*(fight/50.0)*aoe_targets
        if has('thorns'):  d_mag += 0.5*(1.2*fight)*(20+0.06*(armor-bs['armor'])+0.01*bonusHP)
        d_mag *= amp*m_f
        d_phys = bs['AS']*ad*fight*p_f
        if has('hs_proc'): d_phys += hearts_proc*(140+0.035*maxHP)*p_f   # A4
        if has('spellblade'):
            n_sb = min(fight/1.5, n_q+n_w+n_e_cast)
            d_phys += n_sb*(1.0*bs['ad']+0.25*(armor-bs['armor']))*p_f*aoe_targets
        if has('titanic'):
            n_t = fight/1.75
            d_phys += n_t*(25+0.03*bonusHP)*p_f
            if aoe_targets > 1: d_phys += n_t*(80+0.10*bonusHP)*p_f*(aoe_targets-1)
        return (d_mag+d_phys)/fight

    aoe_t = min(3.0, 1.5 + 1.5*(size-1.0)/1.55)      # A6
    dps_fighter = dps_vs(ENEMIES['fighter'])
    dps_tank    = dps_vs(ENEMIES['tank'])
    dps_squishy = dps_vs(ENEMIES['squishy'])
    dps_aoe     = dps_vs(ENEMIES['fighter'], aoe_targets=aoe_t, torments=aoe_t)

    # ── EHP estático ──
    block_mult = 1.0/(1-0.10*0.7) if B.get('block') else 1.0             # A8
    ehp_p = maxHP*(1+armor/100.0)*block_mult
    ehp_m = maxHP*(1+mr/100.0)
    if has('anticrit'): ehp_p *= 1+0.5*0.176         # A7
    if has('as_slow'):  ehp_p *= 1+0.5*0.212         # A7

    # ── EHP EN VENTANA (5 s de teamfight, protocolo §1b.6.2) ──
    sh_p = sh_m = 0.0
    if B.get('shield_phys'): sh_p += B['shield_phys'](maxHP)
    if B.get('shield_mag'):  sh_m += B['shield_mag'](maxHP)
    if has('garg'):                                   # A9
        g = (100+0.90*bonusHP)*0.75*bless
        sh_p += g/2; sh_m += g/2                      # escudo mixto
    if has('kaenic'): sh_m += 0.5*(110+0.14*maxHP)*bless                  # A7
    if has('sterak'):
        s = 0.5*0.75*bonusHP*bless; sh_p += s/2; sh_m += s/2
    if has('colossus'):
        c = (120+0.045*mana)*1.8*0.5*bless; sh_p += c/2; sh_m += c/2
    heals5 = (fight and 1.7*(0.013*maxHP)) or 0.0     # Grasp ~1.7 procs/5 s
    if has('anguish'): heals5 += 1.25*(2.5*0.03*maxHP)
    if has('voidcorr'): heals5 += 0.10*(dps_fighter*window*0.5)
    heals5 *= bless
    if has('mantle'):                                 # A7
        heals5 += (250 + (300 + 1.2*(armor-bs['armor']) + 1.2*(mr-bs['mr']) + 0.15*bonusHP))*0.5*bless
    if has('tw'):                                                            # A2
        if tw_mode == 'total': armor_tw, mr_tw = armor*1.3, mr*1.3
        elif tw_mode == 'bonus':
            armor_tw = bs['armor'] + (armor-bs['armor'])*1.3
            mr_tw    = bs['mr'] + (mr-bs['mr'])*1.3
        else: armor_tw, mr_tw = armor, mr
    else: armor_tw, mr_tw = armor, mr
    ew_p = (maxHP+sh_p+heals5)*(1+armor_tw/100.0)*block_mult
    ew_m = (maxHP+sh_m+heals5)*(1+mr_tw/100.0)
    ehp_window = 0.5*ew_p + 0.5*ew_m

    # ── execute de R (daño VERDADERO) ──
    r_base = {1:300, 2:450, 3:600}[r_rank]
    r_exec = (r_base + 0.5*ap + 0.10*bonusHP) * (1.10 if axiom else 1.0) # A3
    r_monster = (1200 + 0.5*ap + 0.10*bonusHP) * (1.10 if axiom else 1.0)
    if smite is None:
        smite = 600 if minute < 8 else (1000 if minute < 14 else 1400)   # A14

    # ── sustain en pelea (hp/s) y fuera de pelea ──
    hps = (0.013*maxHP)/3.0                           # Grasp
    if has('anguish'): hps += (2.5*0.03*maxHP)/4.0
    if has('voidcorr'): hps += 0.10*dps_fighter*0.6
    hps += (bs['regen5']/5.0)*(1.0 + sum(i.get('hpregen',0) for i in its))
    hps *= bless
    ooc_hps = (bs['regen5']/5.0)*(1.0+sum(i.get('hpregen',0) for i in its)) \
            + (0.035*maxHP if has('warmog') else 0.0)

    # ── utilidad (peso bajo): MS, tenacidad, GW, slows, amp de equipo ──
    util = 0.4*ms + 0.3*ten + (15 if has('gw') else 0) + (10 if has('slow') else 0) \
         + (12 if has('unmake') else 0)*0.5 + (10 if has('stasis') else 0)

    return dict(gold=gold, maxHP=maxHP, bonusHP=bonusHP, armor=armor, mr=mr, ap=ap, ah=ah,
                size=size, rng=atk_range, aoe_t=aoe_t,
                dps_fighter=dps_fighter, dps_tank=dps_tank, dps_squishy=dps_squishy,
                dps_aoe=dps_aoe, ehp_p=ehp_p, ehp_m=ehp_m, ehp_window=ehp_window,
                r_exec=r_exec, r_monster=r_monster, hps=hps, ooc_hps=ooc_hps, util=util,
                smite_exec=smite+r_monster, demolish=(85+0.28*maxHP), hs_growth=hs_growth)

# ══════════════════════════════ SCORE PONDERADO (§A.5 Tanque) ══════════════════════════════
PESOS = dict(ehp_p=0.15, ehp_m=0.15, ehp_window=0.20, r_exec=0.15,
             dps_fighter=0.10, dps_tank=0.10, dps_aoe=0.05, hps=0.05, util=0.05)
PESOS_AD  = dict(PESOS, ehp_p=0.22, ehp_m=0.08, ehp_window=0.22)   # vs comp AD
PESOS_AP  = dict(PESOS, ehp_p=0.08, ehp_m=0.22, ehp_window=0.22)   # vs comp AP
PESOS_TK  = dict(PESOS, dps_tank=0.20, dps_fighter=0.07, ehp_window=0.15, util=0.03)  # vs doble tanque
PESOS_DPS = dict(ehp_p=0.10, ehp_m=0.10, ehp_window=0.10, r_exec=0.15,
                 dps_fighter=0.20, dps_tank=0.20, dps_aoe=0.10, hps=0.00, util=0.05)  # sesgo carry-top

def composite(res, mx, pesos=PESOS):
    return sum(pesos[k]*(res[k]/mx[k]) for k in pesos if mx.get(k))

# ══════════════════════════════ BÚSQUEDA EXHAUSTIVA (Ley 0: 1 botas + 5 ítems) ══════════════════════════════
def optimize(pool, boots, oro=17250, S=15, r_rank=3, pesos=PESOS, top=8, n_items=5, **kw):
    cands = []
    for bk in boots:
        bg = BOOTS.get(bk, BOOTS_T2.get(bk))['g']
        for combo in itertools.combinations(pool, n_items):
            g = bg + sum(ITEMS[k]['g'] for k in combo)
            if g > oro or not exclusivo_ok(combo): continue
            cands.append((bk, combo))
    res = [(bk, cb, evaluate(bk, list(cb), S=S, r_rank=r_rank, **kw)) for bk, cb in cands]
    mx = {k: max(r[2][k] for r in res) for k in PESOS}
    scored = sorted(((composite(r[2], mx, pesos),)+r for r in res), reverse=True)
    return scored[:top], mx, len(res)

def fmt(score, bk, cb, r):
    items = ' + '.join([bk]+list(cb))
    return (f"score {score:.3f} | {r['gold']:>6.0f}g | HP {r['maxHP']:.0f} | arm {r['armor']:.0f} | "
            f"MR {r['mr']:.0f} | AP {r['ap']:.0f} | EHPp {r['ehp_p']:.0f} | EHPm {r['ehp_m']:.0f} | "
            f"VENT {r['ehp_window']:.0f} | R {r['r_exec']:.0f} | DPSf {r['dps_fighter']:.0f} | "
            f"DPSt {r['dps_tank']:.0f} | AoE {r['dps_aoe']:.0f} | hps {r['hps']:.0f}\n        {items}")


# ══════════════ NOMBRES OFICIALES WR 7.3 (items_7.3.csv) ══════════════
# Mapa key-interno → nombre oficial para reportes/lint (v1.17). Cualquier
# ítem nuevo del motor DEBE agregarse acá y existir en el CSV (test lo exige).
NOMBRES_OFICIALES = {
    "Heartsteel": "Heartsteel", "HollowRadiance": "Hollow Radiance", "Sunfire": "Sunfire Aegis",
    "Liandry": "Liandry's Torment", "Riftmaker": "Riftmaker", "RodOfAges": "Rod of Ages",
    "Rylai": "Rylai's Crystal Scepter", "Morello": "Morellonomicon", "Cryptbloom": "Cryptbloom",
    "Abyssal": "Abyssal Mask", "Zeke": "Zeke's Convergence", "FrozenHeart": "Frozen Heart",
    "Thornmail": "Thornmail", "Randuin": "Randuin's Omen", "DeadMans": "Dead Man's Plate",
    "ForceOfNature": "Force of Nature", "KaicRookern": "Kaenic Rookern", "Warmog": "Warmog's Armor",
    "Gargoyle": "Gargoyle Stoneplate", "UnendingDespair": "Unending Despair", "Iceborn": "Iceborn Gauntlet",
    "Mantle": "Mantle of the Twelfth Hour", "Twinguard": "Amaranth's Twinguard", "TitanicHydra": "Titanic Hydra",
    "Fimbulwinter": "Fimbulwinter", "OverlordBlood": "Overlord's Bloodmail", "Sterak": "Sterak's Gage",
    "BlackCleaver": "Black Cleaver", "Zhonyas": "Zhonya's Hourglass", "Rabadon": "Rabadon's Deathcap",
    "Stormsurge": "Stormsurge", "ArmoredAdvance": "Armored Advance", "Chainlaced": "Chainlaced Crushers",
    "ImmortalTreads": "Immortal Treads", "Plated": "Plated Steelcaps", "Mercurys": "Mercury's Treads",
    "Gluttonous": "Gluttonous Greaves",
}

def nombre_oficial(key):
    return NOMBRES_OFICIALES.get(key, key)

if __name__ == '__main__':
    OUT = []
    def P(*a):
        s = ' '.join(str(x) for x in a); OUT.append(s); print(s)

    P('='*112)
    P("WR-LAB · MOTOR ROTACIÓN-TANQUE (batch4) — CHO'GATH nivel 15 · Feast 15 stacks · R3 · oro ≤ 17 250")
    P('='*112)

    # ── 1. OPTIMIZACIÓN DEFAULT ──
    top, mx, n = optimize(TANK_POOL, ['ArmoredAdvance','Chainlaced','ImmortalTreads'], top=10)
    P(f"\n[1] ÓPTIMAS DEFAULT — pesos §A.5 tanque (EHP .15/.15 + ventana .20 + R .15 + DPS .25 + sustain .05 + util .05) · {n} builds evaluadas:")
    for i,(sc,bk,cb,r) in enumerate(top,1):
        P(f"  #{i:>2} " + fmt(sc,bk,cb,r))

    # ── 2. BUILDS DE REFERENCIA ──
    PUB = {
      'LAB-JUNGLA (pub. 28/09)': ('ArmoredAdvance', ['Heartsteel','HollowRadiance','Liandry','ForceOfNature','Warmog']),
      'LAB-BARON (pub. 28/09)':  ('ArmoredAdvance', ['Heartsteel','RodOfAges','Twinguard','Gargoyle','Liandry']),
      'COMUNIDAD wr-meta':       ('Chainlaced',     ['Heartsteel','HollowRadiance','Liandry','ForceOfNature','Warmog']),
      'TANQUE PURO (0 AP)':      ('ArmoredAdvance', ['Heartsteel','Twinguard','Gargoyle','Warmog','Randuin']),
      'AP PURO (glass cannon)':  ('Chainlaced',     ['Liandry','Riftmaker','Cryptbloom','Rabadon','Rylai']),
      'TITANIC HYDRA (control)': ('ArmoredAdvance', ['Heartsteel','TitanicHydra','Twinguard','Gargoyle','Liandry']),
    }
    P("\n[2] BUILDS DE REFERENCIA (mismas métricas, minuto 20, S=15):")
    refs = {}
    for name,(bk,cb) in PUB.items():
        r = evaluate(bk, cb); refs[name] = (bk,cb,r)
        P(f"  {name:<26} " + fmt(composite(r,{k:max(x[2][k] for x in refs.values()) if False else 1 for k in PESOS}),bk,cb,r).split('|',1)[1])
    best_bk, best_cb = top[0][1], top[0][2]
    P("\n  CONTROLES Ley 4 (sustituir el 5.º ítem de la óptima):")
    for ctrl in ('OverlordBlood','Sterak','BlackCleaver'):
        cb2 = list(best_cb[:4]) + [ctrl]
        r = evaluate(best_bk, cb2)
        P(f"  {ctrl:<26} " + fmt(0,best_bk,cb2,r).split('|',1)[1])
        refs['CTRL-'+ctrl] = (best_bk, tuple(cb2), r)

    mx_all = {k: max(x[2][k] for x in refs.values()) for k in PESOS}
    for k in PESOS: mx_all[k] = max(mx_all[k], top[0][3][k])
    P("\n  SCORE COMPOSITE (normalizado al máx de la corrida; la óptima del motor = referencia 1.00 relativa):")
    rows = [(name, composite(r, mx_all)) for name,(bk,cb,r) in refs.items() if not name.startswith('CTRL')]
    rows.append(('ÓPTIMA LAB (motor batch4)', composite(top[0][3], mx_all)))
    ref_opt = composite(top[0][3], mx_all)
    for name, sc in sorted(rows, key=lambda x:-x[1]):
        P(f"    {name:<28} {sc:.3f}   ({(sc/ref_opt-1)*100:+.1f} % vs óptima)")
    for name,(bk,cb,r) in refs.items():
        if name.startswith('CTRL'):
            sc = composite(r, mx_all)
            P(f"    {name:<28} {sc:.3f}   ({(sc/ref_opt-1)*100:+.1f} % vs óptima)")

    # ── 3. VARIANTES SITUACIONALES ──
    for etiqueta, pesos in [('vs COMP AD (75 % físico)', PESOS_AD),
                            ('vs COMP AP (75 % mágico)', PESOS_AP),
                            ('vs DOBLE TANQUE (dps_tank ×2)', PESOS_TK),
                            ('SESGO DAÑO (carry-top, DPS 50 %)', PESOS_DPS)]:
        t2, _, _ = optimize(TANK_POOL, ['ArmoredAdvance','Chainlaced','ImmortalTreads'], pesos=pesos, top=3)
        P(f"\n[3] ÓPTIMA {etiqueta}:")
        for i,(sc,bk,cb,r) in enumerate(t2,1):
            P(f"  #{i} " + fmt(sc,bk,cb,r))

    # ── 4. SENSIBILIDAD DE STACKS ──
    P("\n[4] SENSIBILIDAD — stacks de Feast (búsqueda completa por punto):")
    for S, rr, mn in [(6,2,13.0),(15,3,20.0),(22,3,26.0)]:
        t3, _, _ = optimize(TANK_POOL, ['ArmoredAdvance','Chainlaced','ImmortalTreads'], S=S, r_rank=rr, minute=mn, top=2)
        for i,(sc,bk,cb,r) in enumerate(t3,1):
            P(f"  S={S:>2} R{rr} min{mn:.0f} #{i}: " + fmt(sc,bk,cb,r))

    # ── 5/6. SENSIBILIDADES D2 y D4 ──
    for modo, etiqueta in [('bonus', "D2a — Endurance = +30 % solo a resistencias BONUS"),
                           ('none',  "D2b — Endurance sin multiplicador (peor caso)")]:
        t4, _, _ = optimize(TANK_POOL, ['ArmoredAdvance','Chainlaced','ImmortalTreads'], tw_mode=modo, top=2)
        P(f"\n[5] SENSIBILIDAD {etiqueta}:")
        for i,(sc,bk,cb,r) in enumerate(t4,1):
            P(f"  #{i} " + fmt(sc,bk,cb,r))
    t5, _, _ = optimize(TANK_POOL, ['ArmoredAdvance','Chainlaced','ImmortalTreads'], axiom=False, top=1)
    P("\n[6] SENSIBILIDAD D4 (Axiom Arcanist NO amplifica el true damage de R):")
    for i,(sc,bk,cb,r) in enumerate(t5,1):
        P(f"  #{i} " + fmt(sc,bk,cb,r))

    # ── 7. CHECKPOINTS DE RUTA (niveles/oros de las rutas publicadas) ──
    P("\n[7] CHECKPOINTS DE RUTA (oro de las Tablas B publicadas; nivel real; fight 8 s):")
    cps = [
      ('CP1 min 9:30 · lvl 9 · R2 · S=4 · ≤5 300 g · botas T2 + 1 ítem',
       dict(oro=5300, S=4, r_rank=2, level=9, minute=9.5, fight=8.0), ['Plated','Mercurys','Gluttonous'], 1),
      ('CP2 min 12:00 · lvl 12 · R2 · S=6 · ≤8 000 g · botas T2 + 2 ítems',
       dict(oro=8000, S=6, r_rank=2, level=12, minute=12.0, fight=8.0), ['Plated','Mercurys','Gluttonous'], 2),
      ('CP3 min 15:00 · lvl 14 · R3 · S=9 · ≤12 200 g · botas T3 + 3 ítems',
       dict(oro=12200, S=9, r_rank=3, level=14, minute=15.0, fight=8.0), ['ArmoredAdvance','Chainlaced','ImmortalTreads'], 3),
      ('CP4 min 18:00 · lvl 15 · R3 · S=12 · ≤15 100 g · botas T3 + 4 ítems',
       dict(oro=15100, S=12, r_rank=3, level=15, minute=18.0, fight=8.0), ['ArmoredAdvance','Chainlaced','ImmortalTreads'], 4),
    ]
    for etiqueta, kw2, boots, n_items in cps:
        cands=[]
        for bk in boots:
            bg = BOOTS.get(bk, BOOTS_T2.get(bk))['g']
            for combo in itertools.combinations(TANK_POOL, n_items):
                g = bg + sum(ITEMS[k]['g'] for k in combo)
                if g > kw2['oro'] or not exclusivo_ok(combo): continue
                cands.append((bk,combo))
        ev = {k:v for k,v in kw2.items() if k!='oro'}
        res=[(bk,cb,evaluate(bk,list(cb),**ev)) for bk,cb in cands]
        mx2={k:max(x[2][k] for x in res) for k in PESOS}
        res_s=sorted(((composite(x[2],mx2),)+x for x in res),reverse=True)[:4]
        P(f"  {etiqueta}:")
        for i,(sc2,bk,cb,r) in enumerate(res_s,1):
            P(f"    #{i} score {sc2:.3f} | {r['gold']:>5.0f}g | {' + '.join([bk]+list(cb))} | HP {r['maxHP']:.0f} | R {r['r_exec']:.0f} | VENT {r['ehp_window']:.0f} | DPSf {r['dps_fighter']:.0f} | hps {r['hps']:.0f}")

    # ── 8. CURVA DE STACKS POR MINUTO (protocolo §1b.6.3) ──
    P("\n[8] CURVA DE STACKS + EXECUTE DE R (ruta recomendada; supuestos A5/A13/A14):")
    LVL = {6:6, 8:7, 9.5:9, 12:10, 14:12, 16:12, 18:13, 20:14, 22:15, 24:15}
    # Ruta recomendada (ítems COMPLETADOS por minuto):
    ROUTE_TOP = [
      (6.0,  'Plated T2', 'Plated', [], 0, 6, 1),
      (9.5,  'Heartsteel', 'Plated', ['Heartsteel'], 4, 9, 2),
      (12.0, '+T3', 'ArmoredAdvance', ['Heartsteel'], 6, 10, 2),
      (14.5, '+Unending', 'ArmoredAdvance', ['Heartsteel','UnendingDespair'], 8, 12, 3),
      (17.0, '+Twinguard', 'ArmoredAdvance', ['Heartsteel','UnendingDespair','Twinguard'], 10, 13, 3),
      (19.5, '+Gargoyle', 'ArmoredAdvance', ['Heartsteel','UnendingDespair','Twinguard','Gargoyle'], 12, 14, 3),
      (22.0, '+Warmog (default)', 'ArmoredAdvance', ['Heartsteel','UnendingDespair','Twinguard','Gargoyle','Warmog'], 14, 15, 3),
    ]
    # Stacks (min, S_top, S_jungla): TOP = minions cap6 ~min13 + épicos/campeones; JUNGLA = cap6 ~min10
    STACKS = {6.0:(0,0), 9.5:(2,4), 12.0:(4,6), 14.5:(6,8), 17.0:(7,10), 19.5:(8,12), 22.0:(10,14)}
    P(f"    {'min':>4} {'ítems':<34} {'lvl':>3} {'S-top':>5} {'R':>4} {'HP':>5} {'R champ':>7} {'R monstruo':>10} {'Smite+R':>8}")
    for (mn, etiqueta, bk, cb, S_t, lvl, rr) in ROUTE_TOP:
        S_j = STACKS[mn][1]; S = STACKS[mn][0]
        er = 3 if mn <= 6 else 4        # E rank 3 a min 6 (lvl 6), rank 4 desde ~min 7
        r = evaluate(bk, cb, S=S, r_rank=rr, level=lvl, minute=mn, fight=6.0, e_rank=er)
        rj = evaluate(bk, cb, S=S_j, r_rank=rr, level=lvl, minute=mn, fight=6.0, e_rank=er)
        P(f"    {mn:>4.0f} {etiqueta:<34} {lvl:>3} {S:>2}/{S_j:<2} R{rr}  {r['maxHP']:>5.0f} {r['r_exec']:>7.0f} {r['r_monster']:>10.0f} {r['smite_exec']:>8.0f}")
    P("    (S-top/S-jungla: stacks TOP y JUNGLA al minuto; R = execute vs campeón con Axiom; Smite+R = umbral de robo de épico)")

    # ── 9. FICHA DE LA ÓPTIMA (números para el documento) ──
    sc,bk,cb,r = top[0]
    P("\n[9] FICHA DE LA ÓPTIMA DEFAULT (S=15, min 20, R3):")
    P(json.dumps({k:(round(v,1) if isinstance(v,float) else v) for k,v in r.items()}, indent=1, ensure_ascii=False))
    P(f"\n  Smite(1400)+R monstruo = {r['smite_exec']:.0f} verdadero — umbral de robo de Baron")
    P(f"  Demolish (3.er golpe a torreta) = {r['demolish']:.0f} físico + cristal ~770 verdadero (11 % de 7 000)")
    P(f"  Rango de ataque = {r['rng']:.0f} | Tamaño +{(r['size']-1)*100:.0f} % | E golpea ~{r['aoe_t']:.1f} objetivos")

    with open('model/chogath_resultados.txt','w',encoding='utf-8') as f:
        f.write('\n'.join(OUT)+'\n')
    print('\n[salida guardada en model/chogath_resultados.txt]')
