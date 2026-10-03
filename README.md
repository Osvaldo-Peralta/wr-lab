# ⚗️ WR-LAB — Laboratorio de builds matemáticas para Wild Rift (parche 7.3)

Todo lo recabado y razonado en el análisis de **Jinx 7.3**, convertido en infraestructura reutilizable
para analizar **cualquier campeón** con el mismo rigor, sin depender de la memoria de un chat.

**Estado de datos:** parche 7.3 (21-sep-2026), verificados al 25-sep-2026.

---

## 📁 Mapa del laboratorio

```
wr-lab/
├── wrlab.py                           ← ⭐ CLI UNIFICADO + MENÚ INTERACTIVO (python3 wrlab.py)
├── README.md                          ← estás aquí
├── data/
│   ├── FUENTES.md                     ← URLs, fechas, discrepancias y reglas de resolución
│   ├── raw/                           ← HTML/texto crudo descargado (evidencia, no tocar)
│   │   ├── patch73.html/.txt          ← notas OFICIALES 7.3 completas
│   │   ├── patch72.txt                ← notas OFICIALES 7.2 (sistema de botas/encantamientos)
│   │   ├── wrmeta_items.html          ← BD de los 228 ítems (24-sep-2026)
│   │   └── wrmeta_jinx.html/.txt      ← ficha de Jinx + change history
│   └── estructurada/                  ← bases listas para consultar/reusar
│       ├── items_7.3.csv / .md        ← 186 ítems únicos: precio, stats, pasivas, categorías
│       ├── runas_7.3.md               ← keystones + 4 árboles, con advertencias 7.3
│       ├── champion_attack_speed_7.3.csv   ← ⭐ los 140 campeones: ratio/base/bonus/growth (apéndice oficial)
│       ├── champion_durability_7.3.csv     ← cambios de vida/armadura/RM del parche
│       ├── cambios_campeones_7.3.md   ← todos los ajustes de campeones (marksman y otros críticos)
│       ├── cambios_items_7.3.md       ← diff completo antes→después de cada ítem
│       ├── cambios_runas_7.3.md       ← LT rehecho, Legend: Haste, removidas
│       ├── cambios_7.3a.md            ← ⭐ diff estructurado del hotfix 7.3a (insumo de update_reports.py)
│       ├── sistemas_campo_7.3.md      ← jungla/smite, torretas 7000HP, cristales, minions, lifesteal
│       ├── mecanica_attack_speed_7.3.md ← fórmula oficial de AS + ejemplo de Caitlyn (test del modelo)
│       ├── reportes_registry.json     ← índice derivado: builds publicadas + golden metrics por reporte
│       └── champion_winrates.csv/.md  ← ⭐ win rates del roster (wr-meta Diamond+): las refresca
│                                          el vigía 2×/día en el mismo proceso que busca parches
├── model/
│   ├── extract_data.py                ← regenera data/estructurada/ desde data/raw/
│   ├── dps_model.py                   ← ⭐ motor de DPS parametrizado por campeón (engine + Jinx precargado)
│   ├── analysis_batch2.py             ← modelos batch: Kalista on-hit, Diana rotación, Yuumi/Karma valor-aliado, TAMAÑO
│   ├── update_reports.py              ← ⭐ triador de hotfixes sobre reportes publicados (anota, NO regenera)
│   ├── optimize_build.py              ← ⭐ optimizador exhaustivo (4 motores + presets defensa/utilidad)
│   ├── optimize_runes.py              ← ⭐ buscador de runas (keystone × secundaria, valor marginal)
│   ├── sim_timings.py                 ← ⭐ simulador de timings de oro (curvas derivadas del vault)
│   ├── lint_reportes.py               ← ⭐ linter de reportes del vault (ítems alucinados, Ley 0, estilo v1.4)
│   ├── generate_report.py             ← ⭐ auto-generador de reportes ("Espera de verificación" + aprobación)
│   └── backfill_frontmatter.py        ← backfill del contrato de datos (champion/slug/role/patch/custom/variant…)
│   └── build_bundles.py               ← regenera los bundles portables desde las fuentes (+ --check para CI)
├── metodologia/
│   ├── FRAMEWORK.md                   ← ⭐ las 7 Leyes + flujo de 10 pasos + arquetipos + protocolo de parche nuevo
│   ├── TEMPLATE_REPORTE.md            ← estructura exacta del reporte + checklist de calidad
│   └── ESCALADO_DE_TAMANIO.md         ← size scaling: Cho'Gath/Malphite/Shyvana
├── deploy/
│   ├── GITHUB_PAGES_QUARTZ.md         ← sitio público de guías (Quartz 5 + Pages): setup, bug del baseUrl y arreglo
│   ├── README_SITIO.md                ← personalización del sitio: tema minimalista + reglas de win rates
│   ├── PLAN_MIGRACION_VERCEL.md       ← plan del autor (Next.js + backend comunidad + Supabase, 8 fases)
│   └── quartz-theme/wrlab-minimal.css ← tema minimalista drop-in para el vault
└── reportes/                          ← 16 reportes del vault (29-sep-2026), cada uno con su
    │                                      bloque WRLAB-VERIF de verificación contra 7.3a:
    ├── Jinx.md · Caitlyn.md · Kalista.md · Yunana.md (Yunara) · Sivir.md      ← ADC
    ├── Diana - Jungla.md · Diana - Mid.md · Norra.md                          ← jungla/mid
    ├── Cho'Gath - Titán de la Jungla.md · Cho'Gath - Titán del Barón.md
    ├── Volibear Pesadilla.md · Mordekaiser.md · Rammus.md                     ← top/jungla
    └── Heimerdinger.md · Seraphine.md · Yuumi.md                              ← mid/support
```

