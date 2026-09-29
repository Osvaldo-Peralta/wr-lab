# -*- coding: utf-8 -*-
"""
WR-LAB · Modelo de DPS generalizado — Wild Rift 7.3
====================================================
Motor matemático reutilizable: el mismo con el que se derivó la build de Jinx
(reportes/Jinx_WildRift_7.3_Build_Optimizada.md), parametrizado por campeón.

USO RÁPIDO
    python3 model/dps_model.py            # demo con Jinx: reproduce las tablas del reporte
    from dps_model import *               # como librería para otro campeón (ver §NUEVO CAMPEÓN)

CONVENIOS / SUPUESTOS (idénticos al reporte de Jinx):
    - SLOTS: Wild Rift = 6 slots TOTALES; las botas ocupan UNO. La mejora T2→T3 (min 10:00)
      ocurre EN EL MISMO SLOT: en una build final se lista la T3 (p.ej. Gunmetal), NUNCA
      T2+T3 como dos ítems. eval_build() valida esto automáticamente (validate_slots).
    - DPS pre-mitigación salvo que se pase armor>0.
    - LT y Alacrity a cargas máximas; buff propio de AS del campeón activo (p.ej. Pow-Pow x3).
    - Bala de Lethal Tempo escala con el AS bonus TOTAL (incluye base-bonus y niveles).
    - Los rayos de Runaan's NO heredan multiplicadores del autoataque del campeón (conservador).
    - Penetración % de ítems se SUMA (LDR 35 + Mortal 30 = 65).
    - Kraken promedia missing_hp% configurable (default 50%).
    - Magnification de C44 solo aplica si el campeón ataca a >=550 de rango (flag en spec).

FUENTES DE NÚMEROS: notas oficiales 7.3/7.2 + wr-meta.com 24-sep-2026 + HOTFIX 7.3a (29-sep-2026,
ver data/estructurada/cambios_7.3a.md). Items marcados "7.3a" ya incluyen el hotfix.
"""
from dataclasses import dataclass, field

# ---------------------------------------------------------------- constantes globales 7.3
AS_CAP        = 3.0      # 7.3: 2.5 -> 3.0
CRIT_DMG_BASE = 2.00     # 7.3: 175% -> 200%
CRIT_DMG_IE   = 2.30     # Infinity Edge
LT_MELEE_STACK, LT_RANGED_STACK = 0.08, 0.064   # 6 cargas
LT_BULLET_MIN, LT_BULLET_MAX    = 6, 24          # ranged 6-24 / melee 9-30 (aprox: usamos rango y mod)
LT_BULLET_SCALE = 0.0067                          # +0.67% por 1% de AS bonus (ranged; melee 1%)
ALACRITY_FULL   = 0.21                            # 3% + 18% (el ejemplo oficial de Caitlyn usa 18%)
KRAKEN_RANGED_L15, KRAKEN_MELEE_L15 = 168, 210
KRAKEN_MISSING_BONUS = 0.0075                     # +0.75% por 1% de vida faltante, máx +75%

# ---------------------------------------------------------------- spec de campeón
@dataclass
class ChampSpec:
    name: str
    base_ad: float          # AD nivel 1
    ad_growth: float        # AD por nivel
    base_as: float          # = Attack Speed Ratio en casi todos (apéndice oficial 7.3)
    as_ratio: float
    base_bonus_as: float    # "Base Bonus Attack Speed" del apéndice 7.3
    as_per_lvl: float       # "Attack Speed per Level" del apéndice 7.3
    ranged: bool = True
    attack_range: int = 575
    self_as_buff: float = 0.0        # AS bonusconditional en pelea (Jinx Pow-Pow x3 = 1.10)
    aa_mult: float = 1.0             # multiplicador del autoataque (Jinx cohetes = 1.12)
    aa_aoe: bool = False             # el auto golpea a varios (Jinx = True)
    aoe_max_targets: int = 4         # objetivo del splash que modelamos
    crit_dmg_mod: float = 1.0        # Jhin/Senna/Yasuo/Yone: 0.8-0.9 sobre el daño crítico
    uses_magnification: bool = False # True si siempre ataca a >=550 (Jinx con Fishbones)
    passive_burst_as: float = 0.0    # AS extra que rompe el cap (Get Excited 0.25) — informativo
    mana_pool_l1: float = 345; mana_growth: float = 49   # informativo (gestión de maná)
    notes: str = ""

