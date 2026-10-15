# -*- coding: utf-8 -*-
"""
WR-LAB · model/xayah_model.py — RE-VERIFICACIÓN XAYAH DRAGON LANE (batch4, 12/10/2026)
=======================================================================================
Motor de verificación independiente del reporte publicado `xayah` v2 (08-09/10/2026,
engine: autos, verification: AL_DIA). Objetivos:
  1. REPRODUCIR las cifras publicadas (3 146 / 5 929 / 1 767 / 1 582 / heal 498 /
     burst E / v1 Beta 2 819 / comunidad 2 654) con una reimplementación propia.
  2. Correr las SENSIBILIDADES pendientes que el reporte declaró pero no publicó:
     D1 (AS growth 0.034 vs 0.03) · D3 (BotRK 6 % engine vs 7 % oficial 7.3) ·
     D7 (W uptime: ventana vs sostenido 29 % vs sin W) · Flurry de Yun Tal
     (no modelado en el engine) · on-hit de BotRK en rayos de Runaan's (upside) ·
     D8 (Navori ×0.75).
  3. RE-OPTIMIZAR con objetivo EXTENDIDO: el engine de autos del lab NO modela
     E/Q/R/pasiva (términos manuales en el reporte); aquí la búsqueda exhaustiva
     puntúa engine + skills juntos (E escala con crit/IE/bAD desde 7.3 → debe
     entrar en el objetivo). Restricciones del reporte: crit = 100 exacto (Ley 1),
     pen ≥ 30 (Ley 3), Ley 3b (1 solo pen_pct), presupuesto 18 000 g.
  4. Curva de poder (checkpoints lvl 9/12/14) con las convenciones publicadas.

FUENTES: WR-LAB v1.15.2 — notas oficiales 7.3 (sección XAYAH + apéndice AS),
items_7.3.csv + diff 7.3/7.3a (Yun Tal AS 35), dps_model.py (constantes engine),
wiki oficial (decaimiento E −10 %/pluma piso 10 %, cleave 45 % AD, R 5 plumas),
reporte xayah v2 (§2/§3 convenciones y supuestos).

CONVENCIONES DEL REPORTE (se respetan para que la verificación sea comparable):
  - self_as_buff = 0.55 (W rank 4) activo en ventana de pelea; sostenido real 29 %
    → w_mult = 1 + 0.25×(4/14) = 1.0714 sobre el engine (pluma de W = 25 % del ataque).
  - TOTAL = engine×w_mult + E-DPS + Q-DPS + R-DPS (+ cleave en 3v3), luego ×mit del
    escenario. GS amp solo sobre autos/rayos (engine), NO sobre skills.
  - E: 5 plumas (Σ decaimiento 4.0) · R: 3 de 5 · Q: 1 daga/objetivo · cleave ~1
    auto empoderado/s (45 % AD, sin crit) a 2 objetivos extra en 3v3.
  - BotRK base 6 % (piso del engine); 7 % oficial como sensibilidad D3.
  - LT full (6×6.4 % ranged + bala 24×(1+0.0067×B×100)) · Alacrity 21 %.
"""
import itertools, math

# ══════════════════════════ CONSTANTES (dps_model.py) ══════════════════════════
AS_CAP        = 3.0
CRIT_DMG_BASE = 2.00
CRIT_DMG_IE   = 2.30
LT_RANGED_STACK = 0.064
LT_BULLET_SCALE = 0.0067
ALACRITY_FULL = 0.21
EPS_AS = 0.02

# ══════════════════════════ SPEC XAYAH (champspecs.py, 09/10) ══════════════════════════
SPEC = dict(name="Xayah", base_ad=60.0, ad_growth=4.2, base_as=0.658, as_ratio=0.658,
            base_bonus_as=0.22, as_per_lvl=0.034, ranged=True, attack_range=575,
            self_as_buff=0.55, aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0,
            uses_magnification=True, free_crit=0.0)

