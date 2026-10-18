# -*- coding: utf-8 -*-
"""
WR-LAB · model/yuumi_agresiva_model.py — DERIVACIÓN CUSTOM "DAÑO Q+R" (batch5, 16/10/2026)
============================================================================================
Nueva derivación custom de Yuumi (petición del autor): curación/escudo en SEGUNDO
plano; maximizar daño de Q (Prowling Projectile) y R (Final Chapter).
Parche vigente: 7.3 + 7.3a + **7.3b (14/10/2026, notas EN oficiales descargadas)**:
  - Yuumi SIN cambios directos en 7.3b (su último cambio: 7.3a W HSP 6-9 %+0.01 %AP).
  - Runas 7.3b: **Electrocute 40-210 → 60-210** (early; 210 a lvl 15 intacto) ·
    **Cheap Shot CD 7→5 s** (· +40 % de su DPS verdadero) · Aery escudo 25-120→20-100
    (baseline enchanter) · Grasp 3.3→3 % (no aplica).
  - Ítems 7.3b: **Locket 2 600→2 500, HP 200→300** · Warmog umbral 900→1 250 (no aplica)
    · Yun Tal 3 100→3 000 / Thornmail 2 850 / Statikk 2 900 / Youmuu 2 900 (fuera del pool).

MOTOR = extensión de analysis_batch2.yuumi() (valor-aliado, MISMA convención de
fórmulas para e_shield/r_heal/adc_dps_add → los sacrificios son comparables 1:1 con
el baseline publicado) + MÓDULO DE DAÑO NUEVO (Q/R/runas/pasivas de ítems) que el lab
tenía en model_terms_pending ("Q daño poke").

FÓRMULAS DE DAÑO (fuente: ficha wr-meta 24/09, valores 7.3):
  Q mejorada (rank 4)  = 340 + 35 % AP  (misil ≥1 s de viaje: poke attachado estándar)
  R (rank 3, 7 olas)   = ola1 (120+15 %AP) + olas 2-7 con Wave Damage Stacks:
    interp B (default, stacking por ola impactada): Σ = 7×(120+.15AP) + 21×(40+.05AP)
                                                    = 1 680 + 2.10×AP
    interp A (conservadora, extra plano por ola):    = 1 080 + 1.35×AP
    teamfight efectivo (olas repartidas ≥2 objetivos): 0.75×B (declarado)
  Haste: cdr = AH/(100+AH) · Q/R son "CC abilities" → +20 AH con Imperial Mandate
    (Control) · R además +20 con Malignance (Scorn).
  Mitigación: mit = 100/(100+MR_ef) · MR_ef = MR×(1−pen%)−pen_flat −shreds
    (Bloodletter −30 % máx ×uptime .7 · Hatefog −10 flat ×uptime .4 post-R).
  Amps declarados: Hypershot ×1.10 (Q ≥600u, uptime 1.0; R 0.8) · Mandate Command
    ×1.07 (Q slow siempre marca, BF) · Madness ×1.04 promedio · Infinity Orb ×1.05
    promedio (×1.20 a <40 % HP, uptime .25) · Empowerment/First Strike según runa.
  Runas (7.3b): Electrocute (210+5 %AP)/13 s ×upt .7 · Dark Harvest (145+5 %AP)/20 s
    ×upt .5 · Cheap Shot 45 verdadero/5 s (Q slow BF = uptime ~100 %) · Sudden Impact
    +5 verdadero/s eq. · Scorch 49/8 s · Transcendence +10 AH · Gathering Storm +16 AP
    (min 18+) · Coup/Cut Down ×1.02/×1.033 promedio.
  Ítems de daño: Torment 2 % máx/s + Madness · Luden Echo 7.3 (140+15 %AP +3×(20+1.2 %AP)
    single-focus /9 s) · Blackfire (20+2 %AP)/s + 4 %AP/enemigo quemado (2 = +8 %) ·
    Squall (125+10 %AP)/25 s · Hatefog (180+15 %AP) por R · Protobelt (100+10 %AP)/30 s.
  Pasiva Feline Friendship: (70+25 %AP) self+aliado / CD 12-8 s → sustain (aliado ×2).

VALOR-ALIADO (idéntico a batch2.yuumi(), para la tabla de sacrificio [!DANGER]):
  hsp = Σhsp + W_BF(9+0.01AP) + Revitalize(5) · e_shield = (170+0.4AP)(1+hsp) ·
  r_heal = 7×(52+0.08AP)(1+hsp) · q_onhit aliado = 22+0.05AP · adc_dps_add (Censer) ·
  Helia: min(250, 30 % daño pre-mit) por E → en build agresiva siempre al cap ·
  Harmonic ×1.32 · Mandate team-amp +7 % · shield_per_min.

SUJETOS DE COMPARACIÓN:
  Y1 ENCHANTER (baseline lab): Scythe+Crimson+Censer+Echoes+Staff+Redemption
    (e_shield 338.8 · r_heal 650.7 · shld/min 3 953 — fixture de tests del lab).
  POKE-HÍBRIDA PUBLICADA (27/09, ANOTAR 7.3a): Scythe+Crimson+Echoes+Mandate+
    Stormsurge+Harmonic (e_shield 304.7 post-7.3a — verif block). Sus cifras de daño
    publicadas ("Q ~120-150", "haste 65-75") están mal → se recorrigen aquí (D-nuevas).

PRESUPUESTO: 13 000 g (convención lab aliado; Scythe quest 0 g fija + 1 botas + 4 ítems;
sensibilidad 12 000/14 000). Scythe: AP 0 conservador (su Versatile/Soulcast dan hasta
~68 AP adaptativo a min 20 — upside declarado, no puntuado).
"""
import itertools

