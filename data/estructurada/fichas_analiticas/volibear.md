---
tags: [wrlab, ficha, volibear]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Volibear
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — VOLIBEAR (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** Top o Jungla. Frontline que amenaza carries con E de execute blando.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Juggernaut de tormentas: dives de torre gratuitos con R y duelos de on-hit sostenido.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** SOLO A WR 48.25 % (pick 5.03 %, ban 4.51 %, Confidence Med) · JUNGLE B WR 48.31 % (pick 2.34 %, ban 4.51 %, Confidence Low).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- Sin cambios directos en 7.3/7.3a: su balance vive en cambios sistémicos (crit 200 %, AS cap 3.0, torretas 7 000 HP).

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | 62 (56) | champion_base_stats.json |
| HP base (growth) | 660 (120) | champion_base_stats.json |
| Armadura / RM | 46 (4.71) / 38 (2) | champion_base_stats.json |
| AS 7.3 | ratio 0.7 · base 0.7 · BBA 0.05 · growth 0.014 | champion_attack_speed_7.3.csv |
| Rango de ataque | 150 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Pasiva de on-hit en área creciente: pelea sostenida y clear.
- Q dash con stun: engage y chase.
- W mordisco doble con execute blando y heal.
- E rayo en zona: daño + escudo propio.
- R transform: HP + rango + dive de torreta sin daño.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Fuerte 1-2 ítems; R hace objetivos tempranos casi gratis.
- Top o Jungla. Frontline que amenaza carries con E de execute blando.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **R bajo torreta enemiga: dive sin castigo.**
2. **W segundo mordisco como execute en duelos.**
3. **E sobre tu posición al ser kiteado: escudo + zona.**

**Sinergias/counters:** Comps de dive coordinado; counter de kiting de rango y grievous.

## 6. LEYES QUE LA GOBIERNAN

- Juggernaut on-hit: blade/wit's del pool; sin crit.
- Ley 0.

## 7. DIRECCIÓN DE BUILD

- Blade → sunfire/iceborn → spirit visage; gunmetal si on-hit puro.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py volibear` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py volibear` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