# ══════════════════════════ ÍTEMS (registro del lab, valores 7.3a) ══════════════════════════
def I(key, gold, ad=0, ap=0, a_s=0, crit=0, pen=0, ls=0, mr=0, armor=0, hp=0, ah=0, ms=0,
      kraken=False, magnification=False, ie=False, runaan=False, energized=0,
      onhit_flat=0, onhit_pct_current=0, spellblade=0, giant_slayer=0, execute_pct=0,
      pen_pct_group=False, comment=""):
    return dict(key=key, gold=gold, ad=ad, ap=ap, a_s=a_s, crit=crit, pen=pen, ls=ls,
                mr=mr, armor=armor, hp=hp, ah=ah, ms=ms, kraken=kraken,
                magnification=magnification, ie=ie, runaan=runaan, energized=energized,
                onhit_flat=onhit_flat, onhit_pct_current=onhit_pct_current,
                spellblade=spellblade, giant_slayer=giant_slayer, execute_pct=execute_pct,
                pen_pct_group=pen_pct_group, comment=comment)

ITEMS = {i['key']: i for i in [
    I("c44",       2900, ad=55, crit=25, magnification=True),
    I("ie",        3400, ad=75, crit=25, ie=True),
    I("runaan",    2650, a_s=40, crit=25, ms=4, runaan=True),
    I("ldr",       3300, ad=35, pen=35, crit=25, giant_slayer=12, pen_pct_group=True),
    I("mortal",    3000, ad=35, pen=30, crit=25, pen_pct_group=True),
    I("kraken",    2900, ad=45, a_s=35, ms=4, kraken=True),
    I("rfc",       2650, a_s=40, crit=25, ms=4, energized=80),
    I("storm",     3000, ad=50, crit=25, a_s=20, energized=120),
    I("bt",        3200, ad=75, ls=15),
    I("gale",      3100, ad=60, crit=25, ms=4),
    I("shieldbow", 3000, ad=55, crit=25),
    I("fiend",     2650, a_s=45, crit=25, ms=4),
    I("collector", 3000, ad=50, pen=10, crit=25, execute_pct=5),
    I("pd",        2650, a_s=40, crit=25, ms=7),
    I("navori",    2650, a_s=40, crit=25, ms=4),
    I("er",        3000, ad=50, crit=25, ah=20, spellblade=1.0),
    I("yuntal",    3100, ad=50, a_s=35, crit=25),
    I("manamune",  2900, ad=40, ah=15),
    I("witsend",   2800, a_s=50, mr=45, onhit_flat=40),
    I("terminus",  3000, ad=35, a_s=35, onhit_flat=30, pen=30, pen_pct_group=True),
    I("botrk",     3100, ad=40, a_s=30, ls=12, onhit_pct_current=6),
    I("guinsoo",   3000, ad=35, ap=30, a_s=30, onhit_flat=30),
    I("statikk",   3000, ad=40, ap=40, a_s=30, ms=4, energized=60),
    I("scimitar",  3100, ad=45, mr=40, ls=12),
    I("ga",        3200, ad=45, armor=40),
    I("maw",       3000, ad=55, mr=45, ah=10),
    I("deathsdance",3300, ad=50, armor=45, ah=15),
    # botas
    I("berserker", 1200, a_s=35),
    I("gunmetal",  2200, a_s=50, ls=5),
    I("chainlaced",2200, hp=150, mr=30),
    I("armored_adv",2200, hp=150, armor=30),
    I("crimson",   2000, ah=25),
    I("armorcrusher",2200, ad=25, pen=12),
    I("mercury_t", 1200, hp=150, mr=25),
    I("plated",    1200, hp=150, armor=20),
]}
BOOTS = {"gunmetal","chainlaced","armored_adv","crimson","armorcrusher","berserker","mercury_t","plated"}
KRAKEN_RANGED_L15, KRAKEN_MISSING_BONUS = 168, 0.0075

