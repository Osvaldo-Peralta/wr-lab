---
tags: [wrlab, ficha, senna, support, adc, dragon-lane, crit-modificado, parche-7.3a]
version: 1.0
Status: Borrador (entregado 12/10/2026 — pendiente de verificación en juego del autor)
champion: Senna
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — SENNA (Wild Rift 7.3 + hotfix 7.3a)

**Fecha:** 12/10/2026 · **Fuentes:** WR-LAB v1.15 (primaria) + notas oficiales 7.3/7.3a + wiki oficial + wr-meta/wildriftfire/wildriftcore (11/10/2026)
**Roles:** Support (S+) / ADC-Dragon en dúo (S+) · **Arquetipo lab:** Crítico modificado (`crit_dmg_mod` 0.9) + enchanter híbrido
**Tesis:** Artillera de asedio con escalado infinito de Niebla (AD + crítico + rango gratis). Su daño es poke/burst por ventanas, NO DPS sostenido: las kills las habilita (root, escudo global, cura, camuflaje) más de lo que las cierra.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, 09–11/10/2026):** SUPPORT S+ · WR 53.63–54.11 % · pick ~13 % · **ban 34.6–38 %** (Confidence High, señal ⛔ Perma-ban) · DUO S+ · WR 55.16–55.58 % · pick ~3.4 % (Confidence Med). wildriftcore: WR 30 d 53.95 % (+1.81 pts); el ajuste 7.3a le midió **−1.81 pts en 10 días** y sigue S+.

---

## 1. QUÉ LE HIZO ESTE PARCHE (por qué la banea 1 de cada 3 partidas)

### 1.1 Cambios 7.3 (21-sep-2026, notas oficiales — verificados por el lab)

| Stat / Habilidad | Antes | Ahora | Impacto |
|---|---|---|---|
| HP base | 600 | **570** | Más frágil en lane (−5 %) |
| Sistema AS (nuevo) | AS restringida | ratio 0.4 · base 0.4 · BBA 0.6 · growth 0.05 | **Riot le quitó la restricción de AS** → los ítems de AS pasaron a funcionarle |
| Pasiva: daño por vida actual | 1.2–12 % | **1–10 %** | Nerf al trade |
| Pasiva: crit por 20 Niebla | 15 % | **10 %** | Escalado de crit más lento |
| **[Nuevo] Daño crítico** | 141.75 % (sistema viejo) | **90 % del crítico normal = 180 % (207 % con IE)** | **BUFF ENORME disfrazado de nerf**: su crit gratis de Niebla pasó de pegar 141.75 % a 180–207 % |
| Q base | 50/90/130/170 | **50/80/110/140** | Poke early −11 % (ranks 2-4) |
| R daño | 250/375/500 +120 % bAD +50 % AP | **250/400/550 +120 % bAD +70 % AP** | BUFF: ejecutora global y híbrida AP |
| R escudo | 120/160/200 +40 % AP + Niebla×4 | **120/160/200 +50 % AP + Niebla×2** | Menos escala-Niebla, más escala-AP |

### 1.2 Hotfix 7.3a (29-sep-2026) — el ajuste

Cita oficial: *"Senna has been overperforming across all skill levels **since we removed her Attack Speed restrictions**. We're adjusting her Attack Speed ratio to rein in how effectively she scales with Attack Speed."*

| Parámetro | 7.3 | 7.3a | Efecto real |
|---|---|---|---|
| AS ratio / AS base | 0.4 / 0.4 | **0.3 / 0.3** | Cada 1 % de AS de ítems rinde 0.3 % (antes 0.4 %) |
| Base Bonus AS | 0.6 | **1.1** | Compensación early: AS lvl 1 ≈ 0.63 (similar) |
| AS por nivel | 0.05 | **0.025** | Lvl 15 sin ítems: 0.735 (era ~0.92 con valores 7.3) |
| Wind-up | la AS bonus lo reduce | **lo reduce menos** | Autos y Q cast más lentos con AS alta |

