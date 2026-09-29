# -*- coding: utf-8 -*-
"""
WR-LAB · Análisis batch 2: Kalista (on-hit), Diana (AP rotación), Yuumi/Karma (soportes)
+ cálculos del apéndice de TAMAÑO (Cho'Gath/Malphite/Shyvana). Parche 7.3.
Todas las fuentes: data/estructurada/*. Supuestos declarados en cada bloque.
"""
CAP = 3.0

def as_kalista(items_as, lt=0.384, alac=0.21, guinsoo_stacks=False):
    B = 0.16 + 0.644 + items_as + lt + alac + (0.32 if guinsoo_stacks else 0)
    return min(0.694*(1+B), CAP), 0.694*(1+B), B

def mit_phys(dmg, armor, pen=0): return dmg * 100/(100+max(0, armor*(1-pen/100)))
def mit_magic(dmg, mr, pen_pct=0, pen_flat=0): return dmg * 100/(100+max(0, mr*(1-pen_pct/100)-pen_flat))

# ══════════════════════════════ KALISTA ══════════════════════════════
# E Rend no critica (sin mención de crit en ficha). W = 19% max HP / 8s por objetivo (condicional Oathsworn).
# Guinsoo: cada 3er ataque aplica on-hit 1 vez额外 -> flat on-hit x4/3. Terminus dark: 30% pen (3 hits).
# Statikk: Energized cada ~4 ataques (Kalista gana 5 stacks/ataque), 60 mágico + bounces con on-hit.
K_ITEMS = {
 'Gunmetal':   dict(g=2200, ad=0,  as_=50, ls=5),
 'Statikk':    dict(g=3000, ad=40, as_=30, ap=40, energized=60),
 'Guinsoo':    dict(g=3000, ad=35, as_=30, ap=30, wrath=30, double=True),
 'Terminus':   dict(g=3000, ad=35, as_=35, shadow=30, pen=30),
 'Runaan':     dict(g=2650, ad=0,  as_=40, bolts=2),
 'WitsEnd':    dict(g=2800, ad=0,  as_=50, onhit=40, mr=45),
 'BotRK':      dict(g=3100, ad=40, as_=30, pct=6, ls=12),
 'LDR':        dict(g=3300, ad=35, crit=25, pen=35, gs=12),
 'C44':        dict(g=2900, ad=55, crit=25),
 'IE':         dict(g=3400, ad=75, crit=25),
 'Kraken':     dict(g=2900, ad=45, as_=35),
}
def kalista(items, armor=120, mr=50, ehp=2200, targets=1, oathsworn=True, level=15):
    its = [K_ITEMS[i] for i in items]
    gold = sum(i['g'] for i in its)
    ad = 57 + 5.2*(level-1) + sum(i.get('ad',0) for i in its)
    as_i = sum(i.get('as_',0) for i in its)/100
    guin = any(i.get('double') for i in its)
    AS, raw, B = as_kalista(as_i, guinsoo_stacks=guin)
    pen = max([i.get('pen',0) for i in its] or [0])
    # on-hit por golpe (fis->mag separados)
    oh_mag = sum(i.get('wrath',0)+i.get('shadow',0)+i.get('onhit',0) for i in its)
    mult_double = 4/3 if guin else 1.0
    pct_cur = sum(i.get('pct',0) for i in its)/100
    # auto (físico) + on-hit (mágico) + BotRK (físico)
    auto_phys = AS*ad + AS*pct_cur*ehp*0.9  # vida actual ~90% de max en pelea
    auto_mag  = AS*oh_mag*mult_double
    # Energized Statikk (~cada 4 ataques)
    en = sum(i.get('energized',0) for i in its)
    auto_mag += AS/4*en if en else 0
    # E Rend: ciclo 7s, lanzas = AS*4 (+1 por Q)
    n = max(1, AS*4)
    e_dmg = 75 + 0.70*ad + n*(42 + 0.57*ad)
    e_dps = e_dmg/7
    q_dps = (265 + 1.10*ad)/6.5
    w_dps = 0.19*ehp/8 if oathsworn else 0
    lt_bullet = 24*(1+0.0067*B*100)
    lt_dps = AS*lt_bullet
    # mitigación
    dps_phys = mit_phys(auto_phys + e_dps + q_dps + AS*pct_cur*ehp*0, armor, pen)
    dps_mag  = mit_magic(auto_mag, mr)
    dps_true_w = mit_phys(w_dps, 0) if False else w_dps  # W es mágico
    dps_mag += mit_magic(w_dps, mr)
    # LT bala = adaptiva (física aquí)
    dps_phys += mit_phys(lt_dps, armor, pen)
    # AoE: Runaan bolts (0.55AD + on-hit completo) + Statikk bounces
    aoe = 0
    if targets > 1:
        bolts = sum(i.get('bolts',0) for i in its)
        per_bolt = 0.55*ad + oh_mag*mult_double + pct_cur*ehp*0.9
        aoe += mit_phys(AS*per_bolt*min(bolts, targets-1)*0.55/0.55, armor, pen)*0  # (simplificado abajo)
        aoe = AS*min(bolts, targets-1)*(mit_phys(0.55*ad + pct_cur*ehp*0.9, armor, pen) + mit_magic(oh_mag*mult_double, mr))
        if en: aoe += AS/4*en*4*mit_magic(1, mr)  # 4 bounces extra aprox
    total = dps_phys + dps_mag + (aoe if targets>1 else 0)
    return dict(gold=gold, AD=ad, AS=AS, raw=raw, pen=pen, e_hit=e_dmg,
                single=dps_phys+dps_mag, multi=total, aoe=aoe,
                heal=(dps_phys+dps_mag)*sum(i.get('ls',0) for i in its)/100)

