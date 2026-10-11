---
tags: [wrlab, ficha, seraphine]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Seraphine
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — SERAPHINE (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** Support. Teamfight-comp: su valor crece con la duración de la pelea.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Enchanter de cadena: cada habilidad se duplica y encadena CC/curas en área creciente.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** SUPPORT A WR 49.59 % (pick 6.59 %, ban 1.03 %, Confidence Med).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- Sin cambios directos en 7.3/7.3a: su balance vive en cambios sistémicos (crit 200 %, AS cap 3.0, torretas 7 000 HP).

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | 52 (3.64) | champion_base_stats.json |
| HP base (growth) | 600 (112) | champion_base_stats.json |
| Armadura / RM | 34 (4.71) / 36 (1.2) | champion_base_stats.json |
| AS 7.3 | ratio 0.699 · base 0.669 · BBA 0.12 · growth 0.017 | champion_attack_speed_7.3.csv |
| Rango de ataque | 525 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Pasiva de notas duplicadas: cada 3.ª habilidad se repite con notas de daño/cura.
- Q daño en área que escala por nota: poke sostenido.
- W escudo+cura en área con MS: sustain de pelea.
- E slow/root en cadena: setup de picks.
- R encantamiento en línea larga: engage o peel masivo.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Pico medio-juego con 2-3 piezas de utility; decae vs burst inmediato.
- Support. Teamfight-comp: su valor crece con la duración de la pelea.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **R desde flanco: la línea larga atrapa 3+.**
2. **W antes del burst enemigo, no después.**
3. **Notas de pasiva en lane: Q+auto duplicado.**

**Sinergias/counters:** Comps de pelea larga (hypercarries); counter de engages de 1 botón.

## 6. LEYES QUE LA GOBIERNAN

- Support valor-aliado: heal/shield power + haste.
- Ley 0; sin crit.

## 7. DIRECCIÓN DE BUILD

- Crimson → moonstone/echo → censer/redemption.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py seraphine` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py seraphine` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
