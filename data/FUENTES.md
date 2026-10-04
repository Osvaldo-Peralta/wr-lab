# FUENTES — Registro de datos y verificación

**Última actualización del lab:** 1 de octubre de 2026 · **Parche base:** 7.3 (lanzado 21-sep-2026) + **hotfix 7.3a** (despliegue 29-sep-2026)

## Registro de verificaciones de parche

| Fecha | Verificación | Resultado | Evidencia |
|---|---|---|---|
| 29/09/2026 | ¿Hotfix nuevo tras 7.3a? (`check_patch.py` + inspección manual) | **NO.** Sin páginas 7.3b/7.4 (404 en todos los slugs); changelogs wr-meta de centinelas sin cambios (22-sep, 7.3); la página oficial 7.3 tiene **contenido idéntico** al snapshot del 28-sep — el md5 crudo difería solo por ruido dinámico (carrusel de "artículos relacionados" y token `mappersVersion` del CMS). Cero menciones de hotfix/7.3a/7.3b/7.4 en la página EN | `data/raw/patch73_0929.html` (diff vs `patch73_0928.html`: 1 línea de metadata CMS; texto del artículo: 2 497 líneas idénticas) |
| 29/09/2026 | Falso positivo del vigía | `check_patch.py` v1.6: el hash pasa a ser de **contenido normalizado** (texto del artículo cortado antes del pie dinámico), no del HTML crudo | `.watch_state.json` con `official_73_content_md5` |
| 29/09/2026 | Reportes publicados vs 7.3a (set original de 5) | `update_reports.py triage --patch 7.3a`: 5/5 ✅ ANOTAR (ninguno requiere regeneración). Yuumi: Δ resultado −1.4 % (E-shield/R-heal) pese a HSP −5 % (input) | Commit v1.6 (bloques `WRLAB-VERIF:7.3a` + `reportes_registry.json`) |
| 29/09/2026 | Vault externo integrado (16 reportes sustituyen a los 5 del lab, commit 163d9bc) | Re-triage 7.3a del vault: **Caitlyn ❌ y Rammus ❌ REGENERAR** (7.3a tocó inputs de su spec: AS growth / armadura base — sus reportes declaran datos 7.3), **Yuumi ⚠️ REVISAR** (nerf W sin hook para la build poke-híbrida: Stormsurge/Harmonic Echo fuera del modelo), 13 ✅ ANOTAR/SIN IMPACTO | Bloques `WRLAB-VERIF:7.3a` en los 16 reportes + registro |
| 29/09/2026 | Validación cruzada del optimizador (`optimize_build.py`) | ✅ **Redescubre la build C de Jinx** dentro del pool de candidatos del reporte (Leyes 1+3 duras, 3 042 dps1). Pool completo post-7.3a: `Gunmetal+C44+Terminus+YunTal+LDR+IE` supera a C ~7 % en eficiencia ponderada normalizada (supuestos: Yun Tal a rampa máxima 125 ataques, Terminus a stacks) — **hallazgo registrado, reporte publicado intacto** (Regla de Oro) | ROADMAP.md §Hallazgos del optimizador |
| 29/09/2026 | **Nota EN oficial de 7.3a publicada** (detectada por check_patch.py en vivo) | Descargada y verificada número por número contra `cambios_7.3a.md` (traducción CN): **todo coincide** — specs/motor/tests del lab quedan confirmados contra fuente primaria. Discrepancia menor registrada: Crown of Songs (ver §Discrepancias). wr-meta indexó changelogs "30 SEP 2026 (7.3A)" en Yuumi/Malphite | `data/raw/patch73a_en.html/.txt` |
| 01/10/2026 | **Win rates integradas al vigía** (v1.11, petición del autor: "dato vital siempre actualizado") | `check_patch.py` paso 4: bloque Meta Overview de wr-meta (bucket Diamond+) para el roster (17 campeones = 16 reportes + 13 specs, ampliado por el registro); escribe `champion_winrates.csv/.md`, alimenta la tabla `winrates` de la BD y el §7b de los bundles; alerta si |Δ win rate| ≥ 2 pts; el lint avisa si el callout meta de un reporte diverge >3 pts. Siembra en vivo: 17 campeones · 22 filas · "Updated: 01 OCT 2026 UTC 00:00". IDs verificados contra home + sitemap.xml de wr-meta (descubiertos: caitlyn 317, sivir 394, norra 552, rammus 242, hwei 505) | `data/estructurada/champion_winrates.csv`, `.watch_state.json` (secciones `winrates`/`wrmeta_ids`) |
| 29/09/2026 | Bundles regenerables | `WR-LAB_lite.md` (176 KB) y `WR-LAB_completo.md` (836 KB) regenerados desde las fuentes con los 16 reportes del vault + módulos nuevos (optimizador §10c, batch2 §10b, actualizador §17b, infra §18); CI verifica sincronía (`build_bundles.py --check`) | `model/build_bundles.py` |