**AS efectiva resultante (fórmula oficial 7.3):** lvl 1 = 0.63 · lvl 15 sin ítems = **0.735** · lvl 15 con build full-AS (Gunmetal+Statikk+RFC+Alacrity) = **1.16** · techo absoluto con LT full = ~1.45. Para tocar el cap 3.0 necesitaría **+755 % de AS bonus: imposible por diseño.** Una Yunara/Jinx pelean a 2.2–2.6.

---

## 2. FICHA MATEMÁTICA (spec 7.3a)

| Parámetro | Valor | Fuente |
|---|---|---|
| HP | **570** (+120/niv → 2 250) | notas 7.3 (lab §7.2) |
| AD base | **54 · growth 0** (¡nunca sube por nivel!) | wiki V6.2c ⚠️ D1: wr-meta/wildriftfire muestran 50 (stale) |
| Armadura / RM | 35 (+4.5) / 30 (+1.4) | wiki |
| Maná / regen | 345 (+65) / 21 (+0.5) | wiki |
| MS | 340 | wiki V4.2 |
| **Rango de ataque** | **625** (+15 cada 20 Niebla, cap +400 → 1 025 teórico) | wiki V4.2 |
| AS (7.3a) | ratio **0.3** · base **0.3** · BBA **1.1** · growth **0.025** | notas oficiales 7.3a (override del lab) |
| Daño crítico | **0.9×** → 180 % base / **207 % con IE** | notas 7.3 |
| Proyectil | Non-projectile (hitscan) · wind-up 0.5 s en lvl 1, no cancelable con habilidades (6.3) | wiki |
| `crit_dmg_mod` motor | 0.9 | tabla de arquetipos lab §C |

**AD lvl 15 real = 54 + 1.25×Niebla + ítems.** Con 140 de Niebla: 54 + 175 = 229 AD **sin comprar un solo ítem de AD**.

---

## 3. PASIVA — ABSOLUTION (el campeón entero vive aquí)

### 3.1 Relic Cannon
- El auto tarda más en disparar (wind-up largo; **no se cancela casteando** desde 6.3). La AS bonus reduce el wind-up (menos desde 7.3a).
- On-hit bonus físico: **20 % AD** (wiki) ⚠️ D2: wr-meta dice "+10 plano" → verificar en juego; el ranking de builds NO cambia entre ambas (sensibilidad medida: −5.4 % DPS con +10 plano).
- **Roba 10/15/20 % de la MS del objetivo** (según nivel) por 0.5 s → kiting vs comps rápidas.
- Críticos al 90 % del daño crítico normal.

### 3.2 Living Extraction
- **Autos Y habilidades dañinas marcan** campeones 4 s; el siguiente impacto consume la marca: **+1 Niebla + 1–10 % de la vida actual como daño físico** (según nivel), CD ~6 s por objetivo.
- Funciona **incluso haciendo 0 de daño** (invulnerables incluidos) — wiki.
- Combo base: Q (marca) → auto (consume), o W (marca) → Q (consume). En teamfight: **rotar objetivos** (el CD es por target) = 3 extracciones en la misma pelea.

### 3.3 Soul Reap (economía de Niebla — la parte que MÁS se juega mal)
| Fuente | Wraiths |
|---|---|
| Campeón enemigo muerto cerca | **siempre** |
| Monstruo grande / épico | siempre / **2** |
| Minion que **NO** mata Senna | **más chance** (los grandes: **siempre**) |
| Minion que Senna mata (last hit) | **solo 3 %** |
| Minion ejecutado por Tribute aliado (Spoils) | 4.166 % |
| Recogida | auto/Q/R los mata (+3 oro); los que expiran a ≤750 se auto-absorben (6.3) |

