---
tags:
  - Support
  - Marksman
  - Crítico
  - Bot-Lane
version: 1
Status: Beta
champion: Senna
slug: senna
role: support
patch: "7.3+7.3a"
archetype: "Crítico modificado / sitiadora híbrida"
engine: autos
custom: false
generate: manual
mode: sr
published_at: "2026-10-09"
updated_at: "2026-10-11"
verification: AL_DIA
verified_patch: "7.3a"
---
**Fecha del análisis:** 11/10/2026
**Parche:** 7.3 (21-sep-2026) + hotfix 7.3a (29-sep-2026)
**Rol principal:** Support (con variante DUO/ADC declarada en [!TIP])
**Arquetipo:** Crítico modificado (`crit_dmg_mod` 0.9) + enchanter híbrida
**Enfoque:** Valor-aliado (cura Q / escudo R / buff Censer) como columna support, con lado DPS medido por el motor de autos para la variante DUO y para el daño de asedio que Senna aporta aunque juegue de support.

> [!NOTE]
> **Estado Meta Actual (Diamond+, 09/10/2026):
> - **SUPPORT Win Rate 54.11 %** | Pick Rate 13.33 % | Ban 36.40 % | Tendencia 0 | Tier S+ (Confidence High).
> - **DUO Win Rate 55.16 %** | Pick 3.45 % | Ban 36.40 % | Tier S+ (Confidence Med).

---

## 0. RESUMEN EJECUTIVO

### Tabla A — BUILD FINAL (Support valor-aliado)

| Slot | Ítem | Oro | Rol en la build |
|---|---|---|---|
| 1 (botas) | **Ionian Boots → ⬆️ Crimson Lucidity** (min 10:00, MISMO slot) | 2 000 | Haste 25 + regen; Noxian Haste proca con cura/escudo |
| 2 | **Essence Reaver** | 3 000 | Spellblade 135 % AD base + 0.8/1 % crit (el crit gratis de Niebla lo alimenta) + maná |
| 3 | **Ardent Censer** | 2 400 | +30 % AS y +25 dmg mágico al aliado curado/escudado (Q y R lo procan) |
| 4 | **Black Cleaver** | 3 000 | AD + HP (570 base agradece) + shred 30 % para el daño de asedio propio |
| 5 | **Harmonic Echo** | 2 500 | Enlaza la cura Q / escudo R al segundo aliado más bajo (30/35 %) |
| 6 | **Guardian Angel** | 3 200 | Revivir: la única respuesta a su fragilidad estructural (570 HP, sin movilidad dura) |

> **Oro total: 16 100 g** · AD bonus de Niebla aparte (+1.25/stack) · crit 50 % gratis al checkpoint de 100 stacks · AS irrelevante para el plan support (ratio 0.3 post-7.3a).

### Tabla A2 — BUILD FINAL (Variante DUO/ADC, óptima del motor)

| Slot | Ítem | Oro | Rol en la build |
|---|---|---|---|
| 1 (botas) | **Berserker's → ⬆️ Gunmetal Greaves** (min 10:00, MISMO slot) | 2 200 | 50 % AS (rinde 0.3× por el ratio) + 5 % Lifesteal |
| 2 | **Hexoptics C44** | 2 900 | 55 AD + Magnification (pelea a 625+ ≥ 550 siempre) |
| 3 | **Yun Tal Wildarrows** | 3 100 | Flurry +35 % AS condicional (buff 7.3a) + crit progresivo |
| 4 | **Blade of the Ruined King** | 3 100 | 6 % vida actual on-hit: no depende de su AD bajo temprano |
| 5 | **Runaan's Hurricane** | 2 650 | 2 rayos 55 % AD que critican y aplican Relic/on-hit |
| 6 | **Infinity Edge** | 3 400 | Crit 200 % → 230 %; con `crit_dmg_mod` 0.9: 180 % → 207 % |

> **Oro total: 17 350 g** · AD 274 · AS 1.38 · Crit 100 % (50 ítems + 50 Niebla) · Pen 0 % (ver Ley 3: BotRK la sustituye vs tanques).

### Tabla B — Ruta de compra cronológica (Support)

