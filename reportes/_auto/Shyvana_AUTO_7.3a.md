---
tags:
  - Jungla
  - Auto
version: 0.9
Status: Espera de verificación
champion: Shyvana
slug: shyvana-auto-73a
role: jungla
variant: auto-7-3a
patch: "7.3a"
archetype: "Q Twin Bite: doble golpe (100% + 20/40/60/80% AD) y los auto"
engine: autos
custom: false
generate: auto
mode: sr
published_at: "2026-10-03"
updated_at: "2026-10-04"
verification: pending
---
**Fecha del análisis:** 03/10/2026 (auto-generado)
**Parche:** 7.3 (21-sep-2026) + hotfix 7.3a
**Rol principal:** jungla (asumido por motor — revisar)
**Arquetipo:** motor `autos` del optimizador (búsqueda exhaustiva, 539,646 hojas legales)
**Enfoque:** build óptima bajo objetivo ponderado normalizado del lab; leyes 0-7 verificadas numéricamente.

> [!WARNING] REPORTE AUTO-GENERADO — ESPERA DE VERIFICACIÓN
> Generado por `model/generate_report.py` el 03/10/2026. Los NÚMEROS son
> reproducibles por el motor; los JUICIOS (orden de habilidades, plan de juego, primera
> compra, matices de matchup) llevan **TODO** y requieren revisión humana antes de publicar.
> El autor debe: verificar en juego los supuestos, completar los TODO, y entonces
> `generate_report.py aprobar` (o regenerar a mano si detecta inconsistencias).

> [!WARNING] Aproximación del motor
> motor autos NO modela su Q doble golpe ni la forma dragón — resultados aproximados

> [!NOTE]
> **Estado Meta Actual (2026-10-01):**
> Win Rate 46.14 % | Pick Rate 3.76 % | Ban 1.45 % | Tendencia 0 | Tier B | Rol JUNGLE · bucket Diamond + · actualizado 2026-10-01 (champion_winrates.csv)

---

## 0. RESUMEN EJECUTIVO

### Tabla A — BUILD FINAL

| Slot | Ítem | Oro | Rol en la build |
|------|------|-----|-----------------|
| 1 (botas) | **Gunmetal Greaves** | 2 200 | botas (Ley 0: 1 slot) |
| 2 | **Runaan's Hurricane** | 2 650 | 2 rayos 55% AD, critan y aplican on-hit |
| 3 | **Stormrazor** | 3 000 | Energized +120 mágico +45% MS |
| 4 | **Yun Tal Wildarrows** | 3 100 | 7.3a BUFF: AS 25->35; Flurry +35%AS CD25; crit 0->25% en 125 ataques |
| 5 | **Blade of the Ruined King** | 3 100 | 6% vida actual (min 15) |
| 6 | **Infinity Edge** | 3 400 | crítico 200->230% |

> **Oro total: 17 450 g** · métricas del motor: 1v1=2 585, 3v3=4 711, vs120=1 175, vsTanque=914

### Tabla B — Ruta de compra cronológica (aproximación por curvas de oro del vault)

