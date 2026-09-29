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

<!-- WRLAB-VERIF:7.3a:START — generado por model/update_reports.py · no editar a mano -->
> [!NOTE] ✅ ANOTAR Verificación automática (29/09/2026) — **NO requiere regeneración — hotfix 7.3a**
> **Cambios directos a Diana:** ninguno en 7.3a.
> **Δ del modelo:** 0 % — ningún input del campeón/build cambió en el motor.
> **Build publicada (6 slots, Ley 0):** Spellslinger's Shoes + Dusk and Dawn + Nashor's Tooth + Rabadon's Deathcap + Zhonya's Hourglass + Cryptbloom — **sin cambios**.
> **Ítems cambiados fuera de la build final:** Death's Dance (NERF) — verificar variantes/rechazados del reporte.
> **Sistema (7.3a):** Smite burn vs monstruos: 30–198/s → **22–162/s** → Jungla early más lenta → Diana jungla: Nashor's 1.º aún más correcto; Shyvana/Volibear/Cho'Gath jungla: clear early −15-20 %
> **Nota del lab (diff 7.3a):** Smite burn −18 % → clear early más lento (refuerza Nashor's 1.º en jungla) → Anotado
> **Veredicto:** ✅ ANOTAR — build, ruta de compra y veredictos siguen vigentes; este bloque es la constancia de verificación.
<!-- WRLAB-VERIF:7.3a:END -->

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