def lvl_as_bonus(as_per_lvl, level):
    return as_per_lvl * sum(0.7 + 0.04*L for L in range(1, level))

def as_total(keys, level=15, lt=True, alacrity=ALACRITY_FULL, self_buff_on=True,
             as_per_lvl=None, flurry_uptime=0.0, self_as_buff=None):
    sp = SPEC
    apl = sp['as_per_lvl'] if as_per_lvl is None else as_per_lvl
    sab = sp['self_as_buff'] if self_as_buff is None else self_as_buff
    ai = sum(ITEMS[k]['a_s'] for k in keys)/100.0
    lt_as = LT_RANGED_STACK*6 if lt else 0
    B = (sp['base_bonus_as'] + lvl_as_bonus(apl, level) + ai + lt_as + alacrity
         + (sab if self_buff_on else 0) + flurry_uptime*0.35)
    raw = sp['base_as'] + sp['as_ratio']*B
    return min(raw, AS_CAP), raw, B

def lt_bullet(level, B):
    base = 6 + (24-6)*(level-1)/14
    return base * (1 + LT_BULLET_SCALE*B*100)

def eval_build(keys, level=15, targets=1, armor=0.0, tank=False, lt=True,
               alacrity=ALACRITY_FULL, missing_hp=50, enemy_hp=2200,
               self_buff_on=True, spellblade_uptime=1/1.5, botrk_pct=None,
               flurry_uptime=0.0, as_per_lvl=None, bolts_onhit=False, self_as_buff=None):
    """Port fiel de dps_model.eval_build (+ parámetros de sensibilidad)."""
    its = [ITEMS[k] for k in keys]
    gold = sum(i['gold'] for i in its)
    base_ad = SPEC['base_ad'] + SPEC['ad_growth']*(level-1)
    ad   = base_ad + sum(i['ad'] for i in its)
    crit = min(sum(i['crit'] for i in its) + SPEC['free_crit'], 100)/100.0
    pen  = min(sum(i['pen'] for i in its), 100)
    ls   = sum(i['ls'] for i in its)
    AS, raw_as, B = as_total(keys, level, lt, alacrity, self_buff_on, as_per_lvl, flurry_uptime, self_as_buff)
    cdmg = (CRIT_DMG_IE if any(i['ie'] for i in its) else CRIT_DMG_BASE) * SPEC['crit_dmg_mod']
    cmult = 1 + crit*(cdmg-1)
    magn = 1.10 if (SPEC['uses_magnification'] and any(i['magnification'] for i in its)) else 1.0
    amp  = 1 + (sum(i['giant_slayer'] for i in its)/100.0 if tank else 0)

    hit = ad * SPEC['aa_mult'] * cmult * magn * amp
    d   = AS * hit
    bolts = 0.0
    for i in its:
        if i['kraken']:
            base = KRAKEN_RANGED_L15*(level/15)
            d += AS/3 * base * (1 + KRAKEN_MISSING_BONUS*missing_hp)
        if i['energized']: d += AS/7 * i['energized']
        if i['onhit_flat']: d += AS * i['onhit_flat']
        if i['onhit_pct_current']:
            pct = (botrk_pct if (botrk_pct is not None and i['key']=='botrk') else i['onhit_pct_current'])
            d += AS * max(15, pct/100*enemy_hp)
        if i['spellblade']: d += spellblade_uptime * (1.35*base_ad + 80*crit)
    bullet = AS * lt_bullet(level, B) if lt else 0
    d += bullet

    aoe = 0.0
    if targets > 1 and any(i['runaan'] for i in its):
        bolts = AS * 0.55 * ad * cmult * amp * min(2, targets-1)
        aoe += bolts
        if bolts_onhit and any(i['key']=='botrk' for i in its):
            pct = botrk_pct if botrk_pct is not None else 6
            extra = AS * max(15, pct/100*enemy_hp) * min(2, targets-1)
            aoe += extra; bolts += extra
    mit = 100/(100+armor*(1-pen/100)) if armor > 0 else 1.0
    heal = d*(ls/100)*mit
    if 'gunmetal' in keys: heal += 12*AS
    elif 'berserker' in keys: heal += 10*AS

    return dict(gold=gold, AD=ad, base_ad=base_ad, AS=AS, raw_AS=raw_as, B=B,
                crit=crit*100, crit_dmg=cdmg*100, pen=pen, cmult=cmult, amp=amp,
                dps1=d*mit, dpsN=(d+aoe)*mit, engine1=d, engineN=d+aoe,
                bullet=bullet, bolts=bolts, heal=heal, overcap=raw_as>AS_CAP+EPS_AS, mit=mit)