print("="*118)
print("KALISTA nivel 15 (LT+Alacrity full; E cada 7s con ~AS×4 lanzas; W 19% maxHP/8s con Oathsworn)")
print("="*118)
K_BUILDS = {
 'K1 Comunidad (Statikk+Guinsoo+Term+Runaan+WE)': ['Gunmetal','Statikk','Guinsoo','Terminus','Runaan','WitsEnd'],
 'K2 BotRK (saca Statikk)':                       ['Gunmetal','BotRK','Guinsoo','Terminus','Runaan','WitsEnd'],
 'K3 LDR anti-tanque (saca Statikk)':             ['Gunmetal','LDR','Guinsoo','Terminus','Runaan','WitsEnd'],
 'K4 CRIT (descarte teórico)':                    ['Gunmetal','C44','IE','Runaan','LDR','Kraken'],
 'K5 Single-target (sin Runaan/Statikk)':         ['Gunmetal','BotRK','Guinsoo','Terminus','Kraken','WitsEnd'],
}
print(f"{'BUILD':<48}{'oro':>6}{'AD':>5}{'AS':>6}{'pen':>4}{'1v1':>7}{'3v3':>8}{'vsTanq':>8}{'E-hit':>7}")
for n, b in K_BUILDS.items():
    r1 = kalista(b); r3 = kalista(b, targets=3); rt = kalista(b, armor=220, mr=150, ehp=4500)
    print(f"{n:<48}{r1['gold']:>6}{r1['AD']:>5.0f}{r1['AS']:>6.2f}{r1['pen']:>4.0f}{r1['single']:>7.0f}{r3['multi']:>8.0f}{rt['single']:>8.0f}{r1['e_hit']:>7.0f}")
print("\nCheckpoint nivel 11 (2 items, Berserker's): ")
for n,b in {'Statikk+Guinsoo':['Statikk','Guinsoo'],'Guinsoo+WE':['Guinsoo','WitsEnd'],'Statikk+Runaan':['Statikk','Runaan'],'C44+Runaan(crit)':['C44','Runaan']}.items():
    r = kalista(['Gunmetal' if False else 'Statikk']+[] if False else b, level=11, armor=90, mr=40, ehp=1800)
    # sin botas T3 (aún no, min 10 ok sí -> usar Gunmetal si >=10min; nivel 11 ~ 12min: incluir Gunmetal)
    r = kalista(['Gunmetal']+b, level=11, armor=90, mr=40, ehp=1800)
    print(f"  {n:<22} AD={r['AD']:.0f} AS={r['AS']:.2f} 1v1={r['single']:.0f} 3v3={kalista(['Gunmetal']+b, level=11, armor=90, mr=40, ehp=1800, targets=3)['multi']:.0f}")