## Hotfix 7.3a (29-sep-2026)

| Fuente | Acceso | Qué aporta | Fiabilidad |
|---|---|---|---|
| **Notas oficiales EN 7.3a (FUENTE PRIMARIA)** — wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-7-3a/ | 29/09/2026 (`data/raw/patch73a_en.html/.txt`) | Confirmación oficial de todos los valores: Hwei, Samira, Rammus, Malphite, Tristana, Draven, Caitlyn, Senna, Syndra, Swain, Yuumi, Viego · Yun Tal (AS 35, Flurry 35/CD 25) · Whispering Circlet + **Diadem of Songs** (Harmony 0.25 %) · Death's Dance 3300 · Smite 22-162 · Nexus 4000 · placas +20/10 s · AAA ARAM | **Definitiva** — verificación número por número contra la traducción CN: ✅ todo coincide |
| Notas oficiales CN (lolm.qq.com docid 15413436308828016227) vía traducción comunitaria r/wildrift (thread 1wskk84), recuperada por Arctic Shift API | 28/09/2026 (`data/raw/patch73a_cn_en.txt`, diff completo en `data/estructurada/cambios_7.3a.md`) | Nerfs: Hwei, Rammus, Malphite, Caitlyn, Senna (ajuste), Syndra, Yuumi · Buffs: Samira, Tristana, Draven, Viego · Yun Tal buff · Diadem/Circlet/Whispering nerf · Death's Dance 3300 · Smite burn −, Nexus 4000, placas −resist · ARAM | Alta — **✅ re-verificada contra la nota EN oficial el 29/09/2026**: números idénticos; única desviación: EN lista solo Diadem of Songs (la CN decía Crown/Diadem). wr-meta ya indexa changelogs 7.3A (30-sep) |

## Fuentes primarias (MANDAN sobre cualquier otra)

| Fuente | URL | Acceso | Qué aporta |
|---|---|---|---|
| Notas oficiales Wild Rift 7.3 | wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-7-3/ | 25/09/2026 (HTML completo, 646 KB → `data/raw/patch73.html/.txt`) | Sistema de crítico 200/230 %, nuevo sistema de AS + tope 3.0, apéndice de AS de los 140 campeones, todos los cambios de ítems/runas/campo, nerfs de Jinx, fórmula oficial de AS con ejemplo de Caitlyn |
| Notas oficiales Wild Rift 7.2 | wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-7-2/ | 25/09/2026 (`data/raw/patch72.txt`) | Fin de los encantamientos de botas; QSS/Mercurial Scimitar/Galeforce como ítems de clase; botas Tier 2/T3 y regla del minuto 10:00 |

## Fuentes secundarias (solo para lo que las notas no tocan)

| Fuente | URL | Acceso | Qué aporta | Fiabilidad |
|---|---|---|---|---|
| wr-meta.com/items | wr-meta.com/items/ | 25/09/2026 (`data/raw/wrmeta_items.html`, 510 KB) | Stats completos y precio de los 186 ítems únicos (incluye nuevos de 7.3), pasivas, botas T2/T3, runas | Alta: incluye ítems 7.3; desfasada en runas removidas (lista Ingenious Hunter) y texto viejo de Lethal Tempo |
| wr-meta.com Jinx | wr-meta.com/39-jinx.html | 25/09/2026 (`data/raw/wrmeta_jinx.html/.txt`) | Stats base de Jinx (58 AD/630 HP/335 MS/575 rango), valores por habilidad, change history completo, build popular y meta (WR 49.82 %, pick 10.97 %, Diamond+, 24/09) | Alta para números de kit; la build popular es insumo, no conclusión |
| wr-meta.com — Meta Overview (win rates) | wr-meta.com/{id}-{champ}.html (bloque `wrCnFsSnapWrap`) + sitemap.xml para ids | vivo, 2×/día vía `check_patch.py` paso 4 (`champion_winrates.csv/.md`) | Win/pick/ban/trend + tier y confianza por rol, bucket Diamond+ (select por defecto de la página) | Contexto meta (secundaria): no decide builds; para callouts de reportes y detección de movimientos ≥ 2 pts |
| wr-meta.com — 11 fichas del equipo | wr-meta.com/{id}-{champ}.html (yuumi 321, yunara 545, mordekaiser 365, kalista 349, diana 216, karma 323, heimerdinger 346, volibear 411, seraphine 34, shyvana 23, chogath 339) | 25/09/2026 (`data/raw/campeones/*.html` → `data/estructurada/campeones/*.md` + `champion_base_stats.json`) | Stats base, habilidades con valores, change history y builds populares de los 11 campeones del roster | Alta en general; ⚠️ Volibear muestra ad_growth "56" (errata probable — verificar); el rango de ataque no se publica (verificar Kalista/Yunara en juego) |