# ══════════════════════════ TÉRMINOS DE SKILLS (manual §3 del reporte) ══════════════════════════
W_MULT = 1 + 0.25*(4/14)          # sostenido: pluma 25 % × uptime 4/14 = ×1.0714

def e_decay_sum(n):
    """Σ del decaimiento de E: −10 % por pluma previa sobre el mismo objetivo, piso 10 %."""
    return sum(max(0.10, 1.0 - 0.10*k) for k in range(n))

def skills(keys, level=15, e_feathers=5, e_cd=8.0, q_cd=7.0, r_cd=60.0, r_feathers=3,
           e_rank=4, targets=1, navori_cdr=1.0, armor=0.0, **evkw):
    ev = eval_build(keys, level=level, armor=armor, **evkw)
    bAD = ev['AD'] - ev['base_ad']
    crit = ev['crit']/100.0
    cdmg = ev['crit_dmg']/100.0
    e_mult = 1 + 0.5*crit + 0.5*(cdmg-2)*crit          # fórmula oficial 7.3
    e_base = {1:70, 2:80, 3:90, 4:100}[e_rank]
    e_per = (e_base + 0.5*bAD) * e_mult
    e_dps = e_per * e_decay_sum(e_feathers) / (e_cd*navori_cdr)
    q_dps = (125 + 0.5*bAD) / (q_cd*navori_cdr)         # Q rank 4 (1 daga al principal)
    r_rank = 3 if level >= 13 else (2 if level >= 9 else 1)
    r_base = {1:150, 2:250, 3:350}[r_rank]
    r_dps = r_feathers * (r_base + 1.0*bAD) / r_cd
    cleave = 0.0
    if targets > 1:
        cleave = 1.0 * 0.45 * ev['AD'] * min(2, targets-1)   # ~1 auto empoderado/s, 45 % AD sin crit
    return dict(e_per=e_per, e_mult=e_mult, e_sum=e_decay_sum(e_feathers), e_dps=e_dps,
                q_dps=q_dps, r_dps=r_dps, cleave=cleave, bAD=bAD,
                total_skills=(e_dps+q_dps+r_dps+cleave))

def totals(keys, level=15, scenario='1v1', botrk_pct=None, flurry_uptime=0.0,
           w_mode='window', bolts_onhit=False, as_per_lvl=None, e_feathers=5,
           e_rank=4, e_cd=8.0, navori_cdr=1.0, self_as_buff=None):
    """TOTAL del reporte: engine×w_mult + skills, ×mit del escenario."""
    kw = dict(level=level, botrk_pct=botrk_pct, flurry_uptime=flurry_uptime,
              bolts_onhit=bolts_onhit, as_per_lvl=as_per_lvl, self_as_buff=self_as_buff)
    scen = {'1v1': dict(), '3v3': dict(targets=3), 'vs120': dict(armor=120),
            'vsTanque': dict(armor=220, tank=True, enemy_hp=4500)}[scenario]
    if w_mode == 'off':
        kw2 = dict(kw); kw2['self_buff_on'] = False
        ev = eval_build(keys, **{**kw2, **scen}); w_mult = 1.0
    else:
        ev = eval_build(keys, **{**kw, **scen}); w_mult = W_MULT
    sk = skills(keys, level=level, targets=scen.get('targets',1), e_feathers=e_feathers,
                e_rank=e_rank, e_cd=e_cd, navori_cdr=navori_cdr, armor=scen.get('armor',0.0),
                **{k:v for k,v in kw.items() if k!='level'})
    eng = ev['engineN'] if scenario=='3v3' else ev['engine1']    # crudo (sin mitigar)
    total = (eng*w_mult + sk['total_skills']) * (ev['mit'] if scenario in ('vs120','vsTanque') else 1.0)
    return dict(engine=eng, w_mult=w_mult, total=total, heal=ev['heal'], AS=ev['AS'],
                AD=ev['AD'], crit=ev['crit'], pen=ev['pen'], raw_AS=ev['raw_AS'], B=ev['B'],
                bolts=ev['bolts'], bullet=ev['bullet'], overcap=ev['overcap'],
                **{k:sk[k] for k in ('e_dps','q_dps','r_dps','cleave','e_per','e_mult','e_sum','bAD')})

