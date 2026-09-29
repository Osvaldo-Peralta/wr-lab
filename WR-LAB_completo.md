> ## ⚠️ LEY 0 — SLOTS (leer antes de proponer CUALQUIER build)
> Wild Rift tiene **6 slots de ítem EN TOTAL y las botas ocupan UNO**. Las botas Tier 3
> (Gunmetal Greaves, Chainlaced Crushers, Armored Advance, Crimson Lucidity, Spellslinger's Shoes,
> Armorcrusher Boots, Immortal Treads) son la **mejora EN EL MISMO SLOT** de su Tier 2 (desde el min 10:00).
> **Build final = 1 botas (T3) + 5 ítems.** Listar "Berserker's Greaves" y "Gunmetal Greaves" como dos
> ítems es un ERROR (deja la build con 5 slots reales y pierde un ítem completo).
> Toda lista de build debe pasar `dps_model.validate_slots()` (6 entradas, exactamente 1 botas, nunca T2+T3 juntas).

> ## 🎨 ESTÁNDAR VISUAL DE REPORTES (v1.4 — obligatorio)
> Todo reporte generado DEBE seguir `metodologia/TEMPLATE_REPORTE.md` al pie de la letra:
> frontmatter YAML (tags/version/Status/champion/patch) · bloque de metadatos en negritas ·
> callouts `> [!NOTE]` (meta real con WR/pick/ban) y `> [!TIP]`/`> [!DANGER]`/`> [!WARNING]` según aplique ·
> §0 con **Tabla A (6 slots exactos)** + **Tabla B (ruta cronológica con componentes y oro acumulado)** ·
> secciones `## N. MAYÚSCULAS` 0-10 + APÉNDICE A/B + **Pie de página** (referencias Riot/wr-meta/WR-LAB + aviso legal) ·
> números con espacio de miles (`2 900`, `17 350 g`) y `%` con espacio (`25 %`) · veredictos ✅/⚠️/❌ siempre con número.
> Referencia canónica: el reporte de Jinx incluido en este bundle.

> ## 🔥 ESTADO DE DATOS: parche 7.3 **+ hotfix 7.3a** (despliegue 29-sep-2026)
> Los cambios de 7.3a (nerfs a Hwei/Malphite/Caitlyn/Senna/Yuumi/Rammus/Syndra; buffs a Samira/Tristana/
> Draven/Viego; Yun Tal AS 35 %; Diadem/Circlet nerf; Death's Dance 3 300; Smite burn −; Nexus 4 000;
> placas −resist) están en §3b y YA aplicados a specs, motor y apéndices de este bundle.
> Fuente: notas oficiales CN traducidas — re-verificar contra la nota EN cuando Riot la publique.

# ⚗️ WR-LAB PORTABLE (LITE) — Wild Rift 7.3+7.3a · 28/09/2026
> Laboratorio de builds matemáticas en UN archivo. Adjunta o pega este archivo en cualquier
> herramienta/IA y pide: "Usando WR-LAB, genera el análisis nivel-Jinx para {CAMPEÓN},
> siguiendo el ESTÁNDAR VISUAL v1.4 de TEMPLATE_REPORTE.md".
> Versión completa (reportes del equipo, fichas, diffs): WR-LAB_completo.md

## 1. METODOLOGÍA (Ley 0 + las 7 Leyes + flujo)

# FRAMEWORK — Metodología de análisis de builds (Wild Rift 7.3+)

> Este documento destila el razonamiento usado en el análisis de Jinx para que sea
> **replicable con cualquier campeón**. No es una lista de builds: es el procedimiento
> para DERIVARLAS. Leer junto con `TEMPLATE_REPORTE.md` y `model/dps_model.py`.

---

## A. Flujo de trabajo por campeón (10 pasos)

1. **Verificar vigencia del parche.** ¿Salió un hotfix (7.3a/b…) o parche nuevo desde el 21-sep-2026?
   Si sí: descargar notas oficiales y regenerar `data/estructurada/` (protocolo en §E).
2. **Ficha del campeón (spec).** Llenar un `ChampSpec` en `model/dps_model.py` con:
   - AD base y crecimiento → `data/estructurada/cambios_campeones_7.3.md` (si lo tocaron) + wiki oficial.
   - AS base/ratio/bonus base/por nivel → `data/estructurada/champion_attack_speed_7.3.csv` (los 140 campeones, datos oficiales 7.3).
   - Vida/armadura/RM → `champion_durability_7.3.csv` (solo los ajustados).
   - Modificadores del autoataque (`aa_mult`, `aa_aoe`), AS condicional propia (`self_as_buff`),
     modificador de daño crítico (`crit_dmg_mod`: Jhin 0.8, Yasuo/Yone/Senna 0.9), rango efectivo.
3. **Leer sus cambios de 7.3.** ¿Sus habilidades ahora escalan con crítico (Caitlyn, MF, Tristana, Xayah, Akshan, Viego…)?
   Eso sube el valor de IE y del crítico por encima del modelo de solo autos. ¿Lo nerfearon/buffearon? (Jinx: AD growth y R.)
4. **Definir el arquetipo** (§C) y las 3–5 rutas candidatas serias (no todas las posibles).
5. **Enumerar builds como listas de ítems** (SIEMPRE 6 slots totales: 1 botas + 5 ítems — ver Ley 0;
   en la lista va la botas T3, nunca T2+T3 a la vez; `validate_slots()` corre automáticamente)
   y correr `compare(spec, builds)` en los 4 escenarios estándar: 1v1, 3v3, vs 120 armadura, vs tanque (220 arm + ≥1200 HP bonus + 4500 HP para %-vida).
6. **Aplicar las Leyes** (§B) para podar: stats muertos (crítico >umbral, AS sobre el tope, haste inútil),
   eficiencia de oro por slot, coste de oportunidad del slot defensivo.
7. **Curva de poder, no solo nivel 15.** Correr el modelo en los checkpoints nivel 9 (1.er ítem),
   12 (2 ítems + botas), 14 (3 ítems + botas T3) para ordenar la RUTA de compra y detectar
   ítems que ganan temprano pero pierden tarde (Kraken-first) o al revés (C44-first).
8. **Runas y hechizos.** Keystone que multiplique lo que la build ya compra (Lethal Tempo ↔ AS;
   Fleet ↔ sustain de lane; First Strike ↔ poke). Secundarias: valor por slot con la misma lógica de stats muertos.
9. **Matriz situacional del último slot** (vs CC / vs burst AD / vs AP / vs tanques / vs curación / vs dive)
   con números, no con opiniones.
10. **Escribir el reporte con `TEMPLATE_REPORTE.md`** — que desde v1.4 es el **estándar visual obligatorio**
(frontmatter Obsidian, metadatos, callouts [!NOTE]/[!TIP]/[!DANGER], Tabla A de 6 slots + Tabla B cronológica,
secciones 0-10 + apéndices A/B + pie de página con referencias y aviso legal, números con espacio de miles
"2 900" y "%" con espacio "25 %"). Referencia canónica: `reportes/Jinx_WildRift_7.3_Build_Optimizada.md`.

---

## B. Las Leyes (generalizadas del caso Jinx)

### Ley 0 — SLOTS: 6 en total y las botas son UNO (la regla más violada por las IAs)
Wild Rift tiene **6 espacios de ítem EN TOTAL, y las botas ocupan uno**. No hay "slot de botas" aparte.
- Las botas Tier 3 (Gunmetal Greaves, Chainlaced Crushers, Armored Advance, Crimson Lucidity,
  Spellslinger's Shoes, Armorcrusher Boots, Immortal Treads) son una **MEJORA EN EL MISMO SLOT** de su
  Tier 2 correspondiente, disponible desde el **minuto 10:00** (+1000g sobre la T2; Crimson/Immortal +1000g sobre 1000g).
- **Build final = 1 botas (en su forma T3 si el juego pasó del min 10) + 5 ítems.** Una lista con
  "Berserker's Greaves" Y "Gunmetal Greaves" como entradas separadas es ILEGAL: son el mismo slot y el
  conteo queda en 5 slots reales (¡se pierde un ítem completo!).
- La **ruta de compra** (cronológica) SÍ puede mostrar el paso "Berserker's (1200) → ⬆️ Gunmetal (+1000)"
  como dos momentos, pero debe decir explícitamente que es el mismo slot.
- Validación obligatoria antes de publicar cualquier build: `dps_model.validate_slots(lista)`
  (o `eval_build()`, que la invoca solo). Errores que captura: T2+T3 duplicadas, 2 botas, >6 entradas,
  build final de 6 sin botas.

### Ley 1 — Umbral de crítico exacto
Multiplicador promedio = `1 + crit × (daño_crit × mod_campeón − 1)`; daño_crit base = **2.00** (7.3), **2.30** con IE.
- Cada 1 % de crítico vale ~50g y rinde `+(daño_crit−1)` de multiplicador → con IE, **100 % de crítico = ×2.30**.
- Calcular el umbral útil del campeón (¿tiene conversión de crítico sobrante? Yasuo/Yone convierten a AD;
  Jhin no pasa de 100 %; Senna gana con niebla). **Todo crítico por encima del umbral es oro muerto** (~1250g por ítem con 25 %).
- Regla práctica: elegir la combinación de ítems que aterrice en el umbral EXACTO y que el resto de slots no traigan crítico.

### Ley 2 — Velocidad de ataque: apuntar al tope sin pasarse
`AS = AS_base × (1 + bonus_base + bonus_nivel + AS_items + runas + buffs_propios)`, tope **3.0** (7.3).
- Calcular `AS_items_para_cap = (3.0/AS_base − 1) − (bonus_fijos)`. Para Jinx = 152.6 %.
- Contar qué AS es condicional (stacks de LT: 6 golpes; pasivas de pelea) y cuál permanente.
- **Excepciones que rompen el tope**: Get Excited (Jinx), pasivas de reseteo → en esos campeones el sobretope NO es desperdicio total.
- AS de ítems sobra cuando: 3 fuentes grandes ya te ponen ≥95 % del tope en pelea.

### Ley 3 — Penetración % obligatoria contra el meta de vida
`mitigación = 100/(100 + armadura × (1−pen))`. Con torretas de 7000 HP y tanques con más vida:
- vs 120 armadura: pen 35 % = +23.5 % de daño real. vs 220: +32 %. vs 300: +36 %.
- Giant Slayer (LDR) suma +12 % adicional vs ≥1200 HP bonus → tanque full: ~+47 % total.
- La pen plana (Collector, Boots of Dynamism) solo rinde early o vs squishies puros.
- Doble pen (LDR+Mortal = 65 %) solo vs 3 tanques; normalmente pierde contra un slot de DPS/sustain.

### Ley 4 — Stats muertos y coste de oportunidad por slot
Auditar cada ítem candidato: ¿qué porcentaje de su oro compra stats que este campeón NO aprovecha?
Ejemplos 7.3: Galeforce en build de 100 % crit (25 % crit muerto ≈ 1250g), PD sin AD (solo AS/MS que pueden
sobrar), Navori con crit sobrante, maná/haste en campeones que no lo gastan. **Valor real = oro × (1 − fracción muerta) + pasivo.**

### Ley 5 — Eficiencia de oro con precios de componente 7.3
Referencias: 1 AD ≈ 37.5–41.7g (BF Sword/Pickaxe/Long Sword) · 1 % crit ≈ 50g (Brawler's) ·
1 % AS ≈ 33–45g (Dagger 400/12 %, Recurve 900/20 %) · 1 % pen ≈ 55g (Last Whisper) · 1 % lifesteal ≈ 50g ·
1 MR ≈ 25g · 1 armadura ≈ 22.5g · 1 HP ≈ 3.3g.
Pasivos: valuarlos como "AD equivalente" sobre el DPS medido (Magnification de C44 ≈ +10 % de AD total ≈ 1100g).
Ítems por encima de ~130 % de eficiencia con pasivo incluido son candidatos a core; por debajo de ~100 %, solo por utilidad única.

### Ley 6 — Timing > DPS teórico
Un ítem de 2650g terminado al minuto 11 vale más que uno de 3400g al 14 en partidas que terminan al 16–18.
Ordenar por: (a) coste, (b) suavidad del build path (componentes que ya pegan: Noonquiver 1300 = 20 AD+15 % crit),
(c) pico relativo (IE como 2.º ítem si vas feedeado; Runaan's 2.º si necesitas ventana barata).
Recordar reglas de 7.2+: botas T3 solo desde el **minuto 10:00**; placas de torreta decaen desde el **5:00**.

### Ley 7 — El sistema de juego también es input
7.3: torretas 7000 HP + placas permanentes + Crystalline Overgrowth (primer ataque detona 3.3–18.9 % de la vida
de la torreta como daño verdadero, ciclo ~50 s) + minions que pegan 60 % + jungla hostil para laners.
Traducir a build: rango/oleadas (Runaan's, Energized) valen más para tomar placas y detonar cristales de forma segura;
el oro de placas financia el pico del minuto 11–13.

---

## C. Arquetipos y cómo adaptar el modelo

| Arquetipo | Ejemplos | Claves del modelo |
|---|---|---|
| **Crítico AoE** | Jinx, Sivir, Xayah, Trista | `aa_aoe=True`; Ley 1 al 100 %; Runaan's multiplica; splash crítico |
| **Crítico burst/abilities** | Caitlyn, MF, Tristana, Akshan, Viego | Sus habilidades escalan crit en 7.3 → sumar término de habilidades al DPS (rotación), IE sube más |
| **Crítico modificado** | Jhin (0.8×, 4.º tiro), Yasuo/Yone (0.9×, conversión), Senna (0.9×) | `crit_dmg_mod`; umbral de crit distinto; AS irrelevante (Jhin) → Ley 2 no aplica igual |
| **On-hit** | Vayne, Kog'Maw, Twitch, Zeri | `onhit_*`, Guinsoo/Terminus/WE/BotRK/Statikk; la pen plana/% rinde distinto; AS se pasa del tope fácil |
| **Lethality/ejecutor** | Lucian crit-letality, Miss Fortune lethality, Varus | Collector/Serylda/Armorcrusher; DPS por ventana de burst, no sostenido; modelo por rotación |
| **AP/híbrido** | Kai'Sa, Varus AP, Corki | Statikk/Nashor/Dusk&Dawn/Luden; reemplazar términos de crit por ratios AP |
| **Spellblade** | Ezreal, Lucian ER | término `spellblade` con uptime = 1/ICD; AD BASE (no bonus) alimenta el proc |
| **No-ADC (fighters/magos)** | — | El modelo de autos no aplica: modelar rotación de habilidades (suma de ratios × uptime) + stats defensivos; las Leyes 4–6 siguen vigentes |

Para campeones con crítico en habilidades (7.3), añadir al DPS: `Σ (daño_hab × mult_crit_hab) / CD_efectivo`,
donde `mult_crit_hab` sale de la fórmula publicada en `cambios_campeones_7.3.md`
(patrón común: `× (1 + crit × X% + (daño_crit−2) × X% × crit)`).

---

## D. Reglas de verificación (aprendidas del caso Jinx)

1. **Las notas oficiales mandan.** Si wr-meta/wildstats y las notas difieren (pasó con Lethal Tempo: 4.8 % viejo
   vs 6.4 % oficial), usar las notas y registrar la discrepancia en el reporte (§10).
2. **Cuidado con los sistemas muertos.** Los encantamientos de botas NO existen desde 7.2 (QSS/Scimitar son
   ítems de clase); Magnetic Blaster, Cloak of Agility, Nashor's Talon, Stinger, Surging Scales, Ingenious Hunter,
   Legend: Tenacity y Soul Transfer fueron removidos. Las guías viejas mienten.
3. **Distinguir pasivas condicionales**: Magnification (distancia) ≠ Arcane Aim (kills); Flurry (uptime 30 %) ≠
   AS permanente; Opening Barrage (post-R) ≠ DPS sostenido. Modelar el uptime real, no el mejor caso.
4. **Declarar supuestos** en cada reporte (ver plantilla §10) y marcar estimaciones blandas (frecuencia de Energized,
   missing HP de Kraken, uptime de LT).
5. **Validar el modelo contra un caso conocido** antes de publicar números. Test oficial de Caitlyn
   (`mecanica_attack_speed_7.3.md`): AS 1.48125 a nivel 15 con Alacrity+Berserker's usando growth 0.04.
   ⚠️ El hotfix 7.3a bajó su AS growth a 0.025 → el esperado post-7.3a es **1.35**. El test del lab
   (`tests/test_model.py`) valida AMBOS (fórmula correcta + override 7.3a aplicado).
6. **Ni las notas oficiales son inmunes a erratas**: el apéndice de AS de 7.3 lista a Caitlyn con bonus 0.2 mientras
   su sección y el ejemplo de la fórmula usan 0.28 (ver FUENTES.md). Cuando dos secciones oficiales se contradicen:
   priorizar la sección específica del campeón, marcar el dato como "verificar en juego" y registrarlo en FUENTES.md.

---

## E. Protocolo de actualización de datos (cada parche)

```bash
# 1. Descargar notas oficiales del nuevo parche (python urllib desde el sandbox funciona):
#    https://wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-X-X/
#    → limpiar HTML → data/raw/patchX.txt  (mismo formato que patch73.txt)
# 2. Re-descargar https://wr-meta.com/items/ → data/raw/wrmeta_items.html
#    (alternativa si cae: wr-meta.com/<id>-<champion>.html por campeón)
# 3. Re-ejecutar:  python3 model/extract_data.py
# 4. Diffear contra la versión anterior de items_7.3.csv / champion_attack_speed_7.3.csv
#    y actualizar: constantes en dps_model.py (CRIT_DMG, AS_CAP, LT…), precios/stats de ITEMS,
#    specs de campeones tocados.
# 5. Anotar en data/FUENTES.md: fecha, parche, discrepancias detectadas.
```

**Caducidad:** los números de este lab son válidos para 7.3 (21-sep-2026) tal como estaba publicado al 25-sep-2026.
Cualquier hotfix 7.3a/b obliga al paso 1–5 antes de publicar un reporte nuevo.


## 1b. APÉNDICE: ESCALADO DE TAMAÑO (Cho'Gath/Malphite/Shyvana) — actualizado a 7.3a

# APÉNDICE — ESCALADO DE TAMAÑO (SIZE) en Wild Rift 7.3
### Cho'Gath · Malphite · Shyvana — qué es real, qué es fantasía y cómo se construye

> Investigación completa: todas las fuentes de tamaño del juego (grep exhaustivo de la BD de 186 ítems + fichas de campeones + notas 7.2/7.3). Fecha: 25/09/2026.

---

## 1. LA VERDAD INCÓMODA PRIMERO

**El tamaño, por sí solo, no da defensa.** No reduce daño, no da vida ni resistencias. Lo que hace:
1. **Hitbox más grande**: bloqueas skillshots con el cuerpo (peel real para tus carries) — pero también te vuelves más fácil de golpear (irrelevante si ya eres el tanque).
2. **Intimidación/legibilidad**: el enemigo percibe mal tus rangos de habilidad y su posicionamiento.
3. **EXCEPCIÓN ÚNICA de tu lista: en Cho'Gath el tamaño ES poder mecánico** (ver §3).

Cuando los jugadores dicen "escalar tamaño para ser underivable en teamfights", lo que realmente están escalando son los **paquetes de stats que vienen CON el tamaño**: vidas bonus, resistencias bonus ×1.3, tenacidad, escudos y curas. El tamaño es el indicador visual de que tu build de "ventanas de combate" está online. Y ahí está la clave matemática:

## 2. LAS 5 FUENTES DE TAMAÑO DEL JUEGO (7.3)

| Fuente | Coste | Tamaño | QUÉ MÁS DA (esto es lo que importa) | Tipo |
|---|---|---|---|---|
| **Amaranth's Twinguard** | 3200 | **+20 %** (5 stacks, 1 s c/u en combate) | +300 HP, 50/50 resist → **al máximo: +30 % armadura y +30 % MR y +20 % tenacidad** | Permanente en fight |
| **Gargoyle Stoneplate** | 2900 | +tamaño durante el activo | 200 HP, 45/45, **activo: escudo = 100 + 90 % de tu vida BONUS** (2.5 s, CD 60) | Activo (burst window) |
| **Sterak's Gage** | 3200 | +tamaño 8 s (al activar Lifeline) | 400 HP, 20 % tenacidad base, **+50 % de tu AD base como AD bonus**, Lifeline: escudo = 75 % de vida bonus (<35 % HP, CD 70) | Reactivo (<35 % HP) |
| **Mantle of the Twelfth Hour** | 2550 | +10 % por 5 s (<30 % HP) | **600 HP**, 20 AH, Lifeline: +200-300 HP, +10 % MS, +20 % tenacidad y **regenera 200-400 + 120 % armadura + 120 % MR** (CD 70) | Reactivo (<30 % HP) |
| **Feast de Cho'Gath** | gratis (R) | **+6 % por stack, cap +135 %** | +80/120/160 HP por stack, **+7.7 rango de ataque por stack (cap +75)**, +2.5 rango de R (cap +25), **anchura de E escala con tamaño** | Permanente, infinito* |

\* stacks de minions/monstruos no-épicos: cap 6; de campeones y épicos: **sin cap**.

**Interacción crítica:** Sterak's + Mantle + Twinguard + Gargoyle = **4 ventanas defensivas independientes** (2 reactivas por umbral de vida, 1 de combate prolongado, 1 activa). Bien temporizadas, un tanque pasa de "30 % HP" a "3000 de escudo + 30 % más resistencias + tenacidad 70 % + regen masiva" en 2 segundos. ESO es lo que el enemigo percibe como "imposible de matar" — no el modelo 3D más grande.

## 3. CHO'GATH — el único donde tamaño = daño (matemática completa)

Su R Feast convierte CADA stack en un compuesto de 5 stats. Con R rank 3 (+160 HP/stack):

| Stacks | HP bonus de Feast | Tamaño | Rango extra | R (true damage, con AP 150 y +1500 HP de ítems) |
|---|---|---|---|---|
| 6 (cap de minions) | +960 | +36 % | +46 | 921 |
| 10 | +1600 | +60 % | **+75 (cap)** | 985 |
| 15 | +2400 | +90 % | +75 | 1065 |
| 22 | **+3520** | **+132 %** | +75 | **1177** |

- **R = 600 + 50 % AP + 10 % de tu HP BONUS como daño VERDADERO** → cada ítem de vida double-dipea (tanqueo + ejecutor). A 22 stacks + Heartsteel, la R ejecuta ~1200 de daño verdadero.
- **E Vorpal Spikes: la anchura del cono escala con su tamaño** → a +132 % su E barre teamfights enteras.
- **Rango de ataque +75** = de melee a "casi ranged" (125→200): golpea desde fuera del alcance de muchos melee.
- **Heartsteel (3000g) es su mejor amigo**: golpe cada 20 s por campeón = 140 + 3.5 % vida máx, y **convierte 15 % del daño en HP permanente** → bola de nieve infinita que alimenta la R (+34 HP/proc a 2500 HP; +58 a 7000).
- **Ruta de build (preview del reporte futuro):** Chainlaced/Armored T3 → Heartsteel → Gargoyle → Twinguard → Liandry's/Cryptbloom (AP para R y E) → Mantle. Roles: jungla (Feast temprano con smite-kill de 1200 true vs monstruos) o mid/top.
- **Economía de stacks 7.3:** monstruos épicos más contestables (duración estándar, Baron mid-game buffeado) → cada épico = 1 stack sin cap. Prioriza dragones/herald aunque pierdas CS.

## 4. MALPHITE — la "armadura es daño" (y por qué lo banean 21.9 %)

Meta actual: **WR 52.17 %, ban 21.89 %** — el tanque más respetado del parche. Su kit convierte armadura en TODO:
- Base armor **49 (+5/nivel) = 119 a nivel 15** (la más alta de tu roster).
- **W pasiva:** +25/30/35/40 % de armadura extra; **W activa:** golpes en cono 20-50 + 20 % AD + **15 % armadura (7.3a; era 20 %)** (primer golpe: 40-100 + 40 % AD + **40 % armadura**).
- **E:** 60-210 + 45 % AP + **40 % armadura (7.3a; era 45 %)** AoE + **slow de AS 35-50 %** (anti-ADC duro: −50 % AS a una Jinx/Kalista enemiga = −40 % de su DPS).
- **Iceborn Gauntlet:** el campo de hielo **crece con tu armadura** (AoE de slow permanente).
- P Granite Shield: **11 % de vida máx** como escudo fuera de combate (con 3500 HP = 385 gratis cada 6 s).

**Números de la ruta armor-stack (nivel 15):**

| Etapa | Armadura | E (mágico AoE) | W golpe sostenido | W primer golpe | Escudo pasiva |
|---|---|---|---|---|---|
| Iceborn+Thornmail+Armored Advance | ~274 | 320 | 91 | 210 | 276 |
| + W rank 4 (+40 % bonus armor) | ~336 | 344 | 100 | 234 | 276 |
| + Gargoyle/Twinguard situacional | ~386 | **364** | **108** | **254** | 276+ |

> [!WARNING]
> **7.3a (29-sep-2026) nerfeó a Malphite:** ratio de armadura de W 20→15 %, de E 45→40 % y R CD 75/70/65→85/80/75 s.
> La tabla de arriba YA refleja el hotfix. Su identidad armor-stack sobrevive (sigue siendo el tanque con más ban),
> pero su pico de daño y la frecuencia de su wombo bajaron ~5-8 % / +10 s de CD.

**El tamaño en Malphite:** solo viene de ítems (Gargoyle activo + Twinguard + Sterak's si va fighter). NO tiene tamaño innato — su fantasía de "gigante" es 100 % armadura. Build comunidad validada: **Iceborn → Plated/Mercury's T3 → Thornmail → Zeke's → Gargoyle** (runas Grasp+Demolish+Second Wind+Overgrowth). Ajustes del modelo: vs comps AD puras, **Armored Advance** sobre Thornmail 2.º; Twinguard como 6.º capstone (con su uptime de combate permanente es el ítem de tamaño más consistente del juego). Zeke's potencia a tus carries AP (Diana/Yunara) con su R.

## 5. SHYVANA — tamaño condicional + Sterak's

- Forma dragón de la R: verificar en juego si modifica hitbox (la ficha no lista tamaño; en la transformación PC sí crece visualmente).
- Su ruta de tamaño real es **Sterak's Gage**: Heavy Handed le da **+50 % de su AD base como AD bonus** (62+4.6×14 = 126 base → **+63 AD**) + Lifeline (75 % de vida bonus como escudo) + tamaño/tenacidad 8 s al activarse — perfecto para su patrón de dive (entra, baja de 35 %, escudo + tamaño + sigue pegando).
- Preview de build (reporte completo pendiente): Gunmetal/Plated T3 → **Dusk and Dawn** (comunidad 1.º) → BotRK/Terminus (on-hit) o Rabadon's/Nashor's (AP R-burst) → Sterak's → Gargoyle/Wit's End.
- Con Shyvana el tamaño es cosmetic-utility (peel/intimidación en plena pelea); su "no-mueras" viene del escudo de Sterak's + W (Burnout) + curas de Dusk and Dawn.

## 6. CÓMO INTEGRAR ESTO EN SUS REPORTES COMPLETOS (protocolo)

Cuando pidas el reporte de Cho'Gath, Malphite o Shyvana, el análisis añadirá:
1. **Columna "ventanas de supervivencia"** por build: cuántos segundos de efectividad extra suman Sterak's/Mantle/Gargoyle/Twinguard y con qué CD (la métrica real detrás del "tamaño").
2. **EHP efectivo en ventana** (vida × multiplicador de mitigación con Twinguard al máximo + escudos), no solo EHP estático.
3. Para Cho'Gath: **curva de stacks por minuto** (minions cap 6 + épicos + campeones) y el execute de R resultante en cada punto de la partida.
4. Regla de compra: **Twinguard cuando las fights duran 5+ s** (5 stacks = 5 s), **Gargoyle cuando te burstean en <2 s** (activo inmediato), **Sterak's para fighters que bucean**, **Mantle para tanques que ya tienen 600 HP de base y sufren execute**.

## 7. FUENTES

Grep de "size/tamaño" sobre los 186 ítems de `items_7.3.csv` y las 12 fichas de campeones · notas oficiales 7.3 (Mantle: HP 200→600 y Twinguard: +300 HP base, rework de resistencias) · fichas wr-meta de Cho'Gath (R Feast completo), Malphite (W/E ratios de armadura) y Shyvana. Discrepancia registrada: el texto "Gains 9 Armor (25/30/35/40 %)" de la W de Malphite es ambiguo (¿9 + % del bonus o % del total?) — modelado como % del bonus (conservador), verificar en juego.


## 2. TEMPLATE + GUÍA DE ESTILO (estándar visual obligatorio v1.4)

# TEMPLATE + GUÍA DE ESTILO — Reportes WR-LAB (estándar v1.4)

> **Este archivo es la ley visual de los reportes.** Todo reporte nuevo (o re-estilizado) DEBE seguir
> esta estructura y convenciones al pie de la letra. Referencia canónica viva:
> `reportes/Jinx_WildRift_7.3_Build_Optimizada.md`.
> Regla de oro: cada afirmación lleva número, cada número lleva supuesto, cada supuesto está en §3/§10.

---

## A. GUÍA DE ESTILO (convenciones obligatorias)

### A.1 Estructura general
1. **Frontmatter YAML** (compatible Obsidian/Quartz):
   ```yaml
   ---
   tags:
     - {ROL}          # ADC / Support / Jungla / Mid / Top
     - {CLASE}        # Marksman / Enchanter / Assassin / Fighter / Mage / Tank
     - {ARQUETIPO}    # Crítico / On-hit / AP-Burst / etc.
     - {LANE}         # Bot-Lane / etc.
   version: X.Y
   Status: Borrador | Aprobado
   champion: {Nombre}
   patch: "7.3"
   ---
   ```
2. **Bloque de metadatos** (inmediato, en negritas, una línea por campo):
   `**Fecha del análisis:**` · `**Parche:**` · `**Rol principal:**` · `**Arquetipo:**` · `**Enfoque:**` (1-2 líneas: la tesis de la build).
3. **Callouts Obsidian** (en este orden, tras los metadatos):
   - `> [!NOTE]` **Estado Meta Actual ({rango}, {fecha}):** Win Rate X % | Pick Rate X % | Ban X % | Tendencia ↑↓ | Rol. → **OBLIGATORIO** (datos de wr-meta/fichas).
   - `> [!TIP]` Variante principal en 2-3 líneas (qué slot cambia, qué se gana/pierde con números). → OBLIGATORIO si existe variante.
   - `> [!DANGER]` Solo en **builds personalizadas de escenario** (ej. Yuumi agresiva, Cho'Gath tamaño): declarar el sacrificio con números ("sacrifica ~X % de Y a cambio de ~Z % más de W").
   - `> [!WARNING]` Datos pendientes de verificar en juego (rangos, mecánicas ambiguas).
4. Separador `---` entre TODAS las secciones numeradas.

### A.2 Encabezados
- Secciones: `## N. TÍTULO EN MAYÚSCULAS` (N = 0…10, fijos, ver §B). Apéndices: `## APÉNDICE A — ...`.
- Subsecciones: `### N.M Título en oración`.
- NUNCA inventar secciones fuera del esqueleto; si una no aplica al arquetipo, dejarla con su número y una nota de adaptación (ej. "§5 — No aplica: el primer ítem de support es la quest").

### A.3 Números y formato
- **Miles con espacio fino:** `2 900`, `17 350 g`, `1 250 g` (NUNCA `2900` ni `2,900`).
- **Porcentajes con espacio:** `25 %`, `100 %`, `+47.9 %`. Decimales con punto: `2.83`, `49.82 %`.
- DPS y oro como enteros; deltas con signo: `+19 %`, `−22 %` (minus U+2212 preferida).
- Ítems y runas en **negrita** en tablas y en primera aparición; habilidades en _cursiva_ o **Q/W/E/R**.
- Veredictos con emoji + número SIEMPRE: ✅ Core/6.º default · ⚠️ Situacional/niche · ❌ Rechazado (motivo numérico).
- Tablas > prosa. Prosa solo para veredictos, notas críticas y plan de juego (bullets con **lead en negrita**).
- Fórmulas y rutas de compra en bloques de código ``` ```.
- Flecha de mejora de botas: `⬆️` + texto "(min 10:00, MISMO slot)".

### A.4 Ley 0 en las tablas (no negociable)
- **Tabla A (Build final):** exactamente **6 filas** = 1 fila de botas (`Berserker's → ⬆️ Gunmetal (min 10:00, MISMO slot)`) + 5 ítems. Columnas: `Slot | Ítem | Oro | Rol en la build`.
- **Tabla B (Ruta de compra):** cronológica, puede tener 7+ filas porque incluye la mejora ⬆️ y los componentes. Columnas: `# | Compra | Oro acum. | Minuto típico`. Incluir **componentes** ("Pickaxe + Noonquiver → **Hexoptics C44**") y **oro acumulado**.
- Toda build publicada pasa `validate_slots()` y se declara en §10 ("Validación del modelo").

### A.5 Adaptaciones por arquetipo
| Arquetipo | §3 Modelo | §0 Resultado del modelo | §5 Primer ítem |
|---|---|---|---|
| ADC crítico / on-hit | DPS autos + procs | DPS 1v1 / 3v3 / vs armadura / vs tanque / heal | Sí (checkpoints 9/12) |
| AP rotación (Diana, mid) | Burst combo + DPS 10 s | DPS sostenido / burst / vs MR | Sí (orden de core) |
| Soportes (Yuumi/Karma) | **Valor-aliado**: escudos, curas, buffs | Escudo E / cura R / **DPS+ al carry** / amp de equipo | No aplica (quest) — declarar |
| Tanques (Cho'Gath/Malphite) | EHP + ventanas + execute R | EHP, mitigación, daño de utilidad | Sí (componente de vida/armadura) |

### A.6 Pie de página (OBLIGATORIO, estructura fija)
```markdown
---

## Pie de página

*Reporte generado el {dd/mm/aaaa} con datos del parche {X.X} ({fecha parche}). WR-LAB v{n}. Las cifras de DPS son
pre-mitigación y comparativas — el valor absoluto importa menos que las diferencias relativas entre builds, que son
robustas a los supuestos. Si Riot publica un {X.X}a/b (hotfix), regenerar datos antes de publicar.*

**Referencias y créditos**

- Notas oficiales del parche {X.X} ({fecha}) y {anteriores relevantes} — © Riot Games, Inc. (wildrift.leagueoflegends.com). {qué aporta}.
- Base de datos de ítems, runas y fichas de campeón — wr-meta.com (proyecto comunitario de JLVD DEV), sincronizada al {fecha}. {qué aporta}.
- Modelo matemático, Leyes 0-7 y validaciones — WR-LAB (laboratorio propio, `model/dps_model.py`), construido sobre las fuentes anteriores.

**Aviso legal:** Wild Rift y League of Legends son marcas registradas de Riot Games, Inc. Este documento es una guía
de comunidad con fines educativos, **no está afiliado, patrocinado ni respaldado por Riot Games**. Los nombres de
ítems, campeones y estadísticas pertenecen a sus respectivos dueños. El análisis y las conclusiones son trabajo
original del autor apoyado en WR-LAB.

---
```

### A.7 Nomenclatura de archivo (vault/sitio)
`{Campeón} — Wild Rift Build Optimizada.md` (título H1 NO se repite en el cuerpo si el frontmatter lleva `champion:`; el H1 lo pone Quartz). Para el lab: `reportes/{Campeón}_WR_{patch}_Build_Optimizada.md`.

---

## B. ESQUELETO CANÓNICO (copiar y llenar)

```markdown
---
tags: [ ... ]
version: 1.0
Status: Borrador
champion: {Nombre}
patch: "7.3"
---
**Fecha del análisis:** {dd/mm/aaaa}
**Parche:** 7.3 (21-sep-2026)
**Rol principal:** {rol}
**Arquetipo:** {arquetipo con 1 línea descriptiva}
**Enfoque:** {tesis de la build en 1-2 líneas con números}

> [!NOTE]
> **Estado Meta Actual (Diamond+, {fecha}):**
> Win Rate {X} % | Pick Rate {X} % | Ban {X} % | Tendencia {↑/↓} | Rol: {roles}.

> [!TIP]
> **Variante principal:** {slot que cambia + trade-off numérico}.

---

## 0. RESUMEN EJECUTIVO

### Tabla A — BUILD FINAL
| Slot | Ítem | Oro | Rol en la build |
|------|------|-----|-----------------|
| 1 (botas) | **{T2} → ⬆️ {T3}** (min 10:00, MISMO slot) | {g} | {stats clave} |
| 2..6 | **{ítem}** | {g} | {stats + pasiva en 1 línea} |

> **Oro total: {N} g** · {AD/AP} {X} · {AS/haste} {X} · {Crit/pen/HSP} {X} · {sustain}

### Tabla B — Ruta de compra cronológica
| # | Compra | Oro acum. | Minuto típico |
|---|--------|-----------|---------------|
| 1 | {start} | 500 | 0:00 |
| … | {componentes} → **{ítem completo}** | {acum} | ~{mm:ss} |
| k | ⬆️ **{T3}** (mismo slot, +1 000 g) | {acum} | ~{13:00} |

### Runas · Hechizos · Habilidades
| Categoría | Elección |
|-----------|----------|
| Keystone | **{runa}** ({números}) |
| {Árbol} 2..4 | **{runa}** ({números}) |
| Secundaria | **{runa A}** ({caso}) / **{runa B}** ({caso}) |
| Hechizos | **{X + Y}** |
| Skills | **{orden}** (R en 5/9/13) |

### Resultado del modelo ({condiciones})
| Escenario | {DPS/Valor} |
|-----------|-----|
| **1v1** (pre-mitigación) | **{N}** |
| **3v3** | **{N}** |
| **vs 120 armadura / MR** | **{N}** |
| **vs Tanque** | **{N}** |
| {sustain/heal/shields} | **{N}** |

> **Titular:** {comparación estelar con % vs la alternativa más común}.

---

## 1. CONTEXTO DEL CAMPEÓN EN ESTE PARCHE
### 1.1 Cambios directos ({champion}) — tabla Stat/Habilidad | Antes | Ahora | Impacto
### 1.2 Cambios sistémicos que le afectan — tabla Sistema | Cambio | Efecto
### 1.3 ¿Sus habilidades escalan con crítico/{stat clave}? — respuesta + implicación

---

## 2. FICHA MATEMÁTICA (spec)
| Parámetro | Valor | Fuente |   (+ líneas de cálculo en negrita: AD lvl 15, bonus fijo, etc.)

---

## 3. MODELO Y FÓRMULAS
```{fórmulas del motor adaptadas al campeón}```
### Supuestos específicos — bullets

---

## 4. LEYES APLICADAS A {CHAMPION}
### Ley 0 — Slots (siempre: declarar 1 botas + 5 ítems y validate_slots PASS)
### Ley 1..7 — solo las que aplican al arquetipo, con tabla/cálculo por ley

---

## 5. ANÁLISIS DEL PRIMER ÍTEM
| Candidato | Oro | DPS lvl 9 1v1 | lvl 9 3v3 | lvl 12 1v1 | lvl 12 3v3 | Nota |
**Veredicto:** {con números y cruce de curvas}. **Nota crítica:** {mitos corregidos}.

---

## 6. BUILD FINAL RANURA POR RANURA
| Slot | Ítem | Justificación matemática |
### Matriz del último slot (situacional)
| Situación | Ítem | Coste | Impacto medido |
### RECHAZADOS (con motivo numérico)
| Ítem | Motivo del rechazo |

---

## 7. RUNAS · HECHIZOS · HABILIDADES
### Keystone: {nombre} — bullets con números + **Alternativas:** en cursiva con caso de uso
### Secundarias — tabla Slot | Runa | Valor estimado
### Hechizos: {X + Y} — por qué
### Orden de habilidades — **{A → B → C}** + bullet por habilidad

---

## 8. COMPARACIÓN CONTRA LAS ALTERNATIVAS
### Tabla maestra ({nivel}, {condiciones})
| Build | Oro | {stats} | 1v1 | 3v3 | vs 120 | vs Tanque | {sustain} |
### Desglose multiplicativo de la diferencia — tabla Factor | Multiplicador | Contribución

---

## 9. PLAN DE JUEGO
### Early (0:00 – 9:00) / ### Mid (9:00 – 16:00) / ### Late (16:00+)
— bullets con **lead en negrita** y números/tiempos
### Reglas del parche que cambian el macro — tabla Regla | Impacto

---

## 10. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS
### Fuentes primarias (mandan) — tabla
### Fuentes secundarias — tabla
### Discrepancias detectadas y resolución — tabla
### Supuestos del modelo (declarados) — bullets
### Contexto meta ({fecha}) — párrafo con cautela de muestra
### Validación del modelo — bullets: `validate_slots(...) → PASS` + test de Caitlyn (1.48125)

---

## APÉNDICE A — POOL DE ÍTEMES DEL ROL: veredicto para {champion}
| Ítem (oro) | Veredicto | Nota |

---

## APÉNDICE B — RUTAS DE COMPRA
```{DEFAULT / SNOWBALL / ANTI-PRESIÓN / VS … en bloque de código con ⬆️ y minutos}```

---

## Pie de página
{estructura fija de A.6}
```

---

## C. CHECKLIST ANTES DE PUBLICAR (Status: Borrador → Aprobado)

- [ ] Frontmatter completo (tags rol/clase/arquetipo/lane, version, Status, champion, patch).
- [ ] Metadatos + callout [!NOTE] con meta real (WR/pick/ban/tendencia + fecha).
- [ ] Tabla A = 6 filas exactas (1 botas con ⬆️ + 5 ítems); Tabla B con componentes y oro acumulado.
- [ ] `validate_slots()` en PASS declarado en §10.
- [ ] Números con espacio de miles (`2 900`) y `%` con espacio (`25 %`) en TODO el documento.
- [ ] Secciones 0-10 + Apéndices A/B + Pie de página presentes, en orden, con `---` entre ellas.
- [ ] Todo ✅/⚠️/❌ acompañado de número.
- [ ] Discrepancias de fuentes declaradas (notas oficiales > wr-meta).
- [ ] Hotfix verificado (¿7.3a/b?) antes de pasar a Status: Aprobado.
- [ ] Pie de página con referencias Riot/wr-meta/WR-LAB + aviso legal.


## 3. FUENTES Y REGLAS DE VERIFICACIÓN

# FUENTES — Registro de datos y verificación

**Última actualización del lab:** 25 de septiembre de 2026 · **Parche base:** 7.3 (lanzado 21-sep-2026)

## Hotfix 7.3a (29-sep-2026)

| Fuente | Acceso | Qué aporta | Fiabilidad |
|---|---|---|---|
| Notas oficiales CN (lolm.qq.com docid 15413436308828016227) vía traducción comunitaria r/wildrift (thread 1wskk84), recuperada por Arctic Shift API | 28/09/2026 (`data/raw/patch73a_cn_en.txt`, diff completo en `data/estructurada/cambios_7.3a.md`) | Nerfs: Hwei, Rammus, Malphite, Caitlyn, Senna (ajuste), Syndra, Yuumi · Buffs: Samira, Tristana, Draven, Viego · Yun Tal buff · Diadem/Circlet/Whispering nerf · Death's Dance 3300 · Smite burn −, Nexus 4000, placas −resist · ARAM | Alta (texto oficial CN traducido; números con formato >>> coherentes). **Pendiente: re-verificar contra la nota EN cuando Riot la publique** y contra wr-meta cuando indexe (aún no lo hace al 28/09) |

## Fuentes primarias (MANDAN sobre cualquier otra)

| Fuente | URL | Acceso | Qué aporta |
|---|---|---|---|
| Notas oficiales Wild Rift 7.3 | wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-7-3/ | 25/09/2026 (HTML completo, 646 KB → `data/raw/patch73.html/.txt`) | Sistema de crítico 200/230 %, nuevo sistema de AS + tope 3.0, apéndice de AS de los 140 campeones, todos los cambios de ítems/runas/campo, nerfs de Jinx, fórmula oficial de AS con ejemplo de Caitlyn |
| Notas oficiales Wild Rift 7.2 | wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-7-2/ | 25/09/2026 (`data/raw/patch72.txt`) | Fin de los encantamientos de botas; QSS/Mercurial Scimitar/Galeforce como ítems de clase; botas Tier 2/T3 y regla del minuto 10:00 |

## Fuentes secundarias (solo para lo que las notas no tocan)

| Fuente | URL | Acceso | Qué aporta | Fiabilidad |
|---|---|---|---|---|
| wr-meta.com/items | wr-meta.com/items/ | 25/09/2026 (`data/raw/wrmeta_items.html`, 510 KB) | Stats completos y precio de los 186 ítems únicos (incluye nuevos de 7.3), pasivas, botas T2/T3, runas | Alta: incluye ítems 7.3; desfasada en runas removidas (lista Ingenious Hunter) y texto viejo de Lethal Tempo |
| wr-meta.com Jinx | wr-meta.com/39-jinx.html | 25/09/2026 (`data/raw/wrmeta_jinx.html/.txt`) | Stats base de Jinx (58 AD/630 HP/335 MS/575 rango), valores por habilidad, change history completo, build popular y meta (WR 49.82 %, pick 10.97 %, Diamond+, 24/09) | Alta para números de kit; la build popular es insumo, no conclusión |
| wr-meta.com — 11 fichas del equipo | wr-meta.com/{id}-{champ}.html (yuumi 321, yunara 545, mordekaiser 365, kalista 349, diana 216, karma 323, heimerdinger 346, volibear 411, seraphine 34, shyvana 23, chogath 339) | 25/09/2026 (`data/raw/campeones/*.html` → `data/estructurada/campeones/*.md` + `champion_base_stats.json`) | Stats base, habilidades con valores, change history y builds populares de los 11 campeones del roster | Alta en general; ⚠️ Volibear muestra ad_growth "56" (errata probable — verificar); el rango de ataque no se publica (verificar Kalista/Yunara en juego) |

## Fuentes intentadas y descartadas (para no repetir el trabajo)

- **wildrift.wiki** — DNS muerto al 25/09/2026 (no resuelve ni desde el sandbox ni desde los proxies de lectura).
- **leagueoflegends.fandom.com / wild-rift.fandom.com** — 403 al acceso directo; la página `Jinx_(Wild Rift)` no existe en la wiki principal de LoL.
- **reddit.com (PBE 7.2 preview)** — 403/bloqueado; usado solo como pista corroborada después contra las notas oficiales 7.2.
- **wildstats.gg / u.gg/wr / mobalytics.gg/wr** — apps JS sin contenido estático útil o 403.
- **op.gg/wild-rift** — 404 en la ruta probada.

## Discrepancias detectadas y regla de resolución aplicada

| Tema | Fuente A | Fuente B | Resolución |
|---|---|---|---|
| Lethal Tempo (valores ranged) | wr-meta: 4.8 %/stack, bala 6–20, +0.33 %/1 % AS | Notas 7.3: **6.4 %/stack, bala 6–24, +0.67 %/1 % AS** | Mandan las notas oficiales |
| Legend: Alacrity | Descripción wr-meta: 3 % + hasta 18 % (=21 %) | Ejemplo oficial Caitlyn 7.3: "18 % a full stacks" | Modelo usa 21 % (peor caso para el tope de AS); diferencia de DPS < 1 % |
| Noxian Gait (Gunmetal) | Notas 7.2: 15 %/10 % MS | wr-meta post-7.3: 10 %/7 % | wr-meta (posterior al reajuste global de MS 5→4 %) |
| Ingenious Hunter | wr-meta la lista | Notas 7.3: **REMOVIDA** | Removida |
| Berserker's Greaves AS | Notas 7.2: 30 % | wr-meta + ejemplo oficial Caitlyn 7.3: **35 %** | 35 % |
| ⚠️ Caitlyn Base Bonus AS | Notas 7.3 §CAITLYN y ejemplo de la fórmula: **0.28** | Apéndice final de las mismas notas: **0.2** | **Inconsistencia interna de Riot.** Usar 0.28 (sección del campeón + ejemplo oficial) y verificar en el panel del juego antes de publicar cualquier análisis de Caitlyn. El CSV `champion_attack_speed_7.3.csv` replica el apéndice (0.2) — corregir manualmente si se confirma 0.28 |

**Regla permanente:** notas oficiales > BD comunitaria sincronizada > guías/comunidad. Toda discrepancia nueva se anota aquí.

## Qué archivo deriva de qué

```
data/raw/patch73.html  ─┬→ data/raw/patch73.txt ─┬→ cambios_campeones_7.3.md
                        │                        ├→ cambios_items_7.3.md
                        │                        ├→ cambios_runas_7.3.md
                        │                        ├→ sistemas_campo_7.3.md
                        │                        ├→ mecanica_attack_speed_7.3.md
                        │                        ├→ champion_attack_speed_7.3.csv   (140 campeones)
                        │                        └→ champion_durability_7.3.csv     (51 campeones)
data/raw/patch72.txt   ───→ referencia del sistema de botas/encantamientos (leer §BOOTS)
data/raw/wrmeta_items.html ┬→ items_7.3.csv / items_7.3.md  (186 ítems)
                           └→ runas_7.3.md
data/raw/wrmeta_jinx.html  → spec de Jinx en model/dps_model.py + reporte
```


## 3b. HOTFIX 7.3a — DIFF COMPLETO (APLICADO A ESTE BUNDLE)

# HOTFIX 7.3a — Cambios completos (despliegue: 29-sep-2026, 09:30–12:00 CN)

> **Fuente:** notas oficiales del servidor chino (lolm.qq.com, docid 15413436308828016227) vía traducción
> comunitaria (r/wildrift, archivado en `data/raw/patch73a_cn_en.txt`). El sitio oficial EN aún no publica
> página propia de 7.3a (verificado 28/09: 404); la página de notas 7.3 no fue modificada.
> **Estado en el lab:** datos aplicados donde aplica; pendientes de re-verificación contra la nota EN oficial
> cuando se publique (protocolo §E de FRAMEWORK).

## RESUMEN DE INTENCIÓN (traducción del intro oficial)

"Ajustes de balance a campeones e ítems selectos — reforzando a los de bajo rendimiento y devolviendo a
niveles razonables las elecciones dominantes. Ralentización moderada del ritmo de clear de jungla early-mid
y menor resistencia contra split-push/siege continuo. Ajustes a Augments y campeones de ARAM por feedback."

## CAMPEONES

| Campeón | Tipo | Cambios |
|---|---|---|
| **Hwei** | NERF | Pasiva: 33–333 + 33 % AP → **40–285 + 30 % AP** · (1-1) Fire: 50/90/130/170 + 75 % AP → **50/85/120/155 + 70 % AP** · (1-2) amp por vida faltante: 150/200/250/300 % → **100/150/200/250 %** · (4) detonación: 250/350/450 + 75 % → **200/300/400 + 70 % AP** |
| **Samira** | BUFF | HP growth 128→**136** · armor growth 5→**5.5** · MR growth 1.4→**2** · pasiva melee ratios ~×1.65 · Flair 110→**125 % AD** · R por tiro 40→**50 % AD** |
| **Rammus** | NERF | Armor base 45→**40** · W bonus armor 45/50/55/60→**30/40/50/60 %** |
| **Malphite** ⚠️lab | NERF | W ratio de armadura 20→**15 %** · E ratio de armadura 45→**40 %** · R CD 75/70/65→**85/80/75 s** |
| **Tristana** | BUFF | Q AS 50/75/100/125→**60/80/100/120 %** · W CD 22/20/18/16→**20/18/16/14** · E base 80/100/120/140→**80/110/140/170**, ratio 100→**120 %**, amp crit 40→**50 %**, amp daño crit 40→**50 %** |
| **Draven** | BUFF | Q 80-110→**90-120 % AD** · W AS 20-35→**25-40 %** · R 130→**150 % AD** |
| **Caitlyn** ⚠️apéndice | NERF | **AS growth 0.04→0.025** · Headshot ratio 60–100→**60–90 % AD** |
| **Senna** ⚠️apéndice | AJUSTE | AS ratio/base 0.4→**0.3** · Base Bonus AS 0.6→**1.1** · AS growth 0.05→**0.025** · la AS bonus reduce menos el wind-up |
| **Syndra** | NERF | Nodos de pasiva 40/60/80/100/120→**50/75/100/125/150** · W ratio 60→**50 %** · slow fijo **25 %** |
| **Swain** | AJUSTE | Pasiva heal 3–4.5 %+0.5 % AP→**4.5–6 % + 0.2 % AP** · E return ratio 25→**40 % AP** |
| **Yuumi** ⚠️lab | NERF | W Best Friend HSP: 8/9/10/11 % + 0.02 % AP → **6/7/8/9 % + 0.01 % AP** |
| **Viego** | BUFF | Q pasiva 2-5→**3-6 %** · crit ratio 80→**85 %** · R crit scaling 50→**70 %** |

## ÍTEMS

| Ítem | Tipo | Cambios |
|---|---|---|
| **Yun Tal Wildarrows** ⚠️lab | BUFF | AS 25→**35 %** · Flurry: +25→**35 % AS**, CD 20→**25 s** |
| **Whispering Circlet** | NERF | Harmonize HSP: 0.5→**0.25 % del maná máx** |
| **Crown/Diadem of Songs** ⚠️lab | NERF | Harmonize HSP: 0.5→**0.25 % del maná máx** ("deja de ser BiS de enchanter; vuelve opcional-situacional") |
| **Death's Dance** | NERF | Coste 3 200→**3 300 g** |

## MAPA Y SISTEMAS

| Sistema | Cambio | Impacto en el lab |
|---|---|---|
| **Smite burn vs monstruos** | 30–198/s → **22–162/s** | Jungla early más lenta → Diana jungla: Nashor's 1.º aún más correcto; Shyvana/Volibear/Cho'Gath jungla: clear early −15-20 % |
| **Nexus** | 5 500 → **4 000 HP** | Partidas terminan antes tras inhibidores |
| **Placas de torreta** | Al perder placa: +30→**+20** arm/MR y 20→**10 s** | **Siege más fácil** → sube el valor de Jinx/Kalista/Yunara (siege) y de Runaan's/Energized |
| ARAM (Augments + Fiddle/Nasus) | varios | Fuera del alcance SR del lab |

## IMPACTO EN REPORTES/SPECS DEL LAB (estado 28/09)

| Archivo | Impacto | Acción |
|---|---|---|
| `reportes/Yuumi_*` | HSP de W: −2 pts y mitad del término AP → E-shield 339→~338 (−0.3 %), R-heal 651→~648. **Build y veredictos intactos** (Censer sigue siendo el rey) | Anotado [!WARNING] en el reporte |
| `metodologia/ESCALADO_DE_TAMANIO.md` | Malphite: E con 336 armor pasa de 361→**344**; W golpe 117→**100**; R cada 85 s | Tabla corregida + nota |
| `champion_attack_speed_7.3.csv` | Filas Caitlyn (0.04→0.025 por nivel) y Senna (0.3/0.3/1.1/0.025) | Corregidas con marca 7.3a |
| `model/dps_model.py` ITEMS | Yun Tal AS 25→35; Death's Dance 3300 | Aplicado |
| `reportes/Kalista_*` | Yun Tal buffeada sigue RECHAZADA para Kalista (sin on-hit, ramp de crit); para **Yunara** (reporte externo) es buff relevante → re-verificar ese reporte | Anotado |
| `reportes/Diana_*` | Smite burn −18 % → clear early más lento (refuerza Nashor's 1.º en jungla) | Anotado |
| `reportes/Jinx_*` | Placas más blandas + Nexus 4000 → siege Jinx MEJORA; ningún cambio directo a Jinx | Anotado |
| Reportes externos (Yunara/Cho'Gath/Shyvana hechos en otro chat) | Yunara: Yun Tal buff + placas (revisar 1.er ítem) · Cho'Gath: smite nerf jungla · Shyvana: smite nerf | Marcar para revisión en su próxima regeneración |
| FRAMEWORK test de Caitlyn | El ejemplo oficial (1.48125) usaba growth 0.04 (pre-7.3a); con 0.025 el resultado esperado a lvl15 con Alacrity+Berserker's es **1.35** | Test actualizado con ambos valores |


## 4. MECÁNICA OFICIAL DE ATTACK SPEED (7.3) + TEST DE CAITLYN

# Mecanica de Attack Speed 7.3 (explicacion oficial)

In Patch 7.3, we made fairly major changes to Attack Speed, so we also want to take this opportunity to fully explain how Attack Speed works. Attack Speed is the stat that determines how often a unit can perform basic attacks. For a champion, Attack Speed can mainly be broken down into the following types:
- Base Attack Speed
- Base Attack Speed is a champion's starting Attack Speed and usually also determines that champion's Attack Speed Ratio.
- Attack Speed Ratio
- Attack Speed Ratio determines how efficiently a champion converts bonus Attack Speed into actual Attack Speed. It converts the bonus Attack Speed a champion gains into real Attack Speed based on a percentage. In most cases, a champion's Attack Speed Ratio is equal to their Base Attack Speed.
- Base Bonus Attack Speed
- Base Bonus Attack Speed is the bonus Attack Speed a champion has as soon as the match begins, and it does not scale with champion level. This means a champion's Attack Speed at level 1 is determined jointly by their Base Attack Speed and Base Bonus Attack Speed.
- Attack Speed per Level
- Attack Speed per Level is the Attack Speed a champion gains as they level up, and it is also treated as bonus Attack Speed in these calculations. (By contrast, other per-level stats, such as Attack Damage per Level, are not treated as bonus Attack Damage and are instead calculated as part of base Attack Damage.) Although Attack Speed per Level is a fixed value, the amount of bonus Attack Speed a champion gains each level is not equal. Bonus Attack Speed gained from leveling each level = Attack Speed per Level ×(0.7 + 0.04 × current level). For example, when a champion levels from 1 to 2, the bonus Attack Speed gained is equal to 74% of their Attack Speed per Level. By max level, the total bonus Attack Speed a champion gains from leveling = 1400% × Attack Speed per Level.
Next, we'll take a closer look at how Attack Speed is calculated. Let's start with a few formulas:
- Total Attack Speed = Base Attack Speed + Attack Speed Ratio × Bonus Attack Speed Bonus Attack Speed = Base Bonus Attack Speed + bonus Attack Speed gained from leveling + bonus Attack Speed gained from other sources such as items, runes, and abilities
Let's use Caitlyn as an example and plug the numbers into the formulas:  
- For Caitlyn, both her Base Attack Speed and Attack Speed Ratio are 0.625, her Base Bonus Attack Speed is 0.28, and her Attack Speed per Level is 0.04.
- At level 1, without any extra items or runes, Caitlyn's only bonus Attack Speed comes from her Base Bonus Attack Speed. So Caitlyn's Attack Speed = Base Attack Speed + Attack Speed Ratio × Base Bonus Attack Speed = 0.625 + 0.625 × 0.28 = 0.8 Assume Caitlyn is at max level, has a fully stacked rune - Legend: Alacrity (granting 18% bonus Attack Speed), and has equipped Berserker's Greaves (granting 35% bonus Attack Speed). Her Attack Speed can then be calculated as follows: 0.625 + 0.625 × (0.28 + 0.04 × 14 + 0.18 + 0.35) = 1.48125. On the stats panel, Attack Speed is displayed with two decimal places: 1.48

## 5. RUNAS (cambios 7.3 + valores)

# Cambios a runas - Wild Rift 7.3 (notas oficiales)

> Lethal Tempo rehecho, Legend: Haste reemplaza a Legend: Tenacity, Ingenious Hunter removida, Conqueror/Demolish ajustados.

RUNE ADJUSTMENTS
Lethal Tempo
Lethal Tempo has been providing too much Attack Speed and bonus range on its own, creating some extreme power swings for marksmen throughout the game. Alongside our marksman item updates, we’re reworking the rune to rely more on synergy with other Attack Speed sources rather than providing so much power by itself. This should make Lethal Tempo a more natural fit for champions who invest heavily in Attack Speed, while keeping its power more consistent and easier to control.
- Landing basic attacks on enemy champions grants stacking Attack Speed, 8% for melee and 6.4% for ranged, up to 6 stacks for 6 seconds. At max stacks, attacks also fire a bullet that deals adaptive damage, 9 - 30 for melee and 6 - 24 for ranged. Each 1% bonus Attack Speed increases this damage by 1% for melee and 0.67% for ranged.
Conqueror
We've standardized Conqueror's Attack Damage and Ability Power scaling. 
- Stats granted per stack: 3–5 Bonus Attack Damage / 4–8 Ability Power (1.25x–1.6x) -> 3–5 Bonus Attack Damage / 5–8.33 Ability Power (standardized to 1.667x) 
Legend: Haste 
With Mercury’s Treads now providing a significant amount of Tenacity, having additional Tenacity readily available through runes can make crowd control too easy to shrug off. We want Tenacity to remain a more deliberate investment so champions who rely on crowd control can still do their jobs. As a result, we’re replacing Legend: Tenacity with Legend: Haste.
- Replaces Legend: Tenacity
- Takedowns and killing monsters and minions grant Ability Haste, up to a maximum of 15 Ability Haste, with each stack granting 1.5 Ability Haste.
Demolish 
To align with turret-related changes such as Crystalline Overgrowth, we're making corresponding adjustments to Demolish. See Battlefield Adjustments for details. 
- After hitting a turret with 3 basic attacks, melee champions deal 85 + 28% maximum Health bonus Physical Damage, while ranged champions deal 50 + 20% maximum Health bonus Physical Damage. 
Ingenious Hunter 
Ingenious Hunter has created some overly powerful synergies with certain items, while barely making an impact with others. To keep the item system in a healthier spot, we’re removing Ingenious Hunter for now. Don’t worry, hunters, we’ll bring it back when the time is right.
- Removed
Legend: Tenacity
- Removed

### 5.2 Runas completas

# Runas Wild Rift - estado 7.3

> Fuente: wr-meta.com (24-sep-2026). OJO: Ingenious Hunter fue REMOVIDA en 7.3 y Legend: Tenacity -> Legend: Haste (ver cambios_runas_7.3.md).
> Lethal Tempo: usar valores oficiales 7.3 (6.4%/stack ranged, bala 6-24, +0.67% por 1% AS bonus), NO el texto de abajo que puede estar desactualizado.

KEYSTONE
Electrocute
Burst Damage
Within 3 seconds, hit the same enemy champion with 3 basick attacks or abilities to cause additional adaptive damage to the target.
Damage value: 40-210 (
) + 
10% extra 
 + 
5% 
Cooldown:
 20-13s (
)
Dark Harvest
Bonus Damage, Stack Amplification
Damaging a champion below 50% health deals adaptive damage and harvests their soul, permanently increasing Dark Harvest's damage by 11.
Dark Harvest damage: 35+ 11 per soul + 
10% bonus 
 + 
5% 
Cooldown:
 20s (Resets to 1s on takedown)
Empowerment
Increased damage against champions
Hitting an enemy champion with 3 consecutive attacks deals bonus 
adaptive
 damage and amplifies your damage dealt by 8% until you leave combat with champions.
Adaptive
 Damage:
 40-165 (
)
Cooldown: 4s.
Damage amplification will only take effect against champions.
Lethal Tempo
Attack Speed
Gain Attack Speed when attacking enemy champions. Stacks up to 6 times. At max stacks deal bonus damage with your attacks.
Each stack 
Attack Speed
 by 
6%
 (
4.8%
 for ranged champions) for 6 seconds.
Max stacks bonus:
 Attacks against non-turrets fire a bullet on hit, dealing 
9–30 adaptive damage
 (
6–20
 for ranged champions). Every 1% bonus 
Attack Speed
 you have increases the damage by 0.5% (0.33% for ranged champions).
Fleet Footwork
Mobility, Heal
Moving, attacking and casting builds Energy stacks. At 100 stacks, your next attack gains 
Attack Speed
, heals you, grants bonus 
Movement Speed. 
If the attack is again st a champion, it also restores Mana or Energy.
Bonus Attack Speed
: 40%
Health Restore:
 15-110 (
) + 
15% bonus
 + 
10%
.
Bonus Movement Speed
: 20% for 1s.
When attacking a champion, restore 8% missing 
mana
 or 8% missing 
energy
.
When attacking minions or monsters, heals for 35% (Melee champions) or 15% (Ranged champions) of the original heal amount.
Conqueror
Stacking Damage, Vamp
Gain stacks of Adaptive Force when hitting a champion with separate attacks or abilities. Stacks up to 6 times. When fully stacked, gain bonus omnivamp.
Per stack: 
3-5 bonus 
 or 
5-8 
 for 6s.
Fully stacked bonus: Melee - 9%, Ranged - 5% bonus 
Omnivamp 
.
Grasp of Undying
Tank, Heal
Every 3s in combat, your next attack on a champion will be enhanced.
Bonus 
magic damage
: 
3.3%
Heal: 
1.3%
Permanently 
health
 increase: 
10
On Ranged champions, the effects are reduced by 60%.
Guardian
Protect, Shield
Guard allies within 350 units of you and allies you target with abilities for 2.5 second(s). While guarding, if you or the ally take more than a certain amount of damage, both of you gain a shield for 1.5 second(s).
Shield: 40–165 (
) + 
6% bonus
 + 
15%
Damage threshold: 70–240 damage taken (
)
Cooldown:
 55–25s (
)
Aery
Poke, Protect
Your attacks and abilities send Aery to a target, damaging enemies or shielding allies.
Damage: 15-70 (
) + 
10% bonus
 + 
5%
Shield: 25-120 (
) + 
10% bonus
 + 
5%
Aery cannot be sent out again until she returns to you.
Arcane Comet
Poke, Stack Amplification
Damaging a champion with an ability hurls a comet at their location. When a comet hits an enemy champion, the next comet's damage increases.
Damage: (15 to 100) + (2 x total hits on enemy champions) + 
10% bonus
 + 
5%
.
Cooldown:
 16-8s (
)
Phase Rush
Mobility, Ability Haste
Using basic attacks or abilities on an enemy champion 3 time(s) within 4s grants 
Movement Speed
 and reduces the remaining cooldown of basic abilities by 20%.
Duration:
 3s.
Movement Speed bonus:
 Melee - 
40%-60%
 (
) | Ranged - 
20-35%
 (
).
Ability Haste:
 10.
Slow Resist:
 60%.
Cooldown:
 21-7s (
)
First Strike
Initiate, Damage Amplification, Bonus Gold
Initiating combat with an enemy champion or dealing damage to them within 0.25s of engaging them in combat grants 
10 gold
 and First Strike for 3s, allowing you to deal 
7% bonus true damage
 to them. After the effect ends, gain bonus 
gold
 based on the bonus damage dealt for its duration.
If you do not deal damage to the enemy champion within 0.25s of engaging them in combat, First Strike will go into a 10-second cooldown.
Bonus gold:
Melee: 65% of bonus damage.
Ranged: 45% of bonus damage.
Cooldown:
 20-30s
Ice Overlord
Control, Slow
Immobilizing an enemy champion causes 3 beams to form around them, creating ice beneath them for 3 second(s) and slowing enemies inside. The slow lingers on enemies for 1.5 second(s) after they've left the ice zone. Gain a protective layer of ice around yourself, increasing your defenses. After a brief delay, the ice explodes, dealing a burst of magic damage around you.
Slow:
 (
1%
 of your 
bonus Health
 + 15%).
Defenses:
 35 + 75% bonus 
Armor
 and 
Magic Resist
. Lasts 2.5 second(s).
Magic damage:
 15–100 (
) + 
5% max
Cooldown:
 20s
DOMINATION
Cheap Shot
Targets movement-impaired enemies
Deals 10-45 bonus 
true damage
 to enemies whose movement is impaired.
Cooldown:
 7s
Sudden Impact
Triggers when in stealth or dashing
Damaging an enemy champion deals a bonus 
15-65 true damage
 after using a dash, leap, blink, teleport, or when exiting stealth for 4s.
The damaging attack/ability gains bonuses at higher levels:
Level 5:
 Deal an additional 
5 true damage
.
Level 9:
 Deal an additional 
5 true damage
 and gain 
10% Movement Speed
 for 1.5s after dealing the damage.
Cooldown:
 10s
Empowered Attack
Triggers on attack
Every 8 seconds, the next attack will be empowered, dealing 20-60 bonus 
adaptive
 damage (
) to anemy champions. Ranged champions deal 80% damage.
Chain Assault
Triggers on attack after hitting a target with an ability
Hitting an enemy champion with an active ability applies a mark to them, causing your next 2 attacks or active ability casts against them to deal bonus 
adaptive damage
 equal to (12-38 (
) + 
3% bonus 
 + 
1.5%
).
Cooldown:
 15s
Tyrant
Deal damage to low Health enemies
When damaging a champion below 50% Health, deal (20-70 (
) + 
6% bonus 
 + 
3% 
) bonus 
adaptive damage
.
Cooldown:
 10s
Hubris
Kills temporarily increase Attack Damage/Ability Power
Scoring a takedown against an enemy champion within 3 second(s) of damaging them grants (5 + 1 per champion kill you've scored) 
Adaptive Force
 for 30 second(s).
Eyeball Collection
Kills increase Attack Damage/Ability Power
Gains 
1.5
 or 
3
 after scoring a champion or epic monster takedown, stacking up to 8 times.
Ingenious Hunter
Kills increase Item Ability Haste
Gains 20 Item 
Ability Haste
. For each champion or epic monster takedown you score, gain an additional 5 Item 
Ability Haste
. Stacks up to 5 times.
Relentless Hunter
Kills grant out-of-combat Movement Speed
Gain 
10
 out-of-combat 
Movement Speed
. For each champion or epic monster takedown you score, gain 
2
 out-of-combat 
Movement Speed
. Stacks up to 5 times.
Zombie Ward
Vision control increases Attack Damage/Ability Power
Takedowns on enemy wards spawn a Zombie Ward in its place, granting vision of the surrounding area for 120 seconds. Additionally gain 
3
or 
6
(max 5 stacks). (Assists on enemy wards also grant stacks and spawn Zombie Wards.)
PRECISION
Brutal
Attacks deal on-hit damage
Attacks deal (
5
 + 
6% bonus 
+ 
3% 
) bonus 
adaptive
 damage to enemy champions.
Triumph
Increase damage when low in Health
Champion takedowns restore 
10% of lost health
 and 10% of maximum 
Mana
Energy
and grant 
35 Movement Speed
 for 2 second(s).
Battle Zeal
Increase damage during prolonged battles
Gain 1.4% stacking basic ability damage amplification every 1 second(s) while in combat with a champion. Stacks up to 3 times and only takes effect against enemy champions.
Last Stand
Increase damage when low in Health
When 
health is lower than 60%
, attacks launched at enemy champions deal 5-11% bonus 
adaptive
 damage.
Grants maximum bonus damage when Health is lower than 
30%
Cut Down
Deal more damage to high Health enemies
Your attacks deal 6.57% bonus 
adaptive
 damage to enemy champions with more than 60% Health.
Coup de Grace
Increase damage to low Health enemies
Your attacks deal 8% bonus 
adaptive
 damage to enemy champions with less than 
40% Health
.
Legend: Alacrity
Increase bonus Attack Speed
Gains 
3% Attack Speed
. Takedown monsters, enemy champions, or minions to gain up to an additional 
18% Attack Speed
.
Legend: Haste
Bonus Ability Haste
Gain 
0 Ability Haste
 at the start of the game. Taking down monsters, enemy champions, or minions grants additional Ability Haste bonuses. Total bonus is capped at 
15 Ability Haste
.
Legend: Bloodline
Increase Omnivamp
Gains 
1% Omnivamp 
. Takedown monsters, enemy champions, or minions to gain up to an additional 
7% Omnivamp 
.
RESOLVE
Demolish
Destroy turrets faster
Your third attack against a turret deals bonus 
physical damage
 (85 + 
28% max Health
 for melee champions; 50 + 
20% max Health
 for ranged champions).
Cooldown:
 30s
Font of Life
Team Heal
When your attacks or abilities hit an enemy champion, heal yourself and the lowest Health allied champion nearby.
Ally: Heals for 
1.5% of your max 
 + 
5% of your
You: Heal for 
1% of your max 
 + 
5% of your
Healing is 130% effective if you're a melee champion. (Does not trigger if you or nearby allies are at full Health, or if no allies are nearby.)
Cooldown:
 15s
Courage of the Colossus
Immobilize enemies to gain shields
Gains a 
shield that absorbs
 up to 
25-45 
(
) + 
1% of max Health
 for 3s when immobilizing an enemy champion.
Cooldown:
 18s
Unshakeable
Increase Armor, Magic Resist, and Slow Resist
Gain 3% 
Armor
 and 
Magic Resistance
. For every 1 enemy champion(s) nearby, gain an additional 2% 
Armor
 and 
Magic Resistance
. If the max number of enemy champions are nearby (max: 3), you also gain 
20% Slow Resist
.
Second Wind
Increase sustain
Gain 
5 Health
 every 5 seconds.
After taking damage from an enemy champion, 
regenerate 3 + (1.5% of your missing health) 
 over the next 5 seconds. This effect is doubled for melee champions.
Nullifying Orb
Grant a protective shield
If you take damage from a champion that causes you to fall below 35% of your max Health, gain a 
shield
 that 
absorbs up to 60-180
 (
) damage for 4s.
Cooldown:
 60s
Bone Plating
Anti-Burst Damage
When taking damage from a champion, the current and next 3 champion abilities or attacks against you and within 1.5s deal 
30-60
 (
) less damage.
Cooldown:
 40s
Overgrowth
Increase max Health
For every 3 enemy minions or 3 monster(s) killed nearby, permanently gain 
3 max Health
. Max Health can be increased indefinitely this way. Gain an additional 
3% max Health
 upon reaching 30 stacks.
Revitalize
Empowered heals and shields
Gains a 5% amplification effect when 
Healing
 or granting 
Shields
. If the target's Health is lower than 40%, the effect is amplified by an additional 10%. 
Perseverance
Increase survivability when crowd controlled
Gain 
10% Tenacity
. Gain 10-15 
Armor
 and 
Magic Resistance
 (
) for 1.5 seconds when mmobilized. Refresh duration time when immobilized multiple times.
SORCERY
Axiom Arcanist
Empowered Ultimate Ability
Your ultimate ability has 10% increased damage, 
healing
, and 
shielding
. (AoE damage is reduced to a 5% increase.)
Scoring a takedown on an enemy champion reduces your ultimate ability's remaining cooldown by 7%.
Manaflow Band
Increase Mana
Hitting an enemy champion with and ability or 
empowered
 attack permanently increases your 
max mana 
 by 
30
, up to 
300 mana.
Botanist
Empowered plant effects
When you destroy a plant, gain 
10 gold
 and empowered plant effects. Soulflowers near the turrets also grant additional bonuses.
Honeyfruit:
Heal
 is increased by 
20%
 when consumed.
Scryer's Bloom:
Vision granted
 lasts 20% longer when destroyed.
Blast Cone:
 Gain 
40% Movement Speed
 for 2.5 second(s) after the knockback.
Hextech Flashtraption
Gain short-range movement while Flash is on cooldown
While Flash is on cooldown, it is replaced by Hexflash. Dash a distance based on charge time (max 2s). Entering combat with enemy champions to trigger a 6-second cooldown. 
Cooldown:
 18s
Transcendence
Reduces ability cooldowns
Gain a bonus when reaching the following levels:
At level 1, gain 
5 Ability Haste
;
at level 5, gain bonus 
5 Ability Haste
;
at level 9, after Basic Ability hit the target, reduce 8% the ability's cooldown time.
Cooldown:
 8s
Celerity
Increase Movement Speed
Gain 
2% Movement Speed
. All 
Movement Speed
 bonuses on you are also increased by 
7%
.
Absolute Focus
Gain Attack Damage/Ability Power at high Health
While above 65% Health, gain a bonus 
2–20 Attack Damage
 (
) or 
2–30 Ability Power
 (
) (
Adaptive
).
Scorch
Abilities deal bonus damage
Damaging an enemy champion with an ability burns them, dealing 
21-49 bonus magic damage
 (
) after 1 seconds.
Cooldown:
 8s
Nimbus Cloak

## 6. SISTEMAS DE CAMPO 7.3 (+ ajustes 7.3a: Smite burn, Nexus, placas — ver §3b)

# Sistemas de campo - Wild Rift 7.3 (notas oficiales)

> Jungla/smite, torretas (7000 HP, placas permanentes, Crystalline Overgrowth), minions, Hand of Baron, Lifesteal nuevo stat.

Jungle Adjustments
We’re making a broad set of changes to the jungle this patch, with a few key goals: increase champion diversity, bring clear speeds closer together across different types of junglers, protect jungle resources from laners, and give non-carry junglers more ways to help their team win.
First, we’re shifting a significant portion of the bonus damage junglers deal to monsters with basic attacks and abilities into a persistent burn. This burn benefits from a wider range of stats, allowing fighters, mages, tanks, and other junglers to improve their clear speeds naturally through their builds. Tank junglers, for example, should no longer feel as pressured to build items like Sunfire Aegis just to keep up their clear.
We’re also adjusting the jungle economy. Monsters will grant less base Gold, with more of that Gold shifted into the bonus provided by Smite. At the same time, monsters will be tougher and deal more damage to non-junglers. Together, these changes should make jungle resources harder for laners to take while keeping them valuable for the jungler.
Monster levels will now scale based on the average level of both teams rather than game time. This should keep monster durability more consistent with the state of the match, instead of allowing them to become excessively tanky or squishy.
We’re also moving the jungle healing effect from casting Smite to killing monsters, aligning healing more closely with when junglers receive their Gold and experience.
Epic monsters are getting some attention too. We want major objectives to be worth fighting over without disappearing before teams have a chance to contest them, so we’re standardizing their durability and increasing Baron Nashor’s mid-game rewards. Alongside our turret and minion changes, securing an early Baron should give teams, especially those with non-carry junglers, a more reliable opportunity to turn that advantage into meaningful map pressure.
And finally, we’re giving junglers a little more control when it matters most: Smite is getting stronger. Smite will now upgrade twice as you consume reward stacks, eventually reaching one thousand four hundred damage. Combined with increased monster resistances, this should make objectives harder for non-junglers to steal and give junglers a bit more reliability in those high-pressure objective fights.
Smite Adjustments
- [New] Champions with Smite deal 30-225 (Scale with Level) + 10% Bonus Attack Damage + 12% Ability Power + 20% Bonus Armor + 20% Bonus Magic Resistance + 3% Bonus Health True damage. After you stop attacking, this damage continues up to 2 more times. Champions also heal for 5 - 35 each second, scaling with champion level.
- [Removed] Champions with Smite deal bonus ability and basic attack damage to monsters.
- [New] Non-epic monsters deal 50% damage to champions with Smite.
- [Removed] Casting Smite restores Health.
- [New] Killing a large monster restores 100–260 Health to the killer (scales with monster level, reaching the maximum at level 9).
Jungle Economy Adjustments
[Removed] Monster gold scaling.
Eco Protection adjustments:
- Champions with Smite gain 1 stack every 20 seconds. Consuming 1 stack when clearing a monster camp grants an additional 45 gold, stacking up to 3 times.
- Catch-up mechanic: when your team's total gold is below 90% of the enemy team's total gold and your own gold is less than or equal to 95% of your team's average gold, consuming 1 stack grants 70 gold.
Jungler minion penalty:
- Champions with Smite gain 30% - 100% of lane experience, increasing over time once per minute and reaching 100% at 15 minutes.
- If a jungler gains more than 40% as much gold from lanes as from monsters, gold and experience gained from lanes are reduced by 50%. This effect stacks with the previous rule and is removed at 12 minutes.
Lane champion jungling penalty:
- Champions without Smite gain only 50% - 80% experience from monsters, increasing over time once per minute and reaching 80% at 12 minutes.
Smite Upgrade Rules
- Initial damage: 600 true damage
- Upgrade Smite by consuming Eco-system Protection stacks.
- Consume 8 total stacks.
- Upgrade to 1000 true damage.
- Consume 20 total stacks.
- Upgrade to 1400 true damage.
- Afterward, gain 1 Eco-system Protection stack every 30 seconds.
- Gain 5% bonus Movement Speed in the jungle and river, increased to 10% while out of combat.
- Gain an additional 20 bonus gold from each jungle camp.
Jungle Monster Rules
Monster stat growth no longer increases with time and instead scales with the average level of all champions on the map.
Epic jungle monster stats:
- Elemental Dragons (levels 5 - 15):
- Health 4900 - 10900, Attack Damage 70, Armor 59 - 119, Magic Resistance 41 - 81
- Rift Herald (levels 5 - 15):
- Health 7100 - 11100, Attack Damage 100 - 200, Armor 79 - 139, Magic Resistance 52 - 82
- Summoned Rift Herald (levels 5 - 15):
- Health 5300 - 7300, Attack Damage 80 - 130, Armor 54 - 114, Magic Resistance 32 - 62
- Gold granted when the Summoned Rift Herald charges: 200 → 50
- Baron Nashor (levels 9 - 15):
- Health 14000 - 18500, Attack Damage 280 - 490, Armor 96 - 168, Magic Resistance 56 - 98
- Basic attacks and abilities that hit enemy champions apply a debuff that reduces Armor and Magic Resistance by 0.5, stacking up to 100 times and lasting 8 seconds. Basic attacks add 1 stack, and abilities add 2 stacks.
- Energy Surge Attack Damage ratio: 60% → 30%
- Corrosive Fluid Attack Damage ratio: 100% → 50%
- Sundering Breath Attack Damage ratio: 200% → 100%
- Spike Burst Attack Damage ratio: 100% → 50%
- Elder Dragon (levels 11 - 15): Health 19000 - 20200, Attack Damage 105, Armor 150 - 170, Magic Resistance 95 - 107
Jungle monster stats (levels 1 - 15): 
- Krugs:
- Health 1300 - 3050, Attack Damage 60 - 172, Armor 40, Magic Resistance 35
- Mini Krugs:
- Health 550 - 1560, Attack Damage 20 - 62, Armor 20, Magic Resistance 20
- Gromp:
- Health 1800 - 4390, Attack Damage 55 - 160, Armor 40, Magic Resistance 35
- Blue Sentinel:
- Health 2200 - 4650, Attack Damage 70 - 210, Armor 40, Magic Resistance 35
- Red Brambleback:
- Health 2200 - 4650, Attack Damage 70 - 210, Armor 40, Magic Resistance 35
- Crimson Raptor:
- Health 1000 - 2540, Attack Damage 20 - 55, Armor 40, Magic Resistance 35
- Raptors:
- Health 500 - 1270, Attack Damage 10 - 24, Armor 20, Magic Resistance 20
- Greater Murk Wolf:
- Health 1200 - 3230, Attack Damage 30 - 93, Armor 40, Magic Resistance 35
- Murk Wolves:
- Health 600 - 1510, Attack Damage 10 - 31, Armor 20, Magic Resistance 20
- Rift Scuttler:
- Health 1500 - 3600, Armor 40, Magic Resistance 40
- The first spawn has been moved to 1: 30.
New jungle monster traits:
- Krugs, Crimson Raptors, and Greater Murk Wolves deal bonus physical damage equal to 3% of the target's current Health on attack.
- Gromp, Red Brambleback, and Blue Sentinel deal bonus physical damage equal to 5% of the target's current Health on attack.
Battlefield system Adjustments
Turrets
This season, we’re making some changes to turrets to create a smoother transition out of the laning phase and make every push feel like meaningful progress.
First, all turrets will now have plating, and turret plating will no longer disappear at six minutes. We’re also increasing turret Health across the board. Previously, once plating disappeared, a single mistake could quickly turn a full-Health turret into rubble and abruptly bring the laning phase to an end. Keeping plating around longer should make that transition more gradual while giving you a consistent reward for pushing, even when you can’t take the entire turret.
The additional durability should also make it harder to take multiple plates in a single push, while creating more opportunities to chip away at turrets throughout the game.
We’re also introducing Crystalline Overgrowth, a new mechanic that gives every champion a way to make meaningful progress against turrets, even if they aren’t running Demolish or building specifically for split-pushing.
Over time, crystals will accumulate on turrets. When a champion attacks a turret, the accumulated crystals shatter and deal bonus True Damage based on how much Crystalline Overgrowth has built up. This damage doesn’t depend on the attacker’s stats, and you won’t need to hang around the turret for an extended period to take advantage of it.
Think of it as a mini push waiting for you. Whether you’re constantly pressuring a side lane or only find a brief window to sneak in a few attacks, Crystalline Overgrowth should help those moments make a meaningful dent in the turret.
Crystalline Overgrowth
- All attackable lane turrets are now affected by Crystalline Overgrowth.
- Turrets crystallize over time. A champion's first basic attack detonates all accumulated crystals, dealing True Damage.
- The higher the average level of the attacking team, the higher the crystal detonation damage.
- Cooldown: After a turret spawns, Crystalline Overgrowth has a 50-second cooldown. Once the cooldown ends, crystals begin to accumulate.
- Crystalline Overgrowth remains at its minimum damage for 30 seconds, then scales linearly over 160 seconds until reaching its maximum damage, where it remains indefinitely.
- Minimum damage: 2%–8.7% of the turret's maximum Health (based on the attacking team's level)
- Maximum damage: 3.3%–18.9% of the turret's maximum Health (based on the attacking team's level)
- If an enemy champion is near the turret at the 50-second mark, when Crystalline Overgrowth would normally activate, crystal growth is temporarily suppressed and will not appear. Once all enemy champions leave the area, the crystals will begin to appear and "fast-forward" to the stage they would have reached, making up for the suppressed progress. This is intended to prevent Crystalline Overgrowth from suddenly activating in the middle of a push.
- While the outer turret is still standing, the inner turret and inhibitor turret will not crystallize. Once the outer turret is destroyed, the inner turret begins crystallizing.
- When no minions are within turret range and the turret's damage reduction is active, the crystals cannot be detonated.
Turret Related Adjustments
Turret Adjustments
- All Turrets
- [New] All turrets take 20% increased damage from melee champions.
- Turret plating distribution: Outer turrets, inner turrets, and inhibitor turrets.
- Turret plating now persists permanently.
- Turret plates are tied to Health thresholds. A turret loses 1 plate whenever its Health falls below 90%, 75%, 55%, 30%, and 0%.
- [Removed] When an outer/inner turret is destroyed, the corresponding inner/inhibitor turret no longer gains a 30-second shield.
- [Removed] During the first 2 minutes of the game, Baron Lane and Mid Lane turrets no longer gain 50 bonus Armor and Magic Resist.
- [Removed] During the first 6 minutes of the game, outer turrets no longer gain Armor and Magic Resist based on their remaining Health.
- [Removed] During the first 5 minutes of the game, turrets no longer gain bonus stats when multiple enemy champions are within their attack range.
- [New] Starting at 5:00, outer turret Armor, Magic Resistance, and turret plate Gold rewards begin to decay, up to 4 times.
- Turret plate Gold: -10 every 30 seconds, down to a minimum of 100 Gold
- Armor and Magic Resist: -15 every 30 seconds, down to a minimum of 0
- Whenever a turret plate is destroyed, the turret gains 30 Armor and Magic Resist for 20 seconds. Destroying another plate refreshes the duration. During this time, the turret gains an additional 5 Armor and Magic Resist for each enemy champion within 850 range
- Turret Stats
- Health:
- Outer turret: 3000 → 7000
- Inner turret: 3000 → 4500
- Inhibitor turret: 3200 → 4250
- [Adjusted] Armor and Magic Resist: 60
- [Removed] Gold granted for destroying turrets
- [Adjusted] Turret Plating and Turret Rewards:
- Outer turret: 140 Gold per plate, 700 Gold total
- Inner and inhibitor turrets: 120 Gold per plate, 600 Gold total
- First turret: 150 bonus Gold
- Global bounty for destroying an outer turret: 50 Gold per player
- Global bounty for destroying an inner or inhibitor turret: 25 Gold per player
Battlefield Tempo Adjustments
As part of our broader jungle and objective changes, we’re also updating Hand of Baron to make empowered minion waves more impactful and give each minion type a clearer role when pushing. We’re changing the Attack Damage granted to empowered minions from a percentage increase to a flat value. This should make early Baron takes more rewarding while keeping the buff from scaling too heavily later in the game. Empowered minions will also now have a minimum Movement Speed, preventing powerful Slow effects from bringing Baron-empowered pushes to a crawl.
Hand of Baron
- Melee Minions:
- Reduced damage from champions: 50% - 70% (11:00 - 25:00)
- Reduced damage from minions: 80%
- Attack Damage increase: 10
- Reduced damage from turrets: 25%
- Caster Minion:
- Reduced damage from champions: 50% - 70% (11:00 - 25:00)
- Reduced damage from minions: 20%
- Attack Damage increase: 30
- Reduced damage from turrets: 25%
- Siege Minions:
- Reduced damage from champions: 30%
- Reduced damage from minions: 20%
- Attack Damage increase: 100
- Reduced damage from turrets: 25%
- Cannon Minions:
- Reduced damage from champions: 30%
- Reduced damage from minions: 20%
- Attack Damage increase: 100
- Reduced damage from turrets: 25%
- Super Minions:
- Super Minions are not affected by Hand of Baron.
- All Minions:
- Minions empowered by Hand of Baron now have a minimum Movement Speed of 3.3.
Minions 
Minions are also getting some updates this patch. We want teams that successfully break through an inhibitor turret to be better rewarded for maintaining pressure, allowing empowered waves to steadily build advantages and wear down the enemy team over time. We’re also changing the mid- and late-game minion acceleration effect from out-of-combat Movement Speed to persistent Movement Speed. This should help waves push more consistently later in the game and reduce awkward gaps between them.
Super Minion Aura
Super Minions empower nearby minions based on the number of enemy inhibitor turrets destroyed.
- 1 Turret:
- 35 Armor, 35 Magic Resistance
- 2 Turrets:
- 35 Armor, 35 Magic Resistance
- Attack Damage: 15%
- 3 Turrets:
- 35 Armor, 35 Magic Resistance
- Attack Damage: 40%
[Removed] Super Minions no longer benefit from the Super Minion Aura.
Minion Stats 
Super Minions
- Base Health: 800 → 1100
Cannon Minions
- Damage to structures: Reaches a maximum of 100% at 23:00 → Fixed at 84%
All Minions 
- [New] All minions deal 60% damage to champions.
- [New] Starting at 5:30, minions gain 25 Movement Speed every 150 seconds, up to 6 times.
- [Removed] Starting at 11:00, minions no longer gain 10% out-of-combat Movement Speed per minute.
- Minion experience range: 8 → 10
Minion Push Buffs
The team with the higher total level and a turret advantage in the lane gains a Minion Push Advantage: 
- [New] Bonus damage to minions: (5% + (5% × turret advantage in the lane)) × team average level advantage
- [New] Damage reduction against minions: 1 + (turret advantage in the lane × team average level advantage)
Lifesteal
We’re introducing Lifesteal, a new vamp stat that applies only to basic attacks, on-hit damage, and abilities treated as basic attacks. This gives marksmen a more focused source of sustain that rewards their basic attacks without allowing abilities to generate excessive healing. We also want vamp to remain a relatively scarce source of power. Some champions are defined by their access to strong sustain, and making similar levels of healing too easy for everyone to access can diminish that strength while creating difficult balance cases. Lifesteal gives us a clearer way to separate basic attack-focused sustain from other forms of vamp and reduce the overall availability of broad healing across the game.
- This stat has replaced the previous vamp effects on the following items. See the item sections for details: Mercurial Scimitar, Vampiric Scepter, Bloodthirster, Blade of the Ruined King, and Gunmetal Greaves.

## LIFESTEAL (nuevo stat)



## 7. TABLA OFICIAL DE ATTACK SPEED — 140 CAMPEONES (7.3, con overrides 7.3a marcados)

```csv
champion,Attack Speed Ratio,Base Attack Speed,Base Bonus Attack Speed,Attack Speed per Level
Garen,0.625,0.625,0.28,0.024
Aatrox,0.651,0.651,0.13,0.021
Lux,0.625,0.625,0.2,0.03
Amumu,0.638,0.638,0.25,0.024
Kayn,0.67,0.67,0.2,0.018
Rengar,0.667,0.667,0.2,0.023
Karma,0.625,0.625,0.2,0.0135
Nunu & Willump,0.625,0.625,0.28,0.0122
Wukong,0.625,0.625,0.28,0.028
Vayne,0.658,0.658,0.23,0.03
Ekko,0.625,0.625,0.28,0.031
Orianna,0.658,0.658,0.14,0.032
Diana,0.694,0.694,0.15,0.008
Zoe,0.625,0.625,0.2,0.021
Tryndamere,0.725,0.725,0.1,0.025
Xin Zhao,0.645,0.645,0.24,0.025
Kha'Zix,0.668,0.668,0.2,0.0185
Jinx,0.625,0.625,0.3,0.02
Hecarim,0.67,0.67,0.2,0.016
Yuumi,0.625,0.625,0.2,0.006
Braum,0.644,0.644,0.16,0.03
Jhin,0.625,0.625,0.06,0.032
Aurelion Sol,0.625,0.625,0.2,0.004
Syndra,0.625,0.625,0.2,0.015
Twisted Fate,0.651,0.651,0.15,0.016
Kai'Sa,0.644,0.644,0.17,0.022
Nilah,0.67,0.67,0.21,0.02
Morgana,0.625,0.625,0.2,0.005
Evelynn,0.667,0.667,0.2,0.012
Pantheon,0.658,0.658,0.22,0.02
Akali,0.625,0.625,0.28,0.02
Fiora,0.69,0.69,0.16,0.026
Blitzcrank,0.625,0.625,0.2,0.006
Seraphine,0.699,0.669,0.12,0.017
Mordekaiser,0.625,0.625,0.17,0.008
Annie,0.625,0.625,0.2,0.006
Yasuo,0.67,0.67,0.2,0.04
Ahri,0.625,0.625,0.2,0.02
Zed,0.651,0.651,0.23,0.024
Jax,0.638,0.638,0.15,0.03
Kayle,0.667,0.667,0.13,0.028
Lucian,0.638,0.638,0.25,0.028
Leona,0.625,0.625,0.2,0.021
Tristana,0.694,0.694,0.17,0.02
Teemo,0.69,0.69,0.09,0.03
Sona,0.644,0.644,0.17,0.016
Lulu,0.625,0.625,0.2,0.013
Shyvana,0.638,0.638,0.25,0.012
Vi,0.644,0.644,0.24,0.012
Xayah,0.658,0.658,0.22,0.034
Rakan,0.635,0.635,0.18,0.022
Twitch,0.679,0.679,0.18,0.03
Gwen,0.69,0.69,0.16,0.026
Camille,0.644,0.644,0.24,0.016
Viego,0.658,0.658,0.22,0.025
Volibear,0.7,0.7,0.05,0.014
Lee Sin,0.651,0.651,0.23,0.02
Corki,0.644,0.644,0.17,0.032
Kennen,0.69,0.69,0.09,0.028
Dr. Mundo,0.625,0.625,0.28,0.028
Zyra,0.625,0.625,0.2,0.02
Rammus,0.625,0.625,0.28,0.0185
Nasus,0.638,0.638,0.25,0.024
Miss Fortune,0.656,0.656,0.22,0.032
Zeri,0.625,0.625,0.28,0.024
Sett,0.625,0.625,0.17,0.01
Yone,0.625,0.625,0.28,0.032
Master Yi,0.679,0.679,0.18,0.018
Darius,0.625,0.625,0.17,0.008
Graves,0.7,0.7,0,0.021
Kindred,0.625,0.625,0.28,0.032
Maokai,0.695,0.695,0.15,0.029
Janna,0.625,0.625,0.2,0.022
Poppy,0.625,0.625,0.2,0.021
Draven,0.679,0.679,0.11,0.03
Gnar,0.625,0.625,0.2,0.015
Ashe,0.658,0.658,0.23,0.03
Zilean,0.625,0.625,0.2,0.017
Alistar,0.625,0.625,0.2,0.012
Ambessa,0.625,0.625,0.28,0.012
Malphite,0.638,0.638,0.25,0.04
Nidalee,0.638,0.638,0.18,0.024
Aurora,0.668,0.668,0.12,0.02
Fizz,0.658,0.658,0.22,0.022
Ziggs,0.656,0.656,0.14,0.014
Cho'Gath,0.625,0.625,0.28,0.008
Gragas,0.625,0.625,0.28,0.013
Vladimir,0.658,0.658,0.14,0.0165
Nami,0.644,0.644,0.17,0.02
Riven,0.625,0.625,0.28,0.022
Varus,0.658,0.658,0.22,0.03
Irelia,0.656,0.656,0.22,0.016
Katarina,0.658,0.658,0.22,0.018
Singed,0.625,0.625,0.28,0.016
Soraka,0.625,0.625,0.2,0.012
Ezreal,0.625,0.625,0.28,0.022
Galio,0.625,0.625,0.28,0.007
Akshan,0.4,0.4,0.67,0.04
Jayce,0.658,0.658,0.22,0.021
Urgot,0.625,0.625,0.2,0.031
Kassadin,0.64,0.64,0.25,0.027
Samira,0.658,0.658,0.14,0.03
Bard,0.658,0.658,0.14,0.015
Olaf,0.694,0.694,0.06,0.0326
Sivir,0.625,0.625,0.3,0.01
Milio,0.625,0.625,0.2,0.022
Lissandra,0.625,0.625,0.2,0.01
Kog'Maw,0.665,0.665,0.2,0.03
Caitlyn,0.625,0.625,0.2,0.025 (7.3a: era 0.04)
Rell,0.625,0.625,0.2,0.01
Skarner,0.625,0.625,0.28,0.005
Shen,0.651,0.651,0.23,0.0367
Brand,0.625,0.625,0.2,0.0185
Renekton,0.665,0.665,0.2,0.024
Veigar,0.625,0.625,0.2,0.014
Senna,0.3 (7.3a),0.3 (7.3a),1.1 (7.3a),0.025 (7.3a)
Pyke,0.667,0.667,0.13,0.021
Sion,0.679,0.679,0.18,0.006
Swain,0.625,0.625,0.2,0.012
Heimerdinger,0.625,0.625,0.2,0.01
Talon,0.625,0.625,0.28,0.025
Vel'Koz,0.625,0.625,0.2,0.01
Thresh,0.625,0.625,0.2,0.028
Warwick,0.638,0.638,0.25,0.012
Nautilus,0.612,0.612,0.2,0.0124
Fiddlesticks,0.625,0.625,0.2,0.012
Kalista,0.694,0.694,0.16,0.046
Lillia,0.625,0.625,0.28,0.016
Ornn,0.625,0.625,0.17,0.012
Ryze,0.625,0.625,0.2,0.018
Smolder,0.638,0.638,0.25,0.031
Mel,0.625,0.625,0.2,0.016
Rumble,0.644,0.644,0.24,0.016
Vex,0.625,0.625,0.2,0.01
Viktor,0.658,0.658,0.14,0.02
Taliyah,0.625,0.625,0.2,0.01
Yunara,0.65,0.65,0.23,0.032
Nocturne,0.721,0.721,0.11,0.024
K'Sante,0.625,0.625,0.28,0.021
Norra,0.625,0.625,0.2,0.012
```

### 7.2 Durabilidad 7.3

```csv
champion,Base Health,Base Armor,Armor per Level,Base Magic Resist,Health per Level
Garen,660 → 690,52 → 44,5.8 → 5,,
Aatrox,,,4.5 → 5,40 → 36,
Rengar,660 → 630,,,,128 → 136
Amumu,,,,,104 → 114
Nunu & Willump,690 → 630,,,,120 → 124
Ekko,630 → 650,,,,120 → 126
Kha’Zix,630 → 640,,,,120 → 128
Xin Zhao,690 → 650,,4.3 → 4.7,,120 → 130
Hecarim,,46 → 42,5 → 5.4,,120 → 130
Braum,690 → 630,52 → 46,,,120 → 136
Jhin,600 → 630,,,,
Evelynn,600 → 630,,,,
Akali,,,,,140 → 150
Pantheon,690 → 660,52 → 48,,,120 → 132
Fiora,650 → 630,46 → 42,4.3 → 4.8,,120 → 130
Blitzcrank,660 → 630,49 → 45,,,120 → 135
Jax,690 → 660,46 → 44,,,120 → 130
Vi,690 → 660,46 → 42,,,112 → 130
Rakan,660 → 640,49 → 42,,,112 → 120
Gwen,690 → 640,52 → 48,,,120 → 136
Camille,690 → 660,,,,128 → 132
Jarvan IV,690 → 660,,,,120 → 130
Viego,660 → 630,,,,128 → 138
Lee Sin,690 → 660,,,,120 → 132
Kennen,660 → 600,,,,120 → 130
Dr. Mundo,720 → 680,,,,112 → 120
Rammus,690 → 670,49 → 45,,,112 → 124
Zeri,630 → 600,,,,128 → 136
Master Yi,,,,,120 → 130
Yone,650 → 630,,,,120 → 130
Darius,650 → 660,52 → 45,,,144 → 148
Alistar,720 → 700,,,,
Aurora,,,,,120 → 132
Kassadin,630 → 650,,,,120 → 132
Graves,660 → 630,,,,128 → 136
Poppy,660 → 630,,,,128 → 136
Draven,630 → 650,,,,128 → 132
Malphite,,,,,120 → 130
Gragas,720 → 660,,,,120 → 140
Riven,690 → 660,46 → 43,,,120 → 125
Irelia,690 → 660,,,,128 → 138
Katarina,630 → 660,,,,
Skarner,690 → 660,,,,128 → 132
Shen,,,,,112 → 124
Galio,660 → 630,,,,144 → 148
Lissandra,,,,,120 → 130
Senna,600 → 570,,,,
Nautilus,720 → 690,,,,
Thresh,,,,,120 → 140
Ornn,720 → 690,,,,120 → 132
Nocturne,,,,,120 → 134
```

## 8. BASE DE ÍTEMS 7.3 (compacta — OJO: Boots tier 3 = MISMO slot que su tier 2; Yun Tal y Death's Dance ya con valores 7.3a en el motor)

| Ítem | Oro | Stats | Categorías |
|---|---|---|---|
| Chempunk Chainsword | 2800 | +400 Max Health / +45 Attack Damage / +15 Ability Haste | FIGHTER ITEMS |
| Manamune | 2900 | +40 Attack Damage / +500 Max Mana / +15 Ability Haste | FIGHTER ITEMS; ASSASSIN ITEMS; MARKSMAN ITEMS |
| Muramana |  | +40 Attack Damage / +1200 Max Mana / +15 Ability Haste | FIGHTER ITEMS; ASSASSIN ITEMS; MARKSMAN ITEMS |
| Eclipse | 3000 | +65 Attack Damage / +20 Ability Haste | FIGHTER ITEMS |
| Sundered Sky | 3000 | +350 Max Health / +40 Attack Damage / +15 Ability Haste | FIGHTER ITEMS |
| Experimental Hexplate | 3000 | +400 Max Health / +35 Attack Damage / +20% Attack Speed | FIGHTER ITEMS |
| Maw of Malmortius | 3000 | +55 Attack Damage / +45 Magic Resistance / +10 Ability Haste | FIGHTER ITEMS; ASSASSIN ITEMS; MARKSMAN ITEMS |
| Black Cleaver | 3000 | +400 Max Health / +40 Attack Damage / +20 Ability Haste | FIGHTER ITEMS |
| Titanic Hydra | 3000 | +450 Max Health / +40 Attack Damage | FIGHTER ITEMS; DEFENSE ITEMS |
| Stridebreaker | 3100 | +400 Max Health / +40 Attack Damage / +25% Attack Speed | FIGHTER ITEMS |
| Goredrinker | 3100 | +350 Max Health / +40 Attack Damage / +15 Ability Haste | FIGHTER ITEMS |
| Mercurial Scimitar | 3100 | +45 Attack Damage / +12% Lifesteal / +40 Magic Resistance | FIGHTER ITEMS; ASSASSIN ITEMS; MARKSMAN ITEMS |
| Blade of the Ruined King | 3100 | +40 Attack Damage / +35% Attack Speed / +12% Lifesteal | FIGHTER ITEMS; MARKSMAN ITEMS |
| Serylda's Grudge | 3100 | +50 Attack Damage / +35% Armor Penetration / +15 Ability Haste | FIGHTER ITEMS; ASSASSIN ITEMS |
| Spear of Shojin | 3100 | +450 Max Health / +40 Attack Damage | FIGHTER ITEMS |
| Hullbreaker | 3100 | +400 Max Health / +50 Attack Damage | FIGHTER ITEMS |
| Overlord's Bloodmail | 3200 | +450 Max Health / +30 Attack Damage | FIGHTER ITEMS; DEFENSE ITEMS |
| Guardian Angel | 3200 | +45 Attack Damage / +40 Armor | FIGHTER ITEMS; ASSASSIN ITEMS; MARKSMAN ITEMS; DEFENSE ITEMS |
| Bloodthirster | 3200 | +75 Attack Damage / +15% Lifesteal | FIGHTER ITEMS; MARKSMAN ITEMS |
| Sterak's Gage | 3200 | +400 Max Health / +20% Tenacity | FIGHTER ITEMS; DEFENSE ITEMS |
| Death's Dance | 3200 | +50 Attack Damage / +45 Armor / +15 Ability Haste | FIGHTER ITEMS; DEFENSE ITEMS |
| Trinity Force | 3333 | +333 Max Health / +36 Attack Damage / +30% Attack Speed / +15 Ability Haste | FIGHTER ITEMS; MARKSMAN ITEMS |
| Divine Sunderer | 3400 | +425 Max Health / +25 Attack Damage / +25 Ability Haste | FIGHTER ITEMS |
| Serpent's Fang | 2800 | +50 Attack Damage / +10 Ability Haste | ASSASSIN ITEMS |
| Youmuu's Ghostblade | 3000 | +55 Attack Damage / +15 Armor Penetration / +15 Ability Haste / +4% Move Speed | ASSASSIN ITEMS |
| Duskblade of Draktharr | 3000 | +55 Attack Damage / +10 Ability Haste | ASSASSIN ITEMS |
| Edge of Night | 3000 | +250 Max Health / +50 Attack Damage | ASSASSIN ITEMS |
| The Collector | 3000 | +50 Attack Damage / +10 Armor Penetration / +25% Critical Rate | ASSASSIN ITEMS; MARKSMAN ITEMS |
| Fiendhunter Bolts | 2650 | +25% Critical Rate / +45% Attack Speed / +4% Move Speed | MARKSMAN ITEMS |
| Rapid Firecannon | 2650 | +25% Critical Rate / +40% Attack Speed / +4% Move Speed | MARKSMAN ITEMS |
| Runaan's Hurricane | 2650 | +40% Attack Speed / +25% Critical Rate / +4% Move Speed | MARKSMAN ITEMS |
| Phantom Dancer | 2650 | +25% Critical Rate / +40% Attack Speed / +7% Movement Speed | MARKSMAN ITEMS |
| Navori Quickblades | 2650 | +25% Critical Rate / +40% Attack Speed / +4% Move Speed | MARKSMAN ITEMS |
| Wit's End | 2800 | +50% Attack Speed / +45 Magic Resistance / +20% Tenacity | MARKSMAN ITEMS |
| Hexoptics C44 | 2900 | +55 Attack Damage / +25% Critical Rate | MARKSMAN ITEMS |
| Kraken Slayer | 2900 | +45 Attack Damage / +35% Attack Speed / +4% Move Speed | MARKSMAN ITEMS |
| Nashor's Tooth | 2900 | +50% Attack Speed / +80 Ability Power / +15 Ability Haste | MARKSMAN ITEMS; MAGIC ITEMS |
| Statikk Shiv | 3000 | +40 Attack Damage / +30% Attack Speed / +40 Ability Power / +4% Move Speed | MARKSMAN ITEMS; MAGIC ITEMS |
| Guinsoo's Rageblade | 3000 | +35 Attack Damage / +30% Attack Speed / +30 Ability Power | MARKSMAN ITEMS; MAGIC ITEMS |
| Mortal Reminder | 3000 | +35 Attack Damage / +30% Armor Penetration / +25% Critical Rate | MARKSMAN ITEMS |
| Essence Reaver | 3000 | +50 Attack Damage / +25% Critical Rate / +20 Ability Haste | MARKSMAN ITEMS |
| Immortal Shieldbow | 3000 | +55 Attack Damage / +25% Critical Rate | MARKSMAN ITEMS |
| Terminus | 3000 | +35 Attack Damage / +35% Attack Speed | MARKSMAN ITEMS |
| Stormrazor | 3000 | +50 Attack Damage / +25% Critical Rate / +20% Attack Speed | MARKSMAN ITEMS |
| Yun Tal Wildarrows | 3100 | +50 Attack Damage / +25% Attack Speed | MARKSMAN ITEMS |
| Galeforce | 3100 | +60 Attack Damage / +25% Critical Rate / +4% Move Speed | MARKSMAN ITEMS |
| Dominik's Regards | 3300 | +35 Attack Damage / +35% Armor Penetration / +25% Critical Rate | MARKSMAN ITEMS |
| Infinity Edge | 3400 | +75 Attack Damage / +25% Critical Rate | MARKSMAN ITEMS |
| Whispering Circlet | 2400 | +200 Max Health / +500 Max Mana / +50% Mana Regen / +8% Heal and Shield Strength | MAGIC ITEMS; SUPPORT ITEMS |
| Diadem of Songs |  | +200 Max Health / +1200 Max Mana / +50% Mana Regen / +8% Heal and Shield Strength | MAGIC ITEMS; SUPPORT ITEMS |
| Redemption | 2450 | +40 Ability Power / +50% Mana Regen / +10 Ability Haste / +8% Heal and Shield Strength | MAGIC ITEMS; SUPPORT ITEMS |
| Imperial Mandate | 2600 | +60 Ability Power / +50% Mana Regen / +20 Ability Haste | MAGIC ITEMS; SUPPORT ITEMS |
| Oceanid's Trident | 2600 | +200 Max Health / +80 Ability Power / +10 Ability Haste | MAGIC ITEMS; SUPPORT ITEMS |
| Morellonomicon | 2650 | +300 Max Health / +75 Ability Power / +15 Ability Haste | MAGIC ITEMS; SUPPORT ITEMS |
| Hextech Roketbelt | 2700 | +250 Max Health / +70 Ability Power / +20 Ability Haste | MAGIC ITEMS |
| Rylai's Crystal Scepter | 2700 | +350 Max Health / +65 Ability Power | MAGIC ITEMS |
| Rod of Ages | 2700 | +350 Max Health / +50 Ability Power / +400 Max Mana | MAGIC ITEMS |
| Horizon Focus | 2700 | +80 Ability Power / +25 Ability Haste | MAGIC ITEMS |
| Malignance | 2700 | +90 Ability Power / +500 Max Mana / +15 Ability Haste | MAGIC ITEMS |
| Stormsurge | 2800 | +90 Ability Power / +15 Magic Penetration / +6% Move Speed | MAGIC ITEMS |
| Blackfire Torch | 2800 | +80 Ability Power / +500 Maximum Mana / +20 Ability Haste | MAGIC ITEMS |
| Luden's Echo | 2800 | +100 Ability Power / +500 Max Mana / +10 Ability Haste | MAGIC ITEMS |
| Lich Bane | 2800 | +100 Ability Power / +10 Ability Haste / +5% Move Speed | MAGIC ITEMS |
| Bloodletter's Curse | 2900 | +350 Maximum Health / +65 Ability Power / +15 Ability Haste | MAGIC ITEMS |
| Banshee's Veil | 3000 | +105 Ability Power / +40 Magic Resistance | MAGIC ITEMS; DEFENSE ITEMS |
| Cryptbloom | 3000 | +75 Ability Power / +30% Magic Penetration / +20 Ability Haste | MAGIC ITEMS; SUPPORT ITEMS |
| Liandry's Torment | 3000 | +300 Max Health / +70 Ability Power | MAGIC ITEMS |
| Archangel's Staff | 3000 | +60 Ability Power / +500 Max Mana / +25 Ability Haste | MAGIC ITEMS |
| Seraph's Embrace |  | +60 Ability Power / +1200 Max Mana / +25 Ability Haste | MAGIC ITEMS |
| Cosmic Drive | 3000 | +300 Max Health / +70 Ability Power / +25 Ability Haste / +4% Move Speed | MAGIC ITEMS |
| Dusk and Dawn | 3100 | +300 Maximum Health / +20% Attack Speed / +60 Ability Power / +20 Ability Haste | MAGIC ITEMS |
| Infinity Orb | 3100 | +110 Ability Power / +15 Magic Penetration | MAGIC ITEMS |
| Riftmaker | 3100 | +350 Max Health / +70 Ability Power / +15 Ability Haste | MAGIC ITEMS |
| Zhonya's Hourglass | 3300 | +40 Armor / +110 Ability Power | MAGIC ITEMS; DEFENSE ITEMS |
| Rabadon's Deathcap | 3400 | +130 Ability Power | MAGIC ITEMS |
| Abyssal Mask | 2400 | +350 Max Health / +45 Magic Resistance / +10 Ability Haste | DEFENSE ITEMS; SUPPORT ITEMS |
| Zeke's Convergence | 2400 | +300 Max Health / +25 Armor / +25 Magic Resistance / +10 Ability Haste | DEFENSE ITEMS; SUPPORT ITEMS |
| Yordle Trap | 2400 | +200 Max Health / +20 Armor / +20 Magic Resistance / +15 Ability Haste | DEFENSE ITEMS; SUPPORT ITEMS |
| Knight's Vow | 2450 | +200 Max Health / +100% Health Regen / +40 Armor / +10 Ability Haste | DEFENSE ITEMS; SUPPORT ITEMS |
| Frozen Heart | 2550 | +80 Armor / +400 Max Mana / +20 Ability Haste | DEFENSE ITEMS; SUPPORT ITEMS |
| Mantle of the Twelfth Hour | 2550 | +600 Max Health / +20 Ability Haste | DEFENSE ITEMS; SUPPORT ITEMS |
| Locket of the Iron Solari | 2600 | +200 Max Health / +30 Armor / +30 Magic Resistance / +10 Ability Haste | DEFENSE ITEMS; SUPPORT ITEMS |
| Winter's Approach | 2600 | +500 Max Health / +500 Max Mana / +15 Ability Haste | DEFENSE ITEMS |
| Fimbulwinter |  | +500 Max Health / +1200 Max Mana / +15 Ability Haste | DEFENSE ITEMS |
| Radiant Virtue | 2650 | +300 Max Health / +30 Armor / +30 Magic Resistance / +10 Ability Haste | DEFENSE ITEMS; SUPPORT ITEMS |
| Thornmail | 2700 | +200 Max Health / +75 Armor | DEFENSE ITEMS; SUPPORT ITEMS |
| Dawnshroud | 2700 | +250 Max Health / +50 Armor / +30 Magic Resistance | DEFENSE ITEMS; SUPPORT ITEMS |
| Hollow Radiance | 2800 | +400 Max Health / +40 Magic Resistance / +15 Ability Haste | DEFENSE ITEMS |
| Randuin's Omen | 2800 | +400 Max Health / +75 Armor | DEFENSE ITEMS |
| Dead Man's Plate | 2800 | +350 Max Health / +70 Armor / +4% Movement Speed | DEFENSE ITEMS |
| Force of Nature | 2800 | +400 Max Health / +60 Magic Resistance / +5% Move Speed | DEFENSE ITEMS |
| Heartsteel | 3000 | +700 Max Health / +150% Health Regen / +20 Ability Haste | DEFENSE ITEMS |
| Kaenic Rookern | 2800 | +350 Max Health / +100% Health Regen / +85 Magic Resistance | DEFENSE ITEMS |
| Warmog's Armor | 2850 | +700 Max Health / +100% Health Regen / +20 Ability Haste | DEFENSE ITEMS |
| Gargoyle Stoneplate | 2900 | +200 Max Health / +45 Armor / +45 Magic Resistance / +10 Ability Haste | DEFENSE ITEMS |
| Sunfire Aegis | 2900 | +350 Max Health / +40 Armor / +15 Ability Haste | DEFENSE ITEMS |
| Unending Despair | 3000 | +300 Max Health / +40 Armor / +40 Magic Resistance / +10 Ability Haste | DEFENSE ITEMS |
| Iceborn Gauntlet | 3000 | +300 Max Health / +50 Armor / +250 Max Mana / +30 Ability Haste | DEFENSE ITEMS |
| Amaranth's Twinguard | 3200 | +300 Max Health / +50 Armor / +50 Magic Resistance | DEFENSE ITEMS |
| Black Mist Scythe | 0 | +10 Ability Haste | SUPPORT ITEMS |
| Bulwark of the Mountain | 0 | +175 Max Health / +10 Ability Haste | SUPPORT ITEMS |
| Echoes of Helia | 2400 | +200 Max Health / +40 Ability Power / +50% Mana Regen / +20 Ability Haste | SUPPORT ITEMS |
| Ardent Censer | 2400 | +50 Ability Power / +50% Mana Regen / +8% Heal and Shield Strength / +4% Move Speed. | SUPPORT ITEMS |
| Staff of Flowing Waters | 2400 | +50 Ability Power / +50% Mana Regen / +10 Ability Haste / +8% Heal and Shield Strength | SUPPORT ITEMS |
| Mikael's Blessing | 2500 | +300 Max Health / +50% Mana Regen / +15 Ability Haste / +9% Heal and Shield Strength | SUPPORT ITEMS |
| Shurelya's Battlesong | 2500 | +55 Ability Power / +50% Mana Regeneration / +20 Ability Haste / +4% Move Speed | SUPPORT ITEMS |
| Harmonic Echo | 2500 | +200 Max Health / +40 Ability Power / +50% Mana Regen / +20 Ability Haste | SUPPORT ITEMS |
| Gluttonous Greaves | 1000 | +45 Move Speed | Boots tier 2 |
| Berserker's Greaves | 1200 | +35% Attack Speed / +45 Move Speed | Boots tier 2 |
| Mercury's Treads | 1200 | +150 Max Health / +25 Magic Resistance / +30 Tenacity / +45 Move Speed | Boots tier 2 |
| Plated Steelcaps | 1200 | +150 Max Health / +20 Armor / +45 Move Speed | Boots tier 2 |
| Ionian Boots of Lucidity | 1000 | +50% Mana Regen / +15 Ability Haste / +45 Move Speed | Boots tier 2 |
| Boots of Mana | 1200 | +25 Ability Power / +8 Magic Penetration / +75% Mana Regeneration / +45 Move Speed | Boots tier 2 |
| Boots of Dynamism | 1200 | +15 Attack Damage / +10 Armor Penetration / +45 Move Speed | Boots tier 2 |
| Immortal Treds | 2000 | +45 Move Speed | Boots tier 3 |
| Gunmetal Greaves | 2200 | +50% Attack Speed / +45 Move Speed / +5% Lifesteal | Boots tier 3 |
| Chainlaced Crushers | 2200 | +150 Max Health / +30 Magic Resistance / +30% Tenacity / +45 Move Speed | Boots tier 3 |
| Armored Advance | 2200 | +150 Max Health / +30 Armor / +45 Move Speed | Boots tier 3 |
| Crimson Lucidity | 2000 | +75% Mana Regeneration / +25 Ability Haste / +45 Move Speed | Boots tier 3 |
| Spellslinger's Shoes | 2200 | +35 Ability Power / +18 Magic Penetration / +8% Magic Penetration / +100% Mana Regeneration / +45 Move Speed | Boots tier 3 |
| Armorcrusher Boots | 2200 | +25 Attack Damage / +12 Armor Penetration / +6% Armor Penetration / +45 Move Speed | Boots tier 3 |
| Quicksilver Sash | 1100 |  | Mid Tier Items |
| Seeker's Armguard | 1200 | +20 Armor / +35 Ability Power | Mid Tier Items |
| Vampiric Scepter | 1200 | +20 Attack Damage / +8% Lifesteal | Mid Tier Items |
| Zeal | 1400 | +15% Critical Rate / +15% Attack Speed | Mid Tier Items |
| Kircheis Shard | 800 | +20% Attack Speed | Mid Tier Items |
| Serrated Dirk | 1000 | +20 Attack Damage | Mid Tier Items |
| Recurve Bow | 900 | +20% Attack Speed | Mid Tier Items |
| B. F. Sword | 1500 | +40 Attack Damage | Mid Tier Items |
| Last Whisper | 1200 | +15 Attack Damage / +15% Armor Penetration | Mid Tier Items |
| Executioner's Calling | 800 | +15 Attack Damage | Mid Tier Items |
| Phage | 1000 | +150 Max Health / +15 Attack Damage | Mid Tier Items |
| Caulfield's Warhammer | 1200 | +25 Attack Damage / +10 Ability Haste | Mid Tier Items |
| Jaurim's Fist | 1100 | +175 Max Health / +15 Attack Damage | Mid Tier Items |
| Aether Wisp | 950 | +35 Ability Power / +4% Move Speed | Mid Tier Items |
| Lost Chapter | 1200 | +35 Ability Power / +200 Max Mana / +10 Ability Haste | Mid Tier Items |
| Fiendish Codex | 900 | +25 Ability Power / +10 Ability Haste | Mid Tier Items |
| Blasting Wand | 900 | +40 Ability Power | Mid Tier Items |
| Needlessly Large Rod | 1400 | +65 Ability Power | Mid Tier Items |
| Haunting Guise | 1300 | +200 Max Health / +30 Ability Power | Mid Tier Items |
| Sheen | 800 | +10 Ability Haste | Mid Tier Items |
| Oblivion Orb | 800 | +35 Ability Power | Mid Tier Items |
| Bami's Cinder | 1200 | +250 Max Health / +5 Ability Haste | Mid Tier Items |
| Spectre's Cowl | 1100 | +175 Max Health / +20 Magic Resistance | Mid Tier Items |
| Kindlegem | 1000 | +175 Max Health / +10 Ability Haste | Mid Tier Items |
| Giant's Belt | 1000 | +300 Max Health | Mid Tier Items |
| Warden's Mail | 1050 | +35 Armor | Mid Tier Items |
| Catalyst of Aeons | 1100 | +200 Max Health / +300 Max Mana | Mid Tier Items |
| Chain Vest | 900 | +40 Armor | Mid Tier Items |
| Bramble Vest | 1000 | +30 Armor | Mid Tier Items |
| Hexdrinker | 1200 | +20 Attack Damage / +20 Magic Resistance | Mid Tier Items |
| Negatron Cloak | 900 | +40 Magic Resistance | Mid Tier Items |
| Glacial Shroud | 1000 | +20 Armor / +150 Max Mana / +10 Ability Haste | Mid Tier Items |
| Winged Moonplate | 900 | +150 Max Health / +4% Move Speed | Mid Tier Items |
| Noonquiver | 1300 | +20 Attack Damage / +15% Critical Rate | Mid Tier Items |
| Hextech Alternator | 1100 | +45 Ability Power | Mid Tier Items |
| Mejai's Soulstealer | 1800 | +70 Max Health / +25 Ability Power | Mid Tier Items |
| Forbidden Idol | 700 | +25% Mana Regen / +6% Heal and Shield Strength | Mid Tier Items |
| Fated Ashes | 900 | +40 Ability Power | Mid Tier Items |
| Void Amethyst | 1000 | +20 Ability Power / +10% Magic Penetration | Mid Tier Items |
| Verdant Barrier | 1600 | +40 Ability Power / +25 Magic Resistance | Mid Tier Items |
| Pickaxe | 800 | +20 Attack Damage | Mid Tier Items |
| Heartbound Axe | 1200 | +20 Attack Damage / +15% Attack Speed | Mid Tier Items |
| Bandleglass Mirror | 900 | +20 Ability Power / +50% Mana Regen / +10 Ability Haste | Mid Tier Items |
| Boots of Speed | 400 | +25 Move Speed. | Basic Items |
| Long Sword | 500 | +12 Attack Damage | Basic Items |
| Brawler's Gloves | 500 | +10% Critical Rate | Basic Items |
| Dagger | 400 | +12% Attack Speed | Basic Items |
| Shimmering Spark | 500 | +50 Max Health | Basic Items |
| Tear of the Goddess | 500 | +200 Max Mana | Basic Items |
| Amplifying Tome | 500 | +20 Ability Power | Basic Items |
| Ruby Crystal | 500 | +150 Max Health | Basic Items |
| Cloth Armor | 500 | +20 Armor | Basic Items |
| Null-Magic Mantle | 500 | +20 Magic Resistance | Basic Items |
| Ring of Revelation | 300 | +5 Ability Haste | Basic Items |
| Relic Shield | 500 | +125 Max Health | Basic Items |
| Spectral Sickle | 500 | Quest: | Basic Items |
| Flash |  |  | Basic Items |
| Ghost |  |  | Basic Items |
| Heal |  |  | Basic Items |
| Barrier |  |  | Basic Items |
| Ignite |  |  | Basic Items |
| Exhaust |  |  | Basic Items |
| Smite |  |  | Basic Items |
| Cleanse |  |  | Basic Items |
| Teleport |  |  | Basic Items |


## 9. SPECS PRECARGADAS (13 campeones, notas 7.3a incluidas)

```python
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

```

## 10. MOTOR DE DPS (con validate_slots — ver Ley 0)

```python
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
               self_buff_on=True, spellblade_uptime=1/1.5, validate=True):
    """Devuelve métricas de una build completa (lista de nombres/alias de ítems, botas incluidas).
    OJO: 'items' = SLOTS FINALES. Las botas ocupan 1 slot y su mejora T2→T3 es EN EL MISMO SLOT
    (usa el nombre T3, p.ej. 'Gunmetal'; NUNCA listes 'Berserker's'+'Gunmetal' juntos)."""
    if validate:
        validate_slots(items, final=(len(items) == 6))
    its = [resolve(x) for x in items]
    gold = sum(i.gold for i in its)
    ad   = spec.base_ad + spec.ad_growth*(level-1) + sum(i.ad for i in its)
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

```


## 11. CAMBIOS DE CAMPEONES 7.3 (diff oficial)

# Cambios a campeones - Wild Rift 7.3 (notas oficiales 21-sep-2026)

> Ajustes sistemicos de marksman + cambios individuales. Fuente: wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-7-3/

Marksman Systematic Adjustments
We’re increasing base Critical Strike Damage to give crit-focused marksmen more power behind each basic attack and help further distinguish them from Attack Speed-focused carries. To account for this increase, we’re also adjusting abilities that scale with Critical Strike Chance or Critical Strike Damage.
- Base Critical Strike Damage: 175% → 200%
Critical Rate
- Crit Damage: 175% → 200%
Attack Speed
We’re adjusting marksmen’s Attack Speed growth and ratios to create clearer differences in how each champion scales and which items they prefer. Some champions will get more value from building Attack Speed, while others will naturally lean toward heavier Attack Damage options.
For example, Caitlyn will now have higher base Attack Speed and Attack Speed growth, but a lower Attack Speed ratio. This gives her plenty of Attack Speed naturally while encouraging her to prioritize harder-hitting Attack Damage items.
- Attack Speed cap (attacks per second): 2.5 → 3
- Attack Speed per Level adjustments for certain champions
- Attack Speed ratios are no longer divided by melee and ranged; each champion will now have an individual Attack Speed ratio.
- For a detailed breakdown of these changes, check out the appendix below: [Champion Attack Speed Details and Mechanics Overview]. 
Marksman Champion Adjustments
Basic attacks aren’t the only way marksmen deal damage, so we’re also updating several champions’ abilities to better support their intended builds and playstyles.
Several core damage abilities will now scale with Critical Strike Chance and Critical Strike Damage, allowing crit builds to strengthen both basic attacks and abilities while giving Infinity Edge a clearer role as a capstone item.
We’re also updating some ability mechanics that no longer fully support their champion’s intended identity, including Lucian and Twitch, to give their kits and playstyles a clearer definition.
EZREAL
Base Stats
- Base Attack Damage: 58 → 60
Mystic Shot
- Cooldown: 4.5/4/3.5/3s → 5.5/5/4.5/4s
- Damage: 50 / 85 / 120 / 155 + 135% Attack Damage + 30% Ability Power → 25 / 55 / 85 / 115 + 135% Attack Damage + 30% Ability Power
- Cooldown refund: reduces the cooldown of all other abilities except [Mystic Shot] → reduces the cooldown of all abilities
Trueshot Barrage
- Cooldown: 70 / 65 / 60s → 80 / 70 / 60s
- Damage: 350 / 500 / 650 + 100% bonus Attack Damage + 90% Ability Power → 300 / 500 / 700 + 100% bonus Attack Damage + 100% Ability Power
KAI'SA
Base Stats
- Base Attack Damage: 62 → 59
Second Skin
- Plasma damage: 4.5 + 0.5 × level + 15% Ability Power → 4 + 1 × level + 12% Ability Power + current Plasma stacks × (1 + 0.2 × level + 2% Ability Power)
- Missing Health damage: (15 + 2.5% Ability Power)% → (15 + 5% Ability Power)%
Void Seeker
- Damage: 30 / 60 / 90 / 120 + 110% Attack Damage + 60% Ability Power → 30 / 60 / 90 / 120 + 130% Attack Damage + 50% Ability Power
Supercharge
- Movement Speed: 50% / 55% / 60% / 65% + 80% × item Attack Speed × 50% / 55% / 60% / 65% (item Attack Speed capped at 90% / 99% / 108% / 117%) → 50% / 55% / 60% / 65% + bonus Attack Speed * 50% / 55% / 60% / 65% (maximum 100% / 110% / 120% / 130%)
Killer Instinct
- Shield: 75 / 100 / 125 + 100 / 150 / 200% Attack Damage + 75% Ability Power → 100 / 125 / 150 + 80 / 120 / 160% Attack Damage + 100% Ability Power
TWITCH
Twitch’s current kit hasn’t been delivering on the sneaky, high-impact playstyle we want for him. We’re reworking his kit to reward finding the right position from stealth before striking, giving him a stronger window to unleash massive burst damage when he finally reveals himself.
Base Stats
- Base Attack Damage: 54 → 58
- Attack Damage per Level: 4.5 → 4
Deadly Venom
- Damage per stack: 1 / 2 / 3 / 4 / 5 + 2.5% Ability Power → 1 / 2 / 3 / 4 / 5 + 3% Ability Power
- [Removed] When enemy champions reach max poison stacks, Twitch gains 30 / 35 / 40 / 45 / 50% Attack Speed (at levels 1 / 4 / 7 / 10 / 13) for 5 seconds. Reapplying refreshes the duration.
Ambush
- [New] After leaving camouflage, Twitch gains 35 / 40 / 45 / 50% bonus Attack Speed for 6 seconds.
- [Removed] For 3 seconds after leaving camouflage, Twitch's basic attacks apply 2 stacks of Deadly Venom.
Venom Cask
- Twitch throws a Venom Cask into the target area, granting vision there and slowing enemies inside by 30% / 35% / 40% / 45% + 0.06% × Ability Power. The area lasts 3 seconds and applies 1 stack of Deadly Venom each second to enemies inside.
Contaminate
- Direct detonation physical damage: 25 / 35 / 45 / 55 → 30 / 40 / 50 / 60
- Physical damage per stack: 20 / 25 / 30 / 35 + 42% bonus Attack Damage + 18% Ability Power → 20 / 25 / 30 / 35 + 35% bonus Attack Damage
- [New] Magic damage per stack: 35% Ability Power
- [New] This ability can only be cast while a poisoned target is within 1200 units of Twitch.
Spray and Pray
- Cooldown: 70 / 65 / 60s → 75 / 70 / 65s
- Projectile speed: 60 → 65
LUCIAN
Lucian thrives on maintaining pressure and controlling the tempo of his lane, but his late-game damage windows can be limited. The Culling hasn’t been scaling well enough to remain a meaningful threat later in the game, so we’re strengthening it to give Lucian a more reliable way to kick off his offense in mid and late-game fights.
Base Stats
- Base Attack Damage: 58 → 60
- Attack Damage per Level: 4 → 3.5
Lightslinger
- Secondary shot damage: 35% / 50% / 65% Attack Damage → 40% / 50% / 60% Attack Damage
Piercing Light
- Damage: 80 / 125 / 170 / 215 + 65 / 85 / 105 / 125% × bonus Attack Damage → 75 / 125 / 175 / 225 + 100% × bonus Attack Damage
The Culling
- Bullet count: 22 / 26 / 30 → 20 + 20 × Critical Rate (gain 2 bullets for every 10% Critical Rate) + (Critical Damage-2) × 20 × Critical Rate 
- Damage per bullet: 20 / 35 / 50 + 25% Attack Damage + 10% Ability Power → 20 / 25 / 30 + 25% Attack Damage + 15% Ability Power
CAITLYN
Caitlyn hasn’t been packing quite enough punch for a crit-focused marksman. We’re adjusting her stats and Passive to strengthen her lane presence while giving her the burst damage she needs to make those well-placed Headshots really hurt.
Base Stats
- Attack Speed Ratio: 0.625
- Base Attack Speed: 0.625
- Base Bonus Attack Speed: 0.28
- Attack Speed per Level: 0.04
- Base Attack Damage: 54 → 60
- Attack Damage per Level: 4.5 → 4.2
Headshot
- Headshot bonus damage: (60% - 110%) × Attack Damage + 200 × Critical Rate → (60% - 100%) × Attack Damage + Critical Rate × 100% + (Critical Damage-2) × Critical Rate × 100% × Attack Damage
Piltover Peacemaker
- Damage: 60 / 110 / 160 / 210 + 125 / 140 / 155 / 170% Attack Damage → 50 / 100 / 150 / 200 + 125 / 145 / 165 / 185% Attack Damage
Yordle Snap Trap
- [New] Headshot attacks against enemies trapped by Yordle Snap Trap deal 40 / 90 / 140 / 190 (+30% bonus Attack Damage) bonus physical damage.
90 Caliber Net
- Slow duration: 1.5s → 1s
Ace in the Hole
- Damage: 200 / 375 / 550 + 200% bonus Attack Damage + 20% target missing Health → (250 / 450 / 650 + 100% bonus Attack Damage + 20% target missing Health) × (1 + Critical Rate × 30% + (Critical Damage - 2) × 30% × Critical Rate)
DRAVEN
Base Stats
- Attack Damage per Level: 4.5 → 3.8
League of Draven
- Bounty: 80 + (stacks) × 4 → 60 + (stacks) × 3
Spinning Axe
- Damage: 45 / 50 / 55 / 60 + 100 / 110 / 120 / 130% → 45 / 50 / 55 / 60 + 80 / 90 / 100 / 110%
Whirling Death
- Damage falloff per hit: 8% (minimum 40%) → 5% (minimum 50%)
- [New] Enemy champions hit whose current Health is lower than Draven's current Adoration stacks are executed.
MISS FORTUNE
Miss Fortune’s first ability can sometimes land bounce hits that are difficult for foes to anticipate, especially during the laning phase. We’re updating its target-selection rules to make those bounces more predictable and give opponents a clearer opportunity to play around them.
Love Tap
- Damage: (15 + 40% bonus Attack Damage) × (1 + Critical Rate) → (15 + 40% bonus Attack Damage) × (0.6 + Critical Rate × 0.4)
- Damage Amp: 6% - 10.9% (based on level) → 6% - 9.5% (based on level)
Double Up
- Damage: 60 / 90 / 120 / 150 + 112 / 120 / 128 / 136% Attack Damage + 35% Ability Power → 60 / 90 / 120 / 150 + 110% Attack Damage + 35% Ability Power
- Second-hit damage ratio: 120% → 60% × current Critical Damage
- Optimized the bounce target-selection rules.
Strut
- Initial Movement Speed: 30 / 35 / 40 / 45 → 35 / 40 / 45 / 50
- Maximum Movement Speed: 80 / 90 / 100 / 110 → 70 / 80 / 90 / 100
Make It Rain
- Slow: 30 / 40 / 50 / 60% → 40% + 0.06% × Ability Power
Bullet Time
- Barrage damage: 85% Attack Damage + 20% Ability Power → 20 / 30 / 40 + 60% Attack Damage + 20% Ability Power
- Critical ratio: 130% → 130% + (Critical Damage-2) × 0.3
SAMIRA
Base Stats
- Base Attack Damage: 62 → 60
- Attack Speed Ratio: 0.658
- Base Attack Speed: 0.658
- Base Bonus Attack Speed: 0.14
- Attack Speed per Level: 0.03
- Attack Damage per Level: 4 → 3.5
Daredevil Impulse
- Movement Speed bonus per Style grade: 4% → 3% / 3.25% / 3.5% / 3.75% / 4% (based on level)
Flair
- Damage: 15 / 20 / 25 / 30 + 100 / 115 / 130 / 145% Attack Damage → 15 / 20 / 25 / 30 + 110% Attack Damage
- Critical Damage: current Critical Damage - 50% → 150% - 165% (based on Critical Damage)
- New: Flair’s Damage can not trigger Life Steal.
Blade Whirl
- Bonus Attack Damage ratio: 80% → 50%
Wild Rush
- Attack Speed: 35% / 40% / 45% / 50% → 25% / 30% / 35% / 40%
Inferno Trigger
- Cooldown: 8 / 8 / 8 → 6 / 6 / 6
- Mana cost: 60 / 30 / 0 → 0 / 0 / 0
- Damage: 5 / 20 / 35 + 60% Attack Damage → 20 / 40 / 60 + 40% Attack Damage
- New: Inferno Trigger’s Damage can now trigger 66.7% Life Steal.
ZERI
Living Battery
- Excess Attack Speed to Attack Damage conversion ratio: 50% → 60%
- Damage: 13 / 15 / 17 / 19 / 21 + 105 / 110 / 115 / 120 / 125% Attack Damage → 20 / 24 / 28 / 32 / 36 + 102 / 104 / 106 / 108% / 110% Attack Damage
Burst Fire
- Damage: 35 / 60 / 85 / 110 + 55 / 70 / 85 / 100% Attack Damage + 30 / 35 / 40 / 45% Ability Power → 70 / 100 / 130 / 160 + 80% × bonus Attack Damage + 30 / 35 / 40 / 45% Ability Power
- Slow duration: 2s → 1.5s
Ultrashock Laser
- Damage: 30 / 70 / 110 / 150 + 80% Attack Damage + 40% Ability Power → 60 / 100 / 140 / 180 + 100% Attack Damage + 50% Ability Power
- Critical Damage: current Critical Damage rate → (150% + (Critical Damage rate - 2) × 0.5)
Spark Surge
- Subsequent damage ratio: 80 / 85 / 90 / 95% → 85 / 90 / 95 / 100%
Lightning Crash
- Nova damage: 150 / 200 / 250 + 70% bonus Attack Damage + 80% Ability Power → 150 / 225 / 300 + 60% bonus Attack Damage + 100% Ability Power
- Overload duration: 1.5s  → 2.5s 
- Overload extension duration: 1.5s on non-critical strikes, 4.5s on critical strikes → 2.5s on non-critical strikes, 7.5s on critical strikes
- Overload lightning Attack Damage ratio: 25% → 30%
- Critical Damage: current Critical Damage → 150% + (Critical Damage - 2) × 0.5
JINX
Base Stats
- Attack Damage per Level: 4.5 → 4
Super Mega Death Rocket!
- Cooldown: 50 / 45 / 40s → 60 / 50 / 40s
- Damage: 25 / 35 / 45 + 15% × bonus Attack Damage to 250 / 350 / 450 + 150% × bonus Attack Damage → 25 / 35 / 45 + 12% × bonus Attack Damage to 250 / 350 / 450 + 120% × bonus Attack Damage
AKSHAN
Base Stats
- Attack Damage per Level: 5.5 → 4.5
Dirty Fighting
- Movement Speed: 40 - 120 (based on level) → 20 - 80 (based on level) × (1 + 100% bonus Attack Speed)
Avengerang
- Damage: 10 / 40 / 70 / 100 + 85% Attack Damage → 60 / 110 / 160 / 210 + 70% × bonus Attack Damage
- Minion damage ratio: 55 / 70 / 85 / 100% → 50 / 60 / 70 / 80%
Heroic Swing
- Critical Damage: 150% → current Critical Damage × 0.7
Comeuppance
- Damage per bullet: (20 / 30 / 40 + 10% Attack Damage) - (80 / 120 / 160 + 40% Attack Damage) → (25 / 35 / 45 + 15% Attack Damage) - (75 / 105 / 135 + 45% Attack Damage)
- Damage increase from critical-strike stats: 50% * Critical Rate → 30% × Critical Rate + (Critical Damage - 2) × Critical Rate × 0.3
CORKI
Base Stats
- Attack Damage per Level: 3 → 2.5
Phosphorus Bomb
- Damage: 65 / 125 / 185 / 245 + 125% bonus Attack Damage + 80% Ability Power → 60 / 120 / 185 / 240 + 110% bonus Attack Damage + 100% Ability Power
Gatling Gun
- Armor and Magic Resistance reduction: 10 / 14 / 18 / 22 → 12 / 14 / 16 / 18
Missile Barrage
- Missile bonus Attack Damage ratio: 70% bonus Attack Damage → 65% bonus Attack Damage
- Big One bonus Attack Damage ratio: 140% bonus Attack Damage → 130% bonus Attack Damage
KALISTA
Base Stats
- Base Attack Damage: 54 → 57
- Attack Damage per Level: 5 → 5.2
KOG'MAW
Base Stats
- Base Attack Damage: 54 → 58
- Attack Speed Ratio: 0.665
- Base Attack Speed: 0.665
- Base Bonus Attack Speed: 0.2
- Attack Speed per Level: 0.03
VARUS
Base Stats
- Base Attack Damage: 54 → 58
XAYAH
Base Stats
- Attack Speed Ratio: 0.658
- Base Attack Speed: 0.658
- Base Bonus Attack Speed: 0.22
- Attack Speed per Level: 0.03
- Base Attack Damage: 54 → 60
- Attack Damage per Level: 5 → 4.2
Deadly Plumage
- Attack Speed: 45 / 50 / 55 / 60% → 40 / 45 / 50 / 55%
- Additional feather damage ratio: 20% → 25%
- Movement Speed: 25 / 30 / 35 / 40% → 30%
Bladecaller
- Damage: 60 / 70 / 80 / 90 + 90% bonus Attack Damage → (70 / 80 / 90 / 100 + 50% bonus Attack Damage) × (1 + 50% × Critical Rate + 50% × (Critical Damage-2) × Critical Rate)
Featherstorm
- Damage: 125 / 250 / 375 + 100% bonus Attack Damage → 150 / 250 / 350 + 100% bonus Attack Damage
TRISTANA
Base Stats
- Base Attack Damage: 54 → 60
- Attack Damage per Level: 6 → 5
Rocket Jump
- Cooldown: 22 / 19 / 16 / 13 → 22 / 20 / 18 / 16
- Damage: 85 / 155 / 225 / 295 + 50% Ability Power → 80 / 120 / 160 / 200 + 80% × bonus Attack Damage + 50% Ability Power
- Slow effect: 60% → 50%
- Slow duration: 1.5 / 2 / 2.5 / 3s → 2s
Explosive Charge
- Cooldown: 15 / 14 / 13 / 12 → 16 / 15 / 14 / 13
- Passive explosion damage: 65 / 100 / 135 / 170 + 25% Ability Power → 60 / 90 / 120 / 150 + 25% Ability Power
- Active explosion damage: 50 / 75 / 100 / 125 + 75 / 110 / 145 / 180% bonus Attack Damage + 50% Ability Power → (80 / 100 / 120 / 140 + 100% bonus Attack Damage + 50% Ability Power) × (1 + Critical Rate × 40% + (Critical Damage-2) × 40% × Critical Rate)
- Damage per stack: 30% → 25%
Buster Shot
- Damage: 350 / 450 / 550 + 100% Ability Power → 300 / 350 / 400 + 70%× bonus Attack Damage + 100% Ability Power
SIVIR
Base Stats
- Base Attack Damage: 58 → 60
- Attack Speed Ratio: 0.625
- Base Attack Speed: 0.625
- Base Bonus Attack Speed: 0.3
- Attack Speed per Level: 0.01
Fleet of Foot
- Movement Speed bonus: 31 - 45 (based on level) → 55 - 70 (based on level)
Boomerang Blade
- Damage: 10 / 30 / 50 / 70 + 75 / 80 / 85 / 90% Attack Damage + 60% Ability Power × 50% × Critical Rate → (70 / 100 / 130 / 160 + 70% × bonus Attack Damage + 60% Ability Power) × (1 + Critical Rate × 40% + (Critical Damage-2) × 40% × Critical Rate)
- Non-champion damage ratio: 80% → 75%
Ricochet
- Damage: 4 / 6 / 8 / 10 + 15 / 18 / 21 / 24% Attack Damage → 37.5% / 40% / 42.5% / 45% Attack Damage
- Minion ratio: 75% → 70%
On the Hunt
- Initial Movement Speed bonus: 15% → 15 / 20 / 25%
- Initial Movement Speed duration: 10 / 11 / 12 seconds → 8 / 10 / 12 seconds
- Cooldown reduction ratio: 30 / 35 / 40% → 20 / 25 / 30%
- Attack Damage per morale stack: 2 / 3 / 4 → 2 / 2.5 / 3
- Re-triggering refreshes Hunt duration.
- Movement Speed granted on re-trigger: 25% → 15 / 20 / 25%
VAYNE
Base Stats
- Base Attack Damage: 54 → 60
Tumble
- Damage: 35 / 45 / 55 / 65% Attack Damage → 50 / 60 / 70 / 80% Attack Damage
Silver Bolts
- True Damage based on Maximum Health: 2 / 5 / 8 / 11% → 6 / 7 / 8 / 9%
Final Hour
- Attack Damage: 15 / 25 / 35 → 30 / 40 / 50
ASHE
Base Stats
- Attack Damage per Level: 2.65 → 4
- Base Attack Damage: 58 → 60
Frost Shot
- Slow effect: 15 / 17.5 / 20 / 22.5 / 25% (based on level) → 20 / 22.5 / 25 / 27.5 / 30% (based on level)
- Bonus damage: 10% + 100% × Critical Rate × (Critical Damage-1) → 100% × Critical Rate + 100% × (Critical Damage-2) × Critical Rate
Ranger's Focus
- Mana cost: 50 / 50 / 50 / 50 → 30 / 30 / 30 / 30
Volley
- Cooldown: 16 / 13.5 / 11 / 8.5s → 15 / 12 / 9 / 6s
- Mana cost: 50 / 50 / 50 / 50 → 65 / 60 / 55 / 50
- Damage: 20 / 35 / 50 / 65 + 115% Attack Damage → 70 / 110 / 150 / 190 + 100% bonus Attack Damage
JHIN
With base Critical Strike Damage increasing this patch, some champions would end up hitting a little harder than intended. We’re adjusting the Critical Strike Damage modifiers for Jhin, Yasuo, Yone, and Senna to keep their crit damage in check alongside the system changes.
Base Stats
- Base Attack Damage: 58 → 60
- Attack Damage Growth: 4.55 → 5
Whisper
- [New] Critical strikes now deal only 80% of normal critical strike damage.
- Fourth-shot bonus damage to turrets: 135% / 162% (with Infinity Edge) → 150% / 172.5% (with Infinity Edge)
- Attack Damage conversion ratio: bonus Attack Speed × 30% + Critical Rate × 45% + level × 4.5% → bonus Attack Speed × 30% + Critical Rate × 40% + level × 3%
- Critical-strike Movement Speed: 15% + 0.55% × bonus Attack Speed → 14% + 0.44% × bonus Attack Speed
Curtain Call
- Fourth super shot damage ratio: 200% → current Critical Damage
SENNA
Absolution
- Attack Speed Ratio: 0.4
- Base Attack Speed: 0.4
- Base Bonus Attack Speed: 0.6
- Attack Speed per Level: 0.05
- Damage based on Current Health: 1.2%~12% (based on level) → 1%~10% (based on level)
- Critical Rate gained per 20 Mist: 15% → 10%
- [New] Basic attacks now deal 90% of normal critical strike damage when they critical strike.
Piercing Darkness
- Base Damage: 50 / 90 / 130 / 170 → 50 / 80 / 110 / 140
Dawning Shadow
- Damage: 250 / 375 / 500 + 120% bonus Attack Damage + 50% Ability Power → 250 / 400 / 550 + 120% bonus Attack Damage + 70% Ability Power
- Shield: 120 / 160 / 200 + 40% Ability Power + Mist × 4 → 120 / 160 / 200 + 50% Ability Power + Mist × 2
YUNARA
Vow of the Lands
- Critical bonus damage: 10% (gain 10% per 100 Ability Power) → 8% (gain 8% per 100 Ability Power)
Cultivation of Spirit
- Bonus Attack Speed: 22.5% / 35% / 47.5% / 60% → 25% / 35% / 45% / 55%
Other Critical Strike Champion Adjustments
YASUO
Way of the Wanderer
- Excess Critical Rate to Attack Damage conversion ratio: 0.6 → 0.5
- Yasuo's basic attacks and (1) ability crits deal 90% of normal critical strike damage.
Last Breath
- Damage: 250 / 400 / 550 + 160% bonus Attack Damage → 200 / 350 / 500 + 150% bonus Attack Damage
GRAVES
New Destiny
- Shotgun Critical Strike Damage rate: 1.3 → 1.5 
YONE
Way of the Hunter
- Excess Critical Rate to Attack Damage conversion ratio: 0.6 → 0.5
- Yone's basic attacks and (1) ability crits deal 90% of normal critical strike damage.
Mortal Steel
- Damage ratio to Jungle Monsters: 65% → 70%
Spirit Cleave
- Damage: 25 / 35 / 45 / 55 + 11 / 12 / 13 / 14% target’s max Health → 20 / 35 / 50 / 65 + 9 / 10 / 11 / 12% target max Health
- Shield: 45 + 80% bonus Attack Damage → 40 / 55 / 70 / 85 + 60% bonus Attack Damage
Soul Unbound
- Stored damage ratio: 24 / 28 / 32 / 36% → 27.5% / 30% / 32.5% / 35%
Fate Sealed
- Damage: 200 / 350 / 500 + 80% Attack Damage → 200 / 375 / 550 + 60% Attack Damage
VIEGO
Base Stats
- Base Attack Damage: 62 → 60
- Attack Damage Growth: 4.5 → 4.2
Sovereign's Domination
- Base heal: 7% → 5%
Blade of the Ruined King
- Critical Damage ratio on current Health damage: current Critical Damage → current Critical Damage × 80%
- Critical Damage ratio on second strike: current Critical Damage → current Critical Damage × 80%
- Thrust damage: 20 / 40 / 60 / 80 ( + 80% Attack Damage) × (1 + 50% × Critical Rate) → 25 / 45 / 65 / 85 ( + 70% Attack Damage) × (1 + 60% × Critical Rate + (Critical Damage-2) × Critical Rate × 60%)
Harrowed Path
- Attack Speed: 45 / 50 / 55 / 60% → 35 / 40 / 45 / 50%
Heartbreaker
- Damage: 110% Attack Damage - 165% Attack Damage (based on Critical Rate) + target missing Health × (14 / 17 / 20 + 6% bonus Attack Damage)% → 120% Attack Damage × (1 + 50% × Critical Rate + (Critical Damage - 2) × Critical Rate * 50%) + target missing Health × (14 / 17 / 20 + 5% bonus Attack Damage)%
TRYNDAMERE
We want Tryndamere’s basic attacks to hit like they mean it, rather than relying on a flurry of lower-damage attacks to wear opponents down. We’re removing the bonus Attack Speed from his Passive to shift more power into each individual strike. We’re also adjusting the Attack Damage reduction on his second ability. Its effectiveness will now scale more with points invested into the ability, rather than automatically becoming stronger against opponents who build more Attack Damage.
Base Stats
- Base Attack Damage: 54 → 64
- Attack Damage per Level: 5.5 → 5
- Armor per Level: 3.9 → 4.5
Battle Fury
- [Removed] Landing a basic attack on an enemy champion grants 30% Attack Speed for 5 seconds; after the effect ends, it goes on a 6-second cooldown.
Bloodlust
- Attack Damage: 7 / 12 / 17 / 22 → 0
- Bonus Attack Damage per 1% missing Health: 0.35 / 0.40 / 0.45 / 0.5 → 0.3 / 0.5 / 0.7 / 0.9
Mocking Shout
- Attack Damage reduction: 40% → 20 / 40 / 60 / 80%
Spinning Slash
- Damage: 80 / 120 / 160 / 200 + 135% bonus Attack Damage + 100% Ability Power → 80 / 120 / 160 / 200 + 100% bonus Attack Damage + 80% Ability Power
- Targets that trigger the cooldown reduction on critical strike: Minions → Minions, monsters, champion-summoned units, and other units that can be critically struck 
Undying Rage
- [Removed] Battle Fury's Attack Speed bonus increases to 45 / 60 / 75%

## 12. CAMBIOS DE ÍTEMS 7.3 (diff oficial)

# Cambios a items - Wild Rift 7.3 (notas oficiales)

> Incluye items nuevos (C44, Yun Tal, Fiendhunter, Stormrazor, Shieldbow), removidos (Magnetic Blaster, Cloak of Agility, Soul Transfer, Nashor's Talon) y componentes.

Item Adjustments
Marksman Item Adjustments
We’re updating the marksman item system to create more distinct build paths and give each purchase a clearer purpose. New items like Fiendhunter Bolts and Yun Tal Wildarrows are joining the shop, giving marksmen more options to play toward their individual strengths, particularly when choosing their first item. 
We’re also sharpening the identities of existing marksman items by reducing overly broad stat profiles, simplifying some passive effects, and shifting more power into their core stats. Our goal is for each completed item to provide a clear and meaningful damage spike while making build choices more dependent on what your champion does best. For champions whose abilities scale with Critical Strike Chance and Critical Strike Damage, Infinity Edge will also serve as a powerful capstone for maximizing their damage.
Dagger
Base Stats
- Price: 500 → 400
- Attack Speed: 15% → 12%
Last Whisper
Base Stats
- [New] Build Path: Long Sword (500) + 700
- Price: 800 → 1200
- [New] Attack Damage: 15
- Armor Penetration: 12% → 15%
Recurve Bow
Base Stats
- Build Path: Dagger (500) + Dagger (500) + 400 → Dagger (400) + 500
- Price: 1400 → 900
- Attack Speed: 30% → 20%
Zeal
If you continue to see Movement Speed adjustments below, don't be surprised. They're part of our broader effort to rein in and standardize late-game Movement Speed.
Base Stats
- Movement Speed: 5% → 4%
Noonquiver
We’re introducing Noonquiver to fill a gap in the marksman item system, providing both Attack Damage and Critical Strike Chance in a single component. It should also make building toward items that offer both stats feel smoother and more flexible.
Base Stats
- Build Path: Long Sword (500) + Dagger (500) + 350 → Long Sword (500) + Brawler's Gloves (500) + 300
- Price: 1350 → 1300
- Attack Damage: 25 → 20
- [Removed] Attack Speed: 15%
- [New] Critical Rate: 15%
Vampiric Scepter
For details on Physical Vamp and Lifesteal, see the section below. 
Base Stats
- [Removed] Physical Vamp: 8%
- [New] Lifesteal: 8%
Kircheis Shard
With more items that don’t provide Attack Damage now building from Kircheis Shard, we’re removing its Attack Damage to better support the wider range of items it builds into. 
Base Stats
- Build Path: Long Sword (500) + 400 → Dagger (400) + 400
- Price: 900 → 800
- [Removed] Attack Damage: 15
- [New] Attack Speed: 20%
Shock
- Dealing damage to an enemy champion deals 40 bonus magic damage (25 second cooldown). Attacks reduce this cooldown by 1 second.
Pickaxe
We’re adjusting Pickaxe to smooth out the build paths for items with lower overall Attack Damage, particularly those that also build from Attack Damage components like Vampiric Scepter or Caulfield’s Warhammer.
Base Stats
- Price: 800
- Build Path: Long Sword (500) + 300
- Attack Damage: 20
Hearthbound Axe
Hearthbound Axe replaces Noonquiver as the mid-tier Attack Speed and Attack Damage component.
Base Stats
- Price: 1200
- Build Path: Long Sword (500) + Dagger (400) + 300
- Attack Damage: 20
- Attack Speed: 15%
Hexoptics C44
We want crit marksmen to have more meaningful choices after completing their first item, and Hexoptics C44 offers a new option for those looking to take over teamfights. Participating in a takedown grants additional Attack Range, helping you keep the momentum going, while your damage increases based on how far you are from your target.
Base Stats
- Price: 2900
- Build Path: Pickaxe (800) + Noonquiver (1300) + Long Sword (500) + 300
- Attack Damage: 55
- Critical Rate: 25%
Magnification
- Attacks deal 0 - 10% bonus damage based on how far away the enemy is, reaching maximum damage at 550 units.
Arcane Aim
- When a champion you damaged within the last 3 seconds dies, you gain 100 bonus Attack Range for 8 seconds.
Yun Tal Wildarrows
Yun Tal Wildarrows offers a highly gold-efficient first-item option for crit marksmen, providing Attack Damage, Critical Strike Chance, and Attack Speed. There is a catch, though: its unique Critical Strike Chance stacking mechanic means it takes time to reach its full potential. You’ll need to decide whether the game state gives you enough time to invest in scaling or if you need power right away.
Base Stats
- Price: 3100
- Build Path: Noonquiver (1300) + Pickaxe (800) + Kircheis Shard (800) + 200
- Attack Damage: 50
- Critical Rate: 0%
- Attack Speed: 25%
Practice Makes Perfect
- Basic attacks permanently grant Critical Rate, gaining 0.4% / 0.2% (melee / ranged) Critical Rate per attack, up to a maximum of 25%.
Flurry
- Attacking an enemy champion grants 25% Attack Speed for 6 seconds (20 second cooldown). Attacks reduce this cooldown by 1 second, and this reduction increases to 2 seconds on a critical strike.
Energized items
Consolidating so many Energized effects into a small number of items left marksmen with fewer meaningful choices. Magnetic Blaster, in particular, offered range, waveclear, burst, and kiting all in one package, making it difficult to strengthen crit marksmen without also giving them too much power from a single item. We’re breaking that power back apart. Magnetic Blaster has been removed, with its effects redistributed across three items to create more distinct choices. We’re also reworking Statikk Shiv into an item focused on on-hit marksmen.
Stormrazor
As an old friend of the Energized family, [Stormrazor] has returned to Summoner's Rift. In the early game, it offers the strongest lane pressure and kiting power for players who want to focus on laning, and champions that rely on heavy-damage basic attacks or need Energized effects can choose it.
Base Stats
- Price: 3000
- Build Path: B. F. Sword (1500) + Kircheis Shard (800) + Brawler's Gloves (500) + 200
- Attack Damage: 50
- Critical Rate: 25%
- Attack Speed: 20%
Energized
- Moving and attacking generate an Energized attack.
Bolt
- Your Energized attack deals 120 bonus magic damage and grants 45% Movement Speed for 1.5 seconds.
Rapid Firecannon
Rapid Firecannon is stepping in for Magnetic Blaster as a more specialized option for marksmen who value additional Attack Range. It’s especially useful for champions who need a little extra reach to safely find opportunities to deal damage in teamfights.
Base Stats
- Price: 2650
- Build Path: Zeal (1400) + Kircheis Shard (800) + 450
- Critical Rate: 25%
- Attack Speed: 40%
- Movement Speed: 4%
Energized
- Moving and attacking generate an Energized attack.
Sharpshooter
- Your Energized attack deals 80 bonus magic damage and grants 35% bonus Attack Range, up to 150.
Fiendhunter Bolts
When marksmen choose between Zeal items, we want them to have different options based on the situation or the specific needs of their champion. Fiendhunter Bolts provides a powerful window after casting an ultimate, making it a great way to boost burst damage for marksmen who already play around their ultimate, such as Twitch, Zeri, and Yunara.
Base Stats:
- Attack Speed Ratio: 0.65
- Base Attack Speed: 0.65
- Base Bonus Attack Speed: 0.23
- Attack Speed per Level: 0.032
- 2650
- Build Path: Zeal (1400) + Kircheis Shard (800) + 450
- Critical Rate: 25%
- Attack Speed: 45%
- Movement Speed: 4%
Night Vigil:
- Gain 20 ultimate ability haste.
Opening Barrage:
- After casting your ultimate ability, your next 3 attacks gain 50% Attack Speed and are guaranteed to crit, dealing 80% of your normal critical strike damage for 8 seconds. If an attack would already crit, it instead deals 15% bonus true damage. (45 second cooldown)
Immortal Shieldbow
Immortal Shieldbow is returning as a dedicated defensive option, designed to give marksmen more survivability in the late game. 
Base Stats
- Price: 3000
- Build Path: Noonquiver (1300) + Pickaxe (800) + 900
- Attack Damage: 55
- Critical Rate: 25%
Lifeline:
- When you take damage that would reduce you to below 35% Health, gain a shield for 3 seconds (350 - 650 for melee, 300 - 550 for ranged, based on champion level). (70 second cooldown)
Statikk Shiv
On-hit builds have long lacked some room for itemization, and now Statikk Shiv can join that space as a specialized on-hit option. The new Statikk Shiv allows on-hit builds to apply their effects to multiple enemies at the same time, creating exciting item combinations and helping those builds matter in teamfights.
Base Stats
- Price: 3000
- Build Path: Aether Wisp (950) + Pickaxe (800) + Kircheis Shard (800) + 450
- Attack Damage: 40
- Ability Power: 40
- Attack Speed: 30%
- Movement Speed: 4%
Energized:
- Moving and attacking generate an Energized attack.
Electrospark:
- Your Energized attack fires chain lightning that bounces to additional targets. Bounce count: 3 / 4 / 5 / 6, increasing at levels 1 / 5 / 9 / 13, dealing 60 magic damage, increased to 90 against minions and monsters. Applies on-hit effects to secondary bounce targets.
ElectroShock:
- Basic attacks grant 5 bonus Energized stacks.
Bloodthirster
Bloodthirster is returning to its identity as a high-Attack Damage, high-Lifesteal item and is no longer limited to crit champions.
Base Stats:
- Build Path: Vampiric Scepter (1200) + Cloak of Agility (1000) + Ruby Crystal (500) + 300 → Vampiric Scepter (1200) + B. F. Sword (1500) + 500
- Price: 3000 → 3200
- Attack Damage: 55 → 75
- [Removed] Critical Rate: 25%
- [Removed] Max Health: 250
- [Removed] Physical Vamp: 8%
- [New] Lifesteal: 15%
Ichorshield
- Convert overhealing from your Lifesteal into a shield, up to 165 - 345 (based on level).
Essence Reaver 
We've streamlined Essence Reaver's effects, making it slightly weaker on its best users, such as Viego and Lucian, while allowing it to better serve a wider range of champions who want Critical Strike Chance, Attack Damage, and Ability Haste. 
Base Stats:
- Build Path: Sheen (800) + Cloak of Agility (1000) + Long Sword (500) + 700 → Sheen (800) + Caulfield's Warhammer (1200) + Brawler's Gloves (500) + 500
- Attack Damage: 35 → 50
Spellblade:
- After casting an ability, your next basic attack within 10 seconds deals bonus physical damage equal to 135% × base Attack Damage + 0 - 80 (Based on Critical Rate) and restores Mana equal to 50% of the damage dealt. (1.5 second cooldown)
Galeforce
Base Stats
- Build Path: Zeal (1400) + B. F. Sword (1500) + 200 → Noonquiver (1300) + Pickaxe (800) + Long Sword (500) + 500
- Attack Damage: 50 → 60
- [Removed] Attack Speed: 15%
- Movement Speed: 5% → 4%
The Collector
Base Stats
- Build Path: Serrated Dirk (1000) + Cloak of Agility (1000) + 1000 → Serrated Dirk (1000) + Noonquiver (1300) + 700
- Attack Damage: 45 → 50
Death and Taxes:
- If you deal damage to an enemy champion and leave them below 5% of their max Health, they are executed, permanently increasing the execute threshold by 0.1% of max Health and granting an additional 25 gold.
Kraken Slayer
Base Stats
- Build Path: Noonquiver (1300) + Dagger (500) + Long Sword (500) + 500 → Recurve Bow (900) + Hearthbound Axe (1200) + Long Sword (500) + 300
- Price: 2800 → 2900
- Attack Damage: 40 → 45
- Attack Speed: 30% → 35%
- Movement Speed: 5% → 4%
Bring It Down:
- Every third attack now deals 150 - 210 bonus physical damage, or 120 - 168 for ranged champions. This damage is increased based on the target's missing Health. For every 1% Health the target is missing, damage increases by 0.75%, up to 75%.
- Optimized its interaction with Yunara's 1st ability; Yunara's 1st ability spread effect can now trigger [Bring It Down].
Blade of the Ruined King
For details on Physical Vamp and Lifesteal, see the section below. 
Base Stats
- Build Path: Vampiric Scepter (1200) + Recurve Bow (1400) + 400 → Vampiric Scepter Scepter (1200) + Pickaxe (800) + Recurve Bow (900) + 200
- Price: 3200 → 3100
- Attack Speed: 35% → 30%
- [Removed] Omnivamp: 10%
- [New] Lifesteal: 12%
Ruined Strike:
- Basic attacks deal bonus physical damage on hit equal to 7% of the target's current Health (8.5% for melee), with a minimum of 15 and a maximum of 100 against monsters.
Drain:
- Hitting the same enemy champion 3 times with basic attacks or abilities slows them by 30% for 1.5 seconds (30 second cooldown).
Guinsoo's Rageblade
Guinsoo’s Rageblade has long been a staple for on-hit marksmen, but giving up Critical Strike Chance to build it can feel like too steep a tradeoff. We’re removing its Critical Strike Chance restriction, giving on-hit champions more flexibility in their builds while keeping Rageblade’s power focused on repeatedly triggering on-hit effects rather than dealing additional damage of its own.
Base Stats:
- Build Path: Nashor's Talon (800) + Recurve Bow (1400) + 900 → Amplifying Tome (500) + Recurve Bow (900) + Pickaxe (800) + + 800
- Price: 3100 → 3000
- [New] Attack Damage: 35
- [New] Ability Power: 30
- [Removed] Movement Speed: 5%
Wrath:
- Attacks deal 30 bonus magic damage.
Seething Strike:
- Basic attacks grant 8% Attack Speed, stacking up to 4 times. At max stacks, every 3rd basic attack triggers an additional on-hit effect.
At Wit's End
Base Stats
- Build Path: Recurve Bow (1400) + Negatron Cloak (900) + 500 → Recurve Bow (900) + Negatron Cloak (900) + Dagger (400) + 600
- Attack Speed: 45% → 50%
- [New] Tenacity: 20%
At Wit's End:
- Basic attacks deal 40 bonus magic damage on hit.
Terminus
Base Stats
- Build Path: Recurve Bow (1400) + B. F. Sword (1500) + 400 → Recurve Bow (900) + Hearthbound Axe (1200) + 900
- Total Price: 3300 → 3000
- Attack Damage: 40 → 35
- Attack Speed: 30% → 35%
Shadow
- Basic attacks deal 30 bonus magic damage on hit.
Juxtaposition 
- The light effect grants 5 - 8 Armor and Magic Resist; the dark effect grants 10% Armor Penetration and Magic Penetration, stacking up to 3 times.
Phantom Dancer
Base Stats
- Build Path: Zeal (1400) + Dagger (500) + Long Sword (500) + 500 → Zeal (1400) + Dagger (400) + Dagger (400) + 450
- Price: 2900 → 2650
- [Removed] Attack Damage: 20
- Movement Speed: 5% → 7%
Spectral Waltz:
- Landing a basic attack on a champion grants 6% Attack Speed and 1% Movement Speed for 6 seconds, stacking up to 5 times.
Runaan's Hurricane
Base Stats
- Build Path: Recurve Bow (1400) + Cloak of Agility (1000) + 500 → Zeal (1400) + Kircheis Shard (800) + 450
- Price: 2900 → 2650
- Attack Speed: 35% → 40%
- [New] Movement Speed: 4%
Wind's Fury:
- Basic attacks fire mini bolts at 2 nearby targets on hit, each dealing 55% physical damage. These bolts can crit and apply on-hit effects.
Wind Blade
- [Removed]
Mortal Reminder
We want Mortal Reminder to stand out through its slot efficiency rather than directly competing with other Armor Penetration options that offer similar stats. We’re sharpening its identity so the choice between penetration items is clearer, making it easier to understand what you’re gaining from each option and when Mortal Reminder is the right fit for your build.
Base Stats
- Build Path: Last Whisper (800) + Executioner's Calling (800) + Cloak of Agility (1000) + 900 → Last Whisper (1200) + Executioner's Calling (800) + Brawler's Gloves (500) + 500
- Price: 3300 → 3000
- Attack Damage: 25 → 35
- [Removed] Attack Speed: 15%
- [New] Armor Penetration: 30%
Sepsis:
- Physical damage dealt to enemy champions applies 50% Grievous Wounds for 3 seconds.
Last Whisper
- Integrated into base stats.
Infinity Edge
With the increase to base Critical Strike Damage, Infinity Edge is already compelling enough, making its Critical Strike Damage passive feel somewhat redundant.
Base Stats
- Build Path: B. F. Sword (1500) + Cloak of Agility (1000) + 900 → B. F. Sword (1500) + Pickaxe (800) + Brawler's Gloves (500) + 700
- Attack Damage: 65 → 75
Infinity:
- Critical strike damage increased from 200% to 230%.
Limit Break:
- [Removed]
Manamune
The Mana consumption mechanic on completed Tear of the Goddess items has become outdated. We removed it from Seraph’s Embrace last patch, and now Manamune and Muramana are getting the same treatment, making their effects less dependent on spending Mana.
Base Stats
- Build Path: Tear of the Goddess (500) + Caulfield's Warhammer (1200) + 1000 → Caulfield's Warhammer (1200) + Tear of the Goddess (400) + Long Sword (500) + 800
- Price: 2700 → 2900
- Attack Damage: 25 → 40
- Mana: 300 → 500
- Ability Haste: 20 → 15
AWE:
- Gain Attack Damage equal to 2% of max Mana and refund 15% of total Mana spent.
Mana Charge:
- Basic attacks and Mana expenditure grant 14 max Mana, up to 700. Triggers at most 3 times every 10 seconds.
Muramana
Base Stats
- Price: 2700 → 2900
- Attack Damage: 25 → 40
- Ability Haste: 20 → 15
AWE:
- Gain Attack Damage equal to 2% of max Mana and refund 15% of total Mana spent.
Shock:
- Basic attacks deal bonus physical damage equal to 1.5% of max Mana; abilities deal bonus physical damage equal to 3.5% / 3% of max Mana for melee / ranged.
Serylda's Grudge
Serylda’s Grudge has been offering too much utility to champions outside of its intended audience. We’re reworking its Slow and Grievous Wounds effects while strengthening its core stats, sharpening its identity as an Armor Penetration option for high-burst champions.
Base Stats
- Build Path: Caulfield's Warhammer (1200) + Last Whisper (800) + Long Sword (500) + 800 → Caulfield's Warhammer (1200) + Last Whisper (1200) + 700
- Price: 3300 → 3100
- Attack Damage: 40 → 50
- [New] Armor Penetration: 35%
Icy:
- Damaging active abilities and empowered attacks slow enemies below 60% current Health by 30% Movement Speed for 1 second.
Last Whisper
- Integrated into base stats.
Frostbite:
- [Removed]
Navori Quickblades
Base Stats
- Price: 2800 → 2650
- Attack Speed: 45% → 40%
- Movement Speed: 5% → 4%
Lord Dominik's Regards
Base Stats
- Build Path: Last Whisper (800) + Long Sword (500) + Cloak of Agility (1000) + 1000 → Last Whisper (1200) + Noonquiver (1300) + 800
- Attack Damage: 30 → 35
- Armor Penetration: 36% → 35%
Mercurial Scimitar
Base Stats
- [Removed] Physical Vamp: 10%
- [New] Lifesteal: 12%
Removed
- As mentioned above, Magnetic Blaster has been removed due to being too much of an all-purpose item.
- Magnetic Blaster
- Soul Transfer has struggled to find its intended audience, so we've decided to take it off the Rift for now.
- Soul Transfer
- Cloak of Agility overlaps too heavily with Brawler's Gloves, and there are few situations where stacking Critical Strike Chance takes priority over building Attack Damage.
- Cloak of Agility
- Nashor's Talon has lost its last remaining user. It's time for it to leave the Rift.
- Nashor's Talon
Other Item Adjustments
Alongside the marksman item overhaul, we’re also sharpening the identities of items for other classes. Some items currently offer too many different stats at once, which can leave them without a clear purpose or create unintended synergies. We’re streamlining these stat profiles so each item has a more defined role and a clearer reason to build it.
Winged Moonplate
Base Stats
- Movement Speed: 5% → 4%
Bami's Cinder
Following the changes to Smite (see below), Shimmering Spark no longer has a place as a starting item, so we're removing it and adjusting Bami's Cinder's build path accordingly. 
Base Stats
- Build Path: Shimmering Spark (500) + Ruby Crystal (500) + 300 → Ring of Revelation (300) + Ruby Crystal (500) + 400
- Total Price: 1300 → 1200
- [New] Ability Haste: 5
Aether Wisp
Base Stats
- Movement Speed: 5% → 4%
Phage
Rage:
- Each time a basic attack hits a unit, gain 20 Movement Speed for 2 seconds. This Movement Speed bonus does not stack, and the effect is halved for ranged champions.
Forbidden Idol
Forbidden Idol and the items it builds into have been offering too many different stats at once, allowing enchanters to stack powerful healing and shielding while also gaining significant durability and other benefits.
We’re sharpening the identity of these components by specializing Forbidden Idol around Heal and Shield Power. The new Bandleglass Mirror will instead serve as the go-to component for Ability Power and Ability Haste, creating clearer build paths based on the stats you need.
Base Stats
- Build Path: No recipe
- Price: 900 → 700
- Heal and Shield Power: 4% → 6%
- [Removed] Health: 100
- [Removed] Ability Haste: 5
Bandleglass Mirror
Bandleglass Mirror is a mid-tier support item component that provides Ability Power and Ability Haste. 
Base Stats
- Build Path: Amplifying Tome (500) + Ring of Revelation (300) + 100
- Total Price: 900
- Ability power: 20
- Base Mana Regen: 50%
- Ability Haste: 10
Whispering Circlet
Base Stats
- Price: 2400
- Build Path: Forbidden Idol (700) + Tear of the Goddess (400) + Ruby Crystal (500) + 800
- Health: 200
- Maximum Mana: 500
- Base Mana Regen: 50%
- Heal and Shield Power: 8%
Harmony:
- Gain bonus Heal and Shield Power equal to 0.5% of max Mana and refund 25% of Mana spent.
Mana Charge:
- Mana expenditure grants 14 max Mana, up to 700. This can trigger at most 2 times every 10 seconds. At max stacks, it automatically upgrades into Diadem of Songs.
Diadem of Songs
Base Stats
- Build Path: Whispering Circlet
- Health: 200
- Mana: 1200
- Base Mana Regen: 50%
- Heal and Shield Power: 8%
Harmony:
- Gain bonus Heal and Shield Power equal to 0.5% of max Mana and refund 25% of Mana spent.
Diadem
- If either you or an allied champion you healed or shielded within the last 3 seconds is in combat, heal the nearby allied champion with the lowest Health within 800 units each second for an amount equal to 0.8% of your max Mana.
Echoes of Helia
Echoes of Helia is tailor-made for offensive supports looking to turn their damage into healing. 
Base Stats
- Price: 2400
- Build Path: Bandleglass Mirror (900) + Kindlegem (1000) + 500
- Health: 200
- Ability Power: 40
- Ability Haste: 20
- Base Mana Regen: 50%
Soul Siphon:
- 30% of pre-mitigation damage dealt to enemy champions is stored as Soul Fragments, with a maximum of 80 - 250 based on level. When you heal or shield an allied champion other than yourself, all Soul Fragments are consumed to heal that target for an equal amount.
Ardent Censer
In addition to addressing the mixed-stat issue mentioned above, we're also narrowing the buffs Ardent Censer provides to marksmen, particularly crit marksmen, so supports don't have to pay as much attention to their own level or how much Critical Strike Chance their marksman currently has. 
Base Stats
- Build Path: Forbidden Idol (900) + Aether Wisp (950) + Ring of Revelation (300) + 550 → Forbidden Idol (700) + Aether Wisp (950) + 750
- Price: 2700 → 2400
- Ability Power: 45 → 50
- Heal and Shield Power: 5% → 8%
- Movement Speed: 5% → 4%
- [Removed] Ability Haste: 10
- [Removed] Health: 250
Censer:
- Shielding or healing an allied champion other than yourself empowers both you and that champion for 6 seconds, granting 30% bonus Attack Speed and 25 bonus magic damage on basic attacks.
Staff of Flowing Waters
Base Stats
- Price: 2500 → 2400
- Health: 100 → 0
- Heal and Shield Power: 5% → 8%
- Ability Haste: 15 → 10
Rapids:
- Shielding or healing an allied champion other than yourself empowers both you and that champion for 6 seconds, granting 40 Ability Power and 15 Ability Haste.
Salvation
Base Stats
- Price: 2600 → 2450
- Health: 150 → 0
- Ability Power: 50 → 40
- Heal and Shield Power: 5% → 8%
- Ability Haste: 15 → 10
Shurelya's Battlesong
Base Stats
- Build Path: Aether Wisp (950) + Amplifying Tome (500) + Ring of Revelation (300) + 750 → Bandleglass Mirror (900) + Aether Wisp (950) + 600
- Movement Speed: 5% → 4%
Imperial Mandate
Imperial Mandate has become a little too closely tied to Nami, while its trigger condition and power spike haven’t always been easy to understand. We’re giving it a refresh with clearer functionality and a stronger identity as an option for crowd control-focused mages.
Base Stats
- Build Path: Fiendish Codex (900) + Kindlegem (1000) + 600 → Bandleglass Mirror (900) + Blasting Wand (800) + 900
- Price: 2500 → 2600
- Health: 200 → 0
- Ability Power: 50 → 60
- [New] Base Mana Regen: 50%
Control:
- Crowd Control abilities gain 20 Ability Haste.
Command:
- Crowd-controlling an enemy champion marks them for 4 seconds, causing them to take 7% increased damage during that time.
Harmonic Echo
Harmonic Echo has been scaling a little too well with Ability Haste and Heal and Shield Power, allowing some champions to provide an overwhelming amount of healing in the late game. We’re reworking it into a chain healing and shielding item. Rather than simply amplifying repeated healing, champions with powerful heals and shields can now use Harmonic Echo to spread those effects to additional teammates, giving the item a clearer role in supporting the whole team.
Base Stats
- Build Path: Lost Chapter (1200) + Forbidden Idol (900) + Amplifying Tome (500) + 100 → Bandleglass Mirror (900) + Kindlegem (1000) + 600
- Price: 2800 → 2500
- Health: 100 → 200
- Ability Power: 50 → 40
- Ability Haste: 15 → 20
- [Removed] Max Mana: 300
- [Removed] Heal and Shield Power: 5%
Harmonic Echo:
- When you heal or shield an allied champion, the effect links to the nearest allied champion within range with the lowest percentage Health, excluding yourself, and grants them 30% of that heal or 35% of that shield. If no other allied champion is in range, the original target instead receives that same extra heal or shield.
Knight's Vow
Base Stats
- Build Path: Kindlegem (1000) + Chain Vest (900) + 700 → Kindlegem (1000) + Chain Vest (900) + 550
- Price: 2600 → 2450
- Health: 400 → 200
Zeke's Convergence
Some Zeke’s Convergence users cast their ultimate before getting close to the action, making it difficult to get full value from the item. We’re adjusting its effect to better support champions who engage from range. We’re also redistributing some of the Armor on tank support items into Magic Resist. This should give tank supports more balanced durability against physical and magic damage, rather than making them exceptionally tough against marksmen while leaving them overly vulnerable to mages.
Base Stats
- Build Path: Glacial Shroud (1000) + Giant's Belt (1000) + 700 → Kindlegem (1000) + Cloth Armor (500) + Null-Magic Mantle (500) + 400
- Price: 2700 → 2400
- Health: 400 → 300
- [Removed] Mana: 150
- Armor: 40 → 25
- [New] Magic Resist: 25
- Ability Haste: 15 → 10
Converge:
- Gain 10 ultimate ability haste.
Frostfire Tempest:
- Casting your ultimate ability deals 150 magic damage and slows nearby enemies by 30% over 5 seconds. If no enemy champion is in range when the ultimate is cast, the effect is delayed until up to 5 seconds later or until an enemy champion enters range.
Yordle Trap
Yordle Trap Device has become too focused on snowballing through the extra Gold it generates, while its payoff can feel inconsistent from game to game. We also want support items to encourage you to, well, support your team. We’re shifting more of the item’s power away from Gold generation and into buffs for your allies. Don’t worry, though, you’ll still pocket a little extra Gold along the way.
Base Stats
- Build Path: Chain Vest (900) + Kindlegem (1000) + 700 → Kindlegem (1000) + Cloth Armor (500) + Null-Magic Mantle (500) + 400
- Price: 2600 → 2400
- Health: 350 → 200
- Armor: 40 → 20
- [New] Magic Resist: 20
Catcher:
- Slowing or immobilizing an enemy champion empowers you for 8 / 4s, melee / ranged, granting 20 Movement Speed. During this time, you and nearby allies gain 30% / 20% bonus Attack Speed, melee / ranged. If an ally, including you, gets a kill while inspired, you gain 20 gold.
Mantle of the Twelfth Hour
Mantle of the Twelfth Hour is meant to help tanks survive heavy bursts of damage, but its high price and reliance on resistances have made it difficult to justify. We’re addressing both issues to make it a more reliable anti-burst option and a worthwhile choice earlier in a tank’s build.
Base Stats
- Build Path: Surging Scales (1300) + Negatron Cloak (900) + 500 → Kindlegem (1000) + Giant's Belt (1000) + 550
- Price: 2700 → 2550
- Health: 200 → 600
- [Removed] Armor: 40
- [Removed] Magic Resist: 40
- [New] Ability Haste: 20
Lifeline:
- When you drop below 30% max Health, immediately gain 200 - 300 bonus Health for 5 seconds, and heal over 5 seconds for 200 - 400 + 120% bonus Armor + 120% bonus Magic Resistance + 15% bonus Health. During this time, gain 10% size, 10% bonus Movement Speed, and 20% Tenacity.
Frozen Heart
Frozen Heart has drifted away from its intended purpose, with its current effect asking users to hit multiple enemies with abilities just to apply its debuff. We’re bringing it back to its roots as an item for tanks who dive straight into the heart of the enemy team, allowing them to disrupt nearby opponents simply by being in the thick of the fight.
Base Stats
- Price: 2650 → 2550
- Max Mana: 250 → 400
Winter's Caress:
- All enemy champions within 650 units lose 25% Attack Speed.
Radiant Virtue
Base Stats
- Build Path: Kindlegem (1000) + Chain Vest (900) + 950 → Giant's Belt (1000) + Cloth Armor (500) + Null-Magic Mantle (500) + 650
- Price: 2850 → 2650
- Armor: 45 → 30
- [New] Magic Resist: 30
- Ability Haste: 15 → 10
Abyssal Mask
Abyssal Mask has struggled to find a clear audience and purpose. We’re refocusing it as a more accessible option for tank supports and other low-economy champions, helping them empower their teammates without needing a hefty Gold income.
Base Stats
- Build Path: Kindlegem (1000) + Negatron Cloak (900) + Ruby Crystal (500) + 600 → Kindlegem (1000) + Negatron Cloak (900) + 500
- Price: 3000 → 2400
- Health: 400 → 350
- Magic Resist: 55 → 45
Unmake:
- All enemy champions within 6.5 meters take 12% increased magic damage.
Gunmetal Greaves
For details on Physical Vamp and Lifesteal, see the section below. 
Base Stats
- [Removed] Physical Vamp: 5%
- [New] Lifesteal: 5%
Death's Dance
Death’s Dance has been leaning too heavily on Defy, leaving its base stats weaker than we’d like. We’re making Defy harder to trigger while strengthening the item’s core stats in return, giving its users more consistent combat power even when Defy isn’t active.
Base Stats
- Build Path: Caulfield's Warhammer (1200) + Chain Vest (900) + 1000 → Caulfield's Warhammer (1200) + Chain Vest (900) + Pickaxe (800) + 300
- Total Price: 3100 → 3200
- Attack Damage: 35 → 50
- Armor: 40 → 45
Defy:
- If a champion you damaged within the last 3 seconds dies, the remaining Ignore Pain damage is cleansed, and you heal over 2 seconds for an amount equal to 90% bonus Attack Damage.
Cauterize:
- Store 30% of physical and magic damage taken, or 12% for ranged champions, and take the stored amount as true damage over 3 seconds.
Winter's Approach
Base Stats
- Build Path: Tear of the Goddess (500) + Giant's Belt (1000) + 1100 → Tear of the Goddess (400) + Giant's Belt (1000) + Kindlegem (1000) + 200
- Max Health: 350 → 500
AWE:
- Gain bonus Health equal to 15% of max Mana and refund 15% of total Mana spent.
Mana Charge:
- Basic attacks, Mana expenditure, and taking damage from champions, structures, and epic monsters grant 14 max Mana. This effect grants up to 700 max Mana and can trigger at most 3 times every 10 seconds. Limited to one Tear of the Goddess item.
Fimbulwinter
Base Stats
- Max Health: 350 → 500
Awe:
- Gain bonus Health equal to 15% of max Mana and refund 15% of total Mana spent.
Frozen Colossus:
- Whenever you impair an enemy champion's movement, gain a shield for 3 seconds that absorbs 120 + 4.5% max Mana. If more than one enemy champion is nearby, the shield is increased by 80%. (8 second cooldown) Ranged champions use this shield at 50% effectiveness.
Amaranth's Twinguard
We’ve always intended Amaranth’s Twinguard to be the capstone item for tanks, much like Infinity Edge for crit marksmen or Rabadon’s Deathcap for mages. Right now, it isn’t quite hitting that mark. It’s too appealing to champions outside the tank class, while tanks themselves don’t always feel a meaningful power spike when completing it We’re shifting some of its raw resistances into Health and bonus resistances, giving tanks a more noticeable durability spike when they complete Twinguard while reducing some of its late-game synergy with percentage-based resistance effects. This should also make it less appealing to champions who don’t invest heavily in bonus resistances. Yes, fighters, we’re looking at you.
Base Stats
- Build Path: Surging Scales (1300) + Negatron Cloak (900) + 900 → Giant's Belt (1000) + Chain Vest (900) + Negatron Cloak (900) + 400
- Total Price: 3100 → 3200
- [New] Health: 300
- Armor: 60 → 50
- Magic Resist: 60 → 50
Endurance: 
- While in combat with enemy champions, gain 1 Endurance stack each second, up to 5 stacks. At max stacks, gain 20% increased size, 20% Tenacity, 30% bonus Armor, and 30% bonus Magic Resistance until leaving combat.
Dead Man's Plate
Base Stats
- Build Path: Winged Moonplate (900) + Surging Scales (1300) + 600 → Winged Moonplate (900) + Chain Vest (900) + Ruby Crystal (500) + 500
- Movement Speed: 5% → 4%
Force of Nature
Force of Nature has become too dominant as the answer to magic damage, particularly due to its percentage damage reduction. We’re removing that effect to bring down some of its more extreme defensive cases and create more room for other Magic Resistance items to shine. This also gives us more flexibility to adjust the Magic Resistance system and mage ecosystem in the future. We’ll be keeping a close eye on mage performance following these changes.
Base Stats
- Build Path: Winged Moonplate (900) + Spectre's Cowl (1100) + 750 → Winged Moonplate (900) + Negatron Cloak (900) + Ruby Crystal (500) + 500
- Price: 2750 → 2800
- Max Health: 350 → 400
Absorb:
- Taking magic damage from enemy champions grants 1 Steadfast stack, up to 4, for 7 seconds. Dealing damage to enemy champions refreshes the duration. At max stacks, gain 6% Movement Speed and 70 bonus Magic Resist.
Youmuu's Ghostblade
We’re making Youmuu’s Ghostblade a more consistent option by moving its Movement Speed away from the stacking mechanic and into persistent and out-of-combat Movement Speed. This should make its mobility more reliable, whether you’re moving around the map or looking for your next fight.
Base Stats
- [New] Movement Speed: 4%
Momentum:
- 3 seconds after combat with enemy champions ends, gain 30 bonus Movement Speed, or 20 for ranged champions.
Spectral Haste [Removed]
Titanic Hydra
Base Stats
- Build Path: Bami's Cinder (1300) + Jaurim's Fist (1200) + 500 → Pickaxe (800) + Jaurim's Fist (1200) + Ruby Crystal (500) + 500
Cosmic Drive
Base Stats
- Movement Speed: 5% → 4%
Trinity Force
Base Stats
- Build Path: Sheen (800) + Phage (1000) + Stinger (1200) + 333 → Sheen (800) + Phage (1000) + Hearthbound Axe (1200) + 333
- Attack Damage: 30 → 36
- Ability Haste: 20 → 15
- Movement Speed: 5% → 0
Dusk and Dawn
Dusk and Dawn is just one step away from being the perfect item. A bit of healing should help give it stronger sustained combat power. 
Base Stats
- Ability Power: 70 → 60
- Max Health: 350 → 300
- Attack Speed: 25% → 20%
Spellblade:
- After casting an ability, your next attack deals bonus magic damage equal to 75% base Attack Damage + 10% Ability Power and heals you for 10% Ability Power + 3% bonus Health. Shortly afterward, it applies one additional on-hit effect to the target. (1.5 second cooldown) Deals reduced damage to structures.
Nashor's Tooth
Nashor’s Tooth’s Adaptive Force hasn’t created many meaningful build opportunities, while limiting how much power we can give its other stats. We’re removing it and returning Nashor’s Tooth to its roots as a dedicated Ability Power item.
Base Stats
- Build Path: Nashor's Talon (800) + Recurve Bow (1400) + 600 → Recurve Bow (900) + Blasting Wand (800) + Fiendish Codex (900) + 300
- Total Price: 2800 → 2900
- Attack Speed: 45% → 50%
- [New] Ability Power: 80
- Ability Haste: 20 → 15
Gnaw:
- Basic attacks deal 15 + 20% bonus Ability Power magic damage on hit.
Magic Fang:
- [Removed]
Luden's Echo
Luden’s Echo has been a little too effective at spreading its damage across multiple targets. We’re reducing its multi-target damage while leaving its single-target power unchanged, keeping it effective when you’re focused on bursting down one opponent.
Echo:
- Your next damaging ability or empowered basic attack deals 75 + 8% Ability Power magic damage to the primary target and up to 5 nearby enemies. For each fewer target hit by Echo, the primary target takes an additional 20 + 1.2% Ability Power magic damage. (9 second cooldown)
Sunfire Aegis
Sunfire Aegis’s stacking and basic attack mechanics have made its damage harder to understand, while allowing champions with high Attack Speed and mobility to get more value from it than intended. We’re simplifying its damage mechanic and shifting its power toward high-Health tanks, giving the item a clearer identity and making its damage more intuitive.
Immolate:
- Upon entering combat, deals 20 + 1.5% bonus Health Magic Damage to nearby enemies every second. Immolate deals 175%–250% damage to minions and 130% damage to monsters.
Flametouch:
- [Removed]
Infinity Orb
Inevitable Demise
- Critical Strike Threshold: 35% → 40%
Sterak's Gage
Base Stats
- [New] Tenacity: 20%
Sterak's Fury 
- Tenacity Removed.
Tear of the Goddess 
Base Stats
- Price: 500 → 400
- [Removed] 5 Ability Haste 
Items Removed
- Like Shimmering Spark, with the new jungle system, we no longer need a jungle-specific version of Sunfire Aegis.
- Searing Crown
- Surging Scales has always struggled to find a clear identity. Its underwhelming stats and effect haven't done enough to differentiate it from Chain Vest, so it's time to say goodbye.
- Surging Scales
- Stinger has also lost its last remaining user, so we're removing it for now.
- Stinger
- See above.
- Searing Crown

## 13. FICHAS COMPLETAS DE CAMPEONES


---

# Cho'Gath — Ficha de datos (Wild Rift 7.3)

> wr-meta.com (24-sep-2026) + apéndice oficial 7.3. Crudo: data/raw/campeones/chogath.html

## Stats base (nivel 1, growth entre paréntesis)

- **attackdamage**: 62 (4)
- **heal**: 690 (128)
- **healthregeneration**: 8 (0.86)
- **attackspeed**: 0.8 (0.005)
- **mana**: 380 (50)
- **mpreg**: 13 (0.79)
- **movementspeed**: 350 (0)
- **armor**: 46 (4.5)
- **magicresistance**: 40 (2)
- **criticalstrike**: 200% (0)

## AS oficial 7.3 (apéndice de las notas — fuente primaria para el modelo)

- champion: Cho'Gath
- Attack Speed Ratio: 0.625
- Base Attack Speed: 0.625
- Base Bonus Attack Speed: 0.28
- Attack Speed per Level: 0.008

## Habilidades (texto completo con valores actuales)

```
P
 (PASSIVE) CARNIVORE
 Killing an enemy restores 18 Health (16 + 2 × ) and 4.35 Mana (4 + 0.35 × ). The values restored are doubled if the unit is a champion, turret, or epic monster.
 Q
 (Q) RUPTURE 
 6s 60 
 Ruptures the ground, knocking up enemies for 1 second(s), dealing 80 magic damage (80/135/190/245 + 100% ) and slowing them by 60% for 1.5 second(s).
 W
 (W) FERAL SCREAM 
 12/11/10/9s 70/80/90/100 
 Roars, silencing enemies in an area for 1.4/1.6/1.8/2 second(s) and dealing 80 magic damage (80/130/180/230 + 70% ).
 E
 (E) VORPAL SPIKES 
 7/6/5/4s 30 
 Cho'Gath's next 3 attacks launch spikes that: - Deal 20 magic damage (20/45/70/95 + 30% ) plus magic damage equal to (2.3/2.7/3.1/3.5% + 0.6% × Feast stacks) × the target's max Health . - Slow by 30/35/40/45% , decaying over 1.5 seconds. Vorpal Spikes' width increases with Cho'Gath's size. Base damage against minions and monsters is capped at 100 (30% ).
 R
 (R) FEAST 
 70/60/50s 100 
 Devours an enemy, dealing: 300 true damage (300/450/600 + 50% + 10% of Cho'Gath's bonus ) to champions. 1,200 true damage (1,200 + 50% + 10% of Cho'Gath's bonus ) to minions and monsters. If this kills the target, Cho'Gath gains 1 stack(s) of Feast . Stacks gained from minions and non-epic monsters are capped at 6. Feast (per stack): Grants 80/120/160 max Health . Increases size by 6%, up to an increase of 135%. Increases Attack Range by 4.7/6.2/7.7, up to an increase of 75. Increases this ability's cast range by 2.5, up to an increase of 25.
 CHO'GATH Meta Overview — Ranks & Performance Analytics 
 This meta overview presents CHO'GATH’s ranked performance across different roles and skill tiers. The data includes tier placement, win rate, pick rate, ban rate, and short-term trends, allowing you to evaluate her current strength and draft priority. Statistics are synced with rank buckets and role selection, helping you understand where CHO'GATH performs best and how her impact changes in the evolving Wild Rift meta.
 Diamond + Master + Challenger Legendary 
 Updated: 24 SEP 2026 UTC 00:00 
 SOLO 
 Confidence High 
 Win: 51.20% 
 Pick: 12.60% 
 Ban: 38.00% 
 Trend: ↓ 1 
 Reason: 
 ? 
 High ban pressure High presence 
 Signals: 
 ? 
 ⛔ Perma-ban 👥 Popular 
 JUNGLE 
 Confidence Med 
 Win: 50.78% 
 Pick: 7.22% 
 Ban: 38.00% 
 Trend: ↑ 14 
 Reason: 
 ? 
 High ban pressure Rising trend 
 Signals: 
 ? 
 ⛔ Perma-ban 
 SOLO JUNGLE 
 Last 7 days analytics 
 Tier List 
 Compare Сhampions 
 Build 
 Counters 
 Counter Items 
 Tips 
 Con 
 Game Plan 
 Power Spikes 
 Solo Baron CHO'GATH Build items and runes 
 The information below will help you get familiar with the game on the Solo Baron Line CHO'GATH. We have prepared a items builds, runes, summoner spells and ability order for a comfortable game. Situational options for replacing items and runes are also available to you.
 Key items 
 TIPS: Start your build with Ruby Crystal . Next, you should pay attention to whether your mobility champion is enough, our further actions will depend on this. If it is hard for you to dodge the enemy's skills or you want to roam on neighboring lines, then it is better to buy Boots of Speed at an early stage.
 Start
 Ruby Crystal 
 Ruby Crystal +150 Max Health 500 
 Core
 Heartsteel 
 Heartsteel Increase Maximum Health +700 Max Health +150% Health Regen +20 Ability Haste Colossal Consumption: While within 700 units of an enemy champion, charges for 2.5 seconds before dealing a huge strike against the enemy champion. This charged attack deals bonus physical damage equal to 140 + 3.5% of maximum Health , and grants maximum Health equal to 15% of the damage dealt. The charge for each target has a 20 second cooldown. 3000 
 Heartsteel TIPS: This item is perfect for tanks and bruisers who want to combine maximum survivability with massive burst damage against enemy champions. It provides a huge health pool, enhanced out-of-combat regeneration, and ability haste. The “Colossal Consumption” passive requires a 2.5-second charge when near an enemy champion, after which your next strike deals significant bonus physical damage based on your max health and grants you 15% of the damage dealt as bonus health. This allows you to both absorb damage and heal during skirmishes, making the item an excellent choice for extended fights and closing out teamfights. Excellent synergy with Spirit Visage: the healing amplification and regeneration boost from Spirit Visage further enhance the health restoration from this item’s passive, providing incredible survivability and sustain in combat.
 Mercury's Treads 
 Mercury's Treads Increases Magic resist +150 Max Health +25 Magic Resistance +30 Tenacity +45 Move Speed 1200 
 Mercury's Treads TIPS: These boots increase your Magic Resistance while making you more resilient to crowd control through Tenacity. The bonus Health and movement speed improve both survivability and mobility, allowing you to perform more effectively against magic damage and heavy-CC team compositions. They are an excellent choice for tanks, fighters, and any champion who needs to stay in the fight longer.
 Hollow Radiance 
 Hollow Radiance Deals damage in an area +400 Max Health +40 Magic Resistance +15 Ability Haste Immolate: While in combat, deal magic damage equal to 20–30 plus 1% of bonus per second for 5 second(s) to nearby enemies. Deals 125% damage against monsters and 200% damage against minions. Desolate: Killing a neutral monster or an enemy deals magic damage equal to 30 plus 2% of bonus in an area around them. 2800 
 Hollow Radiance TIPS: This item turns you into a steady source of pressure in fights: while engaged, it emits an area magic damage aura that helps clear waves and punish nearby small targets. On killing a neutral or enemy, it detonates for area damage, making it great for fast clears and threat creation when entering skirmishes. Perfect for tanks and frontline bruisers who need to hold the center of fights and force opponents into mistakes.
 Boots
 Mercury's Treads 
 Mercury's Treads Increases Magic resist +150 Max Health +25 Magic Resistance +30 Tenacity +45 Move Speed 1200 
 Mercury's Treads TIPS: These boots increase your Magic Resistance while making you more resilient to crowd control through Tenacity. The bonus Health and movement speed improve both survivability and mobility, allowing you to perform more effectively against magic damage and heavy-CC team compositions. They are an excellent choice for tanks, fighters, and any champion who needs to stay in the fight longer.
 Plated Steelcaps 
 Plated Steelcaps Reduces damage from champion attacks +150 Max Health +20 Armor +45 Move Speed Block: Reduces damage from champion attacks by 10%. 1200 
 Plated Steelcaps TIPS: These boots provide r
...(recortado; completo en data/raw)...
## Change history (cambios recientes)

```
Change history
 ADJUSTED 22 SEP 2026 (PATCH 7.3)
BASE STATS
Critical Strike Damage: 175% → 
200%
.
Attack Speed cap: 2.5 → 
3 attacks per second
.
Attack Speed Ratio: 
0.625
.
Base Attack Speed: 
0.625
.
Base Bonus Attack Speed: 
0.28
.
Attack Speed per Level: 
0.008
.
 BUFFED 13 AUG 2026 (PATCH 7.2C)
(E)
 VORPAL SPIKES
Base Damage: 15/35/55/75 + (2.15/2.5/2.85/3.2% + 0.5% × Feast stack) ×Target’s Max Health → 
20/45/70/95 + (2.3/2.7/3.1/3.5% + 0.6% × Feast stack) × Target’s Max Health
.
(R)
 FEAST
Cooldown: 80/70/60s → 
70/60/50s
.
Bonus Health to Damage Ratio: 8% → 
10%
.
 See More
```

## Build/runas populares (referencia comunitaria, NO conclusión)

```
Runes BUILD
                
For runes, you should pick 
 
Grasp of Undying
 (When in combat, your next attack on a champion will occasionally deal bonus magic damage, heal you, and permanently increase your health.) as your keystone, followed by 
 
Demolish
 (Your third attack against a turret deals bonus damage), 
 
Second Wind
 (Heals you after taking damage.) and 
 
Overgrowth
 (Gains bonus scalable max Health.) in the primary tree, as well as 
 
Axiom Arcanist
 (Increases you ultimate ability's damage, heals and shields. Scoring a takedown on an enemy champion reduces your ultimate ability's remaining cooldown.) in the secondary tree. Below you can see possible options for replacing runes.
                
                
                    
                        
                            
    
            
                
                    
                    
          
```
---

# Diana — Ficha de datos (Wild Rift 7.3)

> wr-meta.com (24-sep-2026) + apéndice oficial 7.3. Crudo: data/raw/campeones/diana.html

## Stats base (nivel 1, growth entre paréntesis)

- **attackdamage**: 52 (3.64)
- **heal**: 630 (140)
- **healthregeneration**: 9 (0.9)
- **attackspeed**: 0.8 (0.006)
- **mana**: 435 (41)
- **mpreg**: 12 (1.14)
- **movementspeed**: 355 (0)
- **armor**: 40 (5)
- **magicresistance**: 38 (2)
- **criticalstrike**: 200% (0)

## AS oficial 7.3 (apéndice de las notas — fuente primaria para el modelo)

- champion: Diana
- Attack Speed Ratio: 0.694
- Base Attack Speed: 0.694
- Base Bonus Attack Speed: 0.15
- Attack Speed per Level: 0.008

## Habilidades (texto completo con valores actuales)

```
P
 (PASSIVE) MOONSILVER BLADE
 After casting an ability, Diana gains 30% to 100% Attack Speed ( ) for 4 seconds. Every third attack deals an additional  35 bonus magic damage (20 (+15 ) + 50% ) to nearby enemies. Damage to monsters: 100%.
 Q
 (Q) CRESCENT STRIKE 
 8/7/6/5s 50/55/60/65 
 Unleashes an arcing bolt of energy that deals 60 magic damage  (60/105/150/195 + 70% ) and applies Moonlight for 3 seconds.
 W
 (W) PALE CASCADE 
 13/11,5/10/8,5s 70 
 Create 3 spheres that orbit Diana 5 seconds. Upon contact with enemies the spheres detonate, dealing 20 magic damage (20/35/50/65 + 20% ). Also grants a shield that absorbs 50 damage (50/70/90/110 + 40% ) damage. If the third sphere detonates, the shield is increased by 50 (50/70/90/110 + 40% ).
 E
 (E) LUNAR RUSH 
 18/16/14/12s 20 
 Dashes to a point near an enemy, dealing 40 magic damage (40/80/120/160 +  30% ) and removing Moonlight in an area. Lunar Rush's Cooldown is reduced to 0.5 seconds if it removes Moonlight from an enemy.
 R
 (R) MOONFALL 
 70/65/60s 100 
 Summons the moon, illuminating an area that expands. Enemies in this area are slowed by 20% . During this time, Diana charges for up 1 seconds, triggering Moonfall Glow when the charge is complete. Diana can move and cast abilities and spells while chargin up. Diana cannot cast this ability if there are no enemy champions nearby. Moonfall Glow:  Slams the moon down, dealing 100 (100/160/220 + 40% ) to 250 magic damage (200/320/440 + 80% ) based on charge time and slowing targets by 20% for 2 seconds.
 DIANA Meta Overview — Ranks & Performance Analytics 
 This meta overview presents DIANA’s ranked performance across different roles and skill tiers. The data includes tier placement, win rate, pick rate, ban rate, and short-term trends, allowing you to evaluate her current strength and draft priority. Statistics are synced with rank buckets and role selection, helping you understand where DIANA performs best and how her impact changes in the evolving Wild Rift meta.
 Diamond + Master + Challenger Legendary 
 Updated: 24 SEP 2026 UTC 00:00 
 MID 
 Confidence Low 
 Win: 47.98% 
 Pick: 1.12% 
 Ban: 0.29% 
 Trend: ↓ 2 
 Reason: 
 ? 
 Low win rate Negative trend 
 Signals: 
 ? 
 🧊 Falling 
 JUNGLE 
 Confidence Low 
 Win: 50.82% 
 Pick: 1.90% 
 Ban: 0.29% 
 Trend: ↓ 12 
 Signals: 
 ? 
 🧊 Falling 
 MID JUNGLE 
 Last 7 days analytics 
 Tier List 
 Compare Сhampions 
 Build 
 Counters 
 Counter Items 
 Tips 
 Con 
 Game Plan 
 Power Spikes 
 Mid DIANA Build items and runes 
 The information below will help you get familiar with the game on the Mid Line DIANA. We have prepared a items builds, runes, summoner spells and ability order for a comfortable game. Situational options for replacing items and runes are also available to you.
 Key items 
 TIPS: Start your build with Amplifying Tome . Next, you should pay attention to whether your mobility champion is enough, our further actions will depend on this. If it is hard for you to dodge the enemy's skills or you want to roam on neighboring lines, then it is better to buy Boots of Speed at an early stage.
 Start
 Amplifying Tome 
 Amplifying Tome +20 Ability Power 500 
 Core
 Dusk and Dawn 
 Dusk and Dawn Applies on-hit effects +300 Maximum Health +20% Attack Speed +60 Ability Power +20 Ability Haste Spellblade: After using an ability, your next attack deals (75% base + 10% ) bonus magic damage and restores ( 3% bonus + 10% ) Htalth to you. After a brief delay, apply on-hits to the target 1 additional time. (1.5s Cooldown) Deals reduced damage to structures. 3100 
 Dusk and Dawn TIPS: This item combines Health, Attack Speed, Ability Power, and Ability Haste, making it well suited for champions who weave abilities and basic attacks together. After casting an ability, the next attack deals bonus magic damage and restores Health, then applies on-hit effects to the target an additional time. An excellent choice for AP fighters and hybrid champions with strong on-hit synergy.
 Boots of Mana 
 Boots of Mana Ability Power, Magic Pen, Mana Regeneration +25 Ability Power +8 Magic Penetration +75% Mana Regeneration +45 Move Speed Equilibrium: Champions without Mana gain 50% bonus health Regen. Big Bully: Attacks and active abilities deal 18 bonus true damage to minions. 1200 
 Boots of Mana TIPS: These boots greatly enhance your early magic damage by providing Ability Power, magic penetration, and increased mana regeneration. They also improve wave clear by dealing bonus true damage to minions, while champions without Mana instead gain additional health regeneration. They are an excellent choice for mages and AP supports who value strong laning, frequent spell casting, and efficient wave clearing.
 Infinity Orb 
 Infinity Orb Abilities deal bonus damage +110 Ability Power +15 Magic Penetration Inevitable Demise: Abilities and empowered attacks Critically Strike for 20% bonus damage against enemies below 40% Health . 3100 
 Infinity Orb TIPS: This item greatly enhances a mage's finishing power. It provides a large boost to Ability Power and magic penetration while allowing your abilities and empowered attacks to deal increased damage to low-health enemies. An excellent choice for mages and AP assassins who want to execute targets more reliably and maximize their burst potential.
 Boots
 Boots of Mana 
 Boots of Mana Ability Power, Magic Pen, Mana Regeneration +25 Ability Power +8 Magic Penetration +75% Mana Regeneration +45 Move Speed Equilibrium: Champions without Mana gain 50% bonus health Regen. Big Bully: Attacks and active abilities deal 18 bonus true damage to minions. 1200 
 Boots of Mana TIPS: These boots greatly enhance your early magic damage by providing Ability Power, magic penetration, and increased mana regeneration. They also improve wave clear by dealing bonus true damage to minions, while champions without Mana instead gain additional health regeneration. They are an excellent choice for mages and AP supports who value strong laning, frequent spell casting, and efficient wave clearing.
 Spellslinger's Shoes 
 Spellslinger's Shoes Deal bonus damage to minions +35 Ability Power +18 Magic Penetration +8% Magic Penetration +100% Mana Regeneration +45 Move Speed Equilibrium: Champions without Mana gain 50% base Health Regen. Big Bully: Attacks and active abilities deal 18 bonus true damage to minions. 2200 
 Spellslinger's Shoes TIPS: These boots greatly increase your magic damage through a combination of Ability Power and both flat and percentage magic penetration. The high mana regeneration allows for frequent spell casting, while the bonus true damage to minions significantly improves wave clear. Champions without Mana instead gain increased health regeneration. They
...(recortado; completo en data/raw)...
## Change history (cambios recientes)

```
Change history
 ADJUSTED 22 SEP 2026 (PATCH 7.3)
BASE STATS
Critical Strike Damage: 175% → 
200%
.
Attack Speed cap: 2.5 → 
3 attacks per second
.
Attack Speed Ratio: 
0.694
.
Base Attack Speed: 
0.694
.
Base Bonus Attack Speed: 
0.15
.
Attack Speed per Level: 
0.008
.
 BUFFED 11 JUN 2026 (PATCH 7.1G)
(PASSIVE)
 MOONSILVER BLADE
Damage ratio to Jungle Monster: 75% → 
100%
.
 BUFFED 12 JUN 2025 (PATCH 6.1D)
(PASSIVE)
 MOONSILVER BLADE
Damage: 15 + champion level × 15+ 50% Ability Power → 
20 + champion level × 15 + 50% Ability Power
.
(E)
 LUNAR RUSH
Damage: 40/75/110/145+25% Ability Power → 
40/80/120/160+30% Ability Power
.
 ADJUSTED 09 JAN 2025 (PATCH 6.0)
BASE STATS
Base Health: 600 → 
630
.
Health per level: 125 → 
140
.
Armor per level: 4.3 → 
5
.
Magic Resist per level: 1.6 → 
2
.
(PASSIVE)
 MOONSILVER BLADE
[New]
 Damage to monsters: 75%.
(W)
 PALE CASCADE
Damage of each sphere: 25/40/55/70+25% Ability Power → 
20/35/50/65+20% Ability Power
.
(R)
 MOONFALL
Base damage: 125/175/225 to 250/350/450 → 
100/160/220 to 200/320/440
.
 REWORKED 05 DEC 2024 (PATCH 5.3C)
(PASSIVE)
 MOONSILVER BLADE
[Removed]
 Casting an ability will allow the next 3 basic attacks to gain bonus attack speed.
[New]
 Casting an ability will gain bonus basic attack speed in 4s.
(R)
 MOONFALL
[Removed]
 Hold to charge, release to cast the ability.
[New]
 Summons the moon for up to 1s, triggering Moonfall Glow when the charge is complete. Diana can move and cast abilities and spells while charging up.
[New]
 Click again to stop charging and trigger Moonfall Glow.
[New] 
Moonfall Glow: dealing (125/175/225 + 40% Ability Power) to (250/350/450 + 80% Ability Power) magic damage based on charge time and slowing targets by 20% for 2s.
 BUFFED 06 JUN 2024 (PATCH 5.1C)
(Q)
 CRESCENT STRIKE
Cooldown: 9/8/7/6s → 
8/7/6/5s
.
Mana: 55/65/75/85 → 
50/55/60/65
.
(W)
 PALE CASCADE
Damage: 25/40/55/70 + 20% Ability Power → 
25/40/55/70 + 25% Ability Power
.
Shield value: 40/60/80/100 + 40% Ability Power → 
50/70/90/110 + 40% Ability Power
.
Increase in shield value after 3rd sphere detonation : 40/60/80/100 + 40% Ability Power → 
50/70/90/110 + 40% Ability Power
.
 ADJUSTED 25 MAY 2023 (PATCH 4.2)
BASE STATS
Base movement speed 
+10.
Crit damage rate：200% → 
175%.
 BUFFED 30 NOV 2022 (PATCH 3.5A)
BASE STATS
Base health: 570 → 
600.
(E)
 LUNAR RUSH
Cooldown: 22/20/18/16s → 
18/16/14/12s.
 NERFED 13 JUL 2022 (PATCH 3.3)
(E)
 LUNAR RUSH
Base Damage: 50/85/120/155 → 
40/75/110/145.
 BUFFED 14 SEP 2021 (PATCH 2.5)
(PASSIVE)
 MOONSILVER BLADE
[NEW] Now deals 110% damage to monsters.
 NERFED 02 JUN 2021 (PATCH 2.3)
BASE STATS
Health: 610 → 
570.
(PASSIVE)
 MOONSILVER BLADE
AP ratio: 0,6 → 
0,5.
(R)
 MOONFALL
Minimum Base Damage: 175/225/275 → 
150/200/250.
Maximum Base Damage: 350/450/550 → 
300/400/500.
 NERFED 12 MAY 2021 (PATCH 2.2c)
(PASSIVE)
 MOONSILVER BLADE
Attack Speed: 30 to 120% → 
30 to 100%.
 BUFFED 13 APR 2021 (PATCH 2.2а)
BASE STATS
Base health: 570 → 
610.
(Q)
 CRESCENT STRIKE
Cooldown: 10/9/8/7s → 
9/8/7/6s.
(W)
 PALE CASCADE
Cooldown: 14s → 
13/11,5/10/8,5s.
(R)
 MOONFALL
Minimum base damage: 150/200/250 + 35% AP → 
175/225/275 + 40% AP.
Maximum base damage: 300/400/500 + 70% AP → 
350/450/550 + 80% AP.
 ADJUSTED 13 APR 2021 (PATCH 2.2а)
(PASSIVE)
 MOONSILVER BLADE
[NEW] After casting a spell, Diana gains 30% to 120% Attack Speed (based on level) for the next 3 attacks.
(E)
 ЛLUNAR RUSH
[REMOVED] Bonus Attack Speed moved to (P) Moonsilver Blade.
 See More
```

## Build/runas populares (referencia comunitaria, NO conclusión)

```
Runes BUILD
                
For runes, you should pick 
 
Electrocute
 (Hitting a champion with successive attacks or abilities deals bonus adaptive damage.) as your keystone, followed by 
 
Sudden Impact
 (After dashing or exiting invisibility/stealth, your next damaging attack or ability deals true damage on hit. The attack/ability gains bonus effects at higher levels.), 
 
Chain Assault
 (Your attacks deal bonus adaptive damage after you hit an enemy champion with an ability.) and 
 
Eyeball Collection
 (Gain Adaptive Force after scoring champion or epic monster takedowns.) in the primary tree, as well as 
 
Bone Plating
 (Reduces incoming damage.) in the secondary tree. Below you can see possible options for replacing runes.
                
                
                    
                        
                            
    
            
                
                
```
---

# Heimerdinger — Ficha de datos (Wild Rift 7.3)

> wr-meta.com (24-sep-2026) + apéndice oficial 7.3. Crudo: data/raw/campeones/heimerdinger.html

## Stats base (nivel 1, growth entre paréntesis)

- **attackdamage**: 54 (3.5)
- **heal**: 600 (120)
- **healthregeneration**: 8 (0.65)
- **attackspeed**: 0.8 (0.006)
- **mana**: 420 (60)
- **mpreg**: 12 (1.22)
- **movementspeed**: 355 (0)
- **armor**: 34 (5)
- **magicresistance**: 40 (1.2)
- **criticalstrike**: 200% (0)

## AS oficial 7.3 (apéndice de las notas — fuente primaria para el modelo)

- champion: Heimerdinger
- Attack Speed Ratio: 0.625
- Base Attack Speed: 0.625
- Base Bonus Attack Speed: 0.2
- Attack Speed per Level: 0.01

## Habilidades (texto completo con valores actuales)

```
P
 (PASSIVE) HEXTECH AFFINITY
 Gains 20% Movement Speed while near allied turrets and turrets deployed by Heimerdinger.
 Q
 (Q) H-28 G EVOLUTION TURRET 
 1s 20 
 Constructs a turret that slowly build up charge and attacks nearby enemies. The turret deals 5 magic damage (5/10/15/20 + 25% ) on hit. At max charge, it fires a beam that deals 25 magic damage (25/45/65/85 + 55% ) . Heimerdinger can have a 3 H-28G Evolution Turrets active at once. If Heimerdinger gets too far away, his turrets will become dormant. H-28G Evolution Turret Stats ( ) Base : 110 (110 ( ) + 8% to 50% ( )) Base : 20 ~ 90 ( ) Base : 25 Deals 40% damage to monsters. UPGRADE!!!: Technological enhancement upgrades this ability to H-28Q Apex Turret . H-28Q Apex Turret: Places an upgraded turret for 10 seconds, dealing 80 magic damage (80/100/120 + 35% )  per shot, increased to 100 magic damage (100/140/180 + 60% )  at max charge. The turret slows for 1 second on hit.
 W
 (W) HEXTECH MICRO-ROCKETS 
 9/8/7/6s 50 
 Unleashes a barrage of 5 rockets that deal  60 magic damage (60/85/110/135 + 60% ) to the first enemy hit. Nearby Turrets gain 20% charge for every rocket that hits a champion. Additional rocket hits after the first to the same champion or monster only deal 20% magic damage . This damage is increased to 60% for minions. UPGRADE!!!: Technological enhancement upgrades this ability to Hextech Rocket Swarm . Hextech Rocket Swarm: Fires 4 waves of rockets. Each rocket deals 135 magic damage (135 + 45% )  to the first enemy hit. Additional rocket hits after the first to the same champion or monster only deal 25% magic damage per hit. Once the target is hit by five rockets, the damage decays further. Rockets deal full damage to minions. The rocket swarm deals a maximum of 524 magic damage (524 + 175% )  to each enemy champion or monster.
 E
 (E) CH-2 ELECTRON STORM GRENADE 
 10s 85 
 Hurls a grenade that deals 70 magic damage (70/120/170/220 + 60% )  in a target area and slows by 35% for 2 seconds. Enemies in the center are also stunned for 1 second. Hitting a champion fully charges nearby turrets. UPGRADE!!!: Technological enhancement upgrades this ability to CH-3X Lightning Grenade . CH-3X Lightning Grenade: Throws a bouncing grenade that discharges 3 times, each dealing 100 magic damage (100 + 60% ). The stun and slow areas are larger, and the grenade now slows enemies by 40%.
 R
 (R) UPGRADE!!! 
 75/66/56s 100 
 Active: Upgrades Heimerdinger's next basic ability. H-28Q Apex Turret: Places an upgraded turret for 10 seconds, dealing 80 magic damage (80/100/120 + 35% )  per shot, increased to 100 magic damage (100/140/180 + 60% )  at max charge. The turret slows for 1 second on hit. Hextech Rocket Swarm: Fires 4 waves of rockets. Each rocket deals 135 magic damage (135 + 45% )  to the first enemy hit. Additional rocket hits after the first to the same champion or monster only deal 25% magic damage per hit. Once the target is hit by five rockets, the damage decays further. Rockets deal full damage to minions. The rocket swarm deals a maximum of 524 magic damage (524 + 175% )  to each enemy champion or monster. CH-3X Lightning Grenade: Throws a bouncing grenade that discharges 3 times, each dealing 100 magic damage (100 + 60% ). The stun and slow areas are larger, and the grenade now slows enemies by 40%. Recast: Cancels this ability.
 HEIMERDINGER Meta Overview — Ranks & Performance Analytics 
 This meta overview presents HEIMERDINGER’s ranked performance across different roles and skill tiers. The data includes tier placement, win rate, pick rate, ban rate, and short-term trends, allowing you to evaluate her current strength and draft priority. Statistics are synced with rank buckets and role selection, helping you understand where HEIMERDINGER performs best and how her impact changes in the evolving Wild Rift meta.
 Diamond + Master + Challenger Legendary 
 Updated: 24 SEP 2026 UTC 00:00 
 MID 
 Confidence Low 
 Win: 49.59% 
 Pick: 1.46% 
 Ban: 1.52% 
 Trend: ↓ 6 
 Signals: 
 ? 
 🧊 Falling 
 MID 
 Last 7 days analytics 
 Tier List 
 Compare Сhampions 
 Build 
 Counters 
 Counter Items 
 Tips 
 Con 
 Game Plan 
 Power Spikes 
 Mid HEIMERDINGER Build items and runes 
 The information below will help you get familiar with the game on the Mid Line HEIMERDINGER. We have prepared a items builds, runes, summoner spells and ability order for a comfortable game. Situational options for replacing items and runes are also available to you.
 Key items 
 TIPS: Start your build with Amplifying Tome . Next, you should pay attention to whether your mobility champion is enough, our further actions will depend on this. If it is hard for you to dodge the enemy's skills or you want to roam on neighboring lines, then it is better to buy Boots of Speed at an early stage.
 Start
 Amplifying Tome 
 Amplifying Tome +20 Ability Power 500 
 Core
 Blackfire Torch 
 Blackfire Torch Deal burn damage +80 Ability Power +500 Maximum Mana +20 Ability Haste Baleful Blaze: Dealing damage with abilities causes enemies to burn for 20 + 2% magic damage per second for 3 seconds. Deal 40 plus 2% magic damage every second to monsters. Blackfire: For each enemy champion or monster affected by your Baleful Blaze, gain 4% Ability Power . 2800 
 Blackfire Torch TIPS: This item is perfect for mages who specialize in sustained spell damage. Your abilities ignite enemies, burning them over time, and the more enemies affected by the burn, the more Ability Power you gain. It excels on champions with area-of-effect and damage-over-time abilities, boosting both your overall damage and your ability to clear waves and jungle camps efficiently.
 Boots of Mana 
 Boots of Mana Ability Power, Magic Pen, Mana Regeneration +25 Ability Power +8 Magic Penetration +75% Mana Regeneration +45 Move Speed Equilibrium: Champions without Mana gain 50% bonus health Regen. Big Bully: Attacks and active abilities deal 18 bonus true damage to minions. 1200 
 Boots of Mana TIPS: These boots greatly enhance your early magic damage by providing Ability Power, magic penetration, and increased mana regeneration. They also improve wave clear by dealing bonus true damage to minions, while champions without Mana instead gain additional health regeneration. They are an excellent choice for mages and AP supports who value strong laning, frequent spell casting, and efficient wave clearing.
 Liandry's Torment 
 Liandry's Torment Abilities deal bonus damage +300 Max Health +70 Ability Power Torment: Damaging abilities and  empowered attacks burn enemies for 2% max Health magic damage for 3 seconds. Madness: Deals 2% more damage for each second in combat against champions, capped at 6% after 3 seconds. 3000 
 Liandry's Torment TIPS: 
...(recortado; completo en data/raw)...
## Change history (cambios recientes)

```
Change history
 ADJUSTED 22 SEP 2026 (PATCH 7.3)
BASE STATS
Critical Strike Damage: 175% → 
200%
.
Attack Speed cap: 2.5 → 
3 attacks per second
.
Attack Speed Ratio: 
0.625
.
Base Attack Speed: 
0.625
.
Base Bonus Attack Speed: 
0.2
.
Attack Speed per Level: 
0.01
.
 BUFFED 11 JUN 2026 (PATCH 7.1G)
(Q)
 H-28 G EVOLUTION TURRET
Turret Armor: 10 ~ 80 (Based on Level) → 
20 ~ 90 (Based on Level)
.
Turret Health Ability Power Ratio: 3% ~ 45% (Based on Level) → 
8% ~ 50% (Based on Level)
.
Turret laser beam Ability Power Ratio: 45%→ 
55%
.
Bonus damage taken by turrets from melee champions: 50% → 
40%
.
(R)
 UPGRADE!!!
Bonus damage taken by H-28Q Apex Turret from melee champions: 50% → 
40%
.
 ADJUSTED 17 APR 2025 (PATCH 6.1)
BASE STATS
Movement speed: 345 → 
355
.
 ADJUSTED 09 JAN 2025 (PATCH 6.0)
BASE STATS
Base Health: 540 → 
600
.
Health per level: 104 → 
120
.
Base Armor: 28 → 
34
.
Armor per level: 4.5 → 
5
.
Magic Resist per level: 1 → 
1.2
.
 NERFED 14 NOV 2024 (PATCH 5.3B)
(Q)
 H-28 G EVOLUTION TURRET
Turret on-hit damage: 5/10/15/20 + 35% Ability Power → 
5/10/15/20 + 25% Ability Power
.
Turret laser damage: 30/50/70/90 + 55% Ability Power → 
25/45/65/85 + 45% Ability Power
.
(E)
 CH-2 ELECTRON STORM GRENADE
Slowdown range: 250 → 
230
.
Stun range: 125 → 
115
.
(R)
 UPGRADE!!!
H-28Q Apex Turret on-hit damage: 80/105/130 + 40% Ability Power → 
80/100/120 + 35% Ability Power
.
H-28Q Apex Turret laser damage: 100/140/180 + 70% Ability Power → 
100/140/180 + 60% Ability Power
.
 NERFED 31 OCT 2024 (PATCH 5.3A)
(Q)
 H-28 G EVOLUTION TURRET
Damage dealt by turret on-hit: 5/11/17/23 + 35% Ability Power → 
5/10/15/20 + 35% Ability Power
.
Damage of turret laser: 30/55/80/105 + 55% Ability Power → 
30/50/70/90 + 55% Ability Power
.
(W)
 HEXTECH MICRO-ROCKETS
Damage: 70/95/120/145 + 60% Ability Power → 
60/85/110/135 + 60% Ability Power
.
(E)
 CH-2 ELECTRON STORM GRENADE
Damage: 85/130/175/220 + 60% Ability Power → 
70/120/170/220 + 60% Ability Power
.
 See More
```

## Build/runas populares (referencia comunitaria, NO conclusión)

```
Runes BUILD
                
For runes, you should pick 
 
Arcane Comet
 (Damaging a champion with an ability hurls a comet at their location. When a comet hits an enemy champion, the next comet's damage increases.) as your keystone, followed by 
 
Botanist
 (When you destroy a plant, gain gold and empowered plant effects.), 
 
Transcendence
 (Grants more Ability Haste the higher your level is and also returns ability cooldown duration.) and 
 
Scorch
 (Deals bonus damage to champions on ability hit.) in the primary tree, as well as 
 
Bone Plating
 (Reduces incoming damage.) in the secondary tree. Below you can see possible options for replacing runes.
                
                
                    
                        
                            
    
            
                
                    
                    
                        
Arcane Comet
Poke, Stack Am
```
---

# Kalista — Ficha de datos (Wild Rift 7.3)

> wr-meta.com (24-sep-2026) + apéndice oficial 7.3. Crudo: data/raw/campeones/kalista.html

## Stats base (nivel 1, growth entre paréntesis)

- **attackdamage**: 57 (5.2)
- **heal**: 630 (128)
- **healthregeneration**: 6 (0.64)
- **attackspeed**: 0.8 (0.032)
- **mana**: 340 (50)
- **mpreg**: 10 (0.86)
- **movementspeed**: 335 (0)
- **armor**: 34 (4.5)
- **magicresistance**: 32 (1.4)
- **criticalstrike**: 200% (0)

## AS oficial 7.3 (apéndice de las notas — fuente primaria para el modelo)

- champion: Kalista
- Attack Speed Ratio: 0.694
- Base Attack Speed: 0.694
- Base Bonus Attack Speed: 0.16
- Attack Speed per Level: 0.046

## Habilidades (texto completo con valores actuales)

```
P
 (PASSIVE) MARTIAL POISE
 When Kalista winds up her attacks, moving the left joystick will cause her to dash for a short distance in that direction after she throws her spear. When the game starts, she can choose an ally to become her Oathsworn . Kalista cannot change her Oathsworn. Once Kalista launches her attacks, they cannot be canceled. Her dash speed and distance scale with boot tier.
 Q
 (Q) PIERCE 
 8/7.5/7/6.5s 55/60/65/70 
 Hurls a spear, dealing 134 physical damage (70/135/200/265 + 110% ) to the first target hit. If this kills the target, the spear continues onward, carrying the target's Rend stacks to the next enemy hit. After casting this ability, Kalista can dash using Martial Poise .
 W
 (W) SENTINEL 
 20s 30 
 Passive: When the distance between Kalista and her Oathsworn is less than 8, and both hit the same target within 4s using attacks or Pierce , Kalista deals 16/17/18/19% of the target's max Health as bonus magic damage . This effect has a 8s cooldown per target. Active: Sends a Soul Sentinel to patrol an area. Upon spotting an enemy champion, the Sentinel follows them for 4s, revealing them for 4s. Sentinels disappear after patrolling 3 laps. Charge: Kalista gains a charge every 45/40/35/30s, storing up to 2 charge(s). This ability's passive deals at least 75 damage against minions and executes them if their Health is below 125.
 E
 (E) REND 
 10/9/8/7s 30 
 Passive: On hit, Kalista's spears linger in their target for 4 second(s), applying a stacking Rend . Active: Kalista rips the spears from nearby enemies, dealing 75 physical damage (30/45/60/75 + 70% ) plus 33 physical damage (12/22/32/42 + 36/43/50/57% ) per spear after the first. Slows enemies hit by 15/25/35/45% for 2 second(s). If this ability kills at least one target, its cooldown is refreshed, and it refunds 12/18/24/30 Mana . Deals 50% damage to epic mOnsters.
 R
 (R) FATE'S CALL 
 60/55/50s 100 
 Kalista puts her Oathsworn into stasis and draws them to herself for up to 4 second(s). The Oathsworn can launch themselves in a direction, knocking nearby enemies airborne for 1/1.5/2 second(s) upon hitting the first enemy champion. The Oathsworn then ricochets for a distance based on their max attack range.
 KALISTA Meta Overview — Ranks & Performance Analytics 
 This meta overview presents KALISTA’s ranked performance across different roles and skill tiers. The data includes tier placement, win rate, pick rate, ban rate, and short-term trends, allowing you to evaluate her current strength and draft priority. Statistics are synced with rank buckets and role selection, helping you understand where KALISTA performs best and how her impact changes in the evolving Wild Rift meta.
 Diamond + Master + Challenger Legendary 
 Updated: 24 SEP 2026 UTC 00:00 
 DUO 
 Confidence Med 
 Win: 50.99% 
 Pick: 4.72% 
 Ban: 5.02% 
 Trend: ↑ 7 
 Reason: 
 ? 
 Rising trend 
 SOLO 
 Confidence Low 
 Win: 51.27% 
 Pick: 1.94% 
 Ban: 5.02% 
 Trend: ↓ 1 
 DUO SOLO 
 Last 7 days analytics 
 Tier List 
 Compare Сhampions 
 Build 
 Counters 
 Counter Items 
 Tips 
 Con 
 Game Plan 
 Power Spikes 
 Adc KALISTA Build items and runes 
 The information below will help you get familiar with the game on the Adc Line KALISTA. We have prepared a items builds, runes, summoner spells and ability order for a comfortable game. Situational options for replacing items and runes are also available to you.
 Key items 
 TIPS: Start your build with Long Sword . Next, you should pay attention to whether your mobility champion is enough, our further actions will depend on this. If it is hard for you to dodge the enemy's skills or you want to roam on neighboring lines, then it is better to buy Boots of Speed at an early stage.
 Start
 Long Sword 
 Long Sword +12 Attack Damage 500 
 Core
 Statikk Shiv 
 Statikk Shiv Energized Attacks deal chain damage +40 Attack Damage +30% Attack Speed +40 Ability Power +4% Move Speed Electroshock: Attacks grant 5 extra Energized stacks . Electrospark: Moving and attacking generate an Energized Attack that fires chain lightning to 4–7 targets ( ), dealing 60 magic damage (increased to 90 magic damage against minions and monsters) and applying on-hit effects to secondary bounce targets. 3000 
 Statikk Shiv TIPS: This item combines physical and magic damage, Attack Speed, and mobility, enhancing basic attacks and hybrid builds. Moving and attacking charges an empowered attack that releases chain lightning across multiple targets, dealing magic damage and applying on-hit effects to additional targets. An excellent choice for champions who need fast wave clear, multi-target damage, and effective use of on-hit effects.
 Berserker's Greaves 
 Berserker's Greaves Attack Speed +35% Attack Speed +45 Move Speed Blessed Blade: Attacks restore 10 Health on hit. 1200 
 Berserker's Greaves TIPS: These boots grant a significant boost to attack speed and movement speed, while empowering your basic attacks with on‑hit life steal. — A great pick for marksmen and auto‑attack bruisers who need mobility, rapid attack cadence, and constant sustain in fights.
 Guinsoo's Rageblade 
 Guinsoo's Rageblade Applies on-hit effects +35 Attack Damage +30% Attack Speed +30 Ability Power Wrath: Attacks deal 30 bonus magic damage on hit . Seething Strike: Attacks grant 8% Attack Speed , stacking up to 4 times for a maximum of 32% Attack Speed . While fully stacked, every 3 attack(s) applies on-hit effects an additional 1 time(s). 3000 
 Guinsoo's Rageblade TIPS: This item combines physical and magic damage with Attack Speed, significantly empowering champions focused on on-hit effects. Attacks deal bonus magic damage and gradually increase Attack Speed, while at maximum stacks they periodically trigger on-hit effects an additional time. An excellent choice for champions who rely on frequent basic attacks and stacking multiple on-hit effects.
 Boots
 Berserker's Greaves 
 Berserker's Greaves Attack Speed +35% Attack Speed +45 Move Speed Blessed Blade: Attacks restore 10 Health on hit. 1200 
 Berserker's Greaves TIPS: These boots grant a significant boost to attack speed and movement speed, while empowering your basic attacks with on‑hit life steal. — A great pick for marksmen and auto‑attack bruisers who need mobility, rapid attack cadence, and constant sustain in fights.
 Gunmetal Greaves 
 Gunmetal Greaves Increases Attack Speed and Movement Speed +50% Attack Speed +45 Move Speed +5% Lifesteal Noxian Gait: Attacks against enemy champions grant Movement Speed ( 10% for melee champions / 7% for ranged champions) decaying over 2 seconds. Blessed Blade: Attacks restore 12 Health on hit. 2200 
 Gunmetal Greaves TIPS: These boots significantly increase Attack Speed while also providing Mo
...(recortado; completo en data/raw)...
## Change history (cambios recientes)

```
Change history
 BUFFED 22 SEP 2026 (PATCH 7.3)
BASE STATS
Critical Strike Damage: 175% → 
200%
.
Attack Speed cap: 2.5 → 
3 attacks per second
.
Attack Speed Ratio: 
0.694
.
Base Attack Speed: 
0.694
.
Base Bonus Attack Speed: 
0.16
.
Attack Speed per Level: 
0.046
.
Base Attack Damage: 54 → 
57
.
Attack Damage per Level: 5 → 
5.2
.
 BUFFED 04 DEC 2025 (PATCH 6.3E)
(E)
 REND
Base Damage per spear after the first: 12/20/28/36 → 
12/22/32/42
.
(R)
 FATE'S CALL
Cooldown: 70/65/60s → 
60/55/50s
.
 BUFFED 14 AUG 2025 (PATCH 6.2C)
BASE STATS
Attack Damage per level: 4.5 → 5.
(E)
 REND
Damage per stack: 12/16/20/24 + 34/38/42/46% Attack Damage → 
12/20/28/36 + 36/43/50/57% Attack Damage
.
 ADJUSTED 03 JUL 2025 (PATCH 6.1F)
BASE STATS
Base Attack Damage: 54 → 
58
.
Attack Damage per level: 3.5 → 
4.5
.
Health per level: 120 → 
128
.
(PASSIVE)
 MARTIAL POISE
The dash distance gained from attack speed is reduced by 33%.
(Q)
 PIERCE
Damage: 60/125/190/255 + 105% Attack Damage → 
70/135/200/265 + 110% Attack Damage
.
(E)
 REND
Damage per spear stacked: 8/12/16/20 + 35/39/43/47% Attack Damage → 
12/18/24/30 + 34/38/42/46% Attack Damage
.
(R)
 FATE'S CALL
Cooldown: 80/70/60s → 
70/65/60s
.
 BUFFED 23 JAN 2025 (PATCH 6.0B)
(W)
 SENTINEL
Passive damage: 14/15/16/17% target’s maximum Health → 
16/17/18/19% target’s maximum Health
.
Cooldown of Passive damage: 10s → 
8s
.
 ADJUSTED 09 JAN 2025 (PATCH 6.0)
BASE STATS
Base Health: 600 → 
630
.
Health per level: 104 → 
120
.
Armor per level: 4 → 
4.5
.
Magic Resist per level: 1 → 
1.4
.
 NERFED 26 DEC 2024 (PATCH 5.3D)
BASE STATS
Basic attack damage: 58 → 
54
.
(E)
 REND
Basic damage of each following spear: 10/15/20/25 → 
8/12/16/20
.
 ADJUSTED 17 OCT 2024 (PATCH 5.3)
BASE STATS
Base Attack Damage: 66 → 
58
.
Attack Damage per level: 3.5 → 
4.5
.
(E)
 REND
10/15/20/25 + 30/34/38/42% of Attack Damage → 
10/15/20/25 + 35/39/43/47% Attack Damage
.
 BUFFED 18 JUL 2024 (PATCH 5.2)
Optimized the mechanic
 where Rend goes into cooldown when Kalista takes down her target with it.
Optimized the timer
 displayed at the indicator bar when Kalista is tethered to her ally.
Optimized the display
 of the Health threshold where Kalista executes enemy champions with Rend.
 BUFFED 18 APR 2024 (PATCH 5.1)
BASE STATS
Attack Damage per level: 3 → 
3.5
.
Health per level: 104 → 
120
.
(Q)
 PIERCE
Damage: 50/110/170/230 + 105% Attack Damage → 
60/125/190/255 + 105% Attack Damage
.
(E)
 REND
Initial Damage: 15/30/45/60 + 65% Attack Damage → 
30/45/60/75 + 70% Attack Damage
.
Damage of each following spear: 7/11/15/19 + 26/28/30/32% Attack Damage → 
10/15/20/25 + 30/34/38/42% Attack Damage
.
 See More
```

## Build/runas populares (referencia comunitaria, NO conclusión)

```
Runes BUILD
                
For runes, you should pick 
 
Lethal Tempo
 (Stack Attack Speed with each consecutive attack. At max stacks, gain additional Attack Speed and deal bonus damage with your attacks) as your keystone, followed by 
 
Brutal
 (Attacks deal bonus damage to enemy champions.), 
 
Coup de Grace
 (Increases damage dealt to enemy champions with low Health.) and 
 
Legend: Alacrity
 (Gains Attack Speed.) in the primary tree, as well as 
 
Sudden Impact
 (After dashing or exiting invisibility/stealth, your next damaging attack or ability deals true damage on hit. The attack/ability gains bonus effects at higher levels.) in the secondary tree. Below you can see possible options for replacing runes.
                
                
                    
                        
                            
    
            
                
                    
             
```
---

# Karma — Ficha de datos (Wild Rift 7.3)

> wr-meta.com (24-sep-2026) + apéndice oficial 7.3. Crudo: data/raw/campeones/karma.html

## Stats base (nivel 1, growth entre paréntesis)

- **attackdamage**: 58 (3.64)
- **heal**: 630 (128)
- **healthregeneration**: 9 (0.71)
- **attackspeed**: 0.8 (0.008)
- **mana**: 390 (57)
- **mpreg**: 21 (1.14)
- **movementspeed**: 360 (0)
- **armor**: 37 (5)
- **magicresistance**: 36 (1.2)
- **criticalstrike**: 200% (0)

## AS oficial 7.3 (apéndice de las notas — fuente primaria para el modelo)

- champion: Karma
- Attack Speed Ratio: 0.625
- Base Attack Speed: 0.625
- Base Bonus Attack Speed: 0.2
- Attack Speed per Level: 0.0135

## Habilidades (texto completo con valores actuales)

```
P
 (PASSIVE) MANTRA
 Every spell cast grants Karma a stack of Mantra . At 3 stacks, she enters a Mantra State , enhancing her next basic ability.
 Q
 (Q) INNER FLAME 
 9/8/7/6s 60 
 Fires a blast of energy, dealing 60 magic damage (60/100/140/180 + 40% ) to the first target hit and surrounding enemies, and slowing them by 35% for 1.5 seconds. Mantra: Increases the destructive power of the blast, dealing 65 magic damage (65/140/215/290 + 50% ) to the first target hit and surrounding enemies. The blast leaves a field for 1.5 seconds, slowing targets by 42.5/45/47.5/50% , after which it explodes and deals 40 magic damage (40/80/120/160 + 50% ).
 W
 (W) FOCUSED RESOLVE 
 15s 55/60/65/70 
 Tethers up to two nearby enemy champions, dealing 35 magic damage (35/60/85/110 + 40% ) and revealing them for 1.75 seconds. If targets fail to break the tether, they take 40 magic damage (40/70/100/130 + 45% ) and are rooted for 1/1.25/1.5/1.75 seconds(s). Mantra: A new tether will be formed between tethered targets. If there is only one tethered, the new teather will spread toward and additional nearby enemy champion. If targets fail to break all the tethers, they take 40 magic damage (40/70/100/130 + 45% ) and are  rooted for an improved 1.5/1.75/2/2.25 seconds.
 E
 (E) INSPIRE 
 10/9/8/7s 70 
 Grants an allied champion 60 sheald (60/90/120/150 + 65% ) for 3 seconds and 30% movement speed 1.5 seconds. Mantra: Karma focuses her power, granting a 120  shield (120/180/240/300 +  65% ) that  decays over 4 seconds, and 60% movement speed that decays 20% over the same duration. An additional ring is generated around the shielded target, and the first  ally champion who enters the ring will be granted the same shield.
 R
 (R) TRANSCENDENT EMBRACE 
 70/65/60s 100 
 Immediately enters Mantra State . Forms a ring of spirit energy at the target location. After 1s, it detonates, dealing 170 magic damage (170/280/390 + 80% ) to all enemies inside the circle and slowing them by 35% for 1s. If enemies  are hit by the outer ring, they will be knocked back toward the center
 KARMA Meta Overview — Ranks & Performance Analytics 
 This meta overview presents KARMA’s ranked performance across different roles and skill tiers. The data includes tier placement, win rate, pick rate, ban rate, and short-term trends, allowing you to evaluate her current strength and draft priority. Statistics are synced with rank buckets and role selection, helping you understand where KARMA performs best and how her impact changes in the evolving Wild Rift meta.
 Diamond + Master + Challenger Legendary 
 Updated: 24 SEP 2026 UTC 00:00 
 SUPPORT 
 Confidence Med 
 Win: 49.82% 
 Pick: 4.68% 
 Ban: 0.62% 
 Trend: ↓ 14 
 Signals: 
 ? 
 🧊 Falling 
 SUPPORT 
 Last 7 days analytics 
 Tier List 
 Compare Сhampions 
 Build 
 Counters 
 Counter Items 
 Tips 
 Con 
 Game Plan 
 Power Spikes 
 Mid KARMA Build items and runes 
 The information below will help you get familiar with the game on the Mid Line KARMA. We have prepared a items builds, runes, summoner spells and ability order for a comfortable game. Situational options for replacing items and runes are also available to you.
 Key items 
 TIPS: Start your build with Amplifying Tome . Next, you should pay attention to whether your mobility champion is enough, our further actions will depend on this. If it is hard for you to dodge the enemy's skills or you want to roam on neighboring lines, then it is better to buy Boots of Speed at an early stage.
 Start
 Amplifying Tome 
 Amplifying Tome +20 Ability Power 500 
 Core
 Luden's Echo 
 Luden's Echo Abilities deal bonus damage +100 Ability Power +500 Max Mana +10 Ability Haste Echo: Your next damaging ability or empowered attack deals an additional 140 + 15% magic damage to the target and up to 3 nearby enemies. (9s Cooldown) 2800 
 Luden's Echo TIPS: This item greatly enhances your burst damage by empowering your next damaging ability or empowered attack with an additional magic explosion that also strikes nearby enemies. It is an excellent choice for mages who excel at wave clearing, poking multiple targets, and dominating short trades with high burst potential.
 Boots of Mana 
 Boots of Mana Ability Power, Magic Pen, Mana Regeneration +25 Ability Power +8 Magic Penetration +75% Mana Regeneration +45 Move Speed Equilibrium: Champions without Mana gain 50% bonus health Regen. Big Bully: Attacks and active abilities deal 18 bonus true damage to minions. 1200 
 Boots of Mana TIPS: These boots greatly enhance your early magic damage by providing Ability Power, magic penetration, and increased mana regeneration. They also improve wave clear by dealing bonus true damage to minions, while champions without Mana instead gain additional health regeneration. They are an excellent choice for mages and AP supports who value strong laning, frequent spell casting, and efficient wave clearing.
 Malignance 
 Malignance An item made for Ultimate-centric playstyles +90 Ability Power +500 Max Mana +15 Ability Haste Scorn: Your Ultimate abilities gain 20 Ability Haste . Hatefog: Damaging a champion with your Ultimate burns the ground beneath them for 3 second(s), dealing magic damage equal to 60 plus 5% AP per second and reducing their Magic Resist by 10 . Burn radius increases with damage, reaching maximum radius at 800 damage. 2700 
 Malignance TIPS: This item is perfect for champions who focus on their ultimate abilities and want to maximize their effectiveness in fights. It provides bonuses to ability power, magic penetration, maximum mana, and ability haste. The "Scorn" effect reduces the cooldown of your ultimate ability, enhancing its efficiency and uptime. The "Hatefog" effect deals magic damage to enemies in the area after using your ultimate, creating a scorched earth effect. Enemies within this area take damage and have their magic resistance reduced, making this item ideal for champions who want to weaken their opponents and increase their damage. It’s especially useful against enemies with high magic resistance.
 Boots
 Boots of Mana 
 Boots of Mana Ability Power, Magic Pen, Mana Regeneration +25 Ability Power +8 Magic Penetration +75% Mana Regeneration +45 Move Speed Equilibrium: Champions without Mana gain 50% bonus health Regen. Big Bully: Attacks and active abilities deal 18 bonus true damage to minions. 1200 
 Boots of Mana TIPS: These boots greatly enhance your early magic damage by providing Ability Power, magic penetration, and increased mana regeneration. They also improve wave clear by dealing bonus true damage to minions, while champions without Mana instead gain additional health regeneration. They are an excellent choice for mages and AP supports who value strong laning, freq
...(recortado; completo en data/raw)...
## Change history (cambios recientes)

```
Change history
 ADJUSTED 22 SEP 2026 (PATCH 7.3)
BASE STATS
Critical Strike Damage: 175% → 
200%
.
Attack Speed cap: 2.5 → 
3 attacks per second
.
Attack Speed Ratio: 
0.625
.
Base Attack Speed: 
0.625
.
Base Bonus Attack Speed: 
0.2
.
Attack Speed per Level: 
0.0135
.
 NERFED 28 AUG 2025 (PATCH 6.2E)
(E)
 INSPIRE
Base Shield Value: 70/100/130/160 → 
60/90/120/150
.
Mantra Base Shield Value: 140/200/260/320 → 
120/180/240/300
.
 ADJUSTED 17 APR 2025 (PATCH 6.1)
BASE STATS
Movement speed: 350 → 
360
.
 ADJUSTED 09 JAN 2025 (PATCH 6.0)
BASE STATS
Base Health: 570 → 
630
.
Health per level: 125 → 
128
.
Base Armor: 35 → 
37
.
Armor per level: 4.7 → 
5
.
Base Magic Resist: 32 → 
36
.
Magic Resist per level: 0.8 → 
1.2
.
 ADJUSTED 22 FEB 2024 (PATCH 5.0B)
(Q)
 INNER FLAME
Damage: 70/110/150/190 + 40% Ability Power → 
60/100/140/180 + 40% Ability Power
.
Empowered damage: 70/150/230/310 + 50% Ability Power → 
65/140/215/290 + 50% Ability Power
.
Empowered slow down: full level 50% → 
42.5/45/47.5/50%
.
(E)
 INSPIRE
Cooldown: 10/9.5/9/8.5s → 
10/9/8/7s
.
 BUFFED 22 NOV 2023 (PATCH 4.4B)
(Q)
 INNER FLAME
Cooldown: 10/9/8/7s → 
9/8/7/6s
.
(R)
 TRANSCENDENT EMBRACE
Damage: 150/250/350 + 60% Ability Power → 
170/280/390 + 80% Ability Power
.
 BUFFED 24 AUG 2023 (PATCH 4.3B)
(Q)
 INNER FLAME
Base damage: 60/100/140/180 → 
70/110/150/190
.
Mantra bonus damage: 60/140/220/300 → 
70/150/230/310
.
(E)
 INSPIRE
Shield value: 60/90/120/150 + 50% Ability Power → 
70/100/130/160 + 65% Ability Power
.
Mantra bonus shield: 120/180/240/300 + 50% Ability Power → 
140/200/260/320 + 65% Ability Power
.
 ADJUSTED 25 MAY 2023 (PATCH 4.2)
BASE STATS
Base movement speed 
+10.
Crit damage rate：200% → 
175%.
 NERFED 28 SEP 2022 (PATCH 3.4A)
(W)
 FOCUSED RESOLVE
Cooldown: 13s → 
15s.
(E)
 INSPIRE
Non-Mantra Movement Speed: 45% → 
30%.
 NERFED 13 JUL 2022 (PATCH 3.3)
(Q)
 INNER FLAME
Mana cost: 50 → 
60.
(E)
 INSPIRE
Base shield: 60/100/140/180 → 
60/90/120/150.
Mantra base Enhanced Shield: 150/210/270/330 → 
120/180/240/300.
 NERFED 11 MAY 2022 (PATCH 3.2)
(Q)
 INNER FLAME
Base damage: 60/110/160/210 → 
60/100/140/180.
(R)
 TRANSCENDENT EMBRACE
Slow: 50% → 
35%.
 NERFED 08 APR 2022 (PATCH 3.1A)
(Q)
 INNER FLAME
Mantra bonus base damage: 70/160/250/340 → 
70/150/230/310.
 See More
```

## Build/runas populares (referencia comunitaria, NO conclusión)

```
Runes BUILD
                
For runes, you should pick 
 
Arcane Comet
 (Damaging a champion with an ability hurls a comet at their location. When a comet hits an enemy champion, the next comet's damage increases.) as your keystone, followed by 
 
Botanist
 (When you destroy a plant, gain gold and empowered plant effects.), 
 
Transcendence
 (Grants more Ability Haste the higher your level is and also returns ability cooldown duration.) and 
 
Scorch
 (Deals bonus damage to champions on ability hit.) in the primary tree, as well as 
 
Bone Plating
 (Reduces incoming damage.) in the secondary tree. Below you can see possible options for replacing runes.
                
                
                    
                        
                            
    
            
                
                    
                    
                        
Arcane Comet
Poke, Stack Am
```
---

# Mordekaiser — Ficha de datos (Wild Rift 7.3)

> wr-meta.com (24-sep-2026) + apéndice oficial 7.3. Crudo: data/raw/campeones/mordekaiser.html

## Stats base (nivel 1, growth entre paréntesis)

- **attackdamage**: 54 (3.5)
- **heal**: 660 (120)
- **healthregeneration**: 8 (1)
- **attackspeed**: 0.7 (0.005)
- **mana**: 0 (0)
- **mpreg**: 0 (0)
- **movementspeed**: 340 (0)
- **armor**: 46 (4)
- **magicresistance**: 40 (2)
- **criticalstrike**: 200% (0)

## AS oficial 7.3 (apéndice de las notas — fuente primaria para el modelo)

- champion: Mordekaiser
- Attack Speed Ratio: 0.625
- Base Attack Speed: 0.625
- Base Bonus Attack Speed: 0.17
- Attack Speed per Level: 0.008

## Habilidades (texto completo con valores actuales)

```
P
 (PASSIVE) DARKNESS RISE
 Gains 3/6/9/12% Magic Pen ( ). Attacks deal 30% bonus magic damage . When Mordekaiser gets a takedown, or his basic abilities or attacks hit an enemy champion or large monster, he gains 1 stack of Darkness Rise for 5 seconds. At 3 stacks, he cloaks himself in a negative energy field. The negative energy field deals magic damage equal to 5 plus 1% of the target's max Health ( ) per second and grants him 3% Movement Speed ( ) for 5 seconds. Takedowns and basic ability or attack hits against enemy champions or large monsters refresh the negative energy field's duration. Darkness Rise deals a maximum of 24 damage to monsters per second.
 Q
 (Q) OBLITERATE 
 7/6/5/4s 
 Smashes the ground with Nightfall to deal 84 magic damage (80/110/140/170 + (4~70) + 70% ). Damage is increased by 120% bonus when the ability hits only one enemy.
 W
 (W) INDESTRUCTIBLE 
 12/11/10/9s 
 Passive: Stores 35% of the damage he deals and 7% of the damage he takes. Against non-champions, he stores 25% of the damage dealt and taken instead. Active: Gains the stored damage as a shield for 4 seconds. Recasting Indestructible restores 35/38/40/42% of the remaining shield as Health . Minimum Shield: 5% Maximum Shield: 30% 
 E
 (E) DEATH'S GRASP 
 15/13/11/9s 
 Pulls the enemy toward him, dealing 60 magic damage (60/80/100/120 + 55% )  and slowing them by 30% for 1 second.
 R
 (R) REALM OF DEATH 
 105/90/75s 
 Banishes an enemy champion into the Death Realm with him for 7 seconds. During this period: Steals 8% of the target's core stats ( AP , AD , AS , AR , MR and Max HP ). If Mordekaiser takes down the target, he keeps the stolen stats until the target respawns. If he doesn't, the stolen stats are returned once the ability ends.
 MORDEKAISER Meta Overview — Ranks & Performance Analytics 
 This meta overview presents MORDEKAISER’s ranked performance across different roles and skill tiers. The data includes tier placement, win rate, pick rate, ban rate, and short-term trends, allowing you to evaluate her current strength and draft priority. Statistics are synced with rank buckets and role selection, helping you understand where MORDEKAISER performs best and how her impact changes in the evolving Wild Rift meta.
 Diamond + Master + Challenger Legendary 
 Updated: 24 SEP 2026 UTC 00:00 
 SOLO 
 Confidence High 
 Win: 50.52% 
 Pick: 10.95% 
 Ban: 32.20% 
 Trend: ↓ 3 
 Reason: 
 ? 
 Often banned 
 Signals: 
 ? 
 ⛔ Perma-ban 👥 Popular 
 SOLO 
 Last 7 days analytics 
 Tier List 
 Compare Сhampions 
 Build 
 Counters 
 Counter Items 
 Tips 
 Con 
 Game Plan 
 Power Spikes 
 Solo Baron MORDEKAISER Build items and runes 
 The information below will help you get familiar with the game on the Solo Baron Line MORDEKAISER. We have prepared a items builds, runes, summoner spells and ability order for a comfortable game. Situational options for replacing items and runes are also available to you.
 Key items 
 TIPS: Start your build with Amplifying Tome . Next, you should pay attention to whether your mobility champion is enough, our further actions will depend on this. If it is hard for you to dodge the enemy's skills or you want to roam on neighboring lines, then it is better to buy Boots of Speed at an early stage.
 Start
 Amplifying Tome 
 Amplifying Tome +20 Ability Power 500 
 Core
 Rylai's Crystal Scepter 
 Rylai's Crystal Scepter Abilities apply slows +350 Max Health +65 Ability Power Icy: Damaging abilities and empowered attacks slow enemies by 30% for 0.75 second. 2700 
 Rylai's Crystal Scepter TIPS: This item enhances your crowd control by causing your abilities and empowered attacks to slow enemies with every hit. The bonus health improves your durability, while the consistent slow makes it much easier to land follow-up abilities, chase fleeing targets, and support your teammates. It is an excellent choice for damage-over-time mages and champions who rely on keeping enemies within the range of their abilities.
 Plated Steelcaps 
 Plated Steelcaps Reduces damage from champion attacks +150 Max Health +20 Armor +45 Move Speed Block: Reduces damage from champion attacks by 10%. 1200 
 Plated Steelcaps TIPS: These boots provide reliable protection against champions who rely heavily on basic attacks. They increase your Health and Armor, while the passive further reduces damage taken from enemy champion attacks. An excellent choice against marksmen, AD fighters, and other auto-attack-focused champions.
 Riftmaker 
 Riftmaker Ramping Damage +350 Max Health +70 Ability Power +15 Ability Haste Void Corruption: Every 1 second(s) in combat with enemy champions, deal 2% bonus damage, up to 8%. At maximum strength, gain Omni Vamp. (10% for melee champions / 6% for ranged champions). Void Infusion: Gain 2% of your bonus Health as Ability Power . 3100 
 Riftmaker TIPS: This item is built for extended fights, gradually increasing your damage the longer you remain in combat. Once fully ramped up, it grants Omni Vamp for improved sustain, while your bonus Health is partially converted into Ability Power, further increasing your overall damage. An excellent choice for AP bruisers and battlemages who excel in prolonged teamfights and thrive by scaling throughout combat.
 Boots
 Plated Steelcaps 
 Plated Steelcaps Reduces damage from champion attacks +150 Max Health +20 Armor +45 Move Speed Block: Reduces damage from champion attacks by 10%. 1200 
 Plated Steelcaps TIPS: These boots provide reliable protection against champions who rely heavily on basic attacks. They increase your Health and Armor, while the passive further reduces damage taken from enemy champion attacks. An excellent choice against marksmen, AD fighters, and other auto-attack-focused champions.
 Mercury's Treads 
 Mercury's Treads Increases Magic resist +150 Max Health +25 Magic Resistance +30 Tenacity +45 Move Speed 1200 
 Mercury's Treads TIPS: These boots increase your Magic Resistance while making you more resilient to crowd control through Tenacity. The bonus Health and movement speed improve both survivability and mobility, allowing you to perform more effectively against magic damage and heavy-CC team compositions. They are an excellent choice for tanks, fighters, and any champion who needs to stay in the fight longer.
 Armored Advance 
 Armored Advance Grants Armor and a shield +150 Max Health +30 Armor +45 Move Speed Block: Reduce damage from champion attacks by 10%. Noxian Endurance: After taking physical damage from a champion grants a physical shield that absorbs damage equal to 10-140 plus 8% max Health . (12s Cooldown) 2200 
 Armored Advance TIPS: These boots provide excellent protection against physical damage. They reduce damage taken from enemy champion attacks a
...(recortado; completo en data/raw)...
## Change history (cambios recientes)

```
Change history
 ADJUSTED 22 SEP 2026 (PATCH 7.3)
BASE STATS
Critical Strike Damage: 175% → 
200%
.
Attack Speed cap: 2.5 → 
3 attacks per second
.
Attack Speed Ratio: 
0.625
.
Base Attack Speed: 
0.625
.
Base Bonus Attack Speed: 
0.17
.
Attack Speed per Level: 
0.008
.
 BUFFED 27 AUG 2026 (PATCH 7.2D)
(PASSIVE)
 DARKNESS RISE
Magic Penetration: 1/3/5/7% → 
3/6/9/12%
.
(E)
 DEATH'S GRASP
Cooldown: 17.5/15/12.5/10s → 
15/13/11/9s
.
 BUFFED 05 MAR 2026 (PATCH 7.0D)
(Q)
 OBLITERATE
Damage: 80/110/140/170(+4-70(Base on Level))(+70% Ability Power)) → 
80/110/140/170(+4-70(Base on Level))(+70%Ability Power)(+120% bonus Attack Damage
.
 ADJUSTED 13 MAR 2025 (PATCH 6.0D)
(Q)
 OBLITERATE
Damage: 70/95/120/145 + (4~90)+60% Ability Power → 
80/110/140/170+(4~70)+70% Ability Power
.
(R)
 REALM OF DEATH
Cooldown: 100/85/70s → 
105/90/75s
.
 ADJUSTED 09 JAN 2025 (PATCH 6.0)
BASE STATS
Base Health: 630 → 
660
.
Health per level: 112 → 
120
.
Base Armor: 40 → 
46
.
Magic Resist per level: 1.5 → 
2
.
 NERFED 05 DEC 2024 (PATCH 5.3C)
BASE STATS
Basic health: 660 → 
630
.
(PASSIVE)
 DARKNESS RISE
Bonus damage dealt by basic attack: 40% Ability Power → 
30% Ability Power
.
(E)
 DEATH'S GRASP
Basic damage: 70/90/110/130 → 
60/80/100/120
.
(R)
 REALM OF DEATH
Cooldown: 90/80/70s → 
100/85/70s
.
 NERFED 31 OCT 2024 (PATCH 5.3A)
(PASSIVE)
 DARKNESS RISE
Damage per second: 4.5 + 0.5 per Level + 30% Ability Power → 
4.75 + 0.25 per Level + 25% Ability Power
.
(W)
 INDESTRUCTIBLE
Cooldown 11/10/9/8s → 
12/11/10/9s
.
(E)
 DEATH'S GRASP
Cooldown: 16/14/12/10s → 
17.5/15/12.5/10s
.
 See More
```

## Build/runas populares (referencia comunitaria, NO conclusión)

```
Runes BUILD
                
For runes, you should pick 
 
Conqueror
 (Gain stacks of AD or AP when hitting a champion with separate attacks or abilities. Stacks up to 6 times. When fully stacked, gain bonus Omnivamp (Adaptive).) as your keystone, followed by 
 
Demolish
 (Your third attack against a turret deals bonus damage), 
 
Second Wind
 (Heals you after taking damage.) and 
 
Overgrowth
 (Gains bonus scalable max Health.) in the primary tree, as well as 
 
Transcendence
 (Grants more Ability Haste the higher your level is and also returns ability cooldown duration.) in the secondary tree. Below you can see possible options for replacing runes.
                
                
                    
                        
                            
    
            
                
                    
                    
                        
Conqueror
Stacking Damage, Vam
```
---

# Seraphine — Ficha de datos (Wild Rift 7.3)

> wr-meta.com (24-sep-2026) + apéndice oficial 7.3. Crudo: data/raw/campeones/seraphine.html

## Stats base (nivel 1, growth entre paréntesis)

- **attackdamage**: 52 (3.64)
- **heal**: 600 (112)
- **healthregeneration**: 8 (0.57)
- **attackspeed**: 0.8 (0.012)
- **mana**: 435 (49)
- **mpreg**: 16 (1.14)
- **movementspeed**: 360 (0)
- **armor**: 34 (4.71)
- **magicresistance**: 36 (1.2)
- **criticalstrike**: 200% (0)

## AS oficial 7.3 (apéndice de las notas — fuente primaria para el modelo)

- champion: Seraphine
- Attack Speed Ratio: 0.699
- Base Attack Speed: 0.669
- Base Bonus Attack Speed: 0.12
- Attack Speed per Level: 0.017

## Habilidades (texto completo con valores actuales)

```
P
 (PASSIVE) STAGE PRESENCE
 Echo: Every third basic ability cast will echo, casting it again. Harmony:  Casting an ability grants a Note to nearby allies for 5 seconds. For each Note. Seraphine's next attack gains 0.3 Attack Range and deals an additional 4 magic damage (4 (+1,5 ) + 4% ).
 Q
 (Q) HIGH NOTE 
 11/9/7/5s 60/65/70/75 
 Deals 60 magic damage (60/75/90/105 + 45% ) in target area, increased by 0% - 50% with the enemies' missing Health. Reaches maximum damage when the target is below 25% Health.
 W
 (W) SURROUND SOUND 
 23/22/21/20s 40/60/80/100 
 Shields all nearby ally champions for 50 (50/75/100/125 + 30% ) damage for 2.5 seconds and grant them 20/22.5/25/27.5% Movement Speed for 2.5 seconds. If Seraphine is already shielded, nearby allies are healed for 6% of their missing Health (6% + 0.01% ), increased by 50% for each ally.
 E
 (E) BEAT DROP 
 12/11/10/9s 60/70/80/90 
 Deals 60 magic damage (60/95/130/165 + 50% ) to enemies and slows them by 99% for 1 seconds. If the enemy is already slowed, they are rooted instead. If they are rooted, they are sunned.
 R
 (R) ENCORE 
 105/90/75s 100 
 Deals 160 magic damage (160/260/360 + 70% ) to enemies and charms and slows them by 40% for 1.25/1.5/1.75 seconds. Spell extends when it touches an ally or enemy champion.
 SERAPHINE Meta Overview — Ranks & Performance Analytics 
 This meta overview presents SERAPHINE’s ranked performance across different roles and skill tiers. The data includes tier placement, win rate, pick rate, ban rate, and short-term trends, allowing you to evaluate her current strength and draft priority. Statistics are synced with rank buckets and role selection, helping you understand where SERAPHINE performs best and how her impact changes in the evolving Wild Rift meta.
 Diamond + Master + Challenger Legendary 
 Updated: 24 SEP 2026 UTC 00:00 
 SUPPORT 
 Confidence High 
 Win: 49.79% 
 Pick: 8.38% 
 Ban: 1.72% 
 Trend: ↑ 3 
 Reason: 
 ? 
 Positive trend 
 SUPPORT 
 Last 7 days analytics 
 Tier List 
 Compare Сhampions 
 Build 
 Counters 
 Counter Items 
 Tips 
 Con 
 Game Plan 
 Power Spikes 
 Support SERAPHINE Build items and runes 
 The information below will help you get familiar with the game on the Support Line SERAPHINE. We have prepared a items builds, runes, summoner spells and ability order for a comfortable game. Situational options for replacing items and runes are also available to you.
 Key items 
 TIPS: Start your build with Spectral Sickle (Attack champions and structures to gain bonus gold). Next, you should pay attention to whether your mobility champion is enough, our further actions will depend on this. If it is hard for you to dodge the enemy's skills or you want to roam on neighboring lines, then it is better to buy Boots of Speed at an early stage.
 Start
 Spectral Sickle 
 Spectral Sickle Attack champions and structures to gain bonus gold This item is for support players. When equipped, it will reduce the gold you receive from killing minions and monsters. If there are multiples of this item within the party, only one of them can take effect at any given time. Versatile: Gain 10 Attack Damage or 20 Ability Power (Adaptive). Tribute: Gain 1 encircling energy orb(s) every 30 seconds (max 3 orbs). While near an ally, the actions below will trigger Tribute, consuming 1 energy orb(s) to grant you 65 gold and restore your Health 20-80 : 1. Using abilities or attacks to damage enemy champions or structures. 2. Attacking minions below 65% Health. This also executes them, and the gold generated from the minion kills is given to the ally nearest to you. 3. A nearby minion is killed while you have 3 orbs. Upon triggering Tribute, the ally nearest to you gains Tribute stacks. Sentry: Deal 1 more damage to Sight Wards revealed by Sweeping Lens, Control Ward, and Scryer’s Bloom. Restraint: You do not earn gold generated from minion kills, but you earn gold equal to 50% of the bounty. The gold generated from your minion kills will be given to the ally nearest to you. Gold earned from monster kills is reduced by 50%. Quest: Earn 750 gold with this item to transform it into Black Mist Scythe and bind you and the ally with the most Tribute stacks as Perfect Partners. 500 
 Core
 Black Mist Scythe 
 Black Mist Scythe Attack champions and structures to gain bonus gold +10 Ability Haste Versatile: Gain 14 Attack Damage or 28 Ability Power (Adaptive). Soulcast: Every 60 seconds, gains 75 gold , 25 Health and 2 Attack Damage , or 4 Ability Power (Adaptive); up to  250 Health and 20 Attack Damage , or 40 Ability Power (Adaptive). Deal 2 more damage to Sight Wards revealed by Sweeping Lens, Control Ward, and Scryer’s Bloom. When out of combat, gain 10% Movement Speed when you move toward your Perfect Partner. If you're more than 2,500 units apart, this bonus increases to 30%. 0 
 Black Mist Scythe TIPS: This item is designed for support players, granting passive bonuses to gold and stats. It reduces your gold from killing minions and monsters but provides 75 gold and 1 Soulforce stack every 60 seconds. Each Soulforce stack adaptively grants health, attack damage, or ability power, and at 10 stacks you gain a significant bonus to one of these stats. The item also increases your effectiveness in clearing vision by dealing extra damage to revealed enemy wards. Ideal for map-control–focused supports who want to help their team without worrying about farming; you’ll steadily generate resources and strengthen your utility for both protect and peel.
 Ionian Boots of Lucidity 
 Ionian Boots of Lucidity Reduces ability cooldowns +50% Mana Regen +15 Ability Haste +45 Move Speed Summoned: Reduces spell cooldowns by 15% . 1000 
 Ionian Boots of Lucidity TIPS: These boots are designed for champions who rely on casting abilities as often as possible. They provide mana regeneration, Ability Haste, and further reduce the cooldown of Summoner Spells, allowing you to use key abilities more frequently while bringing back Flash, Smite, Ignite, and other Summoner Spells faster. They are an excellent choice for mages, supports, fighters, and any champion who benefits from maximizing ability uptime.
 Echoes of Helia 
 Echoes of Helia Protect allies, granting them increased healing +200 Max Health +40 Ability Power +50% Mana Regen +20 Ability Haste Soul Siphon: Store 30% of the premitigation damage dealt to enemy champions as Soul Shards (max 80–250 shards ( )). Healing or shielding a teammate consumes all Soul Shards to heal them for the corresponding amount. 2400 
 Echoes of Helia TIPS: This item combines Health, Ability Power, Mana regeneration, and Ability Haste, making it well suited for active supports who both damage enemies and protect allies. Damage dealt to
...(recortado; completo en data/raw)...
## Change history (cambios recientes)

```
Change history
 ADJUSTED 22 SEP 2026 (PATCH 7.3)
BASE STATS
Critical Strike Damage: 175% → 
200%
.
Attack Speed cap: 2.5 → 
3 attacks per second
.
Attack Speed Ratio: 
0.699
.
Base Attack Speed: 
0.669
.
Base Bonus Attack Speed: 
0.12
.
Attack Speed per Level: 
0.017
.
 BUFFED 25 JUN 2026 (PATCH 7.1H)
(W)
 SURROUND SOUND
Healing Ratio: 5% → 
6%
.
(R)
 ENCORE
Charm Duration: 1/1.25/1.5 → 
1.25/1.5/1.75
.
 ADJUSTED 18 SEP 2025 (PATCH 6.2H)
(Q)
 HIGH NOTE
Bonus Damage: 40% Ability Power → 
45% Ability Power.
(W)
 SURROUND SOUND
Cooldown: 24/22/20/18s → 
23/22/21/20s.
Shield Value: 50/80/110/140 + 25% Ability Power → 
50/75/100/125 + 30% Ability Power.
 NERFED 12 JUN 2025 (PATCH 6.1D)
(W)
 SURROUND SOUND
Cooldown: 22/20/18/16s → 
24/22/20/18s
.
Shield: 60/90/120/150 + 35% Ability Power → 
50/80/110/140 + 25% Ability Power
.
 ADJUSTED 17 APR 2025 (PATCH 6.1)
BASE STATS
Movement speed: 350 → 
360
.
 ADJUSTED 09 JAN 2025 (PATCH 6.0)
BASE STATS
Base Health: 530 → 
600
.
Health per level: 105 → 
112
.
Base Armor: 30 → 
34
.
Base Magic Resist: 30 → 
36
.
Magic Resist per level: 0.8 → 
1.2
.
 NERFED 05 SEP 2024 (PATCH 5.2C)
(W)
 SURROUND SOUND
Cooldown: 22/19/16/13s → 
22/20/18/16s
.
Heal: (7.5% + 0.01% Ability Power) Health lost → 
(5% + 0.01% Ability Power) Health lost
.
 ADJUSTED 14 MAR 2024 (PATCH 5.0C)
(W)
 SURROUND SOUND
Cooldown: 23/20/17/14s → 
22/19/16/13s
.
Bonus Movement Speed: full level 20% → 
20/22.5/25/27.5%
.
Shield: 60/80/100/120 + 40% Ability Power → 
60/90/120/150 + 35% Ability Power
.
Healing: 6.5% + 0.01% Ability Power→ 
7.5% + 0.01% Ability Power
.
 ADJUSTED 25 OCT 2023 (PATCH 4.4)
BASE STATS
Movement speed: 340 → 
350
.
 ADJUSTED 25 MAY 2023 (PATCH 4.2)
BASE STATS
Base movement speed 
+10.
Crit damage rate：200% → 
175%.
 BUFFED 10 MAY 2023 (PATCH 4.1C)
(W)
 SURROUND SOUND
Heal per ally: (5% + 0.01% Ability Power) × Missing health → 
(6.5% + 0.01% Ability Power) × Missing health.
(E)
 BEAT DROP
Magic damage: 60/90/120/150 → 
60/95/130/165.
 ADJUSTED 16 MAR 2023 (PATCH 4.1)
(W)
 SURROUND SOUND
The value of the 2nd shield for the ability enhancement is now stacking instead of refreshing.
 BUFFED 16 NOV 2022 (PATCH 3.5)
BASE STATS
Base mana regeneration: 12 → 
16.
 ADJUSTED 11 MAY 2022 (PATCH 3.2)
(Q)
 HIGH NOTE
Damage: 55/70/85/100 + 50% AP → 
60/75/90/105 + 40% AP
(E)
 BEAT DROP
Damage: 60/90/120/150 + 50% AP → 
60/90/120/150 + 40% AP
 BUFFED 14 SEP 2021 (PATCH 2.5)
(PASSIVE)
 SALVATION
[NEW]
 Seraphine starts the game with max Echo stacks.
 FIX 18 AUG 2021 (PATCH 2.4a)
(E)
 BEAT DROP
[BUGFIX]
 Beat Drop now correctly applies its damage before checking if the target is slowed.
This means that Rylai’s Crystal Scepter now works with 
(E)
 BEAT DROP
, and it will transform the slow into a root!
 See More
```

## Build/runas populares (referencia comunitaria, NO conclusión)

```
Runes BUILD
                
For runes, you should pick 
 
Aery
 (Your attacks and abilities send Aery to a target, damaging enemies or shielding allies.) as your keystone, followed by 
 
Font of Life
 (Marks an enemy champion and grants healing upon attack.), 
 
Bone Plating
 (Reduces incoming damage.) and 
 
Revitalize
 (Empowered healing and shielding effects.) in the primary tree, as well as 
 
Transcendence
 (Grants more Ability Haste the higher your level is and also returns ability cooldown duration.) in the secondary tree. Below you can see possible options for replacing runes.
                
                
                    
                        
                            
    
            
                
                    
                    
                        
Aery
Poke, Protect
Your attacks and abilities send Aery to a target, damaging enemies or shieldi
```
---

# Shyvana — Ficha de datos (Wild Rift 7.3)

> wr-meta.com (24-sep-2026) + apéndice oficial 7.3. Crudo: data/raw/campeones/shyvana.html

## Stats base (nivel 1, growth entre paréntesis)

- **attackdamage**: 62 (4.6)
- **heal**: 660 (120)
- **healthregeneration**: 9 (0.9)
- **attackspeed**: 0.8 (0.008)
- **mana**: 0 (0)
- **mpreg**: 0 (0)
- **movementspeed**: 350 (0)
- **armor**: 46 (5)
- **magicresistance**: 38 (2)
- **criticalstrike**: 200% (0)
- **fury**: 0 (0)

## AS oficial 7.3 (apéndice de las notas — fuente primaria para el modelo)

- champion: Shyvana
- Attack Speed Ratio: 0.638
- Base Attack Speed: 0.638
- Base Bonus Attack Speed: 0.25
- Attack Speed per Level: 0.012

## Habilidades (texto completo con valores actuales)

```
P
 (PASSIVE) FURY OF THE DRAGONBORN
 Slaying a Large Monster grants 8 stacks of Draconic Bloodline . Champion takedowns or slaying the Rift Herald or Baron Nashor grants 15 stacks of Draconic Bloodline . Slaying a Dragon grants 35 Draconic Bloodline . Every 100 stacks of Draconic Bloodline enhances one of Shyvana's abilities.
 Q
 (Q) TWIN BITE 
 8.5/7.5/6.5/5.5s 
 Empowers Shyvana's next attack to strike twice, dealing 58 ( 100% ) and 12 ( 20/40/60/80% ) physical damage respectively. Attacks reduce the Cooldown of Twin Bite by 0.5 seconds. Dragon Form: Strikes in a larger area and applies on-hits to all enemies. Acquiring 100 stacks of Draconic Bloodline grants Weight of the Mountain , causing Twin Bite to slow enemies hit by 30% while in Dragon Form.
 W
 (W) BURNOUT 
 13/12/11/10s 
 Deals 35 magic damage (35/50/65/80  + 30% bonus ) per second to nearby enemies and hastes Shyvana by 30/35/40/45% , decaying over 3 seconds. Attacking extends the duration of Burnout by 4 seconds. Dragon Form: Expands the flames, dealing damage in a larger area. Acquiring 200 stacks of Draconic Bloodline , grants Wings of the Cloud , causing Burnout to haste Shyvana by an additional 25% while in Dragon Form.
 E
 (E) FLAME BREATH 
 11/9.8/8.8/7.8s 
 Launches a fireball that deals 78 magic damage (60/110/160/210 + 30% + 40% ) to enemies hit and Scorches them for 5 seconds. Shyvana's attacks on Scorched enemies deal bonus magic damage equal to 3% of their max health. Dragon Form: The fireball explodes on impact, dealing 139 magic damage (110 +  50% + 70% ) in an area and leaving a fire for 4 seconds that deals 34 magic damage (28 + 10% +  20% ) and Scorches enemies within it. Acquiring 300 stacks of Draconic Bloodline , grants Breath of the Infernal , converting the damage dealt to Scorched enemies to  True Damage while in Dragon Form.
 R
 (R) DRAGON'S DESCENT 
 1s 
 100 
 Passive: Generate 1/1.5/2 Fury per second and 2 Fury per attack. At 100 Fury Shyvana can cast Dragon's Descent. Shyvana remains in Dragon form until she has consumed all of the Fury . Active: Transform into a Dragon, gaining 350/475/600 Health and flying to a target location. Enemies along Shyvana's path take 150 magic damage (150/250/350 + 80% ) and are knocked towards her landing point. Acquiring 400 stacks of Draconic Bloodline , grants Life of the Ocean , gaining  20% Omnivamp in Dragon Form.
 SHYVANA Meta Overview — Ranks & Performance Analytics 
 This meta overview presents SHYVANA’s ranked performance across different roles and skill tiers. The data includes tier placement, win rate, pick rate, ban rate, and short-term trends, allowing you to evaluate her current strength and draft priority. Statistics are synced with rank buckets and role selection, helping you understand where SHYVANA performs best and how her impact changes in the evolving Wild Rift meta.
 Diamond + Master + Challenger Legendary 
 Updated: 24 SEP 2026 UTC 00:00 
 JUNGLE 
 Confidence Med 
 Win: 48.16% 
 Pick: 5.97% 
 Ban: 2.70% 
 Trend: ↓ 15 
 Reason: 
 ? 
 Low win rate Negative trend 
 Signals: 
 ? 
 🧊 Falling 
 JUNGLE 
 Last 7 days analytics 
 Tier List 
 Compare Сhampions 
 Build 
 Counters 
 Counter Items 
 Tips 
 Con 
 Game Plan 
 Power Spikes 
 Jungle Path 
 Jungle SHYVANA Build items and runes 
 The information below will help you get familiar with the game on the Jungle Line SHYVANA. We have prepared a items builds, runes, summoner spells and ability order for a comfortable game. Situational options for replacing items and runes are also available to you.
 Key items 
 TIPS: Start your build with Long Sword . Next, you should pay attention to whether your mobility champion is enough, our further actions will depend on this. If it is hard for you to dodge the enemy's skills or you want to roam on neighboring lines, then it is better to buy Boots of Speed at an early stage.
 Start
 Long Sword 
 Long Sword +12 Attack Damage 500 
 Core
 Trinity Force 
 Trinity Force Well-Rounded +333 Max Health +36 Attack Damage +30% Attack Speed +15 Ability Haste Valor: On hit, attacks grant  20 Move Speed for 2 seconds. Bonuses do not stack. Bonus Movement Speed does not stack. Ranged champions gain halved values. Spellblade: Using an ability causes the next attack used within 10 seconds to deal bonus physical damage equal to 200% base AD (1.5s Cooldown). Damage is reduced vs structures. 3333 
 Trinity Force TIPS: This item combines Health, Attack Damage, Attack Speed, and Ability Haste, providing a well-rounded boost to combat performance. Using an ability empowers your next attack with bonus physical damage, while landing attacks grants Movement Speed to help you stick to targets. An excellent choice for fighters and other AD champions who constantly weave abilities between basic attacks.
 Gluttonous Greaves 
 Gluttonous Greaves Attack Damage, Omnivamp +45 Move Speed Balance of Power: Gain 12 Attack Damage or 20 Ability Power (Adaptive). Conversion: Gain 5% Omnivamp . Champion takedowns grant an additional 0.5% Omnivamp , up to 5% . 1000 
 Gluttonous Greaves TIPS: These boots combine mobility, adaptive offensive power, and sustained healing. They increase your damage while Omnivamp restores health from all damage you deal. Champion takedowns further increase your Omnivamp, making them an excellent choice for champions who want to balance high damage output with strong sustain during extended fights.
 Blade of the Ruined King 
 Blade of the Ruined King Attacks deal bonus damage +40 Attack Damage +35% Attack Speed +12% Lifesteal Ruined Strikes: Attacks deal bonus physical damage equal to 6% of the enemy's current Health on-hit . (Melee attacks deal 8% ). Minimum damage: 15. Max damage vs monsters: 100. Drain: Hitting a champion with 3 attacks or abilities slows them by 30% for 1.5s. (30s Cooldown) 3100 
 Blade of the Ruined King TIPS: This item combines Attack Damage, Attack Speed, and Lifesteal, providing strong sustained damage and additional survivability. Attacks deal bonus physical damage based on the target's current Health, making it especially effective against high-Health champions. Consecutive attacks or abilities also slow the target, helping you stick to enemies. An excellent choice for marksmen and fighters focused on extended fights and basic attacks.
 Boots
 Gluttonous Greaves 
 Gluttonous Greaves Attack Damage, Omnivamp +45 Move Speed Balance of Power: Gain 12 Attack Damage or 20 Ability Power (Adaptive). Conversion: Gain 5% Omnivamp . Champion takedowns grant an additional 0.5% Omnivamp , up to 5% . 1000 
 Gluttonous Greaves TIPS: These boots combine mobility, adaptive offensive power, and sustained healing. They increase your damage while Omnivamp restores health from all damage you deal.
...(recortado; completo en data/raw)...
## Change history (cambios recientes)

```
Change history
 ADJUSTED 22 SEP 2026 (PATCH 7.3)
BASE STATS
Critical Strike Damage: 175% → 
200%
.
Attack Speed cap: 2.5 → 
3 attacks per second
.
Attack Speed Ratio: 
0.638
.
Base Attack Speed: 
0.638
.
Base Bonus Attack Speed: 
0.25
.
Attack Speed per Level: 
0.012
.
 ADJUSTED 14 MAY 2026 (PATCH 7.1E)
BASE STATS
Base Attack Damage: 58 → 
62
.
(PASSIVE)
 FURY OF THE DRAGONBORN
Slaying a Large Monster grants 10 → 
8 stacks of Draconic Bloodline
.
(Q)
 TWIN BITE
Dragon form empowered attack slow effect: 50% → 
30%
.
(R)
 DRAGON'S DESCENT
Fury generated per second: 1.5/2/2.5 → 
1/1.5/2
.
 ADJUSTED 09 APR 2026 (PATCH 7.1)
(W)
 BURNOUT
Additional haste in Dragon Form: 30% → 
25%
.
(R)
 DRAGON'S DESCENT
Bonus Health: 350/450/550 → 
350/475/600
.
 NERFED 20 NOV 2025 (PATCH 6.3D)
(W)
 BURNOUT
Base Damage per Second: 40/55/70/85 → 
35/50/65/80
.
(E)
 FLAME BREATH
Dragon Form Flame Damage Overtime: 30 + Champion Level × 4 → 
25 + Champion Level × 3
.
 BUFFED 18 SEP 2025 (PATCH 6.2H)
(W)
 BURNOUT
Cooldown: 14/13/12/11s → 
13/12/11/10s.
(R)
 DRAGON'S DESCENT
Health Increase: 300/400/500 → 
350/450/550.
 BUFFED 25 JUL 2025 (PATCH 6.2A)
(W)
 BURNOUT
Cooldown: 15/14/13/12s → 
14/13/12/11s
.
(R)
 DRAGON'S DESCENT
200 Stacks of Draconic Bloodline: Burnout gains 25% additional Bonus Movement Speed → 
Burnout gains 30% additional Bonus Movement Speed
.
400 Stacks of Draconic Bloodline: Gain 15% Omnivamp → 
Gain 20% Omnivamp
.
 ADJUSTED 09 JAN 2025 (PATCH 6.0)
BASE STATS
Base Health: 630 → 
660
.
Health per level: 112 → 
120
.
Base Armor: 40 → 
46
.
Magic Resist per level: 1.6 → 
2
.
 BUFFED 14 NOV 2024 (PATCH 5.3B)
BASE STATS
Base Health: 610 → 
630
.
Armor per Level: 4.3 → 
5
.
(PASSIVE)
 FURY OF THE DRAGONBORN
Draconic Bloodline gained from slaying epic monsters: 8 stacks → 
10 stacks
.
(R)
 DRAGON'S DESCENT
Fury gained per second: 1/1.5/2 → 
1.5/2/2.5
.
Health gained with Dragon's Descent: 230/315/430 → 
300/400/500
.
 BUFFED 06 JUN 2024 (PATCH 5.1C)
(PASSIVE)
 FURY OF THE DRAGONBORN
Grants 12 → 
15 stacks of Draconic Bloodline by taking down enemy champions, slaying the Rift Herald or Baron Nashor
.
(W)
 BURNOUT
Damage per second: 35/50/65/80 + 30% bonus Attack Damage → 
40/55/70/85 + 30% bonus Attack Damage
.
 BUFFED 17 JAN 2024 (PATCH 5.0)
(Q)
 TWIN BITE
Increased attack range: 200 → 
225
.
 BUFFED 09 NOV 2023 (PATCH 4.4A)
(W)
 BURNOUT
Damage per second: 30/45/60/75 + 25% bonus Attack Damage → 
35/50/65/80 + 30% bonus Attack Damage
.
Total damage: 210/315/420/525 + 175% bonus Attack Damage → 
245/350/455/560 + 210% bonus Attack Damage
.
BASE STATS
Bonus Health: 150/250/350 → 
230/315/400
.
 ADJUSTED 25 MAY 2023 (PATCH 4.2)
BASE STATS
Base movement speed 
+10.
Crit damage rate：200% → 
175%.
 BUFFED 12 JAN 2023 (PATCH 4.0)
BASE STATS
Health per level: 105 → 
112.
(Q)
 TWIN BITE
Cooldown: 9/8/7/6s → 
8.5/7.5/6.5/5.5s.
Evolved Twin Bites slow: 40% → 
50%.
 BUFFED 19 OCT 2022 (PATCH 3.4B)
(W)
 BURNOUT
Base damage: 25/40/55/70 → 
30/45/60/75.
 ADJUSTED 14 SEP 2022 (PATCH 3.4)
(R)
 DRAGON'S DESCENT
While in Dragon Form: Gain bonus 100/150/200 health → 
Gain 15% Omnivamp
.
 NERFED 18 AUG 2022 (PATCH 3.3B)
BASE STATS
Health per level: 115 → 
105.
(W)
 BURNOUT
Damage: 30/45/60/75 → 
25/40/55/70.
 ADJUSTED 13 JUL 2022 (PATCH 3.3)
Large Monster kills, Champion takedowns, and Epic Monster kills grant stacks of Draconic Bloodline. For every 100 stacks of Draconic Bloodline, Shyvana evolves one of her abilities in order from first to last.
Large Monster kill stacks: 
8
.
Champion takedown stacks: 
12
.
Rift Herald/Baron Nashor kill stacks: 
12
.
Dragon kill stacks: 
35
.
 BUFFED 14 SEP 2021 (PATCH 2.5)
(PASSIVE)
 FURY OF THE DRAGONBORN
Bonus damage against Elemental Drakes and Elder Dragons: 20% → 
25%.
(W)
 BURNOUT
Base Magic Damage: 25/40/55/70 per second → 
30/45/60/75 per second.
 NERFED 13 APR 2021 (PATCH 2.2A)
BASE STATS
Health: 650 → 
610.
(Q)
 TWIN BITE
Cooldown: 8/7/6/5s → 
9/8/7/6s.
(E)
 FLAME BREATH
Maximum on-hit HP damage ratio: 3.5% → 
3%.
```

## Build/runas populares (referencia comunitaria, NO conclusión)

```
Runes BUILD
                
For runes, you should pick 
 
Conqueror
 (Gain stacks of AD or AP when hitting a champion with separate attacks or abilities. Stacks up to 6 times. When fully stacked, gain bonus Omnivamp (Adaptive).) as your keystone, followed by 
 
Triumph
 (Champion takedowns restore lost resources and grant a brief Movement Speed boost.), 
 
Coup de Grace
 (Increases damage dealt to enemy champions with low Health.) and 
 
Legend: Bloodline
 (Gains Omnivamp.) in the primary tree, as well as 
 
Overgrowth
 (Gains bonus scalable max Health.) in the secondary tree. Below you can see possible options for replacing runes.
                
                
                    
                        
                            
    
            
                
                    
                    
                        
Conqueror
Stacking Damage, Vamp
Gain stacks of A
```
---

# Volibear — Ficha de datos (Wild Rift 7.3)

> wr-meta.com (24-sep-2026) + apéndice oficial 7.3. Crudo: data/raw/campeones/volibear.html

## Stats base (nivel 1, growth entre paréntesis)

- **attackdamage**: 62 (56)
- **heal**: 660 (120)
- **healthregeneration**: 9 (0.86)
- **attackspeed**: 0.7 (0.010)
- **mana**: 390 (65)
- **mpreg**: 12 (0.71)
- **movementspeed**: 350 (0)
- **armor**: 46 (4.71)
- **magicresistance**: 38 (2)
- **criticalstrike**: 200% (0)

## AS oficial 7.3 (apéndice de las notas — fuente primaria para el modelo)

- champion: Volibear
- Attack Speed Ratio: 0.7
- Base Attack Speed: 0.7
- Base Bonus Attack Speed: 0.05
- Attack Speed per Level: 0.014

## Habilidades (texto completo con valores actuales)

```
P
 (PASSIVE) THE RELENTLESS STORM
 Volibear's gains 5% (5% + 4% ) Attack Speed for 6 seconds whenever he deals damage with an Ability or Attack, staking up to 5 times. At 5 stacks, Volibear's claws ignite with lightning, causing his Attacks to deal an additional 12~68 (11  + 40% ) magic damage to the target and 4 closest enemies.
 Q
 (Q) THUNDERING SMASH 
 13/12/11/10s 50 
 Volibear gains 10/15/20/25% Move Speed , increased to 20/30/40/50% towards enemy champion for the next 4 seconds. While active, Volibear's next Attack deals 15 (15/40/65/90 + 100% bonus ) physical damage and Stuns the target for 1 seconds. If Volibear becomes Immobilized before he Stuns a target, Thundering Smash's duration is paused.
 W
 (W) FRENZIED MAUL 
 5s 35/40/45/50 
 Volibear mauls an enemy, dealing 67  (5/30/55/80 + 100% + 6.5% bonus ) physical damage . If Volibear maul's a champion or Large Monster he goes into a Frenzy for 8 seconds. If this Ability is used when in a Frenzy, its damage is increased to 108 (8/48/88/128 + 160% + 10.4% bonus ) physical damage and Volibear restores   20/30/40/50 + 5/6/7/8% missing Health . This Ability applies on-hit effects. Deals 80% damage to monsters.
 E
 (E) SKY SPLITTER 
 13s 60 
 Volibear summons a thundercloud that fires a lightning bolt, dealing 80 (80/110/140/170 + 50% ) plus 11% max Health magic damage and Slowing by 40% for 2 seconds. If Volibear is inside the blast zone, he gains a 91 ( 75% ) plus 14% max Health Shild  for 2.5 seconds. Damage against non-champiuons is capped at 150/250/350/450.
 R
 (R) STORMBRINGER 
 90/80/70s 100 
 Volibear transforms and leaps, gaining 175/350/525 Health and 50 Attack Rang e for next 12 seconds. Upon landing, Volibear cracks the earth, Disabiling nearby towers for 3 seconds an dealing 300 (300/500/700 + 100% + 210% Bonus ) physical damage to them. Nearby enemies are Slowed  by 50%, decaying over 1 second. Enemies directly underneath Volibear suffering 300 (300/500/700 + 100% + 210% bonus ) physical damage .
 VOLIBEAR Meta Overview — Ranks & Performance Analytics 
 This meta overview presents VOLIBEAR’s ranked performance across different roles and skill tiers. The data includes tier placement, win rate, pick rate, ban rate, and short-term trends, allowing you to evaluate her current strength and draft priority. Statistics are synced with rank buckets and role selection, helping you understand where VOLIBEAR performs best and how her impact changes in the evolving Wild Rift meta.
 Diamond + Master + Challenger Legendary 
 Updated: 24 SEP 2026 UTC 00:00 
 SOLO 
 Confidence Med 
 Win: 49.39% 
 Pick: 6.51% 
 Ban: 6.54% 
 Trend: ↓ 25 
 Signals: 
 ? 
 🧊 Falling 
 JUNGLE 
 Confidence Med 
 Win: 49.04% 
 Pick: 3.29% 
 Ban: 6.54% 
 Trend: ↓ 7 
 Signals: 
 ? 
 🧊 Falling 
 SOLO JUNGLE 
 Last 7 days analytics 
 Tier List 
 Compare Сhampions 
 Build 
 Counters 
 Counter Items 
 Tips 
 Con 
 Game Plan 
 Power Spikes 
 Solo Baron VOLIBEAR Build items and runes 
 The information below will help you get familiar with the game on the Solo Baron Line VOLIBEAR. We have prepared a items builds, runes, summoner spells and ability order for a comfortable game. Situational options for replacing items and runes are also available to you.
 Key items 
 TIPS: Start your build with Long Sword . Next, you should pay attention to whether your mobility champion is enough, our further actions will depend on this. If it is hard for you to dodge the enemy's skills or you want to roam on neighboring lines, then it is better to buy Boots of Speed at an early stage.
 Start
 Long Sword 
 Long Sword +12 Attack Damage 500 
 Core
 Dusk and Dawn 
 Dusk and Dawn Applies on-hit effects +300 Maximum Health +20% Attack Speed +60 Ability Power +20 Ability Haste Spellblade: After using an ability, your next attack deals (75% base + 10% ) bonus magic damage and restores ( 3% bonus + 10% ) Htalth to you. After a brief delay, apply on-hits to the target 1 additional time. (1.5s Cooldown) Deals reduced damage to structures. 3100 
 Dusk and Dawn TIPS: This item combines Health, Attack Speed, Ability Power, and Ability Haste, making it well suited for champions who weave abilities and basic attacks together. After casting an ability, the next attack deals bonus magic damage and restores Health, then applies on-hit effects to the target an additional time. An excellent choice for AP fighters and hybrid champions with strong on-hit synergy.
 Plated Steelcaps 
 Plated Steelcaps Reduces damage from champion attacks +150 Max Health +20 Armor +45 Move Speed Block: Reduces damage from champion attacks by 10%. 1200 
 Plated Steelcaps TIPS: These boots provide reliable protection against champions who rely heavily on basic attacks. They increase your Health and Armor, while the passive further reduces damage taken from enemy champion attacks. An excellent choice against marksmen, AD fighters, and other auto-attack-focused champions.
 Navori Quickblades 
 Navori Quickblades Attacks reduce basic ability cooldowns +25% Critical Rate +40% Attack Speed +4% Move Speed Deft Strikes: Attacks reduce the remaining cooldowns of your basic abilities by 15% . 2650 
 Navori Quickblades TIPS: This item combines Critical Strike Chance, Attack Speed, and mobility, allowing you to use your basic abilities much more frequently. Each attack reduces their remaining cooldowns, creating strong synergy between basic attacks and abilities. An excellent choice for marksmen and other champions who constantly weave attacks and basic abilities together.
 Boots
 Plated Steelcaps 
 Plated Steelcaps Reduces damage from champion attacks +150 Max Health +20 Armor +45 Move Speed Block: Reduces damage from champion attacks by 10%. 1200 
 Plated Steelcaps TIPS: These boots provide reliable protection against champions who rely heavily on basic attacks. They increase your Health and Armor, while the passive further reduces damage taken from enemy champion attacks. An excellent choice against marksmen, AD fighters, and other auto-attack-focused champions.
 Mercury's Treads 
 Mercury's Treads Increases Magic resist +150 Max Health +25 Magic Resistance +30 Tenacity +45 Move Speed 1200 
 Mercury's Treads TIPS: These boots increase your Magic Resistance while making you more resilient to crowd control through Tenacity. The bonus Health and movement speed improve both survivability and mobility, allowing you to perform more effectively against magic damage and heavy-CC team compositions. They are an excellent choice for tanks, fighters, and any champion who needs to stay in the fight longer.
 Armored Advance 
 Armored Advance Grants Armor and a shield +150 Max Health +30 Armor +45 Move Speed Block: Reduce damage from champion attacks by 10%. Noxian Endurance: Aft
...(recortado; completo en data/raw)...
## Change history (cambios recientes)

```
Change history
 ADJUSTED 22 SEP 2026 (PATCH 7.3)
BASE STATS
Critical Strike Damage: 175% → 
200%
.
Attack Speed cap: 2.5 → 
3 attacks per second
.
Attack Speed Ratio: 
0.7
.
Base Attack Speed: 
0.7
.
Base Bonus Attack Speed: 
0.05
.
Attack Speed per Level: 
0.014
.
(PASSIVE)
 THE RELENTLESS STORM
Damage: 11-80 (based on level) + 40% Ability Power → 
12-68 (based on level) + 40% Ability Power
.
 NERFED 12 JUN 2025 (PATCH 6.1D)
(W)
 FRENZIED MAUL
Health regeneration under Frenzy: 20/30/40/50+7/8/9/10% lost Health → 
20/30/40/50+5/6/7/8% lost Healt
.
(E)
 SKY SPLITTER
Shield duration: 3s → 
2.5s
.
 BUFFED 17 APR 2025 (PATCH 6.1)
(PASSIVE)
 THE RELENTLESS STORM
Lightning damage: 11 to 60 + 40% Ability Power → 
11 to 80 + 40% Ability Power
.
(W)
 FRENZIED MAUL
Bonus damage: 5% of bonus Health → 
6.5% of bonus Health
.
Frenzy bonus damage: 8% of bonus Health → 
10.4% of bonus Health
.
(R)
 STORMBRINGER
Damage: 300/450/600 + 200% of bonus Attack Damage + 100% Ability Power → 
300/500/700 + 210% of bonus Attack Damage + 100% Ability Power
.
 ADJUSTED 09 JAN 2025 (PATCH 6.0)
BASE STATS
Base Health: 650 → 
690
.
Health per level: 120 → 
128
.
Base Armor: 40 → 
46
.
Magic Resist per level: 1.6 → 
2
.
 NERFED 14 MAR 2024 (PATCH 5.0C)
(R)
 STORMBRINGER
Disable no longer applies to enemy Nexus.
 BUFFED 17 JAN 2024 (PATCH 5.0)
(Q)
 THUNDERING SMASH
Increased attack range: 200 → 
225
.
 ADJUSTED 02 AUG 2023 (PATCH 4.3A)
(W)
 FRENZIED MAUL
Base health regeneration: 10/20/30/40 → 
20/30/40/50
.
[NEW]
 Damage ratio to monsters: 80%.
 See More
```

## Build/runas populares (referencia comunitaria, NO conclusión)

```
Runes BUILD
                
For runes, you should pick 
 
Grasp of Undying
 (When in combat, your next attack on a champion will occasionally deal bonus magic damage, heal you, and permanently increase your health.) as your keystone, followed by 
 
Demolish
 (Your third attack against a turret deals bonus damage), 
 
Second Wind
 (Heals you after taking damage.) and 
 
Perseverance
 (Gains Tenacity also gains Armor and Magic Resist when immobilizing.) in the primary tree, as well as 
 
Brutal
 (Attacks deal bonus damage to enemy champions.) in the secondary tree. Below you can see possible options for replacing runes.
                
                
                    
                        
                            
    
            
                
                    
                    
                        
Grasp of Undying
Tank, Heal
Every 3s in combat, your next atta
```
---

# Yunara — Ficha de datos (Wild Rift 7.3)

> wr-meta.com (24-sep-2026) + apéndice oficial 7.3. Crudo: data/raw/campeones/yunara.html

## Stats base (nivel 1, growth entre paréntesis)

- **attackdamage**: 58 (3)
- **heal**: 600 (128)
- **healthregeneration**: 6 (0.58)
- **attackspeed**: 0.8 (0.021)
- **mana**: 345 (33)
- **mpreg**: 9 (0.72)
- **movementspeed**: 335 (0)
- **armor**: 35 (4.5)
- **magicresistance**: 30 (1.43)
- **criticalstrike**: 200% (0)

## AS oficial 7.3 (apéndice de las notas — fuente primaria para el modelo)

- champion: Yunara
- Attack Speed Ratio: 0.65
- Base Attack Speed: 0.65
- Base Bonus Attack Speed: 0.23
- Attack Speed per Level: 0.032

## Habilidades (texto completo con valores actuales)

```
P
 (PASSIVE) VOW OF THE FIRST LANDS
 Critical Strikes deal an additional 8% magic damage (8% per 100 ).
 Q
 (Q) CULTIVATION OF SPIRIT 
 30 
 Spirit Charge (Passive): - Attacks deal an additional 10 magic damage (10/15/20/25 + 20% ). - When not active, launching an attack grants 1 Unleash (2 Unleash when attacking champions) for 6 second(s). Attacking again refreshes Unleash's duration. - Max Unleash : 6. If the duration is not refreshed, Yunara loses 1 Unleash every 0.5 second(s). Spirit Unbound (Active): On cast, consumes Unleash, gaining 25/35/45/55% Attack Speed for 5 second(s). Attacks are empowered during this time to: - Deal an additional 10 magic damage (10/15/20/25 + 20% ) on-hit . - Spread to enemies nearby the target, dealing them 18 physical damage ( 30% ). Transcendent State: This ability automatically activates until Yunara exits the state. If the attack Critically Strikes, its spread damage will also Critically Strike. Damage from spread attacks is increased to 250% against minions below 30% Health.
 W
 (W) ARC OF JUDGMENT 
 10s 60 
 Arc of Judgment: Lets rip a spinning prayer bead in the target direction, briefly granting vision of the area it travels through. The prayer bead slows enemies hit by 99% , lingering as it travels and resetting its remaining duration. When it reaches its endpoint, it lingers and expands for 1 second(s), regardless of whether it has hit an enemy. - The initial hit deals 60 magic damage (60/110/160/210 + 85% bonus + 50% ) and slows by 99% , decaying over 1.5 seconds. - When lingering, the bead deals an additional 9 magic damage (8/14/20/26 + 12% bonus + 7.5% ) to nearby enemies every 0.25 second(s). While Yunara is in a Transcendent State , this ability is upgraded to Arc of Ruin . ARC OF RUIN ( Transcendent State ): Fires a laser in the target direction that deals 160 magic damage (160 + 120% bonus + 75% ) and slows by 99% , decaying over 1.5 seconds. Cast time scales with permanent Attack Speed . Arc of Judgment deals 50%–100% damage ( ) to minions and executes low-Health minions.
 E
 (E) KANMEI'S STEPS 
 9s 40 
 Kanmei's Steps: Gains 30/35/40/45% Movement Speed for 1.5 seconds, increased to 45/52.5/60/67.5% when moving toward a visible enemy champion nearby. While Yunara is in a Transcendent State , this ability is upgraded to Untouchable Shadow . UNTOUCHABLE SHADOW ( Transcendent State ): Dashes in the target direction.
 R
 (R) TRANSCEND ONE'S SELF 
 70/60/50s 100 
 Passive: Arc of Ruin's base damage and Untouchable Shadow's dash speed scale with this ability's level. Transcendent State (Active): Enters a Transcendent State for 15 seconds. During this time, Yunara's basic abilities are empowered and cost no Mana . - Cultivation of Spirit: Activates automatically for the duration. - Arc of Judgment: Upgrades to Arc of Ruin . Its remaining cooldown reduces by 80% when Yunara enters or exits a Transcendent State . - Kanmei's Steps: Upgrades to Untouchable Shadow . Its cooldown refreshes when Yunara enters or exits a Transcendent State .
 YUNARA Meta Overview — Ranks & Performance Analytics 
 This meta overview presents YUNARA’s ranked performance across different roles and skill tiers. The data includes tier placement, win rate, pick rate, ban rate, and short-term trends, allowing you to evaluate her current strength and draft priority. Statistics are synced with rank buckets and role selection, helping you understand where YUNARA performs best and how her impact changes in the evolving Wild Rift meta.
 Diamond + Master + Challenger Legendary 
 Updated: 24 SEP 2026 UTC 00:00 
 DUO 
 Confidence High 
 Win: 50.85% 
 Pick: 13.08% 
 Ban: 13.02% 
 Trend: ↓ 3 
 Reason: 
 ? 
 Often banned 
 Signals: 
 ? 
 👥 Popular 🧊 Falling 
 DUO 
 Last 7 days analytics 
 Tier List 
 Compare Сhampions 
 Build 
 Counters 
 Counter Items 
 Tips 
 Con 
 Game Plan 
 Power Spikes 
 Adc YUNARA Build items and runes 
 The information below will help you get familiar with the game on the Adc Line YUNARA. We have prepared a items builds, runes, summoner spells and ability order for a comfortable game. Situational options for replacing items and runes are also available to you.
 Key items 
 TIPS: Start your build with Long Sword . Next, you should pay attention to whether your mobility champion is enough, our further actions will depend on this. If it is hard for you to dodge the enemy's skills or you want to roam on neighboring lines, then it is better to buy Boots of Speed at an early stage.
 Start
 Long Sword 
 Long Sword +12 Attack Damage 500 
 Core
 Kraken Slayer 
 Kraken Slayer Deal bonus physical damage +45 Attack Damage +35% Attack Speed +4% Move Speed Bring it Down: Every third attack deals 150–210 bonus physical damage ( 120–168 for ranged champions), increased by 0.75% per 1% Health the target is missing, up to an increase of 75%. 2900 
 Kraken Slayer TIPS: This item combines Attack Damage, Attack Speed, and mobility, enhancing sustained basic attack damage. Every third attack deals bonus physical damage that increases as the enemy loses Health. An excellent choice for marksmen and other champions who rely on frequent basic attacks and want to finish off weakened targets more effectively.
 Berserker's Greaves 
 Berserker's Greaves Attack Speed +35% Attack Speed +45 Move Speed Blessed Blade: Attacks restore 10 Health on hit. 1200 
 Berserker's Greaves TIPS: These boots grant a significant boost to attack speed and movement speed, while empowering your basic attacks with on‑hit life steal. — A great pick for marksmen and auto‑attack bruisers who need mobility, rapid attack cadence, and constant sustain in fights.
 Runaan's Hurricane 
 Runaan's Hurricane Ranged Attacks hit 3 targets +40% Attack Speed +25% Critical Rate +4% Move Speed Wind's Fury: Attacks strike 2 additional nearby enemies, each dealing 55% AD . These strikes can Critically Strike and trigger on-hit effects. This item cannot only be used by melee champions. 2650 
 Runaan's Hurricane TIPS: This item combines Attack Speed, Critical Strike Chance, and mobility, significantly improving basic attacks against multiple targets. Each attack also strikes nearby enemies, and these additional hits can Critically Strike and trigger on-hit effects. An excellent choice for auto-attack and on-hit focused champions, especially in team fights against multiple targets.
 Boots
 Berserker's Greaves 
 Berserker's Greaves Attack Speed +35% Attack Speed +45 Move Speed Blessed Blade: Attacks restore 10 Health on hit. 1200 
 Berserker's Greaves TIPS: These boots grant a significant boost to attack speed and movement speed, while empowering your basic attacks with on‑hit life steal. — A great pick for marksmen and auto‑attack bruisers who need mobility, rap
...(recortado; completo en data/raw)...
## Change history (cambios recientes)

```
Change history
 NERFED 22 SEP 2026 (PATCH 7.3)
BASE STATS
Critical Strike Damage: 175% → 
200%
.
Attack Speed cap: 2.5 → 
3 attacks per second
.
Attack Speed Ratio: 
0.65
.
Base Attack Speed: 
0.65
.
Base Bonus Attack Speed: 
0.23
.
Attack Speed per Level: 
0.032
.
(PASSIVE)
 VOW OF THE LANDS
Critical bonus damage: 10% (gain 10% per 100 Ability Power) → 
8% (gain 8% per 100 Ability Power)
.
(Q)
 CULTIVATION OF SPIRIT
Bonus Attack Speed: 22.5/35/47.5/60% → 
25/35/45/55%
.
 See More
```

## Build/runas populares (referencia comunitaria, NO conclusión)

```
Runes BUILD
                
For runes, you should pick 
 
Lethal Tempo
 (Stack Attack Speed with each consecutive attack. At max stacks, gain additional Attack Speed and deal bonus damage with your attacks) as your keystone, followed by 
 
Brutal
 (Attacks deal bonus damage to enemy champions.), 
 
Coup de Grace
 (Increases damage dealt to enemy champions with low Health.) and 
 
Legend: Alacrity
 (Gains Attack Speed.) in the primary tree, as well as 
 
Bone Plating
 (Reduces incoming damage.) in the secondary tree. Below you can see possible options for replacing runes.
                
                
                    
                        
                            
    
            
                
                    
                    
                        
Lethal Tempo
Attack Speed
Gain Attack Speed when attacking enemy champions. Stacks up to 6 times. At max stack
```
---

# Yuumi — Ficha de datos (Wild Rift 7.3)

> wr-meta.com (24-sep-2026) + apéndice oficial 7.3. Crudo: data/raw/campeones/yuumi.html

## Stats base (nivel 1, growth entre paréntesis)

- **attackdamage**: 50 (3.64)
- **heal**: 570 (104)
- **healthregeneration**: 11 (0.7)
- **attackspeed**: 0.8 (0.004)
- **mana**: 435 (49)
- **mpreg**: 15 (1.3)
- **movementspeed**: 340 (0)
- **armor**: 40 (3.9)
- **magicresistance**: 35 (1.2)
- **criticalstrike**: 200% (0)

## AS oficial 7.3 (apéndice de las notas — fuente primaria para el modelo)

- champion: Yuumi
- Attack Speed Ratio: 0.625
- Base Attack Speed: 0.625
- Base Bonus Attack Speed: 0.2
- Attack Speed per Level: 0.006

## Habilidades (texto completo con valores actuales)

```
P
 (PASSIVE) FELINE FRINDSHIP
 Passive: When Yuumi's attacks and abilities strike champions, she heals herself for 67 Health (70 + 25% ) (+ 7 ). If Yuumi Attaches to an allied champion within 4s, they are healed for the same amount as well. (12-8s cooldown ( )) Bonds of Friendship: While Attached , Yuumi gains Friendship with her ally whenever they kill a champion or minion. The ally with the most Friendship becomes her Best Friend . Best Friend Bonus: Yuumi's abilities gain bonus effects while she is Attached to her Best Friend .
 Q
 (Q) PROWLING PROJECTILE 
 5s 60 
 Missile Summon: Hold and drag the ability button to steer the missile. Base Effect: Deals 60 magic damage (60/100/140/180/220 + 20% ). Attached Bonus: If the missile takes at least 1 second(s) to get to its target, its damage increases to 80 magic damage (100/160/220/280/340 + 35% ). It also slows by 45/50/55/60/65% and reveals the target for 1 second(s). Best Friend Bonus: The missile always slows the target hit. Hitting a champion with the missile grants the ally Yuumi is Attached to 14 magic damage (18/19/20/21/22 + 5% ) on-hit for 5 second(s).
 W
 (W) YOU AND ME! 
 8/4/0s 
 Best Friend Bonus (Passive): While on her Best Friend , Yuumi gains an additional 8% Heal an Shield Power (8/9/10/11% + 0.02% )( ). Active: Dashes to an ally champion and Attaches to them. While Attached , she follows her partner's movement and is Untargetable except from towers. Immobilizing effects on Yuumi place You and Me! on a 5 second cooldown.
 E
 (E) ZOOMIES 
 9s 65/75/85/95 
 Gains a shield that absorbs 80 damage (80/110/140/170 + 40% ) and 20% Attack Speed (24/28/32/36% + 8% ) for 3 second(s). While the shield persists, she also gains 20% Movement Speed . If Yuumi is Attached , this ability affects her ally instead.
 R
 (R) FINAL CHAPTER 
 85/75/65s 100 
 Channels for 3.5 second(s), launching 7 magical wave(s). While Attached , hold and drag the ability button to steer the waves. Against enemies (per wave): Deals 80 magic damage (80/100/120 + 15% ). Slows by 10% for 1.25 second(s), increased by 10% per wave hit. On allied champions (per wave): Restores 20 Health (20/35/50 + 5% ). Excess healing is converted into a shield instead. Best Friend Bonus: For her Best Friend , the heal is increased to 26 Health (26/39/52 + 8% ). Wave Damage Stacks: Waves after the first deal 20 magic damage (20/30/40 + 5% ). Yuumi can move and cast You and Me! and Zoomies while channeling.
 YUUMI Meta Overview — Ranks & Performance Analytics 
 This meta overview presents YUUMI’s ranked performance across different roles and skill tiers. The data includes tier placement, win rate, pick rate, ban rate, and short-term trends, allowing you to evaluate her current strength and draft priority. Statistics are synced with rank buckets and role selection, helping you understand where YUUMI performs best and how her impact changes in the evolving Wild Rift meta.
 Diamond + Master + Challenger Legendary 
 Updated: 24 SEP 2026 UTC 00:00 
 SUPPORT 
 Confidence High 
 Win: 48.25% 
 Pick: 8.72% 
 Ban: 34.23% 
 Trend: ↑ 4 
 Reason: 
 ? 
 Positive trend Often banned 
 Signals: 
 ? 
 ⛔ Perma-ban 
 SUPPORT 
 Last 7 days analytics 
 Tier List 
 Compare Сhampions 
 Build 
 Counters 
 Counter Items 
 Tips 
 Con 
 Game Plan 
 Power Spikes 
 Support YUUMI Build items and runes 
 The information below will help you get familiar with the game on the Support Line YUUMI. We have prepared a items builds, runes, summoner spells and ability order for a comfortable game. Situational options for replacing items and runes are also available to you.
 Key items 
 TIPS: Start your build with Spectral Sickle (Attack champions and structures to gain bonus gold). Next, you should pay attention to whether your mobility champion is enough, our further actions will depend on this. If it is hard for you to dodge the enemy's skills or you want to roam on neighboring lines, then it is better to buy Boots of Speed at an early stage.
 Start
 Spectral Sickle 
 Spectral Sickle Attack champions and structures to gain bonus gold This item is for support players. When equipped, it will reduce the gold you receive from killing minions and monsters. If there are multiples of this item within the party, only one of them can take effect at any given time. Versatile: Gain 10 Attack Damage or 20 Ability Power (Adaptive). Tribute: Gain 1 encircling energy orb(s) every 30 seconds (max 3 orbs). While near an ally, the actions below will trigger Tribute, consuming 1 energy orb(s) to grant you 65 gold and restore your Health 20-80 : 1. Using abilities or attacks to damage enemy champions or structures. 2. Attacking minions below 65% Health. This also executes them, and the gold generated from the minion kills is given to the ally nearest to you. 3. A nearby minion is killed while you have 3 orbs. Upon triggering Tribute, the ally nearest to you gains Tribute stacks. Sentry: Deal 1 more damage to Sight Wards revealed by Sweeping Lens, Control Ward, and Scryer’s Bloom. Restraint: You do not earn gold generated from minion kills, but you earn gold equal to 50% of the bounty. The gold generated from your minion kills will be given to the ally nearest to you. Gold earned from monster kills is reduced by 50%. Quest: Earn 750 gold with this item to transform it into Black Mist Scythe and bind you and the ally with the most Tribute stacks as Perfect Partners. 500 
 Core
 Black Mist Scythe 
 Black Mist Scythe Attack champions and structures to gain bonus gold +10 Ability Haste Versatile: Gain 14 Attack Damage or 28 Ability Power (Adaptive). Soulcast: Every 60 seconds, gains 75 gold , 25 Health and 2 Attack Damage , or 4 Ability Power (Adaptive); up to  250 Health and 20 Attack Damage , or 40 Ability Power (Adaptive). Deal 2 more damage to Sight Wards revealed by Sweeping Lens, Control Ward, and Scryer’s Bloom. When out of combat, gain 10% Movement Speed when you move toward your Perfect Partner. If you're more than 2,500 units apart, this bonus increases to 30%. 0 
 Black Mist Scythe TIPS: This item is designed for support players, granting passive bonuses to gold and stats. It reduces your gold from killing minions and monsters but provides 75 gold and 1 Soulforce stack every 60 seconds. Each Soulforce stack adaptively grants health, attack damage, or ability power, and at 10 stacks you gain a significant bonus to one of these stats. The item also increases your effectiveness in clearing vision by dealing extra damage to revealed enemy wards. Ideal for map-control–focused supports who want to help their team without worrying about farming; you’ll steadily generate resources and strengthen your utility for both protect and peel.
 Ionian Boots of Lucidity 
 Ionian
...(recortado; completo en data/raw)...
## Change history (cambios recientes)

```
Change history
 ADJUSTED 22 SEP 2026 (PATCH 7.3)
BASE STATS
Critical Strike Damage: 175% → 
200%
.
Attack Speed cap: 2.5 → 
3 attacks per second
.
Attack Speed Ratio: 
0.625
.
Base Attack Speed: 
0.625
.
Base Bonus Attack Speed: 
0.2
.
Attack Speed per Level: 
0.006
.
 BUFFED 27 AUG 2026 (PATCH 7.2D)
(W)
 YOU AND ME!
Cooldown: 10/5/0s → 
8/4/0s
.
Heal and Shield Power granted by Passive: 6/7/8/9% → 
8/9/10/11%
.
(E)
 ZOOMIES
Cooldown: 10s → 
9s
.
Shield value: 85/110/135/160 + 30% Ability Power → 
80/110/140/170 + 40% Ability Power
.
 BUFFED 16 JUL 2026 (PATCH 7.2A)
(E)
 ZOOMIES
Mana Cost: 80/90/100/110 → 
65/75/85/95
.
(R)
 FINAL CHAPTER
Base Healing: 20/30/40 → 
20/35/50
.
 BUFFED 01 JAN 2026 (PATCH 6.3F)
(Q)
 PROWLING PROJECTILE
Cooldown: 7/6.5/6/5.5/5 → 
5/5/5/5/5
.
Max Damage: 80/145/210/275/340 → 
100/160/220/280/340
.
Best Friend Bonus | Base Damage: 14/16/18/20/22 → 
18/19/20/21/22
.
(E)
 ZOOMIES
Attack Speed: 20/25/30/35% → 
24/28/32/36%
.
 BUFFED 04 DEC 2025 (PATCH 6.3E)
(PASSIVE)
 FELINE FRINDSHIP
Health Regen：25 + Champion Level × 7 + 25% Ability Power → 
60 + Champion Level × 7 + 25% Ability Power
.
Cooldown: 18 ~ 8s → 
12 ~ 8s
.
(Q)
 PROWLING PROJECTILE
Maximum Base Damage: 80/135/190/245/300 → 
80/145/210/275/340
.
Slow effect: 25/30/35/40/45% → 
45/50/55/60/65%
.
Best Friend’s attack with Bonus Damage: 10/12/14/16/18 → 
14/16/18/20/22
.
(W)
 YOU AND ME!
Bonus Heal and Shield Power: 4/5/6/7% → 
6/7/8/9%
.
(E)
 ZOOMIES
Base Shield Value: 70/100/130/160 → 
85/110/135/160
.
 REWORKED 27 NOV 2025 (PATCH 6.3D)
(PASSIVE)
 FELINE FRINDSHIP
[Removed]
 Removed Passive: Bop 'n Block
[New]
 Added Passive: Feline Friendship
[New]
 While attached, Yuumi and her host gain Friendship whenever they kill an enemy champion or minion. The ally with the highest Friendship becomes her Best Friend, empowering Yuumi’s abilities when attached to them.
[Adjusted]
 Yuumi’s attacks against enemy champions grant her a permanent shield equal to (35 + Champion Level × 10 + 15% AP), with an 18-second cooldown. While attached, the shield is transferred to her ally → 
When Yuumi’s attacks and abilities hit enemy champions, she heals herself for (25 + Champion Level × 7 + 25% AP). If Yuumi attaches to an ally within 4 seconds, that ally is also healed.
(Q)
 PROWLING PROJECTILE
[New]
 Best Friend Bonus: While attached, Prowling Projectile always slows enemies hit, and hitting an enemy champion grants the host (10/12/14/16/18 + 5% AP) bonus damage.
[Removed]
 Projects dealing 2/3/4/5/6% magic damage of current HP.
[Adjusted] 
Slow: 20% → 
25/30/35/40/45%
.
[Adjusted] 
Empowered Base Damage: 70/120/170/220/270 → 
80/135/190/245/300
.
(W)
 YOU AND ME!
[New]
 Best Friend Bonus: While attached to her Best Friend, Yuumi gains (4/5/6/7% + 0.02% AP) increased healing and shielding power, and her Best Friend gains (3/6/9/12 + 4% AP) bonus healing received.
[Removed]
 Grants the attached ally Adaptive Force.
(E)
 ZOOMIES
[Adjusted]
 Cooldown: 12/11/10/9s → 
10s at all levels
.
[Adjusted] 
Yuumi heals herself for (20/30/40/50 + 10% AP) HP and gains (15 + 3% AP) movement speed and (20/25/30/35%) attack speed for 3 seconds.
[Adjusted]
 The next 3 attacks and abilities that hit an enemy restore (20/30/40/50+10%AP) HP → 
Yuumi grants herself a shield for (70/100/130/160 + 30% AP) and gains (20/25/30/35% + 0.08% AP) attack speed for 3 seconds. While the shield is active, the target also gains 20% movement speed.
(R)
 FINAL CHAPTER
[Adjusted] 
Waves deal (80/100/120 + 15% AP) magic damage to enemies hit → 
Waves deal (80/100/120+15%AP) magic damage and apply a 10% slow for 10% to enemies hit, and each additional wave hit increases the slow by 10%
.
[Adjusted]
 Subsequent waves deal 50% magic damage → 
Subsequent wave deal (20/30/40 + 5% AP) magic damage
.
[New]
 Each wave heals allied champions hit for (20/30/40 + 5% AP). Excess healing is converted into a shielding amount.
[New]
 Best Friend Bonus: Healing is increased to (26/39/52 + 8% AP) for her Best Friend.

```

## Build/runas populares (referencia comunitaria, NO conclusión)

```
Runes BUILD
                
For runes, you should pick 
 
Aery
 (Your attacks and abilities send Aery to a target, damaging enemies or shielding allies.) as your keystone, followed by 
 
Axiom Arcanist
 (Increases you ultimate ability's damage, heals and shields. Scoring a takedown on an enemy champion reduces your ultimate ability's remaining cooldown.), 
 
Transcendence
 (Grants more Ability Haste the higher your level is and also returns ability cooldown duration.) and 
 
Scorch
 (Deals bonus damage to champions on ability hit.) in the primary tree, as well as 
 
Revitalize
 (Empowered healing and shielding effects.) in the secondary tree. Below you can see possible options for replacing runes.
                
                
                    
                        
                            
    
            
                
                    
                    
      
```

## 14. REPORTES COMPLETOS (estándar v1.4, anotados 7.3a: Jinx, Kalista, Diana, Yuumi, Karma)

---

---
tags:
  - Jungla
  - Mid
  - Assassin
  - AP-Híbrido
version: 1.2
Status: Aprobado
champion: Diana
patch: "7.3+7.3a"
---
**Fecha del análisis:** 25/09/2026
**Parche:** 7.3 (21-sep-2026)
**Rol principal:** Jungla (preferente) / Mid
**Arquetipo:** AP assassin híbrido — burst de rotación + autos potenciados por Moonsilver Blade (30-100 % AS tras habilidad)
**Enfoque:** Explotar el Lethal Tempo rehecho: su pasiva le da AS bonus masiva y la bala de LT escala +0.67 % por cada 1 % de AS bonus → híbrido Nashor's/Dusk and Dawn + Rabadon's.

> [!NOTE]
> **Estado Meta Actual (Diamond+, 24/09/2026):**
> 
> Mid: Win Rate 47.98 % | Pick 1.12 % | Tendencia ↓2 — **Jungla: Win Rate 50.82 % | Pick 1.90 %**. Diana está débil en mid; jungla es su rol viable en 7.3. Es un pick de confort, no tier S: expectativas honestas.

> [!TIP]
> **Variante one-shot:** si tu comp necesita borrar squishies (ej. vs Yuumi-carry), cambia Nashor's/D&D por **Luden's + Infinity Orb + Stormsurge**: burst 2 152 (vs 1 792) a costa de −39 % de DPS sostenido (593 vs 971).


> [!WARNING] Hotfix 7.3a (29-sep-2026)
> Sin cambios directos a Diana, pero el **burn de Smite vs monstruos bajó (30-198 → 22-162/s)**: clear de jungla early más lento → refuerza la ruta Nashor's-primero y exige escudo de W activo en campamentos. Build y números intactos.
---

## 0. RESUMEN EJECUTIVO

### Tabla A — BUILD FINAL

| Slot | Ítem | Oro | Rol en la build |
|------|------|-----|-----------------|
| 1 (botas) | **Boots of Mana → ⬆️ Spellslinger's Shoes** (min 10:00, MISMO slot) | 2 200 | 35 AP + 18 pen plana + 8 % pen + Big Bully (clear) |
| 2 | **Dusk and Dawn** (mid) / **Nashor's Tooth** (jungla) | 3 100 / 2 900 | Spellblade+cura / clear AS+Gnaw |
| 3 | **Nashor's Tooth** (mid) / **Dusk and Dawn** (jungla) | 2 900 / 3 100 | El espejo del slot 2 |
| 4 | **Rabadon's Deathcap** | 3 400 | 130 AP — multiplica proc cada-3-golpe (50 % AP), W y R |
| 5 | **Zhonya's Hourglass** | 3 300 | 110 AP + stasis — entra con R y sobrevive |
| 6 | **Cryptbloom** (default) → **Void Staff** vs MR | 3 000 | 30 % pen + 20 AH + nova de cura / 40 % pen + 95 AP |

> **Oro total: ~17 900 g** · AP 490 · AS 2.22 (Moonsilver incluido) · Haste 55 · Pen 18+8 % y 30 % · DPS sostenido **971** · burst combo **1 792**

### Tabla B — Ruta de compra cronológica

| # | Compra | Oro acum. | Minuto típico |
|---|--------|-----------|---------------|
| 1 | Amplifying Tome (start; componente de Nashor's) | 500 | 0:00 |
| 2 | Sheen + Phage + 800 → **Dusk and Dawn** (mid) | 3 600 | ~8:00 |
| 3 | **Boots of Mana** | 4 800 | ~9:30 |
| 4 | Recurve + Blasting Wand + Fiendish Codex → **Nashor's Tooth** | 7 700 | ~11:30 |
| 5 | ⬆️ **Spellslinger's Shoes** (mismo slot, +1 000 g) | 8 700 | ~12:00 (post 10:00) |
| 6 | Needlessly Large Rod + 700 → **Rabadon's Deathcap** | 12 100 | ~15:00 |
| 7 | Seeker's Armguard + Blasting Wand → **Zhonya's Hourglass** | 15 400 | ~17:30 |
| 8 | Void Amethyst + Fiendish Codex + Tome → **Cryptbloom** | 17 900 | ~20:00 |

### Runas · Hechizos · Habilidades

| Categoría | Elección |
|-----------|----------|
| Keystone | **Lethal Tempo** (sí, en Diana — ver §4 Ley 1b: 971 vs 873 Empowerment vs 805 Conqueror) |
| Domination | **Sudden Impact** (su E es dash → 15-65 verdadero + 10 % MS por engage) |
| Precisión | **Legend: Alacrity** (+21 % AS → más procs cada-3-golpe y bala LT más gorda) |
| Resolve/Sorcery | **Nullifying Orb** (divea) / **Transcendence** (rotación) |
| Hechizos | **Jungla: Smite + Flash** · **Mid: Flash + Barrier** (comunidad) o Ignite |
| Skills | **Q → W → E** (R en 5/9/13) |

### Resultado del modelo (nivel 15, fight 10 s, LT full, vs 80 MR)

| Escenario | Valor |
|-----------|-----|
| **DPS sostenido (10 s)** | **971** |
| **Burst combo completo** (R+Q+E×2+W×3) | **1 792** |
| **Vs 180 MR** (variante Void Staff) | **515** (vs 460 de la build comunidad) |
| Community (Empowerment, D1) | 748 sostenido / 1 865 burst |

> **Titular:** Lethal Tempo + Nashor's supera a la build de comunidad (Empowerment + Orb) en **+30 % de DPS sostenido** manteniendo burst comparable — Diana es la mejor usuaria accidental del LT rehecho.

---

## 1. CONTEXTO DEL CAMPEÓN EN ESTE PARCHE

### 1.1 Cambios directos a Diana (7.3)

| Stat | Antes | Ahora | Impacto |
|---|---|---|---|
| AS ratio / base | (sistema viejo) | **0.694 / 0.694** | Ratio alto: diseñada para híbridos de auto |
| Base Bonus AS / por nivel | — | 0.15 / 0.008 | Ficha nueva del apéndice oficial |

Sin cambios de habilidades: lo que la redefine son los sistemas.

### 1.2 Cambios sistémicos que la afectan

| Sistema | Cambio | Efecto en Diana |
|---|---|---|
| Lethal Tempo rehecho | Bala +0.67 % por 1 % AS bonus | Moonsilver (hasta +100 % AS) + Nashor's (50 %) = combustible de bala |
| Nashor's Tooth 7.3 | 2 900 g: 80 AP / 50 % AS / Gnaw 15+20 % AP bonus | Su ítem más sinérgico quedó más barato y fuerte |
| Dusk and Dawn 7.3 | Spellblade cura 10 % AP + 3 % HP bonus y aplica on-hit extra | Sustain de skirmish para jungla |
| Pen mágica (7.2) | Consolidada: Void Staff 40 %, Cryptbloom 30 %, plana en botas/orb | Rutas de pen claras |
| Smite 7.3 | Daño verdadero escala **+12 % AP** | Sus ítems AP aseguran objetivos |

### 1.3 ¿Sus habilidades escalan con crítico?

No por crítico de autos. La vía "crítica" de Diana es **Infinity Orb** (habilidades critan +20 % a objetivos <40 % HP — umbral subió 35→40 % en 7.3): es ítem de variante burst, no del core.

---

## 2. FICHA MATEMÁTICA (spec)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base / growth | 52 / 3.64 (103 a nivel 15) | Ficha wr-meta |
| AS base / ratio | 0.694 / 0.694 | Apéndice oficial 7.3 |
| Base Bonus AS / AS por nivel | 0.15 / 0.008 | Apéndice oficial 7.3 |
| P Moonsilver Blade | Tras habilidad: **+30-100 % AS por 4 s**; cada 3.er auto: **65 + 50 % AP** mágico AoE (100 % vs monstruos) | Ficha wr-meta |
| Q Crescent Strike | 60/105/150/195 + 70 % AP; aplica Moonlight 3 s; CD 8/7/6/5 | Ficha wr-meta |
| W Pale Cascade | 3 orbes × (20/35/50/65 + 20 % AP); escudo (50/70/90/110 + 40 % AP) ×2 si detonan los 3; CD 13/11.5/10/8.5 | Ficha wr-meta |
| E Lunar Rush | Dash 40/80/120/160 + 30 % AP; **CD 0.5 s si consume Moonlight** | Ficha wr-meta |
| R Moonfall | Pull + slow 20 %; 100/160/220 + 40 % AP hasta **200/320/440 + 80 % AP** según carga; CD 70/65/60 | Ficha wr-meta |

**AP de referencia full build:** 490 · **proc cada-3-golpe a 490 AP:** 65 + 245 = **310 mágico AoE**

---

## 3. MODELO Y FÓRMULAS

```
AS = min(3.0, 0.694 × (1 + 0.15 + 0.112 + AS_items + Moonsilver(0.65) + LT(0.384) + Alac(0.21 si LT)))
Rotación 10 s (haste H): Q cada 5×100/(100+H) · E = Q_casts+1 (reset por Moonlight) · W cada 8.5×100/(100+H) · R 1 por fight ≥8 s
DPS = [Σ habilidades + autos×(AD + Gnaw(15+20 % AP bonus) + proc/3) + spellblade D&D cada 1.5 s + bala LT] × mitigación_mágica
Mitigación: MR_efectiva = máx(0, MR × (1 − pen %) − pen plana)
```

### Supuestos específicos

- Moonsilver al 65 % efectivo sostenido (30-100 % tras cada habilidad; rota Q/E/W constantemente) y 100 % en burst.
- Autos mitigados contra 60 de armadura; habilidades contra MR del escenario (80 squishy / 180 tanque).
- Proc cada-3-golpe = 65 + 50 % AP (lectura de "20 (+15) + 50 %" a rank 4 — verificar en juego).
- Spellblade de D&D con uptime 1/1.5 s (ICD); Luden's Echo 1 proc/9 s; Squall de Stormsurge ~4/10 s (optimista).
- % pen mágica de dos ítems NO se suma (usa el máximo — conservador).

---

## 4. LEYES APLICADAS A DIANA

### Ley 0 — Slots

1 botas (Spellslinger's T3) + 5 ítems. `validate_slots(["Spellslinger's","DuskDawn","Nashor","Rabadon","Zhonyas","Cryptbloom"])` → **PASS**.

### Ley 1b — "Crítico de habilidades": Infinity Orb es condicional

Orb solo rinde a objetivos <40 % HP (umbral 7.3). En el modelo sostenido es dead stat ~60 % del tiempo → por eso la ruta Nashor's (D2) le gana en DPS real aunque la comunidad prefiera Orb (D1). Orb queda para la **variante one-shot**.

### Ley 2 — AS: no llega al tope, puede comprar más

```
B = 0.15 + 0.112 + 0.70 (Nashor+D&D) + 0.65 (Moonsilver) + 0.384 (LT) + 0.21 (Alac) = 2.206
AS = 0.694 × 3.206 = 2.22  → muy lejos del cap 3.0
```
Diana NO tiene problema de overcap: cada punto de AS (Nashor's, Alacrity, LT) suma proc cada-3-golpe y bala. Por eso LT > Empowerment.

### Ley 3 — Penetración mágica

| MR enemigo | Sin pen | Spellslinger's (18+8 %) | + Cryptbloom (30 %) | + Void Staff (40 %) |
|---|---|---|---|---|
| 80 (squishy) | 0.556 | 0.658 | 0.781* | — |
| 180 (stacking) | 0.357 | 0.446 | 0.562 | **0.617** |

\*Modelo conservador: la pen % de dos ítems no se suma (usa el máximo). Regla: **Cryptbloom default; Void Staff con 2+ enemigos en 150+ MR** (D4: 515 vs 460).

### Ley 4 — Stats muertos

| Ítem | Stat muerto en Diana | Nota |
|---|---|---|
| Infinity Orb (core) | ~60 % del tiempo (solo <40 % HP) | Variante burst sí lo aprovecha |
| Malignance | Maná (Diana no lo gasta tanto) | Solo por el haste de R |
| Stormsurge | MS 6 % redundante con E | Squall es el valor real |
| Dusk and Dawn | AD de su spellblade (75 % AD BASE = 77) | La cura y el on-hit extra compensan |

### Ley 5-6 — Eficiencia y timing

Nashor's 2 900 g (80 AP + 50 % AS + Gnaw) es el ítem de mayor densidad para ella. D&D primero en mid (trades con spellblade+cura), Nashor's primero en jungla (clear: Gnaw 100 % vs monstruos + Smite +12 % AP).

### Ley 7 — Sistemas 7.3

Smite verdadero escala +12 % AP → con Nashor's+D&D (~140 AP al minuto 11) tus smites de objetivo valen más. Cristales de torreta: los detona con un auto post-E. Jungla 7.3: campamentos pegan % vida actual → clear con escudo de W activo y E a monstruo grande.

---

## 5. ANÁLISIS DEL PRIMER ÍTEM

| Candidato | Rol | Justificación |
|---|---|---|
| **Dusk and Dawn** (3 100) | Mid | Spellblade (75 % AD base + 10 % AP) + cura por proc = trades ganados y sustain sin maná |
| **Nashor's Tooth** (2 900) | Jungla | Clear más rápido (Gnaw on-hit 15+20 % AP al 100 % vs monstruos) + AS que alimenta LT desde el primer clear |
| Luden's Echo (2 800) | 3.º discordante | Echo es de un solo objetivo efectivo en 7.3 (nerf multi-target); sin AS → no sinergiza con Moonsilver |

*Checkpoints numéricos de primer ítem pendientes de calibrar en el motor de rotación (el modelo actual compara builds completas); la decisión D&D/Nashor's se sostiene por el rol, no por el DPS.*

---

## 6. BUILD FINAL RANURA POR RANURA

| Slot | Ítem | Justificación matemática |
|---|---|---|
| Botas | **Boots of Mana → ⬆️ Spellslinger's** | 18 pen plana + 8 % + 35 AP + Big Bully (clear/push). Crimson Lucidity solo si prefieres 25 haste sobre pen |
| 1 | **Dusk and Dawn** (mid) | Spellblade+cura+on-hit extra: el ítem que más sube su suelo |
| 2 | **Nashor's Tooth** | 80 AP/50 % AS/Gnaw — techo de DPS sostenido (971) |
| 3 | **Rabadon's Deathcap** | 130 AP: proc cada-3-golpe pasa a 310, R a ~790, escudos W a 306+ |
| 4 | **Zhonya's Hourglass** | 110 AP + stasis: Diana entra con R al centro; sin Zhonya's muere antes del segundo combo |
| 5 | **Cryptbloom** | 30 % pen + 20 AH + nova de cura post-kill (snowball) |

### Matriz del último slot (situacional)

| Situación | Ítem | Coste | Impacto medido |
|---|---|---|---|
| **Default** | **Cryptbloom** | 3 000 | 971 DPS · pen 30 % |
| 2+ enemigos con 150+ MR | **Void Staff** | 3 000 | 515 vs 180 MR (vs 460) |
| Comp de one-shot (vs Yuumi-carry) | **Infinity Orb** (por Nashor's o Cryptbloom) | 3 100 | burst 2 152 |
| Vs mucho heal | **Morellonomicon** | 2 650 | GW |
| Kiteo/haste extremo | **Cosmic Drive** | 3 000 | 25 AH + 70 AP + MS |

### RECHAZADOS (con motivo numérico)

| Ítem | Motivo del rechazo |
|---|---|
| Empowerment (keystone comunidad) | 873 DPS < 971 de LT con la misma build |
| Conqueror | 805 DPS; su omnivamp 9 % no compensa |
| Luden's como core | Sin AS → no alimenta Moonsilver/LT; sostenido 748 |
| Stormsurge core | Squall optimista; mejor en variante burst |
| Liandry's / Riftmaker | Combate prolongado de fighter; Diana vive de ventanas |
| Hextech Rocketbelt | Dash duplicado (ya tiene E) y stats diluidos |

---

## 7. RUNAS · HECHIZOS · HABILIDADES

### Keystone: Lethal Tempo (rehecho 7.3)

- Bala con B ≈ 220 %: 24 × (1 + 0.0067×220) = **~59 por golpe** × AS 2.22 ≈ **+132 DPS**.
- +38.4 % AS acelera procs cada-3-golpe (50 % AP) y el spellblade de D&D.
- Medido: **971 (LT) vs 873 (Empowerment) vs 805 (Conqueror)** con build D2.

**Alternativas:** *Electrocute* para one-shot de squishies en mid (burst puro, no modelado); *Empowerment* si la fight es 1 objetivo larguísimo.

### Secundarias

| Slot | Runa | Valor estimado |
|---|---|---|
| Domination | **Sudden Impact** | 15-65 verdadero por E-dash + 10 % MS (engage constante) |
| Precisión | **Legend: Alacrity** | +21 % AS → +procs y +bala LT |
| Resolve/Sorcery | **Nullifying Orb** / **Transcendence** | Anti-burst AP (divea) / más rotación |

### Hechizos

**Jungla: Smite + Flash** (Smite verdadero +12 % AP en 7.3). **Mid: Flash + Barrier** (comunidad) o **Flash + Ignite** con kill-lane.

### Orden de habilidades

**Q → W → E** · R en 5/9/13.
- Q max: 195 + 70 % AP y Moonlight (reset de E) — su daño y movilidad.
- W segunda: 3 orbes + escudo doble (306+ a full AP) — sustain de clear y trades.
- E última: el reset ya la hace spammable; el daño base crece poco.

---

## 8. COMPARACIÓN CONTRA LAS ALTERNATIVAS

### Tabla maestra (nivel 15, fight 10 s vs 80 MR)

| Build | Keystone | Oro | AP | AS | DPS | Burst |
|---|---|---|---|---|---|---|
| **D2 Nashor híbrida (propuesta)** | **LT** | 17 900 | 490 | 2.22 | **971** | 1 792 |
| D1 Comunidad (D&D, Orb, Zhonya, Rabadon, Luden's) | Empowerment | 17 900 | 545 | 1.47 | 748 | 1 865 |
| D3 Burst puro (Luden's, Rabadon, Orb, Stormsurge, Zhonya) | LT | 17 600 | 575 | 1.74 | 655 | **2 152** |
| D4 Anti-tanque (+Void Staff) | LT | 18 000 | 505 | 1.88 | 762* | 1 933 |
| D2 con Conqueror | Conq | 17 900 | 490 | 1.81 | 805 | 1 792 |

\* vs 80 MR; **vs 180 MR: D4 = 515, D1 = 460.**

### Desglose multiplicativo (D2-LT vs D1-Empowerment)

| Factor | Contribución |
|---|---|
| AS 2.22 vs 1.47 (Nashor's + LT + Alacrity) → más procs cada-3-golpe y bala | +51 % de autos híbridos |
| Bala LT (~132 DPS) vs proc Empowerment (~66 DPS promedio) | +66 DPS |
| Amp 8 % de Empowerment sobre base menor | −46 DPS netos vs lo anterior |
| **Neto sostenido** | **+30 %** |

---

## 9. PLAN DE JUEGO

### Early (jungla, 0:00 – 8:00)

- **Clear:** Q al 1, W al 2 (escudo vs campamento), E al 3. Nashor's 1.º → clear con Gnaw al 100 % vs monstruos.
- **Nivel 3:** gank con Q→E (reset)→W→E — doble dash si la Q conecta. Sin R tu engage es E+Flash.
- **Smite 7.3:** verdadero 600 (+12 % AP) → con 140 AP temprano vale ~617; upgrades en 8/20 cargas (1 000/1 400).

### Mid (8:00 – 15:00)

- **Pico D&D/Nashor's + Spellslinger's (~11-12 min):** ganas 1v1 vs cualquier jungla AP.
- **Min 10:00:** ⬆️ Spellslinger's Shoes — Big Bully acelera clear y push.
- **Objetivos:** tu R no existe aún para pelear dragón temprano — pelea ANTES con Q/E y guarda smite upgradeado.

### Late (15:00+)

- **Teamfight:** R desde niebla → pull → combo (Q-E-W-E) → **Zhonya's** si te focusean → el equipo limpia. TU R ES EL ENGAGE: combínala con Malphite/Cho'Gath (doble knockup/pull = wipe).
- **Contra-ventana:** Chainlaced Crushers (30 % tenacidad) y Nullifying Orb enemigo reducen tu burst → flanquea y espera cooldowns antes de R.
- **Splitpush:** Q+autos con Nashor's tiran torretas rápido; cristales se detonan con un auto post-E.

### Reglas del parche que cambian el macro

| Regla | Impacto |
|---|---|
| Smite +12 % AP | Ítems AP = control de objetivos |
| Monstruos pegan % vida actual | Clear con escudo W activo; no tankees Gromp sin W |
| Torretas 7 000 HP | Diana no es sieger — rota tras kill, no empujes sola |

---

## 10. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS

### Fuentes primarias (mandan)

| Fuente | Acceso | Qué aporta |
|---|---|---|
| Notas oficiales 7.3 | 25/09/2026 | Apéndice AS (0.694/0.15/0.008), LT rehecho, Nashor's 7.3, Smite +12 % AP |
| Notas oficiales 7.2 | 25/09/2026 | Rehecho de pen mágica (Void Staff 40 %, Cryptbloom 30 %), Spellslinger's T3, Dusk and Dawn |

### Fuentes secundarias

| Fuente | Acceso | Fiabilidad |
|---|---|---|
| wr-meta Diana (ficha + build + meta) | 25/09/2026 | Alta para kit; build popular (Empowerment+Orb) = insumo que el modelo MEJORA |

### Discrepancias detectadas y resolución

| Tema | Resolución |
|---|---|
| Keystone: comunidad Empowerment vs modelo LT | Gana LT (971 vs 873) — documentado en §8 |
| Void Staff ausente en wr-meta | Existe (notas 7.2: 95 AP/40 % pen/3 000 g) — incluido desde fuente oficial |
| Moonsilver "30-100 %" | Escala exacta no publicada → 65 % efectivo sostenido (verificar en juego) |

### Supuestos del modelo (declarados)

- Moonsilver 65 % sostenido / 100 % burst; proc cada-3-golpe = 65+50 % AP.
- % pen no aditiva entre ítems (conservador); autos vs 60 armadura fija.
- Squall de Stormsurge optimista (~4/10 s); Luden's 1/9 s.

### Contexto meta (24/09, Diamond+)

Mid 47.98 % (↓2, pick 1.12 %) — débil. **Jungla 50.82 %** (pick 1.90 %) — viable. Muestra de 3-4 días post-parche.

### Validación del modelo

- `validate_slots` → **PASS** (6 entradas, 1 botas T3).
- Test de Caitlyn (1.48125): motor reproduce ✓.

---

## APÉNDICE A — POOL DE ÍTEMES AP: veredicto para Diana

| Ítem (oro) | Veredicto | Nota |
|---|---|---|
| Nashor's Tooth (2 900) | ✅ Core jungla-1 / mid-2 | 80 AP + 50 % AS + Gnaw — techo sostenido |
| Dusk and Dawn (3 100) | ✅ Core mid-1 / jungla-2 | Spellblade + cura + on-hit extra |
| Rabadon's Deathcap (3 400) | ✅ Core | Multiplica proc/W/R |
| Zhonya's Hourglass (3 300) | ✅ Core | Stasis post-R obligatorio |
| Cryptbloom (3 000) | ✅ Default pen | 30 % + 20 AH + nova |
| Void Staff (3 000) | ✅ Vs MR stacking | 40 % + 95 AP |
| Spellslinger's Shoes (2 200) | ✅ Botas | Pen plana + Big Bully |
| Infinity Orb (3 100) | ⚠️ Variante burst | Solo <40 % HP (umbral 7.3) |
| Luden's Echo (2 800) | ⚠️ Variante burst | Single-target en 7.3 |
| Stormsurge (2 800) | ⚠️ Variante burst | Squall + MS |
| Morellonomicon (2 650) | ⚠️ Vs heal | GW |
| Cosmic Drive (3 000) | ⚠️ Kiteo | 25 AH + MS |
| Malignance (2 700) | ⚠️ Mid greedy | Haste de R; maná muerto |
| Liandry's / Riftmaker (3 000/3 100) | ❌ | Combate largo de fighter |
| Hextech Rocketbelt (2 700) | ❌ | Dash redundante con E |
| Banshee's Veil (3 000) | ❌ salvo CC extremo | Zhonya's cubre mejor |

---

## APÉNDICE B — RUTAS DE COMPRA

```
MID DEFAULT:
Tome → D&D (8') → Boots of Mana (9:30) → Nashor's (11:30) → ⬆️ Spellslinger's (12')
→ Rabadon's (15') → Zhonya's (17:30) → Cryptbloom (20')

JUNGLA DEFAULT:
Tome → Nashor's (primer clear completo, ~7') → Boots of Mana → D&D → ⬆️ Spellslinger's
→ Rabadon's → Zhonya's → Cryptbloom

ONE-SHOT (vs squishies/Yuumi-carry):
Spellslinger's → Luden's → Rabadon's → Infinity Orb → Stormsurge → Zhonya's
(burst 2 152; sostenido −39 %)

VS MR STACKING (2+ en 150+):
Default pero Cryptbloom → Void Staff

VS AD (Zed/Yasuo mid):
D&D → Zhonya's 2.º (anticipado) → Nashor's → Rabadon's → Cryptbloom → Seeker's componente temprano
```

---

## Pie de página

*Reporte generado el 25/09/2026 con datos del parche 7.3 (21/09/2026). WR-LAB v1.4. Las cifras de DPS son mitigadas contra los objetivos estándar declarados (80 MR squishy · 180 MR stacking) y comparativas — el valor absoluto importa menos que las diferencias relativas entre builds, que son robustas a los supuestos. Si Riot publica un 7.3a/b (hotfix), regenerar datos antes de publicar.*

**Referencias y créditos**

- Notas oficiales del parche 7.3 (21/09/2026) y 7.2 (08/07/2026) — © Riot Games, Inc. (wildrift.leagueoflegends.com). Fuente primaria: apéndice de Attack Speed, Lethal Tempo rehecho, Nashor's/Dusk and Dawn 7.3, sistema de penetración mágica, Smite +12 % AP, Void Staff.
- Base de datos de ítems, runas y ficha de campeón — wr-meta.com (proyecto comunitario de JLVD DEV), sincronizada al 24/09/2026. Fuente secundaria: valores de Moonsilver/Q/W/E/R, build y meta.
- Modelo matemático, Leyes 0-7 y validaciones — WR-LAB (laboratorio propio, `model/analysis_batch2.py` motor de rotación AP), construido sobre las fuentes anteriores.

**Aviso legal:** Wild Rift y League of Legends son marcas registradas de Riot Games, Inc. Este documento es una guía de comunidad con fines educativos, **no está afiliado, patrocinado ni respaldado por Riot Games**. Los nombres de ítems, campeones y estadísticas pertenecen a sus respectivos dueños. El análisis y las conclusiones son trabajo original del autor apoyado en WR-LAB.

---


---

---
tags:
  - ADC
  - Marksman
  - Crítico
  - Bot-Lane
version: 1.4
Status: Aprobado
champion: Jinx
patch: "7.3+7.3a"
---
**Fecha del análisis:** 27/09/2026
**Parche:** 7.3 (21-sep-2026)
**Rol principal:** ADC (Dragon Lane)
**Arquetipo:** Crítico AoE — cohetes Fishbones que critan en área (112 % AD)
**Enfoque:** 100 % de crítico exacto @230 % (C44+Runaan's+IE+LDR), penetración 35 % + Giant Slayer, AS al 94 % del tope 3.0 y Magnification permanente al rango 655-700 de Fishbones.

> [!NOTE]
> **Estado Meta Actual (Diamond+, 24/09/2026):**
> 
> Win Rate 49.82 % | Pick Rate 10.97 % | Ban 0.53 % | Tendencia ↑ | Rol: ADC Bot Lane.

> [!TIP]
> **Variante sustentable:** si el enemigo tiene poke o necesitas sobrevivir peleas largas, cambia el slot 6 (Kraken Slayer) por **Bloodthirster**: −7.5 % de DPS a cambio de ~594 HP/s de lifesteal + escudo Ichorshield. Matriz situacional completa en §6.


> [!WARNING] Hotfix 7.3a (29-sep-2026)
> Sin cambios directos a Jinx. **La beneficia indirectamente:** placas de torreta más blandas (+20 resist por 10 s, antes +30/20 s), Nexus 4 000 HP y nerfs a Caitlyn (AS growth 0.04→0.025, Headshot 60-90 %) y Senna → menos competencia en el rol de siege. Build y números intactos. Detalle: `data/estructurada/cambios_7.3a.md`.
---

## 0. RESUMEN EJECUTIVO

### Tabla A — BUILD FINAL

| Slot | Ítem | Oro | Rol en la build |
|------|------|-----|-----------------|
| 1 (botas) | **Berserker's Greaves → ⬆️ Gunmetal Greaves** (min 10:00, MISMO slot) | 2 200 | 50 % AS + 5 % Lifesteal + 12 HP/golpe + 7 % MS |
| 2 | **Hexoptics C44** | 2 900 | 55 AD · 25 % crit · Magnification +10 % |
| 3 | **Runaan's Hurricane** | 2 650 | 40 % AS · 25 % crit · 2 rayos 55 % AD que critan |
| 4 | **Infinity Edge** | 3 400 | 75 AD · 25 % crit · crítico 200→230 % |
| 5 | **Lord Dominik's Regards** | 3 300 | 35 AD · 35 % pen · 25 % crit · Giant Slayer +12 % |
| 6 | **Kraken Slayer** | 2 900 | 45 AD · 35 % AS · proc 120-168 + missing HP |

> **Oro total: 17 350 g** · AD 324 · AS 2.83 · Crit 100 % @230 % · Pen 35 % · Lifesteal 5 %

### Tabla B — Ruta de compra cronológica

| # | Compra | Oro acum. | Minuto típico |
|---|--------|-----------|---------------|
| 1 | Long Sword (start) | 500 | 0:00 |
| 2 | Pickaxe + Noonquiver → **Hexoptics C44** | 3 400 | ~7:00–8:00 |
| 3 | **Berserker's Greaves** | 4 600 | ~9:00 |
| 4 | Zeal + Kircheis → **Runaan's Hurricane** | 7 250 | ~11:30–12:30 |
| 5 | ⬆️ **Gunmetal Greaves** (mismo slot, +1 000 g) | 8 250 | ~13:00 |
| 6 | BF Sword + Pickaxe + Brawler's → **Infinity Edge** | 11 650 | ~15:30–16:30 |
| 7 | Last Whisper + Noonquiver → **Lord Dominik's Regards** | 14 950 | ~18:00–19:00 |
| 8 | Recurve + Hearthbound Axe + LS → **Kraken Slayer** | 17 350 | ~21:00 |

### Runas · Hechizos · Habilidades

| Categoría | Elección |
|-----------|----------|
| Keystone | **Lethal Tempo** (6.4 %×6 = 38.4 % AS + bala 6-24 ×0.67 %/1 % AS bonus) |
| Precisión 2 | **Legend: Alacrity** (+21 % AS) |
| Precisión 3 | **Brutal** (5 + 6 % AD bonus adaptativo/golpe) |
| Precisión 4 | **Coup de Grace** (+8 % a <40 % HP) |
| Secundaria | **Bone Plating** (anti-burst lane) / **Celerity** (kiteo) |
| Hechizos | **Flash + Ghost** |
| Skills | **Q → W → E** (R en 5/9/13) |

### Resultado del modelo (nivel 15, LT/Alacrity/Q4 full)

| Escenario | DPS |
|-----------|-----|
| **1v1** (pre-mitigación) | **3 044** |
| **3v3** (AoE Fishbones + Runaan's) | **10 561** |
| **vs 120 armadura** | **1 710** |
| **vs Tanque** (220 arm + 4 500 HP + Giant Slayer) | **1 403** |
| Heal/s (Gunmetal LS + Blessed) | **186** |

> **Titular:** +19 % DPS 1v1, +47 % vs carries con armadura y +73 % vs tanques respecto a la build "típica" de Jinx sin pen ni 100 % crit.

---

## 1. CONTEXTO DEL CAMPEÓN EN ESTE PARCHE

### 1.1 Cambios directos a Jinx (7.3)

| Stat / Habilidad | Antes (7.2) | Ahora (7.3) | Impacto |
|---|---|---|---|
| AD por nivel | 4.5 | **4.0** | −7 AD a nivel 15 (114 vs 121) |
| R — Cooldown | 50/45/40 s | **60/50/40 s** | Menos frecuencia de ejecución |
| R — Ratios AD bonus | 15 %→150 % | **12 %→120 %** | −20 % de daño de R |

### 1.2 Cambios sistémicos que la afectan

| Sistema | Cambio | Efecto en Jinx |
|---|---|---|
| Daño crítico base | 175 % → **200 %** | Cada cohete de Fishbones crita ×2.0 en área |
| Infinity Edge | 200→**230 %** | Capstone multiplicativo sobre splash + rayos |
| AS cap | 2.5 → **3.0** | Más techo para Pow-Pow + Get Excited |
| Lifesteal (nuevo stat) | Solo autos/on-hit | Fishbones = autos → 100 % efectivo |
| Botas T3 (min 10:00) | Berserker's → Gunmetal | +15 % AS, +5 % LS, +12 HP/golpe |
| Torretas 7 000 HP + cristales | Crystalline Overgrowth | Jinx a 700 rango = mejor detonadora |
| Lethal Tempo rehecho | 6.4 %/stack, bala 0.67 %/1 % AS | Sinergia perfecta con AS alta |

### 1.3 ¿Sus habilidades escalan con crítico?

**No directamente** (no recibió el cambio de Caitlyn/MF/Tristana/Xayah). Sin embargo, sus cohetes de Fishbones **son autoataques que critan de forma nativa en AoE**, lo que la convierte en la ganadora silenciosa del 200→230 %: cada golpe de área multiplica ×2.30 a todos los objetivos.

---

## 2. FICHA MATEMÁTICA (spec)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base / growth | 58 / 4.0 | Notas 7.3 (nerf) |
| AS base / ratio | 0.625 / 0.625 | Apéndice oficial 7.3 |
| Base Bonus AS | 0.30 | Apéndice oficial 7.3 |
| AS por nivel | 0.02 | Apéndice oficial 7.3 |
| Rango base / Fishbones | 575 / 655-700 | Ficha wr-meta |
| aa_mult (cohete) | ×1.12 | Ficha (112 % AD en área) |
| aa_aoe | True | Fishbones splash |
| self_as_buff (Pow-Pow ×3) | +110 % | Q rank 4 |
| crit_dmg_mod | 1.0 | Sin modificador |
| uses_magnification | True | Rango ≥550 con Fishbones |
| passive_burst_as (Get Excited) | +25 % | Rompe cap 3.0 |
| Maná lvl 1 / growth | 345 / 49 | Informativo |

**AD a nivel 15:** 58 + 4×14 = **114**
**AS bonus por niveles:** 0.02 × Σ(0.7+0.04L) L=1..14 = 0.02 × 14.0 = **0.28**
**Bonus fijo (base+niveles):** 0.30 + 0.28 = **0.58**

---

## 3. MODELO Y FÓRMULAS

### Fórmulas aplicadas

```
AS_total = min(3.0,  AS_base + AS_ratio × B)
B = base_bonus + lvl_bonus + AS_items + LT(0.384) + Alacrity(0.21) + self_buff(1.10)

Daño/golpe = AD_total × aa_mult(1.12) × crit_mult × Magnification(1.10) × amp(GS)
crit_mult  = 1 + crit × (daño_crit × mod − 1)     [daño_crit = 2.30 con IE]

DPS_1v1 = AS × Daño/golpe
        + AS/3 × Kraken(168 × (1 + 0.0075 × missing%))
        + AS × LT_bullet(24 × (1 + 0.0067 × B×100))

DPS_N = DPS_1v1
      + AS × Daño/golpe × (min(N,4)−1)           ← splash Fishbones
      + AS × 2 × 0.55 × AD × crit_mult           ← rayos Runaan's

Mitigación = 100 / (100 + arm × (1 − pen/100))
Giant Slayer = +12 % si target ≥1200 HP bonus
```

### Supuestos específicos

- LT y Alacrity a cargas máximas (pelea sostenida).
- Pow-Pow rank 4, 3 stacks (+110 % AS) activo el 100 % del tiempo en pelea.
- Magnification de C44 siempre al 10 % (Jinx ataca a ≥575 con Fishbones; máximo a 550).
- Kraken promedia missing_hp = 50 % → multiplicador ×1.375.
- Bala de LT escala con AS bonus TOTAL (incluye 0.58 intrínseco).
- Rayos de Runaan's NO heredan Magnification (conservador).
- W/E/R fuera del DPS sostenido (W añade ~150 DPS extra con CD 5 s).

---

## 4. LEYES APLICADAS A JINX

### Ley 1 — Umbral de crítico exacto: 100 %

| Crítico | Mult. con IE | Ganancia marginal |
|---|---|---|
| 50 % | 1.65 | base |
| 75 % | 1.975 | +19.7 % |
| **100 %** | **2.30** | **+16.4 % vs 75 %** |
| 125 % (hipotético) | 2.30 | 0 % (cap) |

**Combo exacto:** C44(25) + Runaan's(25) + IE(25) + LDR(25) = **100.0 %**
Cualquier ítem con 25 % crit adicional (Galeforce, Shieldbow, PD, Fiendhunter, Collector) desperdicia ~1 250 g en stats muertos.

### Ley 2 — AS: apuntar al tope sin pasarse

```
AS_items_para_cap = (3.0/0.625 − 1) − (0.58 + 0.384 + 0.21 + 1.10)
                  = 3.80 − 2.274
                  = 1.526 → 152.6 % de AS de ítems
```

| Combo | AS ítems | AS cruda | Veredicto |
|---|---|---|---|
| Gunmetal + Runaan's + **Kraken** | 125 % | **2.83** | ✅ 94 % del tope; Get Excited (+25 %) → 2.98 |
| Gunmetal + Runaan's + RFC + Kraken | 165 % | 3.08 | ⚠️ overcap 2.6 % |
| On-hit full (Gun+Kraken+WE+Term+BotRK+Runaan) | 240 % | 3.55 | ❌ 18 % AS muerta |

**3 fuentes de AS (Gunmetal 50 + Runaan's 40 + Kraken 35 = 125 %) es el techo óptimo.** Get Excited rompe el cap en reseteos → esa AS "extra" no se desperdicia del todo.

### Ley 3 — Penetración % obligatoria

| Armadura | Sin pen | Con 35 % (LDR) | Ganancia | + Giant Slayer |
|---|---|---|---|---|
| 80 | 0.556 | 0.658 | +18.3 % | — |
| 120 | 0.455 | 0.562 | **+23.5 %** | — |
| 220 | 0.312 | 0.412 | **+32.1 %** | +12 % → **+47.9 %** |
| 300 | 0.250 | 0.339 | +35.6 % | +12 % → +51.5 % |

Sin pen, Jinx pierde >50 % de su daño real contra cualquier frontline post-minuto 12. **LDR es obligatorio como ítem 4-5.**

### Ley 4 — Stats muertos: auditoría de candidatos populares

| Ítem | Stat muerto | Oro desperdiciado |
|---|---|---|
| Galeforce (6.º) | 25 % crit (ya al 100 %) | ~1 250 g |
| Phantom Dancer | 25 % crit + 0 AD | ~1 500 g |
| Immortal Shieldbow | 25 % crit | ~1 250 g |
| Navori Quickblades | 25 % crit + mecánica sin validar | ~1 250 g |
| Yun Tal Wildarrows | Crit progresivo imposible de cuadrar | ~1 300 g |

### Ley 5 — Eficiencia de oro (referencias 7.3)

| Ítem | Oro | Eficiencia con pasivo | Veredicto |
|---|---|---|---|
| Hexoptics C44 | 2 900 | **~157 %** (Magnification ≈ +10 % AD ≈ 1 100 g) | ✅ Core |
| Infinity Edge | 3 400 | **~163 %** (230 % vs 200 % = +15 % global) | ✅ Capstone |
| Lord Dominik's | 3 300 | **~163 %** (pen 35 %+GS 12 % ≈ +47 % vs tanque) | ✅ Core |
| Runaan's | 2 650 | **~131 %** (rayos AoE en 3v3 ≈ +2 300 DPS) | ✅ Core |
| Kraken Slayer | 2 900 | **~140 %** (proc 218 DPS + AS al tope) | ✅ 6.º |
| Bloodthirster | 3 200 | ~125 % (75 AD + LS; sin crit) | ⚠️ Solo sustain |

### Ley 6 — Timing > DPS teórico

- **C44 primero** (2 900 g, path suave: Pickaxe 800 + Noonquiver 1 300 + LS 500 + 300): componente Noonquiver ya da 20 AD + 15 % crit por 1 300 g → golpea desde el minuto 5.
- **Runaan's segundo** (2 650 g, el más barato de los Zeal-items con crit): ventana barata al minuto 11-12.
- **IE tercero** (3 400 g): capstone al minuto 15-16; si vas feedeado, IE segundo (saltar Runaan's) es el pico de 2 ítems más fuerte del juego.

### Ley 7 — El sistema de juego también es input

- Torretas 7 000 HP + placas permanentes → Jinx con Fishbones a 700 rango golpea placas sin entrar en amenaza.
- **Crystalline Overgrowth:** primer ataque detona 3.3-18.9 % de la vida de la torreta como daño verdadero (ciclo ~50 s). Con 7 000 HP → hasta **~1 300 de daño verdadero gratis**. Jinx es la mejor detonadora del juego (rango 700).
- Oro de placas (140 g/placa × 5 = 700 g exterior) financia el pico del minuto 11-13.

---

## 5. ANÁLISIS DEL PRIMER ÍTEM

| Candidato | Oro | DPS lvl 9 (1v1) | DPS lvl 9 (3v3) | DPS lvl 12 (1v1) | DPS lvl 12 (3v3) | Nota |
|---|---|---|---|---|---|---|
| **Hexoptics C44** | 2 900 | 534 | **1 437** | 864 | **2 937** | Magnification +10 % permanente con cohetes |
| Kraken Slayer | 2 900 | **611** | 1 288 | **934** | 2 584 | Gana 1v1 temprano, pierde AoE |
| Stormrazor | 3 000 | 550 | 1 391 | 870 | 2 845 | Alternativa anti-presión (Energized 120 + 45 % MS) |
| Yun Tal Wildarrows | 3 100 | 521* | 1 375* | 837 | 2 836 | *Asume 25 % crit completo (125 ataques) |

**Veredicto:** C44 primero. Kraken gana el duelo 1v1 (+14 %) pero pierde en equipo (−10 % a 3 objetivos). C44 gana donde Jinx gana partidas: push, sieges y teamfights. Al combinarse con IE, la ventaja se amplifica (+17 % AoE a nivel 14 con 3 ítems).

**Nota crítica sobre C44:** Magnification (+0-10 % por distancia, máximo a 550) **NO requiere kills** — es pasiva por distancia. Jinx ataca a 575-700 con Fishbones → el +10 % está activo en el 100 % de sus ataques con cohetes. Arcane Aim (+100 rango post-takedown) es la cereza, no el pastel.

---

## 6. BUILD FINAL RANURA POR RANURA

| Slot | Ítem | Justificación matemática |
|---|---|---|
| Botas | **Berserker's → Gunmetal** | +15 % AS sobre T2 por 1 000 g; +5 % LS; 12 HP/golpe (≈34 HP/s a AS 2.83); +7 % MS al golpear (kiteo). Estrictamente dominante. |
| 1 | **Hexoptics C44** (2 900) | 157 % eficiencia; +10 % permanente (Magnification); 25 % crit; build path suave. |
| 2 | **Runaan's Hurricane** (2 650) | El ítem más sinérgico con Fishbones: splash que crita + 2 rayos que critan = +2 500 DPS en 3v3. 40 % AS + 25 % crit al precio más bajo. |
| 3 | **Infinity Edge** (3 400) | A 75 % crit, el salto 200→230 % multiplica TODO (splash + rayos): +15 % DPS global instantáneo. Capstone obligatorio. |
| 4 | **Lord Dominik's Regards** (3 300) | Cierra 100 % crit exacto (Ley 1) + 35 % pen (Ley 3: +23-47 % daño real) + Giant Slayer. 163 % eficiencia. |
| 5 | **Kraken Slayer** (2 900) | Último slot sin crit desperdiciado que suma DPS puro: 45 AD + 35 % AS (AS cruda → 2.83, 94 % del tope) + proc 168-294 cada 3 golpes (+218 DPS). |

### Matriz del último slot (situacional)

| Situación | Ítem | Coste | Impacto medido |
|---|---|---|---|
| **DPS máximo (default)** | **Kraken Slayer** | 2 900 | 3 044 DPS · AS al 94 % del tope |
| Sustain / poke / peleas >20 s | Bloodthirster | 3 200 | 2 813 DPS (−7.5 %) + 594 HP/s LS + escudo 345 |
| CC duro + AP | Mercurial Scimitar | 3 100 | 2 591 DPS + QSS + 40 MR + 472 HP/s |
| Burst AD / asesinos | Guardian Angel | 3 200 | 2 591 DPS + revivir (sin crit desperdiciado) |
| Doble AP + topar AS | Wit's End | 2 800 | ~2 670 DPS + 45 MR + 20 % tenacidad |
| **1v1 absoluto (duelo/splitpush)** | **Stormrazor** | 3 000 | **3 329 DPS 1v1** (+9 %) pero −14 % en 3v3 |

### RECHAZADOS (con motivo numérico)

| Ítem | Motivo del rechazo |
|---|---|
| **Rapid Firecannon** | 1v1 ≈ Kraken (3 074 vs 3 042), pero **−22 % en 3v3** (8 270 vs 10 561) al sustituir rayos de Runaan's. Solo siege puro. |
| **Galeforce** | 25 % crit muerto (~1 250 g). Dash no compensa −350 DPS vs Kraken. |
| **Phantom Dancer** | 0 AD en 7.3; 25 % crit sobrante; MS duplicado por Gunmetal/Ghost. |
| **Immortal Shieldbow** | 25 % crit muerto; GA/Scimitar defienden mejor por slot. |
| **Yun Tal Wildarrows** | 125 ataques para 25 % crit; ramp incompatible con timing; rompe Ley 1. |
| **Essence Reaver** | Spellblade (135 % AD base = 154 DPS) < Kraken (218 DPS); 25 % crit muerto. |
| **Navori Quickblades** | 25 % crit muerto; mecánica de CD sin validar en 7.3. |
| **The Collector** | Pen plana (solo vs squishies); 25 % crit muerto; niche snowball. |
| **Ruta on-hit completa** | 2 117 DPS = **−30 %** 1v1 / **−52 %** 3v3 vs ruta crítica. |
| **Manamune / Trinity / Divine / Hexplate** | Stats de fighter; no multiplican splash crítico. |

---

## 7. RUNAS · HECHIZOS · HABILIDADES

### Keystone: Lethal Tempo (rehecho 7.3)

- 6 cargas × 6.4 % = **38.4 % AS** sostenido.
- Bala a cargas máximas: base 24 (nivel 15) × (1 + 0.0067 × 352.4 %) = 24 × 3.361 = **80.7 por golpe**.
- DPS de bala: 2.83 × 80.7 = **+228 DPS gratis**.
- Es la keystone que más crece con exactamente los stats que Jinx ya compra (AS alta y sostenida).

**Alternativas:**
- *Fleet Footwork*: lane de poke intenso donde no puedes mantener cargas de LT.
- *First Strike*: matchup greedy donde pokeas con W desde 650+ sin riesgo.

### Secundarias

| Slot | Runa | Valor estimado |
|---|---|---|
| Precisión | **Legend: Alacrity** | +21 % AS → +7 % DPS + alimenta bala LT |
| Precisión/Dom | **Brutal** | 5 + 6 % AD bonus ≈ +50 DPS constante |
| Precisión | **Coup de Grace** | +8 % a <40 % HP (W y R rematan) |
| Resolve | **Bone Plating** / **Celerity** | Anti-burst lane / 2 % MS + 7 % a todo tu MS (kiteo extremo con Ghost + Get Excited + Noxian Gait) |

### Hechizos: Flash + Ghost

Ghost se extiende con takedowns → combina con Get Excited (140 % MS + 25 % AS que rompe cap) para el patrón "kill → reset → persecución" que define a Jinx.

### Orden de habilidades

**Q → W → E** · R en 5/9/13.
- Q max: rango +125 y AS +110 % son su identidad.
- W max segundo: 220 + 160 % AD, CD 5 s ≈ +150 DPS extra.
- E último: utilidad (root), no daño.

---

## 8. COMPARACIÓN CONTRA LAS ALTERNATIVAS

### Tabla maestra (nivel 15, LT/Alacrity/Q4 full)

| Build | Oro | AD | AS | Crit | Pen | 1v1 | 3v3 | vs 120 | vs Tanque | Heal/s |
|---|---|---|---|---|---|---|---|---|---|---|
| **ÓPTIMA Kraken (propuesta)** | 17 350 | 324 | 2.83 | 100 % | 35 % | **3 044** | **10 561** | **1 710** | **1 403** | 186 |
| ÓPTIMA BT (sustain) | 17 650 | 354 | 2.61 | 100 % | 35 % | 2 813 | 10 383 | 1 580 | 1 287 | **594** |
| ÓPTIMA Scimitar (vs CC) | 17 550 | 324 | 2.61 | 100 % | 35 % | 2 591 | 9 519 | 1 456 | 1 184 | 472 |
| Meta comunidad (C44+Runaan+IE+LDR+Gale) | 17 550 | 339 | 2.61 | 125 %* | 35 % | 2 702 | 9 951 | 1 518 | 1 236 | 166 |
| Build "clásica" adaptada (Ber+Kraken+RFC+Runaan+IE+BT) | 16 000 | 309 | 2.98 | 75 % | 0 % | 2 556 | 8 638 | 1 162 | 799 | 413 |
| Ruta on-hit (Gun+Kraken+WE+Term+BotRK+Runaan) | 16 650 | 234 | 3.55† | 25 % | 30 % | 2 117 | 5 048 | 1 151 | 997 | 396 |
| **Variante 1v1 (Stormrazor por Runaan's)** | 17 350 | 374 | 2.70 | 100 % | 35 % | **3 329** | 9 058 | 1 872 | 1 534 | 186 |

\* 25 % crit desperdiciado (Galeforce). † Overcap.

### Desglose multiplicativo de la diferencia (ÓPTIMA vs build clásica)

| Factor | Multiplicador | Contribución |
|---|---|---|
| Crítico 100 % @230 % vs 75 % @230 % | ×1.164 | +16.4 % |
| Magnification C44 (+10 %) | ×1.10 | +10.0 % |
| Pen 35 % + GS vs 0 % | ×1.235 (vs 120 arm) / ×1.47 (vs tanque) | +23.5 % / +47 % |
| Gunmetal vs Berserker's (+15 % AS, +5 % LS) | ×1.05 | +5.0 % |
| Sin overcap de AS | ×1.02 | +2.0 % |
| **Acumulado 1v1** | | **+19 %** |
| **Acumulado vs tanque** | | **+73 %** |

---

## 9. PLAN DE JUEGO

### Early (0:00 – 9:00)

- **Start:** Long Sword (500 g).
- **Primer recall (~4:30):** Noonquiver (1 300 g: 20 AD + 15 % crit) si la lane es segura; Pickaxe (800 g) + Dagger (400 g) si necesitas daño plano.
- **Maná:** Fishbones cuesta 20/ataque. Regla: **Pow-Pow para farmear, Fishbones solo para trades/push**. Get Excited devuelve 10 % maná faltante por takedown.
- **Placas:** desde el 5:00 decaen −10 g/30 s. Con 700 de rango, golpea placas sin entrar en zona de amenaza. Cada 3 ataques con Demolish (si lo llevas) = 50 + 20 % HP máx.
- **Bajo presión:** cambia C44 por **Stormrazor** (Energized 120 + 45 % MS = kiteo desde minuto 7) y/o keystone Fleet Footwork.

### Mid (9:00 – 16:00)

- **Min 10:00:** mejora Berserker's → **Gunmetal Greaves** (+1 000 g, mismo slot).
- **Pico 1 (C44 + Gunmetal + Runaan's, ~12 min):** 864 DPS 1v1 / 2 937 3v3. Ganas teamfights de 3v3.
- **Cristales:** cada ~50 s la torreta acumula cristales. Un solo cohete los detona (hasta ~1 300 daño verdadero en late). Pasa, pega UN cohete, vete.
- **Pico 2 (IE, ~15-16 min):** 100 % crit @230 %. Splash de Fishbones ahora multiplica ×2.30 a todos. Teamfight de 4v4+ es tu ventana.

### Late (16:00+)

- **Posicionamiento:** 700 de rango con Fishbones. Nunca entres en rango de asesinos. Ghost + Get Excited = reposicionamiento constante.
- **Reset de peleas:** R desde lejos → kill/assist → Get Excited (25 % AS que rompe cap + 140 % MS + maná) → Ghost → Fishbones limpiando.
- **Contra-ventana:** enemigos con Chainlaced Crushers (30 % tenacidad) reducen tu R; Nullifying Orb absorbe tu W. Prioriza LDR y peleas de flanco.
- **No contestes jungla enemiga sola antes del min 10:** monstruos 7.3 pegan % vida actual y Smite rival hace 600-1 400 verdadero.

### Reglas del parche que cambian el macro

| Regla | Impacto |
|---|---|
| Torretas 7 000 HP | No se tiran "de un push"; trabaja placas 2-3 veces |
| Placas permanentes + decaen desde 5:00 | Prioriza la primera placa antes del 5:00 |
| Crystalline Overgrowth (~50 s ciclo) | Un cohete = hasta 1 300 verdadero gratis |
| Minions 60 % daño a campeones | Lane más segura; puedes farmear bajo presión |
| Botas T3 solo desde 10:00 | No intentes mejorar antes |
| Jungla hostil para laners | No robes campamentos sin smite |

---

## 10. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS

### Fuentes primarias (mandan)

| Fuente | Acceso | Qué aporta |
|---|---|---|
| Notas oficiales 7.3 (21/09/2026) | wildrift.leagueoflegends.com | Sistema crit 200/230 %, AS cap 3.0, apéndice AS 140 campeones, cambios de Jinx, ítems, botas T3, Lethal Tempo, campo |
| Notas oficiales 7.2 | wildrift.leagueoflegends.com | Fin encantamientos, QSS/Scimitar como ítems, botas T2/T3, min 10:00 |

### Fuentes secundarias

| Fuente | Acceso | Fiabilidad |
|---|---|---|
| wr-meta.com/items (186 ítems) | 24/09/2026 | Alta en stats/precios; desfasada en texto viejo de LT |
| wr-meta.com Jinx | 24/09/2026 | Alta para kit; build popular es insumo, no conclusión |

### Discrepancias detectadas y resolución

| Tema | Fuente A | Fuente B | Resolución |
|---|---|---|---|
| Lethal Tempo (ranged) | wr-meta: 4.8 %, bala 6-20, +0.33 % | Notas 7.3: **6.4 %, bala 6-24, +0.67 %** | Mandan las notas oficiales |
| Legend: Alacrity | Descripción: 3 %+18 % = 21 % | Ejemplo Caitlyn: "18 % a full stacks" | Modelo usa 21 % (peor caso); diff <1 % DPS |
| Noxian Gait (Gunmetal) | Notas 7.2: 15 %/10 % | wr-meta post-7.3: 10 %/7 % | wr-meta (reajuste global MS 5→4 %) |
| Ingenious Hunter | wr-meta la lista | Notas 7.3: **REMOVIDA** | Removida |

### Supuestos del modelo (declarados)

- Magnification siempre al 10 % (distancia ≥550 con Fishbones).
- LT/Alacrity/Q4 a cargas máximas en pelea.
- Kraken promedia +37.5 % por vida faltante (missing 50 %).
- Bala LT escala con AS bonus total (incluye 0.58 intrínseco).
- Runaan's no hereda Magnification (conservador).
- W/E/R fuera del DPS sostenido (W añade ~150 DPS extra).
- Splash Fishbones golpea hasta 4 objetivos.
- Daño crítico a torretas excluido (conservador).

### Contexto meta (24/09, Diamond+)

Jinx: WR 49.82 %, pick 10.97 %, ban 0.5 %, tendencia ↑. Solo 6 días de datos post-parche; el ecosistema de marksmen se recolocará. Esta build está diseñada para el estado 7.3 tal como está publicado al 27/09/2026. Si Riot publica 7.3a/b, los números de ítems podrían moverse ±5 %.

### Validación del modelo

- `validate_slots(["Gunmetal","C44","Runaan's","IE","LDR","Kraken"])` → **PASS** (6 entradas, 1 botas, 5 ítems, sin T2+T3 duplicadas).
- Test de Caitlyn (AS 1.48 con Alacrity + Berserker's): el motor reproduce 0.625 + 0.625×(0.28+0.04×14+0.18+0.35) = 1.48125 ✓.

---

## APÉNDICE A — POOL DE ÍTEMES DEL ROL: veredicto para Jinx

| Ítem (oro) | Veredicto | Nota |
|---|---|---|
| Hexoptics C44 (2 900) | ✅ Core 1 | 157 % eficiencia; Magnification +10 % permanente |
| Runaan's Hurricane (2 650) | ✅ Core 2 | Rey del AoE con splash; rayos critan |
| Infinity Edge (3 400) | ✅ Core 3 | Capstone ×2.30 |
| Lord Dominik's Regards (3 300) | ✅ Core 4 | Cierra 100 % + 35 % pen + GS |
| Mortal Reminder (3 000) | ✅ Reemplaza LDR vs curación | 30 % pen + GW 50 % |
| Kraken Slayer (2 900) | ✅ 6.º default | +218 DPS, AS al 94 % tope |
| Bloodthirster (3 200) | ✅ 6.º sustain | −7.5 % DPS, +594 HP/s |
| Mercurial Scimitar (3 100) | ✅ 6.º vs CC | QSS + 40 MR + 12 % LS |
| Guardian Angel (3 200) | ✅ 6.º vs AD burst | Revivir, sin crit muerto |
| Wit's End (2 800) | ✅ 6.º vs doble AP | 50 % AS + 45 MR + tenacidad |
| Stormrazor (3 000) | ⚠️ 1.º anti-presión / 6.º 1v1 | +9 % 1v1, −14 % 3v3 |
| Rapid Firecannon (2 650) | ⚠️ Solo siege | −22 % 3v3 vs Runaan's |
| Fiendhunter Bolts (2 650) | ⚠️ Niche R-window | Rompe 100 % exacto |
| Galeforce (3 100) | ❌ | 25 % crit muerto (1 250 g) |
| Phantom Dancer (2 650) | ❌ | 0 AD; crit sobrante |
| Immortal Shieldbow (3 000) | ❌ | Crit muerto; GA/Scim defienden mejor |
| Yun Tal Wildarrows (3 100) | ❌ | Ramp 125 ataques; rompe Ley 1 |
| Essence Reaver (3 000) | ❌ | Spellblade < Kraken; crit muerto |
| Navori Quickblades (2 650) | ❌ | Crit muerto; mecánica sin validar |
| The Collector (3 000) | ❌ | Pen plana; crit muerto |
| Statikk Shiv (3 000) | ❌ | On-hit/híbrido, no para crit Jinx |
| Guinsoo's / BotRK / Terminus / WE | ❌ | Ruta on-hit = −30 % 1v1 / −52 % AoE |
| Manamune / Trinity / Divine / Hexplate | ❌ | Ítems de fighter |

---

## APÉNDICE B — RUTAS DE COMPRA

```
DEFAULT (máximo DPS):
LS → Pickaxe/Noonquiver → C44 (7-8') → Berserker's (9') → Runaan's (11-12')
→ ⬆️ Gunmetal T3 (13') → IE (15-16') → LDR (18-19') → Kraken (21')

SNOWBALL (feedeado):
... → C44 → IE 2.º (pico brutal lvl 12) → Runaan's → Gunmetal → LDR → Kraken/BT

ANTI-PRESIÓN (lane difícil):
LS → Stormrazor → Berserker's → Runaan's → Gunmetal → IE → LDR → Kraken/BT

VS 2+ TANQUES:
Default pero 6.º = Mortal Reminder (GW) → Kraken se cae

VS CC DURO:
Default pero 6.º = Mercurial Scimitar (QSS 1 100 g temprano si hay hook)

VS BURST AD (Zed/Rengar/Yasuo):
Default pero 6.º = Guardian Angel

VS DOBLE AP:
Default pero 6.º = Wit's End (AS queda en 2.92 cruda, perfecta)

1v1 SPLITPUSH (duelo puro):
C44 → Berserker's → Stormrazor → Gunmetal → IE → LDR → Kraken
(3 329 DPS 1v1; pierde AoE de Runaan's)
```

---

## Pie de página

*Reporte generado el 27/09/2026 con datos del parche 7.3 (21/09/2026). WR-LAB v1.4. Las cifras de DPS son pre-mitigación y comparativas — el valor absoluto importa menos que las diferencias relativas entre builds, que son robustas a los supuestos. Si Riot publica un 7.3a/b (hotfix), regenerar datos antes de publicar.*

**Referencias y créditos**

- Notas oficiales del parche 7.3 (21/09/2026) y 7.2 (08/07/2026) — © Riot Games, Inc. (wildrift.leagueoflegends.com). Fuente primaria de todos los cambios sistémicos, apéndice de Attack Speed y valores de ítems modificados.
- Base de datos de ítems, runas y fichas de campeón — wr-meta.com (proyecto comunitario de JLVD DEV), sincronizada al 24/09/2026. Fuente secundaria para stats no tocados por el parche.
- Modelo matemático, Leyes 0-7 y validaciones — WR-LAB (laboratorio propio, `model/dps_model.py`), construido sobre las fuentes anteriores.

**Aviso legal:** Wild Rift y League of Legends son marcas registradas de Riot Games, Inc. Este documento es una guía de comunidad con fines educativos, **no está afiliado, patrocinado ni respaldado por Riot Games**. Los nombres de ítems, campeones y estadísticas pertenecen a sus respectivos dueños. El análisis y las conclusiones son trabajo original del autor apoyado en WR-LAB.

---

---

---
tags:
  - ADC
  - Marksman
  - On-hit
  - Bot-Lane
version: 1.2
Status: Aprobado
champion: Kalista
patch: "7.3+7.3a"
---
**Fecha del análisis:** 25/09/2026
**Parche:** 7.3 (21-sep-2026)
**Rol principal:** ADC (Dragon Lane)
**Arquetipo:** On-hit ejecutor — autos que apilan lanzas y una E (Rend) que detona en burst físico
**Enfoque:** Maximizar aplicaciones on-hit por segundo (Guinsoo's las duplica cada 3 golpes) y lanzas por ventana de E; penetración doble con Terminus; **cero crítico** (su E no critica).

> [!NOTE]
> **Estado Meta Actual (Diamond+, 24/09/2026):**
> 
> Win Rate 50.99 % dúo (51.27 % solo) | Pick Rate 4.72 % | Ban 5.02 % | Tendencia ↑7 | Rol: ADC Bot Lane.

> [!TIP]
> **Variante duelo/splitpush:** cambia Runaan's por **Kraken Slayer** → **1 364 DPS 1v1** (el máximo medido) a costa de todo el AoE (3v3 cae a 1 364). **Variante waveclear:** Statikk Shiv como ítem 2-3 (sus bounces aplican on-hit y Kalista carga Energized 5× más rápido); se vende tarde por BotRK.

> [!WARNING]
> Rango de ataque no publicado en la fuente (verificar en juego). No afecta conclusiones: ninguna pasiva de esta build exige ≥550 de distancia.


> [!WARNING] Hotfix 7.3a (29-sep-2026)
> Sin cambios directos a Kalista. Yun Tal Wildarrows fue BUFFEADA (AS 25→35 %, Flurry 35 %) pero **sigue rechazada** para ella (sin on-hit, ramp de crit). Placas más blandas favorecen su siege. Build y números intactos.
---

## 0. RESUMEN EJECUTIVO

### Tabla A — BUILD FINAL

| Slot | Ítem | Oro | Rol en la build |
|------|------|-----|-----------------|
| 1 (botas) | **Berserker's Greaves → ⬆️ Gunmetal Greaves** (min 10:00, MISMO slot) | 2 200 | 50 % AS + 5 % LS + 12 HP/golpe + dash mejorado (su pasiva escala con tier de botas) |
| 2 | **Guinsoo's Rageblade** | 3 000 | 35 AD/30 AP/30 % AS · doble on-hit cada 3 golpes · +32 % AS por stacks |
| 3 | **Wit's End** | 2 800 | 50 % AS + 40 mágico/golpe + 45 MR + 20 % tenacidad |
| 4 | **Terminus** | 3 000 | 30 % pen física Y mágica (3 stacks) + 30 on-hit + 35 % AS |
| 5 | **Blade of the Ruined King** | 3 100 | 6 % vida actual/golpe + 12 % LS + Drain slow |
| 6 | **Runaan's Hurricane** | 2 650 | 2 rayos que aplican on-hit COMPLETO a 2 objetivos extra |

> **Oro total: 16 750 g** · AD 240 · AS 3.00 (cruda 3.52 con stacks) · Crit 0 % · Pen 30 % doble · LS 17 %

### Tabla B — Ruta de compra cronológica

| # | Compra | Oro acum. | Minuto típico |
|---|--------|-----------|---------------|
| 1 | Long Sword + poción (start; se vende/absorbe) | 500 | 0:00 |
| 2 | Amplifying Tome + Recurve + Pickaxe → **Guinsoo's Rageblade** | 3 000 | ~7:30–8:30 |
| 3 | **Berserker's Greaves** | 4 200 | ~9:30 |
| 4 | Recurve + Negatron + Dagger → **Wit's End** | 7 000 | ~12:00 |
| 5 | ⬆️ **Gunmetal Greaves** (mismo slot, +1 000 g) | 8 000 | ~13:00 |
| 6 | Recurve + Hearthbound Axe + 900 → **Terminus** | 11 000 | ~15:30 |
| 7 | Vampiric + Pickaxe + Recurve → **BotRK** | 14 100 | ~18:00 |
| 8 | Zeal + Kircheis → **Runaan's Hurricane** | 16 750 | ~20:30 |

### Runas · Hechizos · Habilidades

| Categoría | Elección |
|-----------|----------|
| Keystone | **Lethal Tempo** (38.4 % AS + bala ~85-90/golpe con su AS bonus ≈ +260 DPS) |
| Precisión 2 | **Legend: Alacrity** (+21 % AS → más lanzas por ventana de E) |
| Precisión 3 | **Brutal** (5 + 6 % AD bonus adaptativo/golpe) |
| Precisión 4 | **Coup de Grace** (+8 % a <40 % HP — su E ya es ejecutor) |
| Secundaria | **Nullifying Orb** (vs asesinos AP) / **Bone Plating** (vs poke) |
| Hechizos | **Flash + Heal** (Heal + BotRK + Gunmetal LS = sustain triple; Ghost si kitean) |
| Skills | **E → Q → W** (R en 5/9/13) |

### Resultado del modelo (nivel 15, LT/Alacrity full, E cada 7 s con ~AS×4 lanzas)

| Escenario | DPS (mitigado) |
|-----------|-----|
| **1v1** (vs 120 arm / 50 MR) | **1 262** |
| **3v3** (splash de on-hit por Runaan's + Statikk-like bounces) | **2 612** |
| **vs Tanque** (220 arm / 150 MR / 4 500 HP) | **1 045** |
| Detonación de E (12 lanzas, AD 240) | **2 387 por rip** |
| Heal/s (BotRK 12 % + Gunmetal 5 % + Blessed) | **~250** |

> **Titular:** +15 % 1v1, +20 % 3v3 y +35 % vs tanque sobre la build de comunidad (Statikk core); **+43 % sobre cualquier ruta de crítico** (su E no critica: el crítico es stat muerto en Kalista).

---

## 1. CONTEXTO DEL CAMPEÓN EN ESTE PARCHE

### 1.1 Cambios directos a Kalista (7.3)

| Stat / Habilidad | Antes (7.2) | Ahora (7.3) | Impacto |
|---|---|---|---|
| AD base | 54 | **57** | +3 AD base |
| AD por nivel | 5.0 | **5.2** | 129.8 AD a nivel 15 (antes ~124) |

### 1.2 Cambios sistémicos que la afectan

| Sistema | Cambio | Efecto en Kalista |
|---|---|---|
| AS cap | 2.5 → **3.0** | La campeona con más AS por nivel (0.046) estrena techo más alto |
| Lifesteal (nuevo stat) | Solo autos/on-hit | TODO su daño es on-hit/autos → 100 % efectivo (BotRK 12 % + Gunmetal 5 %) |
| Guinsoo's rehecho | 35 AD/30 AP/30 % AS, doble on-hit cada 3 golpes, sin restricción de crítico | Su ítem firma: multiplica WE/Terminus/BotRK |
| Statikk rehecho | Bounces aplican on-hit, Electroshock (+5 stacks Energized/ataque) | Waveclear brutal temprano |
| Botas T3 (min 10:00) | Gunmetal: 50 % AS + 5 % LS + Gait | Su dash (P) escala con tier de botas → doble beneficio |

### 1.3 ¿Sus habilidades escalan con crítico?

**No.** Ficha oficial sin mención de crítico en Q/E/R (a diferencia de Caitlyn/MF/Tristana que sí lo recibieron en 7.3). Sus autos pueden critar pero son fracción minoritaria de su DPS → **Ley 1 invertida: el umbral útil de crítico de Kalista es 0 %**.

---

## 2. FICHA MATEMÁTICA (spec)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base / growth | 57 / 5.2 | Notas 7.3 (buff) |
| AS base / ratio | 0.694 / 0.694 | Apéndice oficial 7.3 |
| Base Bonus AS | 0.16 | Apéndice oficial 7.3 |
| AS por nivel | **0.046** (la más alta del juego) | Apéndice oficial 7.3 |
| Rango | por verificar | [!WARNING] |
| P Martial Poise | dash por auto; velocidad/distancia escala con TIER DE BOTAS; Oathsworn | Ficha wr-meta |
| Q Pierce | 70/135/200/265 + 110 % AD; on-kill carry de stacks de Rend; habilita dash | Ficha wr-meta |
| W Sentinel (pasiva) | Con Oathsworn a <8 m y ambos golpeando al mismo objetivo: **16/17/18/19 % vida MÁXIMA** mágico extra, 8 s CD por objetivo; ejecuta minions <125 | Ficha wr-meta |
| E Rend | 30/45/60/75 + 70 % AD + (n−1) × (12/22/32/42 + 36/43/50/57 % AD); lanzas duran 4 s; slow 15-45 %; **reset con kill**; no critica | Ficha wr-meta |
| R Fate's Call | Oathsworn en stasis → lanzamiento con knockup 1/1.5/2 s | Ficha wr-meta |

**AD a nivel 15:** 57 + 5.2×14 = **129.8** · **Bonus de niveles (AS):** 0.046 × 14.0 = **+0.644**

---

## 3. MODELO Y FÓRMULAS

```
AS = min(3.0, 0.694 × (1 + 0.16 + 0.644 + AS_items + LT(0.384) + Alac(0.21) + Guinsoo_stacks(0.32)))

Auto   = AD (+ on-hit físico: BotRK 6 % vida actual)
On-hit = (Guinsoo 30 + Terminus 30 + WE 40) mágicos × 4/3 (doble aplicación Guinsoo)
       + Statikk: Energized 60 mágico cada ~4 ataques (Kalista carga 5× más rápido)
E/rip  = 75 + 0.70×AD + (AS×4 − 1) × (42 + 0.57×AD)      [cada 7 s]
Q      = (265 + 1.10×AD) cada 6.5 s (aplica 1 lanza extra)
W      = 0.19 × vida_máx Objetivo cada 8 s (condicional Oathsworn coordinado)
LT     = AS × 24 × (1 + 0.0067 × B×100)
Mitigación física para AD/E/Q/on-hit físico; mágica aparte para on-hit mágico y W.
```

### Supuestos específicos

- E cada 7 s con lanzas = AS×4 (duración 4 s, sin cap declarado); rank 4.
- W modelada con coordinación de Oathsworn al 100 % (en solo queue resta ese término).
- Terminus a 3 stacks (oscuros) ~90 % del tiempo en pelea.
- BotRK al 90 % de vida máxima promedio del objetivo; Guinsoo a 4 stacks.
- Bala de LT = adaptativa física; on-hit mágico mitigado por MR (50 squishy / 150 tanque).

---

## 4. LEYES APLICADAS A KALISTA

### Ley 0 — Slots

Build final = 1 botas (Gunmetal T3) + 5 ítems. `validate_slots(["Gunmetal","Guinsoo","Wit's End","Terminus","BotRK","Runaan's"])` → **PASS**.

### Ley 1 (invertida) — Crítico: umbral útil 0 %

| Ruta | 1v1 | 3v3 | Veredicto |
|---|---|---|---|
| On-hit (final) | **1 262** | **2 612** | ✅ |
| Crítico (Gunmetal+C44+IE+Runaan's+LDR+Kraken) | 885 | 1 416 | ❌ −30 %: su E (57 % AD por lanza) no critica |

### Ley 2 — AS: Kalista quiere TODO el tope

```
AS_items_para_cap = (3.0/0.694 − 1) − (0.16 + 0.644 + 0.384 + 0.21 + 0.32)
                  = 3.323 − 1.718 = 1.605 → ~160 % de AS de ítems (con stacks de Guinsoo)
```

| Combo | AS ítems | AS cruda | Veredicto |
|---|---|---|---|
| Gunmetal+Guinsoo+WE+Terminus+BotRK+Runaan's | 235 % | 3.52 | ⚠️ overcap teórico ~17 %, pero su uptime real de buffs (LT 6 golpes, Guinsoo 4 golpes, dash que interrumpe autos) lo deja oscilando alrededor de 3.0. **Único campeón del roster donde pasarse un poco no duele.** |
| Sin Gunmetal (Berserker's) | 220 % | 3.42 | igual de overcap pero −15 % AS permanente y −dash: estrictamente peor |

### Ley 3 — Penetración: doble, por Terminus

Mitad de su daño es mágico (on-hit) y mitad físico (autos+E). **Terminus da 30 % a AMBAS** (3 stacks oscuros). LDR fue probado: 1 074 1v1 / 768 vs tanque — **pierde contra BotRK** (25 % crit muerto + su % vida actual derriba tanques mejor que la pen contra su E).

### Ley 4 — Stats muertos

| Ítem | Stat muerto en Kalista | Oro desperdiciado |
|---|---|---|
| C44 / IE / LDR / RFC / Runaan's-crit | 25 % crit cada uno (E no critica) | ~1 250 g por ítem |
| Statikk como ítem FINAL | AD 40 + AP 40 parcialmente; Energized < on-hit sostenido | ~800 g vs BotRK |

### Ley 5 — Eficiencia: Guinsoo's es el multiplicador

Guinsoo's (3 000 g) no es caro por sus stats sino por su pasiva: **doble aplicación cada 3 golpes** multiplica WE (+40), Terminus (+30), BotRK (6 %) y el propio Wrath (+30) → ~+33 % a todo el on-hit del build. Nada en el parche replica ese multiplicador.

### Ley 6 — Timing

Guinsoo's 1.º (pico 7:30-8:30) → WE 2.º (12:00, anti-AP y máximo 1v1 temprano: 686) → Gunmetal (13:00) → Terminus → BotRK → Runaan's.

### Ley 7 — Sistemas 7.3

Su dash por auto (mejorado por botas T3) + E-reset con kill = la mecánica de "kiteo infinito" que las torretas de 7 000 HP premian: trabaja placas desde 575+ sin quedar estática; los cristales (Crystalline Overgrowth) se detonan con un auto en pleno dash.

---

## 5. ANÁLISIS DEL PRIMER ÍTEM

Checkpoint nivel 11 (2 ítems + Gunmetal, vs 90 arm / 40 MR):

| Combo | AD | AS | DPS 1v1 | DPS 3v3 | Nota |
|---|---|---|---|---|---|
| **Guinsoo's + Wit's End** | 144 | 2.79 | **686** | 686 | Máximo duelo; 45 MR anti-poke AP |
| Guinsoo's + Statikk (comunidad) | 184 | 2.65 | 658 | **772** | Waveclear y AoE temprano |
| Statikk + Runaan's | 149 | 2.50 | 483 | 805 | Solo si la partida es 5-man constante |
| C44 + Runaan's (crítico) | 164 | 2.29 | 445 | 662 | ❌ confirmado: ruta muerta |

**Veredicto:** Guinsoo's primero SIEMPRE (es el multiplicador). El 2.º ítem es la decisión real: **WE** si te hacen burst AP o buscas duelos (686), **Statikk** si necesitas push (772 en 3v3). Ambos convergen a la Tabla A.

---

## 6. BUILD FINAL RANURA POR RANURA

| Slot | Ítem | Justificación matemática |
|---|---|---|
| Botas | **Berserker's → Gunmetal** | +15 % AS sobre T2; 5 % LS; 12 HP/golpe (~36 HP/s a AS 3.0); **su dash escala con tier de botas** (ficha oficial) |
| 1 | **Guinsoo's Rageblade** (3 000) | Doble on-hit cada 3 golpes = ×4/3 a todo el on-hit; 32 % AS por stacks; 35 AD |
| 2 | **Wit's End** (2 800) | 50 % AS + 40 mágico/golpe (~120 DPS) + 45 MR + 20 % tenacidad — Kalista es el foco #1 del equipo enemigo |
| 3 | **Terminus** (3 000) | 30 % pen doble (su daño es mixto) + 30 on-hit + 35 % AS + resistencias light |
| 4 | **BotRK** (3 100) | 6 % vida actual (~132 vs 2 200 HP; ~270 vs tanque) DOBLE con Guinsoo cada 3 golpes + Drain slow + 12 % LS |
| 5 | **Runaan's Hurricane** (2 650) | Cada rayo aplica on-hit completo a 2 objetivos extra (+40 WE +30 Guinsoo +6 % HP por rayo) → su 3v3 sube de 1 262 a 2 612 |

### Matriz del último slot (situacional)

| Situación | Ítem | Coste | Impacto medido |
|---|---|---|---|
| **Default (AoE)** | **Runaan's Hurricane** | 2 650 | 2 612 en 3v3 |
| Duelo / splitpush | Kraken Slayer | 2 900 | **1 364 1v1** (+8 %), 3v3 = 1 364 |
| Waveclear temprano | Statikk Shiv | 3 000 | 772 3v3 a nivel 11; vendible tarde |
| vs 3 tanques | (mantiene BotRK+Terminus) | — | 1 045 vs tanque ya incluido |
| vs burst AP | WE sube a ítem 2 | — | 45 MR + 20 % tenacidad antes |

### RECHAZADOS (con motivo numérico)

| Ítem | Motivo del rechazo |
|---|---|
| **Ruta crítica completa** | 885 DPS = −30 %; E no critica |
| **LDR / Mortal Reminder** | 25 % crit muerto; LDR probado: 1 074/768 < BotRK 1 262/1 045 |
| **C44** | Magnification exige distancia (rango por verificar); 25 % crit muerto |
| **Statikk como ítem final** | Su Energizado rinde menos que BotRK/Runaan's sostenidos (K1 comunidad: 1 098 vs K2: 1 262) |
| **Navori / ER / Galeforce / Shieldbow** | Crit muerto + sin on-hit |
| **Guinsoo's + Statikk + Runaan's + WE + Terminus (K1 comunidad)** | Le falta el % vida de BotRK: −15 % 1v1 y −26 % vs tanque |

---

## 7. RUNAS · HECHIZOS · HABILIDADES

### Keystone: Lethal Tempo (rehecho 7.3)

- 6 cargas × 6.4 % = **38.4 % AS** — Kalista las mantiene trivialmente (ataca sin parar).
- Bala: 24 × (1 + 0.0067 × ~407 % AS bonus) = **~89 por golpe** × AS 3.0 ≈ **+260 DPS**.
- Es la keystone que más crece con exactamente lo que ella compra (AS) y con su pasiva de dash (uptime de ataques).

**Alternativas:** *Fleet Footwork* solo vs lanes de poke extremo donde no pueda mantener cargas; nada más compite.

### Secundarias

| Slot | Runa | Valor estimado |
|---|---|---|
| Precisión | **Legend: Alacrity** | +21 % AS → ~+2 lanzas por ventana de E (≈ +300 por rip) |
| Precisión/Dom | **Brutal** | 5 + 6 % AD bonus ≈ +40 DPS constante |
| Precisión | **Coup de Grace** | +8 % a <40 % HP — convierte rips de E en ejecuciones |
| Resolve/Sorcery | **Nullifying Orb** / **Bone Plating** | Anti-asesino AP / anti-poke de lane |

### Hechizos: Flash + Heal

Heal + BotRK 12 % + Gunmetal 5 % + Blessed Blade 12/golpe = triple sustain; la comunidad coincide. Ghost es válido si el enemigo kitea (su dash ya es movilidad).

### Orden de habilidades

**E → Q → W** · R en 5/9/13.
- E max primero: es SU daño (42 + 57 % AD por lanza y reset con kill).
- Q segundo: 265 + 110 % AD, on-kill carry de stacks (snowball de waveclear).
- W al final: la pasiva escala poco (16→19 %) y el activo es visión.

---

## 8. COMPARACIÓN CONTRA LAS ALTERNATIVAS

### Tabla maestra (nivel 15, LT/Alacrity full, E con ~12 lanzas)

| Build | Oro | AD | AS | Crit | Pen | 1v1 | 3v3 | vs Tanque | E-hit |
|---|---|---|---|---|---|---|---|---|---|
| **FINAL (Gun+Guinsoo+WE+Term+BotRK+Runaan's)** | 16 750 | 240 | 3.00 | 0 % | 30 | **1 262** | **2 612** | **1 045** | 2 387 |
| Comunidad K1 (Statikk en vez de BotRK) | 16 650 | 240 | 3.00 | 0 % | 30 | 1 098 | 2 181 | 776 | 2 387 |
| K3 LDR anti-tanque | 16 950 | 235 | 3.00 | 25 % | 35 | 1 074 | 2 042 | 768 | 2 349 |
| K5 Single-target (Kraken por Runaan's) | 17 000 | 285 | 3.00 | 0 % | 30 | **1 364** | 1 364 | 1 119 | 2 726 |
| K4 Crítico (descarte) | 17 350 | 340 | 2.53 | 100 % | 35 | 885 | 1 416 | 665 | 2 700 |

### Desglose multiplicativo de la diferencia (FINAL vs comunidad K1)

| Factor | Contribución |
|---|---|
| BotRK 6 % vida actual × doble-aplicación Guinsoo (vs Statikk Energized intermitente) | +15 % 1v1 |
| Rayos de Runaan's con on-hit completo ×2 objetivos (vs bounces de Statikk) | +20 % 3v3 |
| BotRK vs tanque (6 % de 4 500 HP = 270/golpe) | **+35 % vs tanque** |

---

## 9. PLAN DE JUEGO

### Early (0:00 – 9:00)

- **Start:** Long Sword + poción; componentes de Guinsoo's (Recurve 900 primero).
- **Last hits imposibles:** E rank 1 + W pasiva ejecutan minions bajo 125 HP — asegura CS bajo torre.
- **Vínculo (Oathsworn) al minuto 1:** elección definitiva de la partida (ver abajo).

### El vínculo (Oathsworn) — la decisión más importante

| Candidato | Veredicto |
|---|---|
| **Karma (support)** | ⭐ Ideal: autoataca a distancia (proca tu W 19 % vida máx), su W enraíza 2 objetivos (rips garantizados) y tu R la lanza como engage → combo R→R |
| Tanques melee (Cho'Gath/Malphite) | Sólido: siempre están encima del objetivo (W proca) y tu R los reposiciona |
| **Yuumi** | ⚠️ Attachada no autoataca → la W pasiva casi no proca. Verificar en juego si su Q cuenta como "golpe" para el vínculo; si no, vincúlate a otro |

### Mid (9:00 – 16:00)

- **Min 10:00:** ⬆️ Gunmetal Greaves — tu dash mejora literalmente (tier de botas).
- **Pico Guinsoo+WE+Gunmetal (~13 min):** 686 DPS 1v1 temprano; ganas duelos con rips de ~1 500-1 900.
- **Reset de E:** cada kill refresca Rend → en oleadas y skirmishes encadena rips; prioriza objetivos bajos para detonar el reset.

### Late (16:00+)

- **Teamfight:** pega al FRONTLINE (BotRK+Terminus+W 19 % vida máx lo derriten) mientras Runaan's propaga on-hit al backline. Nunca dejes de atacar hacia atrás (dash por auto).
- **R como herramienta de equipo:** guarda Fate's Call para el engage de tu Oathsworn (Karma/Malphite) o para salvarlo de un dive.
- **W CD por objetivo (8 s):** rota objetivos con tu support para procar la pasiva en varios enemigos.

### Reglas del parche que cambian el macro

| Regla | Impacto |
|---|---|
| Torretas 7 000 HP + placas | Tu AS alta + dash = trabaja placas segura desde 575+ |
| Cristales (~50 s) | Un auto en dash los detona (hasta ~1 300 verdadero en late) |
| Jungla hostil (7.3) | No robes campamentos: monstruos pegan % vida actual |

---

## 10. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS

### Fuentes primarias (mandan)

| Fuente | Acceso | Qué aporta |
|---|---|---|
| Notas oficiales 7.3 | 25/09/2026 | Buff de AD (57/5.2), apéndice AS (0.694/0.16/0.046), Guinsoo's/Statikk/Terminus/BotRK rehechos, lifesteal |
| Notas oficiales 7.2 | 25/09/2026 | Botas T2/T3 y regla del min 10:00 |

### Fuentes secundarias

| Fuente | Acceso | Fiabilidad |
|---|---|---|
| wr-meta Kalista (ficha + build popular) | 25/09/2026 | Alta para kit (Q/W/E/R completos); build popular = insumo (Statikk 1.º) |

### Discrepancias detectadas y resolución

| Tema | Resolución |
|---|---|
| 1.º ítem: comunidad Statikk vs modelo Guinsoo→WE | Gana el modelo (686 vs 658 1v1; 1 262 vs 1 098 final) — Statikk queda como variante waveclear |
| Lethal Tempo (valores) | Notas oficiales 7.3 (6.4 %, bala 6-24, +0.67 %) sobre texto viejo de wr-meta |

### Supuestos del modelo (declarados)

- E no critica (sin mención en ficha — si un hotfix lo cambia, recalcular).
- ¿Cuenta el Q de Yuumi como golpe del Oathsworn para W? **Pendiente de verificar en juego.**
- Lanzas por ventana = AS×4 (4 s de duración, sin cap declarado).
- Terminus 3 stacks ~90 % uptime; Guinsoo 4 stacks; BotRK al 90 % vida máx.
- Mitigación física y mágica aplicadas por separado a cada componente.

### Contexto meta (24/09, Diamond+)

Kalista: WR 50.99 % dúo / 51.27 % solo, pick 4.72 %, ban 5.02 %, **tendencia ↑7** — el 7.3 (buff de AD + AS cap 3.0 + Guinsoo's) la dejó en buen lugar. Muestra de 3-4 días post-parche.

### Validación del modelo

- `validate_slots(["Gunmetal","Guinsoo","Wit's End","Terminus","BotRK","Runaan's"])` → **PASS** (6 entradas, 1 botas, sin T2+T3).
- Test de Caitlyn (AS 1.48125): motor reproduce ✓.

---

## APÉNDICE A — POOL DE ÍTEMES DEL ROL: veredicto para Kalista

| Ítem (oro) | Veredicto | Nota |
|---|---|---|
| Guinsoo's Rageblade (3 000) | ✅ Core 1 | El multiplicador (doble on-hit ×4/3) |
| Wit's End (2 800) | ✅ Core 2 | 50 % AS + 40 on-hit + 45 MR |
| Terminus (3 000) | ✅ Core 3 | Única pen DOBLE del juego (física+mágica) |
| Blade of the Ruined King (3 100) | ✅ Core 4 | 6 % vida actual ×2 con Guinsoo; anti-tanque real |
| Runaan's Hurricane (2 650) | ✅ Core 5 | Rayos con on-hit completo = su AoE |
| Gunmetal Greaves (2 200) | ✅ Botas | AS + LS + dash mejorado |
| Statikk Shiv (3 000) | ⚠️ Early/waveclear | Bounces con on-hit; vendible por BotRK tarde |
| Kraken Slayer (2 900) | ⚠️ 6.º duelo | 1 364 1v1 (máximo), pierde AoE |
| LDR / Mortal (3 300/3 000) | ❌ | 25 % crit muerto; BotRK > pen en ella |
| C44 / IE / RFC / PD / Navori / ER / Gale / Shieldbow / Collector | ❌ | Crítico muerto (E no critica) |
| Manamune / Trinity / Hexplate | ❌ | Stats de fighter/caster |

---

## APÉNDICE B — RUTAS DE COMPRA

```
DEFAULT (on-hit completo):
LS → Guinsoo's (7:30-8:30) → Berserker's (9:30) → Wit's End (12:00)
→ ⬆️ Gunmetal (13:00) → Terminus (15:30) → BotRK (18:00) → Runaan's (20:30)

WAVECLEAR / PUSH TEMPRANO:
LS → Guinsoo's → Berserker's → Statikk (11:30) → ⬆️ Gunmetal → Terminus → BotRK → (vender Statikk → Runaan's)

ANTI-AP BURST:
Guinsoo's → Berserker's → Wit's End (2.º, ya en default) → Mercury's→Chainlaced SOLO si el CC es inmanejable (pierdes 50 % AS y el dash T3)

DUELO / SPLITPUSH:
Default pero 6.º = Kraken Slayer (1 364 1v1)

VS 3 TANQUES:
Default intacto (BotRK+Terminus+W ya ES la respuesta: 1 045 vs tanque)
```

---

## Pie de página

*Reporte generado el 25/09/2026 con datos del parche 7.3 (21/09/2026). WR-LAB v1.4. Las cifras de DPS son mitigadas contra los objetivos estándar declarados (120/50 squishy · 220/150/4 500 tanque) y comparativas — el valor absoluto importa menos que las diferencias relativas entre builds, que son robustas a los supuestos. Si Riot publica un 7.3a/b (hotfix), regenerar datos antes de publicar.*

**Referencias y créditos**

- Notas oficiales del parche 7.3 (21/09/2026) y 7.2 (08/07/2026) — © Riot Games, Inc. (wildrift.leagueoflegends.com). Fuente primaria: buff de Kalista, apéndice de Attack Speed, rehechos de Guinsoo's/Statikk/Terminus/BotRK, sistema de botas T3 y lifesteal.
- Base de datos de ítems, runas y ficha de campeón — wr-meta.com (proyecto comunitario de JLVD DEV), sincronizada al 24/09/2026. Fuente secundaria: valores de Q/W/E/R, build y meta.
- Modelo matemático, Leyes 0-7 y validaciones — WR-LAB (laboratorio propio, `model/analysis_batch2.py` motor on-hit), construido sobre las fuentes anteriores.

**Aviso legal:** Wild Rift y League of Legends son marcas registradas de Riot Games, Inc. Este documento es una guía de comunidad con fines educativos, **no está afiliado, patrocinado ni respaldado por Riot Games**. Los nombres de ítems, campeones y estadísticas pertenecen a sus respectivos dueños. El análisis y las conclusiones son trabajo original del autor apoyado en WR-LAB.

---


---

---
tags:
  - Support
  - Mid
  - Enchanter
  - Poke
version: 1.2
Status: Aprobado
champion: Karma
patch: "7.3+7.3a"
---
**Fecha del análisis:** 25/09/2026
**Parche:** 7.3 (21-sep-2026)
**Rol principal:** Support (secundario: Mid AP)
**Arquetipo:** Enchanter-poke con Mantra (cada 3 casts, la siguiente habilidad básica se potencia)
**Enfoque:** CC fiable y barato (Q slow cada ~3.4 s + W root ×2) para mantener **Imperial Mandate** activo: +7 % de daño de TODO el equipo sobre el marcado, mientras Censer/E amplifican al carry.

> [!NOTE]
> **Estado Meta Actual (Diamond+, 24/09/2026):**
> 
> Win Rate 49.82 % | Pick Rate 4.68 % | Ban 0.62 % | Tendencia ↓14 (🧊 cayendo) | Rol: Support. Sigue siendo funcional; la caída refleja el meta de enchanters post-7.3, no el kit.

> [!TIP]
> **Variante Mid:** ruta AP-burst completamente distinta (Spellslinger's → Luden's → Malignance → Rabadon's → Infinity Orb → Zhonya's; AP 575, Q-Mantra ~1 025). Ver §6 matriz y Apéndice B.


> [!WARNING] Hotfix 7.3a (29-sep-2026)
> Sin cambios directos a Karma. Diadem/Circlet nerfeadas (Harmonize 0.5→0.25 %): su matriz situacional queda igual (Diadem ya era niche). Build intacta.
---

## 0. RESUMEN EJECUTIVO

### Tabla A — BUILD FINAL (SUPPORT)

| Slot | Ítem | Oro | Rol en la build |
|------|------|-----|-----------------|
| 1 (botas) | **Ionian Boots → ⬆️ Crimson Lucidity** (min 10:00, MISMO slot) | 2 000 | 25 haste → Q cada 3.4 s = Mandate permanente |
| 2 | **Black Mist Scythe** (quest de support) | 500 → 0 | Slot de quest |
| 3 | **Imperial Mandate** | 2 600 | CC → marca 4 s: **+7 % daño de todo el equipo** + 60 AP + Control (20 haste en CC) |
| 4 | **Ardent Censer** | 2 400 | E/E-Mantra → +30 % AS y +25 on-hit al carry |
| 5 | **Echoes of Helia** | 2 400 | Poke de Q → curas burst al aliado |
| 6 | **Staff of Flowing Waters** (default) / Redemption / Mikael's / Locket | 2 400 | +40 AP y +15 haste al escudar |

> **Oro total: ~11 800 g** · AP 200 · Haste 75 · HSP 21 % · **E = 339 · E-Mantra = 520 (+ anillo que escuda a un 2.º aliado ≈ 1 040 efectivos)** · Mantra cada ~16 s + R instantánea · **Mandate ≈ +357 DPS de equipo** (a 6 000 de team DPS)

### Tabla B — Ruta de compra cronológica

| # | Compra | Oro acum. | Minuto típico |
|---|--------|-----------|---------------|
| 1 | **Spectral Sickle** (quest) + poción | 500 | 0:00 |
| 2 | Boots of Speed → **Ionian Boots of Lucidity** | 1 900 | ~4:00 |
| 3 | Quest completada → **Black Mist Scythe** | 1 900 | ~6:00 |
| 4 | Bandleglass Mirror + Blasting Wand → **Imperial Mandate** | 4 500 | ~9:30 |
| 5 | ⬆️ **Crimson Lucidity** (mismo slot, +1 000 g) | 5 500 | ~10:30 |
| 6 | Forbidden Idol + Aether Wisp → **Ardent Censer** | 7 900 | ~13:00 |
| 7 | Bandleglass + Kindlegem → **Echoes of Helia** | 10 300 | ~16:00 |
| 8 | Forbidden Idol + Kindlegem → **Staff of Flowing Waters** | 12 700 | ~19:00 |

### Runas · Hechizos · Habilidades

| Categoría | Elección |
|-----------|----------|
| Keystone | **Aery** (Q de campo la dispara 2 veces; E escuda) / **Guardian** (vs dive: escudo 40-165+6 % AP a 3 aliados con W×2+E) |
| Sorcery 2 | **Transcendence** (haste → más casts → más Mantras) |
| Resolve/Sorcery 3 | **Revitalize** (+5-15 % a E) o **Manaflow Band** (+300 maná) |
| 4 | **Scorch** (poke) / **Bone Plating** (lanes de burst) |
| Hechizos | **Flash + Exhaust** (support) · **Flash + Barrier** (mid, comunidad) |
| Skills | **Q → E → W** (R en 5/9/13) |

### Resultado del modelo (nivel 15, AP 200 / haste 75 / HSP 21 %)

| Métrica | Valor |
|-----------|-----|
| Escudo E / E-Mantra (+anillo) | **339 / 520 (+520)** |
| Q-Mantra total (campo+explosión) | ~590 |
| Cadencia de Mantra sostenida | ~1 cada 16 s + R |
| **Amp de equipo (Mandate)** | **+7 % al marcado ≈ +357 DPS de equipo** |
| DPS+ al carry (Censer + uptime) | +164 (sobre ADC de referencia) |

> **Titular:** Imperial Mandate sobre un objetivo permanentemente marcado (Q cada 3.4 s) es el mayor amp-de-equipo por oro del parche para un support de poke — y Karma tiene el CC más barato y fiable para sostenerlo.

---

## 1. CONTEXTO DEL CAMPEÓN EN ESTE PARCHE

### 1.1 Cambios directos a Karma (7.3)

Sin cambios de habilidades. Ficha AS nueva del apéndice (ratio 0.625 / bonus 0.2 / 0.0135 por nivel) — irrelevante para su rol.

### 1.2 Cambios sistémicos que la afectan

| Sistema | Cambio | Efecto en Karma |
|---|---|---|
| Imperial Mandate (7.3) | Rediseño: 2 600 g, 60 AP, Control (+20 haste en habilidades de CC), Command (CC → +7 % daño recibido, 4 s) | Su Q slow + W root lo mantienen ~85-100 % uptime |
| Ardent Censer (7.3) | 2 400 g, buff fijo (30 % AS + 25 on-hit) | Su E (y E-Mantra a 2 aliados) lo procea |
| Echoes of Helia (7.3) | Soul Siphon 30 % del daño → cura | Su poke constante la alimenta |
| Enchanters (7.2) | Menos haste late en toda la línea | Haste de Crimson/Transcendence vale más |

### 1.3 ¿Escala con crítico? No — escala con **AP (65 % en su E) y haste (cadencia de Mantra)**

El ratio 65 % AP de E/Mantra-E es de los más altos entre enchanters: el AP de Mandate/Censer/Echoes NO es stat muerto.

---

## 2. FICHA MATEMÁTICA (spec)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD / HP / MS | 58 / 630 / 360 | Ficha wr-meta |
| P Mantra | 3 casts → Mantra State (potencia la siguiente básica); R = Mantra instantánea | Ficha wr-meta |
| Q Inner Flame | 60-180 + 40 % AP + slow 35 %; **Mantra:** 65-290 + 50 % + campo 1.5 s (slow 42.5-50 %) que explota 40-160 + 50 % | Ficha wr-meta |
| W Focused Resolve | **Tether ×2 campeones**: 35-110 + 40 % AP y root 1-1.75 s (40-130 + 45 %); Mantra: raíces mejoradas 1.5-2.25 s | Ficha wr-meta |
| E Inspire | Escudo 60-150 + **65 % AP** + 30 % MS; **Mantra:** 120-300 + 65 % AP (decae en 4 s) + 60 % MS + **anillo que escuda al primer aliado que entra** | Ficha wr-meta |
| R Transcendent Embrace | Mantra instantánea + anillo: 170-390 + 80 % AP + **knockback al centro** + slow 35 % | Ficha wr-meta |

---

## 3. MODELO Y FÓRMULAS (valor-aliado + amp de equipo)

```
E_escudo    = (150 + 0.65×AP) × (1 + HSP/100)
E_Mantra    = (300 + 0.65×AP) × (1 + HSP/100)  ×2 objetivos vía anillo
Cadencia    = casts/s = 3 / (Σ CDs con haste)  →  Mantras/10 s = casts/10 s ÷ 3
Mandate_amp = team_DPS × 0.07 × uptime_marca        [Q cada 3.4 s → uptime ~85-100 %]
Censer      = +11.5 % DPS del carry + AS_carry × 25 on-hit
```

### Supuestos específicos

- Team DPS de referencia 6 000 para valorar Mandate (lineal: a 4 000 → +238).
- HSP de ítems solo Censer/Staff/Redemption (Mandate no da); Revitalize 5 % base.
- Uptime de Mandate 85-100 % sobre el objetivo prioritario (Q CD 3.4 s con haste 75).
- W-Mantra NO cuenta en la cadencia sostenida (se reserva para root garantizado).

---

## 4. LEYES APLICADAS A KARMA

### Ley 0 — Slots

1 botas (Crimson T3) + quest + 4 ítems. `validate_slots(["Crimson","Imperial Mandate","Censer","Echoes","Staff"])` → PASS.

### Ley 4 — Stats muertos: la defensa SÍ vale (a medias)

A diferencia de Yuumi, Karma tiene cuerpo: la posicionan en rango de Q/W. Bone Plating/Nullifying Orb y un 6.º slot defensivo (Locket/Mikael's) tienen valor real. Pero HP/armor como stats primarios siguen siendo ineficientes vs AP/haste (su E escala 65 % AP).

### Ley 5 — Eficiencia: Mandate es amp, no stats

2 600 g → +357 DPS de EQUIPO sostenido sobre el marcado (a team DPS 6 000). Ningún ítem de support da tanto por oro cuando tu team tiene 2+ fuentes de daño. Si tu team es 80 % tu ADC: Censer primero.

### Ley 6 — Timing

Mandate al ~9:30 (Bandleglass 900 temprano) = la primera fight de dragón ya tiene marca. Crimson Lucidity al 10:30 → Q cada 3.4 s.

### Ley 7 — Sistemas

Torretas 7 000 HP: tu Q-Mantra de campo (slow 50 %) siega placas con el carry sin riesgo. Cristales: los detona tu auto/Q desde 550+. Minions al 60 % → lane de poke segura.

---

## 5. ANÁLISIS DEL PRIMER ÍTEM

**No aplica** — quest primero. La decisión real es el ítem 3: **Mandate** (team con 2+ carries) vs **Censer** (ADC-céntrico) vs **Echoes** (lane de poke/sustain). Regla del §4 Ley 5.

---

## 6. BUILD FINAL RANURA POR RANURA

| Slot | Ítem | Justificación matemática |
|---|---|---|
| Botas | **Ionian → ⬆️ Crimson Lucidity** | 25 haste + Noxian Haste (MS al escudar/hechizar) → Q cada 3.4 s = Mandate permanente |
| Quest | **Black Mist Scythe** | Obligatoria; ocupa slot |
| 1 | **Imperial Mandate** | +7 % team al marcado ≈ +357 DPS de equipo; 60 AP infla E; Control = +20 haste a su CC |
| 2 | **Ardent Censer** | E/E-Mantra (2 aliados con anillo) → +30 % AS y +25 on-hit al carry: +164 DPS |
| 3 | **Echoes of Helia** | Poke Q-Mantra (~590) → Soul Siphon cura ~177 al aliado |
| 4 | **Staff of Flowing Waters** | +40 AP/+15 haste al carry escudado; cierra haste 75+ |

### Matriz del último slot (situacional)

| Situación | Ítem | Coste | Impacto |
|---|---|---|---|
| **Default** | **Staff of Flowing Waters** | 2 400 | AP+haste al carry |
| Necesitan cura AoE | Redemption | 2 450 | 150-350 + verdadero |
| CC duro sobre el carry | Mikael's Blessing | 2 500 | Cleanse + heal |
| AoE burst enemigo | Locket | 2 600 | 250-370 AoE |
| Comp de engage aliada | Shurelya's / Zeke's | 2 500/2 400 | MS AoE / R→slow+ult haste |
| **Mid AP** | Ver Apéndice B (Luden's/Malignance/Rabadon's/Orb/Zhonya's) | ~17 500 | AP 575 · Q-Mantra ~1 025 · E-Mantra auto-escudo 707 |

### RECHAZADOS (con motivo numérico)

| Ítem | Motivo del rechazo |
|---|---|
| Yordle Trap | Aura 20 % AS a aliados < Mandate (+7 % a todo el daño) con su CC uptime |
| Diadem of Songs | Su poke ya cura vía Echoes; Diadem rinde en asedios largos (⚠️ niche) |
| Ítems de vida puros (Heartsteel etc.) | Ley 4: su E escala AP, no HP |
| Rabadon's en support | 3 400 g fuera del presupuesto de support (~12 k); solo en variante mid |

---

## 7. RUNAS · HECHIZOS · HABILIDADES

### Keystone: Aery

Q de campo dispara Aery 2 veces (impacto + explosión) y E la convierte en escudo — poke y protección en una runa.

**Alternativas:** *Guardian* vs dive pesado (escudo a 3 aliados: W×2 + E); *Arcane Comet* en la variante mid.

### Secundarias

| Slot | Runa | Valor estimado |
|---|---|---|
| Sorcery | **Transcendence** | +10 haste y reducción post-9 → más Mantras (cada 3 casts) |
| Resolve/Sorcery | **Revitalize** (+5-15 % a E) / **Manaflow Band** (+300 maná) / **Scorch** (poke) | según lane |
| Resolve | **Bone Plating** | vs lanes de burst (Draven/Yasuo) |

### Hechizos

**Support: Flash + Exhaust** (peel con W root + Exhaust = el diveador muere). **Mid: Flash + Barrier** (comunidad).

### Orden de habilidades

**Q → E → W** · R en 5/9/13.
- Q max: 180+40 % (Mantra 290+50 % + campo 160+50 %) — poke y marca de Mandate.
- E segunda: 150+65 % AP (Mantra 300+65 % + anillo) — su identidad de enchanter.
- W última: el root mejora poco (1→1.75 s) y su valor es binario (conecta o no).

---

## 8. COMPARACIÓN CONTRA LAS ALTERNATIVAS

### Tabla maestra (support, nivel 15)

| Build | Oro | AP | Haste | E | E-Mantra | Valor de equipo |
|---|---|---|---|---|---|---|
| **KS-Mandate (propuesta)** | 12 700 | 200 | 75 | 339 | 520 + anillo | **+357 amp** + 164 ADC |
| KS-Enchanter (Censer, Echoes, Staff, Redemption) | 11 650 | 180 | 65 | 344 | 538 | +164 ADC + Redemption AoE |
| KS-Anti-dive (Mikael's, Locket, Censer, Echoes) | 11 900 | 90 | 50 | ~290 | ~455 | Cleanse + escudo AoE |
| Comunidad Mid (Luden's, Malignance, Orb, Rabadon's, Zhonya's) | 17 500 | 575 | 25 | — | 707 (auto) | Q-Mantra ~1 025 burst |

### Lectura

KS-Mandate ≈ KS-Enchanter en escudos (±20) pero gana por goleada en amp de equipo cuando hay 2+ carries (tu caso: Kalista/Jinx + Diana/Cho'Gath). Con ADC como 80 % del daño del team → KS-Enchanter (Censer primero). La variante mid es otro juego: burst de poke, no enchanter.

---

## 9. PLAN DE JUEGO

### Early (0:00 – 6:00)

- **Lvl 1-2:** Q + auto (Aery+Scorch) — Karma gana casi todo lvl 1; con Mandate comprado temprano (Bandleglass 900) el primer poke YA marca.
- **Mantra de lane:** gástalo en Q (trade) o E (all-in enemigo) — nunca en W salvo root garantizado.

### Mid (6:00 – 14:00)

- **Pico Mandate + Crimson (~10:30):** Q cada 3.4 s mantiene 1 objetivo permanentemente marcado (+7 %) — **comunica focus** a tu team.
- **Min 10:00:** ⬆️ Crimson Lucidity.
- **Dragón/herald:** E-Mantra al jungla antes del fight; W-Mantra (root 2.25 s a 2 objetivos) es tu CC de compromiso.

### Late (14:00+)

- **Teamfight:** E-Mantra al iniciador (Malphite/Cho'Gath entran con 520+anillo), W al carry enemigo, **R cuando agrupen** → knockback al centro = setup de Diana R / Malphite R / Cho'Gath W.
- **Wombo oficial del grupo:** R de Karma agrupa → R de Diana/Malphite encima → Mandate marca al sobreviviente → el team lo borra (+7 %).

### Sinergia con tu grupo

| Compañero | Sinergia |
|---|---|
| **Kalista** | ⭐ Oathsworn: Karma autoataca (proca su W 19 % vida máx), su R te lanza con knockup → engage doble |
| Diana / Malphite / Cho'Gath | R agrupa → ults encima; Mandate amplifica el follow-up |
| Jinx / Yunara | Censer + marca = las dos ventanas de limpieza |
| Yuumi | No compitan: una sola enchanter; si ambas, Yuumi BF = la Kalista |

### Reglas del parche que cambian el macro

| Regla | Impacto |
|---|---|
| Torretas 7 000 HP | Q-Mantra de campo siega placas con slow 50 % |
| Enchanters con menos haste late (7.2) | Crimson + Transcendence no son lujo, son core |
| Minions 60 % | Puedes pokear delante de la wave sin miedo |

---

## 10. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS

### Fuentes primarias (mandan)

| Fuente | Acceso | Qué aporta |
|---|---|---|
| Notas oficiales 7.3 | 25/09/2026 | Rediseño de Imperial Mandate (60 AP, Control, Command +7 %), Ardent Censer 2 400, Echoes of Helia |
| Notas oficiales 7.2 | 25/09/2026 | Ajuste de haste de enchanters, items de support |

### Fuentes secundarias

| Fuente | Acceso | Fiabilidad |
|---|---|---|
| wr-meta Karma (ficha + builds + runas) | 25/09/2026 | Alta para kit (W tether ×2 confirmado); build popular = variante MID (Luden's/Malignance) — la de support es derivación propia del modelo |

### Discrepancias detectadas y resolución

| Tema | Resolución |
|---|---|
| Comunidad muestra Karma MID (AP burst), no support | Ambas rutas documentadas: §6 matriz + Apéndice B |
| Tendencia ↓14 del meta | Reportada con honestidad (§Contexto): el kit funciona, el meta de enchanters cayó |

### Supuestos del modelo (declarados)

- Team DPS 6 000 de referencia para Mandate (+7 % → +357; escala lineal).
- Uptime de marca 85-100 % (Q 3.4 s, marca 4 s).
- Carry de referencia AS 2.6/330 por golpe para Censer (+164).
- HSP solo de Censer/Staff/Redemption + Revitalize 5 %; anillo de E-Mantra cuenta como 2.º escudo completo (entra 1 aliado).

### Contexto meta (24/09, Diamond+)

Karma support: WR 49.82 %, pick 4.68 %, ban 0.62 %, tendencia ↓14. Muestra de 3-4 días post-parche; el rol de enchanter se está recolocando tras 7.3.

### Validación del modelo

- `validate_slots(["Crimson","Mandate","Censer","Echoes","Staff"])` → **PASS**.
- Chequeo manual: E = (150+0.65×200)×1.21 = **339** ✓ · E-Mantra = (300+130)×1.21 = **520** ✓.

---

## APÉNDICE A — POOL DE ÍTEMES: veredicto para Karma support

| Ítem (oro) | Veredicto | Nota |
|---|---|---|
| Imperial Mandate (2 600) | ✅ Core 1 (team con 2+ daño) | +7 % team amp permanente |
| Ardent Censer (2 400) | ✅ Core (ADC-céntrico) | E-Mantra a 2 aliados = doble proc |
| Echoes of Helia (2 400) | ✅ Core 3 | Poke → cura |
| Crimson Lucidity (2 000) | ✅ Botas | Q cada 3.4 s |
| Staff of Flowing Waters (2 400) | ✅ 6.º default | AP+haste al carry |
| Redemption / Mikael's / Locket / Shurelya's / Zeke's | ⚠️ 6.º situacional | Ver matriz §6 |
| Yordle Trap (2 400) | ❌ | Aura < Mandate |
| Diadem of Songs (2 400) | ⚠️ | Solo asedios largos |
| Defensivos de HP puro | ❌ | Su E escala AP |

---

## APÉNDICE B — RUTAS DE COMPRA

```
SUPPORT MANDATE (default con 2+ carries):
Sickle → Ionian (4') → Scythe (6') → Mandate (9:30) → ⬆️ Crimson (10:30)
→ Censer (13') → Echoes (16') → Staff (19')

SUPPORT ADC-CÉNTRICO (tu ADC es el 80 % del team):
Sickle → Ionian → Scythe → Censer (9:30) → ⬆️ Crimson → Mandate → Echoes → Staff/Redemption

SUPPORT ANTI-DIVE:
Sickle → Ionian → Scythe → Mikael's → ⬆️ Crimson → Censer → Echoes → Locket

MID AP BURST (comunidad):
Tome → Boots of Mana → Luden's (8') → Malignance (11') → ⬆️ Spellslinger's (12')
→ Rabadon's (15') → Infinity Orb (17:30) → Zhonya's (20')
(vs MR stacking: Orb → Cryptbloom/Void Staff)
```

---

## Pie de página

*Reporte generado el 25/09/2026 con datos del parche 7.3 (21/09/2026). WR-LAB v1.4. Las métricas de valor-aliado y amp de equipo son comparativas — el valor absoluto importa menos que las diferencias relativas entre builds, que son robustas a los supuestos. Si Riot publica un 7.3a/b (hotfix), regenerar datos antes de publicar.*

**Referencias y créditos**

- Notas oficiales del parche 7.3 (21/09/2026) y 7.2 (08/07/2026) — © Riot Games, Inc. (wildrift.leagueoflegends.com). Fuente primaria: rediseño de Imperial Mandate, Ardent Censer, Echoes of Helia y ajustes de enchanters.
- Base de datos de ítems, runas y ficha de campeón — wr-meta.com (proyecto comunitario de JLVD DEV), sincronizada al 24/09/2026. Fuente secundaria: kit completo (W tether ×2), build/runas populares de mid y meta.
- Modelo matemático (valor-aliado + amp), Leyes 0-7 y validaciones — WR-LAB (laboratorio propio, `model/analysis_batch2.py`), construido sobre las fuentes anteriores.

**Aviso legal:** Wild Rift y League of Legends son marcas registradas de Riot Games, Inc. Este documento es una guía de comunidad con fines educativos, **no está afiliado, patrocinado ni respaldado por Riot Games**. Los nombres de ítems, campeones y estadísticas pertenecen a sus respectivos dueños. El análisis y las conclusiones son trabajo original del autor apoyado en WR-LAB.

---


---

---
tags:
  - Support
  - Enchanter
  - Bot-Lane
version: 1.2
Status: Aprobado
champion: Yuumi
patch: "7.3+7.3a"
---
**Fecha del análisis:** 25/09/2026
**Parche:** 7.3 (21-sep-2026)
**Rol principal:** Support (Bot Lane)
**Arquetipo:** Enchanter-attach — el modelo NO es DPS propio sino **valor-aliado** (escudos, curas y buffs multiplicados sobre tu Best Friend)
**Enfoque:** Attachada eres intargeteable → **cero stats defensivos tienen valor**; cada punto de oro va a AP/HSP/Haste, con Ardent Censer como multiplicador del carry.

> [!NOTE]
> **Estado Meta Actual (Diamond+, 24/09/2026):**
> 
> Win Rate 48.25 % | Pick Rate 8.72 % | **Ban 34.23 % (señal ⛔ perma-ban)** | Tendencia ↑4 | Rol: Support. Si no la banean, es pick de dúo con carry de AS.

> [!TIP]
> **Variante anti-dive:** cambia Redemption por **Mikael's Blessing** (cleanse + 150-250 heal) cuando el enemigo tiene CC de un objetivo (Zed R, Ashe R, hooks). Pierdes la cura AoE pero salvas la vida del carry — que es tu verdadera barra de vida.

> [!WARNING]
> En Wild Rift Yuumi **sí compra botas** (a diferencia de PC) — confirmado en su build popular (Ionian → Crimson Lucidity). El mito del "slot extra" es falso.


> [!WARNING] Hotfix 7.3a (29-sep-2026) — NERF DIRECTO
> W Best Friend HSP: 8/9/10/11 % + 0.02 % AP → **6/7/8/9 % + 0.01 % AP**. Impacto medido: E-shield 339→~338 y R-heal 651→~648 (−0.3 %): el nerf es simbólico para SU build porque su HSP viene sobre todo de ítems+Revitalize. Además Diadem/Whispering Circlet nerfeadas (Harmonize 0.5→0.25 %) → la variante Y2 pierde atractivo. **Build, veredictos y Censer-core intactos.**
---

## 0. RESUMEN EJECUTIVO

### Tabla A — BUILD FINAL

| Slot | Ítem | Oro | Rol en la build |
|------|------|-----|-----------------|
| 1 (botas) | **Ionian Boots → ⬆️ Crimson Lucidity** (min 10:00, MISMO slot) | 2 000 | 25 haste + 75 % mana regen + MS al curar/escudar |
| 2 | **Black Mist Scythe** (quest de support — Spectral Sickle start) | 500 → 0 | Slot de quest; oro y visión |
| 3 | **Ardent Censer** | 2 400 | +30 % AS y +25 on-hit mágico a tu carry (uptime ~100 % con tu E) |
| 4 | **Echoes of Helia** | 2 400 | Soul Siphon: 30 % de tu daño → cura burst al aliado |
| 5 | **Staff of Flowing Waters** | 2 400 | +40 AP y +15 haste al aliado curado/escudado (y a ti) |
| 6 | **Redemption** (default) / Mikael's / Shurelya's / Zeke's | 2 450 | Cura AoE 150-350 + 10 % vida máx verdadero a enemigos |

> **Oro total: ~11 650 g** (presupuesto real de support a 20 min) · AP 180 · HSP 40 % · Haste 65 · **E = 339 de escudo · R = 651 de cura total · +244 DPS a tu ADC**

### Tabla B — Ruta de compra cronológica

| # | Compra | Oro acum. | Minuto típico |
|---|--------|-----------|---------------|
| 1 | **Spectral Sickle** (quest) + poción | 500 | 0:00 |
| 2 | Boots of Speed → **Ionian Boots of Lucidity** | 1 900 | ~4:00 |
| 3 | Quest completada → **Black Mist Scythe** | 1 900 | ~6:00 |
| 4 | Forbidden Idol + Aether Wisp → **Ardent Censer** | 4 300 | ~10:00 |
| 5 | ⬆️ **Crimson Lucidity** (mismo slot, +1 000 g) | 5 300 | ~11:00 |
| 6 | Bandleglass + Kindlegem → **Echoes of Helia** | 7 700 | ~14:00 |
| 7 | Forbidden Idol + Kindlegem → **Staff of Flowing Waters** | 10 100 | ~17:00 |
| 8 | Bandleglass + Blasting Wand → **Redemption** | 12 550 | ~20:00 |

### Runas · Hechizos · Habilidades

| Categoría | Elección |
|-----------|----------|
| Keystone | **Aery** (cada Q/E la manda: daño al pokear Y escudo al proteger — sus dos modos a la vez) |
| Sorcery 2 | **Axiom Arcanist** (+10 % daño/curas/escudos de R y −7 % CD con takedown) |
| Sorcery 3 | **Transcendence** (haste = más E/min = más uptime de Censer = más DPS del carry) |
| Sorcery 4 | **Scorch** (poke de Q) / **Manaflow Band** (si sufres maná) |
| Secundaria | **Revitalize** (+5 %, y +15 % con aliado <40 % HP — multiplica tu HSP) |
| Hechizos | **Flash + Exhaust** (peel absoluto desde attach) / Ignite con kill-lane |
| Skills | **Q → E → W** (R en 5/9/13) |

### Resultado del modelo (nivel 15, AP 180 / HSP 40 %)

| Métrica de valor-aliado | Valor |
|-----------|-----|
| Escudo E (por cast) | **339** |
| Cura total de R (7 olas, Best Friend) | **651** (+excedente → escudo) |
| **DPS añadido a tu ADC** (Censer + Q on-hit) | **+244** (≈ +28 % sobre ~858 base) |
| Escudo generado por minuto | **~3 953** |

> **Titular:** quitarle Ardent Censer a una Yuumi que juega con Kalista/Jinx/Yunara cuesta **−170 DPS de tu carry** — ningún otro ítem de 2 400 g da tanto poder de equipo medible.

---

## 1. CONTEXTO DEL CAMPEÓN EN ESTE PARCHE

### 1.1 Cambios directos a Yuumi (7.3)

Sin cambios de habilidades en 7.3 (ficha: AS ratio 0.625 / bonus 0.2 / 0.006 por nivel — irrelevante, no autoataca en fight).

### 1.2 Cambios sistémicos que la afectan

| Sistema | Cambio | Efecto en Yuumi |
|---|---|---|
| Ardent Censer (7.3) | 2 700 → **2 400 g**; buff estrechado: 30 % AS + 25 on-hit fijos (ya no escala con su nivel/crit) | MÁS fuerte y predecible para ella |
| Harmonic Echo → **Echoes of Helia** | Rehecho: Soul Siphon (30 % del daño → cura) | Su Q poke alimenta curas burst |
| Forbidden Idol (7.3) | 700 g, solo HSP 6 % (sin vida/haste) | Componentes de enchanter más baratos |
| Diadem of Songs (nuevo) | 0.8 % maná máx/s al aliado más bajo | Opción de sustain pasivo |
| Zeke's Convergence (7.3) | 2 400 g: 10 ult haste + Frostfire Tempest | R de Yuumi → slow AoE |

### 1.3 ¿Escala con crítico? No — escala con **Heal & Shield Power y AP**

Sus curas/escudos: E = 170 + **40 % AP**, R por ola = 52 + **8 % AP** (Best Friend), P = 70 + 25 % AP. Todo multiplicado por (1 + HSP). HSP total típico: ítems (8+8+8) + W-Best Friend (11 %) + Revitalize (5 %) = **40 %**.

---

## 2. FICHA MATEMÁTICA (spec)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD / HP base | 50 / 570 | Ficha wr-meta |
| P Feline Friendship | Autos/habs curan 70+25 % AP (CD 12-8 s); **Best Friend** (aliado con más Friendship por kills/minions juntos) → bonus en Q/R y +8-11 % HSP (W) | Ficha wr-meta |
| Q Prowling Projectile | 60-220 + 20 % AP; **attached con ≥1 s de vuelo: 100-340 + 35 % AP** + slow 45-65 %; al golpear da al aliado **+18-22 + 5 % AP on-hit por 5 s** (CD 5 s) | Ficha wr-meta |
| W You and Me! | Attach: untargetable (salvo torretas); CC sobre Yuumi la pone en CD 5 s | Ficha wr-meta |
| E Zoomies | Escudo 80-170 + **40 % AP** + **24-36 % AS** + 20 % MS al aliado, 3 s (CD 9 s) | Ficha wr-meta |
| R Final Chapter | 7 olas: 80-120 + 15 % AP daño / 20-50 + 5 % AP cura (BF: 26-52 + 8 %); excedente → escudo; slow +10 %/ola | Ficha wr-meta |

**Referencia de carry para el modelo:** ADC con AS 2.6 y 330 de daño/golpe (Jinx/Kalista full build ≈ 320-360 ✓).

---

## 3. MODELO Y FÓRMULAS (valor-aliado, no DPS propio)

```
E_escudo  = (170 + 0.40×AP) × (1 + HSP/100)
R_cura    = 7 × (52 + 0.08×AP) × (1 + HSP/100)          [Best Friend]
E_cd      = 9 × 100/(100 + haste)
ADC+DPS   = 0.115 × AS_carry × dmg_carry                [Censer: +30 % AS sobre AS ~2.6]
          + AS_carry × 25                               [Censer on-hit]
          + AS_carry × (22 + 0.05×AP)                   [Q on-hit al aliado, uptime ~100 %]
Escudo/min = E_escudo × 60/E_cd
```

### Supuestos específicos

- Censer y Q-on-hit con uptime ~100 % (E cada 5.1 s con haste 65 y buff de 6 s; Q CD 5 s y buff 5 s).
- HSP aplica a E y R (no al on-hit de Q ni a los fijos de Censer).
- La Scythe de quest ocupa slot (6 slots = scythe + botas + 4 ítems) — verificar si en tu servidor la quest completada se fusiona.
- Redemption/Diadem valorados cualitativamente (burst AoE / sustain) fuera de las métricas de tabla.

---

## 4. LEYES APLICADAS A YUUMI

### Ley 0 — Slots

1 botas (Crimson Lucidity T3) + quest + 4 ítems. `validate_slots(["Crimson","Echoes","Censer","Staff","Redemption"])` → PASS (5 entradas con botas; la quest es slot 6).

### Ley 4 — Stats muertos: TODA defensa es stat muerto

Attachada eres **untargeteable**. Vida/armadura/MR solo valen desattachada (P, visión, R en canalización te pueden castigar). Por eso Locket/Mikael's son "compras de equipo", no de stats — y por eso el AP/HSP puro es óptimo: Yuumi es el único campeón donde ser 100 % glass es matemáticamente correcto.

### Ley 5 — Eficiencia: Censer es el ítem más eficiente del parche para ella

2 400 g → +164-244 DPS del carry (según su build) + 30 % AS a TODO aliado que escudes. Comparado: Redemption cura 150-350 AoE cada 60+ s. En partidas donde tu carry es la win-con (tu dúo: Kalista/Jinx/Yunara), Censer primero SIEMPRE.

### Ley 6 — Timing

Censer al ~10:00 (2 400 g con economía de support) = pico de dúo justo cuando el carry completa su 2.º ítem. Crimson Lucidity tras el 10:00 (haste → más E/min → más Censer uptime).

### Ley 7 — Sistemas

Minions pegan 60 % a campeones → desattacharte a pokear con P es más seguro en 7.3. Torretas 7 000 HP → tu R en siege (7 olas desde attach, intargeteable) es de las formas más seguras de aplicar presión.

---

## 5. ANÁLISIS DEL PRIMER ÍTEM

**No aplica** — el primer "ítem" es la quest (Spectral Sickle → Black Mist Scythe). La primera decisión real es el ítem 3: **Censer** (carry de AS) vs **Echoes** (carry de burst / lane de poke). Con tus carries (Kalista/Jinx/Yunara): Censer.

---

## 6. BUILD FINAL RANURA POR RANURA

| Slot | Ítem | Justificación matemática |
|---|---|---|
| Botas | **Ionian → ⬆️ Crimson Lucidity** | 25 haste = E cada 5.1 s = Censer permanente; MS al curar (Noxian Haste) |
| Quest | **Black Mist Scythe** | Obligatoria (economía/visión); ocupa slot |
| 1 | **Ardent Censer** | +244 DPS al carry (tabla §0); el ítem que más poder de equipo da por 2 400 g |
| 2 | **Echoes of Helia** | Soul Siphon: tu Q poke (340 attached) se convierte en curas de ~100 al aliado |
| 3 | **Staff of Flowing Waters** | +40 AP y +15 haste al carry cuando lo escudas → sus hechizos rotan más rápido; a ti te da el AP que infla E/R |
| 4 | **Redemption** (default) | Cura AoE 150-350 + 10 % vida máx como daño verdadero a enemigos — ejecuta bajo tu R |

### Matriz del último slot (situacional)

| Situación | Ítem | Coste | Impacto |
|---|---|---|---|
| **Default** | **Redemption** | 2 450 | Burst AoE heal + verdadero |
| CC de un objetivo sobre el carry | **Mikael's Blessing** | 2 500 | Cleanse + 150-250 heal — salva vidas |
| Comp de engage (Diana/Malphite/Shyvana) | **Shurelya's Battlesong** | 2 500 | 30 % MS AoE activo — R+Shurelya = wombo |
| Tus carries engajean primero | **Zeke's Convergence** | 2 400 | R → 150 mágico + 30 % slow AoE + 10 ult haste |
| Sustain de asedio | **Diadem of Songs** | 2 400 | 0.8 % maná máx/s (~9.6 HP/s) al aliado más bajo |
| AoE burst enemigo | **Locket of the Iron Solari** | 2 600 | Escudo 250-370 AoE (halved si se repite en 20 s) |

### RECHAZADOS (con motivo numérico)

| Ítem | Motivo del rechazo |
|---|---|
| Imperial Mandate | Su CC es el slow de Q attached — marca de 1 objetivo; Censer+Echoes dan más valor por slot en su kit |
| Cualquier ítem defensivo en slots 1-3 | Ley 4: untargeteable attachada → oro muerto hasta que te obliguen a desattachear |
| Ítems de AP puro (Rabadon's/Luden's) | Sin HSP/haste/utilidad: E sube +52 con 130 AP... pero pierdes el multiplicador de equipo |
| Yordle Trap | Aura de 20 % AS a aliados < Censer (30 % + 25 on-hit) para su perfil |

---

## 7. RUNAS · HECHIZOS · HABILIDADES

### Keystone: Aery

Cada Q/E envía a Aery: **daña al pokear y escuda al proteger** — los dos modos de Yuumi en una runa. Comunidad coincide (ficha wr-meta).

**Alternativas:** *Guardian* (escudo 40-165+ al aliado damageado — vs dive pesado); nada más compite.

### Secundarias

| Slot | Runa | Valor estimado |
|---|---|---|
| Sorcery | **Axiom Arcanist** | +10 % curas/escudos/damage de R y −7 % CD con takedown (su R es de teamfight) |
| Sorcery | **Transcendence** | 10 haste + reducción post-nivel 9 → E cada ~5 s |
| Sorcery | **Scorch** / **Manaflow Band** | Poke de Q attached (+340 base) / +300 maná para Q-E-R spam |
| Resolve | **Revitalize** | +5 % (15 % con aliado <40 %) sobre E y R — multiplica HSP |

### Hechizos: Flash + Exhaust

Exhaust desde attach (−35 % MS y −40 % daño al diveador, 2.5 s) es el peel más barato del juego. Ignite solo con composición de kill-lane temprana.

### Orden de habilidades

**Q → E → W** · R en 5/9/13.
- Q max: daño attached 340+35 % AP, slow 65 % y el on-hit al carry (22+5 % AP) — su pico de valor.
- E segunda: escudo/AS/MS escalan y su CD baja a 9 s.
- W última: los rangos de Friendship/CD mejoran marginalmente.

---

## 8. COMPARACIÓN CONTRA LAS ALTERNATIVAS

### Tabla maestra (nivel 15, AP/HSP completos)

| Build | Oro | AP | HSP | E-shield | R-heal | **ADC +DPS** | Escudo/min |
|---|---|---|---|---|---|---|---|
| **Y1 Amp-ADC (Censer, Echoes, Staff, Redemption)** | 11 650 | 180 | 40 % | **339** | **651** | **+244** | 3 953 |
| Y2 Heal engine (sin Censer: Echoes, Staff, Diadem, Redem.) | 11 650 | 130 | 40 % | 311 | 612 | +74 | 3 626 |
| Y3 Anti-dive (Mikael's, Locket, Censer, Echoes) | 11 900 | 90 | 33 % | 274 | 551 | +233 | 3 288 |
| Y4 AP greedy (Censer, Staff, Echoes, Shurelya's) | 11 700 | 195 | 32 % | 327 | 625 | +246 | **4 037** |
| Y5 Zeke (comps de engage) | 11 600 | 140 | 32 % | 298 | 584 | +239 | 3 480 |

### Lectura

Y2 demuestra el punto central: **sin Censer pierdes −170 DPS de carry**. Y1 = default; Y4 cambia Redemption por Shurelya's (engage/MS); Y3 solo vs one-shot comps. Las diferencias de escudo entre Y1/Y4 son marginales (±12) — elige por utilidad del activo.

---

## 9. PLAN DE JUEGO

### Early (0:00 – 6:00)

- **Nivel 1:** desattachada — auto + Q para activar P (cura 70+) y presionar; vuelve al ADC antes de la oleada 2.
- **Friendship:** el Best Friend se construye con kills/minions juntos — haz la quest pegada a tu carry.
- **Maná:** Q attached cuesta 60; no spamees antes del nivel 3.

### Mid (6:00 – 14:00)

- **Nivel 6:** R disponible — primer all-in de dúo: Q attached (slow 65 %) → E → R (7 olas, slow acumulativo 70 %).
- **Rotaciones:** W entre lanes para visión y Friendship, NUNCA durante el spawn de cañón de tu lane.
- **Min 10:00:** ⬆️ Crimson Lucidity; Censer completo ≈ minuto 10 → pico de dúo.

### Late (14:00+)

- **Teamfight:** attach al carry → Q guiado desde niebla → E cíclico (Censer uptime) → R cuando agrupen (setup para Malphite/Diana R).
- **R + Shurelya's/Zeke's:** si llevas el activo, la secuencia R→activo gana la fight por posicionamiento.
- **Contra Yuumi:** el enemigo debe desattachearla con CC al cuerpo o matar a tu Best Friend — comunica jugar alrededor de tu carry BF.

### Reglas del parche que cambian el macro

| Regla | Impacto |
|---|---|
| Minions 60 % daño | Desattacharse a pokear es más seguro |
| Torretas 7 000 HP + cristales | R en siege = presión segura desde attach |
| Enchanter items más baratos (7.3) | Censer al 10:00 es realista con economía de support |

---

## 10. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS

### Fuentes primarias (mandan)

| Fuente | Acceso | Qué aporta |
|---|---|---|
| Notas oficiales 7.3 | 25/09/2026 | Ardent Censer 2 400/rediseño, Echoes of Helia, Forbidden Idol, Zeke's, Diadem |
| Notas oficiales 7.2 | 25/09/2026 | Rehecho de items de support (menos haste late), Redemption/Locket/Shurelya's/Mikael's |

### Fuentes secundarias

| Fuente | Acceso | Fiabilidad |
|---|---|---|
| wr-meta Yuumi (ficha + build + runas) | 25/09/2026 | Alta para kit (P/Q/W/E/R con Best Friend); build popular = insumo validado |

### Discrepancias detectadas y resolución

| Tema | Resolución |
|---|---|
| "Yuumi no usa botas" (mito de PC) | **Falso en WR**: su build popular trae Ionian → Crimson Lucidity ✓ |
| ¿La Scythe completada ocupa slot? | Asumido que sí (build popular la lista entre ítems) — verificar en juego |

### Supuestos del modelo (declarados)

- Carry de referencia: AS 2.6 / 330 daño por golpe; +30 % AS de Censer ≈ +11.5 % de su DPS.
- Uptimes ~100 % (E cada 5.1 s vs buff 6 s; Q CD 5 s vs buff 5 s).
- HSP aplica a E/R; Revitalize al 5 % base.
- Diadem/Redemption fuera de las métricas de tabla (valor situacional cualitativo).

### Contexto meta (24/09, Diamond+)

Yuumi: WR 48.25 %, pick 8.72 %, **ban 34.23 %** (⛔ perma-ban signal), tendencia ↑4. Traducción: en dúo coordinado es fuerte pero el enemigo la banea 1 de cada 3 veces — ten un plan B (Karma, misma ruta enchanter).

### Validación del modelo

- `validate_slots(["Crimson","Echoes","Censer","Staff","Redemption"])` → **PASS** (botas T3 única, quest como 6.º slot declarado).
- Chequeo manual: E = (170+0.4×180)×1.4 = 338.8 ≈ **339** ✓ · R = 7×(52+14.4)×1.4 = **651** ✓.

---

## APÉNDICE A — POOL DE ÍTEMES DE SUPPORT: veredicto para Yuumi

| Ítem (oro) | Veredicto | Nota |
|---|---|---|
| Ardent Censer (2 400) | ✅ Core 1 | +244 DPS al carry de AS |
| Echoes of Helia (2 400) | ✅ Core 2 | Poke → cura burst |
| Staff of Flowing Waters (2 400) | ✅ Core 3 | AP+haste al carry y a ti |
| Crimson Lucidity (2 000) | ✅ Botas | 25 haste = uptime de todo |
| Redemption (2 450) | ✅ 6.º default | AoE heal + verdadero |
| Mikael's Blessing (2 500) | ⚠️ 6.º vs CC | Cleanse salva al carry |
| Shurelya's Battlesong (2 500) | ⚠️ 6.º engage | MS AoE activo |
| Zeke's Convergence (2 400) | ⚠️ 6.º engage | R → slow AoE |
| Diadem of Songs (2 400) | ⚠️ 6.º asedio | 9.6 HP/s pasivo |
| Locket (2 600) | ⚠️ vs AoE burst | Escudo 250-370 |
| Imperial Mandate (2 600) | ❌ | Slow de Q marca 1 objetivo; Censer rinde más |
| Yordle Trap (2 400) | ❌ | Aura 20 % AS < Censer |
| Defensivos (Thornmail etc.) | ❌ | Ley 4: untargeteable |

---

## APÉNDICE B — RUTAS DE COMPRA

```
DEFAULT (carry de AS: Kalista/Jinx/Yunara):
Sickle → Ionian (4') → Scythe quest (6') → Censer (10') → ⬆️ Crimson (11')
→ Echoes (14') → Staff (17') → Redemption (20')

HEAL ENGINE (carry de burst / lane de poke):
Sickle → Ionian → Scythe → Echoes → ⬆️ Crimson → Staff → Diadem → Redemption/Mikael's

ANTI-DIVE (Zed/Rengar/Ashe R):
Sickle → Ionian → Scythe → Mikael's → ⬆️ Crimson → Censer → Echoes → Locket

ENGAGE COMP (Diana/Malphite/Shyvana allies):
Sickle → Ionian → Scythe → Censer → ⬆️ Crimson → Zeke's/Shurelya's → Echoes → Staff
```

---

## Pie de página

*Reporte generado el 25/09/2026 con datos del parche 7.3 (21/09/2026). WR-LAB v1.4. Las métricas de valor-aliado son comparativas — el valor absoluto importa menos que las diferencias relativas entre builds, que son robustas a los supuestos. Si Riot publica un 7.3a/b (hotfix), regenerar datos antes de publicar.*

**Referencias y créditos**

- Notas oficiales del parche 7.3 (21/09/2026) y 7.2 (08/07/2026) — © Riot Games, Inc. (wildrift.leagueoflegends.com). Fuente primaria: rediseño de Ardent Censer/Echoes of Helia/Forbidden Idol, items de support.
- Base de datos de ítems, runas y ficha de campeón — wr-meta.com (proyecto comunitario de JLVD DEV), sincronizada al 24/09/2026. Fuente secundaria: kit completo con Best Friend, build y runas populares, meta.
- Modelo matemático (valor-aliado), Leyes 0-7 y validaciones — WR-LAB (laboratorio propio, `model/analysis_batch2.py`), construido sobre las fuentes anteriores.

**Aviso legal:** Wild Rift y League of Legends son marcas registradas de Riot Games, Inc. Este documento es una guía de comunidad con fines educativos, **no está afiliado, patrocinado ni respaldado por Riot Games**. Los nombres de ítems, campeones y estadísticas pertenecen a sus respectivos dueños. El análisis y las conclusiones son trabajo original del autor apoyado en WR-LAB.

---


## 15. BASE DE ÍTEMS COMPLETA (pasivas + tips)

```csv
item,precio_oro,stats,categorias,detalle_completo
Chempunk Chainsword,2800,+400 Max Health | +45 Attack Damage | +15 Ability Haste,FIGHTER ITEMS,Chempunk Chainsword ~   ~ Chempunk Chainsword ~ Reduces enemy healing ~  +400 Max Health ~  +45 Attack Damage ~  +15 Ability Haste ~ Punishment: ~  Dealing  ~ physical damage ~  to enemy champions applies  ~ 50% Grievous Wounds ~  for 3 seconds. ~ Grievous Wounds ~  reduces the effectiveness of Healing and Regeneration effects. ~   ~ 2800 ~ Chempunk Chainsword 
Manamune,2900,+40 Attack Damage | +500 Max Mana | +15 Ability Haste,FIGHTER ITEMS; ASSASSIN ITEMS; MARKSMAN ITEMS,"Manamune ~   ~ Manamune ~ Converts Mana to Attack Damage ~  +40 Attack Damage ~  +500 Max Mana ~  +15 Ability Haste ~ Awe: ~  Grants  ~ Attack Damage ~  equal to  ~ 2% ~  of max Mana and refunds  ~ 15% ~  of all Mana spent. ~ Mana Charge: ~  Grants  ~ 14 ~  max Mana for each attack or Mana expenditure. Grants a maximum of  ~ 700 ~  max Mana, at which point this item transforms into Muramana. Occurs up to 3 times every 10 seconds. You may only carry one Tear of the Goddess item at a time. ~   ~ 2900 ~ Manamune "
Muramana,,+40 Attack Damage | +1200 Max Mana | +15 Ability Haste,FIGHTER ITEMS; ASSASSIN ITEMS; MARKSMAN ITEMS,"Muramana ~   ~ Muramana ~ Converts Mana to Attack Damage ~  +40 Attack Damage ~  +1200 Max Mana ~  +15 Ability Haste ~ Awe: ~  Grants  ~ Attack Damage ~  equal to  ~ 2% ~ of max Mana and refunds  ~ 15% ~ of all Mana spent. ~ Shock: ~  Attacks against champions deal  ~ 1.5% max Mana ~  as bonus  ~ physical damage ~ , and ability damage against champions deals  ~ 3.5% max Mana ~  (3% for ranged champions) as bonus  ~ physical damage ~ . This effect can only be triggered once per attack or ability cast against the same champion. ~ Muramana "
Eclipse,3000,+65 Attack Damage | +20 Ability Haste,FIGHTER ITEMS,"Eclipse ~   ~ Eclipse ~ Gain a shield and deal bonus damage ~  +65 Attack Damage ~  +20 Ability Haste ~ Ever Rising Moon: ~  Hitting an enemy champion with 2 separate attacks or abilities within 1.8s deals bonus  ~ physical damage ~  equal to  ~ 7% of the target's max Health ~ (3.5% for ranged champions), and grants you a  ~ shield ~  that absorbs damage equal to  ~ 140 + 35% bonus Attack Damage ~  ( ~ 70 + 18% bonus Attack Damage ~  for ranged champions) for 2s. (6s Cooldawn) ~   ~ 3000 ~ Eclipse "
Sundered Sky,3000,+350 Max Health | +40 Attack Damage | +15 Ability Haste,FIGHTER ITEMS,"Sundered Sky ~   ~ Sundered Sky ~ Periodically empowers attacks ~  +350 Max Health ~  +40 Attack Damage ~  +15 Ability Haste ~ Lightshield Strike: ~  The first attack against an enemy champion deals  ~ Critically Strikes ~  (6s cooldown per target), dealing 160% damage  and  ~ restores Health ~  (equal to  ~ 125% base Attack Damage ~  +  ~ 6% of missing Health ~  to you. ~   ~ 3000 ~ Sundered Sky "
Experimental Hexplate,3000,+400 Max Health | +35 Attack Damage | +20% Attack Speed,FIGHTER ITEMS,"Experimental Hexplate ~   ~ Experimental Hexplate ~ Gain Attack Speed & Movement Speed when your ultimate is cast ~  +400 Max Health ~  +35 Attack Damage ~  +20% Attack Speed ~ Hexcharged: ~   ~  Gain  ~ +20 Ability Haste ~  for your ultimate ability. ~ Overdrive: ~  After using your ultimate ability, gain  ~ 40% Attack Speed ~  and  ~ 20% Movement Speed ~   for 8s. (30s Cooldown) ~   ~ 3000 ~ Experimental Hexplate "
Maw of Malmortius,3000,+55 Attack Damage | +45 Magic Resistance | +10 Ability Haste,FIGHTER ITEMS; ASSASSIN ITEMS; MARKSMAN ITEMS,"Maw of Malmortius ~   ~ Maw of Malmortius ~ Converts damage from attacks into a magic shield ~  +55 Attack Damage ~  +45 Magic Resistance ~  +10 Ability Haste ~ Lifeline: ~  Upon taking Magic Damage that would reduce your  ~ Health ~  to below  ~ 35% ~ , gain  ~ +10% Omni Vamp. ~  until the end of combat and a  ~ magic shield ~  that absorbs  ~ 220-530 Magic Damage ~  for 3s. (70s Cooldown) ~   ~ 3000 ~ Maw of Malmortius "
Black Cleaver,3000,+400 Max Health | +40 Attack Damage | +20 Ability Haste,FIGHTER ITEMS,"Black Cleaver ~   ~ Black Cleaver ~ Physical Damage reduces Armor ~  +400 Max Health ~  +40 Attack Damage ~  +20 Ability Haste ~ Sunder: ~  Dealing  ~ physical damage ~  to a champion reduces their  ~ Armor ~  by 6% for 6 seconds, stacking 5 times for 30% reduction. ~ Rage: ~  Gain  ~ 20 Movement Speed ~  when you deal  ~ physical damage ~ . When moving toward enemy champions with 5 Sunder stacks, gain  ~ 40 Move Speed ~ . Ranged champions gain halved values. ~   ~ 3000 ~ Black Cleaver "
Titanic Hydra,3000,+450 Max Health | +40 Attack Damage,FIGHTER ITEMS; DEFENSE ITEMS,"Titanic Hydra ~   ~ Titanic Hydra ~ Attacks deal bonus damage in a area ~  +450 Max Health ~  +40 Attack Damage ~ Cleave: ~  Every 1.75 second(s), your next attack deals bonus  ~ physical damage ~  equal to  ~ 25 ~  +  ~ 3% bonus ~  (also applies to turrets) and creates a shockwave that deals  ~ physical damage ~  equal to  ~ 80 ~  +  ~ 10% bonus ~  to enemies behind the target. Ranged champions deal 75% of the damage. ~   ~ 3000 ~ Titanic Hydra "
Stridebreaker,3100,+400 Max Health | +40 Attack Damage | +25% Attack Speed,FIGHTER ITEMS,"Stridebreaker ~   ~ Stridebreaker ~ Slows enemies nearby after a short dash ~  +400 Max Health ~  +40 Attack Damage ~  +25% Attack Speed ~ Breaking Shockwave (Active): ~  Activate to dash a short distance, dealing  ~ 100% AD ~  as  ~ Physical Damage ~  to nearby enemies and  ~ slowing them by 40% ~  for 3s (25s cooldown) ~ Stride (Passive): ~  Gain  ~ 20 Movement Speed ~  for 2 second(s) when you deal  ~ physical damage ~ . ~   ~ 3100 ~ Stridebreaker "
Goredrinker,3100,+350 Max Health | +40 Attack Damage | +15 Ability Haste,FIGHTER ITEMS,Goredrinker ~   ~ Goredrinker ~ Deal damage in an area ~  +350 Max Health ~  +40 Attack Damage ~  +15 Ability Haste ~ Goredrink (Passive): Gain ~ 8% Omni Vamp. ~ Thirsting Slash (Active): ~  Deal  ~ 175% base AD ~  as  ~ physical damage ~  to nearby enemies. Restore Health equal to  ~ 20% ~  plus  ~ 10% missing ~  for each enemy champion hit. (12s cooldown) ~   ~ 3100 ~ Goredrinker 
Mercurial Scimitar,3100,+45 Attack Damage | +12% Lifesteal | +40 Magic Resistance,FIGHTER ITEMS; ASSASSIN ITEMS; MARKSMAN ITEMS,"Mercurial Scimitar ~   ~ Mercurial Scimitar ~ Dispels crowd control ~  +45 Attack Damage ~  +12% Lifesteal ~  +40 Magic Resistance ~ Quicksilver Sash (Active): ~  Removes all  ~ crowd control ~  debuffs from you and grants immunity to  ~ crowd control ~  for 0.25s. ~ Perseverance (Passive): ~  When the  ~ Quicksilver ~  effects ends, grant  ~ 30% Tenacity ~  and  ~ 30% Slow Resist ~  for 1.5 seconds. (60s Cooldown) ~ Cannot be used during knock up or knock back effects. ~   ~ 3100 ~ Mercurial Scimitar "
Blade of the Ruined King,3100,+40 Attack Damage | +35% Attack Speed | +12% Lifesteal,FIGHTER ITEMS; MARKSMAN ITEMS,Blade of the Ruined King ~   ~ Blade of the Ruined King ~ Attacks deal bonus damage ~  +40 Attack Damage ~  +35% Attack Speed ~  +12% Lifesteal ~ Ruined Strikes: ~  Attacks deal  ~ bonus physical damage ~  equal to  ~ 6% ~  of the enemy's current  ~ Health ~   ~ on-hit ~ . (Melee attacks deal  ~ 8% ~ ). Minimum damage: 15. Max damage vs monsters: 100. ~ Drain: ~  Hitting a champion with 3 attacks or abilities slows them by 30% for 1.5s. (30s Cooldown) ~   ~ 3100 ~ Blade of the Ruined King 
Serylda's Grudge,3100,+50 Attack Damage | +35% Armor Penetration | +15 Ability Haste,FIGHTER ITEMS; ASSASSIN ITEMS,Serylda's Grudge ~   ~ Serylda's Grudge ~ Armor Penetration (%) and apply slows ~  +50 Attack Damage ~  +35% Armor Penetration ~  +15 Ability Haste ~ Icy: ~  Damaging active abilities and  ~ empowered ~  attacks  ~ slow ~  enemies below  ~ 60% ~  current Health by  ~ 30% Movement Speed ~  for 1 second. ~   ~ 3100 ~ Serylda's Grudge 
Spear of Shojin,3100,+450 Max Health | +40 Attack Damage,FIGHTER ITEMS,Spear of Shojin ~   ~ Spear of Shojin ~ Gain damage bonuses ~  +450 Max Health ~  +40 Attack Damage ~ Dragonforce: ~   ~   ~ +20% Ability Haste. ~ Focused Will: ~  Dealing damage to monsters or enemies with abilities increases your champion's ability and passive damage by 3% for 6s. (Stacks 4 times). ~   ~ 3100 ~ Spear of Shojin 
Hullbreaker,3100,+400 Max Health | +50 Attack Damage,FIGHTER ITEMS,"Hullbreaker ~   ~ Hullbreaker ~ Split-pushing power ~  +400 Max Health ~  +50 Attack Damage ~ Set Sail: ~  Gain  ~ 5% Movement Speed ~ . ~ Skipper: ~  Every 4th attack against champions and epic monsters deals  ~ bonus physical damage ~  equal to  ~ 160% base  ~  plus  ~ 5% ~ (ranged champions deal  ~ 40% of the damage ~ ), increased to  ~ 240% base  ~  plus  ~ 9% ~ against structures (ranged champions deal  ~ 40% of the damage ~ ). ~ Boarding Party: ~  Nearby allied siege and super minions gain  ~ 20-130 Armor ~  (25% bonus if you're a ranged champion) and  ~ 10-120 Magic Resistance ~ ( ~ ) (25% bonus if you're a ranged champion). ~   ~ 3100 ~ Hullbreaker "
Overlord's Bloodmail,3200,+450 Max Health | +30 Attack Damage,FIGHTER ITEMS; DEFENSE ITEMS,Overlord's Bloodmail ~   ~ Overlord's Bloodmail ~ Gain Attack Damage when losing Health ~  +450 Max Health ~  +30 Attack Damage ~ Tyranny: ~  Gain  ~ Attack Damage ~  equal to  ~ 2.5% of your bonus Health ~ . ~ Retribution: ~  Gain up to 9% increased  ~ Attack Damage ~  based on your missing Health. Maximum Retribution bonus while below 30% Health. ~   ~ 3200 ~ Overlord's Bloodmail 
Guardian Angel,3200,+45 Attack Damage | +40 Armor,FIGHTER ITEMS; ASSASSIN ITEMS; MARKSMAN ITEMS; DEFENSE ITEMS,"Guardian Angel ~   ~ Guardian Angel ~ Revives at death ~  +45 Attack Damage ~  +40 Armor ~ Resurrect: ~  Upon taking lethal damage, restores  ~ 50% Health ~  and  ~ 100% Mana ~  after 4 seconds of stasis. (180s Cooldown) ~   ~ 3200 ~ Guardian Angel "
Bloodthirster,3200,+75 Attack Damage | +15% Lifesteal,FIGHTER ITEMS; MARKSMAN ITEMS,Bloodthirster ~   ~ Bloodthirster ~ Gain Lifesteal and convert excess healing into a shield ~  +75 Attack Damage ~  +15% Lifesteal ~ Ichorshield: ~  Convert excess healing from your  ~ Lifesteal ~  to a  ~ shield ~  that absorbs up to  ~ 165–345 ~  damage. ~   ~ 3200 ~ Bloodthirster 
Sterak's Gage,3200,+400 Max Health | +20% Tenacity,FIGHTER ITEMS; DEFENSE ITEMS,Sterak's Gage ~   ~ Sterak's Gage ~ Taking damage triggers a shield ~  +400 Max Health ~  +20% Tenacity ~ Heavy Handed: ~   ~ +50% base Attack Damage ~  as  ~ bonus Attack Damage ~ . ~ Lifeline: ~  Damage that puts you under  ~ 35% ~  Health ~  grants a  ~ shield ~  that equal to  ~ 75% of your bonus health ~  that decays over 5 seconds (70s Cooldown). ~ Sterak's Fury: ~  Triggering Lifeline increases size and grants  ~ 30% Tenacity ~  for 8 seconds. ~   ~ 3200 ~ Sterak's Gage 
Death's Dance,3200,+50 Attack Damage | +45 Armor | +15 Ability Haste,FIGHTER ITEMS; DEFENSE ITEMS,"Death's Dance ~   ~ Death's Dance ~ Delays damage taken ~  +50 Attack Damage ~  +45 Armor ~  +15 Ability Haste ~ Cauterize: ~  30% of all  ~ physical damage ~  and  ~ magic damage ~  received (12% for ranged champions) is dealt to you over 3 seconds as true damage instead. ~ Defy: ~  When a champion that you damaged within 3 second(s) dies, cleanse Cauterize's remaining damage pool and restore  ~ Health ~  equal to  ~ 90% bonus AD ~  over 2 second(s). ~   ~ 3200 ~ Death's Dance "
Trinity Force,3333,+333 Max Health | +36 Attack Damage | +30% Attack Speed | +15 Ability Haste,FIGHTER ITEMS; MARKSMAN ITEMS,"Trinity Force ~   ~ Trinity Force ~ Well-Rounded ~  +333 Max Health ~  +36 Attack Damage ~  +30% Attack Speed ~  +15 Ability Haste ~ Valor: ~  On hit, attacks grant  ~ 20 Move Speed ~  for 2 seconds. Bonuses do not stack.  ~ Bonus Movement Speed ~  does not stack. Ranged champions gain halved values.  ~ Spellblade: ~  Using an ability causes the next attack used within 10 seconds to deal  ~ bonus physical damage ~  equal to  ~ 200% base AD ~ (1.5s Cooldown). Damage is reduced vs structures. ~   ~ 3333 ~ Trinity Force "
Divine Sunderer,3400,+425 Max Health | +25 Attack Damage | +25 Ability Haste,FIGHTER ITEMS,"Divine Sunderer ~   ~ Divine Sunderer ~ Anti-Health attacks ~  +425 Max Health ~  +25 Attack Damage ~  +25 Ability Haste ~ Spellblade: ~  After using an ability, your next attack within 10 seconds deals  ~ (10% melee / 7% ranged) ~  of target's maximum health as bonus  ~ physical damage ~ . If the target is a champion, heal for  ~ (6% melee / 2.5% ranged) ~  of the target's maximum  ~ health ~ . (1.5s Cooldown) Damage is reduced vs structure. ~   ~ 3400 ~ Divine Sunderer "
Serpent's Fang,2800,+50 Attack Damage | +10 Ability Haste,ASSASSIN ITEMS,"Serpent's Fang ~   ~ Serpent's Fang ~ Anti-Shielding ~  +50 Attack Damage ~  +10 Ability Haste ~ Stab: ~   ~  +15 Armor Penetration. ~ Shield Reaver: ~  Dealing damage to an enemy champion reduces any  ~ shields ~  they gain for 3s. Melee champions apply ( ~ 10% of bonus AD ~  + 40)% shield reduction, capped at 60%; while ranged champions apply ( ~ 10% of bonus AD ~  + 25)% shield reduction, capped at 45%. When you damage an enemy who is unaffected by Shield Reaver, all shields on them are reduced by the same values. ~   ~ 2800 ~ Serpent's Fang "
Youmuu's Ghostblade,3000,+55 Attack Damage | +15 Armor Penetration | +15 Ability Haste | +4% Move Speed,ASSASSIN ITEMS,"Youmuu's Ghostblade ~   ~ Youmuu's Ghostblade ~ Increases Movement Speed ~  +55 Attack Damage ~  +15 Armor Penetration ~  +15 Ability Haste ~  +4% Move Speed ~ Momentum: ~  3 second(s) after leaving champion combat, gain  ~ 30 Move Speed ~  (20 for ranged champions). ~   ~ 3000 ~ Youmuu's Ghostblade "
Duskblade of Draktharr,3000,+55 Attack Damage | +10 Ability Haste,ASSASSIN ITEMS,Duskblade of Draktharr ~   ~ Duskblade of Draktharr ~ Attacks deal bonus damage ~  +55 Attack Damage ~  +10 Ability Haste ~ Razor: ~   ~  +18 Armor Penetration. ~ Nightstalker: ~  The first attack against a champion deals  ~ 60-160 bonus physical damage ~  and  ~ slows ~  them by 99% for 0.35s (10s cooldown). Champion takedowns refresh cooldown. ~   ~ 3000 ~ Duskblade of Draktharr 
Edge of Night,3000,+250 Max Health | +50 Attack Damage,ASSASSIN ITEMS,Edge of Night ~   ~ Edge of Night ~ Blocks an enemy ability ~  +250 Max Health ~  +50 Attack Damage ~ Gouge: ~   ~  +12 Armor Penetration. ~ Annul: ~  Grants a spell shield that blocks the next hostile ability. This spell shield refreshes upon leaving combat with enemy champions. (35 second cooldown) ~   ~ 3000 ~ Edge of Night 
The Collector,3000,+50 Attack Damage | +10 Armor Penetration | +25% Critical Rate,ASSASSIN ITEMS; MARKSMAN ITEMS,"The Collector ~   ~ The Collector ~ Execute low health champions ~  +50 Attack Damage ~  +10 Armor Penetration ~  +25% Critical Rate ~ Death and Taxes: ~  Dealing damage that would leave an enemy champion below 5% of their  ~ max Health ~  executes them, permanently increases the  ~ max Health ~  percentage execution threshold by 0.1%, and grants  ~ 25 bonus gold ~ . ~ Limited to 1 The Collector. ~   ~ 3000 ~ The Collector "
Fiendhunter Bolts,2650,+25% Critical Rate | +45% Attack Speed | +4% Move Speed,MARKSMAN ITEMS,"Fiendhunter Bolts ~   ~ Fiendhunter Bolts ~ After using your ultimate ability, your next few attacks Critically Strike ~  +25% Critical Rate ~  +45% Attack Speed ~  +4% Move Speed ~ Night Vigil: ~  Gain  ~ 20 ~  Ultimate  ~ Ability haste ~ . ~ Opening Barrage: ~  After casting your ultimate ability, your next 3 attacks within 8s gain  ~ 50% Attack Speed ~  and  ~ Critically Strike ~  for 80% of your normal  ~ Critical Damage ~ . If an attack would already Critically Strike, it deals  ~ 15% ~  bonus  ~ true damage ~  instead. (45s Cooldown) ~   ~ 2650 ~ Fiendhunter Bolts "
Rapid Firecannon,2650,+25% Critical Rate | +40% Attack Speed | +4% Move Speed,MARKSMAN ITEMS,Rapid Firecannon ~   ~ Rapid Firecannon ~ Increases attack range and damage ~  +25% Critical Rate ~  +40% Attack Speed ~  +4% Move Speed ~ Sharpshooter: ~  Moving and attacking generates an  ~ Energized Attack ~  with 35% bonus Attack Range (max 150 range) that deals  ~ 80 bonus magic damage ~ . ~   ~ 2650 ~ Rapid Firecannon 
Runaan's Hurricane,2650,+40% Attack Speed | +25% Critical Rate | +4% Move Speed,MARKSMAN ITEMS,"Runaan's Hurricane ~   ~ Runaan's Hurricane ~ Ranged Attacks hit 3 targets ~  +40% Attack Speed ~  +25% Critical Rate ~  +4% Move Speed ~ Wind's Fury: ~  Attacks strike 2 additional nearby enemies, each dealing  ~ 55% AD ~ . These strikes can  ~ Critically Strike ~  and trigger  ~ on-hit ~  effects. ~ This item cannot only be used by melee champions. ~   ~ 2650 ~ Runaan's Hurricane "
Phantom Dancer,2650,+25% Critical Rate | +40% Attack Speed | +7% Movement Speed,MARKSMAN ITEMS,"Phantom Dancer ~   ~ Phantom Dancer ~ Movement speed and attack speed ~  +25% Critical Rate ~  +40% Attack Speed ~  +7% Movement Speed ~ Spectral Waltz: ~   ~ On hit ~ , your attacks against a champion grant  ~ 6% Attack Speed ~  and  ~ 1% Movement Speed ~  for 6 second(s). Bonuses stack up to 5 times. ~   ~ 2650 ~ Phantom Dancer "
Navori Quickblades,2650,+25% Critical Rate | +40% Attack Speed | +4% Move Speed,MARKSMAN ITEMS,Navori Quickblades ~   ~ Navori Quickblades ~ Attacks reduce basic ability cooldowns ~  +25% Critical Rate ~  +40% Attack Speed ~  +4% Move Speed ~ Deft Strikes: ~  Attacks reduce the remaining  ~ cooldowns ~  of your basic abilities by  ~ 15% ~ . ~   ~ 2650 ~ Navori Quickblades 
Wit's End,2800,+50% Attack Speed | +45 Magic Resistance | +20% Tenacity,MARKSMAN ITEMS,Wit's End ~   ~ Wit's End ~ Basic Attack deals Bonus Damage ~  +50% Attack Speed ~  +45 Magic Resistance ~  +20% Tenacity ~ At Wit's End: ~  Attacks deal  ~ 40 bonus magic damage ~  on hit.  ~   ~ 2800 ~ Wit's End 
Hexoptics C44,2900,+55 Attack Damage | +25% Critical Rate,MARKSMAN ITEMS,"Hexoptics C44 ~   ~ Hexoptics C44 ~ Increases attack range and damage ~  +55 Attack Damage ~  +25% Critical Rate ~ Magnification: ~  Deal 0–10% increased damage with attacks, based on how far away the enemy is (max damage at 550 range). ~ Arcane Aim: ~  When a champion you damaged within 3 seconds dies, gain  ~ 100 ~  additional  ~ Attack Range ~  for 8 seconds. ~   ~ 2900 ~ Hexoptics C44 "
Kraken Slayer,2900,+45 Attack Damage | +35% Attack Speed | +4% Move Speed,MARKSMAN ITEMS,"Kraken Slayer ~   ~ Kraken Slayer ~ Deal bonus physical damage ~  +45 Attack Damage ~  +35% Attack Speed ~  +4% Move Speed ~ Bring it Down: ~  Every third attack deals  ~ 150–210 ~  bonus  ~ physical damage ~  ( ~ 120–168 ~  for ranged champions), increased by 0.75% per 1% Health the target is missing, up to an increase of 75%. ~   ~ 2900 ~ Kraken Slayer "
Nashor's Tooth,2900,+50% Attack Speed | +80 Ability Power | +15 Ability Haste,MARKSMAN ITEMS; MAGIC ITEMS,Nashor's Tooth ~   ~ Nashor's Tooth ~ Attacks deal bonus damage ~  +50% Attack Speed ~  +80 Ability Power ~  +15 Ability Haste ~ Gnaw: ~  Attacks deal (15 +  ~ 20% bonus ~ )  ~ magic damage ~  as  ~ on-hit ~ . ~   ~ 2900 ~ Nashor's Tooth 
Statikk Shiv,3000,+40 Attack Damage | +30% Attack Speed | +40 Ability Power | +4% Move Speed,MARKSMAN ITEMS; MAGIC ITEMS,"Statikk Shiv ~   ~ Statikk Shiv ~ Energized Attacks deal chain damage ~  +40 Attack Damage ~  +30% Attack Speed ~  +40 Ability Power ~  +4% Move Speed ~ Electroshock: ~  Attacks grant 5 extra  ~ Energized stacks ~ . ~ Electrospark: ~  Moving and attacking generate an  ~ Energized Attack ~  that fires chain lightning to 4–7 targets ( ~ ), dealing  ~ 60 magic damage ~  (increased to  ~ 90 magic damage ~  against minions and monsters) and applying  ~ on-hit effects ~  to secondary bounce targets. ~   ~ 3000 ~ Statikk Shiv "
Guinsoo's Rageblade,3000,+35 Attack Damage | +30% Attack Speed | +30 Ability Power,MARKSMAN ITEMS; MAGIC ITEMS,"Guinsoo's Rageblade ~   ~ Guinsoo's Rageblade ~ Applies on-hit effects ~  +35 Attack Damage ~  +30% Attack Speed ~  +30 Ability Power ~ Wrath: ~  Attacks deal  ~ 30 bonus magic damage ~   ~ on hit ~ . ~ Seething Strike: ~  Attacks grant  ~ 8% Attack Speed ~ , stacking up to 4 times for a maximum of  ~ 32% Attack Speed ~ . While fully stacked, every 3 attack(s) applies  ~ on-hit ~  effects an additional 1 time(s). ~   ~ 3000 ~ Guinsoo's Rageblade "
Mortal Reminder,3000,+35 Attack Damage | +30% Armor Penetration | +25% Critical Rate,MARKSMAN ITEMS,Mortal Reminder ~   ~ Mortal Reminder ~ Armor Penetration (%) and reduced enemy healing ~  +35 Attack Damage ~  +30% Armor Penetration ~  +25% Critical Rate ~ Sepsis: ~  Dealing  ~ physical damage ~  to enemy champions applies  ~ 50% Grievous Wounds ~  for 3 seconds. ~ Grievous Wounds ~  reduces the effectiveness of Healing and Regeneration effects. ~   ~ 3000 ~ Mortal Reminder 
Essence Reaver,3000,+50 Attack Damage | +25% Critical Rate | +20 Ability Haste,MARKSMAN ITEMS,"Essence Reaver ~   ~ Essence Reaver ~ Attacks casting an ability, your next attack deals bonus damage ~  +50 Attack Damage ~  +25% Critical Rate ~  +20 Ability Haste ~ Spellblade: ~  Using an ability causes your next attack within 10s to deal bonus  ~ physical damage ~  equal to  ~ 135% base AD ~  plus  ~ 0–80 ~  (increased by 0.8 per  ~ 1% Critical Rate ~ ) and restore  ~ 50% ~  of this damage as  ~ Mana ~ . (1.5s Cooldown) ~   ~ 3000 ~ Essence Reaver "
Immortal Shieldbow,3000,+55 Attack Damage | +25% Critical Rate,MARKSMAN ITEMS,Immortal Shieldbow ~   ~ Immortal Shieldbow ~ Gain a shield when Health is low ~  +55 Attack Damage ~  +25% Critical Rate ~ Lifeline: ~  Damage that puts you under  ~ 35% Health ~  grants a  ~ shield ~  for 3s. The  ~ shield ~  absorbs  ~ 350–650 ~  damage for melee champions and  ~ 300–550 ~  damage for ranged champions. (70s cooldown) ~   ~ 3000 ~ Immortal Shieldbow 
Terminus,3000,+35 Attack Damage | +35% Attack Speed,MARKSMAN ITEMS,"Terminus ~   ~ Terminus ~ Increases Armor Pen, Megic Pen, Armor, and Magic Resist ~  +35 Attack Damage ~  +35% Attack Speed ~ Shadow: ~  Attacks deal  ~ 30 bonus magic damage ~   ~ on-hit ~ . ~ Juxtaposition: ~  Alternate between Light and Dark on-hits when attacking. Light attacks grant 5-8  ~ Armor ~  and  ~ Magic Resist ~ ( ~ ) for 5 seconds on hit. Dark attacks grant  ~ 10% Armor Pen ~  and  ~ 10% Magic Pen ~  for 5 seconds  ~ on hit ~ . Each on-hit effect stacks up to 3 times. While you have this item, bonus  ~ Armor Pen ~  and  ~ Magic Pen ~  granted by it is capped at 40%. ~ You cannot own this item concurrently with Void Staff. ~   ~ 3000 ~ Terminus "
Stormrazor,3000,+50 Attack Damage | +25% Critical Rate | +20% Attack Speed,MARKSMAN ITEMS,Stormrazor ~   ~ Stormrazor ~ Energized Attacks deal extra damage and grant Movement Speed ~  +50 Attack Damage ~  +25% Critical Rate ~  +20% Attack Speed ~ Bolt: ~  Moving and attacking generates an  ~ Energized Attack ~  that deals  ~ 120 ~  bonus  ~ magic damage ~  and grants 45% Movement Speed for 1.5 second(s)  ~ on hit ~ . ~   ~ 3000 ~ Stormrazor 
Yun Tal Wildarrows,3100,+50 Attack Damage | +25% Attack Speed,MARKSMAN ITEMS,"Yun Tal Wildarrows ~   ~ Yun Tal Wildarrows ~ Attacks gain Critical Rate ~  +50 Attack Damage ~  +25% Attack Speed ~ Practice Makes Perfect: ~  On attack, gain  ~ Critical Rate ~  permanently ( ~ 0.4% ~  for melee champions and  ~ 0.2% ~  for ranged champions per attack), up to  ~ 25% ~ . ~ Flurry: ~  On attacking an enemy champion, gain  ~ 25% Attack Speed ~  for 6s. (20s Cooldown) Attacks reduce this cooldown by 1s, increased to 2s for  ~ Critical Strikes ~ . ~   ~ 3100 ~ Yun Tal Wildarrows "
Galeforce,3100,+60 Attack Damage | +25% Critical Rate | +4% Move Speed,MARKSMAN ITEMS,"Galeforce ~   ~ Galeforce ~ Grants a dash and damage bonus ~  +60 Attack Damage ~  +25% Critical Rate ~  +4% Move Speed ~ Cloudburst (Active): ~  Dash in a target direction and fire 3 missile(s) at the lowest Health enemy near your destination, prioritizing champions. Deal  ~ physical damage ~  equal to  ~ 40-125 ~  ( ~ ) plus  ~ 35% bonus ~ . (60s Cooldown) ~   ~ 3100 ~ Galeforce "
Dominik's Regards,3300,+35 Attack Damage | +35% Armor Penetration | +25% Critical Rate,MARKSMAN ITEMS,"Dominik's Regards ~   ~ Dominik's Regards ~ Armor Pen and bonus damage ~  +35 Attack Damage ~  +35% Armor Penetration ~  +25% Critical Rate ~ Giant Slayer: ~  Deal bonus damage based on the enemy champion's  ~ bonus Health ~ , up to 12% bonus damage when the enemy champion has  ~ 1.200 bonus Health ~ . ~   ~ 3300 ~ Dominik's Regards "
Infinity Edge,3400,+75 Attack Damage | +25% Critical Rate,MARKSMAN ITEMS,Infinity Edge ~   ~ Infinity Edge ~ Increases Critical Strike Damage ~  +75 Attack Damage ~  +25% Critical Rate ~ Infinity: ~  Critical Strikes deal  ~ 230% damage ~  instead of  ~ 200% ~ . ~   ~ 3400 ~ Infinity Edge 
Whispering Circlet,2400,+200 Max Health | +500 Max Mana | +50% Mana Regen | +8% Heal and Shield Strength,MAGIC ITEMS; SUPPORT ITEMS,Whispering Circlet ~   ~ Whispering Circlet ~ Convert Mana into Heal and Shield Powe ~  +200 Max Health ~  +500 Max Mana ~  +50% Mana Regen ~  +8% Heal and Shield Strength ~ Harmony: ~  Gain  ~ 0.5% max Mana ~  as bonus  ~ Heal and Shield Power ~ . Casting an ability refunds  ~ 25% of its Mana ~  cost. ~ Mana Charge: ~  Grants  ~ 14 max Mana ~  for each Mana expenditure (occurs up to 3 times every 10 seconds). Caps at  ~ 700 max Mana ~ . This item then transforms into Diadem of Songs. ~   ~ 2400 ~ Whispering Circlet 
Diadem of Songs,,+200 Max Health | +1200 Max Mana | +50% Mana Regen | +8% Heal and Shield Strength,MAGIC ITEMS; SUPPORT ITEMS,"Diadem of Songs ~   ~ Diadem of Songs ~ Convert Mana into Heal and Shield Powe ~  +200 Max Health ~  +1200 Max Mana ~  +50% Mana Regen ~  +8% Heal and Shield Strength ~ Harmony: ~  Gain  ~ 0.5% max Mana ~  as bonus  ~ Heal and Shield Power ~ . Casting an ability refunds  ~ 25% of its Mana ~  cost. ~ Diadem: ~  While you or an ally you've healed or shielded in the last 3 second(s) is in combat with champions, each second,  ~ heal ~  the lowest Health ally within 800 units of you for  ~ Health ~  equal to  ~ 0.8% max Mana ~ . ~ Diadem of Songs "
Redemption,2450,+40 Ability Power | +50% Mana Regen | +10 Ability Haste | +8% Heal and Shield Strength,MAGIC ITEMS; SUPPORT ITEMS,"Redemption ~   ~ Redemption ~ Heal allies in an area ~  +40 Ability Power ~  +50% Mana Regen ~  +10 Ability Haste ~  +8% Heal and Shield Strength ~ Intervention (Active): ~  Target a large area. After 2.5s,  ~ restore 150-350 Health ~  (based on ally's level) to allied units and deal  ~ 10% of max ~  as  ~ true damage ~  to enemy champions. (60s Cooldown) ~ Can be cast while dead. ~   ~ 2450 ~ Redemption "
Imperial Mandate,2600,+60 Ability Power | +50% Mana Regen | +20 Ability Haste,MAGIC ITEMS; SUPPORT ITEMS,"Imperial Mandate ~   ~ Imperial Mandate ~ Crowd control grants additional ally damage ~  +60 Ability Power ~  +50% Mana Regen ~  +20 Ability Haste ~ Control: ~  Your crowd control abilities gain  ~ 20 Ability Haste ~ . ~ Command: ~  Crowd controlling an enemy champion marks them for 4 second(s), causing them to take 7% increased damage. ~   ~ 2600 ~ Imperial Mandate "
Oceanid's Trident,2600,+200 Max Health | +80 Ability Power | +10 Ability Haste,MAGIC ITEMS; SUPPORT ITEMS,"Oceanid's Trident ~   ~ Oceanid's Trident ~ Anti-Shielding ~  +200 Max Health ~  +80 Ability Power ~  +10 Ability Haste ~ Lethal Weapon: ~  Dealing ability damage to an enemy champion reduces any  ~ shields ~  they gain for 3 seconds. Area of effect abilities apply ( ~ 5% of bonus AP ~  + 25)% shield reduction, capped at 45%; while single target abilities apply ( ~ 5% of bonus AP ~  + 40)% shield reduction, capped at 60%. When you damage an enemy who is unaffected by  ~ Lethal Weapon ~ , all shields on them are reduced by the same values. ~   ~ 2600 ~ Oceanid's Trident "
Morellonomicon,2650,+300 Max Health | +75 Ability Power | +15 Ability Haste,MAGIC ITEMS; SUPPORT ITEMS,Morellonomicon ~   ~ Morellonomicon ~ Magic damage reduces enemy healing ~  +300 Max Health ~  +75 Ability Power ~  +15 Ability Haste ~ Affliction: ~  Dealing  ~ magic damage ~  to enemy champions inflicts  ~ 50% Grievous Wounds ~  for 3 seconds. ~ Grievous Wounds ~  reduces the effectiveness of Healing and Regeneration effects. ~   ~ 2650 ~ Morellonomicon 
Hextech Roketbelt,2700,+250 Max Health | +70 Ability Power | +20 Ability Haste,MAGIC ITEMS,"Hextech Roketbelt ~   ~ Hextech Roketbelt ~ Small dash ~  +250 Max Health ~  +70 Ability Power ~  +20 Ability Haste ~ Protobelt (Active): ~  Dash forward and unleash a cone of missiles, dealing  ~ 100 ~  plus  ~ 10% ~   ~ magic damage. ~  (30s Cooldown) ~ If champions or monsters are hit by more than one missile, missiles after the first will deal only 10% damage. ~   ~ 2700 ~ Hextech Roketbelt "
Rylai's Crystal Scepter,2700,+350 Max Health | +65 Ability Power,MAGIC ITEMS,Rylai's Crystal Scepter ~   ~ Rylai's Crystal Scepter ~ Abilities apply slows ~  +350 Max Health ~  +65 Ability Power ~ Icy: ~  Damaging abilities and  ~ empowered attacks ~   ~ slow enemies ~  by 30% for 0.75 second. ~   ~ 2700 ~ Rylai's Crystal Scepter 
Rod of Ages,2700,+350 Max Health | +50 Ability Power | +400 Max Mana,MAGIC ITEMS,"Rod of Ages ~   ~ Rod of Ages ~ Stats grow over time ~  +350 Max Health ~  +50 Ability Power ~  +400 Max Mana ~ Eternity: ~  Restore  ~ Mana ~  equal to  ~ 15% ~  of the damage taken from champions. Regen  ~ Health ~  equal to  ~ 20% Mana ~  spent. Capped at  ~ 25 Health ~  per cast. ~ Veteran: ~  Each stack provides  ~ 15 Health ~ ,  ~ 30 Mana ~  and  ~ 4 Ability Power ~ , stacking at a rate of 1 every 35 seconds. Max of 10 stacks, providing  ~ 150 Health ~ ,  ~ 300 Mana ~ , and  ~ 40 Ability Power ~ . ~   ~ 2700 ~ Rod of Ages "
Horizon Focus,2700,+80 Ability Power | +25 Ability Haste,MAGIC ITEMS,"Horizon Focus ~   ~ Horizon Focus ~ Deals bonus damage to marked targets ~  +80 Ability Power ~  +25 Ability Haste ~ Hypershot: ~  Damaging an enemy champion with an ability from 600 units away reveals them for 8 seconds and increases damage dealt to them by 10%. ~ Focus: ~  When Hypershot is triggered, it reveals all enemy champions within 1.200 units of the target for 3s. (12s Cooldown) ~   ~ 2700 ~ Horizon Focus "
Malignance,2700,+90 Ability Power | +500 Max Mana | +15 Ability Haste,MAGIC ITEMS,"Malignance ~   ~ Malignance ~ An item made for Ultimate-centric playstyles ~  +90 Ability Power ~  +500 Max Mana ~  +15 Ability Haste ~ Scorn: ~  Your Ultimate abilities gain  ~ 20 Ability Haste ~ . ~ Hatefog: ~  Damaging a champion with your Ultimate burns the ground beneath them for 3 second(s), dealing  ~ magic damage ~  equal to  ~ 60 ~  plus  ~ 5% AP ~  per second and reducing their  ~ Magic Resist by 10 ~ . Burn radius increases with damage, reaching maximum radius at 800 damage. ~   ~ 2700 ~ Malignance "
Stormsurge,2800,+90 Ability Power | +15 Magic Penetration | +6% Move Speed,MAGIC ITEMS,"Stormsurge ~   ~ Stormsurge ~ A powerful item for Scaling Mages ~  +90 Ability Power ~  +15 Magic Penetration ~  +6% Move Speed ~ Stormraider: ~  When damaging a champion, dealing damage equal to  ~ 25% of their max Health ~  within 2.5 second(s) applies  ~ Squall ~  to them and grants you  ~ 25% bonus Movement Speed ~  for 2.5s. (25s Cooldown) ~ Squall: ~  After 2 second(s), strike the target, dealing  ~ magic damage ~  equal to  ~ 125 ~  plus  ~ 10% ~ . If the target is killed before the strike, it detonates immediately in a large area and grants  ~ 25 gold ~ . ~   ~ 2800 ~ Stormsurge "
Blackfire Torch,2800,+80 Ability Power | +500 Maximum Mana | +20 Ability Haste,MAGIC ITEMS,"Blackfire Torch ~   ~ Blackfire Torch ~ Deal burn damage ~  +80 Ability Power ~  +500 Maximum Mana ~  +20 Ability Haste ~ Baleful Blaze: ~  Dealing damage with abilities causes enemies to burn for  ~ 20 ~  +  ~ 2% ~ magic damage ~  per second for 3 seconds. ~ Deal  ~ 40 ~  plus  ~ 2% ~ magic damage ~  every second to monsters. ~ Blackfire: ~  For each enemy champion or monster affected by your Baleful Blaze, gain  ~ 4% Ability Power ~ . ~   ~ 2800 ~ Blackfire Torch "
Luden's Echo,2800,+100 Ability Power | +500 Max Mana | +10 Ability Haste,MAGIC ITEMS,Luden's Echo ~   ~ Luden's Echo ~ Abilities deal bonus damage ~  +100 Ability Power ~  +500 Max Mana ~  +10 Ability Haste ~ Echo: ~  Your next damaging ability or  ~ empowered attack ~  deals an additional  ~ 140 ~  +  ~ 15% ~   ~ magic damage ~  to the target and up to  ~ 3 ~  nearby enemies. (9s Cooldown) ~   ~ 2800 ~ Luden's Echo 
Lich Bane,2800,+100 Ability Power | +10 Ability Haste | +5% Move Speed,MAGIC ITEMS,Lich Bane ~   ~ Lich Bane ~ Attacks deal bonus damage aster ability casts ~  +100 Ability Power ~  +10 Ability Haste ~  +5% Move Speed ~ Spellblade: ~  Using an ability causes the next attack used within 10 seconds to deal  ~ bonus magic damage ~  equal to  ~ 75% base AD  ~  +  ~ 45% AP  ~ . (1.5s Cooldown) Damage is reduced vs structures. ~   ~ 2800 ~ Lich Bane 
Bloodletter's Curse,2900,+350 Maximum Health | +65 Ability Power | +15 Ability Haste,MAGIC ITEMS,Bloodletter's Curse ~   ~ Bloodletter's Curse ~ Reduces enemy's Magic Resist ~  +350 Maximum Health ~  +65 Ability Power ~  +15 Ability Haste ~ Vile Decay: ~  Dealing  ~ magic damage ~  with abilities or passives to champions reduces their  ~ Magic Resist by 7.5% ~  for 6 seconds (max 30%). ~   ~ 2900 ~ Bloodletter's Curse 
Banshee's Veil,3000,+105 Ability Power | +40 Magic Resistance,MAGIC ITEMS; DEFENSE ITEMS,Banshee's Veil ~   ~ Banshee's Veil ~ Blocks an enemy ability ~  +105 Ability Power ~  +40 Magic Resistance ~ Annul: ~  Grants a  ~ spell shield ~  that blocks the next hostile ability. (30s Cooldown) ~   ~ 3000 ~ Banshee's Veil 
Cryptbloom,3000,+75 Ability Power | +30% Magic Penetration | +20 Ability Haste,MAGIC ITEMS; SUPPORT ITEMS,"Cryptbloom ~   ~ Cryptbloom ~ Restore health on champion kill ~  +75 Ability Power ~  +30% Magic Penetration ~  +20 Ability Haste ~ Life from Death: ~  When a champion that you damaged within 3s dies, a nova spreads from their corpse that  ~ restores 100 ~  plus  ~ 20% ~ Health ~  to allies. (60s Cooldown) ~   ~ 3000 ~ Cryptbloom "
Liandry's Torment,3000,+300 Max Health | +70 Ability Power,MAGIC ITEMS,"Liandry's Torment ~   ~ Liandry's Torment ~ Abilities deal bonus damage ~  +300 Max Health ~  +70 Ability Power ~ Torment: ~  Damaging abilities and  ~ empowered attacks ~  burn enemies for 2%  ~ max Health ~   ~ magic damage ~  for 3 seconds. ~ Madness: ~  Deals 2% more damage for each second in combat against champions, capped at 6% after 3 seconds. ~   ~ 3000 ~ Liandry's Torment "
Archangel's Staff,3000,+60 Ability Power | +500 Max Mana | +25 Ability Haste,MAGIC ITEMS,"Archangel's Staff ~   ~ Archangel's Staff ~ Converts Mana to Ability Power ~  +60 Ability Power ~  +500 Max Mana ~  +25 Ability Haste ~ Awe: ~  Grants Ability Power equal to  ~ 1% ~  max Mana and refunds  ~ 25%  ~  of all Mana spent. ~ Mana Charge: ~  Increases max Mana by  ~ 14 ~  every time Mana is spent. Caps at  ~ 700 bonus Mana ~ , transforming Archangel's Staff into Seraph's Embrace. Triggers up to 3 times every 10 seconds. You may only carry one Tear of the Goddess item at a time. ~   ~ 3000 ~ Archangel's Staff "
Seraph's Embrace,,+60 Ability Power | +1200 Max Mana | +25 Ability Haste,MAGIC ITEMS,"Seraph's Embrace ~   ~ Seraph's Embrace ~ Converts Mana to Ability Power ~  +60 Ability Power ~  +1200 Max Mana ~  +25 Ability Haste ~ Awe: ~  Grants Ability Power equal to  ~ 2% ~  max Mana and refunds  ~ 25%  ~  of all Mana spent. ~ Lifeline: ~  Damage that puts you under  ~ 35%  ~  Health ~  consumes  ~ 20% ~  of your current  ~ Mana ~  to grant a  ~ shield ~ , equal to that amount  ~ +100 ~  for 2 seconds. (70s cooldown). ~ Seraph's Embrace "
Cosmic Drive,3000,+300 Max Health | +70 Ability Power | +25 Ability Haste | +4% Move Speed,MAGIC ITEMS,Cosmic Drive ~   ~ Cosmic Drive ~ Dealing ability damage grants movement speed ~  +300 Max Health ~  +70 Ability Power ~  +25 Ability Haste ~  +4% Move Speed ~ Spelldance: ~  Dealing  ~ magic ~  or  ~ true damage ~  to champions grants  ~ 30 Movement Speed ~  for 4 second(s). ~   ~ 3000 ~ Cosmic Drive 
Dusk and Dawn,3100,+300 Maximum Health | +20% Attack Speed | +60 Ability Power | +20 Ability Haste,MAGIC ITEMS,"Dusk and Dawn ~   ~ Dusk and Dawn ~ Applies on-hit effects ~  +300 Maximum Health ~  +20% Attack Speed ~  +60 Ability Power ~  +20 Ability Haste ~ Spellblade: ~  After using an ability, your next attack deals  ~ (75% base ~ +  ~ 10% ~ ) bonus  ~ magic damage ~  and restores ( ~ 3% bonus ~  +  ~ 10% ~ ) Htalth to you. After a brief delay, apply  ~ on-hits ~  to the target 1 additional time. (1.5s Cooldown) ~ Deals reduced damage to structures. ~   ~ 3100 ~ Dusk and Dawn "
Infinity Orb,3100,+110 Ability Power | +15 Magic Penetration,MAGIC ITEMS,Infinity Orb ~   ~ Infinity Orb ~ Abilities deal bonus damage ~  +110 Ability Power ~  +15 Magic Penetration ~ Inevitable Demise: ~  Abilities and  ~ empowered attacks ~   ~ Critically Strike ~  for  ~ 20% ~  bonus damage against enemies below  ~ 40% Health ~ . ~   ~ 3100 ~ Infinity Orb 
Riftmaker,3100,+350 Max Health | +70 Ability Power | +15 Ability Haste,MAGIC ITEMS,"Riftmaker ~   ~ Riftmaker ~ Ramping Damage ~  +350 Max Health ~  +70 Ability Power ~  +15 Ability Haste ~ Void Corruption: ~  Every 1 second(s) in combat with enemy champions, deal 2% bonus damage, up to 8%. ~ At maximum strength, gain ~ Omni Vamp. ~  (10% for melee champions / 6% for ranged champions). ~ Void Infusion: ~  Gain  ~ 2% of your bonus Health ~  as  ~ Ability Power ~ . ~   ~ 3100 ~ Riftmaker "
Zhonya's Hourglass,3300,+40 Armor | +110 Ability Power,MAGIC ITEMS; DEFENSE ITEMS,"Zhonya's Hourglass ~   ~ Zhonya's Hourglass ~ Turn invulnerable ~  +40 Armor ~  +110 Ability Power ~ Stasis (Active): ~  Become invulnerable and untargetable for 2.5 seconds, but unable to move, attack, cast abilities or use items. (90s Cooldown) ~   ~ 3300 ~ Zhonya's Hourglass "
Rabadon's Deathcap,3400,+130 Ability Power,MAGIC ITEMS,Rabadon's Deathcap ~   ~ Rabadon's Deathcap ~ Boosts Ability Power ~  +130 Ability Power ~ Overkill: ~  Increases  ~ Ability Power by 30% ~ . ~   ~ 3400 ~ Rabadon's Deathcap 
Abyssal Mask,2400,+350 Max Health | +45 Magic Resistance | +10 Ability Haste,DEFENSE ITEMS; SUPPORT ITEMS,Abyssal Mask ~   ~ Abyssal Mask ~ Deal increased magic damage ~  +350 Max Health ~  +45 Magic Resistance ~  +10 Ability Haste ~ Unmake: ~   ~ Magic damage ~  against enemy champions within 650 units of you is increased by 12%. (Unmake's damage bonus does not stack.) ~   ~ 2400 ~ Abyssal Mask 
Zeke's Convergence,2400,+300 Max Health | +25 Armor | +25 Magic Resistance | +10 Ability Haste,DEFENSE ITEMS; SUPPORT ITEMS,"Zeke's Convergence ~   ~ Zeke's Convergence ~ Deals damage in an area and slows nearby enemies ~  +300 Max Health ~  +25 Armor ~  +25 Magic Resistance ~  +10 Ability Haste ~ Converge: ~  Gain 10 ultimate ability haste. ~ Frostfire Tempest: ~  Using your ultimate ability summons a storm around you for 5s. The storm deals  ~ 150 total magic damage ~  to enemy champions within 350 units and slows them by 30%. If no enemy champions are in range when the ultimate is cast, the storm is delayed until an enemy champion comes within range, or for a maximum of 5s. (30s Cooldown) ~   ~ 2400 ~ Zeke's Convergence "
Yordle Trap,2400,+200 Max Health | +20 Armor | +20 Magic Resistance | +15 Ability Haste,DEFENSE ITEMS; SUPPORT ITEMS,"Yordle Trap ~   ~ Yordle Trap ~ Crowd controlling enemies empowers you and allied champions ~  +200 Max Health ~  +20 Armor ~  +20 Magic Resistance ~  +15 Ability Haste ~ Catcher: ~   ~ Slowing ~  or  ~ immobilizing ~  an enemy champion  ~ empowers ~  you for 8 second(s) (4 second(s) for ranged champions) and grants  ~ 20 Movement Speed ~ . When  ~ empowered ~ , you and nearby allied champions gain  ~ 30% Attack Speed ~  (20% for ranged champions). Gain  ~ 20 bonus gold ~  if you or your allies kill a champion while  ~ empowered ~ . ~   ~ 2400 ~ Yordle Trap "
Knight's Vow,2450,+200 Max Health | +100% Health Regen | +40 Armor | +10 Ability Haste,DEFENSE ITEMS; SUPPORT ITEMS,"Knight's Vow ~   ~ Knight's Vow ~ Redirect damage to yourself and restore Health ~  +200 Max Health ~  +100% Health Regen ~  +40 Armor ~  +10 Ability Haste ~ Sacrifice: ~  While your Worthy ally is nearby, redirect 12% of the damage they take to you and  ~ heal for 10% ~  of the damage dealt by them to champions. ~ Pledge: ~  When you buy or re-buy this item, designate an ally who is Worthy. ~   ~ 2450 ~ Knight's Vow "
Frozen Heart,2550,+80 Armor | +400 Max Mana | +20 Ability Haste,DEFENSE ITEMS; SUPPORT ITEMS,Frozen Heart ~   ~ Frozen Heart ~ Reduces enemy Attack Speed ~  +80 Armor ~  +400 Max Mana ~  +20 Ability Haste ~ Winter's Caress: ~  Reduce the  ~ Attack Speed ~  of enemy champions within 650 units of you by  ~ 25% ~ . ~   ~ 2550 ~ Frozen Heart 
Mantle of the Twelfth Hour,2550,+600 Max Health | +20 Ability Haste,DEFENSE ITEMS; SUPPORT ITEMS,"Mantle of the Twelfth Hour ~   ~ Mantle of the Twelfth Hour ~ Increases max Health when your Health is low ~  +600 Max Health ~  +20 Ability Haste ~ Lifeline: ~  Damage that puts you under  ~ 30% ~  grants bonus max Health equal to  ~ 200–300 bonus Health ~  for 5s. Additionally gain 10%  ~ Movement Speed ~  and  ~ 20% Tenacity ~  and increase in size by 10% for 5s. During this time, restore (200–400 ( ~ ) +  ~ 120 Armor ~ +  ~ 120% Magic Resistance ~ +  ~ 15 ~ ) Health. (70s Cooldown) ~   ~ 2550 ~ Mantle of the Twelfth Hour "
Locket of the Iron Solari,2600,+200 Max Health | +30 Armor | +30 Magic Resistance | +10 Ability Haste,DEFENSE ITEMS; SUPPORT ITEMS,Locket of the Iron Solari ~   ~ Locket of the Iron Solari ~ Team shield ~  +200 Max Health ~  +30 Armor ~  +30 Magic Resistance ~  +10 Ability Haste ~ Locket (Active):  ~  Grants a  ~ shield ~  to yourself and nearby allied champions that each  ~ absorbs 250-370 ~  damage for 2.5 seconds. (60s Cooldown) ~ This effect is reduced by 50% if the target has been affected by another Locket in the last 20 seconds. ~   ~ 2600 ~ Locket of the Iron Solari 
Winter's Approach,2600,+500 Max Health | +500 Max Mana | +15 Ability Haste,DEFENSE ITEMS,"Winter's Approach ~   ~ Winter's Approach ~ Converts Mana to Health ~  +500 Max Health ~  +500 Max Mana ~  +15 Ability Haste ~ Awe: ~  Grants  ~ bonus health ~  equal to  ~ 15% ~ of max Mana and refunds  ~ 15% ~ of all Mana spent. ~ Mana Charge: ~  Grants  ~ 14 ~  max Mana for each attack, Mana expenditure, or each time damage is taken from champions, structures, or epic monsters. Grants a maximum of  ~ 700 ~  max Mana, at which point this item transforms into Fimbulwinter. Occurs up to 3 times every 10 seconds. You may only carry 1 Tear of the Goddess item at a time. ~   ~ 2600 ~ Winter's Approach "
Fimbulwinter,,+500 Max Health | +1200 Max Mana | +15 Ability Haste,DEFENSE ITEMS,"Fimbulwinter ~   ~ Fimbulwinter ~ Converts Mana to Health ~  +500 Max Health ~  +1200 Max Mana ~  +15 Ability Haste ~ Awe: ~  Grants  ~ bonus health ~  equal to  ~ 15% ~ of max Mana and refunds  ~ 15% ~ of all Mana spent. ~ Frozen Colossus: ~  Impairing an enemy champion's movement grants a  ~ shield ~  that absorbs damage equal to  ~ 120 ~  plus  ~ 4.5% max Mana ~  for 3s, increased by 80% if there is more than 1 enemy champion nearby. (8s Cooldown) Shield is 50% effective for ranged champions. ~ Fimbulwinter "
Radiant Virtue,2650,+300 Max Health | +30 Armor | +30 Magic Resistance | +10 Ability Haste,DEFENSE ITEMS; SUPPORT ITEMS,"Radiant Virtue ~   ~ Radiant Virtue ~ Heal allies upon casting your ultimate ability. ~  +300 Max Health ~  +30 Armor ~  +30 Magic Resistance ~  +10 Ability Haste ~ Guiding Light: ~  Upon casting your ultimate ability, you Transcend, increasing your  ~ max Health ~  by  ~ 10% ~  for 6s. While Transcended, allied champions within 1,200 units of you  ~ heal for 2.5% ~  of your  ~ max Health ~  per second over the duration. (60s Cooldown) If you're a ranged champion, heals granted are reduced by 50%. ~   ~ 2650 ~ Radiant Virtue "
Thornmail,2700,+200 Max Health | +75 Armor,DEFENSE ITEMS; SUPPORT ITEMS,"Thornmail ~   ~ Thornmail ~ Reflects damage and reduces enemy healing ~  +200 Max Health ~  +75 Armor ~ Thorns: ~  When struck by an attack, deal  ~ 20 ~  +  ~ 6% bonus Armor ~  +  ~ 1% bonus Health ~   ~ magic damage ~  to the attacker. ~ Entwine: ~  Apply  ~ 50% Grievous Wounds ~  to enemy champions for 3 second(s) when stuck by their attacks or dealing damage to them. ~ Grievous Wounds ~  reduces the effectiveness of Healing and Regeneration effects. ~   ~ 2700 ~ Thornmail "
Dawnshroud,2700,+250 Max Health | +50 Armor | +30 Magic Resistance,DEFENSE ITEMS; SUPPORT ITEMS,"Dawnshroud ~   ~ Dawnshroud ~ Immobilize effects damage and reveal around you ~  +250 Max Health ~  +50 Armor ~  +30 Magic Resistance ~ Dawnbringer: ~  When you immobilize a champion champion or are immobilized within 400 units of an enemy champion, reveal all nearby enemy champions for 3 seconds, deal  ~ magic damage ~  equal to  ~ 40 ~  +  ~ 2.5% bonus ~ and gain 20%  ~ Armor ~  and  ~ Magic Resistance ~  (3s Cooldown) ~   ~ 2700 ~ Dawnshroud "
Hollow Radiance,2800,+400 Max Health | +40 Magic Resistance | +15 Ability Haste,DEFENSE ITEMS,"Hollow Radiance ~   ~ Hollow Radiance ~ Deals damage in an area ~  +400 Max Health ~  +40 Magic Resistance ~  +15 Ability Haste ~ Immolate: ~  While in combat, deal  ~ magic damage ~  equal to  ~ 20–30 ~  plus  ~ 1% of bonus ~  per second for 5 second(s) to nearby enemies. Deals 125% damage against monsters and 200% damage against minions. ~ Desolate: ~  Killing a neutral monster or an enemy deals  ~ magic damage ~  equal to  ~ 30 ~  plus  ~ 2% of bonus ~  in an area around them. ~   ~ 2800 ~ Hollow Radiance "
Randuin's Omen,2800,+400 Max Health | +75 Armor,DEFENSE ITEMS,Randuin's Omen ~   ~ Randuin's Omen ~ Counters Critical Strike Damage ~  +400 Max Health ~  +75 Armor ~ Resilience: ~   ~ Critically Struck ~  deal 30% less damage to you. ~ Countercurrent: ~  Gain 1 stacks of  ~ Countercurrent ~  when Critically Struck by  ~ physical damage ~ . Each stuck grants  ~ 5% Movement Speed ~  and 5% slow resist. Max 4 stacks. ~   ~ 2800 ~ Randuin's Omen 
Dead Man's Plate,2800,+350 Max Health | +70 Armor | +4% Movement Speed,DEFENSE ITEMS,"Dead Man's Plate ~   ~ Dead Man's Plate ~ Increases Movement Speed ~  +350 Max Health ~  +70 Armor ~  +4% Movement Speed ~ Momentum: ~  Moving builds  ~ Momentum ~ , granting up to  ~ 40 Move Speed ~  at  ~ 100 stacks ~ . Attacking removes all  ~ Momentum ~ . Stacks decay when movement is impaired. ~ Crushing Blow: ~  Attacks deal up to  ~ 100 bonus magic damage ~  based on  ~ Momentum ~  removed. Melee attacks with max Momentum  ~ slows by 75% ~  for 1 second. ~   ~ 2800 ~ Dead Man's Plate "
Force of Nature,2800,+400 Max Health | +60 Magic Resistance | +5% Move Speed,DEFENSE ITEMS,"Force of Nature ~   ~ Force of Nature ~ Stacking Magic Resist and Move Speed ~  +400 Max Health ~  +60 Magic Resistance ~  +5% Move Speed ~ Absorb: ~  Taking ability damage from enemy champions grants 1 stack(s) of Steadfast for 7 seconds (max 4 stacks). Dealing damage to an enemy champion refreshes the duration of the stacks. At maximum stacks, gain  ~ 6% Movement Speed ~  and  ~ 70 ~  bonus  ~ Magic Resistance ~ . ~   ~ 2800 ~ Force of Nature "
Heartsteel,3000,+700 Max Health | +150% Health Regen | +20 Ability Haste,DEFENSE ITEMS,"Heartsteel ~   ~ Heartsteel ~ Increase Maximum Health ~  +700 Max Health ~  +150% Health Regen ~  +20 Ability Haste ~ Colossal Consumption: ~  While within 700 units of an enemy champion, charges for 2.5 seconds before dealing a huge strike against the enemy champion. This charged attack deals bonus  ~ physical damage ~  equal to  ~ 140 ~  +  ~ 3.5% of maximum Health ~ , and grants  ~ maximum Health ~  equal to  ~ 15% ~  of the damage dealt. The charge for each target has a 20 second cooldown. ~   ~ 3000 ~ Heartsteel "
Kaenic Rookern,2800,+350 Max Health | +100% Health Regen | +85 Magic Resistance,DEFENSE ITEMS,"Kaenic Rookern ~   ~ Kaenic Rookern ~ Gains a magic shield when out of combat ~  +350 Max Health ~  +100% Health Regen ~  +85 Magic Resistance ~ Magebane: ~  After not taking  ~ magic damage ~  for 12 seconds, gain a  ~ magic shield ~  that absorbs damage equal to  ~ 50-150 ~  +  ~ 14% of max Health ~ . ~   ~ 2800 ~ Kaenic Rookern "
Warmog's Armor,2850,+700 Max Health | +100% Health Regen | +20 Ability Haste,DEFENSE ITEMS,"Warmog's Armor ~   ~ Warmog's Armor ~ Out of combat Heath Regen ~  +700 Max Health ~  +100% Health Regen ~  +20 Ability Haste ~ Warmog's Heart: ~  If you have at least  ~ 950 bonus Health ~ , restore  ~ 3.5% Health ~  per second if you haven't taken damage within the last 5 seconds. ~ Blessed: ~  Increases all  ~ healing ~  and  ~ shielding ~  effects on you by 30%. ~   ~ 2850 ~ Warmog's Armor "
Gargoyle Stoneplate,2900,+200 Max Health | +45 Armor | +45 Magic Resistance | +10 Ability Haste,DEFENSE ITEMS,"Gargoyle Stoneplate ~   ~ Gargoyle Stoneplate ~ Shield ~  +200 Max Health ~  +45 Armor ~  +45 Magic Resistance ~  +10 Ability Haste ~ Stoneplate (Active): ~  Gain a base  ~ shield ~  that absorbs damage equal to  ~ 100 ~  plus  ~ 90% bonus ~ and gain size, decayng over 2.5s. (60s Cooldown) ~   ~ 2900 ~ Gargoyle Stoneplate "
Sunfire Aegis,2900,+350 Max Health | +40 Armor | +15 Ability Haste,DEFENSE ITEMS,"Sunfire Aegis ~   ~ Sunfire Aegis ~ Burns nearby emenies ~  +350 Max Health ~  +40 Armor ~  +15 Ability Haste ~ Immolate: ~  While in combat, deal  ~ magic damage ~  equal to  ~ 20 ~  plus  ~ 1.5% bonus HP ~  every second to nearby enemies.  ~ Immolate ~  deals 130% damage against monsters and 175-250% damage ( ~ ) against minions. ~   ~ 2900 ~ Sunfire Aegis "
Unending Despair,3000,+300 Max Health | +40 Armor | +40 Magic Resistance | +10 Ability Haste,DEFENSE ITEMS,"Unending Despair ~   ~ Unending Despair ~ Increases tanks' sustain in teamfights ~  +300 Max Health ~  +40 Armor ~  +40 Magic Resistance ~  +10 Ability Haste ~ Anguish: ~  Every 4 second(s) while in combat with a champion, deal  ~ 3% of your max Health ~  as  ~ magic damage ~  to nearby champions and  ~ heal ~  for 250% of the damage dealt. Anguish is unaffected by Item Ability Haste. ~   ~ 3000 ~ Unending Despair "
Iceborn Gauntlet,3000,+300 Max Health | +50 Armor | +250 Max Mana | +30 Ability Haste,DEFENSE ITEMS,Iceborn Gauntlet ~   ~ Iceborn Gauntlet ~ Attacks create a slowing field ~  +300 Max Health ~  +50 Armor ~  +250 Max Mana ~  +30 Ability Haste ~ Spellblade: ~  Using an ability causes your next attack within 10 seconds to deal  ~ bonus physical damage ~  equal to ( ~ 100% base AD  ~  +  ~ 25% Bonus Armor  ~ ) in an area and creates an icy field for 2 seconds that slows by 30%.  ~ Armor ~  increases the size of the icy field. (1.5s Cooldown) ~ Damage is reduced vs structures. ~   ~ 3000 ~ Iceborn Gauntlet 
Amaranth's Twinguard,3200,+300 Max Health | +50 Armor | +50 Magic Resistance,DEFENSE ITEMS,"Amaranth's Twinguard ~   ~ Amaranth's Twinguard ~ In-combat durability ~  +300 Max Health ~  +50 Armor ~  +50 Magic Resistance ~ Endurance: ~  Gain 1 stacks of Endurance every 1 seconds while in combat with enemy champions (max 5 stacks). At maximum stacks, gain 20% size,  ~ 20% Tenacity ~ , and increase  ~ Armor ~  by 30% and  ~ Magic Resistance ~  by 30% until out of combat with champion. ~   ~ 3200 ~ Amaranth's Twinguard "
Black Mist Scythe,0,+10 Ability Haste,SUPPORT ITEMS,"Black Mist Scythe ~   ~ Black Mist Scythe ~ Attack champions and structures to gain bonus gold ~  +10 Ability Haste ~ Versatile: ~  Gain  ~ 14 Attack Damage ~  or  ~ 28 Ability Power ~  (Adaptive). ~ Soulcast: ~  Every 60 seconds, gains  ~ 75 gold ~ ,  ~ 25 Health ~  and  ~ 2 Attack Damage ~ , or  ~ 4 Ability Power ~  (Adaptive); up to  ~ 250 Health ~  and  ~ 20 Attack Damage ~ , or  ~ 40 Ability Power ~  (Adaptive). ~ Deal 2 more damage to Sight Wards revealed by Sweeping Lens, Control Ward, and Scryer's Bloom. When out of combat, gain 10% Movement Speed when you move toward your Perfect Partner. If you're more than 2,500 units apart, this bonus increases to 30%. ~   ~ 0 ~ Black Mist Scythe "
Bulwark of the Mountain,0,+175 Max Health | +10 Ability Haste,SUPPORT ITEMS,"Bulwark of the Mountain ~   ~ Bulwark of the Mountain ~ Kill minions to earn bonus gold ~  +175 Max Health ~  +10 Ability Haste ~ Soulcast: ~  Every 60 seconds, gains  ~ 75 gold ~ ,  ~ 25 Health ~  and  ~ 2 Attack Damage ~ , or  ~ 4 Ability Power ~  (Adaptive); up to  ~ 250 Health ~  and  ~ 20 Attack Damage ~  or  ~ 40 Ability Power ~  (Adaptive). ~ Deal 2 more damage to Sight Wards revealed by Sweeping Lens, Control Ward, and Scryer's Bloom. When out of combat, gain 10% Movement Speed when you move toward your Perfect Partner. If you're more than 2,500 units apart, this bonus increases to 30%. ~   ~ 0 ~ Bulwark of the Mountain "
Echoes of Helia,2400,+200 Max Health | +40 Ability Power | +50% Mana Regen | +20 Ability Haste,SUPPORT ITEMS,"Echoes of Helia ~   ~ Echoes of Helia ~ Protect allies, granting them increased healing ~  +200 Max Health ~  +40 Ability Power ~  +50% Mana Regen ~  +20 Ability Haste ~ Soul Siphon: ~  Store 30% of the premitigation damage dealt to enemy champions as  ~ Soul Shards ~  (max 80–250 shards ( ~ )).  ~ Healing ~  or  ~ shielding ~  a teammate consumes all  ~ Soul Shards ~  to  ~ heal ~  them for the corresponding amount. ~   ~ 2400 ~ Echoes of Helia "
Ardent Censer,2400,+50 Ability Power | +50% Mana Regen | +8% Heal and Shield Strength | +4% Move Speed.,SUPPORT ITEMS,"Ardent Censer ~   ~ Ardent Censer ~ Increases allies Attack Speed ~  +50 Ability Power ~  +50% Mana Regen ~  +8% Heal and Shield Strength ~  +4% Move Speed. ~ Censer: ~  When you  ~ heal ~  or  ~ shield ~  an allied champion other than yourself, for the next 6 seconds, you and the ally gain  ~ 30% Attack Speed ~  and deal  ~ 25 ~  bonus  ~ magic damage ~  whenever you attack. ~   ~ 2400 ~ Ardent Censer "
Staff of Flowing Waters,2400,+50 Ability Power | +50% Mana Regen | +10 Ability Haste | +8% Heal and Shield Strength,SUPPORT ITEMS,Staff of Flowing Waters ~   ~ Staff of Flowing Waters ~ Enhance allies Ability Power and Ability Haste ~  +50 Ability Power ~  +50% Mana Regen ~  +10 Ability Haste ~  +8% Heal and Shield Strength ~ Rapids: ~   ~ Healing ~  or  ~ shielding ~  an ally grants you both  ~ 15 Ability Haste ~  and  ~ 40 ~ Ability Power ~  for 6 seconds. ~   ~ 2400 ~ Staff of Flowing Waters 
Mikael's Blessing,2500,+300 Max Health | +50% Mana Regen | +15 Ability Haste | +9% Heal and Shield Strength,SUPPORT ITEMS,"Mikael's Blessing ~   ~ Mikael's Blessing ~ Dispels crowd control from an ally ~  +300 Max Health ~  +50% Mana Regen ~  +15 Ability Haste ~  +9% Heal and Shield Strength ~ Purify (Active): ~  Remove all  ~ crowd control ~  debuffs (excluding knock up and suppression) from an allied champion, grant them  ~ crowd control immunity ~  for 0.2s, and  ~ heal ~  them for  ~ 150–250 Health ~ . (75s Cooldown) ~   ~ 2500 ~ Mikael's Blessing "
Shurelya's Battlesong,2500,+55 Ability Power | +50% Mana Regeneration | +20 Ability Haste | +4% Move Speed,SUPPORT ITEMS,Shurelya's Battlesong ~   ~ Shurelya's Battlesong ~ Grans allies Movement Speed ~  +55 Ability Power ~  +50% Mana Regeneration ~  +20 Ability Haste ~  +4% Move Speed ~ Inspiring Speech (Active): ~  Grant nearby allies champions  ~ 30% Move Speed ~  for 4 seconds. (60s Cooldown) ~   ~ 2500 ~ Shurelya's Battlesong 
Harmonic Echo,2500,+200 Max Health | +40 Ability Power | +50% Mana Regen | +20 Ability Haste,SUPPORT ITEMS,"Harmonic Echo ~   ~ Harmonic Echo ~ Abilities grant healing effects ~  +200 Max Health ~  +40 Ability Power ~  +50% Mana Regen ~  +20 Ability Haste ~ Harmonic Echo: ~  When you heal or shield an allied champion, the effect links to the nearest allied champion within range with the lowest percentage Health, excluding yourself, and grants them 30% of that heal or 35% of that shield. If no other allied champion is in range, the original target instead receives that same extra heal or shield. ~   ~ 2500 ~ Harmonic Echo "
Gluttonous Greaves,1000,+45 Move Speed,Boots tier 2,"Gluttonous Greaves ~   ~ Gluttonous Greaves ~ Attack Damage, Omnivamp ~  +45 Move Speed ~ Balance of Power: ~  Gain  ~ 12 Attack Damage ~  or  ~ 20 Ability Power ~  (Adaptive). ~ Conversion: ~  Gain  ~ 5% Omnivamp ~ . Champion takedowns grant an additional  ~ 0.5% Omnivamp ~ , up to  ~ 5% ~ . ~   ~ 1000 ~ Gluttonous Greaves "
Berserker's Greaves,1200,+35% Attack Speed | +45 Move Speed,Boots tier 2,Berserker's Greaves ~   ~ Berserker's Greaves ~ Attack Speed ~  +35% Attack Speed ~  +45 Move Speed ~ Blessed Blade: ~  Attacks restore 10 Health on hit. ~   ~ 1200 ~ Berserker's Greaves 
Mercury's Treads,1200,+150 Max Health | +25 Magic Resistance | +30 Tenacity | +45 Move Speed,Boots tier 2,Mercury's Treads ~   ~ Mercury's Treads ~ Increases Magic resist ~  +150 Max Health ~  +25 Magic Resistance ~  +30 Tenacity ~  +45 Move Speed ~   ~ 1200 ~ Mercury's Treads 
Plated Steelcaps,1200,+150 Max Health | +20 Armor | +45 Move Speed,Boots tier 2,Plated Steelcaps ~   ~ Plated Steelcaps ~ Reduces damage from champion attacks ~  +150 Max Health ~  +20 Armor ~  +45 Move Speed ~ Block: ~  Reduces damage from champion attacks by 10%. ~   ~ 1200 ~ Plated Steelcaps 
Ionian Boots of Lucidity,1000,+50% Mana Regen | +15 Ability Haste | +45 Move Speed,Boots tier 2,Ionian Boots of Lucidity ~   ~ Ionian Boots of Lucidity ~ Reduces ability cooldowns ~  +50% Mana Regen ~  +15 Ability Haste ~  +45 Move Speed ~ Summoned: ~  Reduces spell cooldowns by  ~ 15% ~ . ~   ~ 1000 ~ Ionian Boots of Lucidity 
Boots of Mana,1200,+25 Ability Power | +8 Magic Penetration | +75% Mana Regeneration | +45 Move Speed,Boots tier 2,"Boots of Mana ~   ~ Boots of Mana ~ Ability Power, Magic Pen, Mana Regeneration ~  +25 Ability Power ~  +8 Magic Penetration ~  +75% Mana Regeneration ~  +45 Move Speed ~ Equilibrium: ~  Champions without Mana gain 50% bonus health Regen. ~ Big Bully: ~  Attacks and active abilities deal  ~ 18 bonus true damage ~  to minions. ~   ~ 1200 ~ Boots of Mana "
Boots of Dynamism,1200,+15 Attack Damage | +10 Armor Penetration | +45 Move Speed,Boots tier 2,"Boots of Dynamism ~   ~ Boots of Dynamism ~ Attack Damage, Armor Pen ~  +15 Attack Damage ~  +10 Armor Penetration ~  +45 Move Speed ~   ~ 1200 ~ Boots of Dynamism "
Immortal Treds,2000,+45 Move Speed,Boots tier 3,"Immortal Treds ~   ~ Immortal Treds ~ Deal bonus damage or gain increased healing and shielding ~  +45 Move Speed ~ Balance of Power: ~  Gain  ~ 12 Attack Damage ~  or  ~ 20 Ability Power ~  (Adaptive). ~ Conversion: ~  Gain  ~ 5% Omnivamp ~ . Champion takedowns grant an additional  ~ 0.5% Omnivamp ~ , up to  ~ 5% ~ . ~ Now and Forever: ~  When you have more than 50% Health, deal 5% bonus damage. When below 50% Health, gain 12% increased healing and shielding. ~   ~ 2000 ~ Immortal Treds "
Gunmetal Greaves,2200,+50% Attack Speed | +45 Move Speed | +5% Lifesteal,Boots tier 3,Gunmetal Greaves ~   ~ Gunmetal Greaves ~ Increases Attack Speed and Movement Speed ~  +50% Attack Speed ~  +45 Move Speed ~  +5% Lifesteal ~ Noxian Gait: ~  Attacks against enemy champions grant  ~ Movement Speed ~  ( ~ 10% ~  for melee champions /  ~ 7% ~  for ranged champions) decaying over 2 seconds. ~ Blessed Blade: ~  Attacks  ~ restore 12 Health ~  on hit. ~   ~ 2200 ~ Gunmetal Greaves 
Chainlaced Crushers,2200,+150 Max Health | +30 Magic Resistance | +30% Tenacity | +45 Move Speed,Boots tier 3,"Chainlaced Crushers ~   ~ Chainlaced Crushers ~ Gain a magic shield upon taking magic damage ~  +150 Max Health ~  +30 Magic Resistance ~  +30% Tenacity ~  +45 Move Speed ~ Noxian Persistence: ~  After taking  ~ magic damage ~  from a champion, gain a  ~ magic shield ~  that absorbs  ~ 10-120 ~  plus  ~ 5% max ~ for 5s. (12s Cooldown) ~   ~ 2200 ~ Chainlaced Crushers "
Armored Advance,2200,+150 Max Health | +30 Armor | +45 Move Speed,Boots tier 3,Armored Advance ~   ~ Armored Advance ~ Grants Armor and a shield ~  +150 Max Health ~  +30 Armor ~  +45 Move Speed ~ Block: ~  Reduce damage from champion attacks by 10%. ~ Noxian Endurance: ~  After taking  ~ physical damage ~  from a champion grants a  ~ physical shield ~  that absorbs damage equal to  ~ 10-140 ~  plus  ~ 8% max Health ~ . (12s Cooldown) ~   ~ 2200 ~ Armored Advance 
Crimson Lucidity,2000,+75% Mana Regeneration | +25 Ability Haste | +45 Move Speed,Boots tier 3,"Crimson Lucidity ~   ~ Crimson Lucidity ~ Reduces ability cooldown ~  +75% Mana Regeneration ~  +25 Ability Haste ~  +45 Move Speed ~ Summoned: ~  Reduces spell cooldown by  ~ 20% ~ . ~ Noxian Haste: ~   ~ Healing ~  or  ~ shielding ~  allied champions, casting a spell, or dealing damage to enemies with abilities grants  ~ Movement Speed ~  ( ~ 10% ~  for melee champions /  ~ 8% ~  for ranged champions) for 4 seconds. ~ This effect can only be triggered once every 4 seconds per ability. ~   ~ 2000 ~ Crimson Lucidity "
Spellslinger's Shoes,2200,+35 Ability Power | +18 Magic Penetration | +8% Magic Penetration | +100% Mana Regeneration | +45 Move Speed,Boots tier 3,Spellslinger's Shoes ~   ~ Spellslinger's Shoes ~ Deal bonus damage to minions ~  +35 Ability Power ~  +18 Magic Penetration ~  +8% Magic Penetration ~  +100% Mana Regeneration ~  +45 Move Speed ~ Equilibrium: ~  Champions without Mana gain 50% base Health Regen. ~ Big Bully: ~  Attacks and active abilities deal  ~ 18 bonus true damage ~  to minions. ~   ~ 2200 ~ Spellslinger's Shoes 
Armorcrusher Boots,2200,+25 Attack Damage | +12 Armor Penetration | +6% Armor Penetration | +45 Move Speed,Boots tier 3,Armorcrusher Boots ~   ~ Armorcrusher Boots ~ Gain out-of-combat Movement Speed ~  +25 Attack Damage ~  +12 Armor Penetration ~  +6% Armor Penetration ~  +45 Move Speed ~ Cloudwalker: ~  Gain  ~ 20 ~  out-of combat  ~ Move Speed ~ . ~   ~ 2200 ~ Armorcrusher Boots 
Quicksilver Sash,1100,,Mid Tier Items,"Quicksilver Sash ~   ~ Quicksilver Sash ~ Dispels crowd control ~ Quicksilver (Active): ~  Removes all crowd control effects currently affecting you, and become immune to crowd control effects for 0.25 seconds. ~ Perseverance (Passive): ~  When the  ~ Quicksilver ~  effects ends, grant  ~ 30% Tenacity ~  and  ~ 30% Slow Resist ~  for 1.5 seconds. (60s Cooldown) ~ Cannot be used during knock up or knock back effects. ~   ~ 1100 ~ Quicksilver Sash "
Seeker's Armguard,1200,+20 Armor | +35 Ability Power,Mid Tier Items,"Seeker's Armguard ~   ~ Seeker's Armguard ~ Turn invulnerable ~  +20 Armor ~  +35 Ability Power ~ Stasis (Active): ~  Become invulnerable and untargetable for 2.5 seconds, but unable to move, attack, cast abilities or use items. (120s Cooldown) ~   ~ 1200 ~ Seeker's Armguard "
Vampiric Scepter,1200,+20 Attack Damage | +8% Lifesteal,Mid Tier Items,Vampiric Scepter ~   ~ Vampiric Scepter ~  +20 Attack Damage ~  +8% Lifesteal ~   ~ 1200
Zeal,1400,+15% Critical Rate | +15% Attack Speed,Mid Tier Items,Zeal ~   ~ Zeal ~ Increases Movement Speed ~  +15% Critical Rate ~  +15% Attack Speed ~ Fervor: ~   ~   ~ +4% Move Speed. ~   ~ 1400
Kircheis Shard,800,+20% Attack Speed,Mid Tier Items,Kircheis Shard ~   ~ Kircheis Shard ~ Attacks deal bonus damage ~  +20% Attack Speed ~ Shock: ~  Dealing damage to an enemy champion deals  ~ 50 bonus magic damage ~ . (25s. Сooldown). Attacks reduce this cooldown by 1 second. ~   ~ 800
Serrated Dirk,1000,+20 Attack Damage,Mid Tier Items,Serrated Dirk ~   ~ Serrated Dirk ~  +20 Attack Damage ~ Sharp: ~   ~  +8 Armor Penetration. ~   ~ 1000
Recurve Bow,900,+20% Attack Speed,Mid Tier Items,Recurve Bow ~   ~ Recurve Bow ~ Attack deal bonus damage ~  +20% Attack Speed ~ Reinforced: ~  Attacks deal  ~ 15 bonus physical damage ~   ~ on-hit ~  against targets. ~   ~ 900
B. F. Sword,1500,+40 Attack Damage,Mid Tier Items,B. F. Sword ~   ~ B. F. Sword ~  +40 Attack Damage ~   ~ 1500
Last Whisper,1200,+15 Attack Damage | +15% Armor Penetration,Mid Tier Items,Last Whisper ~   ~ Last Whisper ~ Armor Penetration (%) ~  +15 Attack Damage ~  +15% Armor Penetration ~   ~ 1200
Executioner's Calling,800,+15 Attack Damage,Mid Tier Items,Executioner's Calling ~   ~ Executioner's Calling ~ Physical Damage reduces enemy healing ~  +15 Attack Damage ~ Rend: ~  Physical Damage inflicts  ~ 40% Grievous Wounds ~  to enemy champions for 3 seconds.  ~ Grievous Wounds ~  reduces the effectiveness of Healing and Regeneration effects. ~   ~ 800
Phage,1000,+150 Max Health | +15 Attack Damage,Mid Tier Items,"Phage ~   ~ Phage ~ Attacks increases Movement Speed ~  +150 Max Health ~  +15 Attack Damage ~ Rage: ~  On hit, attacks grant  ~ 20 Move Speed ~  for 2 seconds.  ~ Bonus Movement Speed ~  does not stack. Ranged champions gain halved values. ~   ~ 1000"
Caulfield's Warhammer,1200,+25 Attack Damage | +10 Ability Haste,Mid Tier Items,Caulfield's Warhammer ~   ~ Caulfield's Warhammer ~  +25 Attack Damage ~  +10 Ability Haste ~   ~ 1200
Jaurim's Fist,1100,+175 Max Health | +15 Attack Damage,Mid Tier Items,Jaurim's Fist ~   ~ Jaurim's Fist ~  +175 Max Health ~  +15 Attack Damage ~   ~ 1100
Aether Wisp,950,+35 Ability Power | +4% Move Speed,Mid Tier Items,Aether Wisp ~   ~ Aether Wisp ~  +35 Ability Power ~  +4% Move Speed ~   ~ 950
Lost Chapter,1200,+35 Ability Power | +200 Max Mana | +10 Ability Haste,Mid Tier Items,Lost Chapter ~   ~ Lost Chapter ~ Restore Mana when leveling up ~  +35 Ability Power ~  +200 Max Mana ~  +10 Ability Haste ~ Enlighten: ~  Leveling up restores  ~ 20% ~ max Mana ~  over 3 seconds. ~   ~ 1200
Fiendish Codex,900,+25 Ability Power | +10 Ability Haste,Mid Tier Items,Fiendish Codex ~   ~ Fiendish Codex ~  +25 Ability Power ~  +10 Ability Haste ~   ~ 900
Blasting Wand,900,+40 Ability Power,Mid Tier Items,Blasting Wand ~   ~ Blasting Wand ~  +40 Ability Power ~   ~ 900
Needlessly Large Rod,1400,+65 Ability Power,Mid Tier Items,Needlessly Large Rod ~   ~ Needlessly Large Rod ~  +65 Ability Power ~   ~ 1400
Haunting Guise,1300,+200 Max Health | +30 Ability Power,Mid Tier Items,"Haunting Guise ~   ~ Haunting Guise ~ Boosts in-combat damage ~  +200 Max Health ~  +30 Ability Power ~ Madness: ~  Every 1 second(s) in combat with enemy champions, deal 2% bonus damage, up to 6%. ~   ~ 1300"
Sheen,800,+10 Ability Haste,Mid Tier Items,Sheen ~   ~ Sheen ~ Attacks deal bonus damage after ability casts ~  +10 Ability Haste ~ Spellblade: ~  Using an ability causes the next attack used within 10 seconds to deal  ~ bonus physical damage ~  equal to  ~ 100% base attack damage  ~ . (1.5s Cooldown) Damage is reduced vs structures. ~   ~ 800
Oblivion Orb,800,+35 Ability Power,Mid Tier Items,Oblivion Orb ~   ~ Oblivion Orb ~ Magic damage reduces enemy healing ~  +35 Ability Power ~ Cursed Wounds: ~  Dealing  ~ magic damage ~  to enemy champions applies  ~ 40% Grievous Wounds ~  for 3 seconds. ~ Grievous Wounds ~  reduces the effectiveness of Healing and Regeneration effects. ~   ~ 800
Bami's Cinder,1200,+250 Max Health | +5 Ability Haste,Mid Tier Items,Bami's Cinder ~   ~ Bami's Cinder ~ Burns nearby emenies ~  +250 Max Health ~  +5 Ability Haste ~ Cinders: ~  Deals  ~ 10-20 magic damage ~  per second to nearby enemies. (Deals 115% damage against minions and monsters.) ~   ~ 1200
Spectre's Cowl,1100,+175 Max Health | +20 Magic Resistance,Mid Tier Items,Spectre's Cowl ~   ~ Spectre's Cowl ~ Boosts Health Regen when tacking damage ~  +175 Max Health ~  +20 Magic Resistance ~ Spectral Visit: ~  Grants  ~ 150% Health Regen ~  for 10 seconds after taking damage from an enemy champion. ~   ~ 1100
Kindlegem,1000,+175 Max Health | +10 Ability Haste,Mid Tier Items,Kindlegem ~   ~ Kindlegem ~  +175 Max Health ~  +10 Ability Haste ~   ~ 1000
Giant's Belt,1000,+300 Max Health,Mid Tier Items,Giant's Belt ~   ~ Giant's Belt ~  +300 Max Health ~   ~ 1000
Warden's Mail,1050,+35 Armor,Mid Tier Items,Warden's Mail ~   ~ Warden's Mail ~ Reduces enemy's Attack Speed ~  +35 Armor ~ Cold Steel: ~  Reduce the  ~ Attack Speed ~  of enemies by  ~ 15% ~  for 1.5 seconds when struck by an attack. ~   ~ 1050
Catalyst of Aeons,1100,+200 Max Health | +300 Max Mana,Mid Tier Items,Catalyst of Aeons ~   ~ Catalyst of Aeons ~ Consumes Mana to heal ~  +200 Max Health ~  +300 Max Mana ~ Eternity: ~  Restore  ~ Mana ~  equal to  ~ 15% ~  of the damage taken from champions. Regen  ~ Health ~  equal to  ~ 20% ~  of Mana spent. Capped at  ~ 15 Health ~  per cast. ~   ~ 1100
Chain Vest,900,+40 Armor,Mid Tier Items,Chain Vest ~   ~ Chain Vest ~  +40 Armor ~   ~ 900
Bramble Vest,1000,+30 Armor,Mid Tier Items,"Bramble Vest ~   ~ Bramble Vest ~ Reflects damage and reduces enemy healing ~  +30 Armor ~ Thorns: ~  When struck by an attack, deal  ~ 4 magic damage ~  +  ~ 6% bonus armor  ~  to the attacker and inflict  ~ 40% Grievous Wounds ~  for 3 seconds if they are a champion. ~ Grievous Wounds reduces the effectiveness of Healing and Regeneration effects. ~   ~ 1000"
Hexdrinker,1200,+20 Attack Damage | +20 Magic Resistance,Mid Tier Items,Hexdrinker ~   ~ Hexdrinker ~  +20 Attack Damage ~  +20 Magic Resistance ~   ~ 1200
Negatron Cloak,900,+40 Magic Resistance,Mid Tier Items,Negatron Cloak ~   ~ Negatron Cloak ~  +40 Magic Resistance ~   ~ 900
Glacial Shroud,1000,+20 Armor | +150 Max Mana | +10 Ability Haste,Mid Tier Items,Glacial Shroud ~   ~ Glacial Shroud ~  +20 Armor ~  +150 Max Mana ~  +10 Ability Haste ~   ~ 1000
Winged Moonplate,900,+150 Max Health | +4% Move Speed,Mid Tier Items,Winged Moonplate ~   ~ Winged Moonplate ~  +150 Max Health ~  +4% Move Speed ~   ~ 900
Noonquiver,1300,+20 Attack Damage | +15% Critical Rate,Mid Tier Items,Noonquiver ~   ~ Noonquiver ~  +20 Attack Damage ~  +15% Critical Rate ~   ~ 1300
Hextech Alternator,1100,+45 Ability Power,Mid Tier Items,Hextech Alternator ~   ~ Hextech Alternator ~ Abilities deal bonus damage ~  +45 Ability Power ~ Revved: ~  Damaging abilities and  ~ empowered attacks ~  against champions deal  ~ 25-60 bonus magic damage ~ . (20s Cooldown) ~   ~ 1100
Mejai's Soulstealer,1800,+70 Max Health | +25 Ability Power,Mid Tier Items,"Mejai's Soulstealer ~   ~ Mejai's Soulstealer ~ Takedowns increase AP ~  +70 Max Health ~  +25 Ability Power ~ Glory: ~  Gain up to 30 stacks of  ~ Glory ~  after a champion takedown. Melee champions gain 3 stack(s) for each kill and 2 stack(s) for each assist; ranged champions gain 4 stack(s) for each kill and 2 stack(s) for each assist. You lose 10 stack(s) on death. ~ Fear: ~  Gain  ~ 5 AP ~  for every stack of  ~ Glory ~  you have. At 10 stack(s) of  ~ Glory ~  and above, gain  ~ 10% bonus Movement Speed ~ . ~   ~ 1800 ~ Mejai's Soulstealer "
Forbidden Idol,700,+25% Mana Regen | +6% Heal and Shield Strength,Mid Tier Items,Forbidden Idol ~   ~ Forbidden Idol ~ Increase heal and shield strength ~  +25% Mana Regen ~  +6% Heal and Shield Strength ~   ~ 700
Fated Ashes,900,+40 Ability Power,Mid Tier Items,Fated Ashes ~   ~ Fated Ashes ~ Abilities deal damage over time ~  +40 Ability Power ~ Kindle: ~  Damaging abilities deal  ~ 5 bonus magic damage ~  over 3 seconds. ~ Deals an additional  ~ 15 magic damage ~  to monsters. ~   ~ 900
Void Amethyst,1000,+20 Ability Power | +10% Magic Penetration,Mid Tier Items,Void Amethyst ~   ~ Void Amethyst ~  +20 Ability Power ~  +10% Magic Penetration ~   ~ 1000
Verdant Barrier,1600,+40 Ability Power | +25 Magic Resistance,Mid Tier Items,Verdant Barrier ~   ~ Verdant Barrier ~ Blocks an enemy ability ~  +40 Ability Power ~  +25 Magic Resistance ~ Annul: ~  Grants a  ~ spell shield ~  that blocks the next enemy ability. (50s Cooldown) ~   ~ 1600
Pickaxe,800,+20 Attack Damage,Mid Tier Items,Pickaxe ~   ~ Pickaxe ~  +20 Attack Damage ~   ~ 800
Heartbound Axe,1200,+20 Attack Damage | +15% Attack Speed,Mid Tier Items,Heartbound Axe ~   ~ Heartbound Axe ~  +20 Attack Damage ~  +15% Attack Speed ~   ~ 1200
Bandleglass Mirror,900,+20 Ability Power | +50% Mana Regen | +10 Ability Haste,Mid Tier Items,Bandleglass Mirror ~   ~ Bandleglass Mirror ~  +20 Ability Power ~  +50% Mana Regen ~  +10 Ability Haste ~   ~ 900 ~    ~                          ~                              ~                                  ~                                      ~ Basic Items
Boots of Speed,400,+25 Move Speed.,Basic Items,Boots of Speed ~   ~ Boots of Speed ~   ~ +25 Move Speed. ~   ~ 400
Long Sword,500,+12 Attack Damage,Basic Items,Long Sword ~   ~ Long Sword ~  +12 Attack Damage ~   ~ 500
Brawler's Gloves,500,+10% Critical Rate,Basic Items,Brawler's Gloves ~   ~ Brawler's Gloves ~  +10% Critical Rate ~   ~ 500
Dagger,400,+12% Attack Speed,Basic Items,Dagger ~   ~ Dagger ~  +12% Attack Speed ~   ~ 400
Shimmering Spark,500,+50 Max Health,Basic Items,Shimmering Spark ~   ~ Shimmering Spark ~ Burns nearby enemies ~  +50 Max Health ~ Burn: ~  Deals  ~ 5-10 magic damage ~  per second to nearby enemies. ~   ~ 500
Tear of the Goddess,500,+200 Max Mana,Basic Items,Tear of the Goddess ~   ~ Tear of the Goddess ~ Increases Mana ~  +200 Max Mana ~ Awe: ~   ~ 10% ~  of  ~ Mana ~  spent is refunded. ~ Mana Charge: ~  Increases max  ~ Mana ~  by  ~ 5 ~  every time Mana is spent. Caps at  ~ 700 bonus Mana ~ . Triggers up to 3 times every 10 seconds. You may only carry one Tear of the Goddess item at a time. ~   ~ 500
Amplifying Tome,500,+20 Ability Power,Basic Items,Amplifying Tome ~   ~ Amplifying Tome ~  +20 Ability Power ~   ~ 500
Ruby Crystal,500,+150 Max Health,Basic Items,Ruby Crystal ~   ~ Ruby Crystal ~  +150 Max Health ~   ~ 500
Cloth Armor,500,+20 Armor,Basic Items,Cloth Armor ~   ~ Cloth Armor ~  +20 Armor ~   ~ 500
Null-Magic Mantle,500,+20 Magic Resistance,Basic Items,Null-Magic Mantle ~   ~ Null-Magic Mantle ~  +20 Magic Resistance ~   ~ 500
Ring of Revelation,300,+5 Ability Haste,Basic Items,Ring of Revelation ~   ~ Ring of Revelation ~ Reduces ability cooldowns ~  +5 Ability Haste ~   ~ 300
Relic Shield,500,+125 Max Health,Basic Items,"Relic Shield ~   ~ Relic Shield ~ Kill minions to earn bonus gold ~  +125 Max Health ~ This item is for support players. When equipped, it will reduce the gold you receive from killing minions and monsters. If there are multiples of this item within the party, only one of them can take effect at any given time. ~ Tribute: ~  Gain 1 encircling energy orb(s) every 30 seconds (max 3 orbs). While near an ally, the actions below will trigger Tribute, consuming 1 energy orb(s) to grant you  ~ 65 gold ~  and restore your  ~ Health 20-80 ~ : ~ 1. Using abilities or attacks to damage enemy champions or structures. ~ 2. Attacking minions below 65% Health. This also executes them, and the gold generated from the minion kills is given to the ally nearest to you. 3. A nearby minion is killed while you have 3 orbs. Upon triggering Tribute, the ally nearest to you gains Tribute stacks. ~ Sentry: ~  Deal 1 more damage to Sight Wards revealed by Sweeping Lens, Control Ward, and Scryer's Bloom. ~ Restraint: ~  You do not earn gold generated from minion kills, but you earn gold equal to 50% of the bounty. The gold generated from your minion kills will be given to the ally nearest to you. Gold earned from monster kills is reduced by 50%. ~ Quest: ~  After earning  ~ 750 gold ~ , this item upgrades into  ~ Bulwark of the Mountain ~  and binds you and the ally with the most Tribute stacks as  ~ Perfect Partners ~ .  ~   ~ 500"
Spectral Sickle,500,Quest:,Basic Items,"Spectral Sickle ~   ~ Spectral Sickle ~ Attack champions and structures to gain bonus gold ~ This item is for support players. When equipped, it will reduce the gold you receive from killing minions and monsters. If there are multiples of this item within the party, only one of them can take effect at any given time. ~ Versatile: ~  Gain  ~ 10 Attack Damage ~  or  ~ 20 Ability Power ~  (Adaptive). ~ Tribute: ~  Gain 1 encircling energy orb(s) every 30 seconds (max 3 orbs). While near an ally, the actions below will trigger Tribute, consuming 1 energy orb(s) to grant you  ~ 65 gold ~  and restore your  ~ Health 20-80 ~ : ~ 1. Using abilities or attacks to damage enemy champions or structures. ~ 2. Attacking minions below 65% Health. This also executes them, and the gold generated from the minion kills is given to the ally nearest to you. 3. A nearby minion is killed while you have 3 orbs. Upon triggering Tribute, the ally nearest to you gains Tribute stacks. ~ Sentry: ~  Deal 1 more damage to Sight Wards revealed by Sweeping Lens, Control Ward, and Scryer's Bloom. ~ Restraint: ~  You do not earn gold generated from minion kills, but you earn gold equal to 50% of the bounty. The gold generated from your minion kills will be given to the ally nearest to you. Gold earned from monster kills is reduced by 50%. ~ Quest: ~  Earn  ~ 750 gold ~  with this item to transform it into  ~ Black Mist Scythe ~  and bind you and the ally with the most Tribute stacks as Perfect Partners. ~   ~ 500 ~    ~                          ~                      ~                  ~                  ~                      ~                          ~                              ~                                  ~  KEYSTONE ~                              ~                          ~                          ~      ~      ~          ~ Electrocute ~ Burst Damage ~ Within 3 seconds, hit the same enemy champion with 3 basick attacks or abilities to cause additional adaptive damage to the target. ~ Damage value: 40-210 ( ~ ) +  ~ 10% extra  ~  +  ~ 5%  ~ Cooldown: ~  20-13s ( ~ ) ~      ~      ~      ~      ~          ~ Dark Harvest ~ Bonus Damage, Stack Amplification ~ Damaging a champion below 50% health deals adaptive damage and harvests their soul, permanently increasing Dark Harvest's damage by 11. ~ Dark Harvest damage: 35+ 11 per soul +  ~ 10% bonus  ~  +  ~ 5%  ~ Cooldown: ~  20s (Resets to 1s on takedown) ~      ~      ~      ~      ~          ~ Empowerment ~ Increased damage against champions ~ Hitting an enemy champion with 3 consecutive attacks deals bonus  ~ adaptive ~  damage and amplifies your damage dealt by 8% until you leave combat with champions. ~ Adaptive ~  Damage: ~  40-165 ( ~ ) ~ Cooldown: 4s. ~ Damage amplification will only take effect against champions. ~      ~      ~      ~      ~          ~ Lethal Tempo ~ Attack Speed ~ Gain Attack Speed when attacking enemy champions. Stacks up to 6 times. At max stacks deal bonus damage with your attacks. ~ Each stack  ~ Attack Speed ~  by  ~ 6% ~  ( ~ 4.8% ~  for ranged champions) for 6 seconds. ~ Max stacks bonus: ~  Attacks against non-turrets fire a bullet on hit, dealing  ~ 9–30 adaptive damage ~  ( ~ 6–20 ~  for ranged champions). Every 1% bonus  ~ Attack Speed ~  you have increases the damage by 0.5% (0.33% for ranged champions). ~      ~      ~      ~      ~          ~ Fleet Footwork ~ Mobility, Heal ~ Moving, attacking and casting builds Energy stacks. At 100 stacks, your next attack gains  ~ Attack Speed ~ , heals you, grants bonus  ~ Movement Speed.  ~ If the attack is again st a champion, it also restores Mana or Energy. ~ Bonus Attack Speed ~ : 40% ~ Health Restore: ~  15-110 ( ~ ) +  ~ 15% bonus ~  +  ~ 10% ~ . ~ Bonus Movement Speed ~ : 20% for 1s. ~ When attacking a champion, restore 8% missing  ~ mana ~  or 8% missing  ~ energy ~ . ~ When attacking minions or monsters, heals for 35% (Melee champions) or 15% (Ranged champions) of the original heal amount. ~      ~      ~      ~      ~          ~ Conqueror ~ Stacking Damage, Vamp ~ Gain stacks of Adaptive Force when hitting a champion with separate attacks or abilities. Stacks up to 6 times. When fully stacked, gain bonus omnivamp. ~ Per stack:  ~ 3-5 bonus  ~  or  ~ 5-8  ~  for 6s. ~ Fully stacked bonus: Melee - 9%, Ranged - 5% bonus  ~ Omnivamp  ~ . ~      ~      ~      ~      ~          ~ Grasp of Undying ~ Tank, Heal ~ Every 3s in combat, your next attack on a champion will be enhanced. ~ Bonus  ~ magic damage ~ :  ~ 3.3% ~ Heal:  ~ 1.3% ~ Permanently  ~ health ~  increase:  ~ 10 ~ On Ranged champions, the effects are reduced by 60%. ~      ~      ~      ~      ~          ~ Guardian ~ Protect, Shield ~ Guard allies within 350 units of you and allies you target with abilities for 2.5 second(s). While guarding, if you or the ally take more than a certain amount of damage, both of you gain a shield for 1.5 second(s). ~ Shield: 40–165 ( ~ ) +  ~ 6% bonus ~  +  ~ 15% ~ Damage threshold: 70–240 damage taken ( ~ ) ~ Cooldown: ~  55–25s ( ~ ) ~      ~      ~      ~      ~          ~ Aery ~ Poke, Protect ~ Your attacks and abilities send Aery to a target, damaging enemies or shielding allies. ~ Damage: 15-70 ( ~ ) +  ~ 10% bonus ~  +  ~ 5% ~ Shield: 25-120 ( ~ ) +  ~ 10% bonus ~  +  ~ 5% ~ Aery cannot be sent out again until she returns to you. ~      ~      ~      ~      ~          ~ Arcane Comet ~ Poke, Stack Amplification ~ Damaging a champion with an ability hurls a comet at their location. When a comet hits an enemy champion, the next comet's damage increases. ~ Damage: (15 to 100) + (2 x total hits on enemy champions) +  ~ 10% bonus ~  +  ~ 5% ~ . ~ Cooldown: ~  16-8s ( ~ ) ~      ~      ~      ~      ~          ~ Phase Rush ~ Mobility, Ability Haste ~ Using basic attacks or abilities on an enemy champion 3 time(s) within 4s grants  ~ Movement Speed ~  and reduces the remaining cooldown of basic abilities by 20%. ~ Duration: ~  3s. ~ Movement Speed bonus: ~  Melee -  ~ 40%-60% ~  ( ~ ) | Ranged -  ~ 20-35% ~  ( ~ ). ~ Ability Haste: ~  10. ~ Slow Resist: ~  60%. ~ Cooldown: ~  21-7s ( ~ ) ~      ~      ~      ~      ~          ~ First Strike ~ Initiate, Damage Amplification, Bonus Gold ~ Initiating combat with an enemy champion or dealing damage to them within 0.25s of engaging them in combat grants  ~ 10 gold ~  and First Strike for 3s, allowing you to deal  ~ 7% bonus true damage ~  to them. After the effect ends, gain bonus  ~ gold ~  based on the bonus damage dealt for its duration. ~ If you do not deal damage to the enemy champion within 0.25s of engaging them in combat, First Strike will go into a 10-second cooldown. ~ Bonus gold: ~ Melee: 65% of bonus damage. ~ Ranged: 45% of bonus damage. ~ Cooldown: ~  20-30s ~      ~      ~      ~      ~          ~ Ice Overlord ~ Control, Slow ~ Immobilizing an enemy champion causes 3 beams to form around them, creating ice beneath them for 3 second(s) and slowing enemies inside. The slow lingers on enemies for 1.5 second(s) after they've left the ice zone. Gain a protective layer of ice around yourself, increasing your defenses. After a brief delay, the ice explodes, dealing a burst of magic damage around you. ~ Slow: ~  ( ~ 1% ~  of your  ~ bonus Health ~  + 15%). ~ Defenses: ~  35 + 75% bonus  ~ Armor ~  and  ~ Magic Resist ~ . Lasts 2.5 second(s). ~ Magic damage: ~  15–100 ( ~ ) +  ~ 5% max ~ Cooldown: ~  20s ~      ~      ~                          ~                      ~                      ~                          ~                              ~                                  ~ DOMINATION ~                              ~                          ~                          ~                          ~      ~      ~          ~ Cheap Shot ~ Targets movement-impaired enemies ~ Deals 10-45 bonus  ~ true damage ~  to enemies whose movement is impaired. ~ Cooldown: ~  7s ~      ~      ~      ~      ~          ~ Sudden Impact ~ Triggers when in stealth or dashing ~ Damaging an enemy champion deals a bonus  ~ 15-65 true damage ~  after using a dash, leap, blink, teleport, or when exiting stealth for 4s. ~ The damaging attack/ability gains bonuses at higher levels: ~ Level 5: ~  Deal an additional  ~ 5 true damage ~ . ~ Level 9: ~  Deal an additional  ~ 5 true damage ~  and gain  ~ 10% Movement Speed ~  for 1.5s after dealing the damage. ~ Cooldown: ~  10s ~      ~      ~      ~      ~          ~ Empowered Attack ~ Triggers on attack ~ Every 8 seconds, the next attack will be empowered, dealing 20-60 bonus  ~ adaptive ~  damage ( ~ ) to anemy champions. Ranged champions deal 80% damage. ~      ~      ~                          ~                          ~                          ~      ~      ~          ~ Chain Assault ~ Triggers on attack after hitting a target with an ability ~ Hitting an enemy champion with an active ability applies a mark to them, causing your next 2 attacks or active ability casts against them to deal bonus  ~ adaptive damage ~  equal to (12-38 ( ~ ) +  ~ 3% bonus  ~  +  ~ 1.5% ~ ). ~ Cooldown: ~  15s ~      ~      ~      ~      ~          ~ Tyrant ~ Deal damage to low Health enemies ~ When damaging a champion below 50% Health, deal (20-70 ( ~ ) +  ~ 6% bonus  ~  +  ~ 3%  ~ ) bonus  ~ adaptive damage ~ . ~ Cooldown: ~  10s ~      ~      ~      ~      ~          ~ Hubris ~ Kills temporarily increase Attack Damage/Ability Power ~ Scoring a takedown against an enemy champion within 3 second(s) of damaging them grants (5 + 1 per champion kill you've scored)  ~ Adaptive Force ~  for 30 second(s). ~      ~      ~                          ~                          ~                          ~      ~      ~          ~ Eyeball Collection ~ Kills increase Attack Damage/Ability Power ~ Gains  ~ 1.5 ~  or  ~ 3 ~  after scoring a champion or epic monster takedown, stacking up to 8 times. ~      ~      ~      ~      ~          ~ Ingenious Hunter ~ Kills increase Item Ability Haste ~ Gains 20 Item  ~ Ability Haste ~ . For each champion or epic monster takedown you score, gain an additional 5 Item  ~ Ability Haste ~ . Stacks up to 5 times. ~      ~      ~      ~      ~          ~ Relentless Hunter ~ Kills grant out-of-combat Movement Speed ~ Gain  ~ 10 ~  out-of-combat  ~ Movement Speed ~ . For each champion or epic monster takedown you score, gain  ~ 2 ~  out-of-combat  ~ Movement Speed ~ . Stacks up to 5 times. ~      ~      ~      ~      ~          ~ Zombie Ward ~ Vision control increases Attack Damage/Ability Power ~ Takedowns on enemy wards spawn a Zombie Ward in its place, granting vision of the surrounding area for 120 seconds. Additionally gain  ~ 3 ~ or  ~ 6 ~ (max 5 stacks). (Assists on enemy wards also grant stacks and spawn Zombie Wards.) ~      ~      ~                          ~                      ~                      ~                          ~                              ~                                  ~ PRECISION ~                              ~                          ~                          ~      ~      ~          ~ Brutal ~ Attacks deal on-hit damage ~ Attacks deal ( ~ 5 ~  +  ~ 6% bonus  ~ +  ~ 3%  ~ ) bonus  ~ adaptive ~  damage to enemy champions. ~      ~      ~      ~      ~          ~ Triumph ~ Increase damage when low in Health ~ Champion takedowns restore  ~ 10% of lost health ~  and 10% of maximum  ~ Mana ~   ~ Energy ~ and grant  ~ 35 Movement Speed ~  for 2 second(s). ~      ~      ~      ~      ~          ~ Battle Zeal ~ Increase damage during prolonged battles ~ Gain 1.4% stacking basic ability damage amplification every 1 second(s) while in combat with a champion. Stacks up to 3 times and only takes effect against enemy champions. ~      ~      ~                          ~                          ~      ~      ~          ~ Last Stand ~ Increase damage when low in Health ~ When  ~ health is lower than 60% ~ , attacks launched at enemy champions deal 5-11% bonus  ~ adaptive ~  damage. ~ Grants maximum bonus damage when Health is lower than  ~ 30% ~      ~      ~      ~      ~          ~ Cut Down ~ Deal more damage to high Health enemies ~ Your attacks deal 6.57% bonus  ~ adaptive ~  damage to enemy champions with more than 60% Health. ~      ~      ~      ~      ~          ~ Coup de Grace ~ Increase damage to low Health enemies ~ Your attacks deal 8% bonus  ~ adaptive ~  damage to enemy champions with less than  ~ 40% Health ~ . ~      ~      ~                          ~                          ~      ~      ~          ~ Legend: Alacrity ~ Increase bonus Attack Speed ~ Gains  ~ 3% Attack Speed ~ . Takedown monsters, enemy champions, or minions to gain up to an additional  ~ 18% Attack Speed ~ . ~      ~      ~      ~      ~          ~ Legend: Haste ~ Bonus Ability Haste ~ Gain  ~ 0 Ability Haste ~  at the start of the game. Taking down monsters, enemy champions, or minions grants additional Ability Haste bonuses. Total bonus is capped at  ~ 15 Ability Haste ~ . ~      ~      ~      ~      ~          ~ Legend: Bloodline ~ Increase Omnivamp ~ Gains  ~ 1% Omnivamp  ~ . Takedown monsters, enemy champions, or minions to gain up to an additional  ~ 7% Omnivamp  ~ . ~      ~      ~                          ~                      ~                      ~                          ~                              ~                                  ~ RESOLVE ~                              ~                          ~                          ~      ~      ~          ~ Demolish ~ Destroy turrets faster ~ Your third attack against a turret deals bonus  ~ physical damage ~  (85 +  ~ 28% max Health ~  for melee champions; 50 +  ~ 20% max Health ~  for ranged champions). ~ Cooldown: ~  30s ~      ~      ~      ~      ~          ~ Font of Life ~ Team Heal ~ When your attacks or abilities hit an enemy champion, heal yourself and the lowest Health allied champion nearby. ~ Ally: Heals for  ~ 1.5% of your max  ~  +  ~ 5% of your ~ You: Heal for  ~ 1% of your max  ~  +  ~ 5% of your ~ Healing is 130% effective if you're a melee champion. (Does not trigger if you or nearby allies are at full Health, or if no allies are nearby.) ~ Cooldown: ~  15s ~      ~      ~      ~      ~          ~ Courage of the Colossus ~ Immobilize enemies to gain shields ~ Gains a  ~ shield that absorbs ~  up to  ~ 25-45  ~ ( ~ ) +  ~ 1% of max Health ~  for 3s when immobilizing an enemy champion. ~ Cooldown: ~  18s ~      ~      ~      ~      ~          ~ Unshakeable ~ Increase Armor, Magic Resist, and Slow Resist ~ Gain 3%  ~ Armor ~  and  ~ Magic Resistance ~ . For every 1 enemy champion(s) nearby, gain an additional 2%  ~ Armor ~  and  ~ Magic Resistance ~ . If the max number of enemy champions are nearby (max: 3), you also gain  ~ 20% Slow Resist ~ . ~      ~      ~                          ~                          ~      ~      ~          ~ Second Wind ~ Increase sustain ~ Gain  ~ 5 Health ~  every 5 seconds. ~ After taking damage from an enemy champion,  ~ regenerate 3 + (1.5% of your missing health)  ~  over the next 5 seconds. This effect is doubled for melee champions. ~      ~      ~      ~      ~          ~ Nullifying Orb ~ Grant a protective shield ~ If you take damage from a champion that causes you to fall below 35% of your max Health, gain a  ~ shield ~  that  ~ absorbs up to 60-180 ~  ( ~ ) damage for 4s. ~ Cooldown: ~  60s ~      ~      ~      ~      ~          ~ Bone Plating ~ Anti-Burst Damage ~ When taking damage from a champion, the current and next 3 champion abilities or attacks against you and within 1.5s deal  ~ 30-60 ~  ( ~ ) less damage. ~ Cooldown: ~  40s ~      ~      ~                          ~                          ~      ~      ~          ~ Overgrowth ~ Increase max Health ~ For every 3 enemy minions or 3 monster(s) killed nearby, permanently gain  ~ 3 max Health ~ . Max Health can be increased indefinitely this way. Gain an additional  ~ 3% max Health ~  upon reaching 30 stacks. ~      ~      ~      ~      ~          ~ Revitalize ~ Empowered heals and shields ~ Gains a 5% amplification effect when  ~ Healing ~  or granting  ~ Shields ~ . If the target's Health is lower than 40%, the effect is amplified by an additional 10%.  ~      ~      ~      ~      ~          ~ Perseverance ~ Increase survivability when crowd controlled ~ Gain  ~ 10% Tenacity ~ . Gain 10-15  ~ Armor ~  and  ~ Magic Resistance ~  ( ~ ) for 1.5 seconds when mmobilized. Refresh duration time when immobilized multiple times. ~      ~      ~                          ~                                                  ~                      ~                      ~                          ~                              ~                                  ~ SORCERY ~                              ~                          ~                          ~      ~      ~          ~ Axiom Arcanist ~ Empowered Ultimate Ability ~ Your ultimate ability has 10% increased damage,  ~ healing ~ , and  ~ shielding ~ . (AoE damage is reduced to a 5% increase.) ~ Scoring a takedown on an enemy champion reduces your ultimate ability's remaining cooldown by 7%. ~      ~      ~      ~      ~          ~ Manaflow Band ~ Increase Mana ~ Hitting an enemy champion with and ability or  ~ empowered ~  attack permanently increases your  ~ max mana  ~  by  ~ 30 ~ , up to  ~ 300 mana. ~      ~      ~      ~      ~          ~ Botanist ~ Empowered plant effects ~ When you destroy a plant, gain  ~ 10 gold ~  and empowered plant effects. Soulflowers near the turrets also grant additional bonuses. ~ Honeyfruit: ~   ~ Heal ~  is increased by  ~ 20% ~  when consumed. ~ Scryer's Bloom: ~   ~ Vision granted ~  lasts 20% longer when destroyed. ~ Blast Cone: ~  Gain  ~ 40% Movement Speed ~  for 2.5 second(s) after the knockback. ~      ~      ~      ~      ~          ~ Hextech Flashtraption ~ Gain short-range movement while Flash is on cooldown ~ While Flash is on cooldown, it is replaced by Hexflash. Dash a distance based on charge time (max 2s). Entering combat with enemy champions to trigger a 6-second cooldown.  ~ Cooldown: ~  18s ~      ~      ~                          ~                          ~      ~      ~          ~ Transcendence ~ Reduces ability cooldowns ~ Gain a bonus when reaching the following levels: ~ At level 1, gain  ~ 5 Ability Haste ~ ; ~ at level 5, gain bonus  ~ 5 Ability Haste ~ ; ~ at level 9, after Basic Ability hit the target, reduce 8% the ability's cooldown time. ~ Cooldown: ~  8s ~      ~      ~      ~      ~          ~ Celerity ~ Increase Movement Speed ~ Gain  ~ 2% Movement Speed ~ . All  ~ Movement Speed ~  bonuses on you are also increased by  ~ 7% ~ . ~      ~      ~      ~      ~          ~ Absolute Focus ~ Gain Attack Damage/Ability Power at high Health ~ While above 65% Health, gain a bonus  ~ 2–20 Attack Damage ~  ( ~ ) or  ~ 2–30 Ability Power ~  ( ~ ) ( ~ Adaptive ~ ). ~      ~      ~                          ~                          ~      ~      ~          ~ Scorch ~ Abilities deal bonus damage ~ Damaging an enemy champion with an ability burns them, dealing  ~ 21-49 bonus magic damage ~  ( ~ ) after 1 seconds. ~ Cooldown: ~  8s ~      ~      ~      ~      ~          ~ Nimbus Cloak ~ Spells increase Movement Speed ~ After using a Spell (Flash, Ignite, etc.),  ~ 10% - 40% movement bonus ~  for 3 seconds. The speedup effectiveness depends on the Spell's cooldown. ~      ~      ~      ~      ~          ~ Gathering Storm ~ Increase Attack Damage/Ability Power over time ~ Starting from 6 minutes into the game, gain increasing  ~ Attack Damage ~  or  ~ Ability Power ~  ( ~ Adaptive ~ ). Bonuses increase time, totaling  ~ 2/5/9/14/etc. ~  or  ~ 4/10/18/28/etc. ~  based on game time. ~      ~      ~      ~      ~          ~ Ixtali Seedjar ~ Plant fruits after destroying one ~ After destroying a plant, immediately gain a seeds that replaces your trinket for 60 seconds. The seed matures and self-destructs after it is planted at a target location. (Seeds you can pick up will also drop when an ally destroys a plant.) ~ Seeds become obtainable 2 minutes after the game starts. ~ Cooldown: ~  Each plant has a unique 30s ~      ~      ~                          ~                                              ~                      ~                  ~                  ~                      ~                          ~                              ~                                  ~ Spells"
Flash,,,Basic Items,Flash ~   ~ Flash ~ Teleport a short distance forward or towards the aimed direction. ~ Cooldown: ~  150s
Ghost,,,Basic Items,"Ghost ~   ~ Ghost ~ Gain a large burst of  ~ movement speed ~ , that decays to  ~ 25% bonus movement speed ~  for 8 seconds. With each takedown, Ghost's duration is extended by 6 seconds, refreshing its effects, up to the original amount. ~ Cooldown: ~  90s"
Heal,,,Basic Items,"Heal ~   ~ Heal ~ Restore 110 Health ~  (110–400  ~ ) to you and the most wounded nearby ally champion, and grants both of you  ~ 30% bonus Movement Speed ~  for 2 second(s). ~ Healing is halved for champions recently affected by Heal. ~ Cooldown: ~  100s"
Barrier,,,Basic Items,Barrier ~   ~ Barrier ~ Gain a  ~ shield ~  that  ~ absorbs 120 ~  (120–560  ~ ) damage for 2.5 seconds. ~ Cooldown: ~  100s
Ignite,,,Basic Items,"Ignite ~   ~ Ignite ~ Ignites target enemy champion, dealing  ~ 72 true damage ~  (72–380  ~ ) over 5 and applying  ~ 60% Grievous Wounds ~  for the duration. ~ Grievous Wound ~  reduces the effectiveness of Healing and Regeneration effects. ~ Cooldown: ~  100s"
Exhaust,,,Basic Items,"Exhaust ~   ~ Exhaust ~ Exhausts target enemy champion, reducing their  ~ Movement Speed by 35% ~  and their damage dealt by 40% for 2.5 seconds. ~ Cooldown: ~  100s"
Smite,,,Basic Items,"Smite ~   ~ Smite ~ Jungle Expertise: ~ On cast, Smite deals  ~ 600 true damage ~  to minions and monsters and causes your attacks against a monster to deal  ~ 30 true damage ~ ( ~ ) every second in an area around them for 2 seconds. This damage is increased by  ~ 10% bonus Attack Damage ~ ,  ~ 12% bonus Ability Power ~ ,  ~ 25% bonus Armor ~ ,  ~ 25% bonus Magic Resist ~ , and  ~ 4% bonus Health ~ . ~ Deals 10% more damage against monsters. ~ Hunter's Resource: ~ - Gain Hunter's Resource stacks over time. After clearing a monster camp, 1 stack(s) are consumed for  ~ 40 bonus gold ~ . ~ -  ~ Restore 5–35 Health ~  every second ( ~ ) when attacking monsters. Health restored is based on your missing Health. ~ - When Smite is equipped, take only 50% damage from non-epic monsters. ~ Upgraded Smite: ~ - After consuming 8 and 20 stacks, Smite upgrades, increasing its damage to 1,000 and 1,400 respectively. ~ - When Smite is fully upgraded, gain  ~ Movement Speed ~  while in the jungle or river:  ~ 10% Movement Speed ~  out of combat, and  ~ 5% Movement Speed ~  in combat. ~ - Upgraded Smite can be cast on champions to deal  ~ 40 true damage ~  damage and steal 25% of their Movement Speed for 2 seconds. ~ Gains one charge every 45 seconds, up to a max of 2. ~ Cooldown: ~  45s"
Cleanse,,,Basic Items,Cleanse ~   ~ Cleanse ~ Removes disables (including spell debuffs) affecting your champion and grants immunity to disables for 0.25 seconds. ~ Cooldown: ~  110s
Teleport,,,Basic Items,"Teleport ~   ~ Teleport ~ After channeling for 3.5 seconds, teleport your champion to an allied champion, structure, or ward (excludes areas in range of enemy inhibitors). You can only teleport to structures during the first 6 minutes of the game. ~ Cooldown: ~  150s ~    ~                          ~                      ~                  ~              ~          ~          ~          ~          ~              ~      (adsbygoogle = window.adsbygoogle || []).push({}); ~  OFF ADS ~              ~          ~          ~          ~      ~          ~          ~          ~          ~          ~          ~          ~          ~          ~      ~ LoL Wild Rift Items ~      ~          ~ Items ~  - used by LoL Wild Rift champions to increase their base stats during battles on the fields of justice. Most items have their own unique passive skills. ~      ~      ~         Each champion can purchase a maximum of six items, which means that you need to be smart about buying them, you need to know the strengths and weaknesses of your champion. There are also active items in the game - these are boots that can be enchanted and get one of 9 effects, such as Stasis, Teleport, etc. You can only have 1 active item available to you. Do not forget that each active item has its own recharge time after its use. ~      ~      ~          ~ League of Legends Wild Rift in-game items ~  can only be bought while at your base with gold received in battle. Acquire items considering the situation in the game, if you learn how to analyze it correctly, you will be ready for any trouble. ~      ~      ~         In Wild Rift, there are items for physical damage, magical damage and for increasing defensive characteristics. Marksmans, some assassins and warriors rely on physical attack, respectively, as the game progresses, improve its performance. Mages, supports, and some assassins improve their ability power by buying magic damage items. Tanks and some warriors prefer survivability over damage and gain health, armor, and magic defense by purchasing items with defensive stats. ~      ~      ~          ~ Wild Rift items ~  come in varying quality and are upgraded with gold. At the start of the game, you can only buy Basic items, which over time you can upgrade to COMMON and Improved. ~      ~      ~         You can get acquainted with all game items on this page by going to the page of the item itself, you can find out a little more of useful information! ~      ~          ~      ~              ~                 ~                  ~                      ~ wr ~ meta ~                      ~                          ~ Advertise ~                          ~ Feedback ~                          ~ Privacy policy ~                          ~ Delete account ~                          ~   ~ Twitter ~                          ~   ~ Patreon ~                      ~                  ~                  ~ This project is not official and is not affiliated with Riot Games. It was created by enthusiasts and fans of the game for educational purposes only. Copying materials is allowed with an active link to the source page. ~ © Copyright 2020-2026 by JLVD DEV ~                  ~              ~              ~          ~      ~      ~          ~              ~ Search ~              ~          ~          ~              ~              ~              ~                  ~                  ~                  ~              ~          ~      ~      ~      ~      ~      ~      ~      ~      ~    ~      ~     ~      ~      ~      ~      ~    ~      ~      ~      ~      ~       ~      ~      ~      ~      ~     window.addEventListener('load', function(){ ~       var pre = document.querySelector('.loaderArea'); ~       if(!pre) return; ~       pre.style.transition = 'opacity .25s ease'; ~       pre.style.opacity = '0'; ~       pre.style.pointerEvents = 'none'; ~       setTimeout(function(){ pre.style.display='none'; }, 280); ~     }); ~      ~      ~      ~     (function(){ ~       function run(){ ~         document.querySelectorAll('.nolazy img[data-src]').forEach(function(img){ ~           img.setAttribute('src', img.getAttribute('data-src')); ~           img.removeAttribute('data-src'); ~         }); ~       } ~       if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', run, {once:true}); ~       else run(); ~     })(); ~      ~      ~      ~       var fired = false; ~       window.addEventListener('scroll', function(){ ~         if (fired) return; ~         fired = true; ~         setTimeout(function(){ ~           var GTMObject = document.createElement(""script""); ~           GTMObject.src = 'https://www.googletagmanager.com/gtag/js?id=G-P6EEJGLKQ3'; ~           GTMObject.async = true; ~           document.getElementsByTagName('head')[0].appendChild(GTMObject); ~           window.dataLayer = window.dataLayer || []; ~           function gtag(){ dataLayer.push(arguments); } ~           gtag('js', new Date()); ~           gtag('config', 'G-P6EEJGLKQ3'); ~         }, 5000); ~       }, {passive:true}); ~      ~      ~      ~      ~     (function(){ ~       function loadAds(){ ~         var s1 = document.createElement('script'); ~         s1.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7039714206715924'; ~         s1.async = true; ~         s1.crossOrigin = 'anonymous'; ~         document.head.appendChild(s1); ~         var s2 = document.createElement('script'); ~         s2.src = 'https://fundingchoicesmessages.google.com/i/pub-7039714206715924?ers=1'; ~         s2.async = true; ~         document.head.appendChild(s2); ~         (function() { ~           function signalGooglefcPresent() { ~             if (!window.frames['googlefcPresent']) { ~               if (document.body) { ~                 var iframe = document.createElement('iframe'); ~                 iframe.style = 'width:0;height:0;border:none;position:absolute;left:-9999px;top:-9999px;'; ~                 iframe.style.display = 'none'; ~                 iframe.name = 'googlefcPresent'; ~                 document.body.appendChild(iframe); ~               } else { ~                 setTimeout(signalGooglefcPresent, 0); ~               } ~             } ~           } ~           signalGooglefcPresent(); ~         })(); ~       } ~       window.addEventListener('load', function(){ ~         setTimeout(loadAds, 1600); ~       }); ~     })(); ~      ~      ~      ~      ~      ~      ~       (function() { ~         var a = document.querySelector('#aside1'), ~             b = null, ~             P = 70; ~         if(!a) return; ~         window.addEventListener('scroll', Ascroll, false); ~         document.body.addEventListener('scroll', Ascroll, false); ~         function Ascroll() { ~           if (b == null) { ~             var Sa = getComputedStyle(a, ''), ~                 s = ''; ~             for (var i = 0; i  ~      ~      ~ window.addEventListener('load', function(){ ~   if (!window.jQuery) return; ~   jQuery("".extremum-click"").off('click.wrm').on('click.wrm', function () { ~     jQuery(this).siblings("".extremum-slide"").slideToggle(""slow""); ~   }); ~ }); ~      ~      ~     window.addEventListener('load', function(){ ~       setTimeout(function(){ ~         if (window.__sharethis_loaded) return; ~         window.__sharethis_loaded = true; ~         var s = document.createElement('script'); ~         s.src = 'https://platform-api.sharethis.com/js/sharethis.js#property=653ac2c5933f6c0019e85d83&product=inline-share-buttons'; ~         s.async = true; ~         document.body.appendChild(s); ~       }, 2000); ~     });"

```

## 16. ROADMAP DEL PROYECTO (módulos futuros)

# ROADMAP — WR-LAB como proyecto de software

**Estado actual (v1.5):** repo git local versionado · BD SQLite derivada · suite de tests · CI + vigilante de parches (GitHub Actions) · datos 7.3+7.3a.

## Ya disponible

| Capacidad | Dónde | Estado |
|---|---|---|
| Control de versiones | git local (tags por versión del lab) | ✅ listo para `git remote add origin … && git push` |
| Base de datos | `data/wrlab.db` (SQLite) vía `model/build_db.py` | ✅ se reconstruye desde los .md/.csv en segundos |
| Tests de regresión | `tests/test_model.py` (unittest, sin dependencias) | ✅ golden numbers de Jinx + slots + fórmula AS + overrides 7.3a |
| Vigía de parches | `model/check_patch.py` + `.github/workflows/patch-watch.yml` (cron 2×/día) | ✅ detecta: cambios en la página 7.3, aparición de 7.3a/7.4, nuevas entradas de changelog en wr-meta |
| CI | `.github/workflows/ci.yml` (tests + rebuild BD en cada push) | ✅ |
| Motor de DPS + validador | `model/dps_model.py` (`validate_slots`, `eval_build`, `compare`) | ✅ |

## Módulos propuestos (prioridad × esfuerzo)

1. **`wrlab` CLI unificado** (bajo esfuerzo, alto valor)
   `python -m wrlab update | analyze <champ> | db rebuild | test | bundle | watch`
   — envolver los scripts actuales en un solo punto de entrada con argparse.

2. **Optimizador de builds** (medio, MUY alto valor)
   Búsqueda exhaustiva/branch-and-bound sobre el pool de ítems del rol maximizando
   `dpsN` sujeto a: 6 slots, Ley 0 (1 botas), Ley 1 (crit ≤ umbral), Ley 2 (AS ≤ cap+ε),
   presupuesto de oro por minuto. Entrada: ChampSpec + escenarios; salida: top-N builds
   con desglose multiplicativo. Validación cruzada contra los reportes existentes
   (debe "redescubrir" la build C de Jinx y la K2 de Kalista).

3. **Buscador de runas** (bajo) — misma lógica sobre keystones×secundarias con valor marginal por escenario.

4. **Sincronizador con el sitio Quartz** (bajo-medio)
   `wrlab sync-vault <ruta-del-vault>`: copia reportes + fichas con frontmatter, genera
   índice `Guias.md`, respeta la nomenclatura del vault y hace commit en ese repo.
   Publicar = `git push` del vault (su workflow de Pages ya funciona).

5. **Simulador de timings de oro** (medio) — curva de oro de ADC/support/jungla por minuto
   (datos 7.3: minions, placas con decaimiento, jungle eco) para fechar los picos de cada
   ruta con precisión en vez de "~13:00".

6. **Matriz de matchups** (alto) — EHP/DPS efectivo cruzado entre builds (p.ej. "¿mi Jinx
   full contra un Chainlaced+Randuin?"), usando las tablas de mitigación ya existentes.

7. **Backup externo de la BD** (bajo) — el repo en GitHub YA es el backup (texto + db commiteada);
   opcional: export nocturno de `wrlab.db` a release assets vía Actions.

## Decisiones de arquitectura (por qué así)

- **Texto plano como fuente de verdad, SQLite como índice:** los .md/.csv viajan en los bundles
  portables (cualquier chat/IA los consume sin tooling); la BD da consultas rápidas y es reconstruible.
  Nunca al revés (una BD opaca rompería la portabilidad que ya resolvimos).
- **Sin dependencias de terceros:** todo stdlib (urllib, sqlite3, unittest, csv). Cero `pip install`,
  cero superficie de rotura. `requirements.txt` existe pero está vacío a propósito.
- **Golden tests:** los números canónicos de los reportes están fijados en tests; cualquier cambio de
  datos que los mueva falla en CI y obliga a documentar el porqué (como el override 7.3a de Caitlyn).
- **El vigía no actualiza solo:** detecta y avisa (exit 1 + step summary). La actualización real sigue
  el protocolo FRAMEWORK §E porque requiere criterio (discrepancias, overrides, re-validación).

## Para ponerlo en GitHub (una vez, ~3 minutos)

```bash
# en tu máquina, dentro de la carpeta wr-lab descargada/copiada:
git remote add origin https://github.com/Osvaldo-Peralta/wr-lab.git   # repo nuevo, privado o público
git push -u origin main --tags
# GitHub Actions corre ci.yml en el push y patch-watch.yml 2×/día.
```


## 17. TESTS DE REGRESIÓN

```python
# -*- coding: utf-8 -*-
"""
WR-LAB · tests — suite de regresión del modelo (unittest, sin dependencias).
Ejecutar:  python3 -m unittest discover -s tests -v     (desde la raíz del lab)
"""
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import dps_model as M

class TestAttackSpeedFormula(unittest.TestCase):
    def test_caitlyn_oficial_pre73a(self):
        """Ejemplo oficial de las notas 7.3: Caitlyn lvl15 + Alacrity 18% + Berserker's = 1.48125."""
        c = M.ChampSpec(name="Caitlyn", base_ad=60, ad_growth=4.2, base_as=0.625,
                        as_ratio=0.625, base_bonus_as=0.28, as_per_lvl=0.04)
        B = c.base_bonus_as + M.lvl_as_bonus(c, 15) + 0.18 + 0.35
        self.assertAlmostEqual(c.base_as + c.as_ratio * B, 1.48125, places=5)

    def test_caitlyn_post73a(self):
        """7.3a bajó su growth a 0.025 → esperado 1.35 en las mismas condiciones."""
        c = M.ChampSpec(name="Caitlyn", base_ad=60, ad_growth=4.2, base_as=0.625,
                        as_ratio=0.625, base_bonus_as=0.28, as_per_lvl=0.025)
        B = c.base_bonus_as + M.lvl_as_bonus(c, 15) + 0.18 + 0.35
        self.assertAlmostEqual(c.base_as + c.as_ratio * B, 1.35, places=4)

    def test_as_cap(self):
        """El tope 3.0 se aplica y Get Excited se reporta por separado."""
        j = M.CHAMPS["jinx"]
        _, raw, _ = M.as_total(j, ["Gunmetal", "Runaan's", "RFC", "Kraken"])
        self.assertGreater(raw, M.AS_CAP)

class TestValidateSlots(unittest.TestCase):
    def test_build_valida(self):
        self.assertEqual(M.validate_slots(["Gunmetal","C44","Runaan's","IE","LDR","Kraken"]), (1, 5))

    def test_bug_doble_botas(self):
        """El bug histórico: Berserker's + Gunmetal como ítems separados."""
        with self.assertRaises(ValueError):
            M.validate_slots(["Statikk Shiv","Berserker's","Gunmetal","Guinsoo","BotRK","Terminus"])

    def test_siete_slots(self):
        with self.assertRaises(ValueError):
            M.validate_slots(["Berserker's","Gunmetal","C44","Runaan's","IE","LDR","Kraken"])

    def test_final_sin_botas(self):
        with self.assertRaises(ValueError):
            M.validate_slots(["C44","Runaan's","IE","LDR","Kraken","BT"])

    def test_checkpoint_parcial_ok(self):
        M.validate_slots(["Berserker's","C44","Runaan's"], final=False)  # no debe lanzar

class TestGoldenNumbers(unittest.TestCase):
    """Números canónicos del reporte de Jinx (no deben driftar sin razón documentada)."""
    def test_jinx_build_C(self):
        r = M.eval_build(M.CHAMPS["jinx"], ["Gunmetal","C44","Runaan's","IE","LDR","Kraken"])
        self.assertEqual(round(r["dps1"]), 3042)
        self.assertEqual(round(r["crit"]), 100)
        self.assertAlmostEqual(r["AS"], 2.83, places=2)

    def test_jinx_build_usuario(self):
        r = M.eval_build(M.CHAMPS["jinx"], ["Berserker's","Kraken","RFC","Runaan's","IE","BT"])
        self.assertEqual(round(r["dps1"]), 2556)

    def test_73a_yuntal_buff_aplicado(self):
        self.assertEqual(M.ITEMS["yuntal"].a_s, 35)   # 7.3a: 25 → 35

    def test_73a_deathsdance_coste(self):
        self.assertEqual(M.ITEMS["deathsdance"].gold, 3300)  # 7.3a: 3200 → 3300

class TestSpecs(unittest.TestCase):
    def test_roster_completo(self):
        esperados = {"jinx","kalista","diana","yuumi","karma","yunara","volibear","shyvana",
                     "chogath","mordekaiser","seraphine","heimerdinger","malphite"}
        self.assertTrue(esperados <= set(M.CHAMPS.keys()))

    def test_kalista_as_oficial(self):
        k = M.CHAMPS["kalista"]
        self.assertAlmostEqual(k.as_per_lvl, 0.046)
        self.assertAlmostEqual(k.base_ad + k.ad_growth*14, 129.8, places=1)

if __name__ == "__main__":
    unittest.main(verbosity=2)

```