# ══════════════════════════════ DIANA ══════════════════════════════
# Rotación sostenida (10s) + burst combo. Moonsilver: +30-100% AS 4s tras habilidad (uptime ~85% en pelea -> prom 0.65 efectivo sostenido, 1.0 en burst).
# Cada 3er auto: 65 + 0.5AP mágico AoE. Q 195+0.7AP/5s; E 160+0.3AP (reset w/ Moonlight: 2 casts/ciclo); W 3x(65+0.2AP)+escudo; R 440+0.8AP.
D_ITEMS = {
 'Spellslinger': dict(g=2200, ap=35, pen_f=18, pen_p=8, ah=0),
 'Crimson':      dict(g=2000, ah=25),
 'DuskDawn':     dict(g=3100, ap=60, hp=300, as_=20, ah=20, sb=0.75),   # spellblade 75% base AD +10%AP + cura
 'Nashor':       dict(g=2900, ap=80, as_=50, ah=15, gnaw=1.0),           # on-hit 15+20% bonus AP
 'Rabadon':      dict(g=3400, ap=130),
 'InfinityOrb':  dict(g=3100, ap=110, pen_f=15, crit_exec=0.2),
 'Zhonyas':      dict(g=3300, ap=110, armor=40),
 'Cryptbloom':   dict(g=3000, ap=75, pen_p=30, ah=20),
 'VoidStaff':    dict(g=3000, ap=95, pen_p=40),
 'Luden':        dict(g=2800, ap=100, ah=10, echo=1.0),
 'Stormsurge':   dict(g=2800, ap=90, pen_f=15, squall=1.0),
 'Malignance':   dict(g=2700, ap=90, ah=15),
 'CosmicDrive':  dict(g=3000, ap=70, hp=300, ah=25),
}
# v1.8: añadidos desde items_7.3.csv (Torment/Hypershot/GW sin modelar en la rotación: conservador)
D_ITEMS.setdefault('Morello',      dict(g=2650, ap=75, hp=300, ah=15))
D_ITEMS.setdefault('Rylai',        dict(g=2700, ap=65, hp=350))
D_ITEMS.setdefault('HorizonFocus', dict(g=2700, ap=80, ah=25))
D_ITEMS.setdefault('Liandry',      dict(g=3000, ap=70, hp=300))

def diana(items, ap_extra=0, keystone='empower', mr=80, pen_note=None, level=15, fight=10.0, burst=False):
    its = [D_ITEMS[i] for i in items]
    gold = sum(i['g'] for i in its)
    ap = sum(i.get('ap',0) for i in its) + ap_extra
    base_ad = 52 + 3.64*(level-1)
    haste = sum(i.get('ah',0) for i in its) + (15 if 'Legend: Haste' in (pen_note or '') else 0)
    cdr = haste/(100+haste)
    as_i = sum(i.get('as_',0) for i in its)/100
    moons = 0.65
    B = 0.15 + 0.008*(level-1) + as_i + moons + (0.384 if keystone=='lt' else 0) + (0.21 if keystone=='lt' else 0)
    AS = min(0.694*(1+B), CAP)
    pen_f = sum(i.get('pen_f',0) for i in its); pen_p = max(i.get('pen_p',0) for i in its) if any('pen_p' in i for i in its) else 0
    mrm = max(0, mr*(1-pen_p/100)-pen_f)
    mitm = 100/(100+mrm)
    # --- habilidades en ventana de fight ---
    q_n = max(1, round(fight/(5*(1-cdr))))
    q = q_n*(195+0.7*ap)
    e_n = q_n + 1     # E resetea con Moonlight de cada Q (+1 inicial)
    e = e_n*(160+0.3*ap)
    w_n = max(1, round(fight/(8.5*(1-cdr))))
    w = w_n*3*(65+0.2*ap)
    r = (440+0.8*ap) if burst or fight>=8 else 0
    # --- autos ---
    gnaw = sum(i.get('gnaw',0) for i in its)
    auto_phys = AS*base_ad*fight
    auto_mag = AS*(gnaw*(15+0.2*ap))*fight
    proc3 = (AS*fight/3)*(65+0.5*ap)
    sb_n = int(fight/1.5) if any(i.get('sb') for i in its) else 0
    sb = sb_n*(0.75*sum(i.get('sb',0) for i in its)*base_ad + 0.10*ap)
    # echo Luden / squall
    echo = (75 + 0.08*ap)*max(1,int(fight/9)) if any(i.get('echo') for i in its) else 0
    squall = (125+0.1*ap)*max(1,int(fight/25*4)) if any(i.get('squall') for i in its) else 0  # ~1 cada 2.5s de dmg
    total_mag = (q+e+w+r+auto_mag+proc3+sb+echo+squall)*mitm
    total_phys = auto_phys*100/(100+60)  # autos físicos vs ~60 armadura
    # keystone
    kbonus = 0
    if keystone=='empower':
        proc_n = int(fight/4)                      # proc cada 3 hits, ICD 4s
        emp = proc_n*165*mitm                      # daño adaptivo del proc (late ~165)
        total = (total_mag+total_phys+emp)*1.08    # amp 8% (uptime ~casi todo el fight)
        return dict(gold=gold, AP=ap, AS=AS, dps=total/fight, mr_eff=mrm,
                    burst=(440+0.8*ap+195+0.7*ap+2*(160+0.3*ap)+3*(65+0.2*ap))*mitm)
    if keystone=='lt':
        bul = 24*(1+0.0067*B*100)*AS*fight*mitm
        total_phys += bul
    if keystone=='conq':
        total_phys += AS*fight*30*100/(100+60)*0.6   # ~30 adaptivo (AD) a uptime 60%
        total_mag *= 1.0                              # + omnivamp 9% (sustain, no DPS)
    return dict(gold=gold, AP=ap, AS=AS, dps=(total_mag+total_phys)/fight, burst=(440+0.8*ap+195+0.7*ap+2*(160+0.3*ap)+3*(65+0.2*ap))*mitm, mr_eff=mrm)

