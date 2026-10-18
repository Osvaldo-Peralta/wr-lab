# -*- coding: utf-8 -*-
"""
WR-LAB · model/chogath_jungla.py — MÓDULO JUNGLA del motor batch4 (13/10/2026)
==============================================================================
EXTENSIÓN de model/chogath_model.py (NO la reemplaza): añade las métricas que
solo existen en jungla y re-optimiza con pesos jungla para responder:
  ¿la óptima de 6 slots late es la misma que en top? (las guías v1.3 dicen que sí)

MÉTRICAS NUEVAS:
  1. CLEAR: segundos por limpieza completa (proxy 4 campamentos = 9 500 HP,
     arm 30 / MR 30 — "increased monster resistances" 7.3, declarado).
     Incluye: rotación Q/W/E (E con base capada a 100 vs monstruos — D1),
     %-vida de E (dos modos: full / capado — sensibilidad D1), Immolate ×1.25
     (Hollow) o ×1.3 (Sunfire) vs monstruos, Torment (Liandry) 2 %/s, autos,
     y SMITE 7.3/7.3a: 2 casts/clear × execute (600/1 000/1 400 por minuto)
     + burn 3 ticks/cast = (162 a lvl 15 [7.3a: 22–162/s] + 10 % bAD + 12 % AP
     + 20 % armadura bonus + 20 % MR bonus + 3 % HP bonus) VERDADERO.
     Anguish/Heartsteel/Grasp NO aplican vs monstruos (solo campeones) — la
     build default tiene CERO ítems de clear: aquí se decide si eso importa.
  2. SUSTAIN DE CLEAR: daño recibido (monstruos no-épicos −50 % al smiter,
     proxy 500→250 dps) − Carnivore (10 kills × (16+2×lvl) HP) − regen.
  3. ÉPICOS: TTK de dragón (proxy 10 000 HP, 60/60) y Baron (15 000, 60/60)
     con Smite execute + R (1 200+50 %AP+10 % HP bonus verdadero) + Torment
     + rotación; umbral de robo Smite+R (ya existía).
  4. CHECKPOINTS con curva de ORO DE JUNGLA (7.3: menos oro base de monstruos,
     más en bonus de Smite → ~30 s más lenta que top; declarada):
     4:30→2 200 · 9:00→4 900 · 12:00→7 600 · 15:00→10 900 · 18:00→14 300 · 21:00→17 600.
  5. PESOS JUNGLA (declarados): los de tanque §A.5 ×0.75 + clear 0.13 + épicos 0.12.

SUPUESTOS NUEVOS (J1-J8):
  J1 Full clear = 4 camps, pool 9 500 HP, 10 unidades matables (Carnivore),
     arm/MR 30; se limpia con Q/W/E+autos+Smite (2 casts, 3 ticks de burn c/u).
  J2 %-vida de E vs monstruos: DEFAULT aplica completo (lectura agresiva de D1);
     sensibilidad "capado": todo el daño de E vs monstruos = 100 por pico.
  J3 Smite execute por minuto: 600 (<8'), 1 000 (8-14'), 1 400 (≥14') (A14).
  J4 Daño de monstruos no-épicos al jungler: 500 dps crudo ×0.5 (smiter) = 250.
  J5 Dragón 10 000 HP / Baron 15 000 HP, 60/60 resist (proxies — WR no publica;
     lo relativo importa, no lo absoluto).
  J6 Torment aplica a monstruos/épicos (2 % vida máx/s por objetivo quemado;
     en clear ~2 objetivos simultáneos).
  J7 Inmolate vs monstruos: Hollow ×1.25, Sunfire ×1.3 (texto oficial),
     golpea ~2 unidades promedio en campamento.
  J8 Curva de oro de jungla ≈ top −30 s (7.3 shift de oro a Smite bonus).
"""
import sys, itertools
sys.path.insert(0, __file__.rsplit('/',1)[0])
import chogath_model as M

