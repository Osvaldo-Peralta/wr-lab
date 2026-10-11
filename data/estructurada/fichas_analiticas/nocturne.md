---
tags: [wrlab, ficha, nocturne]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Nocturne
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — NOCTURNE (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** Jungla. Tempo-comp: objetivos tomados bajo oscuridad.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Jungla de presión global: su R apaga el mapa y convierte cada ult en un pick asegurado.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** JUNGLE S+ WR 55.46 % (pick 10.42 %, ban 46.04 %, Confidence High).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- Sin cambios directos en 7.3/7.3a: su balance vive en cambios sistémicos (crit 200 %, AS cap 3.0, torretas 7 000 HP).

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | 54 (5) | champion_base_stats.json |
| HP base (growth) | 660 (134) | champion_base_stats.json |
| Armadura / RM | 43 (4.5) / 40 (2) | champion_base_stats.json |
| AS 7.3 | ratio 0.721 · base 0.721 · BBA 0.11 · growth 0.024 | champion_attack_speed_7.3.csv |
| Rango de ataque | 125 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- R global de ceguera de visión + dash a campeón: pick cross-map.
- Q de estela: MS y AD en camino (kiting y chase).
- W spell-shield: bloquea el CC que lo pararía.
- E miedo: disuasión de pelea y clear de camps.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Pico medio-juego con 2-3 piezas de on-hit/lethalidad.
- Jungla. Tempo-comp: objetivos tomados bajo oscuridad.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **R sobre objetivos sin escape en lados opuestos del mapa.**
2. **W contra el CC conocido del enemigo (timing).**
3. **Clear rápido con Q+E: invade post-6.**

**Sinergias/counters:** Comps de sieje bajo visión reducida; counter de guardianes de zona y cleansers.

## 6. LEYES QUE LA GOBIERNAN

- On-hit/lethalidad: Ley 1 con umbral de crit según build.
- Ley 3b en pen física.

## 7. DIRECCIÓN DE BUILD

- Gunmetal/blade → on-hit (wit's/terminus-like del pool) o lethalidad según comp.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py nocturne` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py nocturne` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
