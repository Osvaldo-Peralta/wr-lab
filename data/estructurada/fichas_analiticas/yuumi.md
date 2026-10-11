---
tags: [wrlab, ficha, yuumi]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Yuumi
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — YUUMI (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** Support. Hypercarry-comp: multiplica al aliado, no existe sola.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Enchanter-parásita: valor-aliado puro sin posición propia; el carry ES tu posición.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** SUPPORT A WR 48.70 % (pick 9.25 %, ban 33.79 %, Confidence High).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- 7.3a · NERF: W Best Friend HSP: 8/9/10/11 % + 0.02 % AP → **6/7/8/9 % + 0.01 % AP**

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | 50 (3.64) | champion_base_stats.json |
| HP base (growth) | 570 (104) | champion_base_stats.json |
| Armadura / RM | 40 (3.9) / 35 (1.2) | champion_base_stats.json |
| AS 7.3 | ratio 0.625 · base 0.625 · BBA 0.2 · growth 0.006 | champion_attack_speed_7.3.csv |
| Rango de ataque | 425 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- W anexión al aliado: stats compartidas y untargetable.
- Q proyectil dirigido desde el aliado: poke y slows.
- E heal+MS en anexión: sustain de lane.
- R páginas de knock-up en área: peel/engage desde el carry.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Valor desde 1-2 piezas de heal/shield power; escala con el carry.
- Support. Hypercarry-comp: multiplica al aliado, no existe sola.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **Cambio de carry en pelea (W hop): valor doble.**
2. **R sobre el dive enemigo, no al inicio.**
3. **Q desde arbustos/aliados para poke sin riesgo.**

**Sinergias/counters:** Hypercarries de AS (jinx/yunara); counter de burst que mata al carry anfitrión.

## 6. LEYES QUE LA GOBIERNAN

- Support valor-aliado: moonstone/censer; sin crit ni DPS propio.
- Ley 0 en builds de utility.

## 7. DIRECCIÓN DE BUILD

- Crimson → moonstone → censer/redemption; hose de heal-shield power.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py yuumi` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py yuumi` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