# ══════════════════════════════ ÍTEMS (items_7.3.csv + 7.3b) ══════════════════════════════
def I(key, g, ap=0, hp=0, ah=0, hsp=0, ms=0, armor=0, mr=0, mana=0, pen_f=0, pen_p=0,
      **flags):
    d = dict(key=key, g=g, ap=ap, hp=hp, ah=ah, hsp=hsp, ms=ms, armor=armor, mr=mr,
             mana=mana, pen_f=pen_f, pen_p=pen_p); d.update(flags); return d

ITEMS = {i['key']: i for i in [
    # ── support/enchanter (pool del lab) ──
    I('Scythe',    0,    ah=10),
    I('Censer',    2400, ap=50, hsp=8, ms=4, censer=1),
    I('Echoes',    2400, ap=40, hp=200, ah=20, helia=1),
    I('Staff',     2400, ap=50, hsp=8, ah=10, rapids=1),
    I('Redemption',2450, ap=40, hsp=8, ah=10, redempt=1),
    I('Mikael',    2500, hp=300, hsp=9, ah=15, cleanse=1),
    I('Diadem',    2400, hp=200, hsp=8, mana=1200, diadem=1),          # 7.3a: Harmonize 0.25 %
    I('Circlet',   2400, hp=200, hsp=8, mana=500, circlet=1),
    I('Shurelya',  2500, ap=55, ah=20, ms=4, shurelya=1),
    I('Harmonic',  2500, ap=40, hp=200, ah=20, harmonic=1),
    I('Mandate',   2600, ap=60, ah=20, mandate=1),
    I('Locket',    2500, hp=300, armor=30, mr=30, ah=10, locket=1),    # 7.3b: 2500/300 HP
    I('Zeke',      2400, hp=300, armor=25, mr=25, ah=10, zeke=1),
    I('YordleTrap',2400, hp=200, armor=20, mr=20, ah=15, trap=1),
    # ── daño AP (pool agresivo) ──
    I('Liandry',   3000, ap=70, hp=300, torment=1),
    I('Morello',   2650, ap=75, hp=300, ah=15, gw=1),
    I('Rylai',     2700, ap=65, hp=350, icy=1),
    I('Horizon',   2700, ap=80, ah=25, hypershot=1),
    I('Malignance',2700, ap=90, ah=15, mana=500, scorn=1, hatefog=1),
    I('Stormsurge',2800, ap=90, pen_f=15, ms=6, squall=1),
    I('Blackfire', 2800, ap=80, ah=20, mana=500, baleful=1),
    I('Luden',     2800, ap=100, ah=10, mana=500, echo=1),
    I('Bloodletter',2900, ap=65, hp=350, ah=15, vile=1),
    I('InfinityOrb',3100, ap=110, pen_f=15, demise=1),
    I('Oceanid',   2600, ap=80, hp=200, ah=10, lethal=1),
    I('Roketbelt', 2700, ap=70, hp=250, ah=20, protobelt=1),
    I('Cryptbloom',3000, ap=75, pen_p=30, ah=20, lifedeath=1),
    I('Rabadon',   3400, ap=130, capstone=1),
    I('Riftmaker', 3100, ap=70, hp=350, ah=15, voidcorr=1, omnivamp=0.10),
    # ── botas ──
    I('Crimson',   2000, ah=25, noxian=1),
    I('Spellslinger',2200, ap=35, pen_f=18, pen_p=8),
]}
BOOTS = ('Crimson','Spellslinger')
DAMAGE_POOL = [k for k in ITEMS if k not in BOOTS and k != 'Scythe']