## Fuentes intentadas y descartadas (para no repetir el trabajo)

- **wildrift.wiki** — DNS muerto al 25/09/2026 (no resuelve ni desde el sandbox ni desde los proxies de lectura).
- **leagueoflegends.fandom.com / wild-rift.fandom.com** — 403 al acceso directo; la página `Jinx_(Wild Rift)` no existe en la wiki principal de LoL.
- **reddit.com (PBE 7.2 preview)** — 403/bloqueado; usado solo como pista corroborada después contra las notas oficiales 7.2.
- **wildstats.gg / u.gg/wr / mobalytics.gg/wr** — apps JS sin contenido estático útil o 403.
- **op.gg/wild-rift** — 404 en la ruta probada.

## Discrepancias detectadas y regla de resolución aplicada

| Tema | Fuente A | Fuente B | Resolución |
|---|---|---|---|
| Lethal Tempo (valores ranged) | wr-meta: 4.8 %/stack, bala 6–20, +0.33 %/1 % AS | Notas 7.3: **6.4 %/stack, bala 6–24, +0.67 %/1 % AS** | Mandan las notas oficiales |
| Legend: Alacrity | Descripción wr-meta: 3 % + hasta 18 % (=21 %) | Ejemplo oficial Caitlyn 7.3: "18 % a full stacks" | Modelo usa 21 % (peor caso para el tope de AS); diferencia de DPS < 1 % |
| Noxian Gait (Gunmetal) | Notas 7.2: 15 %/10 % MS | wr-meta post-7.3: 10 %/7 % | wr-meta (posterior al reajuste global de MS 5→4 %) |
| Ingenious Hunter | wr-meta la lista | Notas 7.3: **REMOVIDA** | Removida |
| Berserker's Greaves AS | Notas 7.2: 30 % | wr-meta + ejemplo oficial Caitlyn 7.3: **35 %** | 35 % |
| 7.3a: Crown of Songs (Harmony) | Traducción CN: "Crown/Diadem of Songs" nerfeadas | Nota EN oficial: solo **Diadem of Songs** + Whispering Circlet | Mandan las notas EN: el nerf listado es de Diadem; si Crown of Songs comparte la pasiva Harmony, heredaría el valor en juego — verificar en tienda antes de publicar análisis de enchanter que use Crown |
| Exclusividad de ítems de penetración % | Modelo del lab: pen % de ítems se SUMA (LDR 35 + Mortal 30 = 65) y nada en wr-meta/notas 7.3/7.3a documenta restricciones | **Juego (verificado por el autor, 03/10/2026):** Lord Dominik's Regards, Mortal Reminder y Terminus NO pueden convivir en la misma build | Manda el juego: `data/estructurada/items_exclusivos.csv` (grupo `pen_pct`) lo hacen cumplir validate_slots/optimizador/lint. Hallazgos previos con doble pen (Jinx 29/09) CORREGIDOS en ROADMAP; la variante anti-tanques de Jinx.md v1.4 quedó ilegal — corrección pendiente del autor |
| ⚠️ Caitlyn Base Bonus AS | Notas 7.3 §CAITLYN y ejemplo de la fórmula: **0.28** | Apéndice final de las mismas notas: **0.2** | **Inconsistencia interna de Riot.** Usar 0.28 (sección del campeón + ejemplo oficial) y verificar en el panel del juego antes de publicar cualquier análisis de Caitlyn. El CSV `champion_attack_speed_7.3.csv` replica el apéndice (0.2) — corregir manualmente si se confirma 0.28 |

**Regla permanente:** notas oficiales > BD comunitaria sincronizada > guías/comunidad. Toda discrepancia nueva se anota aquí.

## Qué archivo deriva de qué

```
data/raw/patch73.html  ─┬→ data/raw/patch73.txt ─┬→ cambios_campeones_7.3.md
                        │                        ├→ cambios_items_7.3.md
                        │                        ├→ cambios_runas_7.3.md
                        │                        ├→ sistemas_campo_7.3.md
                        │                        ├→ mecanica_attack_speed_7.3.md
                        │                        ├→ champion_attack_speed_7.3.csv   (140 campeones)
                        │                        └→ champion_durability_7.3.csv     (51 campeones)
data/raw/patch72.txt   ───→ referencia del sistema de botas/encantamientos (leer §BOOTS)
data/raw/wrmeta_items.html ┬→ items_7.3.csv / items_7.3.md  (186 ítems)
                           └→ runas_7.3.md
data/raw/wrmeta_jinx.html  → spec de Jinx en model/dps_model.py + reporte
wr-meta.com/{id}-{champ}.html (EN VIVO, vigía 2×/día — check_patch.py paso 4)
                        └→ champion_winrates.csv / champion_winrates.md (Diamond+)
                           └→ BD tabla `winrates` + bundle §7b + callouts meta de reportes
```
