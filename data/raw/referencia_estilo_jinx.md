---
tags:
  - ADC
version: 1.2
Status: Aprobado
---
**Fecha del análisis:** 27/09/2026
**Parche:** 7.3 (21-sep-2026)
**Rol principal:** Jungla / Top Lane  (dato de ejemplo)
**Arquetipo:** Fighter Híbrido (On-Hit + AP Burst) con escalamiento de Velocidad de Ataque (dato de ejemplo)
**Enfoque:** Maximización de escalado infinito mediante _Feast_ (R) y _Heartsteel_, convirtiendo el tamaño en daño verdadero (% vida) y durabilidad extrema para Jungla (datos de ejemplo).

> [!NOTE] (Datos de ejemplo)
> **Estado Meta Actual (Diamond+):**
> 
> Win Rate ~51% | Pick Rate Alto | Rol: ADC Bot Lane / Duo Support.

Y/O por el contrario si es una build personalizada para un escenario, como Yuumi agresiva (donde maximizamos su daño sacrificando escudo/curación o Cho'Gath donde priorizamos su escalado de tamaño junto a su daño + resistencia)

> [!DANGER] (Datos de ejemplo)
> **Advertencia:** Esta build sacrifica ~15-20% de escudo puro (E) a cambio de ~40% más de daño en Q y utilidad de equipo por daño infligido.

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
(Agregar un pie de pagina con incluso agregando disclaimers, derechos de autor y referencias me parece bien, porque esta información biene de alguien y de algun lugar)

*Reporte generado el 27/09/2026 con datos del parche 7.3 (21/09/2026). WR-LAB v1.2. Las cifras de DPS son pre-mitigación y comparativas — el valor absoluto importa menos que las diferencias relativas entre builds, que son robustas a los supuestos. Si Riot publica un 7.3a/b (hotfix), regenerar datos antes de publicar.*

---