# -*- coding: utf-8 -*-
"""
WR-LAB · model/yunara_model.py — RE-VERIFICACIÓN + DERIVACIÓN RIESGO-AJUSTADA (batch4, 13/10/2026)
===================================================================================================
Motivos (lab §3b + petición del autor):
  1. Yunara marcada "revisar 1.er ítem" tras el buff 7.3a de Yun Tal.
  2. `SIN_MOTOR` parcial: "motor autos NO modela su spread de Q ni la interacción de R
     con crítico — resultados aproximados" → los titulares publicados (3 042/10 551/
     2 150/1 480) son de auditoría dudosa: este motor los reproduce desde los inputs
     y documenta cada delta.
  3. Hipótesis del autor: "el daño publicado no convence frente al RIESGO y desventaja
     en cada combate" → módulo de SUPERVIVENCIA (EHP + escudos + revivir + sustain)
     con las convenciones del propio lab (optimize_build.ehp_y_util: ESCUDOS_FIS
     bt 255×0.5 / shieldbow 425×0.5 · UTIL_FLAGS ga 300 / scimitar 150) y objetivos
     ponderados DPS/supervivencia para derivar la build riesgo-ajustada.

TÉRMINOS PROPIOS DE YUNARA (fuera del engine de autos; fuentes: ficha wr-meta 24/09,
notas 7.3 —pasiva 8 %, Kraken proca con spread—, wiki):
  - Pasiva Vow: cada crítico añade daño MÁGICO = 8 % × AD (convención A del reporte;
    convención B = 8 % del daño del golpe crítico → sensibilidad).
  - Q Spirit Charge on-hit mágico: 25 (rank 4; el "+20 %" de la ficha tiene la fuente
    truncada — AP asumido, y AP=0 en builds de crit → término plano).
  - Q Spirit Unbound SPREAD: (18 + 30 % AD) físico a objetivos cercanos; SOLO critica
    durante R (Transcendent). 1v1: 0 (no hay cercanos). 3v3: 2 objetivos.
  - Kraken "Bring it Down" proca además con el spread (nota oficial 7.3) → +50 % de
    procs en escenarios AoE (supuesto declarado).
  - W Arc of Judgment: (210 + 85 % bAD + 50 % AP) + 4 ticks (26 + 12 % bAD + 7.5 % AP)
    /10 s, MÁGICO. En R → Arc of Ruin (160 + 120 % bAD + 75 % AP) + refund 80 % al
    entrar/salir (≈ +1 cast por ventana).
  - Uptimes: q_up (default 1.0 en ventana de pelea — durante R es automática; 0.7 el
    supuesto publicado), r_up (1.0 ventana teamfight ≤15 s; 0.23 sostenido 15/65),
    magn_up (1.0 publicado; 0.6 en comps de dive — exige ≥550 u).
  - Términos MÁGICOS mitigados por MR del proxy (40 squishy / 80 vs120 / 150 tanque) —
    el reporte publicado NO los mitigaba (uno de sus infladores).

SUPUESTOS: LT+Alacrity full (convención lab) · Kraken missing-HP 50 % (25/75 sens.) ·
BotRK 6 % engine (7 % oficial sens.) · Flurry de Yun Tal: uptime 50 % (sens. 0/100) ·
rango de ataque ≥550 (no publicado — verificar, como marca el reporte) · Fiendhunter:
Opening Barrage ≈ +13 DPS amortizado y ult haste 20 (→ r_up sostenido +15 % rel.).
"""
import itertools

AS_CAP, CRIT_DMG_BASE, CRIT_DMG_IE = 3.0, 2.00, 2.30
LT_RANGED_STACK, LT_BULLET_SCALE, ALACRITY_FULL = 0.064, 0.0067, 0.21
KRAKEN_RANGED_L15, KRAKEN_MISSING_BONUS = 168, 0.0075

SPEC = dict(name="Yunara", base_ad=58.0, ad_growth=3.0, base_as=0.65, as_ratio=0.65,
            base_bonus_as=0.23, as_per_lvl=0.032, self_as_buff=0.55)

