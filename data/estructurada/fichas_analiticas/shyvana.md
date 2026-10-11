---
tags: [wrlab, ficha, shyvana]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Shyvana
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — SHYVANA (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** Jungla. Farm-to-scale: objetivos épicos como motor de poder.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Dragón juggernaut de transform: clear monstruoso y teamfights como drake gigante.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** JUNGLE B WR 46.13 % (pick 3.41 %, ban 1.25 %, Confidence Med).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- Sin cambios directos en 7.3/7.3a: su balance vive en cambios sistémicos (crit 200 %, AS cap 3.0, torretas 7 000 HP).

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | 62 (4.6) | champion_base_stats.json |
| HP base (growth) | 660 (120) | champion_base_stats.json |
| Armadura / RM | 46 (5) / 38 (2) | champion_base_stats.json |
| AS 7.3 | ratio 0.638 · base 0.638 · BBA 0.25 · growth 0.012 | champion_attack_speed_7.3.csv |
| Rango de ataque | 125 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Pasiva de daño a monstruos + stacks por drake cazado: escala con objetivos.
- Q doble golpe + reset de auto: duelo y clear.
- W aura de daño + MS: kiting y clear en movimiento.
- E marca de daño %vida: execute blando.
- R transform a dragón: HP + ranged attacks + knock-up.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Clear elite early; pico 2-3 ítems híbridos con drakes stackeados.
- Jungla. Farm-to-scale: objetivos épicos como motor de poder.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **Drakes = stats gratis: prioriza objetivos sobre ganks.**
2. **W activo en movimiento entre camps (clear rodante).**
3. **R como engage o como peel: knock-up de área.**

**Sinergias/counters:** Comps que estiran peleas; counter de kiting extremo y grievous temprano.

## 6. LEYES QUE LA GOBIERNAN

- Híbrida AD/AP: build según stack de drakes (motor cualitativo).
- Ley 0.

## 7. DIRECCIÓN DE BUILD

- Blade/sunfire híbrido → on-hit o AP según transformación dominante.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py shyvana` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py shyvana` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
