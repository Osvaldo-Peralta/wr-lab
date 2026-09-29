# -*- coding: utf-8 -*-
"""
WR-LAB · Specs precargadas — lista de campeones del equipo (28-sep-2026, parche 7.3 + hotfix 7.3a)
====================================================================================
Datos: stats base de wr-meta.com (fichas en data/estructurada/campeones/*.md),
AS oficial del apéndice 7.3 (data/estructurada/champion_attack_speed_7.3.csv),
cambios 7.3 (cambios_campeones_7.3.md). dps_model.py convierte estos dicts en ChampSpec.

⚠️ CAMPOS PENDIENTES = verificar en juego antes de publicar un reporte:
   - attack_range no viene en wr-meta; marcado None donde no se pudo confirmar.
   - Volibear ad_growth: la página muestra "62 (56)" — growth real probablemente 3.5-5; VERIFICAR.
"""

SPECS = {
# ══════════════════════ PRINCIPALES DE DAÑO / CARRYS ══════════════════════
"yunara": dict(
    name="Yunara", roles=["ADC (Dragon)"], archetype="crit-aoe-hibrido",
    base_ad=58, ad_growth=3.0, base_as=0.65, as_ratio=0.65, base_bonus_as=0.23, as_per_lvl=0.032,
    ranged=True, attack_range=None,  # verificar (marksman; estimable ~575)
    self_as_buff=0.55,   # Q Spirit Unbound activo: +25/35/45/55% AS por 5s (consume cargas Unleash)
    aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0, uses_magnification=None,
    notes=("Pasiva Vow: críticos hacen +8% daño mágico extra (+8% por cada 100 AP — híbrida). "
           "Q activa: autos empoderadas +10-25 mágico on-hit y SPREAD físico 30% AD a cercanos; en "
           "Transcendent (R, 15s) el spread CRITEA si el auto crita → Runaan's+crítico sinérgico. "
           "7.3: pasiva 10%→8%; Q AS 25/35/45/55. Kraken 'Bring it Down' proca con su spread (nota oficial 7.3). "
           "Modelo: añadir término de spread como AoE condicional + on-hit mágico 10-25+20%AP."),
    model_terms_pending=["spread AoE con crit (Q activa/R)", "pasiva +8% mágico en críticos", "uptime de Q (~5s cada ~6 cargas)"]),

"kalista": dict(
    name="Kalista", roles=["ADC (Dragon)"], archetype="on-hit-ejecutor",
    base_ad=57, ad_growth=5.2, base_as=0.694, as_ratio=0.694, base_bonus_as=0.16, as_per_lvl=0.046,
    ranged=True, attack_range=None,  # verificar (~575)
    self_as_buff=0.0, aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0, uses_magnification=None,
    notes=("7.3: AD base 54→57, growth 5→5.2 (BUFF). AS por nivel 0.046 = el más alto del juego → "
           "escala AS 'gratis' (a lvl15 bonus de niveles ≈ +0.644). Pasiva Martial Poise: dash al atacar "
           "(kiting extremo; no puede atacar mientras se mueve... compensación). E Rend: stacks de lanza, "
           "detona % vida + slow, resetea con kill → ejecutor. Comunidad 7.3: Statikk Shiv 1.er ítem (energized on-hit). "
           "Modelo: término de E por ventana (stacks×AS) + reseteos. REPORTE COMPLETO: reportes/Kalista_WR_7.3_Build_Optimizada.md (build: Gunmetal+Guinsoo+WE+Terminus+BotRK+Runaan's)."),
    model_terms_pending=["E Rend por stack (ratios)", "uptime de dash (kiting = más DPS efectivo)", "Statikk bounce"]),

# ══════════════════════ JUNGLA / MID LANERS ══════════════════════
"diana": dict(
    name="Diana", roles=["Jungla", "Mid"], archetype="ap-assassin-AS (spellblade/Nashor)",
    base_ad=52, ad_growth=3.64, base_as=0.694, as_ratio=0.694, base_bonus_as=0.15, as_per_lvl=0.008,
    ranged=False, attack_range=None,
    self_as_buff=0.65,   # Moonsilver Blade: +30-100% AS 4s tras habilidad (uptime alto en combo; usar 0.65 conservador)
    aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0, uses_magnification=False,
    notes=("Pasiva: tras habilidad +30-100% AS 4s Y cada 3.er golpe = 20+15/nivel + 50% AP mágico en AoE. "
           "Ratio 0.694 alto + AS condicional enorme → Nashor's Tooth (7.3: 50% AS/80 AP) y Dusk and Dawn core; "
           "Infinity Orb (crítico de habilidades 20% vs <40% HP) synergiza con burst. Comunidad: Dusk and Dawn 1.º. "
           "Modelo: rotación Q→E→W→R + autos. REPORTE COMPLETO: reportes/Diana_WR_7.3_Build_Optimizada.md (hallazgo clave: Lethal Tempo > Empowerment; Nashor+D&D core)."),
    model_terms_pending=["rotación de habilidades (ratios AP)", "proc cada 3er golpe (AP)", "uptime real de Moonsilver"]),

"volibear": dict(
    name="Volibear", roles=["Jungla", "Top"], archetype="fighter-hibrido-AS",
    base_ad=62, ad_growth=None,  # ⚠️ wr-meta muestra "62 (56)" — VERIFICAR growth real antes de modelar
    base_as=0.7, as_ratio=0.7, base_bonus_as=0.05, as_per_lvl=0.014,
    ranged=False, attack_range=None,
    self_as_buff=0.25,   # The Relentless Storm: +5% AS por stack ×5 (dañar con auto/habilidad)
    aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0, uses_magnification=False,
    notes=("7.3 nerf: pasiva relámpago 11-80+40%AP → 12-68+40%AP (a 5 stacks las garras encienden = chain on-hit). "
           "W Frenzy: maul + AS/curación al morder marcado. Hibrido AD/AP: items = Dusk and Dawn/Terminus/híbridos AP-fighter. "
           "Modelo: on-hit de pasiva (40% AP) + autos; growth de AD pendiente de verificar."),
    model_terms_pending=["chain lightning pasiva (AP)", "W execute/heal", "verificar ad_growth"]),

"shyvana": dict(
    name="Shyvana", roles=["Jungla"], archetype="fighter-on-hit / AP-burst (dragón)",
    base_ad=62, ad_growth=4.6, base_as=0.638, as_ratio=0.638, base_bonus_as=0.25, as_per_lvl=0.012,
    ranged=False, attack_range=None,
    self_as_buff=0.0, aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0, uses_magnification=False,
    notes=("Q Twin Bite: doble golpe (100% + 20/40/60/80% AD) y los autos reducen su CD 0.5s → spellblade/on-hit. "
           "R dragon: stats bonus + E mejorada. Rutas: AD on-hit (BotRK/Guinsoo/Terminus — sin crit) o AP-burst de R. "
           "Modelo: Q como 'ataque doble' (aa_mult efectivo ~1.3-1.6 según rank con CD refund por AS alta)."),
    model_terms_pending=["Q doble golpe + refund", "EAP vs AD route", "stats de forma dragón"]),

"chogath": dict(
    name="Cho'Gath", roles=["Jungla", "Mid", "Top"], archetype="ap-tank",
    base_ad=62, ad_growth=4.0, base_as=0.625, as_ratio=0.625, base_bonus_as=0.28, as_per_lvl=0.008,
    ranged=False, attack_range=None,
    self_as_buff=0.0, aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0, uses_magnification=False,
    notes=("E Vorpal Spikes: autos liberan picos en cono (daño mágico + slow) = aa_aoe mágico condicional. "
           "R Feast: stacks permanentes de vida + execute de minions/monstruos → escala vida infinita (Heartsteel/FGO). "
           "Jungla 7.3: Smite-burn scalea con stats → tanques limpian bien (cambio sistémico). "
           "Modelo: AP tank — rotación Q/W/E + vida como stat de daño (R/Heartsteel); no modelo de autos."),
    model_terms_pending=["E cono mágico", "vida de Feast (HP como tanqueo+daño R)", "clear de jungla 7.3"]),

"mordekaiser": dict(
    name="Mordekaiser", roles=["Top", "Jungla"], archetype="ap-juggernaut",
    base_ad=54, ad_growth=3.5, base_as=0.625, as_ratio=0.625, base_bonus_as=0.17, as_per_lvl=0.008,
    ranged=False, attack_range=None,
    self_as_buff=0.0, aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0, uses_magnification=False,
    notes=("Pasiva Darkness Rise: 3 golpes → aura de daño mágico sostenido + MS (on-hit de aura). "
           "R Realm of Death: duelo 1v1 robando stats → win-con de equipo. Items AP-fighter (Riftmaker/Liandry/Rylai/FGO). "
           "Modelo: aura pasiva (AP) + Q spammable; sin crit, sin AS relevante."),
    model_terms_pending=["aura Darkness Rise (dps AP)", "Q ratios", "stat steal de R"]),

"malphite": dict(
    name="Malphite", roles=["Top", "Jungla", "Support"], archetype="ap-tank / armor-stack",
    base_ad=58, ad_growth=3.64, base_as=0.625, as_ratio=0.625, base_bonus_as=0.2, as_per_lvl=0.026,
    ranged=False, attack_range=None,
    self_as_buff=0.0, aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0, uses_magnification=False,
    notes=("Meta 7.3: WR 52.17%, BAN 21.89% — el tanque más respetado. Armadura = daño: W pasiva +25-40% armor, "
           "W activa cono 20-50+20%AD+20%ARMOR (primer golpe +40%/40%), E 60-210+45%AP+45%ARMOR + slow de AS 35-50%. "
           "P Granite Shield: 11% vida máx fuera de combate. Iceborn: campo crece con armadura. Base armor 49(+5) = 119 lvl15. "
           "TAMAÑO: solo de ítems (Gargoyle activo, Twinguard, Sterak's, Mantle) — ver metodologia/ESCALADO_DE_TAMANIO.md. "
           "Comunidad: Iceborn → Plated/Mercury T3 → Thornmail → Zeke's → Gargoyle; Grasp+Demolish+Second Wind+Overgrowth."),
    model_terms_pending=["W pasiva (% armor: ¿bonus o total? verificar)", "E slow-AS al DPS enemigo (defensa)", "R engage value"]),

# ══════════════════════ SOPORTES / MAGOS (modelo de autos NO aplica) ══════════════════════
"yuumi": dict(
    name="Yuumi", roles=["Support"], archetype="enchanter-attach",
    base_ad=50, ad_growth=3.64, base_as=0.625, as_ratio=0.625, base_bonus_as=0.2, as_per_lvl=0.006,
    ranged=True, attack_range=None, self_as_buff=0.0, aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0,
    notes=("CORREGIDO (verificado en ficha): en WR Yuumi SÍ compra botas (Ionian → Crimson Lucidity T3). "
           "Análisis por VALOR ALIADO: Heal&Shield Power × uptime de E/Q, maná. Attachada = intargeteable → CERO stats defensivos valen. "
           "Items 7.3 clave: Ardent Censer (2400g, +30% AS y +25 on-hit al aliado = +244 DPS a un ADC típico), "
           "Echoes of Helia, Staff of Flowing Waters, Redemption/Mikael's/Diadem. Best Friend: +8-11% HSP y bonus en Q/R. "
           "⚠️ 7.3a NERF: W Best Friend HSP 8-11+0.02%AP → 6-9+0.01%AP (E-shield ~339→338, build intacta). "
           "REPORTE COMPLETO: reportes/Yuumi_WR_7.3_Build_Optimizada.md"),
    model_terms_pending=["E heal/shield por punto de HSP", "Q daño poke", "economía de maná", "mejor portador (ADC aliado)"]),

"karma": dict(
    name="Karma", roles=["Support", "Mid"], archetype="enchanter-poke",
    base_ad=58, ad_growth=3.64, base_as=0.625, as_ratio=0.625, base_bonus_as=0.2, as_per_lvl=0.0135,
    ranged=True, attack_range=None, self_as_buff=0.0, aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0,
    notes=("Mantra (R) empodera Q/E/W: poke + shield/heal + MS. Support: HSP + haste (Echoes of Helia 2400, "
           "Ardent Censer, Staff of Flowing Waters, Shurelya's); Mid: AP poke (Luden's/Stormsurge/Horizon Focus). "
           "Uptime de E-Mantra = métrica clave (haste items). REPORTE COMPLETO: reportes/Karma_WR_7.3_Build_Optimizada.md (hallazgo: Imperial Mandate = +7% team dmg)."),
    model_terms_pending=["Q/RE daño", "E/RE escudo por HSP", "rotación con haste"]),

"seraphine": dict(
    name="Seraphine", roles=["Support", "Mid"], archetype="enchanter-mage",
    base_ad=52, ad_growth=3.64, base_as=0.699, as_ratio=0.699, base_bonus_as=0.12, as_per_lvl=0.017,
    ranged=True, attack_range=None, self_as_buff=0.0, aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0,
    notes=("Cada 3.ª habilidad = doble cast (pasiva) → haste es su stat multiplicador; W cura/escudo en AoE, "
           "E root, R charm en línea. Support: Echoes of Helia/Diadem/Ardent/Staff; Mid: AP + haste. "
           "Sinergia 7.3: Ardent Censer más barato (2400) y Echoes rehecho (chain 30/35%)."),
    model_terms_pending=["pasiva doble-cast (haste efectivo)", "W AoE heal/shield", "R setup de teamfight"]),

"heimerdinger": dict(
    name="Heimerdinger", roles=["Mid", "Support"], archetype="mage-zona (turrets)",
    base_ad=54, ad_growth=3.5, base_as=0.625, as_ratio=0.625, base_bonus_as=0.2, as_per_lvl=0.01,
    ranged=True, attack_range=None, self_as_buff=0.0, aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0,
    notes=("Q turrets = su DPS real (escala AP; las torretas aplican on-hit?). Zona + waveclear: Liandry's/Rylai's/"
           "Cryptbloom; 7.3 relevantísimo: torretas ENEMIGAS con 7000 HP y cristales — su push de oleadas con "
           "turrets + Crystalline Overgrowth = presión de mapa única. Verificar si sus torretas detonan cristales."),
    model_terms_pending=["DPS de torretas (AP)", "E grenade setup", "push con minions 7.3"]),
}

# Roles repetidos (Diana/Cho'Gath) usan el mismo spec; la diferencia jungla/mid va en runas-summoners-orden de items
ROLE_VARIANTS = {
    "diana_jungla":  dict(base="diana",  summoners="Smite+Flash", runes="Lethal Tempo o Conqueror; jungla: Smite upgrades 600→1000→1400 (7.3)"),
    "diana_mid":     dict(base="diana",  summoners="Flash+Ignite/Barrier", runes="Lethal Tempo/Electrocute; First Strike greedy"),
    "chogath_jungla":dict(base="chogath", summoners="Smite+Flash", runes="Grasp/Aftershock-like; Feast stacks tempranas; burn de Smite scalea con HP (7.3)"),
    "chogath_mid":   dict(base="chogath", summoners="Flash+Ignite/TP", runes="Grasp; E-push; R execute"),
    "volibear_jungla":dict(base="volibear", summoners="Smite+Flash", runes="Lethal Tempo/Conqueror"),
    "volibear_top":  dict(base="volibear", summoners="Flash+Ignite/TP", runes="Conqueror/Grasp"),
}