print()
print("="*118)
print("DIANA nivel 15 — DPS sostenido (fight 10s, vs 80 MR squishy) y burst combo completo (R+Q+E×2+W×3)")
print("="*118)
D_BUILDS = {
 'D1 Comunidad (D&D,Orb,Zhonya,Rabadon,Luden)':      ['Spellslinger','DuskDawn','InfinityOrb','Zhonyas','Rabadon','Luden'],
 'D2 Nashor híbrida (D&D,Nashor,Rabadon,Zhonya,Crypt)':['Spellslinger','DuskDawn','Nashor','Rabadon','Zhonyas','Cryptbloom'],
 'D3 Burst puro (Luden,Rabadon,Orb,Stormsurge,Zhonya)':['Spellslinger','Luden','Rabadon','InfinityOrb','Stormsurge','Zhonyas'],
 'D4 Anti-tanque (Void Staff)':                       ['Spellslinger','DuskDawn','Rabadon','VoidStaff','Zhonyas','Cryptbloom'],
}
for ks in ['empower','lt','conq']:
    print(f"\n-- Keystone: {ks.upper()} --")
    print(f"{'BUILD':<52}{'oro':>6}{'AP':>5}{'AS':>6}{'MR-ef':>6}{'DPS10s':>8}{'burst':>8}")
    for n,b in D_BUILDS.items():
        r = diana(b, keystone=ks)
        print(f"{n:<52}{r['gold']:>6}{r['AP']:>5.0f}{r['AS']:>6.2f}{r['mr_eff']:>6.0f}{r['dps']:>8.0f}{r['burst']:>8.0f}")
print("\nDiana vs tanque (180 MR): D1 vs D4")
for n,b in [('D1',D_BUILDS['D1 Comunidad (D&D,Orb,Zhonya,Rabadon,Luden)']),('D4',D_BUILDS['D4 Anti-tanque (Void Staff)'])]:
    r = diana(b, mr=180); print(f"  {n}: DPS={r['dps']:.0f} MR efectiva={r['mr_eff']:.0f}")