# ══════════════════════════════ ESTADO ══════════════════════════════
def stats(keys, keystone='electro', minors=('cheap','transc','coup'), second='gather', minute=20.0):
    its = [ITEMS[k] for k in keys]
    has = lambda f: any(f in i for i in its)
    gold = sum(i['g'] for i in its)
    ap  = sum(i['ap'] for i in its)
    if second == 'gather':
        # Gathering Storm: +2/5/9/14/20 AP por tramos desde min 6-8 (tabla del reporte Xayah)
        gs = [(8,2),(11,5),(14,9),(17,14),(20,20)]
        ap += max((v for m,v in gs if minute >= m), default=0)
    if has('rapids'):  ap += 40*(6/9)          # Staff Rapids uptime 6/9 s (E CD 9)
    ap_mult = 1.0
    if has('baleful'): ap_mult += 0.04*2        # Blackfire: +4 % AP por enemigo quemado (2 decl.)
    if has('capstone'): ap *= 1.30              # Rabadon +30 % AP total (convención lab)
    ap *= ap_mult
    ah  = sum(i['ah'] for i in its)
    if 'transc' in minors: ah += 10
    if keystone == 'phaserush': ah += 15        # Phase Rush: −20 % CDs restantes → AH eq. en pelea (decl.)
    hsp = sum(i['hsp'] for i in its) + (9 + 0.01*ap) + (5 if second=='revitalize' else 0)
    pen_f = sum(i['pen_f'] for i in its)
    pen_p = max([i['pen_p'] for i in its], default=0)
    ms = sum(i['ms'] for i in its)
    return dict(its=its, has=has, gold=gold, ap=ap, ah=ah, hsp=hsp, pen_f=pen_f, pen_p=pen_p, ms=ms)

def mit_mr(mr, st, malign_upt=0.4, vile_upt=0.7):
    mr_ef = mr*(1 - st['pen_p']/100.0) - st['pen_f']
    if st['has']('vile'):   mr_ef *= (1 - 0.30*vile_upt)
    if st['has']('hatefog'): mr_ef -= 10*malign_upt
    return 100.0/(100.0+max(0.0, mr_ef))

