---
tags: [wrlab, ficha, heimerdinger]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Heimerdinger
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — HEIMERDINGER (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** Mid. Zone-control: el dragón/herald se pelea en su terreno.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Mago de asedio con torretas: convierte zonas en territorio propio y gana guerras de objetivo estático.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** MID A WR 50.16 % (pick 1.70 %, ban 1.23 %, Confidence Low).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- Sin cambios directos en 7.3/7.3a: su balance vive en cambios sistémicos (crit 200 %, AS cap 3.0, torretas 7 000 HP).

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | 54 (3.5) | champion_base_stats.json |
| HP base (growth) | 600 (120) | champion_base_stats.json |
| Armadura / RM | 34 (5) / 40 (1.2) | champion_base_stats.json |
| AS 7.3 | ratio 0.625 · base 0.625 · BBA 0.2 · growth 0.01 | champion_attack_speed_7.3.csv |
| Rango de ataque | 550 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Torretas (Q): daño persistente que escala con AP y se potenciaban en zona.
- Granada (E) stun en área + carga torretas: setup.
- W cohetes en cono: burst a quemarropa o poke lejano.
- R ult de torreta gigante o upgrade de kit: objetivo-toma.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Fuerte desde 2 ítems en objetivos estáticos; débil en pelea móvil.
- Mid. Zone-control: el dragón/herald se pelea en su terreno.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **Torretas en arbustos de río: visión + daño gratis.**
2. **E sobre el path de escape, no al centro.**
3. **Push lateral con torretas mientras el equipo agrupa.**

**Sinergias/counters:** Comps de siege (caitlyn-like); counter de asesinos de dash que borran torretas.

## 6. LEYES QUE LA GOBIERNAN

- AP de zona: haste + AP bruto; sin crit.
- Ley 0 en builds de 6 slots como todos.

## 7. DIRECCIÓN DE BUILD

- Luden → shadowflame → cap genio; liandry vs comps de HP.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py heimerdinger` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py heimerdinger` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