CHAMPS = {
    "jinx": ChampSpec(
        name="Jinx", base_ad=58, ad_growth=4.0,          # 7.3: growth 4.5->4
        base_as=0.625, as_ratio=0.625, base_bonus_as=0.30, as_per_lvl=0.02,  # apéndice oficial 7.3
        ranged=True, attack_range=575,
        self_as_buff=1.10,           # Pow-Pow rank 4, 3 cargas
        aa_mult=1.12, aa_aoe=True,   # Fishbones 112% en área
        uses_magnification=True,     # rango cohetes 655-700 >= 550
        crit_dmg_mod=1.0, passive_burst_as=0.25,
        notes="W: 220+160%AD CD5s (~150 DPS extra, fuera del modelo). R: 450+120% bAD + 35% missing (7.3 nerf).",
    ),
    # ---- PLANTILLA para el próximo campeón (copiar y llenar desde data/estructurada/) ----
    # "nombre": ChampSpec(
    #     name="...", base_ad=?, ad_growth=?,            # cambios_campeones_7.3.md o wiki
    #     base_as=?, as_ratio=?, base_bonus_as=?, as_per_lvl=?,   # champion_attack_speed_7.3.csv
    #     self_as_buff=?,       # AS condicional de su kit (0 si no tiene)
    #     aa_mult=?, aa_aoe=?,  # modificadores del auto (1.0 default)
    #     crit_dmg_mod=?,       # 0.8 Jhin / 0.9 Yasuo-Yone-Senna / 1.0 resto
    #     uses_magnification=?, # True si su rango efectivo de pelea es >=550
    # ),
}

# ---------------------------------------------------------------- base de ítems (stats que importan al modelo)
@dataclass
class Item:
    key: str; gold: int; ad: float=0; ap: float=0; a_s: float=0; crit: float=0
    pen: float=0; ls: float=0; mr: float=0; armor: float=0; hp: float=0; ah: float=0; ms: float=0
    kraken: bool=False; magnification: bool=False; ie: bool=False
    runaan: bool=False; energized: float=0; onhit_flat: float=0
    onhit_pct_current: float=0; spellblade: float=0; giant_slayer: float=0
    execute_pct: float=0; comment: str=""

def I(key, gold, **kw): return Item(key=key, gold=gold, **kw)

