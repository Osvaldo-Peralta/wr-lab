---
tags: [wrlab, ficha, norra]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Norra
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — NORRA (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** Mid. Siege-mage: waveclear y zone-denial de objetivos.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Artillera de Yordle con mortero: daño en área y control de zona a distancia absurda.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** MID S WR 51.21 % (pick 1.50 %, ban 7.62 %, Confidence Low).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- Sin cambios directos en 7.3/7.3a: su balance vive en cambios sistémicos (crit 200 %, AS cap 3.0, torretas 7 000 HP).

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| HP base (growth) | — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| Armadura / RM | — (fuera del JSON del lab: ver wiki/ficha del autor) / — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| AS 7.3 | ratio 0.625 · base 0.625 · BBA 0.2 · growth 0.012 | champion_attack_speed_7.3.csv |
| Rango de ataque | 550 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Q mortero en área grande: waveclear y poke de sieje.
- W trampa/slow de zona: control de embudos.
- E escudo/dash defensivo con daño.
- R mega-mortero global en zona: objetivo-toma y teamfight.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Pico 2-3 ítems de AP+ hache; sostenida en sieje.
- Mid. Siege-mage: waveclear y zone-denial de objetivos.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **R en objetivos épicos antes del engage: zona negada.**
2. **Q sobre la ola + campeones: value doble.**
3. **W en retiradas propias del equipo.**

**Sinergias/counters:** Comps de sieje lento; counter de engages rápidos que cierran su distancia.

## 6. LEYES QUE LA GOBIERNAN

- AP de zona: haste+AP; sin crit.
- Ley 0.

## 7. DIRECCIÓN DE BUILD

- Luden → shadowflame → cap genio; morellonomicon vs heal.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py norra` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py norra` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