> [!TIP]
> **Regla de oro support:** NO lasthees. Cada minion grande que no matas = 1 Niebla garantizada. Lasthear reduce tu escalado. La R además **recoge wraiths en toda su trayectoria global** (stacks desde base enemiga) — castea R aunque no haga falta el daño.

### 3.4 Niebla (stacks infinitos)
- **+1.25 AD bonus** por stack (alimenta ratios bAD de Q/W/R y el on-hit de la pasiva).
- Cada **20 stacks**: **+15 rango** y **+10 % crítico** (7.3: era 15 %). Caps: +400 rango, 100 % crit de Niebla.
- **Exceso de crítico >100 % → 35 % se convierte en Physical Vamp.** En Senna el overcap NO es oro muerto (Ley 1: umbral blando) — pasarse de 100 % crit compra sustain.
- Benchmarks declarados (guías wildriftcore + reglas de drop; ⚠️ verificar en juego): support ≈ 50 (11 min) / 90 (14 min) / **140 (18 min)** / 180+ (22 min); ADC ≈ 35 / 65 / **110** / 150 (lasthear frena el drop).

---

## 4. HABILIDADES (valores 7.3/7.3a) Y MECÁNICAS EXPLOTABLES

### Q — Piercing Darkness · CD 15 s · 70/80/90/100 maná
Láser de 1 300 que **atraviesa todo**: **50/80/110/140 + 60 % bAD** físico · slow **15 % + 10 %/100 bAD + 6 %/100 AP** (0.75–1.5 s) · **cura aliados en línea (ancho 280): 40/70/100/130 + 40 % bAD + 25 % AP**.
- **Cada auto/on-hit baja 1 s su CD** → en pelea continua (AS 1.2) el CD real ≈ 15/(1+1.2) ≈ **6.8 s**; con haste 30 ≈ 5.9 s.
- Cast time = 80 % del wind-up → mejora con AS/nivel.
- **Aplica on-hit a campeones Y torretas** (BotRK/Terminus procan con Q; siegue con on-hit) y cuenta como auto a torretas/wards/wraiths. Spell shield enemigo NO bloquea los on-hit.
- Golpea a través de la ola: daño gratis + cura a tu ADC detrás de los minions.

### W — Last Embrace · CD 11 s · rango 1 300
**90/155/220/285 + 70 % bAD** al primer enemigo; se adhiere 1 s → **root en área (280) de 1.3/1.6/1.9/2.2 s**.
- ⚡ **Si el objetivo MUERE, el root detona de inmediato** (wiki) → **W a un minion moribundo junto al enemigo = root AoE instantáneo sin el delay**.
- Desde la E (camuflaje) el proyectil es invisible: indodgeable.
- Spell shield y proyectiles la bloquean (no es hitscan).

### E — Curse of the Black Mist · CD 22/20/18/16 s · cast 1 s (movible)
Senna = Wraith **camuflada** 6–7.5 s (si la revelan, **re-camufla a los 1.75 s**); aliados dentro → *Wraith Form*: camuflaje + **intargeteables** + identidades ocultas en el minimapa + **+20 % MS**.
- Engages "fantasma" de Baron/dragón, escapes, flanqueos de W a quemarropa.
- **La R la revela durante el cast** → R primero o después, no durante el stealth.
- Su única defensa real con 570 HP: MS + intargeteable + reposicionamiento.

### R — Dawning Shadow · CD 85/80/75 s · GLOBAL
Dos ondas: **central** = **250/400/550 + 120 % bAD + 70 % AP** + revela 3 s + **recoge wraiths del camino**; **ancha** = **escudo a Senna y aliados 120/160/200 + 50 % AP + 2×Niebla** (3 s).
- Con 140 de Niebla: escudo **480–545** por aliado; con 180: **560–632**. Castéalo **~1 s antes del engage** (el escudo dura 3 s).
- Ejecución cross-map (velocidad 17 000: casi instantánea), anti-stealth (revela), y farmea Niebla global.

---