# ══════════════════════════ BUILDS DE REFERENCIA ══════════════════════════
B_OPT   = ['gunmetal','yuntal','runaan','botrk','ldr','ie']            # ⭐ Tabla A publicada
B_OPT2  = ['gunmetal','c44','runaan','botrk','ldr','ie']               # 🔬 top-2
B_OPT4  = ['gunmetal','yuntal','runaan','c44','terminus','ie']         # 🔬 top-4 glass
B_V1    = ['gunmetal','c44','runaan','ie','ldr','bt']                  # 📌 v1 Beta
B_KRAK  = ['gunmetal','c44','runaan','ie','ldr','kraken']              # 🔬 análoga Jinx
B_COMM  = ['gunmetal','yuntal','navori','ie','ldr','ga']               # 🌐 comunidad
B_MORT  = ['gunmetal','yuntal','runaan','botrk','mortal','ie']         # anti-heal
B_GA    = ['gunmetal','yuntal','runaan','ga','ldr','ie']               # anti-burst

def run_verification():
    print('='*112)
    print("VERIFICACIÓN — cifras publicadas del reporte xayah v2 (nivel 15, LT+Alacrity full, W en ventana)")
    print('='*112)
    objetivos = {  # (build, (1v1, 3v3, vs120, vsTanque, heal), kwargs)
        '⭐ ÓPTIMA (Tabla A)': (B_OPT,  (3146, 5929, 1767, 1582, 498), {}),
        '🔬 top-2 (C44)':      (B_OPT2, (3144, 5769, 1766, 1571, 495), {}),
        '🔬 top-4 (glass)':    (B_OPT4, (3218, 6162, 1749, 1267, 174), {}),
        '📌 v1 Beta':          (B_V1,   (2819, 5535, 1584, 1278, 510), {}),
        '🔬 análoga Jinx':     (B_KRAK, (3063, 5758, 1721, 1379, 165), {}),
        '🌐 comunidad':        (B_COMM, (2654, 2945, 1491, 1198, 142), dict(navori_cdr=0.75)),  # convención D8
    }
    for name,(b, exp, kw) in objetivos.items():
        row = [totals(b, scenario=s, **kw)['total'] for s in ('1v1','3v3','vs120','vsTanque')]
        heal = totals(b, scenario='1v1', **kw)['heal']
        got = (*row, heal)
        deltas = [f"{(g/e-1)*100:+.1f}%" for g,e in zip(got,exp)]
        ok = all(abs(g/e-1) < 0.01 for g,e in zip(got,exp))
        print(f"  {name:<20} {'✅' if ok else '⚠️'} 1v1 {row[0]:>6.0f} ({deltas[0]:>6}) · 3v3 {row[1]:>6.0f} ({deltas[1]:>6}) · "
              f"vs120 {row[2]:>6.0f} ({deltas[2]:>6}) · vsT {row[3]:>6.0f} ({deltas[3]:>6}) · heal {heal:>4.0f} ({deltas[4]:>6})")
    # variantes publicadas (anti-heal / anti-burst, Tablas A2/A3)
    for name, b in [('A2 anti-burst (GA)', B_GA), ('A3 anti-heal (Mortal)', B_MORT)]:
        t1 = totals(b, scenario='1v1')['total']; tt = totals(b, scenario='vsTanque')['total']
        base1 = totals(B_OPT, scenario='1v1')['total']
        print(f"  {name:<24} 1v1 {t1:.0f} ({(t1/base1-1)*100:+.1f} % vs óptima) · vsTanque {tt:.0f}")
    # desglose de la óptima
    t = totals(B_OPT, scenario='1v1'); t3 = totals(B_OPT, scenario='3v3')
    ev = eval_build(B_OPT)
    print(f"\n  DESGLOSE ÓPTIMA 1v1: engine {ev['engine1']:.0f} (autos {ev['AS']*ev['AD']*ev['cmult']:.0f} + bala {ev['bullet']:.0f} + BotRK {ev['AS']*132:.0f}) "
          f"×W {t['w_mult']:.4f} + E {t['e_dps']:.0f} + Q {t['q_dps']:.0f} + R {t['r_dps']:.0f} = {t['total']:.0f}")
    print(f"  DESGLOSE ÓPTIMA 3v3: engine {ev['engineN']:.0f} (rayos {eval_build(B_OPT, targets=3)['bolts']:.0f}) → total {t3['total']:.0f} (cleave {t3['cleave']:.0f})")
    print(f"  AS {ev['AS']:.3f} (raw {ev['raw_AS']:.3f}, B {ev['B']:.3f}) · AD {ev['AD']:.1f} · crit {ev['crit']:.0f} % · E(5) burst {t['e_per']*t['e_sum']:.0f} · auto crit {ev['AD']*2.30:.0f}")