# ══════════════════════════════ MÓDULO DE DAÑO ══════════════════════════════
def damage(keys, mr=50, enemy_hp=2200, keystone='electro', minors=('cheap','transc','coup'),
           second='gather', minute=20.0, r_interp='B', q_enhanced_upt=1.0, teamfight=False,
           cheap_cd=5.0):
    st = stats(keys, keystone, minors, second, minute)
    ap, ah = st['ap'], st['ah']
    has = st['has']
    ah_cc  = ah + (20 if has('mandate') else 0)                  # Control: CC abilities
    ah_r   = ah_cc + (20 if has('scorn') else 0)                 # Scorn: ult
    cdr    = ah/(100.0+ah); cdr_cc = ah_cc/(100.0+ah_cc); cdr_r = ah_r/(100.0+ah_r)
    mit = mit_mr(mr, st)

    # ── Q ──
    q_base = 340 + 0.35*ap; q_weak = 220 + 0.20*ap
    q_hit  = q_base*q_enhanced_upt + q_weak*(1-q_enhanced_upt)
    q_amp  = (1.10 if has('hypershot') else 1.0) * (1.07 if has('mandate') else 1.0)
    if has('demise'): q_amp *= 1.05
    if keystone == 'empower': q_amp *= 1.056
    if keystone == 'firststrike': q_amp *= 1.0084
    q_dmg = q_hit*q_amp*mit
    q_cd  = 5.0*(1-cdr_cc)
    q_dps = q_dmg/q_cd

    # ── R ──
    if r_interp == 'B': r_raw = 1680 + 2.10*ap
    else:               r_raw = 1080 + 1.35*ap
    if teamfight: r_raw *= 0.75
    r_amp = (1.10*0.8+ (1-0.8) if has('hypershot') else 1.0)     # 80 % de las olas ≥600u
    r_amp *= (1.07 if has('mandate') else 1.0)
    if has('demise'): r_amp *= 1.05
    if keystone == 'empower': r_amp *= 1.08                      # en ventana R el amp está arriba
    r_dmg = r_raw*r_amp*mit + ((180+0.15*ap)*mit if has('hatefog') else 0)
    r_cd  = 65.0*(1-cdr_r)
    r_dps = r_dmg/r_cd

    # ── pasivas de ítems (dps sostenido en combate) ──
    extra = 0.0
    if has('torment'):  extra += 0.02*enemy_hp*mit*1.04          # Torment + Madness prom.
    if has('baleful'):  extra += (20+0.02*ap)*mit
    if has('echo'):     extra += ((140+0.15*ap) + 3*(20+0.012*ap))/9.0*mit   # single-focus 7.3
    if has('squall'):   extra += (125+0.10*ap)*mit/25.0
    if has('protobelt'):extra += (100+0.10*ap)*mit/30.0
    if has('voidcorr'): extra *= 1.054                            # Void Corruption prom.

    # ── runas de daño ──
    runes = 0.0; rune_true = 0.0
    if keystone == 'electro':      runes += (210+0.05*ap)*mit/13.0*0.7
    if keystone == 'darkharvest':  runes += (145+0.05*ap)*mit/20.0*0.5
    if 'cheap' in minors:          rune_true += 45.0/cheap_cd     # 7.3b: CD 5 s (verdadero)
    if 'sudden' in minors:         rune_true += 5.0
    if 'scorch' in minors:         runes += 49*mit/8.0
    amp_post = 1.0
    if 'coup' in minors: amp_post *= 1.02
    if 'cutdown' in minors: amp_post *= 1.033

    total = (q_dps + r_dps + extra + runes)*amp_post + rune_true
    return dict(q_dmg=q_dmg, q_cd=q_cd, q_dps=q_dps, r_dmg=r_dmg, r_cd=r_cd, r_dps=r_dps,
                extra=extra, runes=runes+rune_true, total=total, ap=ap, ah=ah, cdr=cdr,
                mit=mit, st=st)

