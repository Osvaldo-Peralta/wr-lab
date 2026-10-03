---
tags:
  - Jungla
  - Auto
version: 0.9
Status: Espera de verificación
champion: Rammus
slug: rammus-auto-73a
role: jungla
patch: "7.3a"
archetype: "tanque/juggernaut — sin motor cuantitativo (generación cualitativa)"
engine: none
published_at: "2026-10-03"
custom: false
generate: auto
mode: sr
---
**Fecha del análisis:** 03/10/2026 (auto-generado, modo cualitativo)
**Parche:** 7.3 (21-sep-2026) + hotfix 7.3a
**Rol principal:** jungla (derivado del reporte publicado)
**Arquetipo:** tanque — **sin motor cuantitativo** (motor de tanques: ROADMAP). Método:
datos reales + cálculos parciales con supuestos declarados + TODOs explícitos.
**Enfoque:** re-derivar la guía publicada (Rammus.md, datos 7.3) contra 7.3a SIN cambiar
la build hasta que el autor valide los números parciales.

> [!WARNING] REPORTE AUTO-GENERADO (MODO CUALITATIVO) — ESPERA DE VERIFICACIÓN
> Generado por `model/generate_report.py` el 03/10/2026. Este campeón no tiene
> motor cuantitativo en el lab: las secciones numéricas completas (DPS/EHP por build) llevan
> **TODO**; los cálculos incluidos (EHP físico, W) usan supuestos DECLARADOS en §10 y deben
> verificarse en juego. El autor debe completar TODOs y aprobar, o regenerar a mano.

> [!NOTE]
> **Estado Meta Actual (2026-10-01):**
> Win Rate 56.81 % | Pick 5.42 % | Ban 5.84 % | Tendencia 0 | **Tier S+** | Rol JUNGLE · Diamond + · actualizado 2026-10-01 (champion_winrates.csv)

---

## 0. RESUMEN EJECUTIVO

### Tabla A — BUILD FINAL (heredada del reporte publicado + corrección Ley 0 de botas)

| Slot | Ítem | Oro | Categoría |
|------|------|-----|-----------|
| 1 | **Sunfire Aegis** | 2 900 | Defense Items |
| 2 (botas) | **Plated Steelcaps → ⬆️ Armored Advance** (min 10:00, MISMO slot) | 1 200 | Boots Tier 2 |
| 3 | **Thornmail** | 2 700 | Defense Items |
| 4 | **Dead Man's Plate** | 2 800 | Defense Items |
| 5 | **Force of Nature** | 2 800 | Defense Items |
| 6 | **Gargoyle Stoneplate** | 2 900 | Defense Items |

> **Oro total: 16 300 g** (incluye +1 000 del upgrade T2→T3 que la ruta publicada omitía — Ley 0)
> Stats agregados de ítems (CSV oficial): HP +1 650 · Armadura +250 · MR +105

### Tabla B — Ruta de compra cronológica (minutos del reporte publicado)

| # | Compra | Oro acum. | Minuto típico |
|---|--------|-----------|---------------|
| 1 | Sunfire Aegis | 2 900 | ~8:00 |
| 2 | Plated Steelcaps | 4 100 | ~9:30 |
| 3 | Thornmail | 6 800 | ~12:00 |
| 4 | Dead Man's Plate | 9 600 | ~14:00 |
| 5 | Force of Nature | 12 400 | ~16:30 |
| 6 | Gargoyle Stoneplate | 15 300 | ~19:00 |
| 7 | ⬆️ Armored Advance (mismo slot, +1 000) | 16 300 | ~19:30 (post 10:00) |

### Runas · Hechizos · Habilidades

| Categoría | Elección |
|-----------|----------|
| Keystone | **TODO** (sin fuente de runas verificada para tanques en el lab — verificar en juego/wr-meta) |
| Hechizos | Smite + Flash (jungla) |
| Habilidades | W = Defensive Ball Curl (fuente: notas EN 7.3a) — **TODO: resto del kit y orden** |