# ══════════════════════════════ YUUMI ══════════════════════════════
# v1.8: diccionario expandido desde data/estructurada/items_7.3.csv (stats oficiales).
# Pasivas no modeladas en yuumi()/karma() quedan como flag inerte (comentario por ítem):
# el modelo de valor-aliado consume AP/HSP/haste; las pasivas de daño/amp se declaran pero
# no puntúan (conservador).
Y_ITEMS = {
 'Scythe':     dict(g=0,    ah=10),
 'Mandate':      dict(g=2600, ap=60, ah=20, mandate=1),      # CC marca: +7% dmg aliado (amp de equipo, no HSP)
 'Stormsurge':   dict(g=2800, ap=90, ah=0,  squall=1),       # +15 pen mágica (pen no entra en e_shield/r_heal)
 'HarmonicEcho': dict(g=2500, ap=40, hp=200, ah=20, harmonic=1),  # cura post-cast no modelada (conservador)
 'Morello':      dict(g=2650, ap=75, hp=300, ah=15, gw=1),
 'Rylai':        dict(g=2700, ap=65, hp=350, slow=1),
 'HorizonFocus': dict(g=2700, ap=80, ah=25, hypershot=1),
 'Liandry':      dict(g=3000, ap=70, hp=300, torment=1),
 'Crimson':    dict(g=2000, ah=25),
 'Censer':     dict(g=2400, ap=50, hsp=8),
 'Echoes':     dict(g=2400, ap=40, hp=200, ah=20, siphon=1),
 'Staff':      dict(g=2400, ap=50, hsp=8, ah=10, rapids=1),
 'Redemption': dict(g=2450, ap=40, hsp=8, ah=10, redempt=1),
 'Mikael':     dict(g=2500, hp=300, hsp=9, ah=15, cleanse=1),
 'Diadem':     dict(g=2400, hp=200, hsp=8, diadem=1),
 'Locket':     dict(g=2600, hp=200, armor=30, mr=30, ah=10, locket=1),
 'Shurelya':   dict(g=2500, ap=55, ah=20, shurelya=1),
 'Zeke':       dict(g=2400, hp=300, armor=25, mr=25, ah=10, zeke=1),
 'YordleTrap': dict(g=2400, hp=200, armor=20, mr=20, ah=15, trap=1),
}
def yuumi(items, revitalize=True, bf=True, adc_as_base=2.6, adc_dmg_per_hit=330,
          w_flat=None, w_ap_pct=0.01):
    # 7.3a NERF: W Best Friend HSP 8/9/10/11 % + 0.02 %/AP → 6/7/8/9 % + 0.01 %/AP (rank 5).
    # w_flat=None → valor del parche vigente (9 attach / 6 sin attach). Para reproducir el
    # baseline publicado pre-7.3a (E=339): w_flat=11, w_ap_pct=0.0 (ver update_reports.params_yuumi).
    its = [Y_ITEMS[i] for i in items]
    gold = sum(i['g'] for i in its)
    ap = sum(i.get('ap',0) for i in its)
    if w_flat is None: w_flat = 9 if bf else 6
    hsp = sum(i.get('hsp',0) for i in its) + w_flat + w_ap_pct*ap + (5 if revitalize else 0)
    haste = sum(i.get('ah',0) for i in its)
    # E shield rank4: 170+0.4AP, multiplicado por (1+HSP%)
    e_shield = (170+0.4*ap)*(1+hsp/100)
    e_cd = 9*100/(100+haste)
    # R heal total (BF): 7 olas x (52+0.08AP) x (1+HSP)
    r_heal = 7*(52+0.08*ap)*(1+hsp/100)
    # Q on-hit aliado: 22+0.05AP (5s, Q cd5 -> uptime ~100%)
    q_onhit = 22+0.05*ap
    # Censer: +30% AS y +25 on-hit mágico al ADC; Q de Yuumi: +22+5%AP on-hit al aliado (uptime ~100%)
    censer = 'Censer' in items
    # +30% AS sobre AS total ~2.6 del carry => ~+11.5% DPS (30/260); on-hit y Q-onhit por golpe
    adc_dps_add = (0.115*adc_as_base*adc_dmg_per_hit if censer else 0)
    adc_dps_add += adc_as_base*(25 if censer else 0) + adc_as_base*q_onhit
    # Echoes/Diadem/Redemption throughput
    echo_val = 0.30*e_shield if any(i.get('siphon') for i in its) else 0
    diadem_hps = 0.008*(1200)*1.0 if any(i.get('diadem') for i in its) else 0  # 0.8% mana max/s ~9.6
    redempt_burst = 350*(1+hsp/100)*0 + 350 if any(i.get('redempt') for i in its) else 0
    return dict(gold=gold, AP=ap, HSP=hsp, haste=haste, e_shield=e_shield, e_cd=e_cd,
                r_heal=r_heal, q_onhit=q_onhit, adc_dps_add=adc_dps_add,
                shield_per_min=e_shield*(60/e_cd), echo_val=echo_val, diadem_hps=diadem_hps)