## 5. ¿CON QUÉ ESCALA SENNA? (respuesta por stat)

| Stat | ¿Escala? | Números |
|---|---|---|
| **AD** | ✅ **PRIMARIO E INFINITO** | AD base 54 fijo → TODO es bonus: Niebla ×1.25 + ítems. Ratios: Q 60 % bAD · W 70 % bAD · R 120 % bAD · on-hit pasiva · slow de Q (+10 %/100 bAD). 140 Niebla = +175 AD gratis. |
| **Crítico** | ✅ **ÚNICO (gratis + sin desperdicio)** | +10 %/20 stacks sin comprar nada; ×1.8 (×2.07 con IE); exceso → 35 % Physical Vamp. Llega a 100 % crit con 1–2 ítems. |
| **AP** | ⚠️ **HÍBRIDO SECUNDARIO (buffeado en 7.3)** | R daño 70 % + escudo 50 % · cura Q 25 % · slow Q 6 %/100. Statikk (40 AD/40 AP) y ER-spellblade la hacen híbrida natural. Full-AP = extremo; híbrido inclinado-AP potencia el lado enchanter. |
| **AS** | ❌ **LIMITADA (nerfeada en 7.3a)** | Ratio 0.3 → techo real ~1.2–1.45. Su valor: acorta wind-up y cast de Q, y acelera el −1 s de CD de Q por auto. Riot nerfeó esto exacto en 7.3a. Ley 2 no aplica igual (caso Jhin). |
| **MS** | ⚠️ **UTILIDAD (no daño)** | E +20 %, robo pasivo 10–20 % de la MS del objetivo, ítems (RFC/Galeforce/Statikk +4 %). Es su supervivencia: posicionamiento = EHP real. |

---

## 6. CURVA DE PODER Y LECTURA DE ROLES

- **Early (0–9 min):** débil. AD 54 + AS 0.63 + 570 HP. Ganas la lane con trades de Extraction (Q→auto) y rango 625, no con all-ins.
- **Mid (9–16 min):** umbral 60–100 Niebla (+75–125 AD, +30–50 % crit, rango 670–700). Empieza el asedio fuera del alcance enemigo.
- **Late (16+):** 140–200 Niebla: AD 230–300 sin ítems, crit ~100 % con 1–2 ítems, rango 730–775 (850+ con RFC energized), escudo de R 500–630 por aliado. Escalado infinito.
- **Por qué "mucho daño, pocas kills" como ADC:** DPS sostenido capado (AS ~1.2 vs 2.2–2.6 de una ADC normal) + perfil de poke que ablanda pero no ejecuta. Las kills viven en ventanas: **W(root) → Q+auto crit → R**, o en dúo coordinado (su WR más alto: 55.16–55.58 % DUO). Como support, el daño lo pones tú y las kills se las lleva tu carry — el equipo gana igual: S+ con confianza High.
- **Sinergias (wildriftcore):** **Jhin (Ideal:** root W → 4.º tiro/trampa garantizados; dobles ultis globales), **Jarvan IV (Ideal)**, **Ashe/Maokai (Fuerte:** cadenas de CC). **Counters:** Blitzcrank (Hard), Thresh, Malphite — dive/engage instantáneo la borra antes de que reposicione.

---

## 7. SOBREEXPLOTACIÓN — LAS 9 PALANCAS (resumen ejecutivo)

1. **No lasthees como support** (wraiths garantizados de minions grandes ajenos).
2. **Ciclo Extraction por objetivo** (habilidad marca → auto consume; rota targets en teamfight).
3. **W + minion moribundo = root instantáneo** (sin delay de 1 s) desde 1 300 de rango.
4. **Motor de Q:** −1 s/auto; a través de ola y torretas (on-hit + placas + cristales desde la niebla).
5. **Economía de crit exacta:** 100 stacks (50 %) + IE+RFC (50 %) = 100 % justos; el exceso → vamp (overcap deliberado es válido).
6. **R triple uso:** ejecución global + escudo pre-engage (500+) + recolección global de Niebla.
7. **Rango creciente:** 625 → 700+ (Niebla) → 850 energized (RFC): siege intocable.
8. **E de equipo:** intargeteable + camuflaje + 20 % MS → engages y escapes imposibles.
9. **Robo de MS pasivo** vs comps rápidas.