| # | Compra | Oro acum. | Minuto típico |
|---|--------|-----------|---------------|
| 1 | Ítem inicial + poción (start) | 500 | ~0:00 |
| 2 | Botas T2 (Berserker's Greaves) | 1 700 | ~4:30 |
| 3 | runaan | 4 350 | ~8:15 |
| 4 | storm | 7 350 | ~9:53 |
| 5 | yuntal | 10 450 | ~13:28 |
| 6 | botrk | 13 550 | ~15:55 |
| 7 | ie | 16 950 | ~18:37 |
| 8 | ⬆️ Upgrade Gunmetal Greaves (mismo slot, +1 000) | 17 950 | ~20:15 |

> **TODO (humano):** revisar el ORDEN de compra (criterio automático: coste ascendente;
> el orden real depende de componentes, matchups y recalls).

### Runas · Hechizos · Habilidades

| Categoría | Elección |
|-----------|----------|
| Runas (top del buscador) | **Lethal Tempo × Legend: Alacrity** |
| Hechizos | TODO: por rol (jungla) — verificar contra el meta |
| Habilidades | sin ficha en data/estructurada/campeones/ — **TODO: orden de subida** |

### Resultado del modelo (nivel 15)

| Escenario | Valor |
|-----------|-------|
| 1v1 | **2 585** |
| 3v3 | **4 711** |
| vs120 | **1 175** |
| vsTanque | **914** |

---

## 1. CONTEXTO DEL CAMPEÓN EN ESTE PARCHE

### 1.1 Cambios directos (Shyvana)

| Cambio |
|--------|
| **Smite burn vs monstruos** · 30–198/s → **22–162/s** · Jungla early más lenta → Diana jungla: Nashor's 1.º aún más correcto; Shyvana/Volibear/Cho'Gath jungla: clear early −15-20 % |

### 1.2 Cambios sistémicos relevantes (jungla)

| Sistema |
|---------|
| Smite burn vs monstruos: 30–198/s → **22–162/s** → Jungla early más lenta → Diana jungla: Nashor's 1.º aún más correcto; Shyvana/Volibear/Cho'Gath jungla: clear early −15-20 % |

### 1.3 ¿Escala con crítico/otro stat? — TODO humano (leer ficha y notas del spec)

## 2. FICHA MATEMÁTICA (spec)

| Parámetro | Valor |
|---|---|
| AD base / growth | 62 / 4.6 |
| AS base / ratio | 0.638 / 0.638 |
| Base Bonus AS / AS por nivel | 0.25 / 0.012 |
| Rango / melee | 575 / True |
| Notas del spec | Q Twin Bite: doble golpe (100% + 20/40/60/80% AD) y los autos reducen su CD 0.5s → spellblade/on-hit. R dragon: stats bonus + E mejorada. Rutas: AD on-hit (BotRK/Guinsoo/Terminus — sin crit) o AP-burst de R. Modelo: Q como 'ataque doble' (aa_mult efectivo ~1.3-1.6 según rank con CD refund por AS alt |

## 3. MODELO Y FÓRMULAS

Motor `autos` (dps_model.eval_build). Supuestos
estándar del lab (LT/Alacrity full, nivel 15, enemigos de referencia por escenario) — ver
docstring del motor. **TODO:** supuestos específicos del campeón.

## 4. LEYES APLICADAS A SHYVANA

- **Ley 0 — Slots:** `validate_slots` de la build → **PASS** (1 botas + 5 ítems).
- **Ley 1 — Crítico:** total 100 % (umbral 100 %; exceso = oro muerto).
- **Ley 2 — AS:** final 2.46 · cruda 2.46 (tope 3.0) ✅.
- **Ley 3 — Penetración:** 0 % en la build óptima.
- **Ley 4/5 — Stats muertos y eficiencia:** ver tabla de RECHAZADOS (swap medido).
- **Ley 6 — Timing:** ruta de compra fechada con las curvas del vault (Apéndice B).
- **Ley 7 — Sistemas:** cambios de campo del parche en §1.2.

## 5. ANÁLISIS DEL PRIMER ÍTEM

**TODO (humano):** validar primera compra. Pista del motor: ítem más barato de la build
óptima = `gunmetal`; alternativa temprana típica = componentes de `runaan`.

## 6. BUILD FINAL RANURA POR RANURA

**TODO (humano):** justificación prose por slot. Números de referencia en §8 y RECHAZADOS:

| Ítem rechazado | Motivo numérico (mismo escenario) |
|---|---|
| Kraken Slayer | +14.0 % vs build óptima (swap por Gunmetal Greaves) |
| Terminus | +5.8 % vs build óptima (swap por Gunmetal Greaves) |
| Guinsoo's Rageblade | +4.3 % vs build óptima (swap por Gunmetal Greaves) |
| Wit's End | +3.8 % vs build óptima (swap por Gunmetal Greaves) |
| Statikk Shiv | +3.4 % vs build óptima (swap por Gunmetal Greaves) |
| Essence Reaver | +1.8 % vs build óptima (swap por Gunmetal Greaves) |
| Bloodthirster | +0.1 % vs build óptima (swap por Gunmetal Greaves) |
| Fiendhunter | -1.4 % vs build óptima (swap por Gunmetal Greaves) |

## 7. RUNAS · HECHIZOS · HABILIDADES

Top del buscador (valor marginal vs baseline del lab):

| # | Combinación | Marginal | Notas |
|---|-------------|----------|-------|
| 1 | Lethal Tempo × Legend: Alacrity | +0.0 % |  |
| 2 | Lethal Tempo × Cut Down | -2.2 % |  |
| 3 | Lethal Tempo × Last Stand | -3.6 % |  |
| 4 | Lethal Tempo × Coup de Grace | -4.0 % |  |

**TODO (humano):** hechizos y orden de habilidades.

## 8. COMPARACIÓN CONTRA LAS ALTERNATIVAS

| # | Build | Oro | EFIC | Escenarios | Fuente |
|---|-------|-----|------|------------|--------|
| 1 | Gunmetal Greaves + Runaan's Hurricane + Stormrazor + Yun Tal Wildarrows + Blade of the Ruined King + Infinity Edge | 17 450 | 90.1 % | 1v1=2 585 · 3v3=4 711 · vs120=1 175 · vsTanque=914 | ⭐ LAB (óptima) |
| 2 | Gunmetal Greaves + Runaan's Hurricane + Essence Reaver + Yun Tal Wildarrows + Blade of the Ruined King + Infinity Edge | 17 450 | 88.7 % | 1v1=2 564 · 3v3=4 580 · vs120=1 165 · vsTanque=902 | 🔬 LAB top-2 |
| 3 | Gunmetal Greaves + Runaan's Hurricane + Kraken Slayer + Yun Tal Wildarrows + Blade of the Ruined King + Infinity Edge | 17 350 | 88.7 % | 1v1=2 590 · 3v3=4 459 · vs120=1 177 · vsTanque=920 | 🔬 LAB top-3 |
| 4 | Gunmetal Greaves + Runaan's Hurricane + Terminus + Yun Tal Wildarrows + Blade of the Ruined King + Infinity Edge | 17 450 | 88.6 % | 1v1=2 370 · 3v3=4 183 · vs120=1 288 · vsTanque=1 072 | 🔬 LAB top-4 |
| 5 | Gunmetal Greaves + Runaan's Hurricane + Kraken Slayer + Stormrazor + Yun Tal Wildarrows + Infinity Edge | 17 250 | 88.0 % | 1v1=2 562 · 3v3=4 747 · vs120=1 164 · vsTanque=800 | 🔬 LAB top-5 |
| 6 | Gunmetal Greaves + Runaan's Hurricane + Kraken Slayer + Essence Reaver + Yun Tal Wildarrows + Infinity Edge | 17 250 | 86.8 % | 1v1=2 543 · 3v3=4 616 · vs120=1 156 · vsTanque=795 | 🔬 LAB top-6 |

> Convención (estándar v1.13.1): **⭐/🔬 LAB** = builds derivadas por el optimizador del
> laboratorio; las builds de comunidad/externas se marcan `🌐 comunidad` y las publicadas
> `📌 publicada`. Nombres de ítem SIEMPRE completos (decisión del autor, 02/10/2026).

## 9. PLAN DE JUEGO

**TODO (humano):** early/mid/late. Picos de poder de la ruta (Tabla B):
Botas T2 ~4:30, runaan ~8:15, storm ~9:53, yuntal ~13:28.

## 10. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS

- **Fuentes:** motor del lab (specs 7.3+7.3a verificadas contra nota EN oficial),
  champion_winrates.csv (2026-10-01), diffs cambios_*.md,
  curvas de oro de las Tablas B del vault.
- **Validación:** build pasa `validate_slots` (Ley 0) · top-1 de 539,646 hojas legales ·
  runas del buscador con supuestos declarados en optimize_runes.py.
- **Supuestos pendientes de verificación en juego:** TODO humano (véanse WARNING superiores).

## APÉNDICE A — POOL DEL ROL: veredicto automático

Tabla de RECHAZADOS de §6 (swap medido) — ampliar a mano si se requiere.

## APÉNDICE B — RUTAS DE COMPRA

Tabla B de §0 (curvas del vault, rol jungla).

---

## Pie de página

*Reporte AUTO-GENERADO el 03/10/2026 con datos del parche 7.3 + 7.3a
(verificados contra nota EN oficial el 29/09/2026). WR-LAB v1.13. Estado: **Espera de
verificación** — no publicar hasta aprobación del autor. Las cifras son de modelo
comparativo; el valor absoluto importa menos que las diferencias relativas.*

**Referencias y créditos**

- Notas oficiales del parche 7.3 y hotfix 7.3a — © Riot Games, Inc. (wildrift.leagueoflegends.com).
- Base de datos de ítems, runas y fichas — wr-meta.com (proyecto comunitario), win rates Diamond+ del 2026-10-01.
- Modelo matemático, Leyes 0-7, optimizador y validaciones — WR-LAB (`model/generate_report.py` sobre los motores del lab).

**Aviso legal:** Wild Rift y League of Legends son marcas registradas de Riot Games, Inc.
Este documento es una guía de comunidad con fines educativos, **no está afiliada, patrocinada
ni respaldada por Riot Games**.
