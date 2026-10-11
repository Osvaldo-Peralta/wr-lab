---
tags: [wrlab, ficha, caitlyn]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Caitlyn
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — CAITLYN (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** ADC. Lane-dominance: gana el draft de posición, no el DPS race.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Marksman de asedio y trampas: el rango más largo base del juego convierte la lane en zona prohibida.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** DUO A WR 49.70 % (pick 20.58 %, ban 10.79 %, Confidence High).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- 7.3a · NERF: **AS growth 0.04→0.025** · Headshot ratio 60–100→**60–90 % AD**

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| HP base (growth) | — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| Armadura / RM | — (fuera del JSON del lab: ver wiki/ficha del autor) / — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| AS 7.3 | ratio 0.625 · base 0.625 · BBA 0.2 · growth 0.025 (7.3a: era 0.04) | champion_attack_speed_7.3.csv |
| Rango de ataque | 625 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Rango base 625 (750 con ult pasiva de headshot): asedio de torreta temprano.
- Trampas (W) en embudos: root + headshot garantizado.
- Q de línea: poke y waveclear; E = dash de kiting con slow.
- Headshots: auto cargado que proca on-hit doble.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Fuerte 0-14 (lane + 2 piezas); decae relativo late vs hypercarries.
- ADC. Lane-dominance: gana el draft de posición, no el DPS race.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **Trampas en entradas de jungle y detrás de minions de asedio.**
2. **Headshot a torre: placas sin exposición.**
3. **Q+E como unitario de escape si flashean sobre ti.**

**Sinergias/counters:** Morgana/Lux support (root → trampa garantizada); counter de draven/ejecutores de inmovilidad.

## 6. LEYES QUE LA GOBIERNAN

- Ley 1 estricta: crit 100 % con 4 piezas.
- Ley 6: C44/IE en checkpoints de oro de lane ganada.

## 7. DIRECCIÓN DE BUILD

- Gunmetal + C44 + Runaan + IE + LDR; Galeforce vs dive.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py caitlyn` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py caitlyn` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