def _stats(boot_key, item_keys, level=15, minute=20.0):
    """Agregador ligero (mismo orden que evaluate) para los términos de jungla."""
    B = M.BOOTS.get(boot_key) or M.BOOTS_T2[boot_key]
    its = [M.ITEMS[k] for k in item_keys] + [B]
    has = lambda f: any(f in i for i in its)
    bs = M.base(level)
    hp_i   = sum(i.get('hp',0) for i in its)
    armor  = bs['armor'] + sum(i.get('armor',0) for i in its)
    mr     = bs['mr'] + sum(i.get('mr',0) for i in its)
    ap     = sum(i.get('ap',0) for i in its)
    ah     = sum(i.get('ah',0) for i in its) + (10 if level >= 5 else 5)
    ad     = bs['ad'] + sum(i.get('ad',0) for i in its)
    mana   = bs['mana'] + sum(i.get('mana',0) for i in its)
    if has('absorb'): mr += 70*0.75
    awe_hp = 0.15*mana if has('awe') else 0.0
    gflat = 10*min(40, minute*2); oflat = min(100, minute*6)
    opct  = 0.03 if minute >= 13 else 0.0
    hs_growth = 0.9*max(0.0, minute-9.5)*45 if has('hs_proc') else 0.0
    return dict(its=its, has=has, bs=bs, hp_i=hp_i, armor=armor, mr=mr, ap=ap, ah=ah,
                ad=ad, mana=mana, awe_hp=awe_hp, gflat=gflat, oflat=oflat, opct=opct,
                hs_growth=hs_growth, cdr=ah/(100.0+ah))

def smite_exec(minute):  return 600 if minute < 8 else (1000 if minute < 14 else 1400)   # J3
def smite_burn_tick(st, level, S):
    bonusHP0 = st['hp_i'] + st['gflat'] + st['oflat'] + st['awe_hp'] + st['hs_growth']
    return (22 + (162-22)*min(1.0,(level-1)/14)          # 7.3a: 22-162/s por nivel
            + 0.10*max(0.0, st['ad']-st['bs']['ad']) + 0.12*st['ap']
            + 0.20*(st['armor']-st['bs']['armor']) + 0.20*(st['mr']-st['bs']['mr'])
            + 0.03*bonusHP0)

# Ranks por nivel con orden E→Q→W (R 5/9/13): L1 E1·L2 Q1·L3 E2·L4 E3·L5 R1·L6 E4·
# L7 Q2·L8 Q3·L9 R2·L10 Q4·L11 W1·L12 W2·L13 R3·L14 W3·L15 W4  (declarado)
Q_RANK = {1:0,2:1,3:1,4:1,5:1,6:1,7:2,8:3,9:3,10:4,11:4,12:4,13:4,14:4,15:4}
W_RANK = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:1,12:2,13:2,14:3,15:4}
Q_BASE = {0:0,1:80,2:135,3:190,4:245}
W_BASE = {0:0,1:80,2:130,3:180,4:230}
def e_rank_at(level): return {1:1,2:1,3:2,4:3,5:3,6:4}.get(level, 4)