print()
print("="*118)
print("YUUMI — valor por build (E shield, R heal total, DPS añadido al ADC carry [AS 2.6, 330 dmg/golpe], escudo/min)")
print("="*118)
Y_BUILDS = {
 'Y1 Amp-ADC (Censer,Echoes,Staff,Redemption)': ['Scythe','Crimson','Censer','Echoes','Staff','Redemption'],
 'Y2 Heal engine (Echoes,Staff,Diadem,Redempt)': ['Scythe','Crimson','Echoes','Staff','Diadem','Redemption'],
 'Y3 Anti-dive (Mikael,Locket,Censer,Echoes)':   ['Scythe','Crimson','Mikael','Locket','Censer','Echoes'],
 'Y4 AP greedy (Censer,Staff,Echoes,Shurelya)':  ['Scythe','Crimson','Censer','Staff','Echoes','Shurelya'],
 'Y5 Zeke (para comps de engage)':              ['Scythe','Crimson','Zeke','Censer','Echoes','Staff'],
}
print(f"{'BUILD':<46}{'oro':>6}{'AP':>5}{'HSP%':>5}{'E-shield':>9}{'E-cd':>6}{'R-heal':>8}{'ADC+DPS':>8}{'shld/min':>9}")
for n,b in Y_BUILDS.items():
    r = yuumi(b)
    print(f"{n:<46}{r['gold']:>6}{r['AP']:>5.0f}{r['HSP']:>5.0f}{r['e_shield']:>9.0f}{r['e_cd']:>6.1f}{r['r_heal']:>8.0f}{r['adc_dps_add']:>8.0f}{r['shield_per_min']:>9.0f}")

# ══════════════════════════════ KARMA ══════════════════════════════
def karma(items, ap_extra=0, revitalize=True):
    its = [Y_ITEMS.get(i) or D_ITEMS.get(i) for i in items]
    gold = sum(i['g'] for i in its)
    ap = sum(i.get('ap',0) for i in its) + ap_extra
    haste = sum(i.get('ah',0) for i in its)
    hsp = sum(i.get('hsp',0) for i in its) + (5 if revitalize else 0)
    e_shield = (150+0.65*ap)*(1+hsp/100)
    e_mantra = (300+0.65*ap)*(1+hsp/100)
    e_cd = 7*100/(100+haste)
    q_dmg = (180+0.4*ap); q_mantra = (290+0.5*ap)+(160+0.5*ap)
    w_dmg = (110+0.4*ap)+(130+0.45*ap)
    r_dmg = 390+0.8*ap
    mantra_cad = 3  # casts por mantra
    casts_per_10s = 10/((6+7+15)/3*100/(100+haste))  # Q+E+W promedio
    mantras_10s = casts_per_10s/3
    return dict(gold=gold, AP=ap, HSP=hsp, haste=haste, e_shield=e_shield, e_mantra=e_mantra,
                e_cd=e_cd, q_mantra=q_mantra, mantras_10s=mantras_10s,
                dmg_10s=(casts_per_10s/3)*q_mantra + (casts_per_10s*2/3)*q_dmg*0.5)

