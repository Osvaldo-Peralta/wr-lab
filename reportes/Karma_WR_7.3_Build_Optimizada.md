---
tags:
  - Support
  - Mid
  - Enchanter
  - Poke
version: 1.2
Status: Aprobado
champion: Karma
patch: "7.3+7.3a"
---
**Fecha del análisis:** 25/09/2026
**Parche:** 7.3 (21-sep-2026)
**Rol principal:** Support (secundario: Mid AP)
**Arquetipo:** Enchanter-poke con Mantra (cada 3 casts, la siguiente habilidad básica se potencia)
**Enfoque:** CC fiable y barato (Q slow cada ~3.4 s + W root ×2) para mantener **Imperial Mandate** activo: +7 % de daño de TODO el equipo sobre el marcado, mientras Censer/E amplifican al carry.

> [!NOTE]
> **Estado Meta Actual (Diamond+, 24/09/2026):**
> 
> Win Rate 49.82 % | Pick Rate 4.68 % | Ban 0.62 % | Tendencia ↓14 (🧊 cayendo) | Rol: Support. Sigue siendo funcional; la caída refleja el meta de enchanters post-7.3, no el kit.

> [!TIP]
> **Variante Mid:** ruta AP-burst completamente distinta (Spellslinger's → Luden's → Malignance → Rabadon's → Infinity Orb → Zhonya's; AP 575, Q-Mantra ~1 025). Ver §6 matriz y Apéndice B.


> [!WARNING] Hotfix 7.3a (29-sep-2026)
> Sin cambios directos a Karma. Diadem/Circlet nerfeadas (Harmonize 0.5→0.25 %): su matriz situacional queda igual (Diadem ya era niche). Build intacta.
---

## 0. RESUMEN EJECUTIVO

### Tabla A — BUILD FINAL (SUPPORT)

| Slot | Ítem | Oro | Rol en la build |
|------|------|-----|-----------------|
| 1 (botas) | **Ionian Boots → ⬆️ Crimson Lucidity** (min 10:00, MISMO slot) | 2 000 | 25 haste → Q cada 3.4 s = Mandate permanente |
| 2 | **Black Mist Scythe** (quest de support) | 500 → 0 | Slot de quest |
| 3 | **Imperial Mandate** | 2 600 | CC → marca 4 s: **+7 % daño de todo el equipo** + 60 AP + Control (20 haste en CC) |
| 4 | **Ardent Censer** | 2 400 | E/E-Mantra → +30 % AS y +25 on-hit al carry |
| 5 | **Echoes of Helia** | 2 400 | Poke de Q → curas burst al aliado |
| 6 | **Staff of Flowing Waters** (default) / Redemption / Mikael's / Locket | 2 400 | +40 AP y +15 haste al escudar |

> **Oro total: ~11 800 g** · AP 200 · Haste 75 · HSP 21 % · **E = 339 · E-Mantra = 520 (+ anillo que escuda a un 2.º aliado ≈ 1 040 efectivos)** · Mantra cada ~16 s + R instantánea · **Mandate ≈ +357 DPS de equipo** (a 6 000 de team DPS)

### Tabla B — Ruta de compra cronológica

| # | Compra | Oro acum. | Minuto típico |
|---|--------|-----------|---------------|
| 1 | **Spectral Sickle** (quest) + poción | 500 | 0:00 |
| 2 | Boots of Speed → **Ionian Boots of Lucidity** | 1 900 | ~4:00 |
| 3 | Quest completada → **Black Mist Scythe** | 1 900 | ~6:00 |
| 4 | Bandleglass Mirror + Blasting Wand → **Imperial Mandate** | 4 500 | ~9:30 |
| 5 | ⬆️ **Crimson Lucidity** (mismo slot, +1 000 g) | 5 500 | ~10:30 |
| 6 | Forbidden Idol + Aether Wisp → **Ardent Censer** | 7 900 | ~13:00 |
| 7 | Bandleglass + Kindlegem → **Echoes of Helia** | 10 300 | ~16:00 |
| 8 | Forbidden Idol + Kindlegem → **Staff of Flowing Waters** | 12 700 | ~19:00 |