def clear_metrics(boot_key, item_keys, level=12, minute=12.0, S=6, r_rank=2, e_rank=None,
                  e_pct_mode='full', pool_hp=9800.0, kills=10):  # 7.3b: raptors +HP (J9)
    """Segundos por full-clear (J1) y net-HP perdido."""
    st = _stats(boot_key, item_keys, level, minute)
    e_rank = e_rank or e_rank_at(level)
    F = M.feast(S, r_rank)
    bonusHP = st['hp_i'] + F['hp'] + st['gflat'] + st['oflat'] + st['awe_hp'] + st['hs_growth']
    maxHP = (st['bs']['hp'] + bonusHP)*(1+st['opct']); bonusHP = maxHP - st['bs']['hp']
    ap, cdr, AS = st['ap'], st['cdr'], st['bs']['AS']
    m_mag = 100/(100+30); m_phys = 100/(100+30)
    # rotación vs monstruos (skills golpean ~2 unidades en campamento — J1)
    E_BASE = {1:20,2:45,3:70,4:95}[e_rank]
    e_pct = (0.023+0.004*(e_rank-1)) + 0.006*S
    camp_hp_avg = pool_hp/4.0
    if e_pct_mode == 'capado':
        e_spike = min(E_BASE + 0.3*ap + e_pct*camp_hp_avg, 100 + 0.3*ap)   # J2 sens.
    else:
        e_spike = min(E_BASE,100) + 0.3*ap + e_pct*camp_hp_avg              # base capada (D1), %-vida full
    n_q_ps = 1/(6.0*(1-cdr)); n_w_ps = 1/(9.0*(1-cdr))
    spikes_ps = min(AS, 3/(4.0*(1-cdr)))
    q_dmg = Q_BASE[Q_RANK[level]] + (1.0*ap if Q_RANK[level] else 0)
    w_dmg = W_BASE[W_RANK[level]] + (0.7*ap if W_RANK[level] else 0)
    dps_clear = ((n_q_ps*q_dmg + n_w_ps*w_dmg)*2.0*m_mag                     # Q/W AoE ×2 unidades
                 + spikes_ps*e_spike*m_mag*2.0                               # E ×2 unidades
                 + AS*st['ad']*m_phys)                                       # autos (1 objetivo)
    # Immolate vs monstruos (J7)
    if st['has']('immolate'):
        kind = next(i['immolate'][0] for i in st['its'] if 'immolate' in i)
        imm = (25 + 0.01*bonusHP) if kind=='hollow' else (20 + 0.015*bonusHP)
        mult = 1.25 if kind=='hollow' else 1.3
        dps_clear += imm*mult*2.0*m_mag
    if st['has']('torment'):
        dps_clear += 0.02*camp_hp_avg*2.0*m_mag                              # J6
    # Smite: 2 casts (execute a un campamento grande cada uno) + burn 6 ticks
    smite_dmg = 2*smite_exec(minute) + 6*smite_burn_tick(st, level, S)
    t_clear = max(4.0, (pool_hp - smite_dmg)/max(1.0, dps_clear))
    # sustain: recibido − Carnivore − regen (Anguish/Heartsteel/Grasp = solo campeones)
    carn = kills*(16+2*level)
    taken = 250*t_clear                                                      # J4
    regen = (st['bs']['regen5']/5.0)*(1.0+sum(i.get('hpregen',0) for i in st['its']))*t_clear
    net_hp = taken - carn - regen
    return dict(t_clear=t_clear, dps_clear=dps_clear, smite_dmg=smite_dmg, net_hp=net_hp,
                burn_tick=smite_burn_tick(st, level, S))

def epic_metrics(boot_key, item_keys, level=15, minute=20.0, S=15, r_rank=3, e_rank=None,
                 e_pct_mode='full', boss_hp=10000.0):
    """TTK de épico con todo (Smite execute + R monstruo + Torment + rotación)."""
    st = _stats(boot_key, item_keys, level, minute)
    e_rank = e_rank or e_rank_at(level)
    F = M.feast(S, r_rank)
    bonusHP = st['hp_i'] + F['hp'] + st['gflat'] + st['oflat'] + st['awe_hp'] + st['hs_growth']
    maxHP = (st['bs']['hp'] + bonusHP)*(1+st['opct']); bonusHP = maxHP - st['bs']['hp']
    ap, cdr, AS = st['ap'], st['cdr'], st['bs']['AS']
    m_mag = 100/(100+60)
    E_BASE = {1:20,2:45,3:70,4:95}[e_rank]
    e_pct = (0.023+0.004*(e_rank-1)) + 0.006*S
    e_spike = (min(E_BASE,100) + 0.3*ap + e_pct*boss_hp) if e_pct_mode=='full' else (100 + 0.3*ap)
    n_q_ps = 1/(6.0*(1-cdr)); n_w_ps = 1/(9.0*(1-cdr))
    spikes_ps = min(AS, 3/(4.0*(1-cdr)))
    q_dmg = Q_BASE[Q_RANK[level]] + (1.0*ap if Q_RANK[level] else 0)
    w_dmg = W_BASE[W_RANK[level]] + (0.7*ap if W_RANK[level] else 0)
    dps = (n_q_ps*q_dmg + n_w_ps*w_dmg + spikes_ps*e_spike)*m_mag
    if st['has']('immolate'):
        kind = next(i['immolate'][0] for i in st['its'] if 'immolate' in i)
        imm = (25 + 0.01*bonusHP) if kind=='hollow' else (20 + 0.015*bonusHP)
        dps += imm*(1.25 if kind=='hollow' else 1.3)*m_mag
    if st['has']('torment'): dps += 0.02*boss_hp*m_mag
    if st['has']('hs_proc'): pass
    burst = smite_exec(minute) + (1200 + 0.5*ap + 0.10*bonusHP)*1.10          # Smite + R (A3)
    dps += 3*smite_burn_tick(st, level, S)/10.0                                 # burn amortizado
    ttk = max(1.0, (boss_hp - burst)/max(1.0, dps))
    return dict(ttk=ttk, dps_epic=dps, burst=burst, steal=burst)

