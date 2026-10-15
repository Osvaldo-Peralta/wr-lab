---
tags: [wrlab, ficha, xayah, adc, dragon-lane, critico-aoe, re-verificacion, parche-7.3a]
version: 1.0
Status: Borrador (entregado 12/10/2026 — re-verificación del reporte publicado xayah v2; pendiente de verificación en juego del autor)
champion: Xayah
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — XAYAH · DRAGON LANE (Wild Rift 7.3 + hotfix 7.3a)

**Fecha:** 12/10/2026 · **Fuentes:** WR-LAB v1.15 (primaria: reporte publicado `xayah` v2 engine 08-09/10 + notas oficiales 7.3/7.3a + apéndice AS + items_7.3.csv + win rates vigía 11/10 + wiki oficial + wildriftcore 09/10) + **motor de re-verificación batch4** `model/xayah_model.py` (resultados en `model/xayah_resultados.txt`)
**Rol:** ADC — Dragon Lane (DUO, A ↑3) · **Arquetipo lab:** Crítico AoE (`aa_aoe` vía Runaan's; E escala crit desde 7.3) · **engine:** autos (spec en `champspecs.py` desde 09/10) + **términos de skills ahora integrados en la búsqueda**
**Tesis:** El buff 7.3 la convirtió de "ADC de utilidad sin burst" en **ejecutora de área escalada al crítico**: E pasa a ×1.65 con IE y el crítico alimenta **4 fuentes** (autos, pluma de W, E, rayos de Runaan's). Con AS-base 0.658, **la AS es el multiplicador del multiplicador** (autos + balas LT + rayos + BotRK + cadencia de plumas). Build de techo de daño: **cero defensa comprada, todo multiplicadores** — la defensa ES la R (1.5 s intargeteable) y el posicionamiento front-to-back.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, 11/10/2026):** DUO **A** · WR **50.10 %** · pick **4.32 %** · ban **0.18 %** (Confidence Med, **↑ 3**). Banda reciente: 49.87 % (05/10) → 50.17 % (08/10, ↑2) → 50.10 % (11/10); wildriftcore 30 d: 49.89 %, efecto 7.3 = **+0.40 pts WR / +2.68 pts pick en 10 días** — A-tier en ascenso post-buff. Contexto bot 11/10: **Yunara S+ 51.44** (ban 22.94 — la ADC que define el parche), **Kalista S 51.34**, Jinx A 50.20, Caitlyn A 49.56 (pick 20.13), Sivir A 49.23. Xayah no compite en prioridad de draft con Yunara/Jinx pero su ban ~0.2 % = **siempre disponible**; pick de teamfight estructurado con soporte de engage (Rakan/Nautilus/Leona/Jarvan IV).
> **Veredicto de la re-verificación:** ✅ **REPRODUCIDO** — las 6 builds de referencia del reporte v2 se reproducen al ±0.3 % en los 4 escenarios con motor independiente; el optimizador extendido (engine + skills integrados, 27 720 hojas legales) **re-encuentra la Tabla A como top-1 (91.1 %)**. Δ = 0 % < 2 % → la build publicada sigue vigente (regla de oro v1.6: no se regenera).

---

## 1. QUÉ LE HIZO ESTE PARCHE (por qué sube mientras nadie la banea)

### 1.1 Cambios 7.3 (21-sep-2026, notas oficiales — sección XAYAH)

| Stat / Habilidad | Antes (7.2) | Ahora (7.3) | Impacto |
|---|---|---|---|
| AD base | 54 | **60** | +11.1 % early |
| AD growth | 5.0 | **4.2** | −11.2 AD a lvl 15 → neto **−5.2 AD late** (pago del buff) |
| AS (apéndice oficial) | — | **0.658 / 0.658 / 0.22 / 0.034** | La sección XAYAH dice 0.03 → discrepancia D1 (display in-game 0.022 = 0.658×0.034 corrobora el apéndice) |
| W — AS | 45/50/55/60 % | **40/45/50/55 %** | −5 %/rank |
| W — pluma extra | 20 % del daño del ataque | **25 %** | ✅ ×1.25 en ventana de 4 s (copia el ataque: hereda crit y on-hit) |
| W — MS | 25/30/35/40 % | **30 % flat** (1.5 s) | neutro en rank 4 |
| **E — Bladecaller** | 60/70/80/90 + 90 % bAD | **(70/80/90/100 + 50 % bAD) × (1 + 50 %·crit + 50 %·(critDmg−2)·crit)** | ✅ **BUFF ESTRUCTURAL:** a 100 % crit + IE = **×1.65** — E deja de ser AD-plano y escala con TODA la build |
| R — Featherstorm | 125/250/375 + 100 % bAD | **150/250/350 + 100 % bAD** | +25 base rank 1 (early) |

### 1.2 Hotfix 7.3a (29-sep-2026) — Xayah sin cambios; su core 1 sí

| Cambio | Detalle | Efecto |
|---|---|---|
| **Yun Tal Wildarrows** | AS 25→**35 %** · Flurry +25→**+35 % AS** (CD 20→25 s) | Su primer ítem (diseñado por Riot como first-item de eficiencia) mejora: converge aún más al óptimo del lab |
| Nexus | 5 500→**4 000 HP** | Partidas ~1-2 min más cortas: el 6.º ítem (LDR, ~20:15) **sí llega a importar** |
| Placas | +30 arm/MR 20 s → **+20 / 10 s** | Siege más fácil con W+Runaan's |

**Efecto neto 7.3+7.3a:** el crítico pasa de valer solo en autos a valer en 4 fuentes; la AS sube de tope (2.5→3.0) justo para su build de 155 %; y su ítem puente recibe el buff del hotfix. Resultado medido (wildriftcore): +0.40 pts de WR y +2.68 pts de pick en 10 días, con ban ~0.2 % — **valor de draft en ascenso sin presión de baneo**.

---

## 2. FICHA MATEMÁTICA (spec 7.3a — en `champspecs.py` desde 09/10)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base / growth | **60 / 4.2** → 118.8 @15 | notas 7.3 (sección XAYAH) — primaria |
| HP | 630 (+120 → **2 310**) | ficha wr-meta 08/10 + wiki |
| Armadura / RM | 40 (+4 → 96) / 30 (+1.4 → 49.6) | ficha wr-meta + wiki |
| Maná / MS / rango | 435 (+41 → 1 009) / 335 / **575** | ficha wr-meta; rango wiki |
| AS (7.3) | ratio **0.658** · base **0.658** · BBA **0.22** · growth **0.034** → lvl 1 = 0.8 display · **lvl 15 sin ítems = 1.116** | apéndice oficial (D1) |
| `self_as_buff` | **0.55** (W rank 4, 4 s / CD 14 s → uptime sostenido 29 %) | convención engine; sensibilidad D7 |
| Daño crítico | 200 % base / **230 % con IE** · `crit_dmg_mod` 1.0 | notas 7.3 |
| `uses_magnification` | True (575 ≥ 550) — **irrelevante en la óptima** (no lleva C44) | engine |
| Proyectil / viento | autos físicos a 575 · Q/E/R físicos | wiki |

**B total de la build óptima = 3.390** (0.22 base + 0.476 niveles + 1.55 ítems + 0.384 LT + 0.21 Alacrity + 0.55 W) → **AS = 0.658×4.390 = 2.889** (96.3 % del cap; cruda con W+Flurry = **3.119 → cap 3.0** en ventana). AS de ítems para cap exacto con W: **171.9 %** — la build lleva 155 %: 0 overshoot estructural, el resto lo cubren Flurry/LT por ventanas.

---

## 3. PASIVA — CLEAN CUTS + ECONOMÍA DE PLUMAS (el campeón entero vive aquí)

### 3.1 Clean Cuts
Castear cualquier habilidad → **3 cargas** (cap 5, ventana 7.5 s). El próximo auto consume una carga y lanza una **pluma**: daño del auto al principal **+ 45 % AD físico a todos los enemigos en línea** (sin crit). Las plumas clavadas en el suelo duran **6 s** — E las recupera TODAS.

### 3.2 Economía de plumas (la parte que MÁS se juega mal)

| Fuente | Plumas | Nota |
|---|---|---|
| Auto empoderado (3 cargas por casteo) | 1 por auto | ~3.3 casteos/10 s ≈ **1 auto empoderado/s** en pelea |
| Q (Double Daggers) | **2** por casteo | CD 7 s, rango 1 000 — coloca plumas SIN pelear |
| R (Featherstorm) | **5** en cono | R→E instantáneo = E de **8 plumas (1 716)** |

- **E (Bladecaller):** (100 + 50 % bAD) × **1.65** (100 % crit + IE) por pluma, con **decaimiento −10 % por pluma previa sobre el mismo objetivo (piso 10 %)** → Σ(5) = 4.0 · Σ(8) = 5.2 · Σ(15) = 6.0 (¡no 15×!). **3+ plumas sobre un objetivo = root 1.25 s.** Minions reciben 50 %. CD 8 s.
- **Burst de referencia (bAD 200, 100 % crit + IE):** 330 la primera pluma · **E(3) = 891 + root** · **E(5) = 1 320** · **E(8 post-R) = 1 716** · E(15 alfombra completa) = 1 980.
- **Regla de alfombra:** las plumas duran 6 s y E tiene CD 8 → la pelea se prepara ANTES: Q + autos sobre la zona, pelea encima de TU alfombra, E multi-root (3+ plumas por enemigo), R defensiva o de reposicionamiento + 5 plumas, E otra vez.

> [!TIP]
> **El root de E es a distancia de pluma, no de Xayah:** puedes enrootar desde 1 000+ (donde cayó la Q) sin estar a rango de auto. Y contra diving: R (intargeteable 1.5 s) → las 5 plumas caen alrededor tuya → E al salir = 8 plumas (1 716) + root sobre el diver. Es SU combo defensivo-ofensivo: la R gastada en daño te deja sin la única defensa (CD 60 s).

---

## 4. HABILIDADES (valores 7.3) Y MECÁNICAS EXPLOTABLES

### Q — Double Daggers · CD 7 s (10→7 por rank) · 50 maná · rango 1 000
2 dagas: **(125 + 50 % bAD)** c/u (2.º+ objetivo: 50 %) · deja **2 plumas**. Poke, waveclear y colocación de root a distancia.
### W — Deadly Plumage · CD 14 s · 50 maná
4 s de **+55 % AS** (rank 4) y autos que disparan **pluma extra = 25 % del daño del ataque** (hereda crit ×2.30 y on-hit — la convención ×1.0714 del engine) · +30 % MS 1.5 s al golpear campeón. **Uptime sostenido 29 %** → activarla SOLO en ventana de pelea (sensibilidad D7: pelear sin W = **−17.8 % de DPS total**).
### E — Bladecaller · CD 8 s · 40 maná · ver §3.2
### R — Featherstorm · CD 60 s · 100 maná · rango 1 000
**1.5 s intargeteable** (sin autos/casteos,移动 permitida) + **5 plumas en cono: 350 + 100 % bAD** c/u (**1 650** si 3/5 conectan · 2 750 las 5 a quemarropa). Anti-gank/anti-burst (R de Zed, hook de Thresh, CC de Leona) + setup de E(8).

---

## 5. ¿CON QUÉ ESCALA XAYAH? (respuesta por stat)

| Stat | ¿Escala? | Números |
|---|---|---|
| **AS** | ✅ **PRIMARIO (el multiplicador del multiplicador)** | AS-base 0.658: cada 1 % de AS multiplica autos + balas LT + rayos + BotRK + cadencia de plumas. Build: 155 % ítems → 2.889 (96.3 % cap); cap exacto pide 171.9 %; W+Flurry rompen a 3.0 en ventana (overshoot solo 3.9 %). Lección v1 Beta: 40 AD extra con AS 2.46 **perdió** contra 155 % AS con AD 319 (+11.6 % DPS neto). |
| **Crítico** | ✅ **ÚNICO EXACTO (100 %)** | Alimenta 4 fuentes: autos ×2.30 · pluma W (copia ×2.30×0.25) · **E ×1.65 (fórmula 7.3)** · rayos Runaan's ×2.30. Yun Tal(25)+Runaan's(25)+IE(25)+LDR(25) = **100.0 exacto**; +25 % sobrante = 1 250 g muertos (Ley 1). |
| **AD** | ⚠️ **SECUNDARIO (pero alimenta TODO)** | bAD 200 en la óptima: E 50 % · Q 50 % · R 100 % · autos/rayos 100 %. El trade AS>AD plano ya está resuelto (v1→v2: −40 AD, +11.6 % DPS). |
| **Pen %** | ✅ **OBLIGATORIA (Ley 3)** | Meta de tanques 7.3a (Cho'Gath jungla 50.8 · Malphite S+): LDR 35 % + GS 12 % = **+47.9 % vs tanque full**; sin pen, vsTanque −32 %. Control del optimizador sin restricciones: la build 0-pen gana +12.3 % de 1v1 crudo pero **−9.2 % vs120 y −21.7 % vsTanque** ❌. |
| **LS / sustain** | ⚠️ **SU ÚNICA DEFENSA COMPRADA** | 17 % (BotRK 12 + Gunmetal 5) → **498 HP/s** + Blessed 12/golpe. La build NO compra escudos/revivir/armadura: 2 310 HP, 96 arm, 49.6 MR a lvl 15. |
| **AH / Maná** | ❌ **MUERTOS** | Pool 1 009 basta (Q50/E40/W50); Crimson Lucidity = −0.36 AS ≈ −260 DPS ❌. |
| **AP / RM / armadura** | ❌ muertos (solo variantes: GA/Scimitar/Shieldbow/Chainlaced/Armored cuestan −11.3 a −17.7 % DPS, medido §8.5). |
| **MS** | ⚠️ **UTILIDAD (kiting)** | W +30 % (1.5 s) + Noxian Gait +7 % + 4 % Runaan's/Yun Tal + 7 % PD-no-tomado. Sin dashes propios: la R es el único reposicionamiento. |

---

## 6. CURVA DE PODER Y LECTURA DE ROL (DRAGON LANE)

- **Early (0–6 min):** AD 60 (+11 % vs 7.2) pero growth bajado: pico early neutro. Long Sword start → componentes de Yun Tal (Noonquiver pega desde min 2). Trade pattern lvl 2-5: **Q (2 plumas) → auto ×2-3 → E con 3+ = root 1.25 s** → W y remate. El ramp de Yun Tal (125 ataques → 25 % crit) se completa farmeando (~min 8).
- **Pico 1 — Yun Tal (~6:00):** 564 DPS 1v1 / 693 3v3 a lvl 9 (AS 2.07, AD 144). Empata con Stormrazor/Kraken (±2 %) pero es el único **convergente** a la óptima sin oro muerto.
- **Pico 2 — Runaan's (~10:15) + ⬆️Gunmetal (~11:30):** 913/1 756 a lvl 12: el 3v3 casi se triplica (rayos 404×2 que critican). Spike de waveclear y siegue (placas +20/10 s en 7.3a).
- **Pico 3 — IE (~14:15) = EL spike:** 1 697/3 380 a lvl 14 (**+86 % 1v1 sobre lvl 12**): todo critica ×2.30 y **E pasa a ×1.65** (E(5) = 1 320 + root). Ventana min 14-17: de los carries más peligrosos en teamfight.
- **Pico 4 — BotRK (~17:00) + LDR (~20:15):** 2 577 → **3 146/5 929** full build. Nexus 4 000 (7.3a) garantiza que el pico llegue a importar.
- **Ruta Navori (comunidad):** gana +3.7 % 1v1 en lvl 12 y +2.9 % en lvl 14 (CDR de E) pero **−8.6 % en lvl 15 y −38 % de 3v3** en el camino (sin Runaan's) — incluso con la convención más generosa de Deft Strikes (CD×0.75, D8) se queda **−15.6 %** vs óptima ❌.
- **Lectura DUO:** Xayah **castiga engages, no los crea** (wildriftcore): posicionamiento front-to-back, R guardada para el dive. Sus picos son de teamfight estructurado → pide soporte de engage/CC lineal que meta enemigos en la alfombra: **Rakan (ideal — Lover's Leap + W compartida), Nautilus/Leona/Jarvan IV (fuerte)**. **Counters:** poke de rango antes de colocar plumas (**Jhin, Caitlyn** — Bones+Barrier+Fleet), dive doble (→ variantes GA/Scimitar), y el techo del parche en la lane: Yunara S+ / Senna S+ en dúo.
- **Dónde encaja vs el meta bot 11/10:** WR 50.10 estable, pick 4.32, ban 0.18 — **el pick A-tier que siempre está disponible** cuando Yunara (ban 22.94) y Kalista (ban 6.70) se van de la mesa; superior a Caitlyn (49.56) y Sivir (49.23) en WR y en techo de teamfight.

---

## 7. SOBREEXPLOTACIÓN — LAS 9 PALANCAS (resumen ejecutivo)

1. **Alfombra antes del engage:** Q + autos colocan 5+ plumas (6 s de vida) — pelea donde TÚ elegiste; E multi-root a todo el que pise.
2. **Root a distancia de pluma (1 000+):** E enroota donde cayeron Q/R sin acercarte — abre picks con engage aliado.
3. **R→E instantáneo (8 plumas = 1 716 + root):** la defensiva también es el mayor burst del kit; úsala al salir del intargeteable sobre el diver.
4. **W solo en ventana:** uptime 29 % — cada W en farmeo es −17.8 % de DPS en el trade siguiente.
5. **Yun Tal desde el minuto 2:** el ramp (125 ataques → 25 % crit) cuenta minions — farmea con autos, no solo con Q.
6. **Flurry (7.3a) = cap de AS por ventana:** +35 % AS/6 s → raw 3.119 → **3.0 efectivo** (+3.9 % DPS con uptime 50 %, +4.2 % al 100 % — el cap amortigua el overshoot).
7. **Los rayos de Runaan's SÍ aplican on-hit (texto oficial):** con BotRK, cada rayo añade ~132-154 → 3v3 real = **6 746-6 950** (la cifra publicada 5 929 es piso conservador sin este término, +13.8-17.2 %).
8. **Cristales desde 575:** Q/auto detona Crystalline Overgrowth (3.3-18.9 % verdadero, ~50 s) sin exponerte; torreta con W+Runaan's en ~4 autos bajo cristal.
9. **La bala LT escala con B total:** 78.5/golpe con B 3.39 = **+227 DPS solo por la runa** — cada punto de AS (ítems, Alacrity, W, Flurry) double-dipea en cadencia Y bala.

---

## 8. BUILDS — RE-VERIFICACIÓN DEL MOTOR (batch4; el reporte v2 NO se regenera)

> **Motor `model/xayah_model.py`:** port fiel de `dps_model.eval_build` (constantes del lab: LT 6×6.4 % + bala 24×(1+0.0067·B·100), Alacrity 21 %, GS, Magnification, Kraken…) + los términos manuales de §3 del reporte (E con decaimiento −10 %/pluma piso 10 %, W ×1.0714 sostenido, Q 1 daga, R 3/5, cleave 45 % AD) **integrados por primera vez en la búsqueda exhaustiva** (el optimizador del lab puntuaba solo engine de autos). Restricciones del reporte: crit = 100 exacto (Ley 1 + poda estructural), pen ≥ 30 (Ley 3), Ley 3b (1 solo `pen_pct`), ≤18 000 g.

### 8.1 Verificación de las cifras publicadas (nivel 15, LT+Alacrity full, W en ventana)

| Build | 1v1 | 3v3 | vs120 | vsTanque | heal/s | Δ vs publicado |
|---|---|---|---|---|---|---|
| **⭐ ÓPTIMA Tabla A** (Gunmetal+Yun Tal+Runaan's+BotRK+LDR+IE) | **3 146** | **5 929** | **1 767** | **1 582** | **498** | ✅ ±0.0 % |
| 🔬 top-2 (C44 por Yun Tal) | 3 144 | 5 769 | 1 766 | 1 571 | 495 | ✅ ±0.1 % |
| 🔬 top-4 glass (C44+Terminus) | 3 218 | 6 162 | 1 749 | 1 267 | 174 | ✅ ±0.0 % |
| 📌 v1 Beta (C44+Runaan's+IE+LDR+BT) | 2 819 | 5 535 | 1 584 | 1 278 | 510 | ✅ ±0.0 % |
| 🔬 análoga Jinx (C44+Kraken) | 3 063 | 5 758 | 1 721 | 1 379 | 165 | ✅ ±0.3 % |
| 🌐 comunidad (Yun Tal+Navori+IE+LDR+GA, D8 ×0.75) | 2 654 | 2 945 | 1 491 | 1 198 | 142 | ✅ ±0.3 % |
| A2 anti-burst (GA por BotRK) | 2 587 | — | — | 1 171 | — | ✅ −17.7 % (publicado −17.7 %) |
| A3 anti-heal (Mortal por LDR) | 3 146 | — | 1 710 | 1 407 | — | ✅ ±0 1v1 · −175 vsT (publicado −175) |

Desglose auditado de la óptima: **engine 2 726** (autos 2 118 + bala LT 227 + BotRK 381) **×1.0714 (W) + E 165 + Q 32 + R 28 = 3 146** · 3v3: +rayos 2 330 + cleave 287 = 5 929 · vsTanque: (3 379×1.0714 + 225)×0.4115 = 1 582 · AS 2.889 · AD 318.8 · bAD 200 · E-mult 1.65 · auto crítico 734 · rayo 404.

### 8.2 Re-optimización extendida (engine + skills en el objetivo — 27 720 hojas legales)

| # | Score | Build | 1v1 | 3v3 | vs120 | vsTanque |
|---|---|---|---|---|---|---|
| **1** | **91.1 %** | **Gunmetal + Yun Tal + Runaan's + BotRK + LDR + IE (= Tabla A publicada)** | 3 146 | 5 929 | 1 767 | 1 582 |
| 2 | 90.2 % | Gunmetal + C44 + Runaan's + BotRK + LDR + IE | 3 144 | 5 769 | 1 766 | 1 571 |
| 3 | 89.5 % | **Armorcrusher** + Yun Tal + Runaan's + BotRK + LDR + IE | 2 962 | 5 657 | **1 810** | **1 662** |
| 4 | 89.3 % | Gunmetal + Yun Tal + Runaan's + BotRK + LDR + **Stormrazor** | 3 090 | 5 788 | 1 736 | 1 549 |
| 5 | 89.2 % | Gunmetal + Yun Tal + Runaan's + C44 + **Terminus** + IE (glass) | 3 218 | 6 162 | 1 749 | 1 267 |
| 6 | 88.6 % | Gunmetal + Yun Tal + Runaan's + BotRK + **Mortal** + IE (anti-heal) | 3 146 | 5 929 | 1 710 | 1 407 |

**Conclusión:** integrar E/Q/R en el objetivo **no mueve el top-1** (E favorece IE+LDR que ya están). El reporte decía 91.6 % (objetivo engine-only) vs 91.1 % (extendido) — misma build; Armorcrusher sube de #5 a #3 con skills integrados (la pen plana rinde más en los escenarios mitigados). Control SIN Ley 1/3 (283 760 hojas): gana una build 0-pen en 1v1 crudo (+12.3 %) pero cae −9.2 % vs120 / −21.7 % vsTanque → **las restricciones del reporte quedan validadas**.

### 8.3 Sensibilidades pendientes — AHORA con números (el reporte las declaró sin publicar)

| Sensibilidad | Resultado | Veredicto |
|---|---|---|
| **D3 — BotRK 7 % oficial** (engine trae 6 %) | 1v1 **3 214** (+2.2 %) · vsTanque **1 640** (+3.6 %) | Build sin cambio. El reporte predijo "3 210 / 1 712": el 1v1 cuadra; su +130 vsTanque era **pre-mitigación** (mitigado = +58 → 1 640; nueva nota D11). Pendiente del autor: `dps_model.ITEMS["botrk"]` 6→7 (triage Δ<2 % = ✅ ANOTAR) |
| **D1 — AS growth 0.03** (vs 0.034) | 1v1 3 105 (−1.3 %) | Rankings sin cambio ✅ (coincide con el reporte) |
| **D7 — W fuera de ventana** | 1v1 2 587 (**−17.8 % total**; el −13.3 % publicado era solo engine) | La W es ~1 de cada 6 DPS: no la gastes farmeando |
| **Flurry de Yun Tal** (no modelado en v2) | +3.9 % (uptime 50 %) / +4.2 % (100 %) · AS raw 3.00-3.12 → **cap 3.0** | Upside real pero acotado por el tope — no cambia nada |
| **Rayos con on-hit** (texto oficial) | 3v3 **6 746** (+13.8 %) con BotRK 6 % · **6 950** (+17.2 %) con 7 % | Confirma la predicción del reporte (~6 700) |
| **TECHO 7.3a** (7 % + Flurry 50 % + rayos on-hit) | **1v1 3 338 (+6.1 %) · 3v3 7 207 (+21.6 %) · vs120 1 875 · vsT 1 703 (+7.6 %)** | Las cifras publicadas son el **piso conservador**; la build es la misma |
| **D8 — Navori ×0.75** | Comunidad 2 587→2 654 (+2.6 %) — sigue **−15.6 %** vs óptima | Rechazo confirmado |

### 8.4 Tabla A/B publicada — confirmada (no se re-deriva; regla de oro v1.6)

**Build final (6 slots, `validate_slots()` PASS):** Berserker's → ⬆️ **Gunmetal Greaves** (2 200) + **Yun Tal Wildarrows** (3 100) + **Runaan's Hurricane** (2 650) + **Infinity Edge** (3 400) + **Blade of the Ruined King** (3 100) + **Lord Dominik's Regards** (3 300) = **17 750 g** (18 250 acum. con start) · AD 319 · AS 2.89 · crit 100 exacto · pen 35 · LS 17 %.
**Ruta:** Long Sword (0:00) → Yun Tal (~6:00) → Berserker's (~7:30) → Runaan's (~10:15) → ⬆️ Gunmetal (~11:30, MISMO slot) → IE (~14:15) → BotRK (~17:00) → LDR (~20:15).
**Runas:** Lethal Tempo × Legend: Alacrity (baseline #1 del buscador; Conqueror −9.2 %, sin LT −16.3 %) · Brutal (+49 DPS) · Cut Down (default) / Coup de Grace (sinergia E-ejecutor) · Gathering Storm (default) / Bone Plating (vs poke) · **Flash+Heal** (Barrier vs burst, Exhaust vs dive) · Skills **Q→E→W** (R 5/9/13; Q→W→E = +0.9 % sostenido pero −8 % burst de E).

### 8.5 Matriz situacional (Δ medidos sobre 3 146/5 929/1 767/1 582)

| Situación | Cambio | Coste | Qué compras |
|---|---|---|---|
| Vs burst AD/asesinos (Zed, Rengar) | BotRK → **Guardian Angel** | −558 (−17.7 %) · vsT 1 171 | Revivir (180 s) + 40 arm |
| Vs CC en cadena + AP | BotRK → **Mercurial Scimitar** | −558 (−17.7 %) | QSS + 40 MR + 12 % LS |
| Vs poke sostenido | BotRK → **Immortal Shieldbow** | −487 (−15.5 %) | Lifeline 300-550 |
| Vs curación (Soraka/Yuumi/Mundo/Sylas) | LDR → **Mortal Reminder** | −0 1v1 · −57 vs120 · −175 vsT (1 407) | GW 50 % · Ley 3b: nunca con LDR |
| Vs CC de botas / dive | Gunmetal → **Chainlaced / Armored Advance** | −355 (−11.3 %) c/u | Tenacidad+escudo mágico / armadura+escudo físico |
| Vs 4 squishies (60-120 arm) | Gunmetal → **Armorcrusher** | −184 1v1 · **+43 vs120 · +80 vsT** (optimizador extendido #3: 89.5 %) | Pen plana 12+6 % + 25 AD |
| 0 tanques, duelo/splitpush | Runaan's+LDR → **Terminus+C44** (glass) | +72 1v1 (+2.3 %) · +233 3v3 · **−315 vsT (−19.9 %)** | Máximo DPS crudo (1v1 3 218); heal cae a 174 |

---

## 9. DISCREPANCIAS REGISTRADAS (protocolo lab §D — D1-D10 heredadas del reporte v2 + nuevas de esta re-verificación)

| # | Tema | Resolución |
|---|---|---|
| D1 | AS growth: apéndice 0.034 vs sección XAYAH 0.03 | **0.034** (display in-game 0.022 = 0.658×0.034 lo corrobora). Sensibilidad re-corrida: −1.3 %, rankings iguales ✅ |
| D2 | Ficha wr-meta con W/E de 7.2 (45-60 %, 90 % bAD) | Mandan notas 7.3 (W 40-55 %, E ×mult-crítico) |
| D3 | BotRK: engine 6 % vs nota oficial 7 % | Publicado al 6 % (piso). **Re-verificado al 7 %: 1v1 3 214 / vsT 1 640 — build sin cambio**; actualización de `dps_model.ITEMS` sigue pendiente del autor |
| D4 | Decaimiento de E (−10 %/pluma, piso 10 %) | De wiki oficial; verificado: E(3/5/8/15) = 891/1 320/1 716/1 980 ✅ |
| D5 | AD "348" de la v1 Beta | Error aritmético corregido en v2 (358.8); re-verificado: 318.8 en la óptima |
| D6 | Yun Tal ramp (0→25 % crit en 125 ataques) | Engine cuenta 25 % pleno (válido desde ~min 8-9; −3.5 % transitorio) |
| D7 | Uptime de W | Convención engine (W en ventana ×1.0714 + 0.55 en B). Sensibilidad total re-corrida: **sin W = −17.8 %** (el −13.3 % publicado era solo engine) |
| D8 | Navori Deft Strikes (mecánica sin verificar) | Convención ×0.75; re-verificado: comunidad sigue −15.6 % ❌ |
| D9 | WR/ban de fuentes (49.87-50.17; ban 1.83 errata vs 0.17-0.19 real) | Vigía 11/10 canónico: **50.10 / 4.32 / 0.18 (↑3, Med)** |
| D10 | HP/arm/MR/rango "estimados" en v1 | Oficiales desde ficha 08/10 + wiki: 630(120)/40(4)/30(1.4)/575 |
| **D11 (nueva)** | El reporte predijo BotRK 7 % → "vsTanque 1 712 (+130)" | El +130 es **pre-mitigación**; con la convención del propio lab (mit ×0.4115 + W), el correcto es **+58 → 1 640**. El 1v1 predicho (3 210) tampoco aplica el ×1.0714 de W al delta (correcto: **3 214**). Δ < 0.3 % del total: no afecta nada, queda anotado |
| **D12 (nueva)** | Supuesto de checkpoints: el reporte declara "self_as_buff 0.55 constante" pero sus cifras (565/901/1 719) solo se reproducen con el **rank real de W por nivel** (0.40/0.45/0.50) | Mi curva con ranks reales: **564/913/1 697** (±1.3 % de lo publicado). Nuance de documentación; la curva y el orden de ruta no cambian |
| **D13 (nueva)** | Score del optimizador: 91.6 % (engine-only, reporte) vs **91.1 %** (objetivo extendido con E/Q/R/cleave) | Mismo top-1; Armorcrusher sube #5→#3 al integrar skills en escenarios mitigados. Diferencia esperada por cambio de objetivo, registrada para futuras regeneraciones |

---

## Pie de página
Fuentes: WR-LAB completo v1.15 (reporte publicado `xayah` v2 engine 08-09/10/2026 con bloque WRLAB-VERIF AL_DIA 7.3a + FRAMEWORK/Leyes + `dps_model.py`/`champspecs.py`/`optimize_build.py`/`optimize_runes.py` + notas oficiales 7.3/7.3a + apéndice AS + items_7.3.csv + win rates vigía 11/10 + wiki oficial WR:Xayah 09/10 + wildriftcore 09/10) · motor de re-verificación `model/xayah_model.py` (batch4) con resultados completos en `model/xayah_resultados.txt` (6 builds de referencia reproducidas ±0.3 % · 27 720 hojas con restricciones + 283 760 sin ellas · 7 sensibilidades · curva de poder lvl 9-15). **Veredicto global: ✅ build publicada CONFIRMADA (Δ 0 %) con techo 7.3a cuantificado (1v1 3 338 · 3v3 7 207).** Esta ficha no regenera el reporte publicado (regla de oro v1.6). Documento no oficial; Wild Rift es marca de Riot Games.
