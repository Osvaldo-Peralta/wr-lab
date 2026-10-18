---
tags:
  - Support
  - Enchanter
  - AP-Burst
  - Bot-Lane
version: 2.0
Status: Beta
champion: Yuumi
slug: yuumi
role: support
patch: "7.3+7.3b"
archetype: "AP-burst agresivo (Q/R)"
engine: yuumi-agresiva
custom: true
generate: manual
mode: sr
published_at: "2026-09-27"
updated_at: "2026-10-12"
verification: SIN_IMPACTO
verified_patch: "7.3b"
---
**Fecha del análisis:** 18/10/2026 (re-derivación v2.0 con motor `yuumi_agresiva_model.py`, batch5, constantes 7.3b)
**Parche:** 7.3 (21-sep-2026) + hotfix 7.3a (29-sep-2026) + hotfix 7.3b (15-oct-2026)
**Rol principal:** Support agresivo (custom): dañar con Q mejorada y R de 7 olas
**Arquetipo:** AP-burst de poke montado (Best Friend): el daño es Q/R + runas de daño, no autos
**Enfoque:** Maximizar daño de Q/R con maná y haste sostenibles: Imperial Mandate + Horizon Focus + Malignance + Stormsurge sobre botas de penetración, con Black Mist Scythe de quest. La curación pasa a segundo plano pero NO colapsa (R-heal 647, −4 % vs baseline enchanter).

> [!NOTE]
> **Estado Meta Actual (Diamond+, 17/10/2026):** SUPPORT Win Rate 48.23 % | Pick Rate 8.92 % | Ban 33.84 % | Tendencia ↓3 | Tier A (Confidence High). Fuente: `data/estructurada/champion_winrates.csv` (vigía 2×/día). Tras los nerfs 7.3/7.3a (HSP de W 6-9 % + 0.01 % AP) y el meta de engages rápidos, la Yuumi enchanter pura cayó de S a A: la variante agresiva existe precisamente para devolver impacto medible por oro.

> [!WARNING]
> **Runas publicadas en v1.2 eran ILEGALES en el cliente** (6 slots: Aery/Comet + Manaflow + Transcendence + Scorch + Revitalize). Un testeo en juego de un set parecido (Electrocute + Axiom + Transcendence + Gathering Storm + Cheap Shot) midió **CDs mayores a los publicados**: la página real no aceptaba Transcendence + Axiom a la vez (misma fila de árbol) ni la secundaria del árbol del keystone. La página de esta v2.0 está **verificada en cliente por el autor y un amigo (16/10)** y validada por `model/runas_wr.py` (reglas L1-L4).

> [!DANGER]
> **Sacrificio declarado vs baseline enchanter (Y1: Censer + Echoes + Staff + Redemption):** ADC+ **106 vs 248 (−57 %)** y Helia/E 0 (la cura por daño de Q desaparece). A cambio: Q-hit 275→**509 (+85 %)**, R-burst 1 409→**2 833 (+101 %)**, DPS sostenido 162→**332 (+105 %)**, y el escudo/curación propios casi no caen (E-shield 361, +2 %; R-heal 647, −4 %). Es una build de *impacto*, no de protección: si tu ADC necesita babysitting, jugá Y1.

---

## 0. RESUMEN EJECUTIVO

### Tabla A — BUILD FINAL (óptima agresiva batch5, 28 822 hojas legales)