# ══════════════════════════════ PESOS JUNGLA ══════════════════════════════
PESOS_JG = dict(ehp_p=0.1125, ehp_m=0.1125, ehp_window=0.15, r_exec=0.1125,
                dps_fighter=0.075, dps_tank=0.075, dps_aoe=0.0375, hps=0.0375, util=0.0375,
                clear=0.13, epic=0.12)

def jg_metrics(boot_key, item_keys, S=15, r_rank=3, level=15, minute=20.0, e_pct_mode='full', **kw):
    r = M.evaluate(boot_key, item_keys, S=S, r_rank=r_rank, level=level, minute=minute, **kw)
    cm = clear_metrics(boot_key, item_keys, level=12, minute=12.0, S=6, r_rank=2, e_pct_mode=e_pct_mode)
    em = epic_metrics(boot_key, item_keys, level=level, minute=minute, S=S, r_rank=r_rank, e_pct_mode=e_pct_mode)
    r['clear'] = 100.0/cm['t_clear']        # inverso: más score = más rápido
    r['epic']  = 100.0/em['ttk']
    r['t_clear'] = cm['t_clear']; r['net_hp'] = cm['net_hp']; r['ttk_dragon'] = em['ttk']
    r['burn_tick'] = cm['burn_tick']
    return r

def optimize_jg(pesos=PESOS_JG, oro=17250, S=15, r_rank=3, top=5, e_pct_mode='full', label=""):
    cands = []
    for bk in ['ArmoredAdvance','Chainlaced','ImmortalTreads']:
        bg = M.BOOTS.get(bk, M.BOOTS_T2.get(bk))['g']
        for combo in itertools.combinations(M.TANK_POOL, 5):
            g = bg + sum(M.ITEMS[k]['g'] for k in combo)
            if g > oro or not M.exclusivo_ok(combo): continue
            cands.append((bk, combo))
    res = [(bk, cb, jg_metrics(bk, list(cb), S=S, r_rank=r_rank, e_pct_mode=e_pct_mode)) for bk, cb in cands]
    keys = list(pesos.keys())
    mx = {k: max(r[2][k] for r in res) for k in keys}
    scored = sorted(((sum(pesos[k]*(r[2][k]/mx[k]) for k in keys),)+r for r in res), reverse=True)
    print(f"\n{'='*118}\nOPT JUNGLA {label} — {len(cands)} hojas · pesos: tanque×0.75 + clear .13 + épicos .12 · %-vida E vs monstruos: {e_pct_mode}")
    for i,(sc,bk,cb,r) in enumerate(scored[:top],1):
        print(f"  #{i} {sc:.3f} | {r['gold']:>6.0f}g | {' + '.join([bk]+list(cb)):<62} | VENT {r['ehp_window']:>6.0f} · R {r['r_exec']:>5.0f} · DPSf {r['dps_fighter']:>4.0f} · clear {r['t_clear']:>4.1f}s · dragón {r['ttk_dragon']:>4.1f}s · netHP {r['net_hp']:>+5.0f}")
    return scored, mx