ITEMS = {i.key: i for i in [
    # --- críticos / marksman (7.3) ---
    I("c44",       2900, ad=55, crit=25, magnification=True, comment="+0-10% dmg a distancia (max a 550); +100 rango post-takedown"),
    I("ie",        3400, ad=75, crit=25, ie=True, comment="crítico 200->230%"),
    I("runaan",    2650, a_s=40, crit=25, ms=4, runaan=True, comment="2 rayos 55% AD, critan y aplican on-hit"),
    I("ldr",       3300, ad=35, pen=35, crit=25, giant_slayer=12, comment="+12% vs >=1200 HP bonus"),
    I("mortal",    3000, ad=35, pen=30, crit=25, comment="Grievous Wounds 50%"),
    I("kraken",    2900, ad=45, a_s=35, ms=4, kraken=True, comment="cada 3er golpe 120-168 (rango) +missing HP"),
    I("rfc",       2650, a_s=40, crit=25, ms=4, energized=80, comment="Energized +80 mágico, +150 rango"),
    I("storm",     3000, ad=50, crit=25, a_s=20, energized=120, comment="Energized +120 mágico +45% MS"),
    I("bt",        3200, ad=75, ls=15, comment="overheal->escudo 165-345"),
    I("gale",      3100, ad=60, crit=25, ms=4, comment="dash+misiles 40-125+35% bAD (activo)"),
    I("shieldbow", 3000, ad=55, crit=25, comment="Lifeline: escudo 300-550 bajo 35% (70s)"),
    I("fiend",     2650, a_s=45, crit=25, ms=4, comment="20 ult haste; post-R 3 ataques +50%AS y crit garantizado (80% dmg crit; si ya critaba +15% true)"),
    I("collector", 3000, ad=50, pen=10, crit=25, execute_pct=5, comment="pen plana; ejecuta <5% (+25g)"),
    I("pd",        2650, a_s=40, crit=25, ms=7, comment="stacks 6%AS+1%MS x5; ya NO da AD en 7.3"),
    I("navori",    2650, a_s=40, crit=25, ms=4, comment="ataques -15% CDs básicos (validar mecánica)"),
    I("er",        3000, ad=50, crit=25, ah=20, spellblade=1.0, comment="Spellblade 135% AD base + 0-80 por crit (1.5s ICD)"),
    I("yuntal",    3100, ad=50, a_s=35, crit=25, comment="7.3a BUFF: AS 25->35; Flurry +35%AS CD25; crit 0->25% en 125 ataques"),
    I("manamune",  2900, ad=40, ah=15, comment="+2% mana como AD; Shock 1.5% mana (Muramana)"),
    # --- on-hit ---
    I("witsend",   2800, a_s=50, mr=45, onhit_flat=40, comment="+20% tenacidad"),
    I("terminus",  3000, ad=35, a_s=35, onhit_flat=30, pen=30, comment="stacks light/dark; pen cap 40%"),
    I("botrk",     3100, ad=40, a_s=30, ls=12, onhit_pct_current=6, comment="6% vida actual (min 15)"),
    I("guinsoo",   3000, ad=35, ap=30, a_s=30, onhit_flat=30, comment="cada 3er golpe aplica on-hit 2 veces"),
    I("statikk",   3000, ad=40, ap=40, a_s=30, ms=4, energized=60, comment="cadena 4-7 objetivos, aplica on-hit"),
    # --- defensa/utilidad ---
    I("scimitar",  3100, ad=45, mr=40, ls=12, comment="activo Quicksilver (CC cleanse)"),
    I("ga",        3200, ad=45, armor=40, comment="revivir"),
    I("maw",       3000, ad=55, mr=45, ah=10, comment="escudo vs daño mágico"),
    I("deathsdance",3300, ad=50, armor=45, ah=15, comment="7.3a: coste 3200->3300; Defy/Cauterize"),
    # --- botas (T1 / T2 / T3) ---
    # REGLA DE SLOTS: Wild Rift tiene 6 slots TOTALES y las botas ocupan UNO.
    # Las T3 son MEJORA EN EL MISMO SLOT de su T2 (disponibles desde el min 10:00), NO un ítem extra.
    # Convención del modelo: las listas de build = los 6 slots FINALES -> usar el nombre T3 (p.ej. "Gunmetal").
    # Los checkpoints tempranos usan la T2 (p.ej. "Berserker's"). NUNCA ambas en la misma lista.
    I("boots_speed",  400, comment="T1 base"),
    I("berserker", 1200, a_s=35, comment="T2 ADC; +45 MS; Blessed Blade 10 HP/golpe"),
    I("gunmetal",  2200, a_s=50, ls=5, comment="T3 de Berserker's (mismo slot, min 10:00, +1000g); +45 MS; Blessed 12/golpe; Noxian Gait 7% MS"),
    I("mercury_t", 1200, hp=150, mr=25, comment="T2; 30% tenacidad"),
    I("chainlaced",2200, hp=150, mr=30, comment="T3 de Mercury's (mismo slot); 30% tenacidad + escudo mágico"),
    I("plated",    1200, hp=150, armor=20, comment="T2; Block 10%"),
    I("armored_adv",2200, hp=150, armor=30, comment="T3 de Plated (mismo slot); Block 10% + escudo físico"),
    I("ionian",    1000, ah=15, comment="T2 caster"),
    I("crimson",   2000, ah=25, comment="T3 de Ionian (mismo slot); Noxian Haste"),
    I("boots_mana",1200, ap=25, comment="T2 AP (+8 pen plana)"),
    I("spellslinger",2200, ap=35, comment="T3 de Boots of Mana (mismo slot); +18 pen plana +8% pen; Big Bully"),
    I("boots_dynamism",1200, ad=15, pen=10, comment="T2 AD lethality"),
    I("armorcrusher",2200, ad=25, pen=12, comment="T3 de Dynamism (mismo slot); +6% pen; Cloudwalker"),
    I("gluttonous",1000, comment="T2 adaptive + omnivamp"),
    I("immortal_treads",2000, comment="T3 de Gluttonous (mismo slot); Now and Forever"),
]}

