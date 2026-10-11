---
tags: [wrlab, ficha, sivir]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Sivir
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — SIVIR (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** ADC. Tempo-comp: su R de MS global crea engages propios.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Marksman de rebotes y oleadas: el waveclear más rápido del juego convertido en presión de mapa.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** DUO A WR 48.78 % (pick 3.54 %, ban 0.06 %, Confidence Med).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- Sin cambios directos en 7.3/7.3a: su balance vive en cambios sistémicos (crit 200 %, AS cap 3.0, torretas 7 000 HP).

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| HP base (growth) | — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| Armadura / RM | — (fuera del JSON del lab: ver wiki/ficha del autor) / — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| AS 7.3 | ratio 0.625 · base 0.625 · BBA 0.3 · growth 0.01 | champion_attack_speed_7.3.csv |
| Rango de ataque | 500 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Q bumerán con daño doble: poke y clear.
- W rebotes en cadena: clear instantáneo y teamfight AoE.
- E spell-shield: bloqueo gratuito de habilidad clave (y maná).
- R MS en área global: el engage de equipo más barato.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Pico de clear 2 piezas; teamfight con W+R desde 3.
- ADC. Tempo-comp: su R de MS global crea engages propios.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **E sobre el engage enemigo conocido (maná + tempo).**
2. **R para iniciar o para responder dives.**
3. **Push lateral con Q+W: torretas sin pelea.**

**Sinergias/counters:** Comps de engage propio (malphite/ornn-like); counter de poke que quiebra su positioning.

## 6. LEYES QUE LA GOBIERNAN

- Ley 1 estricta crit; Ley 3b pen.
- Ley 6: checkpoints de clear.

## 7. DIRECCIÓN DE BUILD

- Gunmetal + C44/Runaan + IE + LDR; RFC en sieje.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py sivir` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py sivir` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
