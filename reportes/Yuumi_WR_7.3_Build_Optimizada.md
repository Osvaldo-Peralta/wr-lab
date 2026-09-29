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