# ── Registro de botas y mapa de mejoras T2→T3 (MISMO SLOT) ──
BOOT_UPGRADES = {  # T3 -> T2 (misma familia, mismo slot)
    "gunmetal": "berserker", "chainlaced": "mercury_t", "armored_adv": "plated",
    "crimson": "ionian", "spellslinger": "boots_mana", "armorcrusher": "boots_dynamism",
    "immortal_treads": "gluttonous",
}
BOOTS_ALL = {"boots_speed"} | set(BOOT_UPGRADES.keys()) | set(BOOT_UPGRADES.values())
# alias legibles
ALIAS = {"C44":"c44","Hexoptics C44":"c44","IE":"ie","Infinity Edge":"ie","Runaan's":"runaan",
         "Runaan's Hurricane":"runaan","LDR":"ldr","Lord Dominik's":"ldr","Mortal Reminder":"mortal",
         "Kraken Slayer":"kraken","Kraken":"kraken","RFC":"rfc","Rapid Firecannon":"rfc",
         "Stormrazor":"storm","Bloodthirster":"bt","BT":"bt","Galeforce":"gale","Shieldbow":"shieldbow",
         "Fiendhunter":"fiend","Fiendhunter Bolts":"fiend","Collector":"collector","Phantom Dancer":"pd",
         "PD":"pd","Navori":"navori","Essence Reaver":"er","ER":"er","Yun Tal":"yuntal",
         "Wit's End":"witsend","WE":"witsend","Terminus":"terminus","BotRK":"botrk","Guinsoo":"guinsoo",
         "Statikk Shiv":"statikk","Mercurial Scimitar":"scimitar","Scimitar":"scimitar",
         "Guardian Angel":"ga","GA":"ga","Maw of Malmortius":"maw","Death's Dance":"deathsdance",
         "Berserker's Greaves":"berserker","Berserker's":"berserker","Gunmetal Greaves":"gunmetal",
         "Gunmetal":"gunmetal","Mercury's Treads":"mercury_t","Chainlaced Crushers":"chainlaced",
         "Plated Steelcaps":"plated","Armored Advance":"armored_adv","Ionian Boots":"ionian",
         "Ionian Boots of Lucidity":"ionian","Boots of Speed":"boots_speed",
         "Crimson Lucidity":"crimson","Crimson":"crimson","Boots of Mana":"boots_mana",
         "Spellslinger's Shoes":"spellslinger","Spellslinger's":"spellslinger",
         "Boots of Dynamism":"boots_dynamism","Armorcrusher Boots":"armorcrusher","Armorcrusher":"armorcrusher",
         "Gluttonous Greaves":"gluttonous","Immortal Treads":"immortal_treads","Immortal Treds":"immortal_treads"}

