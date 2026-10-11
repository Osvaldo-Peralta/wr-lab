---
tags: [wrlab, ficha, xayah]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Xayah
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — XAYAH (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** ADC. Self-peel único: su R la hace intargetable y recupera plumas.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Marksman de plumas recuperables: el auto-positioning de sus plumas crea burst y raíz a voluntad.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** DUO A WR 50.44 % (pick 4.49 %, ban 0.18 %, Confidence Med).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- Sin cambios directos en 7.3/7.3a: su balance vive en cambios sistémicos (crit 200 %, AS cap 3.0, torretas 7 000 HP).

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| HP base (growth) | — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| Armadura / RM | — (fuera del JSON del lab: ver wiki/ficha del autor) / — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| AS 7.3 | ratio 0.658 · base 0.658 · BBA 0.22 · growth 0.034 | champion_attack_speed_7.3.csv |
| Rango de ataque | 525 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Pasiva: habilidades dejan plumas; E las召回 con daño creciente y root con 3+.
- Q lanza plumas en línea; W AS+daño bonus al auto al campeón.
- R intargetable + abanico de plumas: el mejor self-peel del rol.
- Plumas persisten en el suelo: zoning permanente.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Pico 2-3 ítems de crit; root de E hace duelos ganables.
- ADC. Self-peel único: su R la hace intargetable y recupera plumas.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **E tras R: root garantizado de 5 plumas.**
2. **Plumas en embudos: zona de root permanente.**
3. **W en objetivos: el AS bonus es tu burst window.**

**Sinergias/counters:** Rakan-like/peel supports; counter de cleaners de plumas y dives por detrás.

## 6. LEYES QUE LA GOBIERNAN

- Ley 1 estricta; Ley 3b.
- Ley 6 checkpoints de crit.

## 7. DIRECCIÓN DE BUILD

- Gunmetal + C44/Runaan + IE + LDR; Galeforce vs dive duro.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py xayah` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py xayah` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