---

## 8. BUILDS DERIVADAS POR EL MOTOR (resumen — detalle en el reporte)

> Modelo propio `model/senna_model.py` (batch3): autos×crit0.9 + Relic + Extraction + Q/W en rotación + valor-aliado. Optimización exhaustiva bajo Leyes 0/1/3b, presupuesto y checkpoints 9/12/15.

| Rol | Build óptima (motor) | Score | Evidencia |
|---|---|---|---|
| **DUO/ADC** | Gunmetal + **BotRK** + IE + Runaan's + Kraken + **Terminus** (17 250 g) | 0.950 | 1v1 **1 749** (Fleet) / **1 931** (LT) · 3v3 3 086/3 317 · vsTanque 806/881. Meta comunidad (Statikk+RFC+Mortal+IE+GA): **−43 % off** (0.567). |
| **SUPPORT** | Gunmetal + Scythe + **Ardent Censer** + **Essence Reaver** + **Black Cleaver** + **IE** (14 000 g) | 0.834 | 1v1 1 176 · vs120 639 · Q-cura 59 hps · R-escudo 545 · **+164 DPS al ADC** (Censer). Meta (Cleaver/RFC/IE/Mortal): 0.651. |

Hallazgos del motor (detallados en el reporte): **BotRK 1.er ítem duo** (su 6 % vida actual no depende de su AD bajo); **ER core support** (spellblade = 135 % AD base + **80 a 100 % crit** → su crit gratis lo maximiza; AH 20 acelera Q/W); **LT > Fleet en daño puro** (+10–12 %) pero Fleet = sustain de lane; **Cleaver 6.º slot support** empata el score ofensivo con Runaan's y gana en cura/HP/shred-de-equipo/robustez.

---

## 9. DISCREPANCIAS REGISTRADAS (protocolo lab §D)

| # | Tema | Resolución |
|---|---|---|
| D1 | AD base: 50 (wr-meta/wildriftfire) vs **54** (wiki V6.2c) | Usar 54; Δ DPS ≈ 1–2 % (sensibilidad corrida: S1 991→980 con AD 50). Verificar en juego |
| D2 | Relic on-hit: **20 % AD** (wiki) vs +10 plano (wr-meta) | Wiki primaria; sensibilidad: −5.4 % DPS con +10 plano, rankings sin cambio |
| D3 | Wiki muestra pasiva pre-7.3 (1.2–12 %, 15 %/20) | Mandan notas oficiales 7.3: **1–10 %, 10 %/20** ✅ ya en el lab |
| D4 | Wiki AS block muestra ratio 0.125 (pre-7.3) | Mandan apéndice 7.3 + override 7.3a: **0.3/0.3/1.1/0.025** ✅ |
| D5 | Navori "Deft Strikes" (−15 % CDs restantes por auto) | Convención lab D8 (Xayah): CD efectivo ×0.75. Sensibilidad ×1.0 corrida: la build support cambia pero el arquetipo (Censer+ER+ Cleaver) se mantiene |

---

## Pie de página
Fuentes: WR-LAB completo v1.15 (metodología, diffs 7.3/7.3a, win rates vigía 09/10) · wildrift.leagueoflegends.com (notas 7.3 y 7.3a) · wiki.leagueoflegends.com/WR:Senna (+Patch history) · wr-meta.com/296-senna (11/10) · wildriftfire.com/guide/senna (7.3a) · wildriftcore.com/en/champions/senna (11/10). Documento no oficial; Wild Rift es marca de Riot Games.
