---
tags: [wrlab, ficha, chogath, tank, ap-tank, top, jungla, escalado-infinito, feast, tamanio, parche-7.3a]
version: 1.0
Status: Borrador (entregado 12/10/2026 — pendiente de verificación en juego del autor)
champion: Cho'Gath
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — CHO'GATH (Wild Rift 7.3 + hotfix 7.3a)

**Fecha:** 12/10/2026 · **Fuentes:** WR-LAB v1.15 (primaria: apéndice ESCALADO_DE_TAMAÑO + ficha wr-meta 24/09 + win rates vigía 11/10 + items_7.3.csv + diffs oficiales 7.2c/7.3/7.3a + reportes publicados *titán-de-la-jungla*/*titán-del-barón* v1.2) + **motor NUEVO batch4** `model/chogath_model.py` (resultados en `model/chogath_resultados.txt`)
**Roles:** Top/Barón (S) / Jungla (S) · **Arquetipo lab:** `ap-tank` — tanque de escalado infinito (Feast). Estaba en `SIN_MOTOR` ("el motor de autos no tiene sentido… modelo de rotación pendiente en batch2") → **esta ficha estrena el motor rotación-tanque (batch4)**
**Tesis:** El único campeón del juego donde **el tamaño ES poder mecánico**: cada stack de Feast es un stat compuesto (HP + tamaño + rango + anchura de E + daño de R). Su HP hace *double-dip* (tanqueo + execute verdadero): Cho'Gath no te gana a DPS — te gana a EHP y luego te ejecuta con **1 277 de daño verdadero** cada 33 s.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, 11/10/2026):** SOLO **S** · WR **50.24 %** · pick **11.20 %** · **ban 35.48 %** (Confidence High, tendencia 0) · JUNGLE **S** · WR **50.80 %** · pick 8.57 % · ban 35.48 % (High, ↓ 2). Snapshot 24/09: top 51.20 % (↓1) / jungla 50.78 % (**↑14**) con ban 38 % y señales **⛔ Perma-ban 👥 Popular**. Contexto 7.3a: la meta de tanques sigue viva (el reporte Yunara del lab cita "Cho'Gath 50.9 % WR jungla" como referencia del parche). **Regla de oro v1.6:** esta ficha NO modifica los 2 reportes publicados (engine: none, verificados ✅ ANOTAR en 7.3a); es el insumo de la revisión que el lab ya tenía marcada para Cho'Gath ("smite nerf jungla → revisión en su próxima regeneración", §3b).

---

## 1. QUÉ LE HIZO ESTE PARCHE (por qué lo banea 1 de cada 3 partidas)

### 1.1 El buff real fue 7.2c (13-ago-2026) — la base de todo

| Habilidad | Antes | Ahora (7.2c → 7.3) | Impacto |
|---|---|---|---|
| E base | 15/35/55/75 | **20/45/70/95** | +33 % base rank 4 |
| E % vida máx | 2.15/2.5/2.85/3.2 % | **2.3/2.7/3.1/3.5 %** | Anti-tanque +15 % |
| E por stack Feast | +0.5 %/stack | **+0.6 %/stack** | A 22 stacks: 13.2 % → **16.7 % vida máx por pico** |
| R CD | 80/70/60 s | **70/60/50 s** | Stacks ~14 % más rápido + más executes |
| R ratio de HP bonus | 8 % | **10 %** | **El cambio clave:** cada ítem de vida sube el execute un 25 % más |

### 1.2 Cambios 7.3 (21-sep-2026) — directos: ninguno real; sistémicos: todos a favor

| Cambio | Detalle | Efecto en Cho'Gath |
|---|---|---|
| Daño crítico base | 175 → **200 %** | Irrelevante (stat muerto, Ley 4) |
| Tope de AS | 2.5 → **3.0** | Irrelevante (AS lvl 15 = 0.87) |
| Sistema AS (nuevo) | ratio 0.625 · base 0.625 · BBA 0.28 · growth 0.008 | Formaliza su AS baja por diseño |
| **Jungla rehecha** | Burn de Smite escala con stats: **3 % HP bonus + 20 % armadura bonus + 20 % MR bonus + 12 % AP + 10 % bAD** como daño verdadero; monstruos no-épicos hacen **−50 % de daño** al smiter; Smite sube **600→1 000→1 400** | Su build de tanque AHORA acelera el clear (cita oficial: los tanques "ya no necesitan Sunfire para limpiar"); jungla segura desde lvl 1 |
| **Épicos estandarizados** | Duración estándar + Baron mid-game buffeado → más contestables | **Cada épico = 1 stack de Feast SIN CAP** (regla del apéndice TAMAÑO: prioriza dragón/herald aunque pierdas CS) |
| **Torretas 7 000 HP + Crystalline Overgrowth** | El primer ataque detona **3.3–18.9 % de la vida de la torreta como daño verdadero** (ciclo ~50 s: mínimo 30 s, escala 160 s) | Con Demolish (85 + **28 % HP máx**) + rango 200 = el mejor destructor de torres del juego |
| Placas permanentes | +resistencias al caer placa (decaen desde 5:00) | Tanqueo gratis por siegue |
| Minions | Hacen 60 % de daño a campeones | Lane/splitpush más seguros |

### 1.3 Hotfix 7.3a (29-sep-2026) — sin cambios directos; el toque fue al Smite

| Sistema | 7.3 | 7.3a | Efecto |
|---|---|---|---|
| Smite burn vs monstruos | 30–198/s | **22–162/s** | **Jungla: clear early −15–20 %** (registrado en el triage de ambos reportes) |
| Nexus | 5 500 HP | **4 000 HP** | Partidas terminan antes → el capstone (Twinguard/Gargoyle) llega a tiempo |
| Placas (resist al caer) | +30 arm/MR · 20 s | **+20 arm/MR · 10 s** | Siege más fácil para todos; él siega mejor que nadie |

**Veredicto del lab:** Cho'Gath llega a 7.3a **sin nerfs directos desde 7.2c** (donde fue buffeado) y con la jungla/torretas/épicos rediseñados a su medida. Su ban 35.5–38 % no es histeria: es el paquete completo (escalado infinito + execute verdadero + siegue) en la meta de tanques del parche.

---

## 2. FICHA MATEMÁTICA (spec 7.3a)

| Parámetro | Valor | Fuente |
|---|---|---|
| HP | **690** (+128/niv → **2 482**) | ficha wr-meta 24/09 |
| AD base / growth | **62 / 4.0** (→ 118 lvl 15; solo para last hit) | ficha wr-meta |
| Armadura / RM | **46 (+4.5 → 109) / 40 (+2 → 68)** | ficha wr-meta |
| Maná / regen | 380 (+50 → 1 080) / 13 (+0.79) | ficha wr-meta |
| Regen HP | 8 (+0.86 → 20/5 s) | ficha wr-meta |
| MS | 350 | ficha wr-meta |
| AS (7.3 oficial) | ratio **0.625** · base **0.625** · BBA **0.28** · growth **0.008** → lvl 1 = **0.8** · **lvl 15 = 0.87** (sin ítems) | apéndice oficial 7.3 |
| Rango de ataque | **125 (melee) → +7.7/stack (cap +75) → 200** — sigue siendo melee (Grasp/Demolish al 100 %) | ficha 7.3 |
| Daño crítico | 200 % (7.3) — **stat muerto**, `crit_dmg_mod` 1.0 | notas 7.3 |
| R cast range | base no publicada (⚠️ D7) + 2.5/stack (cap +25) | ficha 7.3 |
| **HP lvl 15 SIN ÍTEMS con 15 stacks + runas** | **~5 540** (2 482 + 2 400 Feast + ~500 runas ×1.03 Overgrowth) | motor batch4 |

**Dato de identidad:** la mitad de su vida "full build" viene gratis de Feast. Con build completa (motor, min 20, S=15): **HP 8 093 · armadura 274 · RM 316 · R 1 277 verdadero**.

---

## 3. PASIVA — CARNIVORE + ECONOMÍA DE FEAST (el campeón entero vive aquí)

### 3.1 Carnivore (sustain infinito)
Matar unidad → recupera **18 HP (16 + 2×nivel) y 4.35 maná (4 + 0.35×nivel)**; **×2 si es campeón, torreta o épico**.
- Lvl 15: **46 HP + 9.25 maná** por minion (92 + 18.5 por campeón/épico).
- **Nunca basees por vida:** 2 olas + un campamento = HP lleno. El maná de Carnivore paga el spam de E (30/cast): poke de lane infinito.

### 3.2 Feast — economía de stacks (la parte que MÁS se juega mal)

| Fuente | Stacks | Nota |
|---|---|---|
| Minion / monstruo NO épico (R mata) | 1 · **cap total 6** | R hace **1 200 + 50 % AP + 10 % HP bonus verdadero** → ejecución garantizada de cannon/campamento grande: no compite con tu maná de trade |
| Campeón enemigo (R mata) | 1 · **SIN cap** | Axiom Arcanist: takedown → **−7 % CD de R** → cadenas de execute en teamfight |
| Monstruo épico (dragón/herald/Baron) | 1 · **SIN cap** | 7.3 los hizo más contestables → **cada objetivo = stack gratis**; R solo ya ejecuta el épico (1 937 verdadero a min 20) |

> [!TIP]
> **Regla de oro:** R a minions/campamentos SOLO hasta el cap 6 (después es CD desperdiciado — guárdalo para campeón/épico). Y como en el épico **R + Smite = 3 337 verdadero instantáneo** (motor, min 20), nadie te roba Baron/dragón por debajo de ese umbral: es el execute de objetivos más alto del juego.

### 3.3 El stat compuesto — qué compra CADA stack (con R rank 3)

| Stacks | HP bonus | Tamaño (Feast) | Rango | E (% vida máx/pico) | R execute — build óptima completa (min 20) | R execute — en ruta real |
|---|---|---|---|---|---|---|
| 6 (cap minions) | +960 | +36 % | +46 | 7.1 % | **1 114** | ~972 (min 14, 2 ítems) |
| **10** | +1 600 | +60 % | **+75 (CAP: 200)** · cast R **+25 (CAP)** | 9.5 % | **1 187** | ~1 101 (min 20, 4 ítems) |
| 15 | +2 400 | +90 % | +75 | 12.5 % | **1 277** | 1 230 (min 22, full) |
| 22–23 | +3 520 | **+132–135 % (CAP tamaño)** | +75 | 16.7 % | **1 404** | — |

Cada stack son **5 stats a la vez**: HP (tanqueo + daño de R al 10 %), tamaño (anchura del cono de E), rango de ataque (125→200), cast range de R y execute de R. *Ningún otro campeón convierte una kill en stats permanentes.* (La columna "en ruta real" usa los ítems completados a ese minuto — tabla §3.4.)

### 3.4 Curva de stacks por minuto + execute resultante (protocolo §1b.6.3, motor batch4)

| Min | Ítems de la ruta | Nvl | S (top/jungla) | R (nvl) | HP | R vs campeón | R vs monstruo | Smite+R |
|---|---|---|---|---|---|---|---|---|
| 6 | Plated T2 | 6 | 0/0 | R1 | 1 636 | 364 | 1 354 | 1 954 |
| 10 | **Heartsteel** | 9 | 2/4 | R2 | 3 051 | 642 | 1 467 | 2 467 |
| 12 | ⬆️ botas T3 | 10 | 4/6 | R2 | 3 585 | 687 | 1 512 | 2 512 |
| 14 | **Unending Despair** | 12 | 6/8 | R3 | 4 931 | **972** | 1 632 | 3 032 |
| 17 | **Twinguard** | 13 | 7/10 | R3 | 5 706 | 1 043 | 1 703 | 3 103 |
| 20 | **Gargoyle** | 14 | 8/12 | R3 | 6 364 | 1 101 | 1 761 | 3 161 |
| 22 | 6.º (FoN default) | 15 | 10/14 | R3 | 7 661 | **1 230** | 1 890 | **3 290** |

(Supuestos A5/A13/A14 del motor: runas acumuladas por minuto, growth de Heartsteel desde min 9.5, Smite 600/1 000/1 400 por minuto. Jungla llega ~2 stacks antes por campamentos+épicos.)

---

## 4. HABILIDADES (valores 7.3) Y MECÁNICAS EXPLOTABLES

### P — Carnivore · ver §3.1
### Q — Rupture · CD 6 s · 60 maná
**80/135/190/245 + 100 % AP** mágico en área · **knock-up 1 s** · slow 60 % (1.5 s). Con AH 50: CD 4 s.
- **Q→R = ejecución garantizada:** en el aire no hay Flash ni dashes → R (200+25 de rango) conecta siempre. Flash+Q+R es el engage-execute sin contrajuego.
### W — Feral Scream · CD 12/11/10/9 s · 70/80/90/100 maná
Cono: **silencio 1.4/1.6/1.8/2 s** + **80/130/180/230 + 70 % AP**.
- El silencio bloquea dashes y Flash → **anti-dive duro** (Katarina/Yasuo/Fizz-like): W sobre tu carry cuando entra el diver.
### E — Vorpal Spikes · CD 7/6/5/4 s · 30 maná
Próximos **3 autos** lanzan conos: **20/45/70/95 + 30 % AP + (2.3/2.7/3.1/3.5 % + 0.6 %×stacks Feast) de la vida MÁX del objetivo** mágico · slow 30/35/40/45 % (decae 1.5 s) · **la anchura escala con su tamaño** · base vs minions/monstruos capada a 100 (⚠️ D1).
- **E es un auto EMPOWERED: un solo cono dispara TODO** — Grasp (3.3 % HP máx + cura + 10 HP permanente), el golpe cargado de Heartsteel, Torment de Liandry's, spellblade de Iceborn. Tira E ANTES del trade, no durante.
- A 15 stacks cada pico = **95 + 12.5 % de la vida máx** → vs tanque 4 500 HP: **657 mágico por pico** (8.7 picos/10 s).
### R — Feast · CD 70/60/50 s · 100 maná · VER §3.2–3.4
**300/450/600 + 50 % AP + 10 % de tu HP BONUS como daño VERDADERO** (campeones) · **1 200 +** lo mismo (minions/monstruos) · kill = +1 stack. Ignora RM: en la meta de stacking MR (FoN/Kaic), **R no se mitiga nunca**.

---

## 5. ¿CON QUÉ ESCALA CHO'GATH? (respuesta por stat)

| Stat | ¿Escala? | Números |
|---|---|---|
| **HP (máx/bonus)** | ✅ **PRIMARIO, INFINITO Y COMPUESTO** | Feast +160/stack · **R +10 % HP bonus verdadero** · Heartsteel (proc 3.5 % máx + 15 % → HP permanente: **+425 a min 20**) · Grasp 3.3 % máx · Demolish 28 % máx · **Smite +3 % HP bonus verdadero** · Gargoyle (escudo = 90 % bonus) · Immolate (1–1.5 % bonus/s) · Anguish (3 % máx + cura 250 %) · Overgrowth +3 % · Thorns +1 % bonus. **Cada punto de HP compra EHP Y daño a la vez — único en el juego.** |
| **Stacks de Feast** | ✅ **SU VERDADERO "AP"** | E rank 4 = 95 + 30 % AP **+ (3.5 % + 0.6 %×S) vida máx**. A S=15 el término %-vida (12.5 %) duplica al término AP → por eso la óptima del motor lleva **AP 0** y aun así hace 444 DPS vs fighter. |
| **AP** | ⚠️ **SECUNDARIO** | Q 100 % · W 70 % · E 30 % · R 50 %. Vale en Q/W/R, pero por oro rinde menos EHP que un slot defensivo (motor: óptima AP-0 gana +18.9 % a la publicada con AP 160). **Riftmaker hace double-dip** (2 % HP bonus → AP) en la variante carry-top. |
| **Armadura / RM** | ✅ **DEFENSA + SMITE** | Twinguard ×1.3 en ventana · Smite +20 %+20 % de resistencias bonus como verdadero · Mantle Lifeline cura 120 % armadura + 120 % RM bonus · FoN Absorb +70 RM. |
| **AH** | ⚠️ **MENOR** | 50 AH (build óptima) → Q 4 s / E 2.67 s / R 33 s: más Torment, más CC, más executes por pelea. |
| **AS** | ❌ **MUERTA (Ley 2)** | 0.87 a lvl 15; E solo pide 3 autos por cast; el tope 3.0 es inalcanzable e inútil. |
| **AD / Crítico** | ❌ **MUERTOS (Ley 4)** | El crit 200 % de 7.3 no le toca; AD 118 solo lasthitea. Controles del motor: Sterak's −7.0 %, Overlord's −9.7 %, Cleaver −9.8 % vs óptima. |
| **Maná** | ⚠️ **RESTRICCIÓN EARLY** | 380 base; E×3 + Q + W ≈ 180 → 2 rotaciones. Carnivore lo repone; RoA/Fimbulwinter/Iceborn lo cubren si hace falta. |
| **MS** | ⚠️ **UTILIDAD (sin dashes)** | 350 base; FoN +11 % (5+6 Absorb). Su posicionamiento ES su movilidad: Q-slow 60 % y W abren el camino. |

---

## 6. CURVA DE PODER Y LECTURA DE ROLES

- **Early (0–9 min):** sustain imbatible (Carnivore), all-in débil. Top: trades E+Q, placas con Demolish desde min 1 (85 + 28 % HP al 3.er golpe), R a minions hasta el cap 6. Jungla: clear SEGURO (−50 % de daño de monstruos) pero LENTO post-7.3a (burn −18 %); smite-kill de campamentos con R (1 200+ verdadero).
- **Mid (9–15 min) — pico 1:** Heartsteel + botas T3 (~min 10): R2 ejecuta ~640–690; ventana de Gargoyle aún no existe → juega por objetivos, no por all-ins. Nvl 9–13 es el salto (Q4/E4 + R2→R3: execute ~972).
- **Late (15–20 min) — pico 2:** Unending Despair + Twinguard + Gargoyle: **VENT 43–56 k**, R3 ~1 000–1 100, hps en pelea ~150–200. Teamfight: Q (knock-up) → W (silencio) → Gargoyle al entrar → E en cono gigante → R al que baje de 1 100.
- **Ultra-late (22+):** S=22 → HP 9 497 · R 1 432 · E 16.7 % vida máx/pico · tamaño +132 % · VENT 65 915. Escalado infinito real (campeones y épicos no tienen cap).
- **TOP vs JUNGLA (ambos S, ban 35.48 %):** **Top** = presencia (pick 11.2 %), stacks predecibles (minions cap 6 + herald/dragón), splitpush con Demolish+cristales+200 de rango. **Jungla** = WR marginalmente mayor (50.80), motor de épicos (stacks sin cap), umbral Smite+R 3 337, pero el nerf 7.3a le pega al early (−15–20 %). Veredicto: **top por consistencia, jungla por techo de objetivos**. Variante mid (existe en `ROLE_VARIANTS` del lab: Flash+Ignite/TP, E-push, R execute): niche, sin datos del vigía.
- **Matchups (reporte publicado titán-del-barón, estimaciones del autor):** vs **Dr. Mundo** ✅ ~60 % (R lo ejecuta antes que su R cure; Ignite/Morello/Thornmail para GW) · vs **Volibear** ✅ ~55 % (sustain + execute > su burst) · vs **Camille** ⚠️ (Q2 verdadero ignora tu armadura — Armored Advance temprano) · vs **Darius** ⚠️ (su R ejecuta a umbrales altos — juega seguro hasta Heartsteel).
- **Counters reales (mecánicos, no de WR):** % vida máxima/daño verdadero (Vayne, Fiora, Kog'Maw, Camille) · ejecutores (Darius) · **kiting** (no tiene dash: Ashe/Senna/Xayah lo mantienen fuera de rango de E) · burst AP antes de que cierre ventanas (→ Mantle/Kaic temprano).
- **Sinergias:** su cadena de CC (Q 1 s + W 2 s + E slow 45 % + Iceborn/Rylai's) = 3+ s de lock para un backline (Jinx/Yunara/Senna) · enchanters que cubren su MS/engage (Yuumi attach, Karma E-Mantra, Seraphine) · Zeke's Convergence (2 400 g) si el equipo quiere seguir su R.

---

## 7. SOBREEXPLOTACIÓN — LAS 10 PALANCAS (resumen ejecutivo)

1. **R a minions/campamentos SOLO hasta el cap 6** (1 200+ verdadero = ejecución garantizada); después, solo campeones/épicos.
2. **Cada épico > una ola:** stack sin cap + 7.3 los hizo contestables → pelea TODO dragón/herald; R solo ejecuta el épico (1 937 a min 20) incluso sin Smite.
3. **Q (knock-up 1 s) → R:** en el aire no existe Flash → ejecución garantizada desde 200+25 de rango; Flash+Q+R sin contrajuego.
4. **Axiom Arcanist = multi-R:** +10 % daño de R y −7 % CD por takedown → cada kill en teamfight acerca el siguiente execute (y el siguiente stack).
5. **E detona todo a la vez:** Grasp + Heartsteel + Torment + spellblade en un cono — el trade perfecto es E→auto→auto→auto con todo proceando.
6. **10 stacks = 200 de rango:** detona cristales de torreta (3.3–18.9 % verdadero, ~770 medio) y lasthitea fuera del alcance melee; 23 stacks = cono de teamfight completa (~2.6–3 objetivos).
7. **Demolish + cristales:** 3.er golpe a torreta = 85 + 28 % HP máx (**2 351** con 8 093 HP) + cristal verdadero → el mejor destructor del juego; placas dan +20 arm/MR (10 s).
8. **Apila ventanas, no stats:** Gargoyle (5 150 activo, CD 60) → rampa Twinguard (5 s → resistencias ×1.3 + 20 % tenacidad) → escudo Noxian de botas (12 s) → Mantle reactivo (70 s). Ventana efectiva: **55 591 EHP en 5 s** ≈ 3 rotaciones de burst enemigas (claim publicado, verificado por el motor).
9. **Economía Carnivore:** nunca baseas por vida (46 HP/minion, 92/campeón); el maná de E se paga solo.
10. **El daño verdadero no negocia:** contra stacking de RM (FoN/Kaic enemigas), R + Smite siguen al 100 % — él es el check de la meta de tanques que él mismo habilita.

---

## 8. BUILDS DERIVADAS POR EL MOTOR (batch4 — resumen; detalle en `model/chogath_resultados.txt`)

> **Motor nuevo `model/chogath_model.py` (rotación-tanque):** búsqueda exhaustiva de 122 632 builds (Ley 0: 1 botas + 5 ítems; presupuesto 17 250 g; exclusividad Immolate Sunfire/Hollow A10). Score ponderado del arquetipo Tanque (§A.5): **EHP físico .15 + EHP mágico .15 + EHP EN VENTANA .20 + execute R .15 + DPS fighter .10 + DPS tanque .10 + DPS AoE .05 + sustain .05 + utilidad .05**, normalizado por escenario. Nivel 15, Feast 15 stacks, min 20, runas Grasp/Demolish/Second Wind/Overgrowth + Transcendence/Axiom. Supuestos A1–A14 declarados en el docstring (retroactividad de Feast, Twinguard ×1.3 total, Axiom sobre verdadero, growth de Heartsteel +425 HP a min 20, condicionalidad al 50 %, etc.).

### 8.1 La óptima del motor (default top/jungla)

**Tabla A — Build final (6 slots, `validate_slots()` PASS manual)**

| Slot | Ítem | Oro | Rol en la build |
|---|---|---|---|
| 1 (botas) | **Plated Steelcaps → ⬆️ Armored Advance** (min 10:00, MISMO slot) | 2 200 | 30 arm + 150 HP + Block 10 % + escudo físico (75 + 8 % HP máx, CD 12 s ≈ 722) |
| 2 | **Heartsteel** | 3 000 | 700 HP + proc 423 físico/20 s + **15 % → HP permanente (+425 a min 20)**: alimenta R, Gargoyle y E |
| 3 | **Unending Despair** | 3 000 | 40/40 resist + **Anguish: 243 mágico AoE/4 s + cura 607 (250 %)** — el motor de pelea del motor |
| 4 | **Amaranth's Twinguard** | 3 200 | 300 HP + 50/50 + **Endurance (5 s): resistencias ×1.3 + 20 % tenacidad + 20 % tamaño** (capstone oficial 7.3) |
| 5 | **Gargoyle Stoneplate** | 2 900 | 45/45 + **activo: escudo 100 + 90 % HP bonus = 5 150** (2.5 s, CD 60) + tamaño |
| 6 | **Force of Nature** (default mixto) | 2 800 | 400 HP + 60 MR (+70 Absorb) + **11 % MS** — el mejor paquete MR post-nerf 7.3 |

> **Total: 17 100 g** · HP **8 093** · arm **274** · MR **316** · AH 50 · AP 0 · tamaño +110 % · rango 200 · **R 1 277 verdadero** · **VENT 55 591** · EHPp/EHPm 32 546/33 626 · DPSf 444 · AoE 957 · **hps 197** · Smite+R vs épico **3 337** · Demolish 2 351.

**Tabla B — Ruta de compra cronológica**

| # | Compra | Oro acum. | Minuto típico |
|---|---|---|---|
| 1 | Ruby Crystal (start) | 500 | 0:00 |
| 2 | **Plated Steelcaps** (T2; Mercury's vs AP) | 1 700 | ~5:00 |
| 3 | Giant's Belt + Kindlegem → **Heartsteel** | 4 700 | ~8:30 |
| 4 | ⬆️ **Armored Advance** (mismo slot, +1 000 g) | 5 700 | ~10:00 |
| 5 | componentes → **Unending Despair** | 8 700 | ~13:00 |
| 6 | Giant's Belt + Chain Vest + Negatron → **Amaranth's Twinguard** | 11 900 | ~15:30 |
| 7 | Kindlegem + Chain Vest + Negatron → **Gargoyle Stoneplate** | 14 800 | ~18:00 |
| 8 | Winged Moonplate + Negatron + Ruby → **Force of Nature** (o 6.º situacional §8.4) | 17 600 | ~20:30 |

**Runas · Hechizos · Habilidades** (baseline publicado, el motor no re-puntúa runas): **Grasp of Undying** (3.3 % HP máx + cura 1.3 % + 10 HP permanente/3 s — con E empower proca solo) · **Demolish** (85 + 28 % HP) · **Second Wind** · **Overgrowth** (+3 % HP máx) | **Transcendence** (+10 AH) · **Axiom Arcanist** (+10 % R, −7 % CD por takedown; alternativa: Revitalize +5–15 % curas/escudos vs poke) · Hechizos: **Top Flash+Ignite/TP · Jungla Smite+Flash** · Skills **E→Q→W** (R 5/9/13).

### 8.2 Comparación con las builds publicadas y la comunidad (mismas métricas, min 20, S=15)

| Build | Fuente | Score (rel. óptima) | Evidencia del motor |
|---|---|---|---|
| **ÓPTIMA batch4** (§8.1) | 🔬 LAB (motor nuevo) | **0.816 (ref.)** | VENT 55 591 · R 1 277 · hps 197 · DPSf 444 |
| Tanque puro (HS+TW+Garg+Warmog+Randuin) | 🌐 variante | 0.726 (−11.1 %) | VENT 49 556 pero DPSf 417 y RM 163 |
| Titánica híbrida (HS+Titanic+TW+Garg+Liandry) | 🔬 control | 0.687 (−15.8 %) | AoE 1 390 (+45 %) — nicho divertido, no óptimo |
| **titán-del-barón publicada** (HS+RoA+TW+Garg+Liandry) | 📌 publicada | 0.680 (**−16.7 %**) | R 1 377 (+7.8 %) y DPSf 518 (+17 %) pero VENT 39 274 (−29 %) y **hps 46** |
| Comunidad wr-meta (Chainlaced+HS+Hollow+Liandry+FoN+Warmog) | 🌐 comunidad | 0.679 (−16.8 %) | DPSf 554 (+25 %) pero **EHPp 18 206** (armadura 109) y VENT 25 437 |
| **titán-de-la-jungla publicada** (HS+Hollow+Liandry+FoN+Warmog) | 📌 publicada | 0.662 (**−18.9 %**) | DPSf 554 (+25 %) pero **VENT 26 292 (−53 %)**: sin Twinguard/Gargoyle no hay ventana |
| AP puro (Liandry+Rift+Crypt+Rabadon+Rylai) | 🔬 control | 0.633 (−22.5 %) | DPSf 733 (+65 %) · AoE 1 603 (+67 %) · **VENT 14 534 (−74 %)** |

### 8.3 Hallazgos del motor (lo que ninguna build publicada tenía)

1. **El cuarteto robusto: Unending Despair + Gargoyle + Twinguard + Force of Nature** aparece en las 10 mejores builds y sobrevive a todas las sensibilidades (S=6/15/22, pesos AD/AP/tanque, Axiom off); solo Twinguard cae en el peor caso de D2b (Endurance sin multiplicador — ver §9 D2). **Unending Despair no está en NINGUNA build publicada ni comunitaria**: Anguish (3 % HP máx AoE/4 s + cura 250 %) le da el mejor sustain en pelea del roster (197 hps vs 46–67 de las publicadas) con 40/40 de resistencias.
2. **Force of Nature rehabilitada:** los reportes Ornn/barón la marcan ❌ ("sin % damage reduction en 7.3") — el motor la pone en TODAS las óptimas: 400 HP + 60 MR + Absorb (+70 MR en pelea) + 11 % MS es el mejor paquete MR del parche aunque haya perdido la reducción %. (El veredicto ❌ publicado vale para Ornn, que no double-dipea HP como Cho'Gath.)
3. **Warmog's rehabilitada (parcial):** el ❌ publicado ("regen fuera de combate inútil en fights") ignora **Blessed: +30 % a curas Y ESCUDOS recibidos — dentro de la pelea**. Con Warmog's, la ventana sube a **56 377 (la más alta de toda la búsqueda**: escudo de Gargoyle 5 150→6 695). Pierde el slot default contra Heartsteel por R/DPS/growth (−1.7 % score), pero es el 6.º legítimo de presión de mapa.
4. **Heartsteel: inversión con fecha.** En el checkpoint min 9:30 el snapshot estático lo pone #30 (−8.9 % vs Unending inmediato) porque el growth (+15 % por proc) aún no existe; comprado a min 10, la trayectoria lo devuelve: empate a min 14, +2.2 % a min 20, **+3.7 % a min 24**. Regla: **Heartsteel 1.º SI y solo si se completa ≤ min 10–11**; si la partida se retrasa (o vas atrás), Unending Despair 1.º es la línea correcta.
5. **AP 0 en la óptima — los stacks son su AP:** a S=15, E pega 12.5 % de la vida máx por pico (el término AP solo añade 30 % ratio + 95 base). Con sesgo de daño (variante carry-top §8.5) el AP vuelve y gana: Liandry's+Riftmaker (2 % HP→AP, double-dip)+Cryptbloom+Abyssal+Iceborn → DPSf 810 (+82 %).
6. **Controles Ley 4 confirmados:** Sterak's (−7.0 %), Overlord's Bloodmail (−9.7 %), Black Cleaver (−9.8 %), cualquier crítico/AS (rechazo estructural). Immortal Treads nunca entró al top-10 (0 resistencias).

### 8.4 Matriz del último slot (situacional, con números del motor)

| Situación | Slot 6 | Impacto medido |
|---|---|---|
| **Default mixto** | **Force of Nature** (2 800) | MR 316 · EHPm 33 626 · 11 % MS ✅ |
| Presión de mapa / sustain | **Warmog's Armor** (2 850) | **VENT 56 377 (máx)** · hps 240 · OOC 3.5 %/s ✅ |
| Vs AD/críticos | **Randuin's Omen** (2 800) | EHPp 38 587 (+18.6 %) ✅ (variante AD completa: −FoN, botas Armored) |
| Vs AD autos + lifesteal (7.3) | **Thornmail** (2 700) | EHPp 34 471 + thorns + GW 50 % ⚠️ |
| Vs AS pesada (Jinx/Yunara) | **Frozen Heart** (2 550) | −25 % AS enemiga en 650 u ≈ +10.6 % EHPp efectivo (50 % uptime) ⚠️ |
| Vs AP burst | **Kaic Rookern** (2 800) | EHPm 38 697–40 041 + escudo mágico 1 243 pre-fight ✅ (botas Chainlaced) |
| Vs execute/burst que te baja de 30 % | **Mantle of the Twelfth Hour** (2 550) | Lifeline: +250 HP + cura 1 638 + 10 % tamaño/tenacidad/MS (CD 70) ⚠️ |
| Vs 2+ tanques MR-stacking | **Cryptbloom** (3 000) o **Liandry's** (3 000) | Crypt: +30 % pen (+36.5 % daño vs 200 MR) · Liandry: Torment 2 % máx/s ⚠️ |
| Vs curación (Mundo/Soraka/Yuumi) | **Morellonomicon** (2 650) | GW 50 % (pierdes ~10 % de daño sostenido — cita publicada) ⚠️ |
| Splitpush/siege | **Iceborn Gauntlet** (3 000) | Spellblade AoE (118 + 25 % armadura bonus) + campo de slow + 30 AH ⚠️ |

### 8.5 Variantes de escenario (búsquedas completas con pesos movidos)

> [!DANGER]
> **CARRY-TOP (sesgo daño, DPS 50 % del score):** Chainlaced + **Liandry's + Riftmaker + Cryptbloom + Abyssal Mask + Iceborn** (16 700 g) → AP 302 · **DPSf 810 (+82 %)** · AoE 1 772 (+85 %) · R 1 327 — **a cambio de VENT 18 774 (−66 %) y EHPp 18 226 (−44 %)**. Es la build "AP puro" corregida: Abyssal (+12 % mágico propio y de equipo) e Iceborn (slow+spellblade) sustituyen al glass-cannon inútil (Rabadon/Rylai). Solo con equipo que proteja (Yuumi/Karma) o vs comps sin % vida.

| Variante | Build óptima (motor) | Score | Evidencia |
|---|---|---|---|
| **vs COMP AD** (75 % físico) | Armored + **Heartsteel + Randuin's** + Gargoyle + Unending + Twinguard | 0.707 | EHPp **42 511** (+30.6 %) · armadura 349 |
| **vs COMP AP** (75 % mágico) | **Chainlaced** + Heartsteel + FoN + Gargoyle + Unending + Twinguard (o Kaenic por Heartsteel vs burst) | 0.738 | EHPm **36 054–40 041** · RM 346–430 |
| **vs DOBLE TANQUE** | = default (el %-vida de E + Anguish + R verdadero YA son anti-tanque) | 0.679 | DPSt 374 · Iceborn entra al top-3 (AoE 1 103) |

### 8.6 Ventanas de supervivencia de la óptima (protocolo §1b.6.1 — la métrica real detrás del "tamaño")

| Ventana | Fuente | Valor (min 20, HP 8 093) | CD |
|---|---|---|---|
| Activa (2.5 s) | Gargoyle Stoneplate | **5 150 de escudo** (6 695 con Warmog's Blessed) + tamaño | 60 s |
| Rampa (5 s) | Twinguard Endurance | arm 274→**356** · MR 316→**410** · +20 % tenacidad · +20 % tamaño (total a S=15: +110 %; el cap de Feast +135 % llega a 23 stacks) | en pelea |
| Reactiva (12 s) | Armored Advance Noxian | **722 físico** (Block 10 % permanente adicional) | 12 s |
| Sostenida | Anguish + Grasp | **607 cura/4 s + 105 cura/3 s** (+ 267 + 243 mágico de daño) | 4 s / 3 s |
| Situacional | Mantle Lifeline / Kaenic Magebane | +250 HP + 1 638 cura (<30 %) / 1 243 escudo mágico pre-fight | 70 s / 12 s |

**EHP efectivo en ventana (5 s, mezcla 50/50):** **55 591** — ~6.9× su HP real. El claim publicado ("el enemigo necesita 3 rotaciones completas de burst") queda verificado con fórmula completa (§1b.6.2: vida + escudos ponderados + curas × mitigación con Twinguard al máximo).

### 8.7 Checkpoints de ruta (niveles/oros reales — no nivel 15 plano)

| CP | Motor #1 (score) | Heartsteel en ese CP | Lectura |
|---|---|---|---|
| 9:30 · lvl 9 · ≤5 300 g | Mercury's + **Unending Despair** (0.785) | #30 (0.716, −8.9 %) | Unending = poder inmediato; Heartsteel = inversión (regla §8.3.4) |
| 12:00 · lvl 12 · ≤8 000 g | Mercury's + Unending + **Twinguard** (0.719) | HS+UD: VENT 11 653 · R 746 | La ventana empieza a existir (Gargoyle aún no) |
| 15:00 · lvl 14 · ≤12 200 g | T3 + FoN + Unending + Twinguard (0.703) | HS+FoN+UD: R 1 186 (CP4) | R3 online: execute ~1 000 |
| 18:00 · lvl 15 · ≤15 100 g | Armored + FoN + **Gargoyle** + Unending + Twinguard (0.692, VENT 43 128) | variante HS #3 (0.687) | Ventana completa; a min 20 la línea HS gana |

---

## 9. DISCREPANCIAS REGISTRADAS (protocolo lab §D)

| # | Tema | Resolución |
|---|---|---|
| D1 | E vs minions/monstruos: "Base damage capped at 100 (30 %)" — ¿el %-vida también se capa? | Ambiguo en la ficha wr-meta. Modelado: solo la base se capa (el %-vida aplica). Afecta velocidad de clear, NO rankings. **Verificar en juego** |
| D2 | **Twinguard Endurance: ¿×1.3 a resistencias TOTALES o solo BONUS?** El código del apéndice TAMAÑO usa total×1.3; el texto de intención 7.3 dice "bonus resistances" | Convención lab: total×1.3. Sensibilidad corrida: **bonus-only → la óptima NO cambia** (Twinguard aguanta); **sin multiplicador (peor caso) → Twinguard sale y entra Kaenic Rookern**. Prioridad ALTA de verificación en juego: decide el slot 4 |
| D3 | Feast retroactivo al subir R (80→120→160/stack) | Modelado retroactivo (comportamiento PC). Si no: −480 HP a S=22; rankings sin cambio. **Verificar en juego** |
| D4 | Axiom Arcanist +10 %: ¿amplifica daño VERDADERO de R? | Modelado que sí. Sensibilidad: R 1 277→1 161 (−9 %), óptima idéntica. **Verificar en juego** |
| D5 | **El reporte publicado titán-de-la-jungla recomienda Spirit Visage** (matriz situacional y rutas anti-AP) | **Spirit Visage NO existe en la BD de 186 ítems de 7.3** (verificado en los reportes barón/Rammus del propio lab). Ítem alucinado/stale → errata del reporte publicado; ya estaba marcado "para revisión en su próxima regeneración" (§3b). Sustituto correcto: **Kaic Rookern / Warmog's (Blessed)** |
| D6 | El reporte jungla publicado lleva FoN+Warmog's que sus propios reportes hermanos (barón/Ornn/Rammus) marcan ❌ | Contradicción interna del lab. El motor resuelve con números: FoN = mejor paquete MR (§8.3.2) y Warmog's = ventana más alta vía Blessed (§8.3.3). Los ❌ publicados valían para Ornn/Rammus (no double-dipean HP) |
| D7 | Rango base de casteo de R no publicado (PC = 175) | Modelado ≈ melee + stacks (+25 cap). No afecta rankings. **Verificar en juego** |
| D8 | wr-meta muestra AS growth "0.005" vs apéndice oficial 0.008 | Convención de display: 0.625 × 0.008 = 0.005 mostrado. NO es discrepancia (mismo caso que Senna D4) |
| D9 | Cifras absolutas de los reportes publicados (HP ~6 500, VENT ~18 000 en barón) | Aproximaciones manuales (engine: none) sin base lvl 15 completa ni runas; el motor con fórmula §1b.6.2 da HP 8 196 / VENT 39 274 para la MISMA build. Las conclusiones RELATIVAS publicadas (titánica > comunidad > AP puro en EHP) se mantienen; las absolutas se reemplazan por las del motor |

---

## Pie de página
Fuentes: WR-LAB completo v1.15 (metodología FRAMEWORK + Leyes 0–7 + apéndice ESCALADO_DE_TAMAÑO §1b + ficha wr-meta Cho'Gath 24/09 + win rates vigía 11/10 + items_7.3.csv 186 ítems + diffs oficiales 7.2c/7.3/7.3a + reportes publicados *chogath-titan-de-la-jungla* y *chogath-titan-del-baron* v1.2 con sus bloques WRLAB-VERIF) · motor nuevo `model/chogath_model.py` (batch4, rotación-tanque) con resultados completos en `model/chogath_resultados.txt` (122 632 builds evaluadas + 4 sensibilidades + 4 checkpoints + curva de stacks). Esta ficha es documento de análisis: NO regenera los reportes publicados (regla de oro v1.6) y sirve de insumo a su próxima revisión. Documento no oficial; Wild Rift es marca de Riot Games.
