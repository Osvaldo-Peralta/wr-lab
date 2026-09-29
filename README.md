# ⚗️ WR-LAB — Laboratorio de builds matemáticas para Wild Rift (parche 7.3)

Todo lo recabado y razonado en el análisis de **Jinx 7.3**, convertido en infraestructura reutilizable
para analizar **cualquier campeón** con el mismo rigor, sin depender de la memoria de un chat.

**Estado de datos:** parche 7.3 (21-sep-2026), verificados al 25-sep-2026.

---

## 📁 Mapa del laboratorio

```
wr-lab/
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
│       └── reportes_registry.json     ← índice derivado: builds publicadas + golden metrics por reporte
├── model/
│   ├── extract_data.py                ← regenera data/estructurada/ desde data/raw/
│   ├── dps_model.py                   ← ⭐ motor de DPS parametrizado por campeón (engine + Jinx precargado)
│   └── update_reports.py              ← ⭐ triador de hotfixes sobre reportes publicados (anota, NO regenera)
├── metodologia/
│   ├── FRAMEWORK.md                   ← ⭐ las 7 Leyes + flujo de 10 pasos + arquetipos + protocolo de parche nuevo
│   ├── TEMPLATE_REPORTE.md            ← estructura exacta del reporte + checklist de calidad
│   └── ESCALADO_DE_TAMANIO.md         ← size scaling: Cho'Gath/Malphite/Shyvana
├── deploy/
│   └── GITHUB_PAGES_QUARTZ.md         ← sitio público de guías (Quartz 5 + Pages): setup, bug del baseUrl y arreglo
└── reportes/
    ├── Jinx_WildRift_7.3_Build_Optimizada.md      ← caso de referencia (crítico AoE)
    ├── Kalista_WR_7.3_Build_Optimizada.md         ← on-hit ejecutor (E Rend)
    ├── Diana_WR_7.3_Build_Optimizada.md           ← jungla+mid (AP híbrido; LT > Empowerment)
    ├── Yuumi_WR_7.3_Build_Optimizada.md           ← support (modelo de valor-aliado)
    └── Karma_WR_7.3_Build_Optimizada.md           ← support+mid (Imperial Mandate = +7% team)
```

📐 Apéndice transversal: `metodologia/ESCALADO_DE_TAMANIO.md` — todas las fuentes de TAMAÑO del juego
(Sterak's, Gargoyle, Twinguard, Mantle, Feast) y la matemática de Cho'Gath/Malphite/Shyvana.

## 🚀 Uso rápido

```bash
cd wr-lab
python3 model/dps_model.py        # reproduce las tablas del reporte de Jinx (validación del motor)
```

**Cuando sale un hotfix/parche nuevo** (tras aplicar datos con FRAMEWORK §E pasos 1–6):

```bash
python3 model/update_reports.py triage   --patch 7.3a          # ¿qué tanto afecta a cada reporte publicado?
python3 model/update_reports.py annotate --patch 7.3a --apply   # inserta el bloque de verificación (idempotente)
python3 model/update_reports.py check                          # CI: drift motor↔registro + reportes sin triar
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
| `WR-LAB_lite.md` | ~108 KB | Pegar/adjuntar en cualquier IA: metodología + 7 Leyes + tabla AS de los 140 campeones + ítems (stats/precio) + specs del equipo + motor de DPS completo |
| `WR-LAB_completo.md` | ~460 KB | Lo anterior + diffs oficiales 7.3 de campeones/ítems + fichas completas de los 11 campeones del equipo + reporte de Jinx + ítems con pasivas |

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
| `model/check_patch.py` + `.github/workflows/patch-watch.yml` | Vigía 2×/día: detecta cambios de CONTENIDO de la página oficial (hash normalizado, inmune al ruido del CMS), aparición de 7.3a/7.4 y changelogs nuevos en wr-meta. Exit 1 + aviso si hay cambios |
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
- v1.6 — 29/09/2026: **Actualizador de reportes publicados** (`model/update_reports.py`): ante un hotfix, TRIA el impacto por reporte (Δ sobre métricas de resultado, no inputs), inserta bloques de verificación idempotentes (`WRLAB-VERIF`) y sella `reportes_registry.json`; las builds definitivas no se re-derivan salvo ❌ REGENERAR (caso de aceptación: Yuumi 7.3a ✅). Verificación de que 7.3a sigue siendo el último hotfix (página oficial: contenido idéntico, solo ruido de CMS) y `check_patch.py` corregido a hash de contenido normalizado (adiós falsos positivos). Tests: 39 (14+25). FRAMEWORK §E ampliado (pasos 6–8) + TEMPLATE A.8.
