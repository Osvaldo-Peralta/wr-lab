---
tags: [wrlab, ficha, mordekaiser]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Mordekaiser
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — MORDEKAISER (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** Top. Split-push que el enemigo no puede ignorar ni contestar 1v1.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Juggernaut de duelos en reino muerto: su R crea un 1v1 obligatorio donde siempre gana.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** SOLO S+ WR 51.73 % (pick 10.59 %, ban 29.24 %, Confidence High).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- Sin cambios directos en 7.3/7.3a: su balance vive en cambios sistémicos (crit 200 %, AS cap 3.0, torretas 7 000 HP).

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | 54 (3.5) | champion_base_stats.json |
| HP base (growth) | 660 (120) | champion_base_stats.json |
| Armadura / RM | 46 (4) / 40 (2) | champion_base_stats.json |
| AS 7.3 | ratio 0.625 · base 0.625 · BBA 0.17 · growth 0.008 | champion_attack_speed_7.3.csv |
| Rango de ataque | 175 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- R: secuestra al objetivo a un reino 1v1 (stats robadas).
- Q de 3 hits con daño creciente: duelo y clear.
- W armadura acumulable que detona en heal/damage.
- E pull: mantiene al objetivo en su zona de muerte.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Fuerte 1-2 ítems en duelos; teamfight depende de R bien usado.
- Top. Split-push que el enemigo no puede ignorar ni contestar 1v1.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **R al carry sin escape o al que gana tu 1v1 siempre.**
2. **W antes del trade largo: la detonación cierra kills.**
3. **Push lateral: el reino muerto hace al split invulnerable a ganks 1v1.**

**Sinergias/counters:** Comps sin peel duro; counter de cleansers (QSS) y campeones de rango sostenido.

## 6. LEYES QUE LA GOBIERNAN

- AP juggernaut: liandry/rimland por HP; sin crit.
- Ley 0.

## 7. DIRECCIÓN DE BUILD

- Riftmaker/liandry → demonic → spirit visage según daño enemigo.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py mordekaiser` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py mordekaiser` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