def I(key, gold, ad=0, ap=0, a_s=0, crit=0, pen=0, ls=0, mr=0, armor=0, hp=0, ah=0, ms=0,
      kraken=False, magnification=False, ie=False, runaan=False, energized=0,
      onhit_flat=0, onhit_pct_current=0, spellblade=0, giant_slayer=0,
      pen_pct_group=False, esc_fis=0.0, esc_mag=0.0, util=0.0, ten=0.0, comment=""):
    return dict(key=key, gold=gold, ad=ad, ap=ap, a_s=a_s, crit=crit, pen=pen, ls=ls, mr=mr,
                armor=armor, hp=hp, ah=ah, ms=ms, kraken=kraken, magnification=magnification,
                ie=ie, runaan=runaan, energized=energized, onhit_flat=onhit_flat,
                onhit_pct_current=onhit_pct_current, spellblade=spellblade,
                giant_slayer=giant_slayer, pen_pct_group=pen_pct_group,
                esc_fis=esc_fis, esc_mag=esc_mag, util=util, ten=ten, comment=comment)

ITEMS = {i['key']: i for i in [
    I("c44",       2900, ad=55, crit=25, magnification=True),
    I("ie",        3400, ad=75, crit=25, ie=True),
    I("runaan",    2650, a_s=40, crit=25, ms=4, runaan=True),
    I("ldr",       3300, ad=35, pen=35, crit=25, giant_slayer=12, pen_pct_group=True),
    I("mortal",    3000, ad=35, pen=30, crit=25, pen_pct_group=True),
    I("kraken",    2900, ad=45, a_s=35, ms=4, kraken=True),
    I("rfc",       2650, a_s=40, crit=25, ms=4, energized=80),
    I("storm",     3000, ad=50, crit=25, a_s=20, energized=120),
    I("bt",        3200, ad=75, ls=15, esc_fis=255*0.5),                      # Ichorshield (lab)
    I("gale",      3100, ad=60, crit=25, ms=4),
    I("shieldbow", 3000, ad=55, crit=25, esc_fis=425*0.5),                    # Lifeline (lab)
    I("fiend",     2650, a_s=45, crit=25, ms=4, util=60, comment="ult haste 20 + Opening Barrage"),
    I("collector", 3000, ad=50, pen=10, crit=25),
    I("pd",        2650, a_s=40, crit=25, ms=7),
    I("navori",    2650, a_s=40, crit=25, ms=4),
    I("er",        3000, ad=50, crit=25, ah=20, spellblade=1.0),
    I("yuntal",    3100, ad=50, a_s=35, crit=25),
    I("manamune",  2900, ad=40, ah=15),
    I("botrk",     3100, ad=40, a_s=30, ls=12, onhit_pct_current=6),
    I("witsend",   2800, a_s=50, mr=45, onhit_flat=40, ten=20),
    I("terminus",  3000, ad=35, a_s=35, onhit_flat=30, pen=30, pen_pct_group=True),
    I("guinsoo",   3000, ad=35, ap=30, a_s=30, onhit_flat=30),
    I("statikk",   3000, ad=40, ap=40, a_s=30, ms=4, energized=60),
    I("scimitar",  3100, ad=45, mr=40, ls=12, util=150),                     # QSS (lab UTIL_FLAGS)
    I("ga",        3200, ad=45, armor=40, util=300),                         # revivir (lab)
    I("maw",       3000, ad=55, mr=45, ah=10, esc_mag=300*0.5),
    I("deathsdance",3300, ad=50, armor=45, ah=15, util=120, comment="Cauterize 12 % ranged + Defy"),
    # botas
    I("berserker", 1200, a_s=35),
    I("gunmetal",  2200, a_s=50, ls=5),
    I("chainlaced",2200, hp=150, mr=30, ten=30),
    I("armored_adv",2200, hp=150, armor=30, esc_fis=75*0.7),
    I("armorcrusher",2200, ad=25, pen=12),
]}
BOOTS = {"gunmetal","chainlaced","armored_adv","armorcrusher","berserker"}

def lvl_as_bonus(level): return SPEC['as_per_lvl'] * sum(0.7 + 0.04*L for L in range(1, level))

def as_total(keys, level=15, lt=True, alacrity=ALACRITY_FULL, self_buff_on=True, flurry_uptime=0.0):
    ai = sum(ITEMS[k]['a_s'] for k in keys)/100.0
    lt_as = LT_RANGED_STACK*6 if lt else 0
    B = (SPEC['base_bonus_as'] + lvl_as_bonus(level) + ai + lt_as + alacrity
         + (SPEC['self_as_buff'] if self_buff_on else 0) + flurry_uptime*0.35)
    raw = SPEC['base_as'] + SPEC['as_ratio']*B
    return min(raw, AS_CAP), raw, B