| Slot | Ítem | Oro | Rol en la build |
|---|---|---|---|
| 1 (botas) | **Boots of Mana → ⬆️ Spellslinger's Shoes** (min 10:00, MISMO slot) | 2 200 | 35 AP + 18 pen plana + 8 % pen: la pen es el "crit" de Yuumi (Ley 1 adaptada) |
| 2 (quest) | **Spectral Sickle → ⬆️ Black Mist Scythe** (Tribute, mismo slot) | 0 | 10 AH gratis + oro pasivo: el slot de quest no compite |
| 3 | **Imperial Mandate** | 2 600 | Q slow/reveal marca siempre: Command +7 % daño aliado + 20 AH (Q/R son CC-abilities) |
| 4 | **Horizon Focus** | 2 700 | Hypershot ×1.10 a ≥600 u: tu Q cargada y R lo cumplen siempre (uptime 1.0/0.8) |
| 5 | **Malignance** | 2 700 | Scorn: −MR sostenido + 20 AH de R + Hatefog post-R; el amplificador de las 7 olas |
| 6 | **Stormsurge** | 2 800 | 90 AP + 15 pen plana + Squall: ejecuta lo que tu R dejó a <25 % |

> **Oro total: 13 000 g** (convención lab de support: quest 0 g + botas + 4) · **AP 375 · AH 80 (cdr 44 %) · pen 33 plana + 8 %** · **Q-CD 2.50 s · R-CD 29.5 s** · validate_slots PASS (1 bota + quest + 4).

### Tabla B — Ruta de compra cronológica

| # | Compra | Oro acum. | Minuto típico |
|---|---|---|---|
| 1 | **Spectral Sickle** (quest start) | 500 | 0:00 |
| 2 | **Boots of Speed** | 1 000 | ~3:00 |
| 3 | **Boots of Mana** (T2) | 2 200 | ~5:00 |
| 4 | Bandleglass Mirror + Blasting Wand → **Imperial Mandate** | 4 800 | ~8:00 |
| 5 | ⬆️ **Spellslinger's Shoes** (mismo slot, +1 000 g) | 5 800 | 10:00 (regla T3) |
| 6 | Blasting Wand + Fiendish Codex → **Horizon Focus** | 8 500 | ~12:30 |
| 7 | Blasting Wand + Codex + 600 → **Malignance** | 11 200 | ~15:00 |
| 8 | Blasting Wand + Void Amethyst + Aether Wisp → **Stormsurge** | 13 500 | ~18:00 |

### Runas · Hechizos · Habilidades (página LEGAL verificada en cliente 16/10)

| Categoría | Elección |
|---|---|
| Keystone | **Electrocute** (7.3b: 60-210 + 10 % bAD + 5 % AP; tu Q cargada + auto attachado lo procan solos) |
| Dominación 1 | **Cheap Shot** (7.3b: CD 5 s; el slow/reveal de Q lo activa con uptime ~100 %: 45 verdadero/5 s) |
| Hechicería 2 | **Transcendence** (+10 AH y el −8 % CD post-hit del nivel 9: es tu "manaflow" de haste) |
| Precisión 3 | **Coup de Grace** (+8 % a <40 % HP: sinergia con Squall de Stormsurge y las olas de R) |
| Secundaria | **Gathering Storm** (Inspiration: árbol libre — +16 AP al min 18; el árbol Sorcery ya está usado por Transcendence, regla L4) |
| Hechizos | **Flash + Ignite** (ejecución post-poke) · **Flash + Exhaust** vs dive |
| Skills | **Q > E > W** (R en 6/11/16): Q maxea el poke; E sostiene el attach; W solo 1 punto early |

### Resultado del modelo (nivel 15, min 20, MR 50 squishy / MR 150 tanque, runas de la Tabla)

| Escenario | Óptima agresiva v2.0 | Poke-híbrida publicada v1.2 | Y1 enchanter (baseline lab) |
|---|---|---|---|
| **Q-hit (poke cargado)** | **509** | 339 | 275 |
| **Q-DPS sostenido** | **204** | 152 | 102 |
| **R-burst (7 olas)** | **2 833** | 1 748 | 1 409 |
| **DPS sostenido total** | **332** | 240 | 162 |
| **vs Tanque (MR 150)** | **184** | 142 | 101 |
| **E-shield / R-heal** | 361 / 647 | 301 / 742 | 354 / 672 |
| **ADC+ (Censer)** | 106 | 90 | 248 |