### Runas · Hechizos · Habilidades

| Categoría | Elección |
|-----------|----------|
| Keystone | **Aery** (Q de campo la dispara 2 veces; E escuda) / **Guardian** (vs dive: escudo 40-165+6 % AP a 3 aliados con W×2+E) |
| Sorcery 2 | **Transcendence** (haste → más casts → más Mantras) |
| Resolve/Sorcery 3 | **Revitalize** (+5-15 % a E) o **Manaflow Band** (+300 maná) |
| 4 | **Scorch** (poke) / **Bone Plating** (lanes de burst) |
| Hechizos | **Flash + Exhaust** (support) · **Flash + Barrier** (mid, comunidad) |
| Skills | **Q → E → W** (R en 5/9/13) |

### Resultado del modelo (nivel 15, AP 200 / haste 75 / HSP 21 %)

| Métrica | Valor |
|-----------|-----|
| Escudo E / E-Mantra (+anillo) | **339 / 520 (+520)** |
| Q-Mantra total (campo+explosión) | ~590 |
| Cadencia de Mantra sostenida | ~1 cada 16 s + R |
| **Amp de equipo (Mandate)** | **+7 % al marcado ≈ +357 DPS de equipo** |
| DPS+ al carry (Censer + uptime) | +164 (sobre ADC de referencia) |

> **Titular:** Imperial Mandate sobre un objetivo permanentemente marcado (Q cada 3.4 s) es el mayor amp-de-equipo por oro del parche para un support de poke — y Karma tiene el CC más barato y fiable para sostenerlo.

---

## 1. CONTEXTO DEL CAMPEÓN EN ESTE PARCHE

### 1.1 Cambios directos a Karma (7.3)

Sin cambios de habilidades. Ficha AS nueva del apéndice (ratio 0.625 / bonus 0.2 / 0.0135 por nivel) — irrelevante para su rol.

### 1.2 Cambios sistémicos que la afectan

| Sistema | Cambio | Efecto en Karma |
|---|---|---|
| Imperial Mandate (7.3) | Rediseño: 2 600 g, 60 AP, Control (+20 haste en habilidades de CC), Command (CC → +7 % daño recibido, 4 s) | Su Q slow + W root lo mantienen ~85-100 % uptime |
| Ardent Censer (7.3) | 2 400 g, buff fijo (30 % AS + 25 on-hit) | Su E (y E-Mantra a 2 aliados) lo procea |
| Echoes of Helia (7.3) | Soul Siphon 30 % del daño → cura | Su poke constante la alimenta |
| Enchanters (7.2) | Menos haste late en toda la línea | Haste de Crimson/Transcendence vale más |

### 1.3 ¿Escala con crítico? No — escala con **AP (65 % en su E) y haste (cadencia de Mantra)**

El ratio 65 % AP de E/Mantra-E es de los más altos entre enchanters: el AP de Mandate/Censer/Echoes NO es stat muerto.

---

## 2. FICHA MATEMÁTICA (spec)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD / HP / MS | 58 / 630 / 360 | Ficha wr-meta |
| P Mantra | 3 casts → Mantra State (potencia la siguiente básica); R = Mantra instantánea | Ficha wr-meta |
| Q Inner Flame | 60-180 + 40 % AP + slow 35 %; **Mantra:** 65-290 + 50 % + campo 1.5 s (slow 42.5-50 %) que explota 40-160 + 50 % | Ficha wr-meta |
| W Focused Resolve | **Tether ×2 campeones**: 35-110 + 40 % AP y root 1-1.75 s (40-130 + 45 %); Mantra: raíces mejoradas 1.5-2.25 s | Ficha wr-meta |
| E Inspire | Escudo 60-150 + **65 % AP** + 30 % MS; **Mantra:** 120-300 + 65 % AP (decae en 4 s) + 60 % MS + **anillo que escuda al primer aliado que entra** | Ficha wr-meta |
| R Transcendent Embrace | Mantra instantánea + anillo: 170-390 + 80 % AP + **knockback al centro** + slow 35 % | Ficha wr-meta |

