# HOTFIX 7.3d — Cambios completos (publicado: 28-oct-2026, 09:00 UTC)

> **Fuente:** notas oficiales EN (wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-7-3d/), leídas directamente el 06-nov-2026.
> **Estado en el lab:** APLICADO (v1.22) a `champion_attack_speed_7.3.csv` (vía `OVERRIDES_73D` en `extract_data.py`), `items_7.3.csv`, `dps_model.py`, `xayah_model.py`, `yunara_model.py`, `analysis_batch2.py`, `yuumi_agresiva_model.py`, `champspecs.py`, `champion_base_stats.json` y `ESCALADO_DE_TAMANIO.md`. Base previa: 7.3+7.3a+7.3b (v1.21).
> **Formato:** igual que `cambios_7.3b.md` (insumo de `update_reports.py`).

## REGISTRO DE 7.3c Y 7.3e (sin impacto en Summoner's Rift)

| Parche | Fecha | Contenido | Acción en el lab |
|---|---|---|---|
| 7.3c | 21-oct-2026 | Solo **AAA ARAM**: 4 augments nuevos (Chromacrash, Quick Reflexes, Back to Basics, Origin: Grasp of the Undying), 10 ajustes de augments, y modificadores de daño de modo para Jarvan IV, Taliyah, Ryze, Kayn, Vladimir | Excluido (el lab es solo SR). Registrar en FUENTES |
| 7.3e | 04-nov-2026, 10:00 UTC | Solo **AAA ARAM**: 6 augments nuevos (series K/DA, Star Guardian, Minion + Mimicking Sands, Arcane Shadow, All in Good Fun). Sin ajustes de campeones, ítems ni números | Excluido. Registrar en FUENTES |
| 7.3d | 28-oct-2026 | Balance de SR (campeones, ítems, Barón, minions, torretas) + ajustes de augments ARAM | **Aplicar** (abajo) |

Los hotfixes 7.3c y 7.3e no obligan a re-triar reportes. El estado de datos pasa a **7.3+7.3a+7.3b+7.3c+7.3d+7.3e**, con c y e sin cambios de SR.

## CAMPEONES

| Campeón | Tipo | Cambio |
|---|---|---|
| **Shyvana** | MIXTO | Base: HP/nivel 120→**130**, regen/nivel 9→**12**, **AS/nivel 0.012→0.024**. Twin Bite CD 8.5/7.5/6.5/5.5→**7/6.5/6/5.5 s**. Burnout CD 13/12/11/10→**12/11/10/9 s**; Wings of the Cloud MS 25→**15 %**. Flame Breath CD 11/10/9/8→**10/9/8/7**; ratio 30 % AD+40 % AP→**50 % AD+80 % AP**; detonación forma dragón 50 % AD+70 % AP→**100 % AD+100 % AP**; scorched earth ratio AD 10→**15 %**. Dragon's Descent: omnivamp Life of the Ocean 20→**10 %** |
| **Camille** | BUFF | AS/nivel 0.016→**0.028** |
| **Malphite** | NERF | Granite Shield: ratio vida máx 11→**10 %**. Thunderclap primer golpe: daño base 40/60/80/100→**30/45/60/75**; ratio de armadura 30→**20 %** |
| **Ekko** | NERF | Z-Drive Resonance vs monstruos 120→**110 %**; Timewinder vs monstruos 115→**100 %** |
| **Lee Sin** | BUFF | AS/nivel 0.02→**0.04**; Dragon's Rage base 125/350/575→**150/375/600** |
| **Akali** | BUFF | AS/nivel 0.02→**0.04**; armadura base 34→**37** |
| **Nasus** | MIXTO | AD base 58→**62**; Spirit Fire base 55/110/165/220→**50/90/130/170**; Fury of the Sands RA/RM 40/50/60→**40/55/70** |
| **Samira** | NERF | Flair ratio AD 125→**115 %**; Inferno Trigger ratio AD 50→**45 %** |
| **Ashe** | NERF | Frost Shot, daño bonus de autos 0~130 %→**0~123.5 %** (según crit) |
| **Miss Fortune** | BUFF | Love Tap multiplicador de AD bonus 40→**50 %**; Bullet Time crit 130~139 %→**135~145.5 %** (según crit) |
| **Singed** | NERF | HP 690→**660**; MS 355→**350**; Mega Adhesive CD 11→**14/13/12/11 s**; Fling CD 12→**13 s** |

## ÍTEMS (aplicar a items_7.3.csv, §8 del bundle y `dps_model.py`)

| Ítem | Cambio |
|---|---|
| **Fiendhunter Bolts** | Opening Barrage: crit normal 80→**85 %**; daño verdadero 15→**17.5 %** |
| **Divine Sunderer** | precio 3 400→**3 300** |
| **Essence Reaver** | AD 50→**55** |
| **Whispering Circlet** | Heal and Shield Power 8→**6 %** |
| **Diadem of Songs** | Heal and Shield Power 8→**6 %** |
| **Stormrazor** | Bolt: daño 120→**100**; MS 45→**35 %** |

## MAPA Y SISTEMAS