> **Titular:** la v2.0 gana a la publicada en todo el eje de daño (**+50 % Q-hit, +62 % R-burst**) con el mismo oro, porque corrige dos errores de la v1.2: botas de penetración desde el slot 1 (la pen plana de Spellslinger multiplica Q/R enteros) y el doble amplificador Mandate+Horizon que la v1.2 dividía con Echoes/Harmonic. El costo real es único y declarado: el buff de AS al ADC (−57 %).

### 0.3 ¿Por qué esta build funciona para "dañar con Q"?
- **Q mejorada rank 4 = 340 + 35 % AP** y se castea GRATIS estando attachada (Best Friend): cada 2.5 s (cdr 44 %) es un misil de 509 con pen de 33+8 %.
- **R de 7 olas con Wave Damage Stacks:** Σ = 7×(120+15 % AP) + 21×(40+5 % AP) = 1 680 + 2.10×AP → con 375 AP = **2 467 base + amps** (Malignance ×1.04, Hypershot 0.8, Mandate ×1.07): 2 833 medidos.
- **Electrocute + Cheap Shot** convierten cada Q cargada en ~105 daño verdadero/mágico extra por ventana de 5 s: las runas de daño suman ~18 % del Q-hit (antes, las runas de la v1.2 sumaban sustain que esta build no usa).

---

## 1. LEYES APLICADAS A YUUMI AGRESIVA

- **Ley 0 — Slots:** 6 entradas (botas T3 + quest + 4); la quest vive en su slot propio y no compite. PASS.
- **Ley 1 adaptada — Penetración = crit del mago:** 33 plana + 8 % (Spellslinger) + 15 (Stormsurge) + Scorn de Malignance (−MR sostenido): contra MR 50, el paquete de pen vale +27 % de daño efectivo de Q/R; sin botas de pen (v1.2 con Crimson) se perdían 18 puntos de pen plana.
- **Ley 2 adaptada — Haste = frecuencia de Q:** AH 80 → Q-CD 2.50 s y R-CD 29.5 s: cada punto de AH por encima de 60 rinde +0.9 % de daño minuto a minuto (medido en el motor).
- **Ley 3b:** sin ítems de pen física porcentual en el pool (grupo pen_pct ajeno a AP) — no aplica.
- **Ley 5-6 — Timing:** Mandate al min 8 (su Command necesita un slow: tu Q lo da desde lvl 1); Spellslinger estricto a las 10:00 (regla T3); Malignance antes que Stormsurge si el enemigo tiene 2+ curas (GW de Scorn).

---

## 2. ANÁLISIS DEL PRIMER ÍTEM COMPLETADO

| Candidato (post-quest) | Veredicto | Números del motor (min 8, lvl 9) |
|---|---|---|
| **Imperial Mandate** | ✅ **Core 1** | Command +7 % en cada Q marcada (uptime 100 %) + 20 AH: +9 % de daño de equipo desde 2 600 g |
| **Horizon Focus** | ✅ Core 2 | Hypershot ×1.10: sin él, el R-burst cae 8 % |
| **Echoes of Helia** | ⚠️ Solo híbrida | Convierte 30 % del daño en cura: en la óptima agresiva su oro rinde menos que Malignance (−6 % R-burst pero +18 % E-shield): ver variante [!TIP] |
| **Luden's Echo** | ❌ | Su proc compite con el misil de Q por el mismo objetivo ya marcado; sin pen ni AH de CC: −7 % Q-DPS vs Mandate |
| **Riftmaker** | ❌ | Omnivamp sin daño de auto: el_void corr multiplica daño que Yuumi casi no sostiene |

---

## 3. BUILD FINAL RANURA POR RANURA