KARMA_SUP = {
 'KS1 Mandate+Censer (team amp)':  ['Scythe','Crimson','Censer','Echoes','Staff','Redemption'],
 'KS2 Escudos puros':              ['Scythe','Crimson','Censer','Echoes','Staff','Mikael'],
 'KS3 Mandate (marcar +7% team)':  ['Scythe','Crimson','Censer','Echoes','Staff','Redemption'],
}
print()
print("="*118)
print("KARMA support — E shield / E-Mantra / cadencia de Mantras en 10s (con Imperial Mandate: +7% dmg team a marcados)")
print("="*118)
KB = {
 'KS1 Enchanter (Censer,Echoes,Staff,Redemption)': ['Scythe','Crimson','Censer','Echoes','Staff','Redemption'],
 'KS2 Mandate amp (Censer,Mandate*,Echoes,Staff)': ['Scythe','Crimson','Censer','Echoes','Staff','Redemption'],
}
print(f"{'BUILD':<50}{'oro':>6}{'AP':>5}{'HSP%':>5}{'E-shield':>9}{'E-Mantra':>9}{'E-cd':>6}{'mantras/10s':>12}")
for n,b in KB.items():
    r = karma(b)
    print(f"{n:<50}{r['gold']:>6}{r['AP']:>5.0f}{r['HSP']:>5.0f}{r['e_shield']:>9.0f}{r['e_mantra']:>9.0f}{r['e_cd']:>6.1f}{r['mantras_10s']:>12.1f}")
print("\nKARMA mid (comunidad):", end=" ")
rm = karma(['Spellslinger','Luden','Malignance','Rabadon','InfinityOrb','Zhonyas']) if False else None
# mid karma usa items AP puros:
items_mid = ['Spellslinger','Luden','Malignance','Rabadon','InfinityOrb','Zhonyas']
gold = sum(D_ITEMS[i]['g'] for i in items_mid); ap = sum(D_ITEMS[i].get('ap',0) for i in items_mid)
haste = sum(D_ITEMS[i].get('ah',0) for i in items_mid)
print(f"oro={gold} AP={ap:.0f} haste={haste} E-mantra shield={(300+0.65*ap)*(1.05):.0f} Q-mantra={(290+0.5*ap)+(160+0.5*ap):.0f}")

# ══════════════════════════════ TAMAÑO (SIZE) ══════════════════════════════
print()
print("="*118)
print("TAMAÑO — Cho'Gath Feast: HP bonus, rango y ejecucion R por stacks")
print("="*118)
print(f"{'stacks Feast':>12}{'HP bonus':>10}{'size +':>8}{'rango +':>9}{'R true dmg (AP150, HP items 1500)':>36}")
for st in [6, 10, 15, 22]:
    hp = st*160; size = min(6*st, 135); rng = min(7.7*st, 75)
    r_true = 600 + 0.5*150 + 0.10*(hp+1500)
    print(f"{st:>12}{hp:>10}{size:>7.0f}%{rng:>9.1f}{r_true:>36.0f}")
print()
print("MALPHITE armor-stacking (lvl 15, base armor 119):")
for combo, armor in [("Iceborn(50)+Thornmail(75)+Armored(30)", 119+155), ("+ W rank4 (+40% bonus armor)", 119+155+0.4*155), ("+ Gargoyle/Twinguard situacional", 119+155+62+50)]:
    e = 210+0.45*armor; w = 50+0.2*armor; w1 = 100+0.4*armor
    print(f"  armor~{armor:.0f} ({combo}): E={e:.0f} mág AoE | W golpe={w:.0f} | W primero={w1:.0f} | pasiva Granite={0.11*(690+130*14):.0f} escudo")
print()
print("GARGOYLE activo (escudo = 100 + 90% bonus HP) + SIZE:")
for bhp in [800, 1200, 1800, 2500]:
    print(f"  bonus HP {bhp}: escudo {100+0.9*bhp:.0f} (+aumento de tamaño 2.5s)")
print()
print("TWINGUARD Endurance (5 stacks): +20% size, +20% tenacidad, +30% armadura y +30% MR bonus")
for base_ar, base_mr in [(150,80),(250,120),(320,180)]:
    print(f"  con {base_ar} arm / {base_mr} MR -> {base_ar*1.3:.0f} arm / {base_mr*1.3:.0f} MR en pelea (mitigación {100/(100+base_ar)*100:.1f}% -> {100/(100+base_ar*1.3)*100:.1f}% dmg físico recibido)")
print()
print("HEARTSTEEL scaling (3.5% max HP de daño, 15% del daño como HP permanente, 20s CD/target):")
for hp in [2500, 3500, 5000, 7000]:
    dmg = 140+0.035*hp
    print(f"  con {hp} HP: golpe {dmg:.0f} -> +{0.15*dmg:.0f} HP permanente (por campeón cada 20s)")