| Sistema | Cambio |
|---|---|
| **Hand of Baron** | Reducción de daño de minions vs campeones: melee/caster 50-70→**55-75 %**; cañón/siege 30→**35 %**. Vs minions: melee 80→**90 %**, otros 20→**25 %** (excepto super minion). Vs torretas 25→**30 %** (excepto super minion) |
| **Minions (ventaja de empuje)** | Sube la reducción de daño de minions del equipo que va ganando. **⚠️ El texto oficial extraído NO trae las cifras** — verificar en la nota original antes de registrar números |
| **Torretas** | Multiplicador por ataques consecutivos 100/150/215/300 %→**100/150/210/270 %** |
| **ARAM** | Ajustes a Violet Toxin, Chromacrash Series, Rhythm Hunter, Red-Blue Remix, Transmissible Agents, Crimson Burst: excluidos del lab. Skins K/DA Ahri: sin efecto |

## APLICADO EN EL LAB

- `extract_data.py`: `OVERRIDES_73D` (Shyvana 0.024, Camille 0.028, Lee Sin 0.04, Akali 0.04) y `champion_attack_speed_7.3.csv` con marca `(7.3d: era …)`.
- `items_7.3.csv`: Divine Sunderer 3 300 · Essence Reaver +55 AD · Circlet/Diadem HSP 6 % · Stormrazor Bolt 100 / MS 35 % · Fiendhunter 85 % / 17.5 %. (`items_7.3.md` y `data/raw/wrmeta_items.html` siguen en el estado 7.3: re-ejecutar `extract_data.py` NO toca el CSV de ítems.)
- Motores: `storm` energized 100 y `er` AD 55 en `dps_model.py`, `xayah_model.py`, `yunara_model.py`; HSP 6 en `analysis_batch2.py` y `yuumi_agresiva_model.py`. `yunara_model.py` conserva el supuesto amortizado de Opening Barrage (13) sin reescalar.
- `champspecs.py`: Shyvana `as_per_lvl` 0.024; notas de Malphite con 7.3d.
- `champion_base_stats.json` (Shyvana): HP/nivel 130 y AS 7.3d. Regen 9→12 NO se aplicó: el campo de wr-meta ("9 (0.9)") no permite saber si «per level» de la nota es base o crecimiento.
- `metodologia/ESCALADO_DE_TAMANIO.md`: Malphite según el hotfix (escudo 10 %, W primer golpe 30/45/60/75 + 20 % armadura).

## DISCREPANCIAS A REGISTRAR EN data/FUENTES.md

1. **Malphite, primer golpe de W:** el apéndice del lab traía 40 % de armadura; la nota 7.3d declara 30 %→20 %. **Regla aplicada: manda la fuente oficial** — el apéndice y los números derivados se rehicieron con 30/45/60/75 + 20 %.
2. **Minions:** la nota oficial describe el cambio de ventaja de empuje sin cifras; no modelado, sin impacto en motores.
3. **Shyvana:** el texto oficial describe subidas de ratio en Flame Breath mientras la intención declarada es recortar su fuerza a pleno escalado. Transcrito tal cual está publicado.
4. **Regen de Shyvana (wr-meta):** ver «Aplicado en el lab».

## IMPACTO EN REPORTES/SPECS DEL LAB (hipótesis previa al triage)

| Archivo | Exposición | Veredicto probable |
|---|---|---|
| `Caitlyn` | Ruta con Stormrazor a los 8' y Essence Reaver | ⚠️ REVISAR |
| `Yuumi` (×2) | HSP −2 pts en Circlet/Diadem; precedente 7.3a: −5 % de input → −1.4 % de resultado | ⚠️ REVISAR o ✅ ANOTAR |
| `Xayah` | Stormrazor alternativa (−1.8 % a nivel 15), ER; Fiendhunter sigue ❌ por Ley 1 | ✅ ANOTAR o ⚠️ |
| `Sivir` | Stormrazor alternativa (+9 % 1v1 / −14 % 3v3) empeora | ✅ ANOTAR |
| `Senna` | Essence Reaver +5 AD (buff) | ✅ ANOTAR |
| `Yunara`, `Nocturne` | Fiendhunter/Stormrazor/Divine Sunderer ya rechazados; el precio o el buff no cambia el veredicto | ✅ SIN_IMPACTO |
| `Jinx` y resto (Kalista, Diana ×2, Cho'Gath ×2, Mordekaiser, Norra, Ornn, Rammus, Seraphine, Heimerdinger, Volibear ×2) | Sin ítems ni campeones tocados; Malphite, Ashe y Samira solo como referencia en texto (Jinx cita a Malphite 9 veces: revisar cifras citadas) | ✅ SIN_IMPACTO |
| `Shyvana` (spec) | Sin reporte publicado en el bundle; AS/nivel ×2 y cambios de kit | Regenerar en `_auto/` si se quiere reporte |

## CHECKLIST (FRAMEWORK §E)

1. ✅ Notas 7.3c/7.3d/7.3e leídas de la fuente oficial (06-nov-2026). Pendiente: guardar `data/raw/patch73d.txt` y re-descargar `wrmeta_items.html` (requiere red fuera del sandbox).
2. ✅ Datos y motores (ver arriba).
3. ⏳ `python3 wrlab.py winrates` (win rates tras 7.3d) — local con red.
4. ✅ Este archivo en `data/estructurada/`; falta anotar 7.3c/7.3d/7.3e en `data/FUENTES.md`.
5. ✅ Triage/refresh/annotate/baseline ejecutados (ver commit siguiente).
6. ✅ Tests, bundles y BD regenerados.
7. ⏳ Revisar slugs vigilados en `check_patch.py` (siguiente: 7.3f / 7.4) y el pie de los reportes.
