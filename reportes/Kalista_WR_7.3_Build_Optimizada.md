---
tags:
  - ADC
  - Marksman
  - On-hit
  - Bot-Lane
version: 1.2
Status: Aprobado
champion: Kalista
patch: "7.3+7.3a"
---
**Fecha del análisis:** 25/09/2026
**Parche:** 7.3 (21-sep-2026)
**Rol principal:** ADC (Dragon Lane)
**Arquetipo:** On-hit ejecutor — autos que apilan lanzas y una E (Rend) que detona en burst físico
**Enfoque:** Maximizar aplicaciones on-hit por segundo (Guinsoo's las duplica cada 3 golpes) y lanzas por ventana de E; penetración doble con Terminus; **cero crítico** (su E no critica).

<!-- WRLAB-VERIF:7.3a:START — generado por model/update_reports.py · no editar a mano -->
> [!NOTE] ✅ ANOTAR Verificación automática (29/09/2026) — **NO requiere regeneración — hotfix 7.3a**
> **Cambios directos a Kalista:** ninguno en 7.3a.
> **Δ del modelo:** 0 % — ningún input del campeón/build cambió en el motor.
> **Build publicada (6 slots, Ley 0):** Gunmetal Greaves + Guinsoo's Rageblade + Wit's End + Terminus + Blade of the Ruined King + Runaan's Hurricane — **sin cambios**.
> **Ítems cambiados fuera de la build final:** Yun Tal Wildarrows (BUFF) — verificar variantes/rechazados del reporte.
> **Sistema (7.3a):** Nexus: 5 500 → **4 000 HP** → Partidas terminan antes tras inhibidores
> **Sistema (7.3a):** Placas de torreta: Al perder placa: +30→**+20** arm/MR y 20→**10 s** → **Siege más fácil** → sube el valor de Jinx/Kalista/Yunara (siege) y de Runaan's/Energized
> **Nota del lab (diff 7.3a):** Yun Tal buffeada sigue RECHAZADA para Kalista (sin on-hit, ramp de crit); para **Yunara** (reporte externo) es buff relevante → re-verificar ese reporte → Anotado
> **Veredicto:** ✅ ANOTAR — build, ruta de compra y veredictos siguen vigentes; este bloque es la constancia de verificación.
<!-- WRLAB-VERIF:7.3a:END -->

> [!NOTE]
> **Estado Meta Actual (Diamond+, 24/09/2026):**
> 
> Win Rate 50.99 % dúo (51.27 % solo) | Pick Rate 4.72 % | Ban 5.02 % | Tendencia ↑7 | Rol: ADC Bot Lane.

> [!TIP]
> **Variante duelo/splitpush:** cambia Runaan's por **Kraken Slayer** → **1 364 DPS 1v1** (el máximo medido) a costa de todo el AoE (3v3 cae a 1 364). **Variante waveclear:** Statikk Shiv como ítem 2-3 (sus bounces aplican on-hit y Kalista carga Energized 5× más rápido); se vende tarde por BotRK.

> [!WARNING]
> Rango de ataque no publicado en la fuente (verificar en juego). No afecta conclusiones: ninguna pasiva de esta build exige ≥550 de distancia.


> [!WARNING] Hotfix 7.3a (29-sep-2026)
> Sin cambios directos a Kalista. Yun Tal Wildarrows fue BUFFEADA (AS 25→35 %, Flurry 35 %) pero **sigue rechazada** para ella (sin on-hit, ramp de crit). Placas más blandas favorecen su siege. Build y números intactos.
---

## 0. RESUMEN EJECUTIVO

### Tabla A — BUILD FINAL

| Slot | Ítem | Oro | Rol en la build |
|------|------|-----|-----------------|
| 1 (botas) | **Berserker's Greaves → ⬆️ Gunmetal Greaves** (min 10:00, MISMO slot) | 2 200 | 50 % AS + 5 % LS + 12 HP/golpe + dash mejorado (su pasiva escala con tier de botas) |
| 2 | **Guinsoo's Rageblade** | 3 000 | 35 AD/30 AP/30 % AS · doble on-hit cada 3 golpes · +32 % AS por stacks |
| 3 | **Wit's End** | 2 800 | 50 % AS + 40 mágico/golpe + 45 MR + 20 % tenacidad |
| 4 | **Terminus** | 3 000 | 30 % pen física Y mágica (3 stacks) + 30 on-hit + 35 % AS |
| 5 | **Blade of the Ruined King** | 3 100 | 6 % vida actual/golpe + 12 % LS + Drain slow |
| 6 | **Runaan's Hurricane** | 2 650 | 2 rayos que aplican on-hit COMPLETO a 2 objetivos extra |

> **Oro total: 16 750 g** · AD 240 · AS 3.00 (cruda 3.52 con stacks) · Crit 0 % · Pen 30 % doble · LS 17 %

### Tabla B — Ruta de compra cronológica

| # | Compra | Oro acum. | Minuto típico |
|---|--------|-----------|---------------|
| 1 | Long Sword + poción (start; se vende/absorbe) | 500 | 0:00 |
| 2 | Amplifying Tome + Recurve + Pickaxe → **Guinsoo's Rageblade** | 3 000 | ~7:30–8:30 |
| 3 | **Berserker's Greaves** | 4 200 | ~9:30 |
| 4 | Recurve + Negatron + Dagger → **Wit's End** | 7 000 | ~12:00 |
| 5 | ⬆️ **Gunmetal Greaves** (mismo slot, +1 000 g) | 8 000 | ~13:00 |
| 6 | Recurve + Hearthbound Axe + 900 → **Terminus** | 11 000 | ~15:30 |
| 7 | Vampiric + Pickaxe + Recurve → **BotRK** | 14 100 | ~18:00 |
| 8 | Zeal + Kircheis → **Runaan's Hurricane** | 16 750 | ~20:30 |

### Runas · Hechizos · Habilidades

| Categoría | Elección |
|-----------|----------|
| Keystone | **Lethal Tempo** (38.4 % AS + bala ~85-90/golpe con su AS bonus ≈ +260 DPS) |
| Precisión 2 | **Legend: Alacrity** (+21 % AS → más lanzas por ventana de E) |
| Precisión 3 | **Brutal** (5 + 6 % AD bonus adaptativo/golpe) |
| Precisión 4 | **Coup de Grace** (+8 % a <40 % HP — su E ya es ejecutor) |
| Secundaria | **Nullifying Orb** (vs asesinos AP) / **Bone Plating** (vs poke) |
| Hechizos | **Flash + Heal** (Heal + BotRK + Gunmetal LS = sustain triple; Ghost si kitean) |
| Skills | **E → Q → W** (R en 5/9/13) |

### Resultado del modelo (nivel 15, LT/Alacrity full, E cada 7 s con ~AS×4 lanzas)

| Escenario | DPS (mitigado) |
|-----------|-----|
| **1v1** (vs 120 arm / 50 MR) | **1 262** |
| **3v3** (splash de on-hit por Runaan's + Statikk-like bounces) | **2 612** |
| **vs Tanque** (220 arm / 150 MR / 4 500 HP) | **1 045** |
| Detonación de E (12 lanzas, AD 240) | **2 387 por rip** |
| Heal/s (BotRK 12 % + Gunmetal 5 % + Blessed) | **~250** |

> **Titular:** +15 % 1v1, +20 % 3v3 y +35 % vs tanque sobre la build de comunidad (Statikk core); **+43 % sobre cualquier ruta de crítico** (su E no critica: el crítico es stat muerto en Kalista).

---

## 1. CONTEXTO DEL CAMPEÓN EN ESTE PARCHE

### 1.1 Cambios directos a Kalista (7.3)

| Stat / Habilidad | Antes (7.2) | Ahora (7.3) | Impacto |
|---|---|---|---|
| AD base | 54 | **57** | +3 AD base |
| AD por nivel | 5.0 | **5.2** | 129.8 AD a nivel 15 (antes ~124) |

### 1.2 Cambios sistémicos que la afectan

| Sistema | Cambio | Efecto en Kalista |
|---|---|---|
| AS cap | 2.5 → **3.0** | La campeona con más AS por nivel (0.046) estrena techo más alto |
| Lifesteal (nuevo stat) | Solo autos/on-hit | TODO su daño es on-hit/autos → 100 % efectivo (BotRK 12 % + Gunmetal 5 %) |
| Guinsoo's rehecho | 35 AD/30 AP/30 % AS, doble on-hit cada 3 golpes, sin restricción de crítico | Su ítem firma: multiplica WE/Terminus/BotRK |
| Statikk rehecho | Bounces aplican on-hit, Electroshock (+5 stacks Energized/ataque) | Waveclear brutal temprano |
| Botas T3 (min 10:00) | Gunmetal: 50 % AS + 5 % LS + Gait | Su dash (P) escala con tier de botas → doble beneficio |

### 1.3 ¿Sus habilidades escalan con crítico?

**No.** Ficha oficial sin mención de crítico en Q/E/R (a diferencia de Caitlyn/MF/Tristana que sí lo recibieron en 7.3). Sus autos pueden critar pero son fracción minoritaria de su DPS → **Ley 1 invertida: el umbral útil de crítico de Kalista es 0 %**.

---

## 2. FICHA MATEMÁTICA (spec)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base / growth | 57 / 5.2 | Notas 7.3 (buff) |
| AS base / ratio | 0.694 / 0.694 | Apéndice oficial 7.3 |
| Base Bonus AS | 0.16 | Apéndice oficial 7.3 |
| AS por nivel | **0.046** (la más alta del juego) | Apéndice oficial 7.3 |
| Rango | por verificar | [!WARNING] |
| P Martial Poise | dash por auto; velocidad/distancia escala con TIER DE BOTAS; Oathsworn | Ficha wr-meta |
| Q Pierce | 70/135/200/265 + 110 % AD; on-kill carry de stacks de Rend; habilita dash | Ficha wr-meta |
| W Sentinel (pasiva) | Con Oathsworn a <8 m y ambos golpeando al mismo objetivo: **16/17/18/19 % vida MÁXIMA** mágico extra, 8 s CD por objetivo; ejecuta minions <125 | Ficha wr-meta |
| E Rend | 30/45/60/75 + 70 % AD + (n−1) × (12/22/32/42 + 36/43/50/57 % AD); lanzas duran 4 s; slow 15-45 %; **reset con kill**; no critica | Ficha wr-meta |
| R Fate's Call | Oathsworn en stasis → lanzamiento con knockup 1/1.5/2 s | Ficha wr-meta |

**AD a nivel 15:** 57 + 5.2×14 = **129.8** · **Bonus de niveles (AS):** 0.046 × 14.0 = **+0.644**

---

## 3. MODELO Y FÓRMULAS

```
AS = min(3.0, 0.694 × (1 + 0.16 + 0.644 + AS_items + LT(0.384) + Alac(0.21) + Guinsoo_stacks(0.32)))

Auto   = AD (+ on-hit físico: BotRK 6 % vida actual)
On-hit = (Guinsoo 30 + Terminus 30 + WE 40) mágicos × 4/3 (doble aplicación Guinsoo)
       + Statikk: Energized 60 mágico cada ~4 ataques (Kalista carga 5× más rápido)
E/rip  = 75 + 0.70×AD + (AS×4 − 1) × (42 + 0.57×AD)      [cada 7 s]
Q      = (265 + 1.10×AD) cada 6.5 s (aplica 1 lanza extra)
W      = 0.19 × vida_máx Objetivo cada 8 s (condicional Oathsworn coordinado)
LT     = AS × 24 × (1 + 0.0067 × B×100)
Mitigación física para AD/E/Q/on-hit físico; mágica aparte para on-hit mágico y W.
```

### Supuestos específicos

- E cada 7 s con lanzas = AS×4 (duración 4 s, sin cap declarado); rank 4.
- W modelada con coordinación de Oathsworn al 100 % (en solo queue resta ese término).
- Terminus a 3 stacks (oscuros) ~90 % del tiempo en pelea.
- BotRK al 90 % de vida máxima promedio del objetivo; Guinsoo a 4 stacks.
- Bala de LT = adaptativa física; on-hit mágico mitigado por MR (50 squishy / 150 tanque).

---

## 4. LEYES APLICADAS A KALISTA

### Ley 0 — Slots

Build final = 1 botas (Gunmetal T3) + 5 ítems. `validate_slots(["Gunmetal","Guinsoo","Wit's End","Terminus","BotRK","Runaan's"])` → **PASS**.

### Ley 1 (invertida) — Crítico: umbral útil 0 %

| Ruta | 1v1 | 3v3 | Veredicto |
|---|---|---|---|
| On-hit (final) | **1 262** | **2 612** | ✅ |
| Crítico (Gunmetal+C44+IE+Runaan's+LDR+Kraken) | 885 | 1 416 | ❌ −30 %: su E (57 % AD por lanza) no critica |

### Ley 2 — AS: Kalista quiere TODO el tope

```
AS_items_para_cap = (3.0/0.694 − 1) − (0.16 + 0.644 + 0.384 + 0.21 + 0.32)
                  = 3.323 − 1.718 = 1.605 → ~160 % de AS de ítems (con stacks de Guinsoo)
```

| Combo | AS ítems | AS cruda | Veredicto |
|---|---|---|---|
| Gunmetal+Guinsoo+WE+Terminus+BotRK+Runaan's | 235 % | 3.52 | ⚠️ overcap teórico ~17 %, pero su uptime real de buffs (LT 6 golpes, Guinsoo 4 golpes, dash que interrumpe autos) lo deja oscilando alrededor de 3.0. **Único campeón del roster donde pasarse un poco no duele.** |
| Sin Gunmetal (Berserker's) | 220 % | 3.42 | igual de overcap pero −15 % AS permanente y −dash: estrictamente peor |

### Ley 3 — Penetración: doble, por Terminus

Mitad de su daño es mágico (on-hit) y mitad físico (autos+E). **Terminus da 30 % a AMBAS** (3 stacks oscuros). LDR fue probado: 1 074 1v1 / 768 vs tanque — **pierde contra BotRK** (25 % crit muerto + su % vida actual derriba tanques mejor que la pen contra su E).

### Ley 4 — Stats muertos

| Ítem | Stat muerto en Kalista | Oro desperdiciado |
|---|---|---|
| C44 / IE / LDR / RFC / Runaan's-crit | 25 % crit cada uno (E no critica) | ~1 250 g por ítem |
| Statikk como ítem FINAL | AD 40 + AP 40 parcialmente; Energized < on-hit sostenido | ~800 g vs BotRK |

### Ley 5 — Eficiencia: Guinsoo's es el multiplicador

Guinsoo's (3 000 g) no es caro por sus stats sino por su pasiva: **doble aplicación cada 3 golpes** multiplica WE (+40), Terminus (+30), BotRK (6 %) y el propio Wrath (+30) → ~+33 % a todo el on-hit del build. Nada en el parche replica ese multiplicador.

### Ley 6 — Timing

Guinsoo's 1.º (pico 7:30-8:30) → WE 2.º (12:00, anti-AP y máximo 1v1 temprano: 686) → Gunmetal (13:00) → Terminus → BotRK → Runaan's.

### Ley 7 — Sistemas 7.3

Su dash por auto (mejorado por botas T3) + E-reset con kill = la mecánica de "kiteo infinito" que las torretas de 7 000 HP premian: trabaja placas desde 575+ sin quedar estática; los cristales (Crystalline Overgrowth) se detonan con un auto en pleno dash.

---

## 5. ANÁLISIS DEL PRIMER ÍTEM

Checkpoint nivel 11 (2 ítems + Gunmetal, vs 90 arm / 40 MR):

| Combo | AD | AS | DPS 1v1 | DPS 3v3 | Nota |
|---|---|---|---|---|---|
| **Guinsoo's + Wit's End** | 144 | 2.79 | **686** | 686 | Máximo duelo; 45 MR anti-poke AP |
| Guinsoo's + Statikk (comunidad) | 184 | 2.65 | 658 | **772** | Waveclear y AoE temprano |
| Statikk + Runaan's | 149 | 2.50 | 483 | 805 | Solo si la partida es 5-man constante |
| C44 + Runaan's (crítico) | 164 | 2.29 | 445 | 662 | ❌ confirmado: ruta muerta |

**Veredicto:** Guinsoo's primero SIEMPRE (es el multiplicador). El 2.º ítem es la decisión real: **WE** si te hacen burst AP o buscas duelos (686), **Statikk** si necesitas push (772 en 3v3). Ambos convergen a la Tabla A.

---

## 6. BUILD FINAL RANURA POR RANURA

| Slot | Ítem | Justificación matemática |
|---|---|---|
| Botas | **Berserker's → Gunmetal** | +15 % AS sobre T2; 5 % LS; 12 HP/golpe (~36 HP/s a AS 3.0); **su dash escala con tier de botas** (ficha oficial) |
| 1 | **Guinsoo's Rageblade** (3 000) | Doble on-hit cada 3 golpes = ×4/3 a todo el on-hit; 32 % AS por stacks; 35 AD |
| 2 | **Wit's End** (2 800) | 50 % AS + 40 mágico/golpe (~120 DPS) + 45 MR + 20 % tenacidad — Kalista es el foco #1 del equipo enemigo |
| 3 | **Terminus** (3 000) | 30 % pen doble (su daño es mixto) + 30 on-hit + 35 % AS + resistencias light |
| 4 | **BotRK** (3 100) | 6 % vida actual (~132 vs 2 200 HP; ~270 vs tanque) DOBLE con Guinsoo cada 3 golpes + Drain slow + 12 % LS |
| 5 | **Runaan's Hurricane** (2 650) | Cada rayo aplica on-hit completo a 2 objetivos extra (+40 WE +30 Guinsoo +6 % HP por rayo) → su 3v3 sube de 1 262 a 2 612 |

### Matriz del último slot (situacional)

| Situación | Ítem | Coste | Impacto medido |
|---|---|---|---|
| **Default (AoE)** | **Runaan's Hurricane** | 2 650 | 2 612 en 3v3 |
| Duelo / splitpush | Kraken Slayer | 2 900 | **1 364 1v1** (+8 %), 3v3 = 1 364 |
| Waveclear temprano | Statikk Shiv | 3 000 | 772 3v3 a nivel 11; vendible tarde |
| vs 3 tanques | (mantiene BotRK+Terminus) | — | 1 045 vs tanque ya incluido |
| vs burst AP | WE sube a ítem 2 | — | 45 MR + 20 % tenacidad antes |

### RECHAZADOS (con motivo numérico)

| Ítem | Motivo del rechazo |
|---|---|
| **Ruta crítica completa** | 885 DPS = −30 %; E no critica |
| **LDR / Mortal Reminder** | 25 % crit muerto; LDR probado: 1 074/768 < BotRK 1 262/1 045 |
| **C44** | Magnification exige distancia (rango por verificar); 25 % crit muerto |
| **Statikk como ítem final** | Su Energizado rinde menos que BotRK/Runaan's sostenidos (K1 comunidad: 1 098 vs K2: 1 262) |
| **Navori / ER / Galeforce / Shieldbow** | Crit muerto + sin on-hit |
| **Guinsoo's + Statikk + Runaan's + WE + Terminus (K1 comunidad)** | Le falta el % vida de BotRK: −15 % 1v1 y −26 % vs tanque |

---

## 7. RUNAS · HECHIZOS · HABILIDADES

### Keystone: Lethal Tempo (rehecho 7.3)

- 6 cargas × 6.4 % = **38.4 % AS** — Kalista las mantiene trivialmente (ataca sin parar).
- Bala: 24 × (1 + 0.0067 × ~407 % AS bonus) = **~89 por golpe** × AS 3.0 ≈ **+260 DPS**.
- Es la keystone que más crece con exactamente lo que ella compra (AS) y con su pasiva de dash (uptime de ataques).

**Alternativas:** *Fleet Footwork* solo vs lanes de poke extremo donde no pueda mantener cargas; nada más compite.

### Secundarias

| Slot | Runa | Valor estimado |
|---|---|---|
| Precisión | **Legend: Alacrity** | +21 % AS → ~+2 lanzas por ventana de E (≈ +300 por rip) |
| Precisión/Dom | **Brutal** | 5 + 6 % AD bonus ≈ +40 DPS constante |
| Precisión | **Coup de Grace** | +8 % a <40 % HP — convierte rips de E en ejecuciones |
| Resolve/Sorcery | **Nullifying Orb** / **Bone Plating** | Anti-asesino AP / anti-poke de lane |

### Hechizos: Flash + Heal

Heal + BotRK 12 % + Gunmetal 5 % + Blessed Blade 12/golpe = triple sustain; la comunidad coincide. Ghost es válido si el enemigo kitea (su dash ya es movilidad).

### Orden de habilidades

**E → Q → W** · R en 5/9/13.
- E max primero: es SU daño (42 + 57 % AD por lanza y reset con kill).
- Q segundo: 265 + 110 % AD, on-kill carry de stacks (snowball de waveclear).
- W al final: la pasiva escala poco (16→19 %) y el activo es visión.

---

## 8. COMPARACIÓN CONTRA LAS ALTERNATIVAS

### Tabla maestra (nivel 15, LT/Alacrity full, E con ~12 lanzas)

| Build | Oro | AD | AS | Crit | Pen | 1v1 | 3v3 | vs Tanque | E-hit |
|---|---|---|---|---|---|---|---|---|---|
| **FINAL (Gun+Guinsoo+WE+Term+BotRK+Runaan's)** | 16 750 | 240 | 3.00 | 0 % | 30 | **1 262** | **2 612** | **1 045** | 2 387 |
| Comunidad K1 (Statikk en vez de BotRK) | 16 650 | 240 | 3.00 | 0 % | 30 | 1 098 | 2 181 | 776 | 2 387 |
| K3 LDR anti-tanque | 16 950 | 235 | 3.00 | 25 % | 35 | 1 074 | 2 042 | 768 | 2 349 |
| K5 Single-target (Kraken por Runaan's) | 17 000 | 285 | 3.00 | 0 % | 30 | **1 364** | 1 364 | 1 119 | 2 726 |
| K4 Crítico (descarte) | 17 350 | 340 | 2.53 | 100 % | 35 | 885 | 1 416 | 665 | 2 700 |

### Desglose multiplicativo de la diferencia (FINAL vs comunidad K1)

| Factor | Contribución |
|---|---|
| BotRK 6 % vida actual × doble-aplicación Guinsoo (vs Statikk Energized intermitente) | +15 % 1v1 |
| Rayos de Runaan's con on-hit completo ×2 objetivos (vs bounces de Statikk) | +20 % 3v3 |
| BotRK vs tanque (6 % de 4 500 HP = 270/golpe) | **+35 % vs tanque** |

---

## 9. PLAN DE JUEGO

### Early (0:00 – 9:00)

- **Start:** Long Sword + poción; componentes de Guinsoo's (Recurve 900 primero).
- **Last hits imposibles:** E rank 1 + W pasiva ejecutan minions bajo 125 HP — asegura CS bajo torre.
- **Vínculo (Oathsworn) al minuto 1:** elección definitiva de la partida (ver abajo).

### El vínculo (Oathsworn) — la decisión más importante

| Candidato | Veredicto |
|---|---|
| **Karma (support)** | ⭐ Ideal: autoataca a distancia (proca tu W 19 % vida máx), su W enraíza 2 objetivos (rips garantizados) y tu R la lanza como engage → combo R→R |
| Tanques melee (Cho'Gath/Malphite) | Sólido: siempre están encima del objetivo (W proca) y tu R los reposiciona |
| **Yuumi** | ⚠️ Attachada no autoataca → la W pasiva casi no proca. Verificar en juego si su Q cuenta como "golpe" para el vínculo; si no, vincúlate a otro |

### Mid (9:00 – 16:00)

- **Min 10:00:** ⬆️ Gunmetal Greaves — tu dash mejora literalmente (tier de botas).
- **Pico Guinsoo+WE+Gunmetal (~13 min):** 686 DPS 1v1 temprano; ganas duelos con rips de ~1 500-1 900.
- **Reset de E:** cada kill refresca Rend → en oleadas y skirmishes encadena rips; prioriza objetivos bajos para detonar el reset.

### Late (16:00+)

- **Teamfight:** pega al FRONTLINE (BotRK+Terminus+W 19 % vida máx lo derriten) mientras Runaan's propaga on-hit al backline. Nunca dejes de atacar hacia atrás (dash por auto).
- **R como herramienta de equipo:** guarda Fate's Call para el engage de tu Oathsworn (Karma/Malphite) o para salvarlo de un dive.
- **W CD por objetivo (8 s):** rota objetivos con tu support para procar la pasiva en varios enemigos.

### Reglas del parche que cambian el macro

| Regla | Impacto |
|---|---|
| Torretas 7 000 HP + placas | Tu AS alta + dash = trabaja placas segura desde 575+ |
| Cristales (~50 s) | Un auto en dash los detona (hasta ~1 300 verdadero en late) |
| Jungla hostil (7.3) | No robes campamentos: monstruos pegan % vida actual |

---

## 10. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS

### Fuentes primarias (mandan)

| Fuente | Acceso | Qué aporta |
|---|---|---|
| Notas oficiales 7.3 | 25/09/2026 | Buff de AD (57/5.2), apéndice AS (0.694/0.16/0.046), Guinsoo's/Statikk/Terminus/BotRK rehechos, lifesteal |
| Notas oficiales 7.2 | 25/09/2026 | Botas T2/T3 y regla del min 10:00 |

### Fuentes secundarias

| Fuente | Acceso | Fiabilidad |
|---|---|---|
| wr-meta Kalista (ficha + build popular) | 25/09/2026 | Alta para kit (Q/W/E/R completos); build popular = insumo (Statikk 1.º) |

### Discrepancias detectadas y resolución

| Tema | Resolución |
|---|---|
| 1.º ítem: comunidad Statikk vs modelo Guinsoo→WE | Gana el modelo (686 vs 658 1v1; 1 262 vs 1 098 final) — Statikk queda como variante waveclear |
| Lethal Tempo (valores) | Notas oficiales 7.3 (6.4 %, bala 6-24, +0.67 %) sobre texto viejo de wr-meta |

### Supuestos del modelo (declarados)

- E no critica (sin mención en ficha — si un hotfix lo cambia, recalcular).
- ¿Cuenta el Q de Yuumi como golpe del Oathsworn para W? **Pendiente de verificar en juego.**
- Lanzas por ventana = AS×4 (4 s de duración, sin cap declarado).
- Terminus 3 stacks ~90 % uptime; Guinsoo 4 stacks; BotRK al 90 % vida máx.
- Mitigación física y mágica aplicadas por separado a cada componente.

### Contexto meta (24/09, Diamond+)

Kalista: WR 50.99 % dúo / 51.27 % solo, pick 4.72 %, ban 5.02 %, **tendencia ↑7** — el 7.3 (buff de AD + AS cap 3.0 + Guinsoo's) la dejó en buen lugar. Muestra de 3-4 días post-parche.

### Validación del modelo

- `validate_slots(["Gunmetal","Guinsoo","Wit's End","Terminus","BotRK","Runaan's"])` → **PASS** (6 entradas, 1 botas, sin T2+T3).
- Test de Caitlyn (AS 1.48125): motor reproduce ✓.

---

## APÉNDICE A — POOL DE ÍTEMES DEL ROL: veredicto para Kalista

| Ítem (oro) | Veredicto | Nota |
|---|---|---|
| Guinsoo's Rageblade (3 000) | ✅ Core 1 | El multiplicador (doble on-hit ×4/3) |
| Wit's End (2 800) | ✅ Core 2 | 50 % AS + 40 on-hit + 45 MR |
| Terminus (3 000) | ✅ Core 3 | Única pen DOBLE del juego (física+mágica) |
| Blade of the Ruined King (3 100) | ✅ Core 4 | 6 % vida actual ×2 con Guinsoo; anti-tanque real |
| Runaan's Hurricane (2 650) | ✅ Core 5 | Rayos con on-hit completo = su AoE |
| Gunmetal Greaves (2 200) | ✅ Botas | AS + LS + dash mejorado |
| Statikk Shiv (3 000) | ⚠️ Early/waveclear | Bounces con on-hit; vendible por BotRK tarde |
| Kraken Slayer (2 900) | ⚠️ 6.º duelo | 1 364 1v1 (máximo), pierde AoE |
| LDR / Mortal (3 300/3 000) | ❌ | 25 % crit muerto; BotRK > pen en ella |
| C44 / IE / RFC / PD / Navori / ER / Gale / Shieldbow / Collector | ❌ | Crítico muerto (E no critica) |
| Manamune / Trinity / Hexplate | ❌ | Stats de fighter/caster |

---

## APÉNDICE B — RUTAS DE COMPRA

```
DEFAULT (on-hit completo):
LS → Guinsoo's (7:30-8:30) → Berserker's (9:30) → Wit's End (12:00)
→ ⬆️ Gunmetal (13:00) → Terminus (15:30) → BotRK (18:00) → Runaan's (20:30)

WAVECLEAR / PUSH TEMPRANO:
LS → Guinsoo's → Berserker's → Statikk (11:30) → ⬆️ Gunmetal → Terminus → BotRK → (vender Statikk → Runaan's)

ANTI-AP BURST:
Guinsoo's → Berserker's → Wit's End (2.º, ya en default) → Mercury's→Chainlaced SOLO si el CC es inmanejable (pierdes 50 % AS y el dash T3)

DUELO / SPLITPUSH:
Default pero 6.º = Kraken Slayer (1 364 1v1)

VS 3 TANQUES:
Default intacto (BotRK+Terminus+W ya ES la respuesta: 1 045 vs tanque)
```

---

## Pie de página

*Reporte generado el 25/09/2026 con datos del parche 7.3 (21/09/2026). WR-LAB v1.4. Las cifras de DPS son mitigadas contra los objetivos estándar declarados (120/50 squishy · 220/150/4 500 tanque) y comparativas — el valor absoluto importa menos que las diferencias relativas entre builds, que son robustas a los supuestos. Si Riot publica un 7.3a/b (hotfix), regenerar datos antes de publicar.*

**Referencias y créditos**

- Notas oficiales del parche 7.3 (21/09/2026) y 7.2 (08/07/2026) — © Riot Games, Inc. (wildrift.leagueoflegends.com). Fuente primaria: buff de Kalista, apéndice de Attack Speed, rehechos de Guinsoo's/Statikk/Terminus/BotRK, sistema de botas T3 y lifesteal.
- Base de datos de ítems, runas y ficha de campeón — wr-meta.com (proyecto comunitario de JLVD DEV), sincronizada al 24/09/2026. Fuente secundaria: valores de Q/W/E/R, build y meta.
- Modelo matemático, Leyes 0-7 y validaciones — WR-LAB (laboratorio propio, `model/analysis_batch2.py` motor on-hit), construido sobre las fuentes anteriores.

**Aviso legal:** Wild Rift y League of Legends son marcas registradas de Riot Games, Inc. Este documento es una guía de comunidad con fines educativos, **no está afiliado, patrocinado ni respaldado por Riot Games**. Los nombres de ítems, campeones y estadísticas pertenecen a sus respectivos dueños. El análisis y las conclusiones son trabajo original del autor apoyado en WR-LAB.

---