| # | Compra | Oro acum. | Minuto típico |
|---|---|---|---|
| 1 | Quest de support (relic inicial) | 0 | 0:00 |
| 2 | Long Sword + ward de control | 500 | ~2:30 |
| 3 | **Ionian Boots of Lucidity** | 1 500 | ~4:30 |
| 4 | Caulfield's + Pickaxe → **Essence Reaver** | 4 500 | ~8:00 |
| 5 | ⬆️ **Crimson Lucidity** (mismo slot, +1 000 g) | 5 500 | 10:00 (regla T3) |
| 6 | **Ardent Censer** | 7 900 | ~12:00 |
| 7 | **Black Cleaver** | 10 900 | ~15:00 |
| 8 | **Harmonic Echo** | 13 400 | ~17:30 |
| 9 | **Guardian Angel** | 16 600 | ~20:00 |

### Runas · Hechizos · Habilidades

| Categoría | Elección |
|---|---|
| Keystone | **Glacial Augment** (slow en cadena con Q/W para el root de W) · alt. **Fleet Footwork** vs poke extremo |
| Precisión 2 | **Triumph** (ejecuciones con R y resets de pelea) |
| Precisión 3 | **Legend: Alacrity** solo en DUO; en support **Tenacity** vs CC |
| Dominación | **Treasure Hunter** (acelera Crimson y el primer Censer) |
| Hechizos | **Flash + Heal** (support) · Flash + Exhaust vs dive |
| Skills | **Q → W → E** (R en 6/11/16). Maxear Q primero: cura+daño en línea es su motor. |

### Resultado del modelo (nivel 15, LT full, 100 stacks de Niebla)