def run_sensitivities():
    print('\n'+'='*112)
    print("SENSIBILIDADES (las que el reporte declaró sin publicar / pendientes de resolución)")
    print('='*112)
    base = totals(B_OPT, scenario='1v1')['total']
    baseT = totals(B_OPT, scenario='vsTanque')['total']
    base3 = totals(B_OPT, scenario='3v3')['total']

    # D3 — BotRK 7 % oficial
    t7  = totals(B_OPT, scenario='1v1', botrk_pct=7)['total']
    t7T = totals(B_OPT, scenario='vsTanque', botrk_pct=7)['total']
    print(f"  D3 BotRK 7 % oficial : 1v1 {t7:.0f} ({(t7/base-1)*100:+.1f} %) · vsTanque {t7T:.0f} ({(t7T/baseT-1)*100:+.1f} %)  [reporte predijo 3 210 / 1 712]")

    # D1 — AS growth 0.03
    t03 = totals(B_OPT, scenario='1v1', as_per_lvl=0.03)['total']
    print(f"  D1 AS growth 0.03    : 1v1 {t03:.0f} ({(t03/base-1)*100:+.1f} %)  [reporte: Δ +1.5 % AS, rankings sin cambio]")

    # D7 — W: sostenido real (29 % uptime → sin AS de W fuera de ventana) vs sin W
    toff = totals(B_OPT, scenario='1v1', w_mode='off')['total']
    print(f"  D7 sin W (farmeo/uptime 0): 1v1 {toff:.0f} ({(toff/base-1)*100:+.1f} %)  [reporte: −13.3 % engine]")

    # Flurry de Yun Tal (uptime 50 % y 100 %)
    for up in (0.5, 1.0):
        tf = totals(B_OPT, scenario='1v1', flurry_uptime=up)['total']
        ev = eval_build(B_OPT, flurry_uptime=up)
        print(f"  Flurry uptime {up:.0%}     : 1v1 {tf:.0f} ({(tf/base-1)*100:+.1f} %) · AS raw {ev['raw_AS']:.2f} → efectiva {ev['AS']:.2f} {'(CAP)' if ev['raw_AS']>3.0 else ''}")

    # Rayos con on-hit (upside 3v3)
    t3on = totals(B_OPT, scenario='3v3', bolts_onhit=True)['total']
    print(f"  Rayos+on-hit BotRK 6%: 3v3 {t3on:.0f} ({(t3on/base3-1)*100:+.1f} %)  [reporte predijo ~6 700 (+13 %)]")
    t3on7 = totals(B_OPT, scenario='3v3', bolts_onhit=True, botrk_pct=7)['total']
    print(f"  Rayos+on-hit BotRK 7%: 3v3 {t3on7:.0f} ({(t3on7/base3-1)*100:+.1f} %)")

    # Todo junto (techo realista 7.3a): BotRK 7 % + Flurry 50 % + rayos on-hit
    tall  = totals(B_OPT, scenario='1v1', botrk_pct=7, flurry_uptime=0.5)['total']
    tall3 = totals(B_OPT, scenario='3v3', botrk_pct=7, flurry_uptime=0.5, bolts_onhit=True)['total']
    tallT = totals(B_OPT, scenario='vsTanque', botrk_pct=7, flurry_uptime=0.5)['total']
    print(f"  TECHO (7%+Flurry50%+rayos on-hit): 1v1 {tall:.0f} ({(tall/base-1)*100:+.1f} %) · 3v3 {tall3:.0f} ({(tall3/base3-1)*100:+.1f} %) · vsT {tallT:.0f} ({(tallT/baseT-1)*100:+.1f} %)")

    # D8 — Navori con convención ×0.75 (comunidad)
    tn = totals(B_COMM, scenario='1v1')['total']; tn75 = totals(B_COMM, scenario='1v1', navori_cdr=0.75)['total']
    print(f"  D8 comunidad Navori  : 1v1 {tn:.0f} · con CD×0.75 {tn75:.0f} ({(tn75/tn-1)*100:+.1f} %) — ¿cierra el gap vs óptima ({base:.0f})? NO ({(tn75/base-1)*100:+.1f} %)")

    # Burst E por plumas (tabla del reporte)
    print("\n  BURST E (100 % crit + IE, bAD 200): ", end='')
    for n in (3,5,8,15):
        e = (100+0.5*(318.8-118.8))*1.65*e_decay_sum(n)
        print(f"E({n})={e:.0f} ", end='')
    print(f" [reporte: E(3)=891 root 1.25 s · E(5)=1 320 · E(8)=1 716]")