📐 Apéndice transversal: `metodologia/ESCALADO_DE_TAMANIO.md` — todas las fuentes de TAMAÑO del juego
(Sterak's, Gargoyle, Twinguard, Mantle, Feast) y la matemática de Cho'Gath/Malphite/Shyvana.

## 🚀 Uso rápido

```bash
cd wr-lab
python3 wrlab.py                  # ⭐ MENÚ INTERACTIVO — todo el lab en opciones numeradas
python3 wrlab.py estado           # salud local: reportes verificados + bundles al día + lint
python3 wrlab.py hotfix 7.3b      # ciclo completo de hotfix (§E pasos 7-8) con confirmación
python3 model/dps_model.py        # reproduce las tablas del reporte de Jinx (validación del motor)
```

El menú (`wrlab.py` sin argumentos) agrupa: **📊 Estado** (salud, vigía de parches + win rates, git) ·
**🔥 Ciclo de hotfix** (completo o paso a paso: triage/refresh/borrador/annotate/baseline) ·
**🧮 Análisis** (optimizador de builds, buscador de runas, demo del motor, lint) ·
**📦 Artefactos** (bundles, BD, tests). Cada función nueva del lab se registra en `MENU`
y aparece automáticamente. Modo no interactivo para CI y chats externos: `wrlab.py <comando> [args]`.

**Cuando sale un hotfix/parche nuevo** (tras aplicar datos con FRAMEWORK §E pasos 1–6):

```bash
python3 model/update_reports.py triage   --patch 7.3a          # ¿qué tanto afecta a cada reporte publicado?
python3 model/update_reports.py refresh  --patch 7.3a --apply   # APLICA números nuevos donde el motor los reproduce 1:1
python3 model/update_reports.py borrador --patch 7.3a           # ❌ REGENERAR → esqueleto en reportes/_borradores/
python3 model/update_reports.py annotate --patch 7.3a --apply   # inserta el bloque de verificación (idempotente)
python3 model/update_reports.py check                          # CI: drift motor↔registro + reportes sin triar
python3 model/lint_reportes.py                                 # calidad de reportes externos (ítems inventados, Ley 0…)
```

**Ciclo completo de hotfix (una sola línea por paso, en orden):** datos nuevos (§E 1-6) →
`triage` → `refresh --apply` → `borrador` → `annotate --apply` → `baseline` → tests →
`build_bundles.py` → `build_db.py` → `check` → commit/push. Los reportes publicados
**nunca se borran ni se re-derivan solos**: `refresh` solo actualiza números reproducibles,
`borrador` prepara el reemplazo en un directorio aparte y el autor decide.

**Simulador de timings de oro** (curvas por rol derivadas de las Tablas B del vault — sin constantes inventadas):

```bash
python3 model/sim_timings.py --curvas                    # anclas y curvas por rol (adc/support/jungla/mid/top)
python3 model/sim_timings.py --reporte Jinx.md --leave-one-out   # ¿es consistente su Tabla B? (validación honesta)
python3 model/sim_timings.py --rol adc --build "Berserker's,Hexoptics C44,Terminus,Yun Tal,IE,LDR" --upgrade Gunmetal
#   ↑ fecha cada compra de una ruta NUEVA (p.ej. la variante anti-tanques: pico 6 slots ~22:00)
```

**Auto-regeneración de reportes** (escalabilidad 100+ campeones — el publicado NUNCA se toca sin aprobación):

```bash
python3 model/generate_report.py generar --champion shyvana --rol jungla   # → reportes/_auto/ (Espera de verificación)
#   revisas TODOs y números, comparas con el publicado, y si te convence:
python3 model/generate_report.py aprobar --archivo Shyvana_AUTO_7.3a.md    # → reportes/ (Status: Aprobado) + ciclo
```

**Buscador de runas** (keystone × secundaria con valor marginal contra el baseline LT+Alacrity):

```bash
python3 model/optimize_runes.py jinx                # build publicada del registro; LT×Alacrity gana ✓
python3 model/optimize_runes.py diana --build "Spellslinger,DuskDawn,Nashor,Rabadon,Zhonyas,Cryptbloom"
```

**Optimizador de builds** (búsqueda exhaustiva, 4 motores: autos / on-hit / rotación / valor-aliado):

```bash
python3 model/optimize_build.py jinx --crit-min 100 --pen-min 30 --validar   # motor autos (Jinx, Yunara, Sivir…)
python3 model/optimize_build.py kalista --validar                            # motor on-hit (E Rend + Guinsoo)
python3 model/optimize_build.py diana --keystone lt --validar                # motor rotación AP
python3 model/optimize_build.py yuumi --oro 13000 --validar                  # motor valor-aliado (quest fija + Crimson)
python3 model/optimize_build.py jinx --incluir "Gunmetal,C44,Runaan's,IE,LDR,Kraken,BT,Galeforce,Scimitar,RFC,Berserker's" --validar
#   ↑ NIVEL 1 de validación: redescubre la build C publicada (3 042 dps1) dentro del pool del reporte.
#   NIVEL 2 (pool completo): puede superarla — hallazgos en ROADMAP §Hallazgos, no se auto-aplican.
python3 model/optimize_build.py jinx --preset balanceado   # 70 % DPS + 15 % EHP + 15 % utilidad
#   ↑ modelos de defensa (EHP mixto con escudos ponderados) y utilidad (activas GA/Zhonyas/QSS + heal/s)
```

**Bundles portables** (artefactos derivados — NO editar a mano):

```bash
python3 model/build_bundles.py            # regenera WR-LAB_lite.md + WR-LAB_completo.md desde las fuentes
python3 model/build_bundles.py --check    # CI: falla si los bundles están desfasados
```

Los reportes **NO se regeneran**: el triage mide el Δ sobre métricas de resultado y sella cada
reporte con su veredicto (✅ ANOTAR <2 % · ⚠️ REVISAR 2–5 % · ❌ REGENERAR ≥5 % o cambio a
inputs del spec). Solo los ❌ pasan por el flujo completo de 10 pasos. Caso de referencia:
**Yuumi 7.3a** — nerf directo a su W (HSP −5 % de input) → escudo/cura −1.4 % de resultado →
✅ build definitiva intacta, anotada sin re-derivar.

**Para analizar un campeón nuevo** (solo o con ayuda de un asistente):
1. Leer `metodologia/FRAMEWORK.md` (flujo de 10 pasos y las 7 Leyes).
2. Buscar al campeón en `data/estructurada/champion_attack_speed_7.3.csv` y `cambios_campeones_7.3.md`.
3. Copiar la plantilla de `ChampSpec` en `model/dps_model.py` y llenarla (datos del kit: wiki oficial / wr-meta `/{id}-{nombre}.html`).
4. Proponer 4–6 builds candidatas y correr `compare(spec, builds)`.
5. Escribir el reporte con `metodologia/TEMPLATE_REPORTE.md` y guardarlo en `reportes/`.

**Prompt sugerido para pedir el siguiente análisis** (con este lab cargado/adjunto):
> "Usando wr-lab (FRAMEWORK.md + dps_model.py + data/estructurada), genera el análisis completo
> nivel-Jinx para {CAMPEÓN} en el parche vigente, con reporte en Markdown según TEMPLATE_REPORTE.md."

## ⚠️ Reglas de higiene del lab

- **LEY 0 — SLOTS:** Wild Rift tiene **6 slots totales y las botas ocupan UNO**. Las botas Tier 3 (Gunmetal, Chainlaced, etc.) son la **mejora en el MISMO slot** de su Tier 2 (min 10:00), no un ítem extra. Build final = 1 botas + 5 ítems. Nunca listar "Berserker's + Gunmetal" como dos entradas. `dps_model.validate_slots()` lo verifica automáticamente.
- **Las notas oficiales mandan** sobre wr-meta y sobre guías (ver `data/FUENTES.md` §Discrepancias).
- **Los reportes publicados NO se regeneran con cada hotfix**: se TRIAN con `model/update_reports.py`
  (Δ de resultado <2 % → bloque de verificación y siguen vigentes; solo ❌ REGENERAR autoriza re-derivar la build).
- Antes de cualquier análisis nuevo: verificar si salió hotfix (7.3a/b…) o parche nuevo; si sí → protocolo §E del FRAMEWORK.
- Wild Rift tiene **6 espacios totales (botas incluidas)**; las botas T3 solo desde el **min 10:00**; los
  **encantamientos de botas no existen desde 7.2** (QSS/Scimitar/Galeforce son ítems normales de clase).
- Ítems/runas **removidos** que las guías viejas aún recomiendan: Magnetic Blaster, Cloak of Agility,
  Nashor's Talon, Stinger, Surging Scales, Searing Crown, Soul Transfer, Ingenious Hunter, Legend: Tenacity.
- Todo número publicado en un reporte debe poder reproducirse con `dps_model.py` + sus supuestos declarados.

## 🚚 Portabilidad (el lab viaja contigo — SIN necesidad de zip)

Todo el lab es **texto plano** (.md/.csv/.py): puedes descargar/adjuntar cada archivo por separado en cualquier herramienta.
Además existen dos bundles autocontenidos en la raíz:

| Archivo | Tamaño | Para qué |
|---|---|---|
| `WR-LAB_lite.md` | ~176 KB | Pegar/adjuntar en cualquier IA: metodología + 7 Leyes + Regla de Oro + tabla AS de los 140 campeones + ítems (stats/precio) + specs del equipo + motor de DPS + motor batch + **optimizador de builds** |
| `WR-LAB_completo.md` | ~836 KB | Lo anterior + diffs oficiales 7.3/7.3a + fichas de los 11 campeones del equipo + **los 16 reportes del vault con sus bloques WRLAB-VERIF** + ítems con pasivas + ROADMAP + tests + actualizador de reportes + infraestructura (extract/build_db/check_patch) |

Ambos se **regeneran desde las fuentes** con `model/build_bundles.py` (el CI verifica que no se
desfasen). Tras cualquier cambio de datos/modelo/reportes: regenerar y commitear.

Prompt sugerido con el bundle adjunto:
> "Usando WR-LAB (leyes + dps_model.py + specs), genera el análisis nivel-Jinx para {CAMPEÓN} en el parche vigente, con reporte según TEMPLATE_REPORTE."

**Dentro de este workspace los archivos persisten entre conversaciones del proyecto**: puedes volver aquí y pedir el siguiente análisis sin adjuntar nada.

## 👥 Roster del equipo — specs precargadas (v1.1, 25-sep-2026)

| Campeón | Roles | Arquetipo | Estado del spec |
|---|---|---|---|
| **Jinx** | ADC | crítico AoE | ✅ análisis completo en `reportes/` |
| **Yunara** | ADC | crítico AoE híbrido (spread) | ✅ precargada — falta modelo de spread/pasiva |
| **Kalista** | ADC | on-hit ejecutor (E Rend) | ✅ precargada — falta modelo de Rend |
| **Diana** | Jungla / Mid | AP assassin con AS condicional (30–100 %) | ✅ precargada — falta rotación AP |
| **Volibear** | Jungla / Top | fighter híbrido (AS por stacks) | ⚠️ precargada — VERIFICAR ad_growth (la fuente muestra "56") |
| **Shyvana** | Jungla | on-hit / AP dragón | ✅ precargada — falta modelo Q doble golpe |
| **Cho'Gath** | Jungla / Mid / Top | AP tank (Feast) | ✅ precargada — modelo de rotación, no de autos |
| **Mordekaiser** | Top / Jungla | AP juggernaut | ✅ precargada — modelo de rotación |
| **Yuumi** | Support | enchanter-attach | ✅ precargada — análisis por valor al aliado (HSP/uptime), no DPS propio |
| **Karma** | Support / Mid | enchanter-poke | ✅ precargada — igual que Yuumi |
| **Seraphine** | Support / Mid | enchanter-mage (doble cast) | ✅ precargada — haste como multiplicador |
| **Heimerdinger** | Mid / Support | mage-zona (turrets) | ✅ precargada — DPS de torretas + push 7.3 |

Fichas con stats/habilidades/change history: `data/estructurada/campeones/*.md`.
Datos pendientes de verificar en juego: rango de ataque de Kalista/Yunara (no viene en la fuente) y growth de AD de Volibear.

## 🏗️ Arquitectura de proyecto (v1.5+)

El lab es un **proyecto de software versionado**, no solo documentos:

| Pieza | Qué hace |
|---|---|
| `git` (repo local, tag por versión) | Historial completo; listo para `git remote add origin … && git push` |
| `data/wrlab.db` (SQLite, `model/build_db.py`) | Capla de consulta/respaldo: 13 campeones, 140 fichas AS oficiales, 186 ítems, cambios por parche, reportes y fuentes. Reconstruible desde los .md/.csv en segundos |
| `tests/test_model.py` | 14 tests de regresión: fórmula oficial de AS (test Caitlyn pre/post 7.3a), validate_slots (incluye el bug histórico de botas), golden numbers de los reportes, overrides de hotfix |
| `tests/test_update_reports.py` | 25 tests del triador: golden numbers por modelo (Jinx/Kalista/Diana/Yuumi), parseo de Tabla A, caso Yuumi 7.3a (no regenerar), idempotencia de anotación, rúbrica de veredictos |
| `model/update_reports.py` + `data/estructurada/reportes_registry.json` | Triador/actualizador de reportes publicados ante hotfixes: cuantifica el Δ (métricas de resultado vs input), inserta bloques de verificación idempotentes y sella el registro. `check` vigila drift y reportes sin triar |
| `model/optimize_build.py` | Optimizador exhaustivo v2 con **4 motores** (autos/on-hit/rotación/valor-aliado), objetivo ponderado normalizado, Leyes 1/3 como restricciones opcionales. Validación cruzada en 2 niveles (redescubre C de Jinx, D2-LT de Diana, Y1 de Yuumi; K2 de Kalista a 0.3 % del top-1) |
| `update_reports.py refresh/borrador` | `refresh` aplica números post-parche in-place SOLO donde el motor reproduce el publicado 1:1; `borrador` genera esqueletos de regeneración en `reportes/_borradores/` para los ❌ (el publicado no se toca) |
| `wrlab.py` | **CLI unificado + menú interactivo** (registro escalable de acciones): estado, ciclo hotfix completo, optimizador, runas, lint, bundles, BD, tests, git. Modo comando para CI/chats externos |
| `model/sim_timings.py` | Simulador de timings: curvas de oro por rol derivadas de las Tablas B del vault (112 anclas); audita rutas publicadas (leave-one-out) y fecha picos de rutas nuevas; tolerancia ±150 s |
| `model/optimize_runes.py` | Buscador de runas: grid keystone×secundaria, valor marginal vs baseline, supuestos declarados y runas excluidas con motivo (fuente rasgada). Valida LT×Alacrity (Jinx) y LT (Diana) |
| `model/generate_report.py` + `reportes/_auto/` | **Auto-regenerador** (v1.13): reporte completo TEMPLATE v1.4 desde optimizador+runas+timings+winrates, `Status: Espera de verificación`, `generate: auto`, TODOs explícitos donde hace falta juicio humano; `aprobar` lo mueve a reportes/ y corre el ciclo. Solo campeones con spec+motor; sin motor → `borrador` (fallback). Cubre el flujo ❌ REGENERAR a escala |
| `model/lint_reportes.py` | Linter del vault: ERRORES (build no extraíble, Ley 0, **ítems inexistentes en la BD oficial**) + AVISOS (frontmatter, rol, parche, pie de página, espacio de miles). `--strict` para gates |
| `model/build_bundles.py` | Regenerador de los bundles portables (lite/completo) desde las fuentes + `--check` anti-drift en CI |
| `model/check_patch.py` + `.github/workflows/patch-watch.yml` | Vigía 2×/día: detecta cambios de CONTENIDO de la página oficial (hash normalizado, inmune al ruido del CMS), aparición de 7.3a/7.4 y changelogs nuevos en wr-meta, **y actualiza las win rates del roster (`champion_winrates.csv/.md`, wr-meta Diamond+) en el mismo proceso**; alerta con \|Δ win rate\| ≥ 2 pts. Exit 1 + aviso si hay cambios. Manual: `wrlab.py winrates` |
| `.github/workflows/ci.yml` | Tests + rebuild de BD en cada push |
| `ROADMAP.md` | Módulos siguientes: CLI unificado, optimizador de builds, sync con vault de Quartz, simulador de timings, matchups |

Reglas: **texto plano = fuente de verdad; SQLite = índice derivado; cero dependencias externas.**

## 📌 Versión

- v1.0 — 25/09/2026: creación a partir del análisis de Jinx 7.3 (datos oficiales 7.3/7.2 + wr-meta 24/09).
- v1.1 — 25/09/2026: roster del equipo precargado (11 campeones, fichas + specs), bundles portables LITE/COMPLETO.
- v1.2 — 25/09/2026: reportes completos de Kalista/Diana/Yuumi/Karma + apéndice de escalado de tamaño + spec de Malphite (12+1 campeones) + análisis batch 2 (model/analysis_batch2.py).
- v1.3 — 25/09/2026: **Ley 0 de slots** (botas T2→T3 = mismo slot) tras bug detectado al usar los bundles en otro chat: `validate_slots()` en el motor, FRAMEWORK/TEMPLATE/ítems/reportes actualizados, extract_data.py corregido y reproducible.
- v1.5 — 28/09/2026: **HOTFIX 7.3a integrado** (nerfs Malphite/Yuumi/Caitlyn/Senna/Hwei…, buffs Yun Tal/Samira/Tristana/Draven/Viego, Smite/Nexus/placas) con diff estructurado, overrides en datos y tests. **Arquitectura de proyecto:** git + SQLite (wrlab.db) + tests (14) + CI/patch-watch (GitHub Actions) + ROADMAP de módulos.
- v1.4 — 28/09/2026: **Estándar visual de reportes** (TEMPLATE_REPORTE.md = guía de estilo obligatoria: frontmatter Obsidian, callouts, Tabla A/B, números con espacio de miles, pie de página con créditos Riot/wr-meta/WR-LAB). Los 5 reportes (Jinx, Kalista, Diana, Yuumi, Karma) re-estilizados al estándar; reporte de Jinx adoptado desde la versión del autor con datos de ejemplo corregidos.
- v1.13.1 — 02/10/2026: **Plantilla del generador según feedback del autor:** §4 LEYES en formato COMPACTO como estándar (TEMPLATE §A.4b) · §8 con nombres de ítems COMPLETOS y columna **Fuente** (⭐ LAB óptima / 🔬 LAB top-N / 📌 publicada / 🌐 comunidad) — el reporte de Jinx sigue siendo el estándar de contenido. **Modo cualitativo** del generador para campeones sin motor (tanques): plantilla completa con datos reales (diffs, win rates, stats del CSV, ruta publicada) + cálculos parciales con supuestos declarados + TODOs explícitos; corrige Ley 0 de la ruta base (botas T2→T3). **Caso Rammus generado** (`_auto/Rammus_AUTO_7.3a.md`): EHP −1.3 %, W rank1 −34 % (nerf early, late intacto) — pendiente de verificación del autor.
- v1.13 — 02/10/2026: **Auto-regenerador de reportes** (`generate_report.py`: generar→`_auto/` en "Espera de verificación"→aprobar; consume optimizador/runas/timings/winrates por puertos — arquitectura hexagonal; Shyvana generado como primer deliverable). **Reconciliación lab↔vault** (decisiones del autor 01/10): Caitlyn v1.3 y Seraphine "Modo Agresiva" y Volibear.md ingeridos (⏩ AL_DIA), **Yunana→Yunara renombrado**, guías custom formalizadas (tags Personalizado; Volibear Pesadilla etiquetado). **Contrato v1.1** (custom/variant/generate/mode:aram + vocabulario de Status + flujo de aprobación) y **backfill v2** (28 claves custom/variant). `ALIAS` del motor gana nombres oficiales completos. Tests: 136. Bundles: lite 243 KB / completo 1.05 MB (§10f generador). Rammus sigue ❌ (tanque sin motor — borrador vigente).
- v1.12.2 — 01/10/2026: **Migración Fase 0+1 ejecutadas** (plan del autor). Fase 0: informe de estado + matriz de divergencia lab↔vault (`deploy/MIGRACION_FASE0_ESTADO.md` — el vault está adelante en Caitlyn/Seraphine/Volibear/Shyvana; el lab en verificación) + auditoría del sitio Quartz 5 y componentes reutilizables. Fase 1: `deploy/CONTRATO_MARKDOWN_FRONTEND.md` v1.0 (frontmatter canónico, guias_index.json, reglas de renderizado WRLAB-VERIF/callouts/números, sync unidireccional lab→frontend) + `model/backfill_frontmatter.py` APLICADO (99 claves en 16 reportes; lint 55→26 avisos). Tests: 130.
- v1.12.1 — 01/10/2026: **Tema minimalista adoptado** (`deploy/quartz-theme/wrlab-minimal.css`, drop-in para el vault; portable a Next.js cuando el sitio migre). **Plan de migración del sitio** archivado como fuente de verdad (`deploy/PLAN_MIGRACION_VERCEL.md`, autor, v1.0) con las tareas del lab identificadas (fases 0-1: informe de estado + backfill de frontmatter desde el registro). ROADMAP: §Pistas activas (migración + módulo ARAM AAA propuesto) y §Backlog APROBADO (matchups → runas v2 → calibración). Linaje fetch_meta del chat retirado en favor del sistema oficial de win rates (check_patch --winrates-only). Suite oficial: 124 tests OK.
- v1.11 — 01/10/2026: **Win rates integradas al vigía** (`check_patch.py` paso 4, petición del autor): el MISMO proceso que busca parches/hotfixes actualiza `data/estructurada/champion_winrates.csv/.md` (bloque Meta Overview de wr-meta, bucket Diamond+, 17 campeones del roster = reportes + specs, ampliado automáticamente por el registro; ids descubiertos vía sitemap.xml). Tabla `winrates` en la BD, §7b en los bundles, comando/menú `wrlab.py winrates`, alerta del vigía con |Δ| ≥ 2 pts y AVISO del linter si el callout meta de un reporte diverge >3 pts del dato actual (TEMPLATE §A.1: los callouts se citan desde el CSV, no de memoria). El workflow patch-watch commitea CSV/MD/estado. Tests: 124 (107+17, todos offline con fixtures + snapshot commiteado). Docs: FRAMEWORK §E, FUENTES (registro + secundaria + derivación), ROADMAP.
- v1.10 — 29/09/2026: **Simulador de timings de oro** (`sim_timings.py`: curvas por rol derivadas de las Tablas B del vault — cero constantes inventadas; audita reportes con leave-one-out y fecha rutas nuevas; la variante anti-tanques de Jinx pica ~22:00 vs ~21:00 de la C). **Fix de arquetipos en el optimizador** (bug reportado: Cho'Gath optimizado "como ADC" — ahora los arquetipos sin motor se rechazan con guía y las aproximaciones avisan; columnas EHP/UTIL solo con pesos activos). **Reporte de Jinx v1.4 integrado** (variante anti-tanques = hallazgo del optimizador verificado por el motor: 17 900 g · pen 65 % · +42 %/+31 %; ⏩ AL_DIA — declara patch 7.3a). Tests: 107. Menú wrlab: +timings. Bundles: §10e.
- v1.9 — 29/09/2026: **CLI unificado + menú interactivo** (`wrlab.py`: estado, ciclo hotfix completo, análisis, artefactos; registro escalable; modo comando para CI). **Auto-regeneración de reportes** (escalabilidad 100+ campeones — el publicado NUNCA se toca sin aprobación):

```bash
python3 model/generate_report.py generar --champion shyvana --rol jungla   # → reportes/_auto/ (Espera de verificación)
#   revisas TODOs y números, comparas con el publicado, y si te convence:
python3 model/generate_report.py aprobar --archivo Shyvana_AUTO_7.3a.md    # → reportes/ (Status: Aprobado) + ciclo
```

**Buscador de runas** (`optimize_runes.py`: keystone×secundaria con valor marginal; autos+rotación; valida las conclusiones de runas de Jinx y Diana; supuestos declarados; runas con fuente rasgada excluidas con motivo). **Defensa/utilidad en el optimizador** (EHP mixto + activas + sustain ponderado; `--preset balanceado/defensivo`; goldens ofensivos intactos por defecto). `eval_build` gana `ad_extra` (Conqueror). Tests: 92. Bundles: lite 200 KB / completo 910 KB (§10d runas, §17 suite completa, §18 CLI+lint+infra).
- v1.8 — 29/09/2026: **Optimizador v2 (4 motores)** — on-hit (Kalista), rotación AP (Diana) y valor-aliado (Yuumi/Karma) además de autos; validación cruzada en 2 niveles + hallazgos documentados (ROADMAP). **Refresh y borradores:** `update_reports.py refresh --apply` actualiza números reproducibles 1:1 dentro del reporte; `borrador` genera esqueletos de reemplazo en `reportes/_borradores/` para los ❌ REGENERAR (Caitlyn y Rammus ya los tienen). **Linter de reportes** (`lint_reportes.py`): caza ítems alucinados ("Bastion of Spirits" en Seraphine), builds no extraíbles y desviaciones del estándar v1.4. **Diccionarios batch2 expandidos** desde items_7.3.csv (Mandate, Stormsurge, Harmonic Echo, Morello, Rylai, Horizon Focus, Liandry) → Yuumi poke-híbrida ya es cuantificable (Δ 7.3a = −1.7 % → ✅ ANOTAR). Tests: 74.
- v1.7 — 29/09/2026: **Optimizador de builds** (`optimize_build.py`, validación cruzada: redescubre la build C de Jinx; hallazgo post-7.3a: con el pool completo, Yun Tal buffeada + Terminus superan a C ~7 % en eficiencia ponderada — decisión de actualizar el reporte queda al autor). **Regenerador de bundles** (`build_bundles.py`, artefactos derivados con `--check` en CI). **Vault integrado:** 16 reportes externos sustituyen a los 5 del lab; parser del actualizador v2 (champion por nombre de archivo, tablas BUILD_FINAL/rutas, alias en paréntesis, ⏩ AL_DIA); triage 7.3a del vault: Caitlyn y Rammus ❌ REGENERAR (inputs del spec tocados), Yuumi ⚠️ REVISAR (nerf W sin hook para build poke-híbrida), 13 ✅. Tests: 60. BD con reports keyed por ruta.
- v1.6 — 29/09/2026: **Actualizador de reportes publicados** (`model/update_reports.py`): ante un hotfix, TRIA el impacto por reporte (Δ sobre métricas de resultado, no inputs), inserta bloques de verificación idempotentes (`WRLAB-VERIF`) y sella `reportes_registry.json`; las builds definitivas no se re-derivan salvo ❌ REGENERAR (caso de aceptación: Yuumi 7.3a ✅). Verificación de que 7.3a sigue siendo el último hotfix (página oficial: contenido idéntico, solo ruido de CMS) y `check_patch.py` corregido a hash de contenido normalizado (adiós falsos positivos). Tests: 39 (14+25). FRAMEWORK §E ampliado (pasos 6–8) + TEMPLATE A.8.