def validate_slots(items, final=True, strict=True):
    """
    VALIDADOR DE SLOTS — previene el error clásico 'Berserker's + Gunmetal como 2 ítems'.
    Reglas: (1) Wild Rift = 6 slots TOTALES; (2) las botas ocupan UNO; (3) la mejora T2→T3
    ocurre EN EL MISMO SLOT (min 10:00) y NO cuenta como ítem nuevo; (4) una build final
    = 1 botas + 5 ítems. Raises ValueError si la composición es ilegal.
    Devuelve (n_boots, n_items) normalizados.
    """
    keys = [resolve(x).key for x in items]
    boots = [k for k in keys if k in BOOTS_ALL]
    no_boots = [k for k in keys if k not in BOOTS_ALL]
    errs = []
    # misma familia T2+T3 a la vez = doble conteo del slot de botas
    for t3, t2 in BOOT_UPGRADES.items():
        if t3 in boots and t2 in boots:
            errs.append(f"'{t2}' y '{t3}' son el MISMO slot (T2→T3). Usa solo la T3 ('{t3}') en builds finales.")
    if len(boots) > 1 and not errs:
        errs.append(f"{len(boots)} botas distintas en la lista ({boots}) — solo existe 1 slot de botas.")
    if len(items) > 6:
        errs.append(f"{len(items)} entradas > 6 slots totales. ¿Contaste la mejora de botas como ítem aparte?")
    if final and not errs and len(items) != 6:
        errs.append(f"Build final con {len(items)} slots (deben ser 6 = 1 botas + 5 ítems). "
                    f"Si es un checkpoint temprano, llama con final=False.")
    if final and not errs and len(boots) != 1:
        errs.append("Toda build final necesita exactamente 1 botas (idealmente ya en su forma T3).")
    if errs and strict:
        raise ValueError("SLOTS ILEGALES:\n  - " + "\n  - ".join(errs))
    return len(boots), len(no_boots)

# ---- carga de specs precargadas (model/champspecs.py) ----
try:
    try:
        from champspecs import SPECS as _SPECS
    except ImportError:
        import os as _os, sys as _sys
        _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
        from champspecs import SPECS as _SPECS
    import dataclasses as _dc
    _defaults = {f.name: f.default for f in _dc.fields(ChampSpec)}
    for _k, _v in _SPECS.items():
        kw = {}
        for f in _dc.fields(ChampSpec):
            if f.name in _v and _v[f.name] is not None:
                kw[f.name] = _v[f.name]
            elif f.name not in _defaults or _defaults[f.name] is _dc.MISSING:
                kw[f.name] = 0 if f.type in ("float", "int", float, int) else ""
        # campos sin default obligatorio que falten -> 0 con aviso en notes
        for req in ("base_ad", "ad_growth", "base_as", "as_ratio", "base_bonus_as", "as_per_lvl"):
            kw.setdefault(req, 0.0)
        extra = {kk: vv for kk, vv in _v.items() if kk not in {f.name for f in _dc.fields(ChampSpec)}}
        if extra:
            kw["notes"] = kw.get("notes", "") + " || extra: " + "; ".join(f"{a}" for a in (extra.get("roles", []) + [extra.get("archetype", "")]))
        CHAMPS[_k] = ChampSpec(**kw)
except Exception as _e:   # el engine sigue funcionando solo con Jinx si falla la carga
    print(f"[dps_model] aviso: champspecs no cargado ({_e})")

def resolve(name): 
    return ITEMS[name] if name in ITEMS else ITEMS[ALIAS[name]]

# ---------------------------------------------------------------- núcleo matemático
def lvl_as_bonus(spec: ChampSpec, level: int) -> float:
    """AS bonus ganada por niveles (fórmula oficial 7.3): suma de as_per_lvl*(0.7+0.04*L), L=1..level-1."""
    return spec.as_per_lvl * sum(0.7 + 0.04*L for L in range(1, level))