if __name__ == '__main__':
    OUT=[]
    import builtins
    _p = builtins.print
    def print(*a, **k):
        s=' '.join(str(x) for x in a); OUT.append(s); _p(s, **k)

    print('='*118)
    print("MÓDULO JUNGLA — Cho'Gath batch4 (extensión de chogath_model.py)")
    print('='*118)

    # [J-1] ¿La óptima top sigue siendo óptima con pesos de jungla?
    jg, mx = optimize_jg(label="(default, min 20, S=15)")
    top_opt = ('ArmoredAdvance', ('Heartsteel','ForceOfNature','Gargoyle','UnendingDespair','Twinguard'))
    for i,(sc,bk,cb,r) in enumerate(jg[:25],1):
        if (bk,cb)==top_opt or (bk,tuple(sorted(cb)))==(top_opt[0],tuple(sorted(top_opt[1]))):
            print(f"  → La óptima de TOP aparece en jungla en la posición #{i} (score {sc:.3f} vs #1 {jg[0][0]:.3f}, Δ {(sc/jg[0][0]-1)*100:+.1f} %)")
            break
    # métricas de jungla de la óptima top vs la óptima jungla
    r_top = jg_metrics(top_opt[0], list(top_opt[1]))
    print(f"\n  ÓPTIMA TOP evaluada como jungla: clear {r_top['t_clear']:.1f}s · dragón {r_top['ttk_dragon']:.1f}s · netHP {r_top['net_hp']:+.0f} · burn tick {r_top['burn_tick']:.0f} verdadero")

    # [J-2] Sensibilidad D1: %-vida de E capado vs monstruos (clear mucho más lento → ¿entran Hollow/Sunfire/Liandry?)
    optimize_jg(e_pct_mode='capado', label="(sensibilidad D1: E %-vida CAPADO vs monstruos)")

    # [J-3] Checkpoints con oro de JUNGLA (J8: ~30 s más lenta que top)
    print(f"\n{'='*118}\nCHECKPOINTS JUNGLA (oro J8; clear+épicos en el score desde CP2)")
    cps = [
      ('CPJ1 min 9:00 · lvl 8 · R1 · S=3 · ≤4 900 g · T2+1', dict(oro=4900, S=3, r_rank=1, level=8,  minute=9.0),  ['Plated','Mercurys','Gluttonous'], 1),
      ('CPJ2 min 12:00 · lvl 10 · R2 · S=6 · ≤7 600 g · T2+2', dict(oro=7600, S=6, r_rank=2, level=10, minute=12.0), ['Plated','Mercurys','Gluttonous'], 2),
      ('CPJ3 min 15:00 · lvl 13 · R3 · S=8 · ≤10 900 g · T3+3', dict(oro=10900, S=8, r_rank=3, level=13, minute=15.0), ['ArmoredAdvance','Chainlaced','ImmortalTreads'], 3),
      ('CPJ4 min 18:00 · lvl 14 · R3 · S=11 · ≤14 300 g · T3+4', dict(oro=14300, S=11, r_rank=3, level=14, minute=18.0), ['ArmoredAdvance','Chainlaced','ImmortalTreads'], 4),
    ]
    for etiqueta, kw2, boots, n_items in cps:
        cands=[]
        for bk in boots:
            bg = M.BOOTS.get(bk, M.BOOTS_T2.get(bk))['g']
            for combo in itertools.combinations(M.TANK_POOL, n_items):
                g = bg + sum(M.ITEMS[k]['g'] for k in combo)
                if g > kw2['oro'] or not M.exclusivo_ok(combo): continue
                cands.append((bk,combo))
        ev = {k:v for k,v in kw2.items() if k!='oro'}
        res=[(bk,cb,jg_metrics(bk,list(cb),fight=8.0,**ev)) for bk,cb in cands]
        keys=list(PESOS_JG.keys())
        mx2={k:max(x[2][k] for x in res) for k in keys}
        res_s=sorted(((sum(PESOS_JG[k]*(x[2][k]/mx2[k]) for k in keys),)+x for x in res),reverse=True)[:4]
        print(f"  {etiqueta}:")
        for i,(sc2,bk,cb,r) in enumerate(res_s,1):
            print(f"    #{i} {sc2:.3f} | {r['gold']:>5.0f}g | {' + '.join([bk]+list(cb)):<52} | HP {r['maxHP']:>5.0f} · R {r['r_exec']:>4.0f} · clear {r['t_clear']:>4.1f}s · netHP {r['net_hp']:>+5.0f}")

    # [J-4] Smite: cuánto alimenta la build al burn (Ley 7 jungla)
    print(f"\n{'='*118}\n[J-4] SMITE 7.3 — burn tick por build (verdadero/tick, 3 ticks × 2 casts por clear):")
    for etiqueta, b in [('Óptima (HS+FoN+Garg+UD+TW)', ('ArmoredAdvance',['Heartsteel','ForceOfNature','Gargoyle','UnendingDespair','Twinguard'])),
                        ('Publicada jungla 28/09', ('ArmoredAdvance',['Heartsteel','HollowRadiance','Liandry','ForceOfNature','Warmog'])),
                        ('Tanque puro armadura (Randuin+Thornmail)', ('ArmoredAdvance',['Heartsteel','Randuin','Thornmail','Gargoyle','Twinguard'])),
                        ('AP (Liandry+Riftmaker)', ('Chainlaced',['Liandry','Riftmaker','Gargoyle','UnendingDespair','Twinguard']))]:
        t = smite_burn_tick(_stats(b[0], b[1]), 15, 20.0)
        cm = clear_metrics(b[0], b[1], level=15, minute=20.0, S=15)
        print(f"  {etiqueta:<40} tick {t:>5.0f} · clear {cm['t_clear']:>4.1f}s · dragón TTK {epic_metrics(b[0], b[1])['ttk']:>4.1f}s · robo {epic_metrics(b[0], b[1])['steal']:>5.0f}")

    # [J-5] Curva de stacks JUNGLA actualizada (S por minuto con R en campamentos)
    print(f"\n{'='*118}\n[J-5] CURVA JUNGLA (R1 desde lvl 5 ~6:00; cap 6 con camps grandes ~min 10-11; épicos sin cap):")
    ROUTE_JG = [
      (6.0,  'Plated T2', 'Plated', [], 0, 6, 1),
      (9.0,  'Heartsteel', 'Plated', ['Heartsteel'], 3, 8, 1),
      (11.0, '⬆️T3', 'ArmoredAdvance', ['Heartsteel'], 5, 9, 2),
      (13.0, '+Unending', 'ArmoredAdvance', ['Heartsteel','UnendingDespair'], 6, 11, 2),
      (16.0, '+Twinguard', 'ArmoredAdvance', ['Heartsteel','UnendingDespair','Twinguard'], 8, 12, 3),
      (18.5, '+Gargoyle', 'ArmoredAdvance', ['Heartsteel','UnendingDespair','Twinguard','Gargoyle'], 10, 14, 3),
      (21.0, '+FoN', 'ArmoredAdvance', ['Heartsteel','UnendingDespair','Twinguard','Gargoyle','ForceOfNature'], 12, 15, 3),
    ]
    print(f"    {'min':>4} {'ítem nuevo':<14} {'lvl':>3} {'S':>2} {'R':>3} {'HP':>5} {'R champ':>7} {'R monstruo':>10} {'Smite+R':>8} {'clear':>6}")
    for (mn, nuevo, bk, cb, S, lvl, rr) in ROUTE_JG:
        r = M.evaluate(bk, cb, S=S, r_rank=rr, level=lvl, minute=mn, fight=6.0)
        cm = clear_metrics(bk, cb, level=lvl, minute=mn, S=S, r_rank=rr)
        print(f"    {mn:>4.0f} {nuevo:<14} {lvl:>3} {S:>2} R{rr}  {r['maxHP']:>5.0f} {r['r_exec']:>7.0f} {r['r_monster']:>10.0f} {r['smite_exec']:>8.0f} {cm['t_clear']:>5.1f}s")

    with open('model/chogath_jungla_resultados.txt','w',encoding='utf-8') as f:
        f.write('\n'.join(OUT)+'\n')
    _p('\n[salida guardada en model/chogath_jungla_resultados.txt]')
