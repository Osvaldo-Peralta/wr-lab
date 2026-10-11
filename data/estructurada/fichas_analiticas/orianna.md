---
tags: [wrlab, ficha, orianna]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Orianna
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — ORIANNA (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** Mid. Teamfight-comp: su R de shockwave define peleas.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Maga de control de área con la bola: el posicionamiento de la esfera es su skill real.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** MID A WR 51.67 % (pick 4.50 %, ban 0.27 %, Confidence Med).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- Sin cambios directos en 7.3/7.3a: su balance vive en cambios sistémicos (crit 200 %, AS cap 3.0, torretas 7 000 HP).

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | 46 (2.7) | champion_base_stats.json |
| HP base (growth) | 630 (120) | champion_base_stats.json |
| Armadura / RM | 28 (4) / 36 (1.2) | champion_base_stats.json |
| AS 7.3 | ratio 0.658 · base 0.658 · BBA 0.14 · growth 0.032 | champion_attack_speed_7.3.csv |
| Rango de ataque | 525 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Q mueve la bola: todo el kit opera desde su posición.
- W área de daño/MS alrededor de la bola.
- E escudo al aliado que porta la bola + daño en camino.
- R shockwave en la bola: el engage/peel más grande del juego.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Escalado AP clásico; pico 3 ítems con teamfight ganada por R.
- Mid. Teamfight-comp: su R de shockwave define peleas.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **Bola en el frontline propio antes del engage enemigo.**
2. **E sobre el diver aliado: escudo + daño de regreso.**
3. **R con 3+ objetivos o al carry sin posición.**

**Sinergias/counters:** Frontlines que agrupan enemigos (amumu/malphite-like); counter de asesinos de burst inmediato.

## 6. LEYES QUE LA GOBIERNAN

- AP: luden/cap; hache para spameo de Q.
- Ley 0; sin crit.

## 7. DIRECCIÓN DE BUILD

- Luden → horizon/cap → zhonya si dive.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py orianna` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py orianna` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