Ver Tabla A. Notas por slot:
- **Spellslinger's Shoes:** 18 pen plana early = +11 % de Q-hit contra MR 50 al min 10; el 8 % porcentual escala con Malignance.
- **Mandate:** tu Q slow/reveal SIEMPRE marca (no requiere inmovilización completa en WR 7.3): Command proca por cast, no por segundo.
- **Horizon:** el misil de Q viaja ≥1 s y pega a ≥600 u cargada: Hypershot uptime 1.0 en poke, 0.8 en R (olas lejanas).
- **Malignance:** Scorn −MR en área + Hatefog (180 + 15 % AP) tras R: el único ítem que amplifica las 7 olas completas.
- **Stormsurge:** Squall a <25 % HP cierra lo que el R dejó vivo; 6 % MS para reposicionar el attach.

### Matriz del último slot (situacional)

| Situación | Slot 6 | Impacto medido |
|---|---|---|
| Default daño | **Stormsurge** | Q-DPS 204 · R 2 833 ✅ |
| Vs 2+ curas | **Malignance duplicada no: Morellonomicon** | GW 50 %: −8 % R-burst por el swap ⚠️ |
| Híbrida con cura de equipo | **Echoes of Helia por Stormsurge** | E-shield 418 (+18 %) · R-heal 738 (+10 %) · ADC+ 277 con Censer en slot 3 ([!TIP]) |
| Vs burst mágico | **Maw of Malmortius**? fuera de pool AP | declarar: jugá Y1 enchanter |
| Oro adelantado (ventaja) | **Rabadon's Deathcap** por Stormsurge | +AP puro: R 2 900 pero sin ejecución Squall ⚠️ |

### RECHAZADOS (con motivo numérico)
| Ítem | Motivo |
|---|---|
| ❌ **Echoes of Helia + Ardent Censer juntos** en agresiva | El motor los mide como redundantes: la cura de Helia escala con daño que esta build ya no spamea (shld/min 4 330 vs 5 431 de la poke v1.2, pero con −35 % de R-burst) |
| ❌ **Crimson Lucidity** | Sin pen: Q-hit 509 → 431 (−15 %) con el mismo AH |
| ❌ **Staff of Flowing Waters** | El buff de AS al ADC no se usa si tu plan es pokear montada: 0 sinergia con Q/R |
| ❌ **Warmog's / Locket** | Umbral 7.3b de Warmog (1 250 HP bonus) inalcanzable para Yuumi; Locket es valor de teamfight que esta build delega |

---

## 4. RUNAS · HECHIZOS · HABILIDADES

### Por qué Electrocute y no Aery/Comet en 7.3b
- **Electrocute (60-210 + 10 % bAD + 5 % AP, CD 20-13 s):** con Q-CD 2.5 s y auto attachado, el proc es cada ~2_procs de Q = una vez por trade de 6 s: ~35 % del Q-hit early cuando más importa (lane).
- **Arcane Comet** quedó sin su sinergia de "Q cargada gratis" tras el nerf de maná de 7.3a: el cometa consume el mismo maná que ya no sobra.
- **Aery** es la opción de la Y1 enchanter (escuda con cada cura): en agresiva, su escudo 20-100 (nerf 7.3b) no compite con 210 de Electrocute.

### La página ilegal de v1.2, explicada (post-mortem)
La v1.2 publicaba Aery/Comet + Manaflow + Transcendence + Scorch + Revitalize = **keystone + 4 runas + secundaria (6 slots)**: el cliente acepta 5. Al reconstruirla en juego, el slot que caía era Transcendence o Scorch → **menos AH o menos daño del declarado**, y en la variante con Axiom + Transcendence (misma fila de árbol) caía una de las dos → **CDs reales mayores que los publicados** (medido por el amigo del autor: Q ~3.1 s vs 2.5 s teóricos). Reglas formales ahora en `model/runas_wr.py` (L1-L4) con test de los 5 sets reales.

---

## 5. COMPARACIÓN CONTRA ALTERNATIVAS