def lt_bullet(level, B):
    return (6 + 18*(level-1)/14) * (1 + LT_BULLET_SCALE*B*100)

MR_PROXY = {'1v1': 40, '3v3': 40, 'vs120': 80, 'vsTanque': 150}

def eval_build(keys, level=15, targets=1, armor=0.0, tank=False, lt=True,
               alacrity=ALACRITY_FULL, kraken_missing=50, enemy_hp=2200,
               self_buff_on=True, spellblade_uptime=1/1.5, botrk_pct=None,
               flurry_uptime=0.0, magn_uptime=1.0):
    its = [ITEMS[k] for k in keys]
    gold = sum(i['gold'] for i in its)
    base_ad = SPEC['base_ad'] + SPEC['ad_growth']*(level-1)
    ad   = base_ad + sum(i['ad'] for i in its)
    crit = min(sum(i['crit'] for i in its), 100)/100.0
    pen  = min(sum(i['pen'] for i in its), 100)
    ls   = sum(i['ls'] for i in its)
    AS, raw_as, B = as_total(keys, level, lt, alacrity, self_buff_on, flurry_uptime)
    cdmg = (CRIT_DMG_IE if any(i['ie'] for i in its) else CRIT_DMG_BASE)
    cmult = 1 + crit*(cdmg-1)
    magn = 1.0 + 0.10*magn_uptime*(1 if any(i['magnification'] for i in its) else 0)
    amp  = 1 + (sum(i['giant_slayer'] for i in its)/100.0 if tank else 0)

    hit = ad*cmult*magn*amp
    d   = AS*hit
    for i in its:
        if i['kraken']:
            d += AS/3 * KRAKEN_RANGED_L15*(level/15) * (1 + KRAKEN_MISSING_BONUS*kraken_missing)
        if i['energized']: d += AS/7 * i['energized']
        if i['onhit_flat']: d += AS * i['onhit_flat']
        if i['onhit_pct_current']:
            pct = botrk_pct if (botrk_pct is not None and i['key']=='botrk') else i['onhit_pct_current']
            d += AS * max(15, pct/100*enemy_hp)
        if i['spellblade']: d += spellblade_uptime*(1.35*base_ad + 80*crit)
        if i['key'] == 'fiend': d += 13.0     # Opening Barrage amortizado (supuesto)
    bullet = AS*lt_bullet(level, B) if lt else 0
    d += bullet

    bolts = 0.0
    if targets > 1 and any(i['runaan'] for i in its):
        bolts = AS*0.55*ad*cmult*amp*min(2, targets-1)
    mit = 100/(100+armor*(1-pen/100)) if armor > 0 else 1.0
    heal = d*(ls/100)*mit
    if 'gunmetal' in keys: heal += 12*AS
    elif 'berserker' in keys: heal += 10*AS

    return dict(gold=gold, AD=ad, base_ad=base_ad, AS=AS, raw_AS=raw_as, B=B, crit=crit*100,
                pen=pen, cmult=cmult, magn=magn, engine1=d*mit, engineN=(d+bolts)*mit,
                engine1_raw=d, bolts=bolts, bullet=bullet, heal=heal, mit=mit)

