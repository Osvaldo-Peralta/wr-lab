# FUENTES — Registro de datos y verificación

**Última actualización del lab:** 25 de septiembre de 2026 · **Parche base:** 7.3 (lanzado 21-sep-2026)

## Hotfix 7.3a (29-sep-2026)

| Fuente | Acceso | Qué aporta | Fiabilidad |
|---|---|---|---|
| Notas oficiales CN (lolm.qq.com docid 15413436308828016227) vía traducción comunitaria r/wildrift (thread 1wskk84), recuperada por Arctic Shift API | 28/09/2026 (`data/raw/patch73a_cn_en.txt`, diff completo en `data/estructurada/cambios_7.3a.md`) | Nerfs: Hwei, Rammus, Malphite, Caitlyn, Senna (ajuste), Syndra, Yuumi · Buffs: Samira, Tristana, Draven, Viego · Yun Tal buff · Diadem/Circlet/Whispering nerf · Death's Dance 3300 · Smite burn −, Nexus 4000, placas −resist · ARAM | Alta (texto oficial CN traducido; números con formato >>> coherentes). **Pendiente: re-verificar contra la nota EN cuando Riot la publique** y contra wr-meta cuando indexe (aún no lo hace al 28/09) |

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
```
