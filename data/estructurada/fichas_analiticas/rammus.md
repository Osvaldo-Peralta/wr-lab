---
tags: [wrlab, ficha, rammus]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Rammus
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — RAMMUS (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** Jungla. Counter-pick de comps físicos; ganks de taunt asegurado.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Bola de armadura con taunt: el anti-AD personificado que convierte tu armadura en su daño.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** JUNGLE S+ WR 57.13 % (pick 4.80 %, ban 6.60 %, Confidence Med).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- 7.3a · NERF: Armor base 45→**40** · W bonus armor 45/50/55/60→**30/40/50/60 %**

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| HP base (growth) | — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| Armadura / RM | — (fuera del JSON del lab: ver wiki/ficha del autor) / — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| AS 7.3 | ratio 0.625 · base 0.625 · BBA 0.28 · growth 0.0185 | champion_attack_speed_7.3.csv |
| Rango de ataque | 125 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Q bola: MS masiva para ganks y objetivos; knock-up al llegar.
- W bola defensiva: armadura que refleja daño de autos.
- E taunt puntual: obliga autos sobre ti (protege carries).
- R salto en área: engage de zona con daño por armadura.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Fuerte desde 1-2 piezas de armadura; decae vs AP.
- Jungla. Counter-pick de comps físicos; ganks de taunt asegurado.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **Gank con Q+E: el taunt hace el resto.**
2. **W activo en cada trade de autos.**
3. **R en torretas/objetivos: zona negada.**

**Sinergias/counters:** Comps AD enemigos (draft-win); counter de AP mages y kiting de rango.

## 6. LEYES QUE LA GOBIERNAN

- Tanque de armadura: su daño escala con armor (único).
- Ley 0; sin crit.

## 7. DIRECCIÓN DE BUILD

- Iceborn/thornmail → sunfire → fuerza natural tardía.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py rammus` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py rammus` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
