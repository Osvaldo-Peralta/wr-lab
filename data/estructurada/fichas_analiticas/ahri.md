---
tags: [wrlab, ficha, ahri]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Ahri
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — AHRI (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** Mid. Pick-comp: gana con charm landeados, no con waveclear.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Assassin-mage de picks: charme + burst móvil; el ult de 3 dashes la hace imposible de fijar.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** MID A WR 50.52 % (pick 4.26 %, ban 0.12 %, Confidence Med).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- Sin cambios directos en 7.3/7.3a: su balance vive en cambios sistémicos (crit 200 %, AS cap 3.0, torretas 7 000 HP).

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | 52 (3.6) | champion_base_stats.json |
| HP base (growth) | 630 (120) | champion_base_stats.json |
| Armadura / RM | 34 (4.5) / 36 (1.2) | champion_base_stats.json |
| AS 7.3 | ratio 0.625 · base 0.625 · BBA 0.2 · growth 0.02 | champion_attack_speed_7.3.csv |
| Rango de ataque | 550 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Charme (E) = setup de todo el burst; falla E, falla el trade.
- Ult con 3 dashes + kill reset: movilidad defensiva y offensiva.
- Q ida/vuelta con daño verdadero en el regreso: poke barato.
- W orbitales: burst de cercana sin skillshot.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Pico 2-ítems (Luden/Shadowflame); decae vs frontlines tanque.
- Mid. Pick-comp: gana con charm landeados, no con waveclear.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **Charme → Q+W+auto con pasiva de MS para reposicionar.**
2. **Ult como herramienta de escape aunque no haya kill.**
3. **Roam lateral con MS de pasiva tras 2 hits.**

**Sinergias/counters:** Sinergia con junglas de CC (setup de charme); counter de asesinos de dash (poppy-like) y QSS temprano.

## 6. LEYES QUE LA GOBIERNAN

- Ley de burst: el combo debe matar al carry en 2.5 s o retirarse.
- Sin crit: AP pura; Leyes 0/3 aplican a su build de pen mágica.

## 7. DIRECCIÓN DE BUILD

- Luden/Shadowflame → horizon u odio eterno vs tanques; zapatos sorc → cap genio.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py ahri` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py ahri` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