### Resultado del modelo — CÁLCULOS PARCIALES (ver §8 y supuestos §10)

| Métrica | Pre-7.3a | Post-7.3a | Δ |
|---|---|---|---|
| Armadura total aprox. (nivel 15) | 295 | 290 | −5 |
| EHP físico aprox. | 14 062 | 13 884 | -1.3 % |
| W rank 4 (60 % armadura) | 177 | 174 | -3 |
| W rank 1 (45→30 %) | 133 | 87 | -46 |

---

## 1. CONTEXTO DEL CAMPEÓN EN ESTE PARCHE

### 1.1 Cambios directos (Rammus)

| Cambio |
|--------|
| **Rammus** · NERF · Armor base 45→**40** · W bonus armor 45/50/55/60→**30/40/50/60 %** |

### 1.2 Cambios sistémicos relevantes (jungla)

| Sistema |
|---------|
| Smite burn vs monstruos: 30–198/s → **22–162/s** → Jungla early más lenta → Diana jungla: Nashor's 1.º aún más correcto; Shyvana/Volibear/Cho'Gath jungla: clear early −15-20 % |

### 1.3 ¿Escala con crítico/otro stat? — **TODO humano** (leer kit completo)

## 2. FICHA MATEMÁTICA (datos disponibles en el lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AS ratio / base / bonus / por nivel | 0.625,0.625,0.28,0.0185 | champion_attack_speed_7.3.csv |
| Armadura base | 45 → **40** (7.3a) | notas EN 7.3a |
| HP/AD/MR base y growths | **TODO** — wr-meta.com/242-rammus.html (id conocido) |
| Kit (Q/W/E/R con valores) | **TODO** — misma fuente |

## 3. MODELO Y FÓRMULAS

**Sin motor cuantitativo** (motor de tanques en ROADMAP: EHP + daño por armadura + pasivas).
Cálculos parciales de §0/§8: EHP = (HP base + HP ítems) × (1 + armadura/100); W = % × armadura
total. Supuestos en §10.

## 4. LEYES APLICADAS A RAMMUS (formato compacto — estándar v1.13.1)

- **Ley 0 — Slots:** 6 slots = 1 botas + 5 ítems. La ruta publicada usaba botas T2 sin upgrade:
  corregida a Armored Advance (+1 000 g, mismo slot, min 10:00).
- **Ley 1/2/3 — Crítico/AS/Pen:** no aplican al arquetipo tanque (stats muertos por diseño —
  verificar que la build no los pague: ✅ ninguno en Tabla A).
- **Ley 4 — Stats muertos:** armadura/MR/HP son el daño Y la defensa de Rammus (sinergia W).
- **Ley 5 — Eficiencia:** TODO al completar el motor de tanques.
- **Ley 6 — Timing:** ruta publicada conservada (Tabla B); smite nerf → clear early más lento,
  **TODO: re-fechar primeros clears**.
- **Ley 7 — Sistemas:** ver §1.2 (smite burn −, placas/Nexus).

## 5. ANÁLISIS DEL PRIMER ÍTEM

Ruta publicada: **Sunfire Aegis** (~8:00).
**TODO humano:** validar contra el nerf de smite (clear early más lento) y el meta 7.3a.

## 6. BUILD FINAL RANURA POR RANURA

**TODO humano:** justificación por slot. Alternativas del pool tanque (CSV oficial) para la
matriz situacional — motivos numéricos pendientes del motor:

| Ítem alternativo | Motivo |
|---|---|
| Titanic Hydra | **TODO numérico** (sin motor de tanques — ROADMAP): justificar vs la build publicada |
| Overlord's Bloodmail | **TODO numérico** (sin motor de tanques — ROADMAP): justificar vs la build publicada |
| Guardian Angel | **TODO numérico** (sin motor de tanques — ROADMAP): justificar vs la build publicada |
| Sterak's Gage | **TODO numérico** (sin motor de tanques — ROADMAP): justificar vs la build publicada |
| Death's Dance | **TODO numérico** (sin motor de tanques — ROADMAP): justificar vs la build publicada |
| Banshee's Veil | **TODO numérico** (sin motor de tanques — ROADMAP): justificar vs la build publicada |

