---
tags: [wrlab, ficha, ornn]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Ornn
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — ORNN (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** Top. Utility-tank: valor de equipo por encima del propio.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Tanque herrero: mejora ítems aliados y crea engages de área con fuelle y fragua.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** SOLO A WR 51.76 % (pick 2.08 %, ban 0.17 %, Confidence Low) · SUPPORT A WR 48.90 % (pick 1.14 %, ban 0.17 %, Confidence Low).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- Sin cambios directos en 7.3/7.3a: su balance vive en cambios sistémicos (crit 200 %, AS cap 3.0, torretas 7 000 HP).

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| HP base (growth) | — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| Armadura / RM | — (fuera del JSON del lab: ver wiki/ficha del autor) / — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| AS 7.3 | ratio 0.625 · base 0.625 · BBA 0.17 · growth 0.012 | champion_attack_speed_7.3.csv |
| Rango de ataque | 175 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Pasiva: forja ítems para aliados (oro extra convertido en stats).
- Q grieta + W fuelle de fragua: knock-up encadenado.
- E dash que rebate en terreno: reposiciona peleas.
- R de carnero global: engage de área con 2 llamadas.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Valor desde 1-2 ítems; la mejora de ítems aliados escala con el juego.
- Top. Utility-tank: valor de equipo por encima del propio.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **Mejora el ítem del carry en cada back (value compuesto).**
2. **W sobre el Q landeado: knock-up asegurado.**
3. **R de segunda llamada como peel, no solo engage.**

**Sinergias/counters:** Carries que agradecen mejoras (IE/Runaan mejorados); counter de ranged kiting sin melee check.

## 6. LEYES QUE LA GOBIERNAN

- Tanque utility: sin crit; presupuesto de HP/armor.
- Ley 0.

## 7. DIRECCIÓN DE BUILD

- Iceborn/sunfire → thornmail → visionary para mejoras aliadas.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py ornn` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py ornn` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