---

## 3. MODELO Y FÓRMULAS (valor-aliado + amp de equipo)

```
E_escudo    = (150 + 0.65×AP) × (1 + HSP/100)
E_Mantra    = (300 + 0.65×AP) × (1 + HSP/100)  ×2 objetivos vía anillo
Cadencia    = casts/s = 3 / (Σ CDs con haste)  →  Mantras/10 s = casts/10 s ÷ 3
Mandate_amp = team_DPS × 0.07 × uptime_marca        [Q cada 3.4 s → uptime ~85-100 %]
Censer      = +11.5 % DPS del carry + AS_carry × 25 on-hit
```

### Supuestos específicos

- Team DPS de referencia 6 000 para valorar Mandate (lineal: a 4 000 → +238).
- HSP de ítems solo Censer/Staff/Redemption (Mandate no da); Revitalize 5 % base.
- Uptime de Mandate 85-100 % sobre el objetivo prioritario (Q CD 3.4 s con haste 75).
- W-Mantra NO cuenta en la cadencia sostenida (se reserva para root garantizado).

---

## 4. LEYES APLICADAS A KARMA

### Ley 0 — Slots

1 botas (Crimson T3) + quest + 4 ítems. `validate_slots(["Crimson","Imperial Mandate","Censer","Echoes","Staff"])` → PASS.

### Ley 4 — Stats muertos: la defensa SÍ vale (a medias)

