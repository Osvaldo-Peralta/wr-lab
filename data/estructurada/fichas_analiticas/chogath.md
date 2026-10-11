---
tags: [wrlab, ficha, chogath]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Cho'Gath
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — CHO'GATH (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** Top o Jungla. Frontline que amenaza carries con ejecuciones reales.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Tanque AP de escalado infinito: Feast convierte kills/objectivos en HP permanente que ningún item iguala.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía —):** sin filas en el CSV del vigía todavía.

---

## 1. QUÉ LE HIZO ESTE PARCHE

- Sin cambios directos en 7.3/7.3a: su balance vive en cambios sistémicos (crit 200 %, AS cap 3.0, torretas 7 000 HP).

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | 62 (4) | champion_base_stats.json |
| HP base (growth) | 690 (128) | champion_base_stats.json |
| Armadura / RM | 46 (4.5) / 40 (2) | champion_base_stats.json |
| AS 7.3 | ratio 0.625 · base 0.625 · BBA 0.28 · growth 0.008 | champion_attack_speed_7.3.csv |
| Rango de ataque | 175 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Feast (R): ejecución de vida + stack de HP permanente (escalado infinito).
- Rupture (Q) knockup + W silencio: cadena de CC en área.
- E: autos en cono con daño mágico % vida: waveclear y pelea.
- Pasiva de regen al matar unidades: sostenibilidad de lane.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Lento early; imparable 3+ stacks de Feast con 2 ítems de HP.
- Top o Jungla. Frontline que amenaza carries con ejecuciones reales.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **Feast a monstruos épicos y minions de asedio: stacks sin kills.**
2. **Q sobre el dash enemigo (predictivo de patrón).**
3. **E activado para tradear: cono > auto simple.**

**Sinergias/counters:** Sinergia con engages lentos (Amumu-like); counter de ejecutores de %vida (Vayne-like) y grievous temprano.

## 6. LEYES QUE LA GOBIERNAN

- Tanque AP: Leyes de slots igual; el 'DPS' es %vida → pen mágica y HP multiplican.
- Ley 0 aplica; Ley 1 no (sin crit).

## 7. DIRECCIÓN DE BUILD

- Cinturón gigante → sunfire/iceborn por rol; zapatos según CC enemigo.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py chogath` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py chogath` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