# ══════════════════════════════ MÓDULO ALIADO (batch2 idéntico) ══════════════════════════════
def ally(keys, keystone='electro', minors=('cheap','transc','coup'), second='gather',
         minute=20.0, adc_as_base=2.6, adc_dmg_per_hit=330, revitalize=None):
    st = stats(keys, keystone, minors, second, minute)
    ap, ah, hsp = st['ap'], st['ah'], st['hsp']
    has = st['has']
    if revitalize is None: revitalize = (second=='revitalize')
    e_shield = (170+0.4*ap)*(1+hsp/100)
    e_cd = 9*(1 - ah/(100.0+ah))
    r_heal = 7*(52+0.08*ap)*(1+hsp/100)
    q_onhit = 22+0.05*ap
    adc_dps_add = adc_as_base*q_onhit
    if has('censer'):
        adc_dps_add += 0.115*adc_as_base*adc_dmg_per_hit + adc_as_base*25
    team_amp = 0.07 if has('mandate') else 0.0
    helia_per_e = 0.0
    if has('helia'):
        dmg_pre = min(250, 0.30*((340+0.35*ap)*2))       # 2 Q cargas el cap
        helia_per_e = dmg_pre*(1+hsp/100)
    harmonic_mult = 1.32 if has('harmonic') else 1.0
    passive_heal = 2*(70+0.25*ap)/10.0                    # self + aliado, CD ~10 s
    util = (0.4*(st['ms']) + (15 if has('gw') else 0) + (12 if has('icy') else 0)
            + (10 if has('lethal') else 0) + (10 if has('shurelya') else 0)
            + (12 if has('cleanse') else 0) + (8 if has('redempt') else 0)
            + (8 if has('locket') else 0) + (6 if has('zeke') else 0) + (6 if has('trap') else 0)
            + (8 if has('lifedeath') else 0))
    return dict(e_shield=e_shield, e_cd=e_cd, shield_per_min=e_shield*(60/e_cd)*harmonic_mult,
                r_heal=r_heal*harmonic_mult, q_onhit=q_onhit, adc_dps_add=adc_dps_add,
                team_amp=team_amp, helia_per_e=helia_per_e, helia_hps=helia_per_e/e_cd,
                passive_heal=passive_heal, util=util, hsp=hsp)

def metrics(keys, **kw):
    d50  = damage(keys, mr=50,  enemy_hp=2200, **kw)
    d150 = damage(keys, mr=150, enemy_hp=4500, **kw)
    a = ally(keys, **{k:kw[k] for k in ('keystone','minors','second','minute') if k in kw})
    return dict(q_dps=d50['q_dps'], r_burst=d50['r_dmg'], dps=d50['total'],
                dps_tank=d150['total'], q_hit=d50['q_dmg'], ap=d50['ap'], ah=d50['ah'],
                e_shield=a['e_shield'], r_heal=a['r_heal'], adc_dps=a['adc_dps_add'],
                helia_hps=a['helia_hps'], team_amp=a['team_amp'], shield_min=a['shield_per_min'],
                passive=a['passive_heal'], util=a['util'], gold=d50['st']['gold'])

PESOS_AGRESIVA = dict(q_dps=.26, r_burst=.20, dps=.14, dps_tank=.10,
                      e_shield=.10, r_heal=.07, adc_dps=.05, helia_hps=.03, team_amp=.02,
                      passive=.015, util=.015)   # daño .70 / aliado .27 / util .03 = 1.00
PESOS_GLASS    = dict(q_dps=.35, r_burst=.30, dps=.20, dps_tank=.15)
PESOS_HIBRIDO  = dict(q_dps=.15, r_burst=.12, dps=.08, dps_tank=.05,
                      e_shield=.18, r_heal=.14, adc_dps=.12, helia_hps=.06, team_amp=.05,
                      passive=.04, util=.01)     # daño .40 / aliado .59 / util .01 ≈ 1.00

def composite(m, mx, pesos):
    return sum(w*(m.get(k,0)/mx[k]) for k,w in pesos.items() if mx.get(k))

def optimize(pesos, budget=13000, top=6, label="", n_free=4, **kw):
    cands = []
    for bk in BOOTS:
        for combo in itertools.combinations(DAMAGE_POOL, n_free):
            g = ITEMS[bk]['g'] + sum(ITEMS[k]['g'] for k in combo)   # Scythe 0 g
            if g > budget: continue
            cands.append(['Scythe', bk]+list(combo))
    res = [(b, metrics(b, **kw)) for b in cands]
    mx = {k: max(r[1].get(k,0) for r in res) for k in PESOS_AGRESIVA}
    scored = sorted(((composite(r[1], mx, pesos),)+r for r in res), reverse=True)
    print(f"\n{'='*116}\nOPT {label} — {len(cands)} hojas (Scythe fija + botas + 4 · ≤{budget} g)")
    for i,(sc,b,m) in enumerate(scored[:top],1):
        print(f"  #{i} {sc*100:>5.1f} % | {m['gold']:>6} g | {' + '.join(b):<58} | "
              f"Q {m['q_dps']:>4.0f}/s · R {m['r_burst']:>5.0f} · DPS {m['dps']:>4.0f} · vsT {m['dps_tank']:>4.0f} · "
              f"E {m['e_shield']:>4.0f} · Rc {m['r_heal']:>4.0f} · ADC+ {m['adc_dps']:>4.0f}")
    return scored, mx

