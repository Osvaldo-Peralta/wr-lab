---
tags: [wrlab, ficha, yunara]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Yunara
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — YUNARA (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** ADC. Nuevo arquetipo del lab: spread de Q y crítico interactúan (aproximado).
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Marksman híbrida de tormentas: crítico + on-hit mágico con movilidad de viento.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** DUO S+ WR 51.67 % (pick 15.97 %, ban 23.02 %, Confidence High).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- Sin cambios directos en 7.3/7.3a: su balance vive en cambios sistémicos (crit 200 %, AS cap 3.0, torretas 7 000 HP).

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | 58 (3) | champion_base_stats.json |
| HP base (growth) | 600 (128) | champion_base_stats.json |
| Armadura / RM | 35 (4.5) / 30 (1.43) | champion_base_stats.json |
| AS 7.3 | ratio 0.65 · base 0.65 · BBA 0.23 · growth 0.032 | champion_attack_speed_7.3.csv |
| Rango de ataque | 550 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Q de abanico con spread que escala con AS/crit (modelado aproximado).
- W dash de viento con slow: kiting y reposición.
- E escudo/amp de on-hit por ventana.
- R tormenta en área: zone-denial de teamfight.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Escalado doble (crit+on-hit): pico 3 piezas.
- ADC. Nuevo arquetipo del lab: spread de Q y crítico interactúan (aproximado).

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **Dash lateral con W tras cada rafaga.**
2. **R en objetivos: la zona fuerza fights a tu favor.**
3. **On-hit y crit se apilan: builds híbridas legales.**

**Sinergias/counters:** Enchanters de AS (censer); counter de burst inmediato que cierra su ventana.

## 6. LEYES QUE LA GOBIERNAN

- Ley 1 con umbral híbrido; Ley 3b en pen física.
- Spread de Q NO modelado exacto (⚠️ declarado).

## 7. DIRECCIÓN DE BUILD

- Gunmetal + on-hit/crit mixto según comp (motor autos).
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py yunara` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py yunara` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