| Build | Oro | Q-hit | R-burst | ADC+ | Score agresivo | Fuente |
|---|---|---|---|---|---|---|
| **Óptima v2.0 (Tabla A)** | 13 000 | **509** | **2 833** | 106 | 84.9 % | ⭐ LAB (batch5) |
| Híbrida balanceada (Scythe + Spellslinger + Censer + Echoes + Mandate + Rabadon) | 13 000 | 412 | 2 169 | **277** | 78.4 % (peso aliado .51) | 🔬 LAB top-N |
| Poke-híbrida publicada v1.2 (Echoes + Mandate + Stormsurge + Harmonic) | 12 300 | 339 | 1 748 | 90 | — | 📌 publicada |
| Y1 enchanter (Censer + Echoes + Staff + Redemption) | 11 650 | 275 | 1 409 | **248** | — | 📌 baseline lab |

### Desglose de la diferencia (v2.0 vs v1.2 publicada)
| Factor | Contribución |
|---|---|
| Spellslinger desde slot 1 (pen 33+8 vs Crimson 0) | +15 % Q-hit |
| Malignance (Scorn + Hatefog en R) | +9 % R-burst |
| Horizon Focus (Hypershot 1.0/0.8) | +8 % Q y R |
| Runas de daño legales (Electrocute/Cheap Shot vs Aery/Scorch ilegales) | +6 % early |
| **Neto medido** | **+50 % Q-hit · +62 % R-burst** |

---

## 6. PLAN DE JUEGO

### Early (0:00 – 8:00)
- **Attach al carry de poke** (Caitlyn/Jinx/Varus-like): Q cargada cada 4-5 s + Electrocute en el trade 2 y 4.
- **Quest primero que componentes:** los executes de Tribute (Spoils) pagan Mandate al min 8.
- **Manaflow no existe en esta página:** gestiona maná con Q SOLO cargada (castear sin carga cuesta el doble por impacto).

### Mid (8:00 – 14:00)
- **Mandate + Spellslinger = ventana de ejecuciones:** el carry enemigo a <40 % activa Coup de Grace + Squall de Stormsurge (min 18) o el execute de R.
- **R como zoning de objetivos:** 7 olas en área = 2 833 repartidos; castealo PRE-engage (el viaje de las olas es lento).

### Late (14:00+)
- **Gathering Storm online (+16 AP/min 18):** el Q-hit cruza 540; el side-poke tuyo quita un tercio de squishy por trade.
- **No pelees sin attach:** 500 HP base y cero escapes: tu posición ES tu carry.

### Regla de Oro
Si al min 10 tu ADC está 0/2 o el jungla enemigo campea bot: **convertite a la híbrida** ([!TIP]: Censer + Echoes por Stormsurge + Malignance) — el motor la puntúa 78.4 % con ADC+ 277: pierdes 18 % de R-burst y recuperas el juego.

### Reglas del parche que cambian el macro
| Regla | Impacto |
|---|---|
| 7.3b: Electrocute 60-210 | El keystone agresivo rinde +20 early vs 7.3a |
| 7.3b: Cheap Shot CD 5 s | True-damage casi permanente sobre Q-mark |
| 7.3b: Aery 20-100 | Enchanter puro ligeramente nerfeado: la híbrida gana valor relativo |
| 7.3: torretas 7 000 HP | Tu poke de torre con Q attachada es de los pocos que escala sin AD |

---

## 7. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS

### Fuentes primarias
| Fuente | Acceso | Qué aporta |
|---|---|---|
| Notas oficiales 7.3/7.3a/7.3b | 21/09, 29/09, 15/10/2026 | Q/R valores, HSP de W 7.3a, Electrocute/Cheap Shot/Aery 7.3b |
| Cliente WR (testeo del autor + amigo) | 16/10/2026 | Legalidad de la página de runas y CDs reales con ella |
| items_7.3.csv + diff 7.3b | vigía | Precios y stats del pool (Locket/Warmog/Statikk/Yun Tal/Youmuu 7.3b) |