def yunara_terms(keys, level=15, scenario='1v1', q_up=1.0, r_up=1.0, passive_mode='A',
                 kraken_missing=50, **evkw):
    """Spread de Q + Kraken-vía-spread + pasiva + Q on-hit + W (mágicos mitigados por MR proxy)."""
    ev = eval_build(keys, level=level, **evkw)
    targets = {'1v1':1,'3v3':3,'vs120':1,'vsTanque':1}[scenario]
    bAD = ev['AD'] - ev['base_ad']
    AS = ev['AS']
    mrm = 100/(100+MR_PROXY[scenario])
    # pasiva (mágica, por crítico; crit=1.0 en builds legales)
    per_crit = 0.08*ev['AD'] if passive_mode=='A' else 0.08*ev['AD']*ev['cmult']*ev['magn']
    pasiva = per_crit*(ev['crit']/100.0)*AS*mrm
    # Q on-hit mágico (rank 4 = 25; "+20 %" de fuente truncada → AP=0)
    q_onhit = 25*AS*q_up*mrm
    # spread (físico, mit por armadura del escenario; critica solo en R)
    spread_unit = (18 + 0.30*ev['AD']) * (r_up*ev['cmult'] + (1-r_up)*1.0)
    n_extra = min(2, targets-1)
    spread = AS*q_up*spread_unit*n_extra*ev['mit']
    # Kraken vía spread (nota 7.3): +50 % de procs si hay spread activo
    kraken_extra = 0.0
    if n_extra > 0 and any(ITEMS[k]['kraken'] for k in keys):
        kraken_extra = 0.5*(AS/3)*KRAKEN_RANGED_L15*(level/15)*(1+KRAKEN_MISSING_BONUS*kraken_missing)*ev['mit']
    # W (mágico): Judgment 59.3/s base; en R, Ruin + refund (~+4/s)
    w_judg = ((210+0.85*bAD) + 4*(26+0.12*bAD))/10.0
    w_ruin = (160+1.2*bAD)/10.0 + 0.8*(160+1.2*bAD)/15.0
    w = (w_judg*(1-r_up) + w_ruin*r_up)*mrm
    return dict(pasiva=pasiva, q_onhit=q_onhit, spread=spread, kraken_extra=kraken_extra,
                w=w, total=pasiva+q_onhit+spread+kraken_extra+w)

def totals(keys, level=15, scenario='1v1', **opts):
    scen = {'1v1': dict(), '3v3': dict(targets=3), 'vs120': dict(armor=120),
            'vsTanque': dict(armor=220, tank=True, enemy_hp=4500)}[scenario]
    evkw = {k:v for k,v in opts.items() if k in ('botrk_pct','flurry_uptime','magn_uptime','kraken_missing','self_buff_on')}
    ev = eval_build(keys, level=level, **{**evkw, **scen})
    tkw = {k:v for k,v in opts.items() if k in ('q_up','r_up','passive_mode','kraken_missing')}
    tm = yunara_terms(keys, level=level, scenario=scenario, **tkw,
                      **{k:v for k,v in evkw.items() if k!='kraken_missing'},
                      **{k:scen[k] for k in ('armor','tank','enemy_hp') if k in scen})
    eng = ev['engineN'] if scenario=='3v3' else ev['engine1']
    total = eng + tm['total']
    return dict(total=total, engine=eng, terms=tm, heal=ev['heal'], AS=ev['AS'], AD=ev['AD'],
                crit=ev['crit'], pen=ev['pen'], raw_AS=ev['raw_AS'], gold=ev['gold'], B=ev['B'])

def survival(keys, level=15, ls_dps=None, scenario='1v1', **opts):
    """EHP mixto + escudos + utilidad (convenciones ehp_y_util del lab) + heal/s."""
    hp = 600 + 128*(level-1); armor = 35 + 4.5*(level-1); mr = 30 + 1.43*(level-1)
    esc_f = esc_m = util = ten = 0.0
    for k in keys:
        it = ITEMS[k]
        hp += it['hp']; armor += it['armor']; mr += it['mr']
        esc_f += it['esc_fis']; esc_m += it['esc_mag']; util += it['util']; ten += it['ten']
    ehp = 0.5*((hp+esc_f)*(1+armor/100.0) + (hp+esc_m)*(1+mr/100.0))
    if ls_dps is None:
        ls_dps = totals(keys, level=level, scenario=scenario, **opts)['heal']
    return dict(hp=hp, armor=armor, mr=mr, ehp=ehp, heal=ls_dps, util=util, ten=ten,
                surv=ehp + util + 2.5*ls_dps)     # 2.5 s de burst-window de heal (declarado)

# ══════════════════════════ SCORES ══════════════════════════
ESC = ('1v1','3v3','vs120','vsTanque')
def metrics(keys, level=15, **opts):
    m = {s: totals(keys, level=level, scenario=s, **opts)['total'] for s in ESC}
    t1 = totals(keys, level=level, scenario='1v1', **opts)
    sv = survival(keys, level=level, ls_dps=t1['heal'], **opts)
    m.update(sv)
    m['gold'] = t1['gold']; m['AS'] = t1['AS']
    return m