def as_total(spec, items, level=15, lt=True, alacrity=ALACRITY_FULL, self_buff_on=True):
    ai = sum(resolve(x).a_s for x in items)/100.0
    lt_as = (LT_RANGED_STACK if spec.ranged else LT_MELEE_STACK)*6 if lt else 0
    B = (spec.base_bonus_as + lvl_as_bonus(spec, level) + ai + lt_as + alacrity
         + (spec.self_as_buff if self_buff_on else 0))
    raw = spec.base_as + spec.as_ratio * B
    return min(raw, AS_CAP), raw, B

def lt_bullet(spec, level, B):
    lo, hi = (6, 24) if spec.ranged else (9, 30)
    base = lo + (hi-lo)*(level-1)/14
    scale = LT_BULLET_SCALE if spec.ranged else 0.01
    return base * (1 + scale*B*100)

def eval_build(spec, items, level=15, targets=1, armor=0.0, tank=False,
               lt=True, alacrity=ALACRITY_FULL, missing_hp=50, enemy_hp=2200,
               self_buff_on=True, spellblade_uptime=1/1.5, validate=True, ad_extra=0.0):
    """Devuelve métricas de una build completa (lista de nombres/alias de ítems, botas incluidas).
    OJO: 'items' = SLOTS FINALES. Las botas ocupan 1 slot y su mejora T2→T3 es EN EL MISMO SLOT
    (usa el nombre T3, p.ej. 'Gunmetal'; NUNCA listes 'Berserker's'+'Gunmetal' juntos)."""
    if validate:
        validate_slots(items, final=(len(items) == 6))
    its = [resolve(x) for x in items]
    gold = sum(i.gold for i in its)
    ad   = spec.base_ad + spec.ad_growth*(level-1) + sum(i.ad for i in its) + ad_extra
    base_ad = spec.base_ad + spec.ad_growth*(level-1)
    crit = min(sum(i.crit for i in its), 100)/100.0
    pen  = min(sum(i.pen for i in its), 100)
    ls   = sum(i.ls for i in its)
    AS, raw_as, B = as_total(spec, items, level, lt, alacrity, self_buff_on)
    cdmg = (CRIT_DMG_IE if any(i.ie for i in its) else CRIT_DMG_BASE) * spec.crit_dmg_mod
    cmult = 1 + crit*(cdmg-1)
    magn = 1.10 if (spec.uses_magnification and any(i.magnification for i in its)) else 1.0
    amp  = 1 + (sum(i.giant_slayer for i in its)/100.0 if tank else 0)

    hit  = ad * spec.aa_mult * cmult * magn * amp
    d    = AS * hit
    for i in its:
        if i.kraken:
            base = (KRAKEN_RANGED_L15 if spec.ranged else KRAKEN_MELEE_L15) * (level/15)
            d += AS/3 * base * (1 + KRAKEN_MISSING_BONUS*missing_hp)
        if i.energized: d += AS/7 * i.energized
        if i.onhit_flat: d += AS * i.onhit_flat
        if i.onhit_pct_current: d += AS * max(15, i.onhit_pct_current/100*enemy_hp)  # sin cap vs campeones
        if i.spellblade: d += spellblade_uptime * (1.35*base_ad + 80*crit)
    bullet = AS * lt_bullet(spec, level, B) if lt else 0
    d += bullet

    aoe = 0.0
    if targets > 1:
        if spec.aa_aoe:
            aoe += hit * AS * (min(targets, spec.aoe_max_targets)-1)   # splash completo
        if any(i.runaan for i in its):
            aoe += AS * 0.55 * ad * cmult * amp * min(2, targets-1)   # 2 rayos (55% AD c/u)
    mit = 100/(100+armor*(1-pen/100)) if armor > 0 else 1.0
    heal = d*(ls/100)*mit
    keys = {resolve(x).key for x in items}
    if "gunmetal" in keys: heal += 12*AS      # Blessed Blade T3
    if "berserker" in keys: heal += 10*AS     # Blessed Blade T2

    return dict(gold=gold, AD=ad, AS=AS, raw_AS=raw_as, bonus_AS=B, crit=crit*100,
                crit_dmg=cdmg*100, pen=pen, dps1=d*mit, dpsN=(d+aoe)*mit,
                bullet=bullet, heal=heal, overcap=raw_as>AS_CAP)