def run_optimizer(botrk_pct=None, flurry_uptime=0.0, bolts_onhit=False, budget=18000,
                  crit_min=100, pen_min=30, top=6, label=""):
    """Búsqueda exhaustiva con objetivo EXTENDIDO (engine×W + skills) y restricciones del reporte."""
    pool = [k for k in ITEMS if k not in BOOTS]
    boots_pool = ['gunmetal','armorcrusher','chainlaced','armored_adv']
    cands = []
    for bk in boots_pool:
        for combo in itertools.combinations(pool, 5):
            keys = [bk]+list(combo)
            g = sum(ITEMS[k]['gold'] for k in keys)
            if g > budget: continue
            crit = min(sum(ITEMS[k]['crit'] for k in keys), 100)
            if crit < crit_min: continue
            if sum(ITEMS[k]['crit'] for k in keys) > 100: continue        # poda estructural Ley 1
            pen = sum(ITEMS[k]['pen'] for k in keys)
            if pen < pen_min: continue                                     # Ley 3
            if sum(1 for k in keys if ITEMS[k]['pen_pct_group']) > 1: continue  # Ley 3b
            cands.append(keys)
    res = []
    for keys in cands:
        r = {}
        for s in ('1v1','3v3','vs120','vsTanque'):
            r[s] = totals(keys, scenario=s, botrk_pct=botrk_pct, flurry_uptime=flurry_uptime,
                          bolts_onhit=bolts_onhit)['total']
        r['keys'] = keys; r['gold'] = sum(ITEMS[k]['gold'] for k in keys)
        ev = eval_build(keys)
        r['AS'] = ev['AS']; r['overcap'] = ev['raw_AS'] > AS_CAP + EPS_AS
        res.append(r)
    mx = {s: max(x[s] for x in res) for s in ('1v1','3v3','vs120','vsTanque')}
    W = dict([('1v1',.30),('3v3',.30),('vs120',.20),('vsTanque',.20)])
    for x in res: x['score'] = sum(W[s]*x[s]/mx[s] for s in W)
    res.sort(key=lambda x:-x['score'])
    print(f"\n{'='*112}\nOPTIMIZADOR EXTENDIDO {label} — {len(cands)} hojas legales (crit=100, pen≥30, ≤{budget} g, Ley 3b)")
    print(f"{'='*112}")
    for i,x in enumerate(res[:top],1):
        mark = ' ⚠️overcap' if x['overcap'] else ''
        print(f"  #{i} {x['score']*100:.1f} % | {x['gold']:>6} g | {' + '.join(x['keys']):<58} | "
              f"1v1 {x['1v1']:>5.0f} · 3v3 {x['3v3']:>5.0f} · vs120 {x['vs120']:>5.0f} · vsT {x['vsTanque']:>5.0f} · AS {x['AS']:.2f}{mark}")
    return res

