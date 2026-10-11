---
tags: [wrlab, ficha, jinx]
version: auto-1.0
Status: derivada (datos del lab 2026-10-11)
champion: Jinx
patch: "7.3+7.3a"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — JINX (Wild Rift 7.3+7.3a)

**Generada:** 2026-10-11 por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** ADC. Escalado puro: protegerla 20 min = ganar.
**Arquetipo lab:** ver tesis · `crit_dmg_mod` 1.0× (estándar)
**Tesis:** Hypercarry de resets: cada takedown regala MS+AS y convierte una kill en teamfight ganada.

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía 2026-10-09):** DUO A WR 50.69 % (pick 12.16 %, ban 0.46 %, Confidence High).

---

## 1. QUÉ LE HIZO ESTE PARCHE

- Sin cambios directos en 7.3/7.3a: su balance vive en cambios sistémicos (crit 200 %, AS cap 3.0, torretas 7 000 HP).

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| HP base (growth) | — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| Armadura / RM | — (fuera del JSON del lab: ver wiki/ficha del autor) / — (fuera del JSON del lab: ver wiki/ficha del autor) | champion_base_stats.json |
| AS 7.3 | ratio 0.625 · base 0.625 · BBA 0.3 · growth 0.02 | champion_attack_speed_7.3.csv |
| Rango de ataque | 575 | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | 1.0× (estándar) | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

- Q intercambiable: minigun AS o cohete AoE (112 % AD, splash).
- Pasiva Get Excited: +140 % MS y AS por 6 s tras takedown/objectivo.
- W slow + reveal; E trampas root en área.
- R global con daño por missing HP: ejecución cross-map.

## 4. CURVA DE PODER Y LECTURA DE ROLES

- Débil 0-8; imparable 3+ piezas con pow-pow activo.
- ADC. Escalado puro: protegerla 20 min = ganar.

## 5. PALANCAS DE SOBREEXPLOTACIÓN

1. **Cohete en teamfight, minigun en 1v1/objetivos.**
2. **Trampas en embudos de retirada propia.**
3. **R a carries bajos cross-map: oro y reset de pasiva.**

**Sinergias/counters:** Enchanter supports (lulu/yuumi-like) que la dejan viva al reset; counter de dive instantáneo.

## 6. LEYES QUE LA GOBIERNAN

- Ley 1: crit 100 % exacto (C44+Runaan+IE+LDR).
- Ley 2: AS cap 3.0 alcanzable con pow-pow+LT.
- Ley 3b: pen única.

## 7. DIRECCIÓN DE BUILD

- Gunmetal + C44 + Runaan + IE + LDR + Kraken (estándar v1.5 del reporte).
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py jinx` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py jinx` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