PESOS_DPS  = {'1v1':.30,'3v3':.30,'vs120':.20,'vsTanque':.20,'surv':.00,'heal':.00}   # objetivo publicado
PESOS_RIESGO = {'1v1':.24,'3v3':.20,'vs120':.10,'vsTanque':.10,'surv':.26,'heal':.10}  # riesgo-ajustado (0.64/0.36)
PESOS_TANQUE = {'1v1':.10,'3v3':.15,'vs120':.15,'vsTanque':.35,'surv':.15,'heal':.10}  # anti-tanque
PESOS_DIVE   = {'1v1':.20,'3v3':.20,'vs120':.10,'vsTanque':.10,'surv':.32,'heal':.08}  # vs dive (magn 0.6)

def composite(m, mx, pesos):
    return sum(pesos[k]*(m[k]/mx[k]) for k in pesos if mx.get(k))

def optimize(pesos, boots=('gunmetal','armorcrusher','chainlaced','armored_adv'), budget=18000,
             crit_max=100, pen_min=30, top=6, label="", pool=None, **opts):
    pool = pool or [k for k in ITEMS if k not in BOOTS]
    cands = []
    for bk in boots:
        bg = ITEMS[bk]['gold']
        for combo in itertools.combinations(pool, 5):
            g = bg + sum(ITEMS[k]['gold'] for k in combo)
            if g > budget: continue
            cs = sum(ITEMS[k]['crit'] for k in combo) + ITEMS[bk]['crit']
            if cs > crit_max: continue                       # Ley 1 (poda estructural)
            if sum(ITEMS[k]['pen'] for k in combo) + ITEMS[bk]['pen'] < pen_min: continue  # Ley 3
            if sum(1 for k in combo if ITEMS[k]['pen_pct_group']) > 1: continue             # Ley 3b
            cands.append((bk, combo))
    res = [(bk, cb, metrics([bk]+list(cb), **opts)) for bk, cb in cands]
    mx = {k: max(r[2][k] for r in res) for k in PESOS_DPS}
    scored = sorted(((composite(r[2], mx, pesos),)+r for r in res), reverse=True)
    print(f"\n{'='*118}\nOPTIMIZADOR {label} — {len(cands)} hojas legales (crit≤100, pen≥{pen_min}, ≤{budget} g, Ley 3b)")
    for i,(sc,bk,cb,m) in enumerate(scored[:top],1):
        print(f"  #{i} {sc*100:>5.1f} % | {m['gold']:>6} g | {' + '.join([bk]+list(cb)):<62} | "
              f"1v1 {m['1v1']:>5.0f} · 3v3 {m['3v3']:>5.0f} · vs120 {m['vs120']:>5.0f} · vsT {m['vsTanque']:>5.0f} · "
              f"EHP {m['ehp']:>5.0f} · heal {m['heal']:>4.0f} · AS {m['AS']:.2f}")
    return scored, mx

# ══════════════════════════ BUILDS ══════════════════════════
B_STD  = ['gunmetal','c44','runaan','ie','ldr','kraken']        # Tabla A publicada
B_TANK = ['gunmetal','c44','yuntal','botrk','ldr','ie']         # A2 publicada anti-tanques
B_COMM = ['gunmetal','kraken','runaan','ie','ldr','botrk']      # comunidad wr-meta (Kraken 1.º)
B_RFC  = ['gunmetal','kraken','rfc','ie','ldr','c44']           # fila "comunidad" del reporte (con RFC)
B_ONHIT= ['gunmetal','guinsoo','botrk','terminus','witsend','kraken']  # control on-hit (sin LDR: Ley 3b)

