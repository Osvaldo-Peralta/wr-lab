---
tags: [wrlab, ficha, diana]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Diana
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — DIANA (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** Jungla o Mid. Dive-comp: entra una vez, decide la pelea.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Assassin-jungla de burst lunar: el dash al objetivo con root hace que su combo no falle una vez dentro.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** MID B WR 47.14 % (pick 1.10 %, ban 0.16 %, Confidence Low) · JUNGLE A WR 49.67 % (pick 1.45 %, ban 0.16 %, Confidence Low).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- Sin cambios directos en 7.3/7.3a: su balance vive en cambios sistémicos (crit 200 %, AS cap 3.0, torretas 7 000 HP).

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | 52 (3.64) | champion_base_stats.json |
| HP base (growth) | 630 (140) | champion_base_stats.json |
| Armadura / RM | 40 (5) / 38 (2) | champion_base_stats.json |
| AS 7.3 | ratio 0.694 · base 0.694 · BBA 0.15 · growth 0.008 | champion_attack_speed_7.3.csv |
| Rango de ataque | 150 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Q lunar marca → E dash reseteado sobre marcados: entrada garantizada.
- W escudo + orbitales que detonan: trades y clear.
- R pull en área + daño: teamfight win si entras segundo.
- Pasiva de autos con daño mágico en arco: clear y burst.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Pico 2-3 ítems; cae si el enemigo estira la pelea 30+ s.
- Jungla o Mid. Dive-comp: entra una vez, decide la pelea.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **Entrar post-CC aliado: R segundo, no primero.**
2. **Q antes de entrar: el reset de E es tu seguro de vida.**
3. **Clear con W+pasiva: rutas de 4 camps.**

**Sinergias/counters:** Follow-up de engages (Malphite-like); counter de zealots de QSS y peel duro.

## 6. LEYES QUE LA GOBIERNAN

- AP burst: shadowflame/cap genio; pen mágica según frontline (Ley 3 análoga).
- Ley 0 en builds; sin crit.

## 7. DIRECCIÓN DE BUILD

- Nashor/cinturón → shadowflame → cap genio o odio vs tanques.
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py diana` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py diana` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
