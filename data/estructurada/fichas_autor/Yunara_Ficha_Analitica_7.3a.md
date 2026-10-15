---
tags: [wrlab, ficha, yunara, adc, dragon-lane, critico-aoe, hibrido, re-verificacion, riesgo-ajustado, parche-7.3a]
version: 1.0
Status: Borrador (entregado 13/10/2026 — re-verificación con derivación nueva; insumo de REGENERACIÓN del reporte publicado)
champion: Yunara
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — YUNARA · DRAGON LANE (Wild Rift 7.3 + hotfix 7.3a)

**Fecha:** 13/10/2026 · **Fuentes:** WR-LAB v1.15 (reporte publicado `yunara` v1.2 08/10 + ficha wr-meta 24/09 + notas oficiales 7.3/7.3a + apéndice AS + items_7.3.csv + win rates vigía 11/10) + **motor de re-verificación batch4** `model/yunara_model.py` (resultados en `model/yunara_resultados.txt`)
**Rol:** ADC — Dragon Lane (DUO, **S+**) · **Arquetipo lab:** `crit-aoe-hibrido` (críticos → daño mágico extra; spread de Q que critica durante R) · **engine:** autos + **términos propios integrados** (spread/pasiva/Q on-hit/W — el lab los tenía en `model_terms_pending`)
**Tesis:** La ADC que define el parche estaba publicada con **cifras irreproducibles** (3v3 inflado −42 %) y un 6.º slot default (Kraken) que no daña ni defiende. La derivación corregida responde a la duda del autor — *daño vs riesgo era una falsa dicotomía*: **Yun Tal + BotRK gana +10.3 % 1v1, +25.5 % vs tanques y ×3.2 de sustain por solo +400 g (17 750 vs 17 350)**, con la misma EHP. El riesgo real de Yunara no se resuelve con armadura (su EHP es idéntica en toda build glass): se resuelve con **sustain, R guardada y la matriz de dive**.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, 11/10/2026):** DUO **S+** · WR **51.44 %** · pick **15.83 %** · **ban 22.94 %** (Confidence High, tendencia 0). Evolución: 24/09 50.85/13.08/**13.02** (↓3, señal "🧊 Falling") → 05/10 51.64/16.83/23.80 → 11/10 51.44/15.83/22.94: **el ban se disparó 13→23 % en dos semanas post-buff**. Cross-checks del reporte: wildriftcore 50.9 % (30 d, Tier S) · riftpatchnotes 53.02 %. Cuando no está baneada es el blind-pick de bot del parche.
> **Veredicto de la re-verificación:** ⚠️→❌ **Los titulares publicados NO se reproducen** (1v1 −14 %, 3v3 −42 %, vs120 −30 %, vsT −19 % contra sus propios supuestos) por errores de inputs (AD sin growth, AS "2.83 con Pow-Pow x3" irrazastreable, spread crítico permanente, mágicos sin mitigar). Δ ≥ 5 % en métricas de resultado + inputs del spec mal → **triage ❌ REGENERAR** según umbrales del lab (§E). Esta ficha es el insumo; el reporte publicado no se edita en silencio (convención v1.15).

---

## 1. QUÉ LE HIZO ESTE PARCHE (por qué el ban pasó de 13 % a 23 %)

### 1.1 Cambios 7.3 (21-sep-2026, notas oficiales — sección YUNARA)

| Stat / Habilidad | Antes (7.2) | Ahora (7.3) | Impacto |
|---|---|---|---|
| **Pasiva Vow of the First Lands** | críticos +**10 %** mágico (+10 %/100 AP) | **+8 %** (+8 %/100 AP) | ⚠️ nerf leve (~−20 % del término mágico); con AD 300 ≈ 24 mágico/crítico (interpretación D9) |
| **Q AS bonus** | 22.5/35/47.5/60 % | **25/35/45/55 %** | ✅ +2.5 % rank 1 (lane), −5 % rank 4 |
| Daño crítico base / AS cap | 175 % / 2.5 | **200 % / 3.0** | ✅ ×2.30 con IE; su AS alta ya no se desperdicia |
| **Kraken Slayer (ítem)** | — | *"Optimized its interaction with Yunara's 1st ability; **spread can now trigger Bring It Down**"* | Interacción oficial (modelada +50 % procs AoE; ni así gana al BotRK — §8.4) |
| **Fiendhunter Bolts (ítem nuevo)** | — | Notas oficiales la nombran usuaria objetivo (*"Twitch, Zeri, and Yunara"*) | Evaluada por primera vez: ❌ para DPS máx (−11 % 1v1 vs C44) pero +ult haste → nicho R-spam ⚠️ |
| AS (apéndice oficial) | — | **0.65 / 0.65 / 0.23 / 0.032** | Fuente primaria del motor |

### 1.2 Hotfix 7.3a (29-sep-2026) — sin cambios directos; su ítem puente sí

| Cambio | Detalle | Efecto |
|---|---|---|
| **Yun Tal Wildarrows** | AS 25→**35 %** · Flurry +25→**+35 % AS** (CD 20→25 s) | **El motivo de esta revisión** (flag §3b del lab): con valores 7.3a, Yun Tal **invierte el veredicto de 1.er ítem** (§8.5) y entra a la óptima de 6 slots |
| Nexus 4 000 · placas +20/10 s | 7.3a | Cierre más rápido (el pico 6 slots ~20:15 importa) + siege con Q a rango (D11) |

---

## 2. FICHA MATEMÁTICA (spec 7.3a — auditada)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base / growth | **58 / 3.0** → **100** @15 | wr-meta + ficha; ⚠️ el reporte publicado usó 268 de AD total = **omitió el growth** (correcto: 100 + ítems) |
| HP | 600 (+128 → **2 392**) | ficha wr-meta |
| Armadura / RM | 35 (+4.5 → 98) / 30 (+1.43 → 50) | ficha wr-meta |
| Maná / MS | 345 (+33 → 807) / 335 | ficha wr-meta |
| AS (7.3 oficial) | ratio **0.65** · base **0.65** · BBA **0.23** · growth **0.032** → bonus de niveles **+0.448** @15 | apéndice oficial |
| Rango | **≥550 estimado** (no publicado — D11; necesario para Magnification) | reporte + spec |
| `self_as_buff` | **0.55** (Q rank 4, 5 s; en R es automática → uptime ~100 % en pelea) | ficha |
| Crítico | 200 % / **230 % con IE** · `crit_dmg_mod` 1.0 | notas 7.3 |
| **AS de la óptima corregida** | ítems 155 % → B = 0.23+0.448+1.55+0.384(LT)+0.21(Alac)+0.55(Q) = **3.372** → **AS 2.842** · con Flurry 50 % → **2.956** · Flurry 100 % → raw 3.07 → **cap 3.0** | motor batch4 |

**Los dos AS del reporte publicado están mal:** "2.83 (con Pow-Pow x3)" es irrazastreable (D2) y su §3 usa 2.42 con AS-ítems 0.90 (omite el 35 % de Kraken). El correcto de su Tabla A: **2.647**.

---

## 3. PASIVA + ECONOMÍA DE UNLEASH (su "stack system")

### 3.1 Vow of the First Lands
Cada **crítico** añade daño **mágico** = 8 % (+8 %/100 AP). Con AD 300 y crit 100 %: ~24 mágico/golpe (×AS 2.96 ≈ 71/s) — pequeño pero **no mitigable con armadura** (perfil híbrido: difícil de itemizar contra ella). ⚠️ D9: la lectura literal ("8 % magic damage" del golpe) daría ~55/golpe (+2.7 % DPS total).

### 3.2 Unleash — la economía que habilita todo

| Regla | Valor | Explotación |
|---|---|---|
| Cargas por auto | 1 (minion) / **2 (campeón)** · cap **6** · duración 6 s (refresh al pegar) · decaimiento 1/0.5 s | **3 autos a campeón = Q instantánea**; pre-stackea en minions antes del engage |
| Q activa (consume cargas) | **+55 % AS (5 s)** + autos empoderadas: **+25 mágico on-hit** y **spread (18 + 30 % AD) físico a cercanos** | El AS de Q ya está en B: pelear sin Q = **−13 % AS y −100 % del spread** |
| Durante R (Transcendent) | Q **automática y permanente** + **el spread CRITICA (×2.30 con IE)** + 250 % vs minions <30 % | La ventana de R (15 s) ES la ventana de daño: spread crítico a 2 objetivos ≈ **+1 350 DPS en 3v3** |
| Spread + Kraken (7.3 oficial) | El spread proca Bring It Down | Modelado +50 % procs AoE (D13) |

> [!TIP]
> **Regla de oro:** el DPS real de Yunara vive en dos ventanas encadenadas — **Q (5 s, siempre activa si gestionas cargas) y R (15 s / CD 50)**. Fuera de R, el spread NO critica: el "3v3 sostenido" honesto es ~5 700, no los 10 551 publicados (que asumían spread crítico permanente). Pelea corta = activa R; pelea larga = el valor de Runaan's (bolts críticos SIEMPRE) sube relativamente.

---

## 4. HABILIDADES (valores 7.3, rank 4 / R rank 3) Y MECÁNICAS EXPLOTABLES

### Q — Cultivation of Spirit · 30 maná · sin CD (consume Unleash) · ver §3
### W — Arc of Judgment · CD 10 s · 60 maná
Cuentas giratorias: **(210 + 85 % bAD + 50 % AP) mágico + slow 99 %** (decae 1.5 s) + lingering 1 s con **4 ticks (26 + 12 % bAD + 7.5 % AP)/0.25 s**. En R → **Arc of Ruin**: láser **(160 + 120 % bAD + 75 % AP)** + slow 99 % + **refund 80 % del CD al entrar/salir de R**; cast time escala con AS permanente; ejecuta minions bajos.
- Su único "CC" (slow 99 % ≈ root funcional): **coloca la alfombra de spread y kitea melees**. W-DPS ≈ 58/s mágico (mitigado por MR — el reporte no lo contaba).
### E — Kanmei's Steps · CD 9 s · 40 maná
**+45 % MS 1.5 s → 67.5 % hacia campeones visibles**. En R → **Untouchable Shadow (dash)** con CD refrescado al entrar/salir de R. Sin R: su única defensa es MS; con R: dash + intargeteable.
### R — Transcend One's Self · CD 70/60/50 s · 100 maná
**15 s de Transcendent:** Q automática (spread crítico permanente), W→Ruin, E→dash, habilidades sin maná. **Es a la vez su burst, su CC y su defensivo** — el CD 50 s a rank 3 dicta el ritmo de las teamfights (pelea SIEMPRE con R disponible; Fiendhunter da 20 ult haste = −16.7 % CD, su nicho).

---

## 5. ¿CON QUÉ ESCALA YUNARA? (respuesta por stat)

| Stat | ¿Escala? | Números |
|---|---|---|
| **AS** | ✅ **PRIMARIO** | Multiplica autos, bolts, **spread** (por auto), bala LT (73.4/golpe con B 3.372), Kraken/BotRK y cadencia de Unleash. Cap 3.0 alcanzable: ítems 155 % + Flurry = 2.96-3.0. Cada 1 % de AS nunca es oro muerto (Ley 2 al límite justo). |
| **Crítico** | ✅ **100 EXACTO (4 fuentes)** | Autos ×2.30 · bolts Runaan's ×2.30 · **spread ×2.30 (en R)** · pasiva (por crítico). Yun Tal+Runaan's+IE+LDR = 100.0; +25 % = 1 250 g muertos (Ley 1). |
| **AD** | ⚠️ **SECUNDARIO HÍBRIDO** | bAD 200 en la óptima: spread 30 % · W 85 %/Ruin 120 % (¡su W escala bAD!) · autos/bolts 100 %. La variante A2 (C44+Yun Tal, AD 355) gana +10.8 % 1v1 a costa de −28 % 3v3. |
| **Pen %** | ✅ **OBLIGATORIA (Ley 3)** | Meta de tanques (Cho'Gath S jungla, Malphite S+): LDR 35 % + GS 12 % = +47.9 % vs tanque full; TTK tanque 3.0 s con la óptima (3.8 s con la publicada). |
| **LS/sustain** | ✅ **SU ÚNICA "DEFENSA" COMPRABLE** | Gunmetal 5 % (+12/golpe) = 155 HP/s · +BotRK 12 % = **500 HP/s** · doble BotRK+BT = 740 HP/s. La matriz de dive (§8.4) muestra que el sustain puntúa MEJOR que la armadura en el objetivo riesgo-ajustado. |
| **Armadura/RM** | ❌ **NO COMPRA (glass por diseño)** | EHP 4 162 idéntica en toda build de daño; GA/Scimitar suman +479 EHP a coste de −16 a −24 % DPS. Su "item defensivo" es la R (1.5 s intargeteable + dash). |
| **AH** | ⚠️ niche | Solo para R (Fiendhunter 20 ult haste); maná 807 basta (R = habilidades gratis 15 s). |
| **AP** | ❌ muerto | Solo alimenta pasiva (8 %/100 AP) y ratios de W — sin conversión suficiente (Nashor/Statikk ❌). |
| **MS** | ⚠️ **UTILIDAD (sin dashes fuera de R)** | E 45→67.5 % + Noxian Gait 7 % + Runaan's/Yun Tal 4 % + Ghost. Kiting = su supervivencia. |

---

## 6. CURVA DE PODER Y LECTURA DE ROL (DRAGON LANE)

- **Early (0–7 min):** Berserker's 4:30 → **Yun Tal 7:30-8:00** (componentes que pegan; ramp de crit 125 autos ≈ min 8-9; Flurry desde 7.3a). Lvl 9: **539 DPS** (Yun Tal) vs 496 (C44) — ver §8.5: el veredicto publicado C44-1.º usaba Yun Tal pre-7.3a (D8).
- **Mid (10–14 min):** Runaan's 10:30 (bolts críticos SIEMPRE: **lvl 12 = 778 1v1 / 1 735 3v3** con Yun Tal) → ⬆️Gunmetal 11:30. **IE 14:30 = EL spike** (spread ×2.30 + bolts ×2.30: **lvl 14 = 1 435 / 3 575**, +84 % 1v1 sobre lvl 12).
- **Late (17–21 min):** BotRK ~17:15 (sustain ×3 + %vida) → LDR ~20:15 (Ley 3 vs tanques). **Pico corregido: 2 881 1v1 / 6 593 3v3-ventana / 1 650 vs120 / 1 504 vsTanque** (sostenido real: 2 864/5 687/1 637/1 494). Nexus 4 000: el pico llega a tiempo.
- **Lectura DUO:** S+ con ban 22.94 % — **prioridad de draft solo bajo Yunara-ban**... ella ES Yunara: cuando sale de la mesa de bans, es la ADC con más techo de teamfight del parche. Comps: **teamfight estructurado con engage aliado** (ella añade spread+slow 99 %, no initiate). Counters: **dive doble** (Zed-like/Rengar + Leona) → matriz §8.4; **poke de rango** (Caitlyn/Jhin — pelea a <550 anula Magnification... que solo vale −2.9 % DPS: el counter real es el burst, no el poke); **CC en cadena** (sin QSS nativo → Scimitar situacional). Sinergias: enchanters (Yuumi/Karma/Seraphine — cubren su falta de defensivos), engage supports (Nautilus/Leona/Jarvan — meten enemigos en la alfombra), Rakan (publicado).

---

## 7. SOBREEXPLOTACIÓN — LAS 10 PALANCAS (resumen ejecutivo)

1. **Pre-stackea Unleash (6 cargas) ANTES del engage:** 3 autos a campeón o 6 a minion → Q instantánea = +55 % AS + spread desde el primer segundo.
2. **R es la teamfight:** 15 s de spread crítico ×2.30 a 2+ objetivos (+1 350 DPS en 3v3) + Ruin (99 % slow + refund 80 %) + dash con CD refresh. Nunca la gastes en daño single-target fuera de ventana.
3. **W→alfombra:** slow 99 % coloca enemigos sobre las plumas/spread y kitea melees; el lingering tick escala bAD (la AD no es stat muerto en ella).
4. **BotRK triple-proc:** en R+Runaan's, cada auto pega principal + 2 bolts (+spread) — todos aplican on-hit (texto oficial): Ruined Strike 7 % por objetivo = el motivo de +25.5 % vs tanques.
5. **Flurry = cap de AS:** +35 % AS/6 s pone la AS efectiva en **3.0 exacto** durante R (raw 3.07) — sincroniza Flurry con la ventana de R.
6. **Cristales desde rango:** Q/W/auto detona Crystalline Overgrowth (3.3-18.9 % verdadero, ~50 s) — placa gratis sin exposición; placas 7.3a +20 arm/MR.
7. **Bala LT escala con B total:** 73.4/golpe ×2.96 AS = **+217 DPS solo de runa** — la AS double-dipea (cadencia + bala).
8. **Pasiva híbrida:** ~71/s de daño mágico no mitigable con armadura — los tanques que stackean armadura contra ella pierden el 100 % de ese término + GS.
9. **E agresiva:** 67.5 % MS HACIA campeones visibles = herramienta de posicionamiento ofensivo (no solo huida); en R es dash — guarda la carga de E para el dive enemigo.
10. **Front-to-back estricto:** sin CC propio y con EHP 4 162, cada pelea empieza con R disponible (CD 50) o no empieza.

---

## 8. BUILDS — RE-VERIFICACIÓN + DERIVACIÓN NUEVA (motor batch4)

> **Motor `model/yunara_model.py`:** port de `eval_build` + términos propios integrados a la búsqueda (spread con crit-condicional-por-R, pasiva, Q on-hit, W Judgment/Ruin mitigados por MR proxy 40/80/150, Kraken-vía-spread +50 %, Flurry, Magnification por uptime) + **módulo de supervivencia** con las convenciones del lab (`ehp_y_util`: EHP mixto 50/50 + escudos ponderados bt 255×0.5/shieldbow 425×0.5 + UTIL ga 300/scimitar 150 + heal×2.5 s). Búsqueda: 119 864 hojas legales (crit≤100, pen≥30, ≤18 000 g, Ley 3b), 4 objetivos ponderados.

### 8.1 Verificación de los titulares publicados (misma convención de ventana, inputs corregidos)

| Build | Escenario | Publicado | Re-verificado | Δ |
|---|---|---|---|---|
| **STD (Gunmetal+C44+Runaan's+IE+LDR+Kraken)** | 1v1 / 3v3 / vs120 / vsT / heal | 3 042 / **10 551** / 2 150 / 1 480 / 186 | **2 613 / 6 142 / 1 498 / 1 199 / 155** | −14 % / **−42 %** / −30 % / −19 % / −17 % |
| **A2 anti-tanques (C44+Yun Tal+BotRK+LDR+IE)** | ídem | 3 115 / 9 285 / 2 451 / 1 850 / 525 | 2 995 / 4 735 / 1 715 / 1 516 / 515 | −4 % / **−52 %** / −30 % / −18 % / −2 % |
| **Comunidad-RFC (Kraken+RFC+IE+LDR)** | 1v1 / 3v3 / vsT | 2 850 / 8 900 / 1 320 | 2 643 / 4 097 / 1 211 | −7 % / −54 % / −8 % |

**Causas raíz (auditadas):** AD 268 sin growth (correcto 310) · AS "2.83" irrazastreable (correcto 2.647; su §3 usaba 2.42 omitiendo Kraken 35 %) · **spread crítico permanente** (solo existe durante R: uptime real 23 % sostenido / 100 % en ventana) · Magnification aplicada a términos que el engine no amplifica · **términos mágicos (pasiva/Q/W) sin mitigar por MR**. Los rankings internos del reporte, en cambio, sí aguantan (STD > comunidad; A2 > STD vs tanques).

### 8.2 La derivación nueva — TABLA A corregida (top-1 de los 4 objetivos del optimizador)

| Slot | Ítem | Oro | Rol en la build |
|---|---|---|---|
| 1 (botas) | **Berserker's → ⬆️ Gunmetal Greaves** (min 10:00, MISMO slot) | 2 200 | 50 % AS + 5 % LS + Blessed 12/golpe + Noxian Gait |
| 2 | **Yun Tal Wildarrows** ⬅️ *cambio vs publicada* | 3 100 | AD 50 + AS **35 % (7.3a)** + crit ramp 25 % + **Flurry +35 % AS** (→ cap 3.0 en R) |
| 3 | **Runaan's Hurricane** | 2 650 | Bolts 55 % AD ×2 que **critican SIEMPRE** ×2.30 + on-hit (el AoE que no depende de R) |
| 4 | **Infinity Edge** | 3 400 | ×2.30 global (autos/bolts/spread-en-R) |
| 5 | **Lord Dominik's Regards** | 3 300 | 100 % crit exacto + 35 % pen + GS 12 % (Ley 3 vs meta de tanques) |
| 6 | **Blade of the Ruined King** ⬅️ *cambio vs publicada* | 3 100 | **7 % vida actual (oficial 7.3)** por golpe Y por bolt + 12 % LS + 30 % AS |

> **Total: 17 750 g** · AD 300 · **AS 2.96** (Flurry 50 %; raw 3.07 → cap 3.0 con Flurry 100 %) · crit 100 exacto · pen 35 % · LS 17 % → **heal 500 HP/s** · EHP 4 162.
> **Piso conservador (engine 6 %, sin Flurry):** 1v1 **2 702** · 3v3 **6 270** · vs120 **1 549** · vsTanque **1 391** → vs STD publicada: **+3.4 % / +2.1 % / +3.4 % / +16.1 %**, heal ×3, surv +17.2 %.
> **Techo oficial 7.3a (BotRK 7 % + Flurry 50 %):** 1v1 **2 881** · 3v3 **6 593** · vs120 **1 650** · vsTanque **1 504** (TTK tanque **3.0 s** vs 3.8 s) → vs STD: **+10.3 % / +7.3 % / +10.2 % / +25.5 %**, heal ×3.2. **Sostenido real** (q 0.7, R 23 %, magn 0.8): 2 864 / 5 687 / 1 637 / 1 494.
> *(Convergencia cross-campeón: son los mismos 6 slots de la óptima de Xayah — el arquetipo crit-AoE 7.3a converge.)*

**Tabla B — Ruta:** Long Sword (0:00) → Berserker's (1 700, ~4:30) → **Yun Tal** (4 800, ~7:30) → Runaan's (7 450, ~10:30) → ⬆️ Gunmetal (8 450, ~11:30) → IE (11 850, ~14:30) → **BotRK** (14 950, ~17:15) → LDR (18 250 acum., ~20:15).
**Runas:** LT × Legend: Alacrity (baseline del arquetipo; verificado en Xayah −16.3 % sin LT) · Brutal · Cut Down (vs tanques, default meta) / Coup de Grace · Bone Plating (vs dive/poke) / Gathering Storm · **Flash + Ghost** (publicado — su MS es su defensa). **Skills Q→W→E** (R 5/9/13).

### 8.3 Optimizadores (119 864 hojas; scores normalizados)

| Objetivo | Top-1 | Score | Evidencia |
|---|---|---|---|
| **DPS puro** (el del reporte) | Gunmetal+**Yun Tal**+Runaan's+IE+LDR+**BotRK** | 91.4 % | 2 702/6 270/1 549/1 391 (engine 6 %, sin Flurry — techo: 2 881/6 593) |
| **Riesgo-ajustado** (DPS .64 / surv+sustain .36) | **la misma** | 81.2 % | heal 500 pesa más que cualquier GA/Scimitar |
| **Anti-tanque** (vsT .35) | A2 publicada (C44+Yun Tal+BotRK+LDR+IE, sin Runaan's) | 85.4 % | vsT 1 516 piso / 1 634 techo pero 3v3 −28 %: **variante duelista**, no default |
| **Vs dive** (surv .32, magn 0.6) | **la misma default** · #4: BotRK+BT (heal 740) | 81.3 % | Su defensa es sustain+R, no armadura — GA/Scimitar solo vs amenazas concretas |
| DPS puro #2/#3 | C44+BotRK (89.9 %) · A2 (89.6 %) | — | Kraken NO aparece en ningún top-5 |

### 8.4 Matriz riesgo/daño (la pregunta del autor, con números — 6.º slot y swaps; params piso uniformes: engine 6 %, sin Flurry)

| Variante | 1v1 | 3v3 | vsT | EHP | heal/s | surv | Lectura (vs STD publicada) |
|---|---|---|---|---|---|---|---|
| **Kraken (publicada STD)** | 2 613 | 6 142 | 1 199 | 4 162 | 155 | 4 551 | referencia |
| **Yun Tal+BotRK (nueva óptima)** | **2 702** | **6 270** | **1 391** | 4 162 | **469** | **5 335** | ✅ +3.4 % 1v1 · +16.1 % vsT · heal ×3 (techo oficial: +10.3 %/+25.5 %) |
| BotRK por Kraken (cambio mínimo) | 2 689 | 6 023 | 1 375 | 4 162 | 465 | 5 325 | ✅ +2.9 % 1v1 · +14.7 % vsT · −1.9 % 3v3 (Kraken-vía-spread) |
| Shieldbow+BotRK (por C44/Kraken) | 2 506 | 5 840 | 1 290 | **4 373** | 434 | 5 458 | ⚠️ −4.1 % 1v1 por Lifeline 300-550: el seguro barato que mantiene crit 100 |
| Scimitar 6.º | 2 193 | 5 325 | 1 015 | **4 641** | 379 | **5 739** | ⚠️ −16 % DPS: solo vs CC en cadena (QSS) — máx surv de la matriz |
| GA 6.º | 2 193 | 5 325 | 1 015 | 4 641 | 132 | 5 271 | ⚠️ −16 %: solo vs one-shot (revivir 180 s) |
| BT 6.º | 2 384 | 5 801 | 1 105 | 4 289 | 478 | 5 484 | ❌ Ichorshield < BotRK en todo (−8.8 %) |
| Death's Dance 6.º | 2 225 | 5 405 | 1 030 | 4 701 | 134 | 5 155 | ⚠️ Cauterize ranged (12 %) no paga el −14.8 % DPS |
| Maw / Wit's End 6.º | 2 256 / 2 288 | 5 484 / 5 358 | 1 045 / 1 051 | **4 847** / 4 701 | 135 / 141 | 5 185 / 5 053 | ⚠️ anti-AP: máx EHP, −12 a −14 % DPS |
| Armored/Chainlaced (botas) | 2 279 | 5 375 | 1 047 | 4 864/4 805 | **0** | 4 864/4 805 | ⚠️ −12.8 % DPS y pierde TODO el sustain de botas |
| Fiendhunter por C44 | 2 333 | 5 621 | 1 065 | 4 162 | 145 | 4 586 | ❌ DPS (−10.7 %); nicho: 20 ult haste = R cada 41.7 s |
| Stormrazor por C44 | 2 565 | 6 213 | 1 173 | 4 162 | 154 | 4 548 | ⚠️ anti-poke (Energized+MS): −1.8 % 1v1, +1.2 % 3v3 |

**Respuesta a la hipótesis del autor:** el riesgo de Yunara NO se paga con daño — se paga eligiendo mal el sustain. La publicada (Kraken, heal 155/s, surv 4 551) era de las opciones más frágiles de jugar entre las legales; la derivación corregida sube daño Y supervivencia efectiva (**surv +17.2 %** con +400 g y la misma EHP). Los defensivos puros (Scimitar/GA/Maw) solo entran contra amenazas nombradas, a −12/−16 % de DPS medido — y su R (1.5 s intargeteable + dash, CD 50) sigue siendo su verdadero "slot defensivo".

### 8.5 Primer ítem — el flag del lab resuelto (checkpoints con modelo completo, valores 7.3a)

| 1.er ítem | lvl 9 1v1 | lvl 9 3v3 | lvl 12 1v1 | Publicado lvl 9 | Nota |
|---|---|---|---|---|---|
| **Yun Tal (Flurry 50 %)** | **539** | **821** | 818 | 480 (pre-7.3a) | ✅ **Nuevo veredicto:** converge a la óptima del optimizador |
| Kraken | 522 | 814 | 824 | 560 (inflado) | ⚠️ su proc no escala crit ni feedea R |
| Stormrazor | 519 | 774 | 787 | 520 ✓ | Alternativa anti-poke |
| C44 (publicado 1.º) | 496 | 741 | 770 | 495 ✓ | ⚠️ Magnification solo vale ~3 % del DPS total (sensibilidad magn 0.6: −2.9 %) — su caso dependía de un supuesto débil |
| BotRK | 683 | 916 | 974 | — | ❌ como 1.º: 3 100 g sin crit retrasa IE/spread ×2.30 (raw-DPS tramposo en dummy) |

La tabla §5 publicada contradecía su propio veredicto (Kraken ganaba lvl 12 en sus cifras: 930 vs 860) y evaluaba Yun Tal con stats pre-7.3a — exactamente lo que el lab marcó en §3b ("revisar 1.er ítem"). **Corregido: Yun Tal primero.**

---

## 9. DISCREPANCIAS REGISTRADAS (protocolo lab §D)

| # | Tema | Resolución |
|---|---|---|
| D1 | **AD publicado 268** | Omitió el growth (58+3.0×14 = 100, no 58): correcto **310** en STD / **300** en la nueva óptima. Afecta todas las fórmulas manuales del §3 publicado |
| D2 | **"AS 2.83 (con Pow-Pow x3)"** | Irrazastreable (¿doble conteo de Q?). Correcto STD: **2.647**; nueva óptima: 2.96 (Flurry 50 %). Su §3 usaba además 2.42 (AS-ítems 0.90, omite Kraken 35 %) — dos AS distintos en el mismo reporte |
| D3 | 1v1 3 042 irreproducible | Correcto: **2 613** (ventana, sus supuestos) — inflado +16.4 %. Ni con AS 2.83 + spread fantasma se alcanza |
| D4 | **3v3 10 551 irreproducible** | Correcto: **6 142** ventana / 5 687 sostenido-real / 5 271 (STD sostenida) — inflado ~+72 %. Causas: spread crítico permanente (R uptime 23 % real), magn sobre spread/bolts, mágicos sin MR, AS errónea |
| D5 | vs120 2 150 / vsT 1 480 | Correcto: 1 498 / 1 199 (STD) — inflados +43 %/+23 % |
| D6 | heal 186/525 | Correcto: 155/515 (el de A2 casi cuadra; el de STD usaba su DPS inflado) |
| D7 | Tabla maestra con fila **ILEGAL** (On-Hit Terminus+LDR, Ley 3b) publicada con cifras; fila "comunidad" (RFC) que no matchea la build wr-meta real (Kraken+Runaan's) y usa RFC (0 AD en 7.3) | Rehacer ambas en la regeneración |
| D8 | §5 primer ítem con **Yun Tal pre-7.3a** (480) y veredicto C44 contradicho por su propia tabla (Kraken 930 > C44 860 a lvl 12) | Con valores 7.3a: **Yun Tal 539 = 1.º** (flag §3b del lab resuelto) |
| D9 | Pasiva: 8 % ¿de AD o del daño del golpe crítico? | Reporte: 8 %×AD (21.4); literal: 8 %×golpe (~55) → Δ +2.7 % DPS. Rankings sin cambio. **Verificar en juego** |
| D10 | Q on-hit "+20 %" con fuente truncada en el scrape (¿AP? ¿bAD?) | Modelado plano 25 (AP=0 en build crit). **Verificar en juego** |
| D11 | Rango de ataque no publicado (≥550 asumido para Magnification) | Heredado del reporte; la sensibilidad magn 0.6 = −2.9 % muestra que ya no decide nada (otro motivo más contra C44-1.º) |
| D12 | Callout meta 05/10 (51.64/16.83/23.80) vs vigía 11/10 | Canónico: **51.44/15.83/22.94 (High, 0)**; banda 50.85-51.64 desde 24/09; ban 13→23 % post-buff |
| D13 | Kraken proca con spread (oficial 7.3): magnitud sin verificar | Modelado +50 % procs en AoE (declarado); ni con ese bonus Kraken gana el slot 6 a BotRK |
| — | **Triage** | Δ ≥5 % en métricas de resultado + inputs del spec erróneos (D1/D2) → **❌ REGENERAR** (umbrales §E del lab). Esta ficha + `model/yunara_model.py` son el insumo; el publicado no se toca en silencio |

---

## Pie de página
Fuentes: WR-LAB completo v1.15 (reporte publicado `yunara` v1.2 08/10 con bloque WRLAB-VERIF + FRAMEWORK/Leyes 0-7 + `dps_model.py`/`optimize_build.py` (convenciones `ehp_y_util` reusadas) + notas oficiales 7.3 (sección YUNARA, Kraken/Fiendhunter/Yun Tal) y 7.3a + apéndice AS + ficha wr-meta 24/09 + win rates vigía 11/10 + flag §3b "Yunara: revisar 1.er ítem") · motor de re-verificación y derivación `model/yunara_model.py` (batch4) con resultados en `model/yunara_resultados.txt` (119 864 hojas × 4 objetivos + matriz de riesgo de 16 variantes + checkpoints + 8 sensibilidades). Hallazgo central: **la derivación corregida (Yun Tal+BotRK) domina a la publicada en los 4 escenarios (+7 a +25 %) con ×3.2 sustain — el trade daño/riesgo era una falsa dicotomía causada por inputs erróneos.** Documento no oficial; Wild Rift es marca de Riot Games.