### Discrepancias y erratas
| # | Tema | Resolución |
|---|---|---|
| D-v2.1 | Página de runas v1.2 ilegal (6 slots) | Reemplazada por la página verificada en cliente; reglas L1-L4 en `model/runas_wr.py` |
| D-v2.2 | Cifras de daño v1.2 ("Q ~120-150", "haste 65-75") sin motor | Re-derivadas con batch5: Q-hit 509 con pen completa; AH 80 |
| D-v2.3 | R de 7 olas: stacking por ola impactada | Interp B default (Σ 1 680 + 2.10×AP); interp A conservadora = 1 080 + 1.35×AP (−38 %): rankings sin cambio |
| D-v2.4 | Q mejorada: misil ≥1 s de viaje | Poke attachado estándar (uptime 1.0); sin attach, el misil falla más: declarado |

### Validación del modelo
- `python3 model/yuumi_agresiva_model.py` reproduce todas las tablas (28 822 hojas legales, presupuesto 13 000 g, Ley 0 y L1-L4 de runas aplicadas).
- Baseline Y1 replicado: e_shield 353.9 / r_heal 671.9 / shld-min 4 365 (fixture de tests del lab: 338.8/650.7/3 953 con sus runas originales).
- `tests/test_yuumi_agresiva.py`: legalidad de runas de la Tabla, presupuesto, y sacrificio acotado (ADC+ ≥ 90 y R-heal ≥ 600).

---

## APÉNDICE A — POOL AP DE SUPPORT: VEREDICTOS

| Ítem (oro) | Veredicto | Nota |
|---|---|---|
| Imperial Mandate (2 600) | ✅ Core 1 | Command con Q slow siempre |
| Horizon Focus (2 700) | ✅ Core 2 | Hypershot 1.0/0.8 |
| Malignance (2 700) | ✅ Core 3 | Scorn + Hatefog en R |
| Stormsurge (2 800) | ✅ Default 6.º | Squall de ejecución |
| Spellslinger's Shoes (2 200) | ✅ Botas | Pen = crit del mago |
| Echoes of Helia (2 400) | ⚠️ Híbrida | Cura por daño de Q |
| Ardent Censer (2 400) | ⚠️ Híbrida | ADC+ 277 en la híbrida |
| Rabadon's Deathcap (3 400) | ⚠️ Ventaja | +AP sin utilidad |
| Luden's / Riftmaker / Crimson | ❌ | Ver §2/§3 |

## APÉNDICE B — RUTA HÍBRIDA DE EMERGENCIA
```text
Quest (0:00) → Boots of Mana (5:00) → Mandate (8:00) → ⬆️ Spellslinger (10:00)
→ Censer (12:30) → Echoes (15:00) → Rabadon (18:30)   [ADC+ 277 · R-heal 738]
```

---

## Pie de página

*Reporte re-derivado el 18/10/2026 con `model/yuumi_agresiva_model.py` (batch5) sobre 7.3+7.3a+7.3b. WR-LAB v1.20. Runas verificadas en cliente 16/10; números de daño pendientes de verificación propia en juego (verification: pending). Si Riot publica 7.3c/7.4, regenerar antes de republishar.*

**Referencias y créditos**
- Notas oficiales 7.3/7.3a/7.3b — © Riot Games, Inc. (wildrift.leagueoflegends.com).
- Win rates Diamond+ del vigía (17/10/2026) vía `data/estructurada/champion_winrates.csv`.
- Testeo en cliente del autor y colaborador (16/10/2026): legalidad de runas y CDs reales.
- Motor batch5 y búsqueda: `model/yuumi_agresiva_model.py` + `model/yuumi_agresiva_resultados.txt`.

**Aviso legal:** Wild Rift y League of Legends son marcas registradas de Riot Games, Inc. Este documento es una guía de comunidad con fines educativos, **no está afiliado, patrocinado ni respaldado por Riot Games**. Los nombres de ítems, campeones y estadísticas pertenecen a sus respectivos dueños. El análisis y las conclusiones son trabajo original del autor apoyado en WR-LAB.