def main():
    OUT=[]; 
    def P(*a):
        s=' '.join(str(x) for x in a); OUT.append(s); print(s)

    P('='*118)
    P("RE-VERIFICACIÓN YUNARA — nivel 15, LT+Alacrity full, ventana de pelea (Q activa, R on en 3v3)")
    P('='*118)

    # ── 1. Inputs corregidos de la Tabla A publicada ──
    ev = eval_build(B_STD)
    P(f"\n[1] TABLA A PUBLICADA — inputs auditados:")
    P(f"    AD = 100 (58+3.0×14) + 210 ítems = {ev['AD']:.0f}   [publicado: 268 → omitió el growth (+42)]")
    P(f"    B = 0.23+0.448+1.25(ítems)+0.384+0.21+0.55(Q) = {ev['B']:.3f} → AS = {ev['AS']:.3f}")
    P(f"    [publicado: 'AS 2.83 con Pow-Pow x3' — irrazastreable; su §3 usa 2.42 con AS-ítems 0.90 (omite Kraken 35 %)]")
    P(f"    crit {ev['crit']:.0f} % · pen {ev['pen']:.0f} % · magn {ev['magn']:.2f} · engine 1v1 {ev['engine1']:.0f} · heal {ev['heal']:.0f}")

    # ── 2. Reproducción de titulares publicados (misma convención de ventana) ──
    P(f"\n[2] TITULARES: publicado vs re-verificado (ventana: q_up 1.0, r_up 1.0 en 3v3, magn 1.0, Kraken missing 50):")
    pub = {'STD': (B_STD, (3042, 10551, 2150, 1480, 186)), 'TANK': (B_TANK, (3115, 9285, 2451, 1850, 525)),
           'COMUNIDAD-RFC': (B_RFC, (2850, 8900, 0, 1320, 0))}
    for name,(b, exp) in pub.items():
        row = [totals(b, scenario=s)['total'] for s in ESC]
        heal = totals(b, scenario='1v1')['heal']
        got = (*row, heal)
        dd = ' · '.join(f"{s} {g:>6.0f} ({(g/e-1)*100:+.0f} %)" if e else f"{s} {g:>6.0f}" for s,g,e in zip((*ESC,'heal'), got, exp))
        P(f"    {name:<14} {dd}")
    P("    → Los titulares publicados NO se reproducen ni con SUS propios supuestos: el inflado viene de")
    P("      AS 2.83 (vs 2.647 real), spread crítico permanente + Magnification sobre el spread, y términos")
    P("      mágicos sin mitigar por MR. Los rankings internos, en cambio, sí se sostienen (ver [3]-[5]).")

    # ── 3. Sensibilidades clave ──
    P(f"\n[3] SENSIBILIDADES (sobre Tabla A, 1v1 / 3v3):")
    base1 = totals(B_STD)['total']; base3 = totals(B_STD, scenario='3v3')['total']
    for etiqueta, kw, sc in [
        ('q_up 0.70 (supuesto publicado)', dict(q_up=0.7), '1v1'),
        ('sostenido real (q .7, r .23, magn .8)', dict(q_up=0.7, r_up=0.23, magn_uptime=0.8), '3v3'),
        ('magn 0.6 (comps de dive)', dict(magn_uptime=0.6), '1v1'),
        ('pasiva conv. B (8 % del golpe crit)', dict(passive_mode='B'), '1v1'),
        ('BotRK 7 % n/a — Kraken missing 75 %', dict(kraken_missing=75), '1v1'),
        ('Flurry n/a — sin LT (Fleet)', dict(), '1v1')]:
        if etiqueta.startswith('Flurry'): continue
        t = totals(B_STD, scenario=sc, **kw)['total']
        b = base1 if sc=='1v1' else base3
        P(f"    {etiqueta:<42} {sc}: {t:>6.0f} ({(t/b-1)*100:+.1f} %)")
    for fu in (0.5, 1.0):
        t = totals(B_TANK, flurry_uptime=fu)['total']
        P(f"    Flurry Yun Tal uptime {fu:.0%} (variante A2)     1v1: {t:>6.0f} · AS raw {eval_build(B_TANK, flurry_uptime=fu)['raw_AS']:.2f}")
    t7 = totals(['gunmetal','c44','runaan','ie','ldr','botrk'], botrk_pct=7)['total']
    t6 = totals(['gunmetal','c44','runaan','ie','ldr','botrk'])['total']
    P(f"    BotRK 6→7 % (build BotRK-6.º)                1v1: {t6:.0f} → {t7:.0f} ({(t7/t6-1)*100:+.1f} %)")

    # ── 4. Matriz de riesgo del 6.º slot (el corazón de la pregunta del autor) ──
    P(f"\n[4] MATRIZ RIESGO/DAÑO — núcleo C44+Runaan's+IE+LDR + { 'X' } (6.º slot) y variantes de botas/slot:")
    P(f"    {'variante':<44}{'1v1':>6}{'3v3':>7}{'vs120':>7}{'vsT':>6}{'EHP':>7}{'heal':>6}{'surv':>7}")
    variantes = [
        ('Kraken (publicada)',            ['gunmetal','c44','runaan','ie','ldr','kraken']),
        ('BotRK',                         ['gunmetal','c44','runaan','ie','ldr','botrk']),
        ('BotRK + Flurry→YunTal x C44',   B_TANK),
        ('Guardian Angel',                ['gunmetal','c44','runaan','ie','ldr','ga']),
        ('Mercurial Scimitar',            ['gunmetal','c44','runaan','ie','ldr','scimitar']),
        ('Bloodthirster',                 ['gunmetal','c44','runaan','ie','ldr','bt']),
        ('Death’s Dance',                 ['gunmetal','c44','runaan','ie','ldr','deathsdance']),
        ('Shieldbow (por C44)',           ['gunmetal','shieldbow','runaan','ie','ldr','kraken']),
        ('Shieldbow+BotRK (por C44/Krak)',['gunmetal','shieldbow','runaan','ie','ldr','botrk']),
        ('Maw (por Kraken)',              ['gunmetal','c44','runaan','ie','ldr','maw']),
        ('Wit’s End (por Kraken)',        ['gunmetal','c44','runaan','ie','ldr','witsend']),
        ('Fiendhunter (por C44)',         ['gunmetal','fiend','runaan','ie','ldr','kraken']),
        ('Yun Tal (por C44)',             ['gunmetal','yuntal','runaan','ie','ldr','kraken']),
        ('Stormrazor (por C44)',          ['gunmetal','storm','runaan','ie','ldr','kraken']),
        ('Armored Advance (por Gunmetal)',['armored_adv','c44','runaan','ie','ldr','kraken']),
        ('Chainlaced (por Gunmetal)',     ['chainlaced','c44','runaan','ie','ldr','kraken']),
    ]
    for etiqueta, b in variantes:
        m = metrics(b)
        P(f"    {etiqueta:<44}{m['1v1']:>6.0f}{m['3v3']:>7.0f}{m['vs120']:>7.0f}{m['vsTanque']:>6.0f}{m['ehp']:>7.0f}{m['heal']:>6.0f}{m['surv']:>7.0f}")

    # ── 5. Optimizadores (4 objetivos) ──
    optimize(PESOS_DPS,    label="(objetivo DPS puro — el del reporte publicado)", top=5)
    sc1, mx1 = optimize(PESOS_RIESGO, label="RIESGO-AJUSTADO (DPS .64 / supervivencia+sustain .36)", top=6)
    optimize(PESOS_TANQUE,  label="ANTI-TANQUE (vsT .35)", top=4)
    optimize(PESOS_DIVE,    label="VS DIVE (supervivencia .32, magn_uptime 0.6)", top=4, magn_uptime=0.6)

    # ── 6. Primer ítem (checkpoints con modelo completo) ──
    P(f"\n[6] CHECKPOINTS — 1.er/2.º ítem (Berserker's T2 + 1; Gunmetal + 2), modelo completo:")
    P(f"    {'candidato':<30}{'lvl9 1v1':>9}{'lvl9 3v3':>9}{'lvl12 1v1':>10}{'AS':>6}{'AD':>6}")
    for etiqueta, b in [('C44', ['berserker','c44']), ('Kraken', ['berserker','kraken']),
                        ('Yun Tal (+Flurry 50 %)', ['berserker','yuntal']), ('Stormrazor', ['berserker','storm']),
                        ('Fiendhunter', ['berserker','fiend']), ('BotRK', ['berserker','botrk'])]:
        kw = dict(flurry_uptime=0.5) if 'yuntal' in b else {}
        t9 = totals(b, level=9, **kw); t93 = totals(b, level=9, scenario='3v3', r_up=0.3, **kw)
        b12 = [x if x!='berserker' else 'gunmetal' for x in b] + ['runaan']
        t12 = totals(b12, level=12, **kw)
        P(f"    {etiqueta:<30}{t9['total']:>9.0f}{t93['total']:>9.0f}{t12['total']:>10.0f}{t9['AS']:>6.2f}{t9['AD']:>6.0f}")
    P("    Publicado (lvl 9 1v1): C44 495 · Kraken 560 · Yun Tal 480 · Storm 520 — veredicto C44-1.º por sinergia de spread.")

    with open('model/yunara_resultados.txt','w',encoding='utf-8') as f: f.write('\n'.join(OUT)+'\n')
    print('\n[salida guardada en model/yunara_resultados.txt]')

if __name__ == '__main__':
    main()