# ══════════════════════════════ BASELINES ══════════════════════════════
Y1_ENCH = ['Scythe','Crimson','Censer','Echoes','Staff','Redemption']
POKE_PUB = ['Scythe','Crimson','Echoes','Mandate','Stormsurge','Harmonic']

def run_baseline(name, keys, **kw):
    d = damage(keys, **kw); a = ally(keys, **{k:kw[k] for k in ('keystone','minors','second','minute') if k in kw})
    print(f"  {name:<34} oro {d['st']['gold']:>6} · AP {d['ap']:>4.0f} · AH {d['ah']:>3.0f} | "
          f"Q-hit {d['q_dmg']:>4.0f} · Q-DPS {d['q_dps']:>4.0f} · R {d['r_dmg']:>5.0f} · DPS {d['total']:>4.0f} | "
          f"E-shield {a['e_shield']:>5.1f} · R-heal {a['r_heal']:>5.1f} · shld/min {a['shield_per_min']:>5.0f} · ADC+ {a['adc_dps_add']:>4.0f}")
    return d, a

if __name__ == '__main__':
    OUT=[]; import builtins; _p=builtins.print
    def print(*a, **k):
        s=' '.join(str(x) for x in a); OUT.append(s); _p(s, **k)

    print('='*116)
    print('YUUMI AGRESIVA (batch5) — parche 7.3+7.3a+7.3b · nivel 15 · min 20 · runas base: Electro+Cheap(5s)+Transc+Coup | Gather')
    print('='*116)

    KW = dict(keystone='electro', minors=('cheap','transc','coup'), second='gather', minute=20.0)

    # [1] baselines (verificación contra fixtures del lab)
    print("\n[1] BASELINES (verificación: Y1 debe dar e_shield≈338.8 · r_heal≈650.7 · shld/min≈3 953):")
    run_baseline('Y1 ENCHANTER (lab)', Y1_ENCH, keystone='electro', minors=('cheap','transc','coup'), second='revitalize', minute=20.0)
    run_baseline('POKE-HÍBRIDA PUBLICADA (corregida)', POKE_PUB, **KW)

    # [2] optimizaciones
    opt_a, mx_a = optimize(PESOS_AGRESIVA, label='AGRESIVA (daño .70 / aliado .21 / util .03+)', top=8, **KW)
    opt_g, _    = optimize(PESOS_GLASS,    label='GLASS (techo de daño puro, aliado 0)', top=4, **KW)
    opt_h, _    = optimize(PESOS_HIBRIDO,  label='HÍBRIDA (daño .40 / aliado .51)', top=4, **KW)

    # [3] tabla comparativa final (mismas métricas)
    print(f"\n[3] COMPARATIVA (min 20, MR 50 squishy / MR 150 tanque, Electro+Cheap 5 s):")
    rows = [('Y1 enchanter (baseline lab)', Y1_ENCH, dict(second='revitalize')),
            ('Poke-híbrida publicada', POKE_PUB, {}),
            ('⭐ ÓPTIMA AGRESIVA', list(opt_a[0][1]), {}),
            ('Glass puro (techo)', list(opt_g[0][1]), {}),
            ('Híbrida balanceada', list(opt_h[0][1]), {})]
    base_d, base_a = None, None
    for name, b, kwo in rows:
        kw2 = dict(keystone='electro', minors=('cheap','transc','coup'), second='gather', minute=20.0); kw2.update(kwo)
        d = damage(b, **kw2); a = ally(b, **{k:kw2[k] for k in ('keystone','minors','second','minute')})
        if base_d is None: base_d, base_a = d, a
        print(f"  {name:<30} {' + '.join(b[2:]):<52}")
        print(f"      Q-hit {d['q_dmg']:>4.0f} · Q-DPS {d['q_dps']:>4.0f} · R-burst {d['r_dmg']:>5.0f} · DPS-sost {d['total']:>4.0f} · vsTanque {damage(b, mr=150, enemy_hp=4500, **kw2)['total']:>4.0f}")
        print(f"      E-shield {a['e_shield']:>5.0f} ({(a['e_shield']/base_a['e_shield']-1)*100:+.0f} %) · R-heal {a['r_heal']:>5.0f} ({(a['r_heal']/base_a['r_heal']-1)*100:+.0f} %) · ADC+ {a['adc_dps_add']:>4.0f} ({(a['adc_dps_add']/max(1,base_a['adc_dps_add'])-1)*100:+.0f} %) · Helia/E {a['helia_per_e']:>4.0f} · team-amp {a['team_amp']*100:>3.0f} %")

    # [4] sensibilidades
    print("\n[4] SENSIBILIDADES (sobre la óptima agresiva):")
    b = list(opt_a[0][1])
    d0 = damage(b, **KW)
    for etiqueta, kw2 in [('R interp A (conservadora)', dict(r_interp='A')),
                          ('Q mejorada uptime 80 %', dict(q_enhanced_upt=0.8)),
                          ('Cheap Shot CD 7 s (pre-7.3b)', dict(cheap_cd=7.0)),
                          ('keystone Dark Harvest', dict(keystone='darkharvest')),
                          ('keystone Empowerment', dict(keystone='empower')),
                          ('keystone First Strike', dict(keystone='firststrike')),
                          ('keystone Phase Rush', dict(keystone='phaserush')),
                          ('secundaria Revitalize', dict(second='revitalize')),
                          ('min 14 (mid-game)', dict(minute=14.0))]:
        d2 = damage(b, **{**KW, **kw2})
        print(f"  {etiqueta:<38} DPS {d2['total']:>4.0f} ({(d2['total']/d0['total']-1)*100:+.1f} %) · Q {d2['q_dps']:>4.0f} · R {d2['r_dmg']:>5.0f}")
    for budget in (12000, 14000):
        t, _ = optimize(PESOS_AGRESIVA, budget=budget, top=1, label=f'(presupuesto {budget})', **KW)
        pass

    # [5] detalle de la óptima para el reporte
    print("\n[5] FICHA DE LA ÓPTIMA AGRESIVA:")
    d = damage(b, **KW); a = ally(b, **{k:KW[k] for k in ('keystone','minors','second','minute')})
    dT = damage(b, mr=150, enemy_hp=4500, **KW)
    print(f"  build: {' + '.join(b)} · oro {d['st']['gold']}")
    print(f"  AP {d['ap']:.0f} · AH {d['ah']:.0f} (cdr {d['cdr']*100:.0f} %) · Q-CD {d['q_cd']:.2f} s · R-CD {d['r_cd']:.1f} s · pen {d['st']['pen_f']:.0f}+{d['st']['pen_p']:.0f} %")
    print(f"  Q-hit {d['q_dmg']:.0f} (MR50) · R-burst {d['r_dmg']:.0f} · DPS sost {d['total']:.0f} · vs tanque {dT['total']:.0f}")
    print(f"  E-shield {a['e_shield']:.0f} · R-heal {a['r_heal']:.0f} · shld/min {a['shield_per_min']:.0f} · ADC+ {a['adc_dps_add']:.0f} · Helia {a['helia_per_e']:.0f}/E · pasiva {a['passive_heal']:.0f} hps")

    with open('model/yuumi_agresiva_resultados.txt','w',encoding='utf-8') as f: f.write('\n'.join(OUT)+'\n')
    _p('\n[salida guardada en model/yuumi_agresiva_resultados.txt]')
