---
tags: [wrlab, ficha, senna]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Senna
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — SENNA (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** Support S+ (valor-aliado + asedio) y DUO S+ (DPS medido por motor).
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 0.9× (kit)
**Tesis:** Artillera de asedio con escalado infinito de Niebla: AD y crit gratis permanentes que reescriben la Ley 1.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** DUO S+ WR 55.16 % (pick 3.45 %, ban 36.40 %, Confidence Med) · SUPPORT S+ WR 54.11 % (pick 13.33 %, ban 36.40 %, Confidence High).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- 7.3a · AJUSTE: AS ratio/base 0.4→**0.3** · Base Bonus AS 0.6→**1.1** · AS growth 0.05→**0.025** · la AS bonus reduce menos el wind-up

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| HP base (growth) | — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| Armadura / RM | — (fuera del JSON del lab: ver wiki/ficha del autor) / — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| AS 7.3 | ratio 0.3 (7.3a) · base 0.3 (7.3a) · BBA 1.1 (7.3a) · growth 0.025 (7.3a) | champion_attack_speed_7.3.csv |
| Rango de ataque | 625 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 0.9× (kit) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Pasiva Niebla: +1.25 AD y +10 % crit/20 stacks; overcap → 35 % vamp.
- Relic Cannon: auto hitscan con on-hit +20 % AD y wind-up largo.
- Q línea que cura aliados y daña (−1 s CD por auto).
- W root en área con truco de minion moribundo; E camuflaje de equipo; R global de escudo+ejecución.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Débil early (570 HP, AS 0.63); asedio imparable 14+ min con 90-140 stacks.
- Support S+ (valor-aliado + asedio) y DUO S+ (DPS medido por motor).

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **No lasthear como support: wraiths garantizados de minions ajenos.**
2. **W + minion moribundo = root instantáneo desde 1 300.**
3. **R triple: ejecución + escudo pre-engage + Niebla global.**
4. **Q a través de ola/torreta: value sin exposición.**

**Sinergias/counters:** Jhin/J4 (roots encadenados); counter de dive instantáneo (blitz/malphite).

## 6. LEYES QUE LA GOBIERNAN

- Ley 1 UMBRAL BLANDO: 50 % crit de ítems + 50 % gratis; overcap → vamp (no oro muerto).
- Ley 2 no vinculante (techo AS 1.44).
- Ley 3: BotRK sustituye pen vs tanques (current-health).

## 7. DIRECCIÓN DE BUILD

- Support: Crimson+ER+Censer+Cleaver+Echo+GA · DUO: óptima del motor (ver reporte).
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py senna` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py senna` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