## 7. RUNAS · HECHIZOS · HABILIDADES

**TODO humano** (keystone de tanque, secundarias, orden de habilidades). Ver §0.

## 8. COMPARACIÓN CONTRA LAS ALTERNATIVAS

Comparación cuantitativa de builds: **PENDIENTE del motor de tanques** (ROADMAP).
Lo que SÍ se puede afirmar con datos de 7.3a (supuestos §10):

| Métrica | 📌 Publicada pre-7.3a | 🔬 LAB post-7.3a (misma build) | Δ |
|---|---|---|---|
| EHP físico aprox. | 14 062 | 13 884 | -1.3 % |
| W rank 4 | 177 | 174 | -3 |
| W rank 1 (early) | 133 | 87 | -34 % |
| Clear de jungla early | baseline | smite burn −18 % → más lento | cualitativo |

> **Lectura:** el nerf 7.3a pega sobre todo al EARLY (W rank 1 −34 %,
> clear más lento); el late apenas cambia (W rank 4 −3, EHP -1.3 %).
> Con WR 56.81 % tier S+: la build publicada
> sigue siendo razonable — **TODO: decidir si se re-optimiza con el motor de tanques**.

## 9. PLAN DE JUEGO

**TODO humano.** Picos de la ruta publicada: Sunfire Aegis ~8:00, Plated Steelcaps ~9:30, Thornmail ~12:00, Dead Man's Plate ~14:00.
Ajustar early por smite nerf (clear −15-20 % estimado en §1.2).

## 10. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS

- **Fuentes:** diffs cambios_campeones_7.3.md + cambios_7.3a.md (verificados contra nota EN
  oficial) · champion_attack_speed_7.3.csv · items_7.3.csv (stats/precios) ·
  champion_winrates.csv (2026-10-01) · build/ruta: Rammus.md (publicado 7.3).
- **Supuestos DECLARADOS de los cálculos parciales:** HP/armadura base nivel 15 aproximados con
  fallback genérico del lab (1 910 HP / 45 arm / 35 MR — Rammus NO está en
  champion_base_stats.json); W = % × armadura TOTAL (la fórmula exacta de bonus vs total debe
  verificarse con la ficha); EHP sin escudos/activas. **Verificar en juego antes de publicar.**
- **Validación:** Ley 0 chequeada (upgrade de botas añadido) · win rates del pipeline oficial.

## APÉNDICE A — POOL DEL ROL: veredicto automático

Alternativas del §6 (pool tanque del CSV) — veredictos numéricos pendientes del motor.

## APÉNDICE B — RUTAS DE COMPRA

Tabla B de §0 (minutos del reporte publicado + upgrade Ley 0).

---

## Pie de página

*Reporte AUTO-GENERADO (modo cualitativo) el 03/10/2026 con datos del parche 7.3 +
7.3a (verificados contra nota EN oficial el 29/09/2026). WR-LAB v1.13.1. Estado: **Espera de
verificación** — no publicar hasta aprobación del autor. Cálculos parciales con supuestos
declarados en §10.*

**Referencias y créditos**

- Notas oficiales del parche 7.3 y hotfix 7.3a — © Riot Games, Inc. (wildrift.leagueoflegends.com).
- Base de datos de ítems y win rates — wr-meta.com (proyecto comunitario), Diamond+ del 2026-10-01.
- Modelo, Leyes 0-7 y validaciones — WR-LAB (`model/generate_report.py`, modo cualitativo).

**Aviso legal:** Wild Rift y League of Legends son marcas registradas de Riot Games, Inc.
Este documento es una guía de comunidad con fines educativos, **no está afiliada, patrocinada
ni respaldada por Riot Games**.
