---
tags: [wrlab, ficha, syndra]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Syndra
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — SYNDRA (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** Mid. Burst-comp: ejecuta carries con combo completo.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Maga de burst por esferas: el daño escala con el tiempo de lane acumulado en orbes.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** MID S WR 50.86 % (pick 6.51 %, ban 21.08 %, Confidence Med).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- 7.3a · NERF: Nodos de pasiva 40/60/80/100/120→**50/75/100/125/150** · W ratio 60→**50 %** · slow fijo **25 %**

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | 54 (3) | champion_base_stats.json |
| HP base (growth) | 630 (120) | champion_base_stats.json |
| Armadura / RM | 34 (4.5) / 36 (1.2) | champion_base_stats.json |
| AS 7.3 | ratio 0.625 · base 0.625 · BBA 0.2 · growth 0.015 | champion_attack_speed_7.3.csv |
| Rango de ataque | 550 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Esferas acumuladas: todo el kit consume/produce orbes (escalado por minutos).
- Q create + W grab/throw: burst de zona.
- E knockback que empuja esferas: stun en línea.
- R ejecución con todas las esferas: el unitario más grande del mid.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Escalado por stacks de pasiva; pico 3 ítems con R de 6+ esferas.
- Mid. Burst-comp: ejecuta carries con combo completo.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **Acumula esferas antes del all-in (no gastes Q gratis).**
2. **E con 2-3 esferas delante: stun de área.**
3. **R solo con execute garantizado: sin desperdicio.**

**Sinergias/counters:** Junglas de follow-up burst; counter de cleansers y spell-shields.

## 6. LEYES QUE LA GOBIERNAN

- AP burst: shadowflame/cap; pen mágica vs frontline.
- Ley 0.

## 7. DIRECCIÓN DE BUILD

- Luden/shadowflame → horizon → cap genio; zhonya vs dive.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py syndra` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py syndra` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