| Escenario | DUO óptima (motor) | DUO community | Soporte (valor-aliado) |
|---|---|---|---|
| **1v1** (pre-mitigación) | **1 326** | 810 (−39 %) | n/a (no es su rol de daño) |
| **3v3** (AoE teamfight) | **2 186** | 810 (sin Runaan's) | n/a |
| **vs 120 armadura** | **603** | 440 | shred Cleaver 30 % de equipo |
| **vs Tanque** (220 arm, 4 500 HP) | **474** | 319 | BotRK/Cleaver del carry buffado |
| **Cura Q (rank 4, 140 Niebla)** | — | — | **200** por impacto en línea (+222 con ER) |
| **Escudo R (140 / 180 Niebla)** | — | — | **480 / 560** por aliado (+ Echo 35 %) |

> **Titular:** Senna support no se evalúa en DPS: se evalúa en *ventanas* — cura de 200+ en línea cada ~6.8 s de CD real de Q, escudo global de 480+ pre-engage y un asedio de 625→700+ de rango que obliga al enemigo a jugar incómodo. Su lado DPS (variante DUO) es top-tier medible: la óptima del motor supera a la community en +39 % 1v1 porque el crit gratis de Niebla reescribe la Ley 1.

---

## 1. CONTEXTO DEL CAMPEÓN EN ESTE PARCHE

### 1.1 Cambios directos (Senna) — Parche 7.3

| Stat/Habilidad | Antes | Ahora | Impacto |
|---|---|---|---|
| HP base | 600 | **570** | −5 % durabilidad early (570 = de las más frágiles) |
| Sistema de AS | restringida | ratio 0.4 · base 0.4 · BBA 0.6 · growth 0.05 | Los ítems de AS pasaron a funcionarle |
| Pasiva: % vida actual | 1.2–12 % | **1–10 %** | Nerf al trade de Extraction |
| Pasiva: crit por 20 Niebla | 15 % | **10 %** | Escalado de crit más lento (100 stacks = 50 %) |
| Daño crítico propio | 141.75 % (sistema viejo) | **90 % del normal = 180 % (207 % con IE)** | Buff estructural disfrazado de nerf |
| Q base | 50/90/130/170 | **50/80/110/140** | Poke early −11 % (ranks 2-4) |
| R daño | 250/375/500 +120 % bAD +50 % AP | **250/400/550 +120 % bAD +70 % AP** | Buff: ejecutora global híbrida |
| R escudo | +40 % AP + Niebla×4 | **+50 % AP + Niebla×2** | Menos escala-Niebla, más escala-AP |

### 1.2 Hotfix 7.3a — el ajuste que define su techo

Cita oficial: *"Senna has been overperforming across all skill levels since we removed her Attack Speed restrictions. We're adjusting her Attack Speed ratio to rein in how effectively she scales with Attack Speed."*

| Parámetro | 7.3 | 7.3a | Efecto real |
|---|---|---|---|
| AS ratio / base | 0.4 / 0.4 | **0.3 / 0.3** | Cada 1 % de AS de ítems rinde 0.3 % |
| Base Bonus AS | 0.6 | **1.1** | Compensación early (AS lvl 1 ≈ 0.63) |
| AS por nivel | 0.05 | **0.025** | Lvl 15 sin ítems: 0.735 |

**AS efectiva resultante:** lvl 1 = 0.63 · lvl 15 sin ítems = **0.735** · con build full-AS = **1.38–1.44** (motor). El cap 3.0 queda a +755 % de AS bonus: **inalcanzable por diseño** → la Ley 2 no gobierna a Senna (caso Jhin: el valor de la AS está en acortar wind-up y el −1 s de CD de Q por auto, no en el DPS bruto).

### 1.3 Cambios sistémicos que le afectan

| Sistema | Cambio 7.3 | Efecto en Senna |
|---|---|---|
| **Crítico base** | 175 % → **200 %** | Con su mod 0.9: 180 %; con IE 207 %. Cada 1 % de crit (incluido el gratis) vale más |
| **AS Cap** | 2.5 → **3.0** | Irrelevante para ella (techo real 1.44) |
| **Torretas** | 3 000 → **7 000 HP** + placas | Su asedio de rango creciente siega placas/cristales desde fuera del alcance |
| **Exclusividades (Ley 3b)** | grupo `pen_pct` | Aplica igual: LDR/Mortal/Terminus no conviven (la óptima no lleva pen) |

---

## 2. FICHA MATEMÁTICA (spec 7.3a)

| Parámetro | Valor | Fuente |
|---|---|---|
| HP base / growth | 570 / +120 | notas 7.3 |
| AD base / growth | **54 / 0** (no sube por nivel) | wiki V6.2c (⚠️ W1) |
| Armadura / RM | 35 (+4.5) / 30 (+1.4) | wiki |
| Maná / regen | 345 (+65) / 21 (+0.5) | wiki |
| Rango de ataque | **625** (+15/20 stacks, cap +400 → 1 025 teórico) | wiki V4.2 |
| AS (7.3a) | ratio **0.3** · base **0.3** · BBA **1.1** · growth **0.025** | notas 7.3a |
| Daño crítico | **0.9×** el normal → 180 % / 207 % con IE | notas 7.3 |
| Niebla | +1.25 AD bonus/stack · +10 % crit/20 stacks · overcap crit → 35 % Physical Vamp | notas 7.3 |
| Proyectil | hitscan (non-projectile) · wind-up 0.5 s no cancelable (️ W3) | wiki 6.3 |
| `crit_dmg_mod` motor | 0.9 · `free_crit` 0.50 (100 stacks al checkpoint) · `aa_mult` 1.2 (Relic +20 % AD) | spec lab v1.15.3 |

**AD lvl 15 real = 54 + 1.25×Niebla + ítems.** Con 140 de Niebla: **229 AD sin comprar un solo ítem de AD** — por eso el spellblade de ER (135 % AD base + 0.8/1 % crit) y los ratios bAD de Q/W/R escalan sin compra.

---

## 3. MODELO Y FÓRMULAS

```text
# Soporte (valor-aliado, fuera del motor DPS — declarado):
cura_Q(r4)   = 130 + 0.40*bAD + 0.25*AP            # bAD = Niebla*1.25 + AD de ítems
escudo_R     = 200 + 0.50*AP + 2*Niebla            # por aliado, 3 s; castear ~1 s pre-engage
echo_Q       = 0.30*cura_Q  ·  echo_R = 0.35*escudo_R   # Harmonic Echo al 2.º aliado
censer_aliado = +30 % AS y +25 dmg mágico por 6 s  # proca con cura_Q y escudo_R
CD_real_Q    = 15 / (1 + AS)                       # −1 s por auto/on-hit

# DUO (motor dps_model, spec senna):
AS_total = min(0.3 + 0.3*(1.1 + 0.025*14 + items_AS + runas), 3.0)
Crit     = min(crit_items + 50 (Niebla 100 stacks), 100)      # Ley 1 con umbral corrido
CritDmg  = (200 | 230 con IE) * 0.9
hit      = AD * 1.2 (Relic) * CritMult * Magnification(C44)
DPS_1v1  = AS * hit · DPS_3v3 = DPS_1v1 + 2 rayos Runaan (55 % AD c/u, critan)
```

### Supuestos específicos
- **Niebla al checkpoint:** 100 stacks (50 % crit gratis) en evaluaciones de motor; benchmarks de stacks de la ficha del autor: support ≈ 90 (14 min) / 140 (18 min); DUO ≈ 65 / 110.
- **Extraction (+1–10 % vida actual por target cada ~6 s)** queda FUERA del motor: conservador a favor del lector.
- **Wind-up 0.5 s** fuera del modelo: el DPS real de Senna es menor que el teórico en kiting duro (⚠️ W3).
- **Spellblade de ER** se valora cualitativo en support (el motor no tiene ítems de support en su pool: declarado en §10).

---

## 4. LEYES APLICADAS A SENNA

- **Ley 0 — Slots:** `validate_slots` → **PASS** en ambas tablas (6 entradas, 1 bota T3 + 5 ítems; la mejora ⬆️ vive en el mismo slot).
- **Ley 1 — Crítico (UMBRAL BLANDO):** con +50 % gratis de Niebla, el objetivo de ítems es **50 %**, no 100 %. El overcap NO es oro muerto en Senna: el exceso de crit se convierte en **35 % Physical Vamp** → pasar de 100 % es una decisión de sustain, no un error. La óptima DUO clava 100 % (50+50) igual.
- **Ley 2 — AS Cap 3.0:** no vinculante (techo real 1.38–1.44). El valor de la AS es utilitario: wind-up y CD real de Q.
- **Ley 3 — Penetración:** la óptima DUO lleva **0 % pen** y gana vs tanque con **BotRK (6 % vida actual)**: contra 4 500 HP el current-health domina al pen al 35 % con su AD alto. Verificado en el motor: 474 vs tanque sin pen.
- **Ley 3b — Exclusividades:** LDR/Mortal/Terminus no conviven; ninguna build publicada los mezcla.
- **Ley 6 — Timing:** ER al minuto 8 (Caulfield temprano da haste y spellblade usable); Crimson estrictamente ≥ 10:00 (regla T3 del parche).

---

## 5. ANÁLISIS DEL PRIMER ÍTEM

| Candidato (post-quest) | Oro | Veredicto support | Nota |
|---|---|---|---|
| **Essence Reaver** | 3 000 | ✅ **Core 1** | Spellblade escala con el crit GRATIS de Niebla (0.8/1 %): 135 % AD base + ~40 con 50 % crit; +20 haste y maná |
| **Ardent Censer** | 2 400 | ✅ Core 2 | El buff proca con cada cura Q y cada escudo R: +30 % AS al carry |
| **Black Cleaver** | 3 000 | ✅ Core 3 | Único AD+HP del pool; shred 30 % que aprovecha TODO el equipo |
| **Harmonic Echo** | 2 500 | ✅ Core 4 | Convierte Q/R en herramientas de 2 objetivos |
| **Infinity Edge** (1.er ítem) | 3 400 | ❌ | Sin crit de ítems previo, el 230 % no compensa el hueco de utility en lane |
| **Statikk Shiv** (1.er ítem support) | 3 000 | ❌ | Energized = valor de waveclear que un support no necesita; sin heal/shield |

En DUO el motor responde distinto: **C44 o BotRK primero** son indistinguibles en el top-3 (1 326 / 1 320 / 1 317 de 1v1 entre óptima, top-2 ER y top-3 Storm); BotRK aporta el sustain de lane que Fleet completa.

---

## 6. BUILD FINAL RANURA POR RANURA (Support)

| Slot | Ítem | Justificación matemática |
|---|---|---|
| Botas | **Crimson Lucidity** | 25 haste + regen; Noxian Haste proca con cada cura/escudo (kiting de 570 HP) |
| 1 | **Essence Reaver** | Ver §5: el crit gratis maximiza su spellblade; mana-fix para spamear Q |
| 2 | **Ardent Censer** | +25 dmg mágico y +30 % AS al aliado: DPS delegado sin oro propio |
| 3 | **Black Cleaver** | 400 HP sobre 570 base = +70 % HP efectivo relativo; shred de equipo |
| 4 | **Harmonic Echo** | 35 % del escudo R al segundo aliado: 480 → ~648 de valor total por cast |
| 5 | **Guardian Angel** | 570 HP sin dashes: el revivir es el único "segundo posicionamiento" |

### 🛡️ MATRIZ SITUACIONAL

| Escenario | Cambio | Motivo numérico |
|---|---|---|
| Vs dive duro (Malphite/Nocturne) | Echo → **Redemption** (2 450) | Activo de 150–350 HP en área + true damage 10 %, casteable muerta |
| Vs poke mágico | Cleaver → **Redemption** + GA conservado | Sustain de área sin depender de AD propio |
| Equipo sin carries de AS | Censer → **Harmonic Echo** temprano y Echo → **Redemption** | El valor de Censer requiere un aliado que ataque |
| DUO/ADC | Tabla A2 completa | motor: +39 % 1v1 vs community |

### RECHAZADOS (con motivo numérico)

| Ítem | Motivo del rechazo |
|---|---|
| ❌ **Infinity Edge** en support | 3 400 g de puro daño en un campeón con 570 HP y rol de utility: el oro compite con Crimson+Censer (4 400 g de valor-aliado) |
| ❌ **Lord Dominik's** + **Mortal Reminder** juntos | ILEGAL (Ley 3b, grupo pen_pct) |
| ❌ **Statikk Shiv** support | 0 heal/shield; su energized no proca Censer |
| ❌ **Full-AP** | El escudo R suma 50 % AP pero el daño Q/W/R suma bAD: la Niebla empuja a híbrido inclinado-AD, no full-AP |

---

## 7. RUNAS · HECHIZOS · HABILIDADES

### Keystone: Glacial Augment (support)
- **Por qué:** el slow de Glacial + el slow de Q (15 % + 10 %/100 bAD) dejan al objetivo dentro del radio 280 del root de W (1.3–2.2 s) y dentro de la línea de Q para el segundo impacto de Extraction.
- **Alternativa:** **Fleet Footwork** vs poke extremo (sustain de lane que Glacial no da); en DUO el motor prefiere **Lethal Tempo** (+10–12 % DPS sobre Fleet en la óptima: 1 326 vs 1 112).

### Orden de habilidades
- **Q → W → E** (R en 6/11/16): Q es cura+daño+−1 s de CD por auto; W es el setup; E es utility de equipo sin escalado numérico.

---

## 8. COMPARACIÓN CONTRA LAS ALTERNATIVAS

### Tabla maestra (Nivel 15, LT full, 100 stacks de Niebla)

| Build | Oro | 1v1 | 3v3 AoE | vs Tanque | Fuente |
|---|---|---|---|---|---|
| **Óptima DUO (Gunmetal + Runaan's Hurricane + Hexoptics C44 + Yun Tal Wildarrows + Blade of the Ruined King + Infinity Edge)** | 17 350 | **1 326** | **2 186** | **474** | ⭐ LAB (óptima) |
| **Top-2 (Gunmetal + Runaan's Hurricane + Essence Reaver + Yun Tal Wildarrows + Blade of the Ruined King + Infinity Edge)** | 17 450 | 1 317 | 2 162 | 471 | 🔬 LAB top-2 |
| **Top-3 (Gunmetal + Runaan's Hurricane + Statikk Shiv + Yun Tal Wildarrows + Blade of the Ruined King + Infinity Edge)** | 17 450 | 1 298 | 2 179 | 468 | 🔬 LAB top-3 |
| **Community DPS (Gunmetal Greaves + Statikk Shiv + Rapid Firecannon + Mortal Reminder + Infinity Edge + Guardian Angel)** | 17 450 | 810 | 810 | 319 | 🌐 comunidad |
| **Support valor-aliado (Crimson Lucidity + Essence Reaver + Ardent Censer + Black Cleaver + Harmonic Echo + Guardian Angel)** | 16 100 | n/a | n/a | n/a (cura 200 / escudo 480) | ⭐ LAB (support) |

### Desglose multiplicativo (óptima DUO vs community DPS)

| Factor | Multiplicador | Contribución |
|---|---|---|
| Crit 100 % vs 76 % (Niebla incluida) | ×1.19 | La community desperdicia el crit gratis solapándolo |
| Runaan's vs RFC (rayos que critican y aplican Relic) | ×1.35 (3v3) | El AoE de Senna son los rayos, no el energized |
| BotRK 6 % vida actual vs Mortal (sin grievous necesario) | ×1.15 vs tanque | Current-health no depende de su AD bajo temprano |
| **Neto** | | **+39 % DPS 1v1 efectivo** |

---

## 9. PLAN DE JUEGO

### Early (0:00 – 9:00)
- **Lane phase:** NO lasthees como support: cada minion grande que no matas = wraith garantizado (+1 Niebla). Lasthear = 3 % de chance.
- **Trade estándar:** Q (marca) → auto (consume Extraction) desde 625 de rango; el CD real de Q con AS 0.63 ≈ 9.2 s.
- **Min 4:30:** Ionian Boots; el haste acorta W (setup) y E (escape).

### Mid (9:00 – 16:00)
- **Pico ER (~8:00):** spellblade con 50–70 stacks ya pega 135 % AD base + ~30: ventana de agresión con W→auto.
- **Min 10:00:** ⬆️ Crimson Lucidity. Desde acá, rota con E: camuflaje de equipo para herald/dragón.
- **R como herramienta global:** ejecución + recolección de wraiths en toda la trayectoria + escudo pre-engage (castear ~1 s antes).

### Late (16:00+)
- **140+ stacks:** AD 229 sin ítems de AD, rango 730+, escudo R 480–560 por aliado. Asedio intocable: Q a través de ola y torretas (on-hit aplica a estructuras).
- **Teamfight:** posición EXTREMA atrás (570 HP), rota targets de Extraction (el CD es por objetivo), W a minion moribundo junto al carry enemigo = root AoE instantáneo.

### Reglas del parche que cambian el macro

| Regla | Impacto |
|---|---|
| Minions 60 % daño a campeones | Su poke de línea es seguro; el enemigo no puede responder igual |
| Placas permanentes + decaen desde 5:00 | Q a torre desde 625+ farmea placas sin exposición |
| Botas T3 solo desde 10:00 | Crimson estrictamente a las 10:00 (Ley 6) |

---

## 10. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS

### Fuentes primarias (mandan)

| Fuente | Acceso | Qué aporta |
|---|---|---|
| Notas oficiales 7.3 / 7.3a | 21/09 y 29/09/2026 | Sistema AS nuevo, nerf de ratio 7.3a, crit 90 %, R buff |
| Wiki oficial (WR:Senna + patch history) | 09/10/2026 | AD base 54 growth 0, rango 625, wind-up, economía de wraiths |

### Fuentes secundarias

| Fuente | Acceso | Fiabilidad |
|---|---|---|
| wr-meta.com (296-senna) | 09/10/2026 | Win rates S+ ambos roles (CSV del vigía) |
| Ficha analítica del autor (Senna 7.3a, 12/10) | 12/10/2026 | D1–D5, benchmarks de Niebla, sinergias/counters |

### Discrepancias detectadas y resolución

| Tema | Resolución |
|---|---|
| AD base 50 (wr-meta) vs 54 (wiki) | **54** (wiki V6.2c); sensibilidad −1 a −2 % DPS (⚠️ W1) |
| Relic on-hit +20 % AD vs +10 plano | **+20 % AD** (wiki); ranking de builds invariante (⚠️ W2) |
| `model/senna_model.py` citado por la ficha del autor NO existe en el repo | Reconstruido como spec `senna` en `dps_model.py` (v1.15.3): números del reporte = motor estándar, reproducibles con `optimize_build.py senna` |

### Validación del modelo

- `validate_slots(["Crimson","ER","Censer","Cleaver","Echo","GA"])` → **PASS** (6 entradas, 1 bota).
- `validate_slots(["Gunmetal","Runaan","C44","YunTal","BotRK","IE"])` → **PASS**.
- `optimize_build.py senna --top 6` reproduce la Tabla A2 (497 800 hojas legales podadas a 2 800).
- Sensibilidad free_crit 0 → 0.5: la óptima no cambia de ranking (el crit de ítems ya satura el cap): el umbral blando de la Ley 1 es informativo, no restrictivo.

---

## APÉNDICE A — POOL DE ÍTEMES DEL ROL: veredicto para Senna

| Ítem (oro) | Veredicto | Nota |
|---|---|---|
| Essence Reaver (3 000) | ✅ Core | Spellblade × crit gratis |
| Ardent Censer (2 400) | ✅ Core support | Buff proca con Q/R |
| Black Cleaver (3 000) | ✅ Core | HP + shred |
| Harmonic Echo (2 500) | ✅ Core | 2.º objetivo de cura/escudo |
| Guardian Angel (3 200) | ✅ Default 6.º | Revivir vs fragilidad |
| Redemption (2 450) | ⚠️ vs dive | Activo casteable muerta |
| Hexoptics C44 (2 900) | ✅ Core DUO | Magnification a 625+ |
| Blade of the Ruined King (3 100) | ✅ Core DUO | 6 % vida actual |
| Yun Tal Wildarrows (3 100) | ✅ Core DUO | Flurry post-7.3a |
| Runaan's Hurricane (2 650) | ✅ Core DUO | Rayos que critican |
| Infinity Edge (3 400) | ✅ DUO / ❌ support 1.er ítem | 207 % con mod 0.9 |
| Statikk Shiv (3 000) | ⚠️ DUO top-3 | Energized ≠ on-hit de Relic |
| Lord Dominik's / Mortal Reminder | ❌ juntos | Ley 3b |
| Rapid Firecannon | ⚠️ niche | +150 rango: asedio 850+; sin stats de pelea |

## APÉNDICE B — RUTAS DE COMPRA

```text
SUPPORT (valor-aliado):
Quest (0:00) → Long Sword (2:30) → Ionian (4:30) → Essence Reaver (8:00)
→ ⬆️ Crimson (10:00) → Ardent Censer (12:00) → Black Cleaver (15:00)
→ Harmonic Echo (17:30) → Guardian Angel (20:00)

DUO/ADC (motor):
Long Sword (0:00) → Berserker's (4:30) → Hexoptics C44 (7:30) → Yun Tal (10:30)
→ ⬆️ Gunmetal (11:30) → Blade of the Ruined King (14:30) → Runaan's (17:00)
→ Infinity Edge (20:00)
```

---

## Pie de página

*Reporte generado el 11/10/2026 con datos del parche 7.3 (21-sep-2026) + hotfix 7.3a (29-sep-2026). WR-LAB v1.15.3 (spec `senna` + `free_crit`). Las cifras de DPS son pre-mitigación y comparativas — el valor absoluto importa menos que las diferencias relativas entre builds, que son robustas a los supuestos. Si Riot publica un 7.3b/7.4, regenerar datos antes de republishar.*

**Referencias y créditos**
- Notas oficiales del parche 7.3 y 7.3a — © Riot Games, Inc. (wildrift.leagueoflegends.com). Fuente primaria de cambios sistémicos y de Senna.
- Wiki oficial WR:Senna + patch history — AD base, rango, wind-up, economía de Niebla.
- Win rates Diamond+ del 09/10/2026 — wr-meta.com vía `data/estructurada/champion_winrates.csv` (vigía del lab).
- Ficha analítica de Senna 7.3a del autor (12/10/2026) — discrepancias D1–D5 y benchmarks de Niebla.
- Modelo matemático, Leyes 0-7 y validaciones — WR-LAB (`model/dps_model.py` + `model/optimize_build.py`).

**Aviso legal:** Wild Rift y League of Legends son marcas registradas de Riot Games, Inc. Este documento es una guía de comunidad con fines educativos, **no está afiliada, patrocinada ni respaldada por Riot Games**. Los nombres de ítems, campeones y estadísticas pertenecen a sus respectivos dueños. El análisis y las conclusiones son trabajo original del autor apoyado en WR-LAB.