def compare(spec, builds, level=15, scenarios=(("1v1",dict()),("3v3",dict(targets=3)),
            ("vs120arm",dict(armor=120)),("vsTanque",dict(armor=220,tank=True,enemy_hp=4500)))):
    rows = []
    for bname, items in builds.items():
        base = eval_build(spec, items, level)
        row = {"build": bname, "oro": base["gold"], "AD": round(base["AD"]),
               "AS": f"{base['AS']:.2f}" + ("*" if base["overcap"] else ""),
               "crit": round(base["crit"]), "pen": round(base["pen"]),
               "heal": round(base["heal"])}
        for sname, kw in scenarios:
            row[sname] = round(eval_build(spec, items, level, **kw)["dps1"] if sname!="3v3"
                               else eval_build(spec, items, level, **kw)["dpsN"])
        rows.append(row)
    return rows

# ---------------------------------------------------------------- demo: Jinx 7.3 (reproduce el reporte)
BUILDS_JINX = {
    "A2. Tu build viable (Ber+Kraken+RFC+Runaan+IE+BT)": ["Berserker's","Kraken","RFC","Runaan's","IE","BT"],
    "B. Meta comunidad (Gun+C44+Runaan+IE+LDR+Gale)":     ["Gunmetal","C44","Runaan's","IE","LDR","Galeforce"],
    "C. OPTIMA Kraken (Gun+C44+Runaan+IE+LDR+Kraken)":    ["Gunmetal","C44","Runaan's","IE","LDR","Kraken"],
    "D. OPTIMA BT (Gun+C44+Runaan+IE+LDR+BT)":            ["Gunmetal","C44","Runaan's","IE","LDR","BT"],
    "E. OPTIMA Scimitar (Gun+C44+Runaan+IE+LDR+Scim)":    ["Gunmetal","C44","Runaan's","IE","LDR","Scimitar"],
    "F. On-hit (Gun+Kraken+WE+Terminus+BotRK+Runaan)":    ["Gunmetal","Kraken","WE","Terminus","BotRK","Runaan's"],
}

if __name__ == "__main__":
    spec = CHAMPS["jinx"]
    print(f"=== WR-LAB · DPS {spec.name} nivel 15 (LT full, Alacrity full, {spec.notes[:40]}...) ===")
    print(f"{'BUILD':<52}{'oro':>6}{'AD':>5}{'AS':>6}{'crit':>5}{'pen':>4}{'1v1':>7}{'3v3':>8}{'vs120':>7}{'vsTanq':>8}{'heal':>6}")
    for row in compare(spec, BUILDS_JINX):
        print(f"{row['build']:<52}{row['oro']:>6}{row['AD']:>5}{row['AS']:>6}{row['crit']:>5}"
              f"{row['pen']:>4}{row['1v1']:>7}{row['3v3']:>8}{row['vs120arm']:>7}{row['vsTanque']:>8}{row['heal']:>6}")
    print("(* = AS cruda excede el tope 3.0)")
    print()
    print("=== Chequeo de leyes (Jinx) ===")
    _,raw,B = as_total(spec, ["Gunmetal","C44","Runaan's","IE","LDR","Kraken"])
    need = (AS_CAP/spec.base_as - 1) - (spec.base_bonus_as + lvl_as_bonus(spec,15) + LT_RANGED_STACK*6 + ALACRITY_FULL + spec.self_as_buff)
    print(f"AS de ítems necesaria para cap 3.0 exacto: {need*100:.1f}%  | build C cruda: {raw:.3f}")
    print(f"Con Get Excited (+{spec.passive_burst_as:.0%}): {spec.base_as*(1+B+spec.passive_burst_as):.3f} (rompe el cap por pasiva)")
