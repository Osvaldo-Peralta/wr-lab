---
tags: [wrlab, ficha, kalista]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Kalista
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — KALISTA (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** ADC. Skill-expression: el techo de ejecución más alto del rol.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Marksman de kiting infinito: el dash por auto permite reposicionarse en cada golpe si respetas el ritmo.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** DUO A WR 50.70 % (pick 5.70 %, ban 6.30 %, Confidence Med) · SOLO S+ WR 53.35 % (pick 2.38 %, ban 6.30 %, Confidence Low).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- Sin cambios directos en 7.3/7.3a: su balance vive en cambios sistémicos (crit 200 %, AS cap 3.0, torretas 7 000 HP).

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | 57 (5.2) | champion_base_stats.json |
| HP base (growth) | 630 (128) | champion_base_stats.json |
| Armadura / RM | 34 (4.5) / 32 (1.4) | champion_base_stats.json |
| AS 7.3 | ratio 0.694 · base 0.694 · BBA 0.16 · growth 0.046 | champion_attack_speed_7.3.csv |
| Rango de ataque | 550 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Pasiva de dash por auto: kiting perpetuo si mueves tras cada attack.
- Lanzas (E) acumulables: slow + extracción con reset al matar.
- W pacto con aliado: daño bonus sincronizado y visión.
- R guarda al support: engage/disengage dual.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Fuerte desde 2 piezas si el jugador mantiene el ritmo de dash.
- ADC. Skill-expression: el techo de ejecución más alto del rol.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **E reset en minions/monstruos: poke gratuito en lane.**
2. **R al support engage: pick garantizado.**
3. **Dash lateral, no hacia atrás: mantiene DPS.**

**Sinergias/counters:** Supports de engage (leona-like) por el pacto y la R; counter de CC puntual que rompe el ritmo.

## 6. LEYES QUE LA GOBIERNAN

- On-hit/crit híbrido: Ley 1 con umbral según build.
- Ley 0 estricta.

## 7. DIRECCIÓN DE BUILD

- Gunmetal + Blade/Runaan según comp + IE + pen; on-hit vs tanques.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py kalista` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py kalista` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
