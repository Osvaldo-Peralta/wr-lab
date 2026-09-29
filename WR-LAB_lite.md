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