A diferencia de Yuumi, Karma tiene cuerpo: la posicionan en rango de Q/W. Bone Plating/Nullifying Orb y un 6.º slot defensivo (Locket/Mikael's) tienen valor real. Pero HP/armor como stats primarios siguen siendo ineficientes vs AP/haste (su E escala 65 % AP).

### Ley 5 — Eficiencia: Mandate es amp, no stats

2 600 g → +357 DPS de EQUIPO sostenido sobre el marcado (a team DPS 6 000). Ningún ítem de support da tanto por oro cuando tu team tiene 2+ fuentes de daño. Si tu team es 80 % tu ADC: Censer primero.

### Ley 6 — Timing

Mandate al ~9:30 (Bandleglass 900 temprano) = la primera fight de dragón ya tiene marca. Crimson Lucidity al 10:30 → Q cada 3.4 s.

### Ley 7 — Sistemas

Torretas 7 000 HP: tu Q-Mantra de campo (slow 50 %) siega placas con el carry sin riesgo. Cristales: los detona tu auto/Q desde 550+. Minions al 60 % → lane de poke segura.

---

## 5. ANÁLISIS DEL PRIMER ÍTEM

**No aplica** — quest primero. La decisión real es el ítem 3: **Mandate** (team con 2+ carries) vs **Censer** (ADC-céntrico) vs **Echoes** (lane de poke/sustain). Regla del §4 Ley 5.

---

## 6. BUILD FINAL RANURA POR RANURA

| Slot | Ítem | Justificación matemática |
|---|---|---|
| Botas | **Ionian → ⬆️ Crimson Lucidity** | 25 haste + Noxian Haste (MS al escudar/hechizar) → Q cada 3.4 s = Mandate permanente |
| Quest | **Black Mist Scythe** | Obligatoria; ocupa slot |
| 1 | **Imperial Mandate** | +7 % team al marcado ≈ +357 DPS de equipo; 60 AP infla E; Control = +20 haste a su CC |
| 2 | **Ardent Censer** | E/E-Mantra (2 aliados con anillo) → +30 % AS y +25 on-hit al carry: +164 DPS |
| 3 | **Echoes of Helia** | Poke Q-Mantra (~590) → Soul Siphon cura ~177 al aliado |
| 4 | **Staff of Flowing Waters** | +40 AP/+15 haste al carry escudado; cierra haste 75+ |

### Matriz del último slot (situacional)

| Situación | Ítem | Coste | Impacto |
|---|---|---|---|
| **Default** | **Staff of Flowing Waters** | 2 400 | AP+haste al carry |
| Necesitan cura AoE | Redemption | 2 450 | 150-350 + verdadero |
| CC duro sobre el carry | Mikael's Blessing | 2 500 | Cleanse + heal |
| AoE burst enemigo | Locket | 2 600 | 250-370 AoE |
| Comp de engage aliada | Shurelya's / Zeke's | 2 500/2 400 | MS AoE / R→slow+ult haste |
| **Mid AP** | Ver Apéndice B (Luden's/Malignance/Rabadon's/Orb/Zhonya's) | ~17 500 | AP 575 · Q-Mantra ~1 025 · E-Mantra auto-escudo 707 |

### RECHAZADOS (con motivo numérico)

| Ítem | Motivo del rechazo |
|---|---|
| Yordle Trap | Aura 20 % AS a aliados < Mandate (+7 % a todo el daño) con su CC uptime |
| Diadem of Songs | Su poke ya cura vía Echoes; Diadem rinde en asedios largos (⚠️ niche) |
| Ítems de vida puros (Heartsteel etc.) | Ley 4: su E escala AP, no HP |
| Rabadon's en support | 3 400 g fuera del presupuesto de support (~12 k); solo en variante mid |

---

## 7. RUNAS · HECHIZOS · HABILIDADES

### Keystone: Aery

Q de campo dispara Aery 2 veces (impacto + explosión) y E la convierte en escudo — poke y protección en una runa.

**Alternativas:** *Guardian* vs dive pesado (escudo a 3 aliados: W×2 + E); *Arcane Comet* en la variante mid.

### Secundarias

| Slot | Runa | Valor estimado |
|---|---|---|
| Sorcery | **Transcendence** | +10 haste y reducción post-9 → más Mantras (cada 3 casts) |
| Resolve/Sorcery | **Revitalize** (+5-15 % a E) / **Manaflow Band** (+300 maná) / **Scorch** (poke) | según lane |
| Resolve | **Bone Plating** | vs lanes de burst (Draven/Yasuo) |

### Hechizos

**Support: Flash + Exhaust** (peel con W root + Exhaust = el diveador muere). **Mid: Flash + Barrier** (comunidad).

### Orden de habilidades

**Q → E → W** · R en 5/9/13.
- Q max: 180+40 % (Mantra 290+50 % + campo 160+50 %) — poke y marca de Mandate.
- E segunda: 150+65 % AP (Mantra 300+65 % + anillo) — su identidad de enchanter.
- W última: el root mejora poco (1→1.75 s) y su valor es binario (conecta o no).

---

## 8. COMPARACIÓN CONTRA LAS ALTERNATIVAS

### Tabla maestra (support, nivel 15)

| Build | Oro | AP | Haste | E | E-Mantra | Valor de equipo |
|---|---|---|---|---|---|---|
| **KS-Mandate (propuesta)** | 12 700 | 200 | 75 | 339 | 520 + anillo | **+357 amp** + 164 ADC |
| KS-Enchanter (Censer, Echoes, Staff, Redemption) | 11 650 | 180 | 65 | 344 | 538 | +164 ADC + Redemption AoE |
| KS-Anti-dive (Mikael's, Locket, Censer, Echoes) | 11 900 | 90 | 50 | ~290 | ~455 | Cleanse + escudo AoE |
| Comunidad Mid (Luden's, Malignance, Orb, Rabadon's, Zhonya's) | 17 500 | 575 | 25 | — | 707 (auto) | Q-Mantra ~1 025 burst |

### Lectura

KS-Mandate ≈ KS-Enchanter en escudos (±20) pero gana por goleada en amp de equipo cuando hay 2+ carries (tu caso: Kalista/Jinx + Diana/Cho'Gath). Con ADC como 80 % del daño del team → KS-Enchanter (Censer primero). La variante mid es otro juego: burst de poke, no enchanter.

---

## 9. PLAN DE JUEGO

### Early (0:00 – 6:00)

- **Lvl 1-2:** Q + auto (Aery+Scorch) — Karma gana casi todo lvl 1; con Mandate comprado temprano (Bandleglass 900) el primer poke YA marca.
- **Mantra de lane:** gástalo en Q (trade) o E (all-in enemigo) — nunca en W salvo root garantizado.

### Mid (6:00 – 14:00)

- **Pico Mandate + Crimson (~10:30):** Q cada 3.4 s mantiene 1 objetivo permanentemente marcado (+7 %) — **comunica focus** a tu team.
- **Min 10:00:** ⬆️ Crimson Lucidity.
- **Dragón/herald:** E-Mantra al jungla antes del fight; W-Mantra (root 2.25 s a 2 objetivos) es tu CC de compromiso.

### Late (14:00+)

- **Teamfight:** E-Mantra al iniciador (Malphite/Cho'Gath entran con 520+anillo), W al carry enemigo, **R cuando agrupen** → knockback al centro = setup de Diana R / Malphite R / Cho'Gath W.
- **Wombo oficial del grupo:** R de Karma agrupa → R de Diana/Malphite encima → Mandate marca al sobreviviente → el team lo borra (+7 %).

### Sinergia con tu grupo

| Compañero | Sinergia |
|---|---|
| **Kalista** | ⭐ Oathsworn: Karma autoataca (proca su W 19 % vida máx), su R te lanza con knockup → engage doble |
| Diana / Malphite / Cho'Gath | R agrupa → ults encima; Mandate amplifica el follow-up |
| Jinx / Yunara | Censer + marca = las dos ventanas de limpieza |
| Yuumi | No compitan: una sola enchanter; si ambas, Yuumi BF = la Kalista |

### Reglas del parche que cambian el macro

| Regla | Impacto |
|---|---|
| Torretas 7 000 HP | Q-Mantra de campo siega placas con slow 50 % |
| Enchanters con menos haste late (7.2) | Crimson + Transcendence no son lujo, son core |
| Minions 60 % | Puedes pokear delante de la wave sin miedo |

---

## 10. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS

### Fuentes primarias (mandan)

| Fuente | Acceso | Qué aporta |
|---|---|---|
| Notas oficiales 7.3 | 25/09/2026 | Rediseño de Imperial Mandate (60 AP, Control, Command +7 %), Ardent Censer 2 400, Echoes of Helia |
| Notas oficiales 7.2 | 25/09/2026 | Ajuste de haste de enchanters, items de support |

### Fuentes secundarias

| Fuente | Acceso | Fiabilidad |
|---|---|---|
| wr-meta Karma (ficha + builds + runas) | 25/09/2026 | Alta para kit (W tether ×2 confirmado); build popular = variante MID (Luden's/Malignance) — la de support es derivación propia del modelo |

### Discrepancias detectadas y resolución

| Tema | Resolución |
|---|---|
| Comunidad muestra Karma MID (AP burst), no support | Ambas rutas documentadas: §6 matriz + Apéndice B |
| Tendencia ↓14 del meta | Reportada con honestidad (§Contexto): el kit funciona, el meta de enchanters cayó |

### Supuestos del modelo (declarados)

- Team DPS 6 000 de referencia para Mandate (+7 % → +357; escala lineal).
- Uptime de marca 85-100 % (Q 3.4 s, marca 4 s).
- Carry de referencia AS 2.6/330 por golpe para Censer (+164).
- HSP solo de Censer/Staff/Redemption + Revitalize 5 %; anillo de E-Mantra cuenta como 2.º escudo completo (entra 1 aliado).

### Contexto meta (24/09, Diamond+)

Karma support: WR 49.82 %, pick 4.68 %, ban 0.62 %, tendencia ↓14. Muestra de 3-4 días post-parche; el rol de enchanter se está recolocando tras 7.3.

### Validación del modelo

- `validate_slots(["Crimson","Mandate","Censer","Echoes","Staff"])` → **PASS**.
- Chequeo manual: E = (150+0.65×200)×1.21 = **339** ✓ · E-Mantra = (300+130)×1.21 = **520** ✓.

---

## APÉNDICE A — POOL DE ÍTEMES: veredicto para Karma support

| Ítem (oro) | Veredicto | Nota |
|---|---|---|
| Imperial Mandate (2 600) | ✅ Core 1 (team con 2+ daño) | +7 % team amp permanente |
| Ardent Censer (2 400) | ✅ Core (ADC-céntrico) | E-Mantra a 2 aliados = doble proc |
| Echoes of Helia (2 400) | ✅ Core 3 | Poke → cura |
| Crimson Lucidity (2 000) | ✅ Botas | Q cada 3.4 s |
| Staff of Flowing Waters (2 400) | ✅ 6.º default | AP+haste al carry |
| Redemption / Mikael's / Locket / Shurelya's / Zeke's | ⚠️ 6.º situacional | Ver matriz §6 |
| Yordle Trap (2 400) | ❌ | Aura < Mandate |
| Diadem of Songs (2 400) | ⚠️ | Solo asedios largos |
| Defensivos de HP puro | ❌ | Su E escala AP |

---

## APÉNDICE B — RUTAS DE COMPRA

```
SUPPORT MANDATE (default con 2+ carries):
Sickle → Ionian (4') → Scythe (6') → Mandate (9:30) → ⬆️ Crimson (10:30)
→ Censer (13') → Echoes (16') → Staff (19')

SUPPORT ADC-CÉNTRICO (tu ADC es el 80 % del team):
Sickle → Ionian → Scythe → Censer (9:30) → ⬆️ Crimson → Mandate → Echoes → Staff/Redemption

SUPPORT ANTI-DIVE:
Sickle → Ionian → Scythe → Mikael's → ⬆️ Crimson → Censer → Echoes → Locket

MID AP BURST (comunidad):
Tome → Boots of Mana → Luden's (8') → Malignance (11') → ⬆️ Spellslinger's (12')
→ Rabadon's (15') → Infinity Orb (17:30) → Zhonya's (20')
(vs MR stacking: Orb → Cryptbloom/Void Staff)
```

---

## Pie de página

*Reporte generado el 25/09/2026 con datos del parche 7.3 (21/09/2026). WR-LAB v1.4. Las métricas de valor-aliado y amp de equipo son comparativas — el valor absoluto importa menos que las diferencias relativas entre builds, que son robustas a los supuestos. Si Riot publica un 7.3a/b (hotfix), regenerar datos antes de publicar.*

**Referencias y créditos**

- Notas oficiales del parche 7.3 (21/09/2026) y 7.2 (08/07/2026) — © Riot Games, Inc. (wildrift.leagueoflegends.com). Fuente primaria: rediseño de Imperial Mandate, Ardent Censer, Echoes of Helia y ajustes de enchanters.
- Base de datos de ítems, runas y ficha de campeón — wr-meta.com (proyecto comunitario de JLVD DEV), sincronizada al 24/09/2026. Fuente secundaria: kit completo (W tether ×2), build/runas populares de mid y meta.
- Modelo matemático (valor-aliado + amp), Leyes 0-7 y validaciones — WR-LAB (laboratorio propio, `model/analysis_batch2.py`), construido sobre las fuentes anteriores.

**Aviso legal:** Wild Rift y League of Legends son marcas registradas de Riot Games, Inc. Este documento es una guía de comunidad con fines educativos, **no está afiliado, patrocinado ni respaldado por Riot Games**. Los nombres de ítems, campeones y estadísticas pertenecen a sus respectivos dueños. El análisis y las conclusiones son trabajo original del autor apoyado en WR-LAB.

---
