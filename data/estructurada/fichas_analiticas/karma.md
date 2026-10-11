---
tags: [wrlab, ficha, karma]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Karma
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — KARMA (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** Support (y mid niche). Flex-pick: se adapta al comp enemigo.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Enchanter de poke y shields: el mantra de 2 cargas convierte cada habilidad en dos efectos.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** SUPPORT A WR 49.77 % (pick 4.76 %, ban 0.37 %, Confidence Med).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- Sin cambios directos en 7.3/7.3a: su balance vive en cambios sistémicos (crit 200 %, AS cap 3.0, torretas 7 000 HP).

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | 58 (3.64) | champion_base_stats.json |
| HP base (growth) | 630 (128) | champion_base_stats.json |
| Armadura / RM | 37 (5) / 36 (1.2) | champion_base_stats.json |
| AS 7.3 | ratio 0.625 · base 0.625 · BBA 0.2 · growth 0.0135 | champion_attack_speed_7.3.csv |
| Rango de ataque | 525 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Q con mantra = doble lanza + explosión: poke y waveclear.
- E escudo con mantra = área + MS: engage/disengage de equipo.
- W root retardado con daño: zone control.
- Pasiva de haste por auto: spameo sostenido.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Pico de impacto medio-juego; decae si el juego se estira a carry-scaling.
- Support (y mid niche). Flex-pick: se adapta al comp enemigo.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **Mantra en E para engages, en Q para poke de sieje.**
2. **Escudo pre-mitigación de burst enemigo (timing > tamaño).**
3. **Poke de lane con Q+auto para stacks de pasiva.**

**Sinergias/counters:** Carries de poke (varus/caitlyn-like); counter de engages duros que ignoran shields.

## 6. LEYES QUE LA GOBIERNAN

- Support: valor-aliado (escudo×haste); sin crit.
- Ley 0 en builds de utility.

## 7. DIRECCIÓN DE BUILD

- Crimson → echo/moonstone → censer/redemption según carry.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py karma` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py karma` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