def run_checkpoints():
    print('\n'+'='*112)
    print("CURVA DE PODER — checkpoints (ranks REALES por nivel: W1@9/W2@12/W3@14; E2@9/E4@12+; LT+Alacrity full)")
    print('='*112)
    cps = [
        ('lvl 9  (~7:30, Yun Tal + Berserker’s)', 9,  ['berserker','yuntal'],
         dict(e_feathers=4, e_rank=2, e_cd=10.0, self_as_buff=0.40)),
        ('lvl 12 (~11:30, +Runaan’s +⬆️Gunmetal)', 12, ['gunmetal','yuntal','runaan'],
         dict(e_feathers=5, e_rank=4, e_cd=8.0, self_as_buff=0.45)),
        ('lvl 14 (~14:15, +IE)',                   14, ['gunmetal','yuntal','runaan','ie'],
         dict(e_feathers=5, e_rank=4, e_cd=8.0, self_as_buff=0.50)),
        ('lvl 15 (~17:00, +BotRK)',                15, ['gunmetal','yuntal','runaan','ie','botrk'],
         dict(e_feathers=5, e_rank=4, e_cd=8.0)),
        ('lvl 15 (~20:15, +LDR = Tabla A)',        15, B_OPT,
         dict(e_feathers=5, e_rank=4, e_cd=8.0)),
    ]
    for etiqueta, lvl, b, kw in cps:
        t1 = totals(b, level=lvl, scenario='1v1', **kw)
        t3 = totals(b, level=lvl, scenario='3v3', **kw)
        print(f"  {etiqueta:<42} 1v1 {t1['total']:>6.0f} · 3v3 {t3['total']:>6.0f} · AS {t1['AS']:.2f} · AD {t1['AD']:>5.1f} · E-burst {t1['e_per']*t1['e_sum']:>5.0f}")
    print("  Publicado: lvl 9 565 → lvl 12 901 → lvl 14 1 719 → lvl 15 3 146 (1v1).")

if __name__ == '__main__':
    run_verification()
    run_sensitivities()
    run_checkpoints()
    run_optimizer(label="(baseline: engine 6 %, sin Flurry, sin on-hit en rayos)")
    run_optimizer(botrk_pct=7, flurry_uptime=0.5, bolts_onhit=True,
                  label="(techo 7.3a: BotRK 7 % + Flurry 50 % + rayos on-hit)")
    run_optimizer(botrk_pct=7, flurry_uptime=0.5, bolts_onhit=True, pen_min=0, crit_min=0,
                  label="(SIN restricciones Ley 1/3 — control: ¿qué cambia?)", top=4)
