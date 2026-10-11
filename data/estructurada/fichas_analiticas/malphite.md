---
tags: [wrlab, ficha, malphite]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Malphite
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — MALPHITE (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** Top o Support. Draft-win vs comps físicos.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Tanque de anti-AD absoluto: su armadura escalada convierte builds físicas en daño decorativo.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** SUPPORT S WR 51.07 % (pick 7.53 %, ban 42.85 %, Confidence Med) · SOLO S+ WR 55.55 % (pick 7.24 %, ban 42.85 %, Confidence Med).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- 7.3a · NERF: W ratio de armadura 20→**15 %** · E ratio de armadura 45→**40 %** · R CD 75/70/65→**85/80/75 s**

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| HP base (growth) | — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| Armadura / RM | — (fuera del JSON del lab: ver wiki/ficha del autor) / — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| AS 7.3 | ratio 0.638 · base 0.638 · BBA 0.25 · growth 0.04 | champion_attack_speed_7.3.csv |
| Rango de ataque | 125 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Pasiva de escudo por %max HP que regenera fuera de combate.
- Q roba AS: debuff doble (tu daño + su DPS menor).
- E ground slam: daño reducido por tu armadura + AS down en área.
- R engage global imparable: el pick más limpio del juego.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Item-spike por pieza de armadura; pico con 2-3 piezas vs AD.
- Top o Support. Draft-win vs comps físicos.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **R sobre el carry AD con follow-up aliado: no lo gastes en poke.**
2. **E en cada teamfight: el AS-down gana trades gratis.**
3. **Q al hypercarry enemigo antes del engage.**

**Sinergias/counters:** Follow-ups de área (yasmal/aoe-mages); counter de AP burst y pen mágica.

## 6. LEYES QUE LA GOBIERNAN

- Tanque: HP+armor multiplican su E; sin crit.
- Ley 0; presupuesto de tanque ≠ DPS.

## 7. DIRECCIÓN DE BUILD

- Iceborn/sunfire → thornmail → fuerza natural vs AP.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py malphite` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py malphite` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
