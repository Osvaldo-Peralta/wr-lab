> ## ⚠️ LEY 0 — SLOTS (leer antes de proponer CUALQUIER build)
> Wild Rift tiene **6 slots de ítem EN TOTAL y las botas ocupan UNO**. Las botas Tier 3
> (Gunmetal Greaves, Chainlaced Crushers, Armored Advance, Crimson Lucidity, Spellslinger's Shoes,
> Armorcrusher Boots, Immortal Treads) son la **mejora EN EL MISMO SLOT** de su Tier 2 (desde el min 10:00).
> **Build final = 1 botas (T3) + 5 ítems.** Listar "Berserker's Greaves" y "Gunmetal Greaves" como dos
> ítems es un ERROR (deja la build con 5 slots reales y pierde un ítem completo).
> Toda lista de build debe pasar `dps_model.validate_slots()` (6 entradas, exactamente 1 botas, nunca T2+T3 juntas).

> ## 🧭 REGLA DE ORO — LOS REPORTES PUBLICADOS NO SE REGENERAN (v1.6)
> Una build publicada y aprobada es **definitiva**. Cuando sale un hotfix se TRIA con
> `model/update_reports.py` (Δ sobre métricas de RESULTADO): **<2 % ✅ se anota** el bloque
> `WRLAB-VERIF` y la build sigue vigente · 2-5 % ⚠️ revisión acotada · **≥5 % o cambio a inputs
> del spec ❌ regenerar** (flujo FRAMEWORK de 10 pasos, con apoyo de `model/optimize_build.py`).
> Los reportes del bundle llevan su bloque de verificación: respétalo, no re-derives builds ✅.

> ## 🎨 ESTÁNDAR VISUAL DE REPORTES (v1.4 — obligatorio)
> Todo reporte generado DEBE seguir `metodologia/TEMPLATE_REPORTE.md` al pie de la letra:
> frontmatter YAML (tags/version/Status/champion/patch) · bloque de metadatos en negritas ·
> callouts `> [!NOTE]` (meta real con WR/pick/ban) y `> [!TIP]`/`> [!DANGER]`/`> [!WARNING]` según aplique ·
> §0 con **Tabla A (6 slots exactos)** + **Tabla B (ruta cronológica con componentes y oro acumulado)** ·
> secciones `## N. MAYÚSCULAS` 0-10 + APÉNDICE A/B + **Pie de página** (referencias Riot/wr-meta/WR-LAB + aviso legal) ·
> números con espacio de miles (`2 900`, `17 350 g`) y `%` con espacio (`25 %`) · veredictos ✅/⚠️/❌ siempre con número.
> Bloque de verificación de hotfix (§A.8): gestionado por tooling, no editar a mano.

> ## 🔥 ESTADO DE DATOS: parche 7.3+7.3a — hotfix 7.3a LIBERADO (29-sep-2026) e integrado
> Los cambios de 7.3a (nerfs a Hwei/Malphite/Caitlyn/Senna/Yuumi/Rammus/Syndra; buffs a Samira/Tristana/
> Draven/Viego; Yun Tal AS 35 %; Diadem/Circlet nerf; Death's Dance 3 300; Smite burn −; Nexus 4 000;
> placas −resist) están en §3b y YA aplicados a specs, motor y apéndices de este bundle.
> **✅ Verificado contra la nota EN oficial de 7.3a** (publicada 29-sep-2026): todos los números del
> diff CN aplicado al lab coinciden con la fuente primaria (registro en §3, data/FUENTES.md).
> Sin páginas 7.3b/7.4 al 29-sep-2026.

# ⚗️ WR-LAB PORTABLE (LITE) — Wild Rift 7.3+7.3a · 02/10/2026

> Laboratorio de builds matemáticas en UN archivo. Adjunta o pega este archivo en cualquier
> herramienta/IA y pide: "Usando WR-LAB, genera el análisis nivel-Jinx para {CAMPEÓN},
> siguiendo el ESTÁNDAR VISUAL v1.4 de TEMPLATE_REPORTE.md".
> Versión completa (reportes del vault, fichas, diffs, infraestructura): WR-LAB_completo.md

## 1. METODOLOGÍA (Ley 0 + las 7 Leyes + flujo)

# FRAMEWORK — Metodología de análisis de builds (Wild Rift 7.3+)

> Este documento destila el razonamiento usado en el análisis de Jinx para que sea
> **replicable con cualquier campeón**. No es una lista de builds: es el procedimiento
> para DERIVARLAS. Leer junto con `TEMPLATE_REPORTE.md` y `model/dps_model.py`.

---

## A. Flujo de trabajo por campeón (10 pasos)

1. **Verificar vigencia del parche.** ¿Salió un hotfix (7.3a/b…) o parche nuevo desde el 21-sep-2026?
   Si sí: descargar notas oficiales y regenerar `data/estructurada/` (protocolo en §E).
2. **Ficha del campeón (spec).** Llenar un `ChampSpec` en `model/dps_model.py` con:
   - AD base y crecimiento → `data/estructurada/cambios_campeones_7.3.md` (si lo tocaron) + wiki oficial.
   - AS base/ratio/bonus base/por nivel → `data/estructurada/champion_attack_speed_7.3.csv` (los 140 campeones, datos oficiales 7.3).
   - Vida/armadura/RM → `champion_durability_7.3.csv` (solo los ajustados).
   - Modificadores del autoataque (`aa_mult`, `aa_aoe`), AS condicional propia (`self_as_buff`),
     modificador de daño crítico (`crit_dmg_mod`: Jhin 0.8, Yasuo/Yone/Senna 0.9), rango efectivo.
3. **Leer sus cambios de 7.3.** ¿Sus habilidades ahora escalan con crítico (Caitlyn, MF, Tristana, Xayah, Akshan, Viego…)?
   Eso sube el valor de IE y del crítico por encima del modelo de solo autos. ¿Lo nerfearon/buffearon? (Jinx: AD growth y R.)
4. **Definir el arquetipo** (§C) y las 3–5 rutas candidatas serias (no todas las posibles).
5. **Enumerar builds como listas de ítems** (apoyo: `model/optimize_build.py <champ>` las busca
   de forma exhaustiva bajo Leyes 0-1-2-3 y presupuesto) (SIEMPRE 6 slots totales: 1 botas + 5 ítems — ver Ley 0;
   en la lista va la botas T3, nunca T2+T3 a la vez; `validate_slots()` corre automáticamente)
   y correr `compare(spec, builds)` en los 4 escenarios estándar: 1v1, 3v3, vs 120 armadura, vs tanque (220 arm + ≥1200 HP bonus + 4500 HP para %-vida).
6. **Aplicar las Leyes** (§B) para podar: stats muertos (crítico >umbral, AS sobre el tope, haste inútil),
   eficiencia de oro por slot, coste de oportunidad del slot defensivo.
7. **Curva de poder, no solo nivel 15.** Correr el modelo en los checkpoints nivel 9 (1.er ítem),
   12 (2 ítems + botas), 14 (3 ítems + botas T3) para ordenar la RUTA de compra y detectar
   ítems que ganan temprano pero pierden tarde (Kraken-first) o al revés (C44-first).
   Fechar la Tabla B con `model/sim_timings.py --rol <rol> --build "…"` (curvas de oro del
   vault) y auditarla con `--reporte X --leave-one-out` antes de publicar.
8. **Runas y hechizos** (apoyo: `model/optimize_runes.py <champ>` puntúa keystone × secundaria
   con valor marginal contra el baseline LT+Alacrity; supuestos declarados en su docstring).
   Keystone que multiplique lo que la build ya compra (Lethal Tempo ↔ AS;
   Fleet ↔ sustain de lane; First Strike ↔ poke). Secundarias: valor por slot con la misma lógica de stats muertos.
9. **Matriz situacional del último slot** (vs CC / vs burst AD / vs AP / vs tanques / vs curación / vs dive)
   con números, no con opiniones.
10. **Escribir el reporte con `TEMPLATE_REPORTE.md`** — que desde v1.4 es el **estándar visual obligatorio**
(frontmatter Obsidian, metadatos, callouts [!NOTE]/[!TIP]/[!DANGER], Tabla A de 6 slots + Tabla B cronológica,
secciones 0-10 + apéndices A/B + pie de página con referencias y aviso legal, números con espacio de miles
"2 900" y "%" con espacio "25 %"). Referencia canónica: `reportes/Jinx_WildRift_7.3_Build_Optimizada.md`.

---

## B. Las Leyes (generalizadas del caso Jinx)

### Ley 0 — SLOTS: 6 en total y las botas son UNO (la regla más violada por las IAs)
Wild Rift tiene **6 espacios de ítem EN TOTAL, y las botas ocupan uno**. No hay "slot de botas" aparte.
- Las botas Tier 3 (Gunmetal Greaves, Chainlaced Crushers, Armored Advance, Crimson Lucidity,
  Spellslinger's Shoes, Armorcrusher Boots, Immortal Treads) son una **MEJORA EN EL MISMO SLOT** de su
  Tier 2 correspondiente, disponible desde el **minuto 10:00** (+1000g sobre la T2; Crimson/Immortal +1000g sobre 1000g).
- **Build final = 1 botas (en su forma T3 si el juego pasó del min 10) + 5 ítems.** Una lista con
  "Berserker's Greaves" Y "Gunmetal Greaves" como entradas separadas es ILEGAL: son el mismo slot y el
  conteo queda en 5 slots reales (¡se pierde un ítem completo!).
- La **ruta de compra** (cronológica) SÍ puede mostrar el paso "Berserker's (1200) → ⬆️ Gunmetal (+1000)"
  como dos momentos, pero debe decir explícitamente que es el mismo slot.
- Validación obligatoria antes de publicar cualquier build: `dps_model.validate_slots(lista)`
  (o `eval_build()`, que la invoca solo). Errores que captura: T2+T3 duplicadas, 2 botas, >6 entradas,
  build final de 6 sin botas.

### Ley 1 — Umbral de crítico exacto
Multiplicador promedio = `1 + crit × (daño_crit × mod_campeón − 1)`; daño_crit base = **2.00** (7.3), **2.30** con IE.
- Cada 1 % de crítico vale ~50g y rinde `+(daño_crit−1)` de multiplicador → con IE, **100 % de crítico = ×2.30**.
- Calcular el umbral útil del campeón (¿tiene conversión de crítico sobrante? Yasuo/Yone convierten a AD;
  Jhin no pasa de 100 %; Senna gana con niebla). **Todo crítico por encima del umbral es oro muerto** (~1250g por ítem con 25 %).
- Regla práctica: elegir la combinación de ítems que aterrice en el umbral EXACTO y que el resto de slots no traigan crítico.

### Ley 2 — Velocidad de ataque: apuntar al tope sin pasarse
`AS = AS_base × (1 + bonus_base + bonus_nivel + AS_items + runas + buffs_propios)`, tope **3.0** (7.3).
- Calcular `AS_items_para_cap = (3.0/AS_base − 1) − (bonus_fijos)`. Para Jinx = 152.6 %.
- Contar qué AS es condicional (stacks de LT: 6 golpes; pasivas de pelea) y cuál permanente.
- **Excepciones que rompen el tope**: Get Excited (Jinx), pasivas de reseteo → en esos campeones el sobretope NO es desperdicio total.
- AS de ítems sobra cuando: 3 fuentes grandes ya te ponen ≥95 % del tope en pelea.

### Ley 3 — Penetración % obligatoria contra el meta de vida
`mitigación = 100/(100 + armadura × (1−pen))`. Con torretas de 7000 HP y tanques con más vida:
- vs 120 armadura: pen 35 % = +23.5 % de daño real. vs 220: +32 %. vs 300: +36 %.
- Giant Slayer (LDR) suma +12 % adicional vs ≥1200 HP bonus → tanque full: ~+47 % total.
- La pen plana (Collector, Boots of Dynamism) solo rinde early o vs squishies puros.
- Doble pen (LDR+Mortal = 65 %) solo vs 3 tanques; normalmente pierde contra un slot de DPS/sustain.

### Ley 4 — Stats muertos y coste de oportunidad por slot
Auditar cada ítem candidato: ¿qué porcentaje de su oro compra stats que este campeón NO aprovecha?
Ejemplos 7.3: Galeforce en build de 100 % crit (25 % crit muerto ≈ 1250g), PD sin AD (solo AS/MS que pueden
sobrar), Navori con crit sobrante, maná/haste en campeones que no lo gastan. **Valor real = oro × (1 − fracción muerta) + pasivo.**

### Ley 5 — Eficiencia de oro con precios de componente 7.3
Referencias: 1 AD ≈ 37.5–41.7g (BF Sword/Pickaxe/Long Sword) · 1 % crit ≈ 50g (Brawler's) ·
1 % AS ≈ 33–45g (Dagger 400/12 %, Recurve 900/20 %) · 1 % pen ≈ 55g (Last Whisper) · 1 % lifesteal ≈ 50g ·
1 MR ≈ 25g · 1 armadura ≈ 22.5g · 1 HP ≈ 3.3g.
Pasivos: valuarlos como "AD equivalente" sobre el DPS medido (Magnification de C44 ≈ +10 % de AD total ≈ 1100g).
Ítems por encima de ~130 % de eficiencia con pasivo incluido son candidatos a core; por debajo de ~100 %, solo por utilidad única.

### Ley 6 — Timing > DPS teórico
Un ítem de 2650g terminado al minuto 11 vale más que uno de 3400g al 14 en partidas que terminan al 16–18.
Ordenar por: (a) coste, (b) suavidad del build path (componentes que ya pegan: Noonquiver 1300 = 20 AD+15 % crit),
(c) pico relativo (IE como 2.º ítem si vas feedeado; Runaan's 2.º si necesitas ventana barata).
Recordar reglas de 7.2+: botas T3 solo desde el **minuto 10:00**; placas de torreta decaen desde el **5:00**.

### Ley 7 — El sistema de juego también es input
7.3: torretas 7000 HP + placas permanentes + Crystalline Overgrowth (primer ataque detona 3.3–18.9 % de la vida
de la torreta como daño verdadero, ciclo ~50 s) + minions que pegan 60 % + jungla hostil para laners.
Traducir a build: rango/oleadas (Runaan's, Energized) valen más para tomar placas y detonar cristales de forma segura;
el oro de placas financia el pico del minuto 11–13.

---

## C. Arquetipos y cómo adaptar el modelo

| Arquetipo | Ejemplos | Claves del modelo |
|---|---|---|
| **Crítico AoE** | Jinx, Sivir, Xayah, Trista | `aa_aoe=True`; Ley 1 al 100 %; Runaan's multiplica; splash crítico |
| **Crítico burst/abilities** | Caitlyn, MF, Tristana, Akshan, Viego | Sus habilidades escalan crit en 7.3 → sumar término de habilidades al DPS (rotación), IE sube más |
| **Crítico modificado** | Jhin (0.8×, 4.º tiro), Yasuo/Yone (0.9×, conversión), Senna (0.9×) | `crit_dmg_mod`; umbral de crit distinto; AS irrelevante (Jhin) → Ley 2 no aplica igual |
| **On-hit** | Vayne, Kog'Maw, Twitch, Zeri | `onhit_*`, Guinsoo/Terminus/WE/BotRK/Statikk; la pen plana/% rinde distinto; AS se pasa del tope fácil |
| **Lethality/ejecutor** | Lucian crit-letality, Miss Fortune lethality, Varus | Collector/Serylda/Armorcrusher; DPS por ventana de burst, no sostenido; modelo por rotación |
| **AP/híbrido** | Kai'Sa, Varus AP, Corki | Statikk/Nashor/Dusk&Dawn/Luden; reemplazar términos de crit por ratios AP |
| **Spellblade** | Ezreal, Lucian ER | término `spellblade` con uptime = 1/ICD; AD BASE (no bonus) alimenta el proc |
| **No-ADC (fighters/magos)** | — | El modelo de autos no aplica: modelar rotación de habilidades (suma de ratios × uptime) + stats defensivos; las Leyes 4–6 siguen vigentes |

Para campeones con crítico en habilidades (7.3), añadir al DPS: `Σ (daño_hab × mult_crit_hab) / CD_efectivo`,
donde `mult_crit_hab` sale de la fórmula publicada en `cambios_campeones_7.3.md`
(patrón común: `× (1 + crit × X% + (daño_crit−2) × X% × crit)`).

---

## D. Reglas de verificación (aprendidas del caso Jinx)

1. **Las notas oficiales mandan.** Si wr-meta/wildstats y las notas difieren (pasó con Lethal Tempo: 4.8 % viejo
   vs 6.4 % oficial), usar las notas y registrar la discrepancia en el reporte (§10).
2. **Cuidado con los sistemas muertos.** Los encantamientos de botas NO existen desde 7.2 (QSS/Scimitar son
   ítems de clase); Magnetic Blaster, Cloak of Agility, Nashor's Talon, Stinger, Surging Scales, Ingenious Hunter,
   Legend: Tenacity y Soul Transfer fueron removidos. Las guías viejas mienten.
3. **Distinguir pasivas condicionales**: Magnification (distancia) ≠ Arcane Aim (kills); Flurry (uptime 30 %) ≠
   AS permanente; Opening Barrage (post-R) ≠ DPS sostenido. Modelar el uptime real, no el mejor caso.
4. **Declarar supuestos** en cada reporte (ver plantilla §10) y marcar estimaciones blandas (frecuencia de Energized,
   missing HP de Kraken, uptime de LT).
5. **Validar el modelo contra un caso conocido** antes de publicar números. Test oficial de Caitlyn
   (`mecanica_attack_speed_7.3.md`): AS 1.48125 a nivel 15 con Alacrity+Berserker's usando growth 0.04.
   ⚠️ El hotfix 7.3a bajó su AS growth a 0.025 → el esperado post-7.3a es **1.35**. El test del lab
   (`tests/test_model.py`) valida AMBOS (fórmula correcta + override 7.3a aplicado).
6. **Ni las notas oficiales son inmunes a erratas**: el apéndice de AS de 7.3 lista a Caitlyn con bonus 0.2 mientras
   su sección y el ejemplo de la fórmula usan 0.28 (ver FUENTES.md). Cuando dos secciones oficiales se contradicen:
   priorizar la sección específica del campeón, marcar el dato como "verificar en juego" y registrarlo en FUENTES.md.

---

## E. Protocolo de actualización de datos (cada parche)

> 💡 Atajo v1.9: `python3 wrlab.py` abre el **menú interactivo**; la opción
> "CICLO COMPLETO" de la sección hotfix ejecuta los pasos 7-8 de una vez.
>
> 🏹 v1.11: el vigía (`python3 model/check_patch.py`, cron 2×/día) busca parches/hotfix
> nuevos **y en el mismo proceso actualiza las win rates del roster**
> (`data/estructurada/champion_winrates.csv/.md`, wr-meta Diamond+). Los callouts
> "Estado Meta Actual" de los reportes nuevos o regenerados se citan desde ese archivo,
> nunca de memoria (TEMPLATE §A.1); refresco manual: `python3 wrlab.py winrates`.

```bash
# 1. Descargar notas oficiales del nuevo parche (python urllib desde el sandbox funciona):
#    https://wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-X-X/
#    → limpiar HTML → data/raw/patchX.txt  (mismo formato que patch73.txt)
# 2. Re-descargar https://wr-meta.com/items/ → data/raw/wrmeta_items.html
# 2b. Win rates (v1.11): las refresca el vigía en este mismo protocolo —
#     python3 wrlab.py winrates → data/estructurada/champion_winrates.csv/.md
#    (alternativa si cae: wr-meta.com/<id>-<champion>.html por campeón)
# 3. Re-ejecutar:  python3 model/extract_data.py
# 4. Diffear contra la versión anterior de items_7.3.csv / champion_attack_speed_7.3.csv
#    y actualizar: constantes en dps_model.py (CRIT_DMG, AS_CAP, LT…), precios/stats de ITEMS,
#    specs de campeones tocados.
# 5. Anotar en data/FUENTES.md: fecha, parche, discrepancias detectadas.
# 6. Escribir el diff estructurado data/estructurada/cambios_<patch>.md
#    (mismo formato que cambios_7.3a.md: tablas CAMPEONES / ÍTEMS / MAPA Y SISTEMAS /
#    IMPACTO EN REPORTES — de esta tabla se alimenta update_reports.py).
# 7. TRIAR los reportes publicados en vez de regenerarlos a ciegas:
#    python3 model/update_reports.py triage   --patch <X.Xx>
#    python3 model/update_reports.py annotate --patch <X.Xx> --apply
#    → ✅ ANOTAR/SIN_IMPACTO: la build publicada NO se toca (bloque de verificación insertado).
#    → ⚠️ REVISAR: revisión manual acotada (matriz último slot, rechazados, variantes).
#    → ❌ REGENERAR: regeneración completa por el flujo de 10 pasos (§A), con
#      `python3 model/optimize_build.py <champ> --crit-min … --pen-min …` para re-derivar
#      la build óptima post-parche (validar contra la publicada con --validar), y `baseline` de nuevo.
# 7b. APLICAR números nuevos donde el motor los reproduce 1:1 (nunca toca builds):
#    python3 model/update_reports.py refresh --patch <X.Xx> --apply
# 7c. Para cada ❌ REGENERAR, generar el esqueleto de reemplazo en directorio aparte
#    (el publicado NO se borra; el autor decide el reemplazo manual):
#    python3 model/update_reports.py borrador --patch <X.Xx>   → reportes/_borradores/
# 7d. Lint de reportes nuevos/externos (ítems alucinados, Ley 0, frontmatter, estilo):
#    python3 model/lint_reportes.py [--strict]
# 8. python3 -m unittest discover -s tests && python3 model/build_bundles.py
#    python3 model/build_db.py && python3 model/update_reports.py check  → y commit.
```

**Regla de oro (v1.6):** una build publicada y aprobada es **definitiva**. Un hotfix se
**anota con su impacto medido** (`update_reports.py`), no se re-deriva la build — salvo que
el triage dé ❌ REGENERAR (Δ de resultado ≥ 5 % o cambio a inputs del spec). Umbrales:
Δ < 2 % ✅ ANOTAR · 2–5 % ⚠️ REVISAR · ≥ 5 % ❌ REGENERAR. El Δ se mide sobre métricas de
**resultado** (DPS/escudos/curas), no sobre stats-input (un HSP −5 % puede diluirse a −1.4 %
de escudo: caso Yuumi 7.3a).

**Caducidad:** los números de este lab son válidos para 7.3 (21-sep-2026) + hotfix 7.3a (29-sep-2026).
Cualquier hotfix 7.3b/7.4 obliga a los pasos 1–8 antes de publicar un reporte nuevo.

## 1b. APÉNDICE: ESCALADO DE TAMAÑO (Cho'Gath/Malphite/Shyvana) — actualizado a 7.3a

# APÉNDICE — ESCALADO DE TAMAÑO (SIZE) en Wild Rift 7.3
### Cho'Gath · Malphite · Shyvana — qué es real, qué es fantasía y cómo se construye

> Investigación completa: todas las fuentes de tamaño del juego (grep exhaustivo de la BD de 186 ítems + fichas de campeones + notas 7.2/7.3). Fecha: 25/09/2026.

---

## 1. LA VERDAD INCÓMODA PRIMERO

**El tamaño, por sí solo, no da defensa.** No reduce daño, no da vida ni resistencias. Lo que hace:
1. **Hitbox más grande**: bloqueas skillshots con el cuerpo (peel real para tus carries) — pero también te vuelves más fácil de golpear (irrelevante si ya eres el tanque).
2. **Intimidación/legibilidad**: el enemigo percibe mal tus rangos de habilidad y su posicionamiento.
3. **EXCEPCIÓN ÚNICA de tu lista: en Cho'Gath el tamaño ES poder mecánico** (ver §3).

Cuando los jugadores dicen "escalar tamaño para ser underivable en teamfights", lo que realmente están escalando son los **paquetes de stats que vienen CON el tamaño**: vidas bonus, resistencias bonus ×1.3, tenacidad, escudos y curas. El tamaño es el indicador visual de que tu build de "ventanas de combate" está online. Y ahí está la clave matemática:

## 2. LAS 5 FUENTES DE TAMAÑO DEL JUEGO (7.3)

| Fuente | Coste | Tamaño | QUÉ MÁS DA (esto es lo que importa) | Tipo |
|---|---|---|---|---|
| **Amaranth's Twinguard** | 3200 | **+20 %** (5 stacks, 1 s c/u en combate) | +300 HP, 50/50 resist → **al máximo: +30 % armadura y +30 % MR y +20 % tenacidad** | Permanente en fight |
| **Gargoyle Stoneplate** | 2900 | +tamaño durante el activo | 200 HP, 45/45, **activo: escudo = 100 + 90 % de tu vida BONUS** (2.5 s, CD 60) | Activo (burst window) |
| **Sterak's Gage** | 3200 | +tamaño 8 s (al activar Lifeline) | 400 HP, 20 % tenacidad base, **+50 % de tu AD base como AD bonus**, Lifeline: escudo = 75 % de vida bonus (<35 % HP, CD 70) | Reactivo (<35 % HP) |
| **Mantle of the Twelfth Hour** | 2550 | +10 % por 5 s (<30 % HP) | **600 HP**, 20 AH, Lifeline: +200-300 HP, +10 % MS, +20 % tenacidad y **regenera 200-400 + 120 % armadura + 120 % MR** (CD 70) | Reactivo (<30 % HP) |
| **Feast de Cho'Gath** | gratis (R) | **+6 % por stack, cap +135 %** | +80/120/160 HP por stack, **+7.7 rango de ataque por stack (cap +75)**, +2.5 rango de R (cap +25), **anchura de E escala con tamaño** | Permanente, infinito* |

\* stacks de minions/monstruos no-épicos: cap 6; de campeones y épicos: **sin cap**.

**Interacción crítica:** Sterak's + Mantle + Twinguard + Gargoyle = **4 ventanas defensivas independientes** (2 reactivas por umbral de vida, 1 de combate prolongado, 1 activa). Bien temporizadas, un tanque pasa de "30 % HP" a "3000 de escudo + 30 % más resistencias + tenacidad 70 % + regen masiva" en 2 segundos. ESO es lo que el enemigo percibe como "imposible de matar" — no el modelo 3D más grande.

## 3. CHO'GATH — el único donde tamaño = daño (matemática completa)

Su R Feast convierte CADA stack en un compuesto de 5 stats. Con R rank 3 (+160 HP/stack):

| Stacks | HP bonus de Feast | Tamaño | Rango extra | R (true damage, con AP 150 y +1500 HP de ítems) |
|---|---|---|---|---|
| 6 (cap de minions) | +960 | +36 % | +46 | 921 |
| 10 | +1600 | +60 % | **+75 (cap)** | 985 |
| 15 | +2400 | +90 % | +75 | 1065 |
| 22 | **+3520** | **+132 %** | +75 | **1177** |

- **R = 600 + 50 % AP + 10 % de tu HP BONUS como daño VERDADERO** → cada ítem de vida double-dipea (tanqueo + ejecutor). A 22 stacks + Heartsteel, la R ejecuta ~1200 de daño verdadero.
- **E Vorpal Spikes: la anchura del cono escala con su tamaño** → a +132 % su E barre teamfights enteras.
- **Rango de ataque +75** = de melee a "casi ranged" (125→200): golpea desde fuera del alcance de muchos melee.
- **Heartsteel (3000g) es su mejor amigo**: golpe cada 20 s por campeón = 140 + 3.5 % vida máx, y **convierte 15 % del daño en HP permanente** → bola de nieve infinita que alimenta la R (+34 HP/proc a 2500 HP; +58 a 7000).
- **Ruta de build (preview del reporte futuro):** Chainlaced/Armored T3 → Heartsteel → Gargoyle → Twinguard → Liandry's/Cryptbloom (AP para R y E) → Mantle. Roles: jungla (Feast temprano con smite-kill de 1200 true vs monstruos) o mid/top.
- **Economía de stacks 7.3:** monstruos épicos más contestables (duración estándar, Baron mid-game buffeado) → cada épico = 1 stack sin cap. Prioriza dragones/herald aunque pierdas CS.

## 4. MALPHITE — la "armadura es daño" (y por qué lo banean 21.9 %)

Meta actual: **WR 52.17 %, ban 21.89 %** — el tanque más respetado del parche. Su kit convierte armadura en TODO:
- Base armor **49 (+5/nivel) = 119 a nivel 15** (la más alta de tu roster).
- **W pasiva:** +25/30/35/40 % de armadura extra; **W activa:** golpes en cono 20-50 + 20 % AD + **15 % armadura (7.3a; era 20 %)** (primer golpe: 40-100 + 40 % AD + **40 % armadura**).
- **E:** 60-210 + 45 % AP + **40 % armadura (7.3a; era 45 %)** AoE + **slow de AS 35-50 %** (anti-ADC duro: −50 % AS a una Jinx/Kalista enemiga = −40 % de su DPS).
- **Iceborn Gauntlet:** el campo de hielo **crece con tu armadura** (AoE de slow permanente).
- P Granite Shield: **11 % de vida máx** como escudo fuera de combate (con 3500 HP = 385 gratis cada 6 s).

**Números de la ruta armor-stack (nivel 15):**

| Etapa | Armadura | E (mágico AoE) | W golpe sostenido | W primer golpe | Escudo pasiva |
|---|---|---|---|---|---|
| Iceborn+Thornmail+Armored Advance | ~274 | 320 | 91 | 210 | 276 |
| + W rank 4 (+40 % bonus armor) | ~336 | 344 | 100 | 234 | 276 |
| + Gargoyle/Twinguard situacional | ~386 | **364** | **108** | **254** | 276+ |

> [!WARNING]
> **7.3a (29-sep-2026) nerfeó a Malphite:** ratio de armadura de W 20→15 %, de E 45→40 % y R CD 75/70/65→85/80/75 s.
> La tabla de arriba YA refleja el hotfix. Su identidad armor-stack sobrevive (sigue siendo el tanque con más ban),
> pero su pico de daño y la frecuencia de su wombo bajaron ~5-8 % / +10 s de CD.

**El tamaño en Malphite:** solo viene de ítems (Gargoyle activo + Twinguard + Sterak's si va fighter). NO tiene tamaño innato — su fantasía de "gigante" es 100 % armadura. Build comunidad validada: **Iceborn → Plated/Mercury's T3 → Thornmail → Zeke's → Gargoyle** (runas Grasp+Demolish+Second Wind+Overgrowth). Ajustes del modelo: vs comps AD puras, **Armored Advance** sobre Thornmail 2.º; Twinguard como 6.º capstone (con su uptime de combate permanente es el ítem de tamaño más consistente del juego). Zeke's potencia a tus carries AP (Diana/Yunara) con su R.

## 5. SHYVANA — tamaño condicional + Sterak's

- Forma dragón de la R: verificar en juego si modifica hitbox (la ficha no lista tamaño; en la transformación PC sí crece visualmente).
- Su ruta de tamaño real es **Sterak's Gage**: Heavy Handed le da **+50 % de su AD base como AD bonus** (62+4.6×14 = 126 base → **+63 AD**) + Lifeline (75 % de vida bonus como escudo) + tamaño/tenacidad 8 s al activarse — perfecto para su patrón de dive (entra, baja de 35 %, escudo + tamaño + sigue pegando).
- Preview de build (reporte completo pendiente): Gunmetal/Plated T3 → **Dusk and Dawn** (comunidad 1.º) → BotRK/Terminus (on-hit) o Rabadon's/Nashor's (AP R-burst) → Sterak's → Gargoyle/Wit's End.
- Con Shyvana el tamaño es cosmetic-utility (peel/intimidación en plena pelea); su "no-mueras" viene del escudo de Sterak's + W (Burnout) + curas de Dusk and Dawn.

## 6. CÓMO INTEGRAR ESTO EN SUS REPORTES COMPLETOS (protocolo)

Cuando pidas el reporte de Cho'Gath, Malphite o Shyvana, el análisis añadirá:
1. **Columna "ventanas de supervivencia"** por build: cuántos segundos de efectividad extra suman Sterak's/Mantle/Gargoyle/Twinguard y con qué CD (la métrica real detrás del "tamaño").
2. **EHP efectivo en ventana** (vida × multiplicador de mitigación con Twinguard al máximo + escudos), no solo EHP estático.
3. Para Cho'Gath: **curva de stacks por minuto** (minions cap 6 + épicos + campeones) y el execute de R resultante en cada punto de la partida.
4. Regla de compra: **Twinguard cuando las fights duran 5+ s** (5 stacks = 5 s), **Gargoyle cuando te burstean en <2 s** (activo inmediato), **Sterak's para fighters que bucean**, **Mantle para tanques que ya tienen 600 HP de base y sufren execute**.

## 7. FUENTES

Grep de "size/tamaño" sobre los 186 ítems de `items_7.3.csv` y las 12 fichas de campeones · notas oficiales 7.3 (Mantle: HP 200→600 y Twinguard: +300 HP base, rework de resistencias) · fichas wr-meta de Cho'Gath (R Feast completo), Malphite (W/E ratios de armadura) y Shyvana. Discrepancia registrada: el texto "Gains 9 Armor (25/30/35/40 %)" de la W de Malphite es ambiguo (¿9 + % del bonus o % del total?) — modelado como % del bonus (conservador), verificar en juego.

## 2. TEMPLATE + GUÍA DE ESTILO (estándar visual obligatorio v1.4)

# TEMPLATE + GUÍA DE ESTILO — Reportes WR-LAB (estándar v1.4)

> **Este archivo es la ley visual de los reportes.** Todo reporte nuevo (o re-estilizado) DEBE seguir
> esta estructura y convenciones al pie de la letra. Referencia canónica viva:
> `reportes/Jinx_WildRift_7.3_Build_Optimizada.md`.
> Regla de oro: cada afirmación lleva número, cada número lleva supuesto, cada supuesto está en §3/§10.

---

## A. GUÍA DE ESTILO (convenciones obligatorias)

### A.1 Estructura general
1. **Frontmatter YAML** (compatible Obsidian/Quartz):
   ```yaml
   ---
   tags:
     - {ROL}          # ADC / Support / Jungla / Mid / Top
     - {CLASE}        # Marksman / Enchanter / Assassin / Fighter / Mage / Tank
     - {ARQUETIPO}    # Crítico / On-hit / AP-Burst / etc.
     - {LANE}         # Bot-Lane / etc.
   version: X.Y
   Status: Borrador | Aprobado
   champion: {Nombre}
   patch: "7.3"
   ---
   ```
2. **Bloque de metadatos** (inmediato, en negritas, una línea por campo):
   `**Fecha del análisis:**` · `**Parche:**` · `**Rol principal:**` · `**Arquetipo:**` · `**Enfoque:**` (1-2 líneas: la tesis de la build).
3. **Callouts Obsidian** (en este orden, tras los metadatos):
   - `> [!NOTE]` **Estado Meta Actual ({rango}, {fecha}):** Win Rate X % | Pick Rate X % | Ban X % | Tendencia ↑↓ | Rol. → **OBLIGATORIO**. Fuente (v1.11): `data/estructurada/champion_winrates.csv` — wr-meta Diamond+, actualizado 2×/día por el vigía (`wrlab.py winrates`); citar de ahí, no de memoria.
   - `> [!TIP]` Variante principal en 2-3 líneas (qué slot cambia, qué se gana/pierde con números). → OBLIGATORIO si existe variante.
   - `> [!DANGER]` Solo en **builds personalizadas de escenario** (ej. Yuumi agresiva, Cho'Gath tamaño): declarar el sacrificio con números ("sacrifica ~X % de Y a cambio de ~Z % más de W").
   - `> [!WARNING]` Datos pendientes de verificar en juego (rangos, mecánicas ambiguas).
4. Separador `---` entre TODAS las secciones numeradas.

### A.2 Encabezados
- Secciones: `## N. TÍTULO EN MAYÚSCULAS` (N = 0…10, fijos, ver §B). Apéndices: `## APÉNDICE A — ...`.
- Subsecciones: `### N.M Título en oración`.
- NUNCA inventar secciones fuera del esqueleto; si una no aplica al arquetipo, dejarla con su número y una nota de adaptación (ej. "§5 — No aplica: el primer ítem de support es la quest").

### A.3 Números y formato
- **Miles con espacio fino:** `2 900`, `17 350 g`, `1 250 g` (NUNCA `2900` ni `2,900`).
- **Porcentajes con espacio:** `25 %`, `100 %`, `+47.9 %`. Decimales con punto: `2.83`, `49.82 %`.
- DPS y oro como enteros; deltas con signo: `+19 %`, `−22 %` (minus U+2212 preferida).
- Ítems y runas en **negrita** en tablas y en primera aparición; habilidades en _cursiva_ o **Q/W/E/R**.
- Veredictos con emoji + número SIEMPRE: ✅ Core/6.º default · ⚠️ Situacional/niche · ❌ Rechazado (motivo numérico).
- Tablas > prosa. Prosa solo para veredictos, notas críticas y plan de juego (bullets con **lead en negrita**).
- Fórmulas y rutas de compra en bloques de código ``` ```.
- Flecha de mejora de botas: `⬆️` + texto "(min 10:00, MISMO slot)".

### A.4 Ley 0 en las tablas (no negociable)
- **Tabla A (Build final):** exactamente **6 filas** = 1 fila de botas (`Berserker's → ⬆️ Gunmetal (min 10:00, MISMO slot)`) + 5 ítems. Columnas: `Slot | Ítem | Oro | Rol en la build`.
- **Tabla B (Ruta de compra):** cronológica, puede tener 7+ filas porque incluye la mejora ⬆️ y los componentes. Columnas: `# | Compra | Oro acum. | Minuto típico`. Incluir **componentes** ("Pickaxe + Noonquiver → **Hexoptics C44**") y **oro acumulado**.
- Toda build publicada pasa `validate_slots()` y se declara en §10 ("Validación del modelo").

### A.5 Adaptaciones por arquetipo
| Arquetipo | §3 Modelo | §0 Resultado del modelo | §5 Primer ítem |
|---|---|---|---|
| ADC crítico / on-hit | DPS autos + procs | DPS 1v1 / 3v3 / vs armadura / vs tanque / heal | Sí (checkpoints 9/12) |
| AP rotación (Diana, mid) | Burst combo + DPS 10 s | DPS sostenido / burst / vs MR | Sí (orden de core) |
| Soportes (Yuumi/Karma) | **Valor-aliado**: escudos, curas, buffs | Escudo E / cura R / **DPS+ al carry** / amp de equipo | No aplica (quest) — declarar |
| Tanques (Cho'Gath/Malphite) | EHP + ventanas + execute R | EHP, mitigación, daño de utilidad | Sí (componente de vida/armadura) |

### A.6 Pie de página (OBLIGATORIO, estructura fija)
```markdown
---

## Pie de página

*Reporte generado el {dd/mm/aaaa} con datos del parche {X.X} ({fecha parche}). WR-LAB v{n}. Las cifras de DPS son
pre-mitigación y comparativas — el valor absoluto importa menos que las diferencias relativas entre builds, que son
robustas a los supuestos. Si Riot publica un {X.X}a/b (hotfix), regenerar datos antes de publicar.*

**Referencias y créditos**

- Notas oficiales del parche {X.X} ({fecha}) y {anteriores relevantes} — © Riot Games, Inc. (wildrift.leagueoflegends.com). {qué aporta}.
- Base de datos de ítems, runas y fichas de campeón — wr-meta.com (proyecto comunitario de JLVD DEV), sincronizada al {fecha}. {qué aporta}.
- Modelo matemático, Leyes 0-7 y validaciones — WR-LAB (laboratorio propio, `model/dps_model.py`), construido sobre las fuentes anteriores.

**Aviso legal:** Wild Rift y League of Legends son marcas registradas de Riot Games, Inc. Este documento es una guía
de comunidad con fines educativos, **no está afiliado, patrocinado ni respaldado por Riot Games**. Los nombres de
ítems, campeones y estadísticas pertenecen a sus respectivos dueños. El análisis y las conclusiones son trabajo
original del autor apoyado en WR-LAB.

---
```

### A.7 Nomenclatura de archivo (vault/sitio)
`{Campeón} — Wild Rift Build Optimizada.md` (título H1 NO se repite en el cuerpo si el frontmatter lleva `champion:`; el H1 lo pone Quartz). Para el lab: `reportes/{Campeón}_WR_{patch}_Build_Optimizada.md`.

### A.8 Bloque de verificación automática de hotfix (gestionado por tooling)
Cuando un hotfix toca (o podría tocar) un reporte publicado, `model/update_reports.py annotate --apply`
inserta/actualiza un bloque **entre marcadores HTML** justo después del bloque de metadatos:

```markdown
<!-- WRLAB-VERIF:{patch}:START — generado por model/update_reports.py · no editar a mano -->
> [!NOTE] {✅|⚠️|❌} Verificación automática ({fecha}) — **{NO requiere regeneración|…} — hotfix {patch}**
> **Cambio directo:** {tipo y detalle, o "ninguno"}.
> **Δ de resultado (conservador):** {métrica pre→post (±%)} · Δ máx **{x} %** (umbrales: anotar 2 %, regenerar 5 %).
> **Build publicada (6 slots, Ley 0):** {slots} — **sin cambios**.
> {ítems de variantes/rechazados cambiados · sistemas relevantes al rol · nota del lab}
> **Veredicto:** {✅ ANOTAR|⚠️ REVISAR|❌ REGENERAR} — {consecuencia}.
<!-- WRLAB-VERIF:{patch}:END -->
```

Reglas: (1) el contenido entre marcadores **no se edita a mano** — se regenera con el tooling;
(2) un bloque por parche verificado (los históricos se conservan encima del nuevo);
(3) el veredicto usa **métricas de resultado** (DPS/escudo/cura), no stats-input;
(4) ❌ REGENERAR es el único veredicto que autoriza re-derivar la build (flujo §A del FRAMEWORK
+ `update_reports.py baseline` al terminar). Los callouts manuales `> [!WARNING] Hotfix…` previos
a v1.6 pueden convivir, pero la constancia canónica es el bloque automático.

---

## B. ESQUELETO CANÓNICO (copiar y llenar)

```markdown
---
tags: [ ... ]
version: 1.0
Status: Borrador
champion: {Nombre}
patch: "7.3"
---
**Fecha del análisis:** {dd/mm/aaaa}
**Parche:** 7.3 (21-sep-2026)
**Rol principal:** {rol}
**Arquetipo:** {arquetipo con 1 línea descriptiva}
**Enfoque:** {tesis de la build en 1-2 líneas con números}

> [!NOTE]
> **Estado Meta Actual (Diamond+, {fecha}):**
> Win Rate {X} % | Pick Rate {X} % | Ban {X} % | Tendencia {↑/↓} | Rol: {roles}.

> [!TIP]
> **Variante principal:** {slot que cambia + trade-off numérico}.

---

## 0. RESUMEN EJECUTIVO

### Tabla A — BUILD FINAL
| Slot | Ítem | Oro | Rol en la build |
|------|------|-----|-----------------|
| 1 (botas) | **{T2} → ⬆️ {T3}** (min 10:00, MISMO slot) | {g} | {stats clave} |
| 2..6 | **{ítem}** | {g} | {stats + pasiva en 1 línea} |

> **Oro total: {N} g** · {AD/AP} {X} · {AS/haste} {X} · {Crit/pen/HSP} {X} · {sustain}

### Tabla B — Ruta de compra cronológica
| # | Compra | Oro acum. | Minuto típico |
|---|--------|-----------|---------------|
| 1 | {start} | 500 | 0:00 |
| … | {componentes} → **{ítem completo}** | {acum} | ~{mm:ss} |
| k | ⬆️ **{T3}** (mismo slot, +1 000 g) | {acum} | ~{13:00} |

### Runas · Hechizos · Habilidades
| Categoría | Elección |
|-----------|----------|
| Keystone | **{runa}** ({números}) |
| {Árbol} 2..4 | **{runa}** ({números}) |
| Secundaria | **{runa A}** ({caso}) / **{runa B}** ({caso}) |
| Hechizos | **{X + Y}** |
| Skills | **{orden}** (R en 5/9/13) |

### Resultado del modelo ({condiciones})
| Escenario | {DPS/Valor} |
|-----------|-----|
| **1v1** (pre-mitigación) | **{N}** |
| **3v3** | **{N}** |
| **vs 120 armadura / MR** | **{N}** |
| **vs Tanque** | **{N}** |
| {sustain/heal/shields} | **{N}** |

> **Titular:** {comparación estelar con % vs la alternativa más común}.

---

## 1. CONTEXTO DEL CAMPEÓN EN ESTE PARCHE
### 1.1 Cambios directos ({champion}) — tabla Stat/Habilidad | Antes | Ahora | Impacto
### 1.2 Cambios sistémicos que le afectan — tabla Sistema | Cambio | Efecto
### 1.3 ¿Sus habilidades escalan con crítico/{stat clave}? — respuesta + implicación

---

## 2. FICHA MATEMÁTICA (spec)
| Parámetro | Valor | Fuente |   (+ líneas de cálculo en negrita: AD lvl 15, bonus fijo, etc.)

---

## 3. MODELO Y FÓRMULAS
```{fórmulas del motor adaptadas al campeón}```
### Supuestos específicos — bullets

---

## 4. LEYES APLICADAS A {CHAMPION}
### Ley 0 — Slots (siempre: declarar 1 botas + 5 ítems y validate_slots PASS)
### Ley 1..7 — solo las que aplican al arquetipo, con tabla/cálculo por ley

---

## 5. ANÁLISIS DEL PRIMER ÍTEM
| Candidato | Oro | DPS lvl 9 1v1 | lvl 9 3v3 | lvl 12 1v1 | lvl 12 3v3 | Nota |
**Veredicto:** {con números y cruce de curvas}. **Nota crítica:** {mitos corregidos}.

---

## 6. BUILD FINAL RANURA POR RANURA
| Slot | Ítem | Justificación matemática |
### Matriz del último slot (situacional)
| Situación | Ítem | Coste | Impacto medido |
### RECHAZADOS (con motivo numérico)
| Ítem | Motivo del rechazo |

---

## 7. RUNAS · HECHIZOS · HABILIDADES
### Keystone: {nombre} — bullets con números + **Alternativas:** en cursiva con caso de uso
### Secundarias — tabla Slot | Runa | Valor estimado
### Hechizos: {X + Y} — por qué
### Orden de habilidades — **{A → B → C}** + bullet por habilidad

---

## 8. COMPARACIÓN CONTRA LAS ALTERNATIVAS
### Tabla maestra ({nivel}, {condiciones})
| Build | Oro | {stats} | 1v1 | 3v3 | vs 120 | vs Tanque | {sustain} |
### Desglose multiplicativo de la diferencia — tabla Factor | Multiplicador | Contribución

---

## 9. PLAN DE JUEGO
### Early (0:00 – 9:00) / ### Mid (9:00 – 16:00) / ### Late (16:00+)
— bullets con **lead en negrita** y números/tiempos
### Reglas del parche que cambian el macro — tabla Regla | Impacto

---

## 10. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS
### Fuentes primarias (mandan) — tabla
### Fuentes secundarias — tabla
### Discrepancias detectadas y resolución — tabla
### Supuestos del modelo (declarados) — bullets
### Contexto meta ({fecha}) — párrafo con cautela de muestra
### Validación del modelo — bullets: `validate_slots(...) → PASS` + test de Caitlyn (1.48125)

---

## APÉNDICE A — POOL DE ÍTEMES DEL ROL: veredicto para {champion}
| Ítem (oro) | Veredicto | Nota |

---

## APÉNDICE B — RUTAS DE COMPRA
```{DEFAULT / SNOWBALL / ANTI-PRESIÓN / VS … en bloque de código con ⬆️ y minutos}```

---

## Pie de página
{estructura fija de A.6}
```

---

## C. CHECKLIST ANTES DE PUBLICAR (Status: Borrador → Aprobado)

- [ ] Frontmatter completo (tags rol/clase/arquetipo/lane, version, Status, champion, patch).
- [ ] Metadatos + callout [!NOTE] con meta real (WR/pick/ban/tendencia + fecha) tomada de `champion_winrates.csv` (el lint avisa si diverge >3 pts del dato actual).
- [ ] Tabla A = 6 filas exactas (1 botas con ⬆️ + 5 ítems); Tabla B con componentes y oro acumulado.
- [ ] `validate_slots()` en PASS declarado en §10.
- [ ] Números con espacio de miles (`2 900`) y `%` con espacio (`25 %`) en TODO el documento.
- [ ] Secciones 0-10 + Apéndices A/B + Pie de página presentes, en orden, con `---` entre ellas.
- [ ] Todo ✅/⚠️/❌ acompañado de número.
- [ ] Discrepancias de fuentes declaradas (notas oficiales > wr-meta).
- [ ] Hotfix verificado (¿7.3a/b?) antes de pasar a Status: Aprobado.
- [ ] Pie de página con referencias Riot/wr-meta/WR-LAB + aviso legal.

## 3. FUENTES Y REGLAS DE VERIFICACIÓN

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

## 3b. HOTFIX 7.3a — DIFF COMPLETO (APLICADO A ESTE BUNDLE)

# HOTFIX 7.3a — Cambios completos (despliegue: 29-sep-2026, 09:30–12:00 CN)

> **Fuente:** notas oficiales del servidor chino (lolm.qq.com, docid 15413436308828016227) vía traducción
> comunitaria (r/wildrift, archivado en `data/raw/patch73a_cn_en.txt`).
> **✅ VERIFICADO contra la nota EN oficial** (wildrift.leagueoflegends.com/…/wild-rift-patch-notes-7-3a/,
> publicada el 29-sep-2026, archivada en `data/raw/patch73a_en.html/.txt`): todos los números de campeones,
> ítems y sistemas coinciden con esta tabla. Única discrepancia: la nota EN lista solo **Diadem of Songs**
> (0.5→0.25 %) además de Whispering Circlet; la traducción CN decía "Crown/Diadem" — mandan las notas EN
> (ver FUENTES.md). Typo de la fuente EN: "0.01%a Ability Power" = 0.01 % AP.
> **Estado en el lab:** datos aplicados en specs, motor, apéndices y tests (v1.5+).

## RESUMEN DE INTENCIÓN (traducción del intro oficial)

"Ajustes de balance a campeones e ítems selectos — reforzando a los de bajo rendimiento y devolviendo a
niveles razonables las elecciones dominantes. Ralentización moderada del ritmo de clear de jungla early-mid
y menor resistencia contra split-push/siege continuo. Ajustes a Augments y campeones de ARAM por feedback."

## CAMPEONES

| Campeón | Tipo | Cambios |
|---|---|---|
| **Hwei** | NERF | Pasiva: 33–333 + 33 % AP → **40–285 + 30 % AP** · (1-1) Fire: 50/90/130/170 + 75 % AP → **50/85/120/155 + 70 % AP** · (1-2) amp por vida faltante: 150/200/250/300 % → **100/150/200/250 %** · (4) detonación: 250/350/450 + 75 % → **200/300/400 + 70 % AP** |
| **Samira** | BUFF | HP growth 128→**136** · armor growth 5→**5.5** · MR growth 1.4→**2** · pasiva melee ratios ~×1.65 · Flair 110→**125 % AD** · R por tiro 40→**50 % AD** |
| **Rammus** | NERF | Armor base 45→**40** · W bonus armor 45/50/55/60→**30/40/50/60 %** |
| **Malphite** ⚠️lab | NERF | W ratio de armadura 20→**15 %** · E ratio de armadura 45→**40 %** · R CD 75/70/65→**85/80/75 s** |
| **Tristana** | BUFF | Q AS 50/75/100/125→**60/80/100/120 %** · W CD 22/20/18/16→**20/18/16/14** · E base 80/100/120/140→**80/110/140/170**, ratio 100→**120 %**, amp crit 40→**50 %**, amp daño crit 40→**50 %** |
| **Draven** | BUFF | Q 80-110→**90-120 % AD** · W AS 20-35→**25-40 %** · R 130→**150 % AD** |
| **Caitlyn** ⚠️apéndice | NERF | **AS growth 0.04→0.025** · Headshot ratio 60–100→**60–90 % AD** |
| **Senna** ⚠️apéndice | AJUSTE | AS ratio/base 0.4→**0.3** · Base Bonus AS 0.6→**1.1** · AS growth 0.05→**0.025** · la AS bonus reduce menos el wind-up |
| **Syndra** | NERF | Nodos de pasiva 40/60/80/100/120→**50/75/100/125/150** · W ratio 60→**50 %** · slow fijo **25 %** |
| **Swain** | AJUSTE | Pasiva heal 3–4.5 %+0.5 % AP→**4.5–6 % + 0.2 % AP** · E return ratio 25→**40 % AP** |
| **Yuumi** ⚠️lab | NERF | W Best Friend HSP: 8/9/10/11 % + 0.02 % AP → **6/7/8/9 % + 0.01 % AP** |
| **Viego** | BUFF | Q pasiva 2-5→**3-6 %** · crit ratio 80→**85 %** · R crit scaling 50→**70 %** |

## ÍTEMS

| Ítem | Tipo | Cambios |
|---|---|---|
| **Yun Tal Wildarrows** ⚠️lab | BUFF | AS 25→**35 %** · Flurry: +25→**35 % AS**, CD 20→**25 s** |
| **Whispering Circlet** | NERF | Harmonize HSP: 0.5→**0.25 % del maná máx** |
| **Crown/Diadem of Songs** ⚠️lab | NERF | Harmonize HSP: 0.5→**0.25 % del maná máx** ("deja de ser BiS de enchanter; vuelve opcional-situacional") |
| **Death's Dance** | NERF | Coste 3 200→**3 300 g** |

## MAPA Y SISTEMAS

| Sistema | Cambio | Impacto en el lab |
|---|---|---|
| **Smite burn vs monstruos** | 30–198/s → **22–162/s** | Jungla early más lenta → Diana jungla: Nashor's 1.º aún más correcto; Shyvana/Volibear/Cho'Gath jungla: clear early −15-20 % |
| **Nexus** | 5 500 → **4 000 HP** | Partidas terminan antes tras inhibidores |
| **Placas de torreta** | Al perder placa: +30→**+20** arm/MR y 20→**10 s** | **Siege más fácil** → sube el valor de Jinx/Kalista/Yunara (siege) y de Runaan's/Energized |
| ARAM (Augments + Fiddle/Nasus) | varios | Fuera del alcance SR del lab |

## IMPACTO EN REPORTES/SPECS DEL LAB (estado 28/09)

| Archivo | Impacto | Acción |
|---|---|---|
| `reportes/Yuumi_*` | HSP de W: −2 pts y mitad del término AP → E-shield 339→~338 (−0.3 %), R-heal 651→~648. **Build y veredictos intactos** (Censer sigue siendo el rey) | Anotado [!WARNING] en el reporte |
| `metodologia/ESCALADO_DE_TAMANIO.md` | Malphite: E con 336 armor pasa de 361→**344**; W golpe 117→**100**; R cada 85 s | Tabla corregida + nota |
| `champion_attack_speed_7.3.csv` | Filas Caitlyn (0.04→0.025 por nivel) y Senna (0.3/0.3/1.1/0.025) | Corregidas con marca 7.3a |
| `model/dps_model.py` ITEMS | Yun Tal AS 25→35; Death's Dance 3300 | Aplicado |
| `reportes/Kalista_*` | Yun Tal buffeada sigue RECHAZADA para Kalista (sin on-hit, ramp de crit); para **Yunara** (reporte externo) es buff relevante → re-verificar ese reporte | Anotado |
| `reportes/Diana_*` | Smite burn −18 % → clear early más lento (refuerza Nashor's 1.º en jungla) | Anotado |
| `reportes/Jinx_*` | Placas más blandas + Nexus 4000 → siege Jinx MEJORA; ningún cambio directo a Jinx | Anotado |
| Reportes externos (Yunara/Cho'Gath/Shyvana hechos en otro chat) | Yunara: Yun Tal buff + placas (revisar 1.er ítem) · Cho'Gath: smite nerf jungla · Shyvana: smite nerf | Marcar para revisión en su próxima regeneración |
| FRAMEWORK test de Caitlyn | El ejemplo oficial (1.48125) usaba growth 0.04 (pre-7.3a); con 0.025 el resultado esperado a lvl15 con Alacrity+Berserker's es **1.35** | Test actualizado con ambos valores |

## 4. MECÁNICA OFICIAL DE ATTACK SPEED (7.3) + TEST DE CAITLYN

# Mecanica de Attack Speed 7.3 (explicacion oficial)

In Patch 7.3, we made fairly major changes to Attack Speed, so we also want to take this opportunity to fully explain how Attack Speed works. Attack Speed is the stat that determines how often a unit can perform basic attacks. For a champion, Attack Speed can mainly be broken down into the following types:
- Base Attack Speed
- Base Attack Speed is a champion's starting Attack Speed and usually also determines that champion's Attack Speed Ratio.
- Attack Speed Ratio
- Attack Speed Ratio determines how efficiently a champion converts bonus Attack Speed into actual Attack Speed. It converts the bonus Attack Speed a champion gains into real Attack Speed based on a percentage. In most cases, a champion's Attack Speed Ratio is equal to their Base Attack Speed.
- Base Bonus Attack Speed
- Base Bonus Attack Speed is the bonus Attack Speed a champion has as soon as the match begins, and it does not scale with champion level. This means a champion's Attack Speed at level 1 is determined jointly by their Base Attack Speed and Base Bonus Attack Speed.
- Attack Speed per Level
- Attack Speed per Level is the Attack Speed a champion gains as they level up, and it is also treated as bonus Attack Speed in these calculations. (By contrast, other per-level stats, such as Attack Damage per Level, are not treated as bonus Attack Damage and are instead calculated as part of base Attack Damage.) Although Attack Speed per Level is a fixed value, the amount of bonus Attack Speed a champion gains each level is not equal. Bonus Attack Speed gained from leveling each level = Attack Speed per Level ×(0.7 + 0.04 × current level). For example, when a champion levels from 1 to 2, the bonus Attack Speed gained is equal to 74% of their Attack Speed per Level. By max level, the total bonus Attack Speed a champion gains from leveling = 1400% × Attack Speed per Level.
Next, we'll take a closer look at how Attack Speed is calculated. Let's start with a few formulas:
- Total Attack Speed = Base Attack Speed + Attack Speed Ratio × Bonus Attack Speed Bonus Attack Speed = Base Bonus Attack Speed + bonus Attack Speed gained from leveling + bonus Attack Speed gained from other sources such as items, runes, and abilities
Let's use Caitlyn as an example and plug the numbers into the formulas:  
- For Caitlyn, both her Base Attack Speed and Attack Speed Ratio are 0.625, her Base Bonus Attack Speed is 0.28, and her Attack Speed per Level is 0.04.
- At level 1, without any extra items or runes, Caitlyn's only bonus Attack Speed comes from her Base Bonus Attack Speed. So Caitlyn's Attack Speed = Base Attack Speed + Attack Speed Ratio × Base Bonus Attack Speed = 0.625 + 0.625 × 0.28 = 0.8 Assume Caitlyn is at max level, has a fully stacked rune - Legend: Alacrity (granting 18% bonus Attack Speed), and has equipped Berserker's Greaves (granting 35% bonus Attack Speed). Her Attack Speed can then be calculated as follows: 0.625 + 0.625 × (0.28 + 0.04 × 14 + 0.18 + 0.35) = 1.48125. On the stats panel, Attack Speed is displayed with two decimal places: 1.48

## 5. RUNAS (cambios 7.3 + valores)

# Cambios a runas - Wild Rift 7.3 (notas oficiales)

> Lethal Tempo rehecho, Legend: Haste reemplaza a Legend: Tenacity, Ingenious Hunter removida, Conqueror/Demolish ajustados.

RUNE ADJUSTMENTS
Lethal Tempo
Lethal Tempo has been providing too much Attack Speed and bonus range on its own, creating some extreme power swings for marksmen throughout the game. Alongside our marksman item updates, we’re reworking the rune to rely more on synergy with other Attack Speed sources rather than providing so much power by itself. This should make Lethal Tempo a more natural fit for champions who invest heavily in Attack Speed, while keeping its power more consistent and easier to control.
- Landing basic attacks on enemy champions grants stacking Attack Speed, 8% for melee and 6.4% for ranged, up to 6 stacks for 6 seconds. At max stacks, attacks also fire a bullet that deals adaptive damage, 9 - 30 for melee and 6 - 24 for ranged. Each 1% bonus Attack Speed increases this damage by 1% for melee and 0.67% for ranged.
Conqueror
We've standardized Conqueror's Attack Damage and Ability Power scaling. 
- Stats granted per stack: 3–5 Bonus Attack Damage / 4–8 Ability Power (1.25x–1.6x) -> 3–5 Bonus Attack Damage / 5–8.33 Ability Power (standardized to 1.667x) 
Legend: Haste 
With Mercury’s Treads now providing a significant amount of Tenacity, having additional Tenacity readily available through runes can make crowd control too easy to shrug off. We want Tenacity to remain a more deliberate investment so champions who rely on crowd control can still do their jobs. As a result, we’re replacing Legend: Tenacity with Legend: Haste.
- Replaces Legend: Tenacity
- Takedowns and killing monsters and minions grant Ability Haste, up to a maximum of 15 Ability Haste, with each stack granting 1.5 Ability Haste.
Demolish 
To align with turret-related changes such as Crystalline Overgrowth, we're making corresponding adjustments to Demolish. See Battlefield Adjustments for details. 
- After hitting a turret with 3 basic attacks, melee champions deal 85 + 28% maximum Health bonus Physical Damage, while ranged champions deal 50 + 20% maximum Health bonus Physical Damage. 
Ingenious Hunter 
Ingenious Hunter has created some overly powerful synergies with certain items, while barely making an impact with others. To keep the item system in a healthier spot, we’re removing Ingenious Hunter for now. Don’t worry, hunters, we’ll bring it back when the time is right.
- Removed
Legend: Tenacity
- Removed

### 5.2 Runas completas

# Runas Wild Rift - estado 7.3

> Fuente: wr-meta.com (24-sep-2026). OJO: Ingenious Hunter fue REMOVIDA en 7.3 y Legend: Tenacity -> Legend: Haste (ver cambios_runas_7.3.md).
> Lethal Tempo: usar valores oficiales 7.3 (6.4%/stack ranged, bala 6-24, +0.67% por 1% AS bonus), NO el texto de abajo que puede estar desactualizado.

KEYSTONE
Electrocute
Burst Damage
Within 3 seconds, hit the same enemy champion with 3 basick attacks or abilities to cause additional adaptive damage to the target.
Damage value: 40-210 (
) + 
10% extra 
 + 
5% 
Cooldown:
 20-13s (
)
Dark Harvest
Bonus Damage, Stack Amplification
Damaging a champion below 50% health deals adaptive damage and harvests their soul, permanently increasing Dark Harvest's damage by 11.
Dark Harvest damage: 35+ 11 per soul + 
10% bonus 
 + 
5% 
Cooldown:
 20s (Resets to 1s on takedown)
Empowerment
Increased damage against champions
Hitting an enemy champion with 3 consecutive attacks deals bonus 
adaptive
 damage and amplifies your damage dealt by 8% until you leave combat with champions.
Adaptive
 Damage:
 40-165 (
)
Cooldown: 4s.
Damage amplification will only take effect against champions.
Lethal Tempo
Attack Speed
Gain Attack Speed when attacking enemy champions. Stacks up to 6 times. At max stacks deal bonus damage with your attacks.
Each stack 
Attack Speed
 by 
6%
 (
4.8%
 for ranged champions) for 6 seconds.
Max stacks bonus:
 Attacks against non-turrets fire a bullet on hit, dealing 
9–30 adaptive damage
 (
6–20
 for ranged champions). Every 1% bonus 
Attack Speed
 you have increases the damage by 0.5% (0.33% for ranged champions).
Fleet Footwork
Mobility, Heal
Moving, attacking and casting builds Energy stacks. At 100 stacks, your next attack gains 
Attack Speed
, heals you, grants bonus 
Movement Speed. 
If the attack is again st a champion, it also restores Mana or Energy.
Bonus Attack Speed
: 40%
Health Restore:
 15-110 (
) + 
15% bonus
 + 
10%
.
Bonus Movement Speed
: 20% for 1s.
When attacking a champion, restore 8% missing 
mana
 or 8% missing 
energy
.
When attacking minions or monsters, heals for 35% (Melee champions) or 15% (Ranged champions) of the original heal amount.
Conqueror
Stacking Damage, Vamp
Gain stacks of Adaptive Force when hitting a champion with separate attacks or abilities. Stacks up to 6 times. When fully stacked, gain bonus omnivamp.
Per stack: 
3-5 bonus 
 or 
5-8 
 for 6s.
Fully stacked bonus: Melee - 9%, Ranged - 5% bonus 
Omnivamp 
.
Grasp of Undying
Tank, Heal
Every 3s in combat, your next attack on a champion will be enhanced.
Bonus 
magic damage
: 
3.3%
Heal: 
1.3%
Permanently 
health
 increase: 
10
On Ranged champions, the effects are reduced by 60%.
Guardian
Protect, Shield
Guard allies within 350 units of you and allies you target with abilities for 2.5 second(s). While guarding, if you or the ally take more than a certain amount of damage, both of you gain a shield for 1.5 second(s).
Shield: 40–165 (
) + 
6% bonus
 + 
15%
Damage threshold: 70–240 damage taken (
)
Cooldown:
 55–25s (
)
Aery
Poke, Protect
Your attacks and abilities send Aery to a target, damaging enemies or shielding allies.
Damage: 15-70 (
) + 
10% bonus
 + 
5%
Shield: 25-120 (
) + 
10% bonus
 + 
5%
Aery cannot be sent out again until she returns to you.
Arcane Comet
Poke, Stack Amplification
Damaging a champion with an ability hurls a comet at their location. When a comet hits an enemy champion, the next comet's damage increases.
Damage: (15 to 100) + (2 x total hits on enemy champions) + 
10% bonus
 + 
5%
.
Cooldown:
 16-8s (
)
Phase Rush
Mobility, Ability Haste
Using basic attacks or abilities on an enemy champion 3 time(s) within 4s grants 
Movement Speed
 and reduces the remaining cooldown of basic abilities by 20%.
Duration:
 3s.
Movement Speed bonus:
 Melee - 
40%-60%
 (
) | Ranged - 
20-35%
 (
).
Ability Haste:
 10.
Slow Resist:
 60%.
Cooldown:
 21-7s (
)
First Strike
Initiate, Damage Amplification, Bonus Gold
Initiating combat with an enemy champion or dealing damage to them within 0.25s of engaging them in combat grants 
10 gold
 and First Strike for 3s, allowing you to deal 
7% bonus true damage
 to them. After the effect ends, gain bonus 
gold
 based on the bonus damage dealt for its duration.
If you do not deal damage to the enemy champion within 0.25s of engaging them in combat, First Strike will go into a 10-second cooldown.
Bonus gold:
Melee: 65% of bonus damage.
Ranged: 45% of bonus damage.
Cooldown:
 20-30s
Ice Overlord
Control, Slow
Immobilizing an enemy champion causes 3 beams to form around them, creating ice beneath them for 3 second(s) and slowing enemies inside. The slow lingers on enemies for 1.5 second(s) after they've left the ice zone. Gain a protective layer of ice around yourself, increasing your defenses. After a brief delay, the ice explodes, dealing a burst of magic damage around you.
Slow:
 (
1%
 of your 
bonus Health
 + 15%).
Defenses:
 35 + 75% bonus 
Armor
 and 
Magic Resist
. Lasts 2.5 second(s).
Magic damage:
 15–100 (
) + 
5% max
Cooldown:
 20s
DOMINATION
Cheap Shot
Targets movement-impaired enemies
Deals 10-45 bonus 
true damage
 to enemies whose movement is impaired.
Cooldown:
 7s
Sudden Impact
Triggers when in stealth or dashing
Damaging an enemy champion deals a bonus 
15-65 true damage
 after using a dash, leap, blink, teleport, or when exiting stealth for 4s.
The damaging attack/ability gains bonuses at higher levels:
Level 5:
 Deal an additional 
5 true damage
.
Level 9:
 Deal an additional 
5 true damage
 and gain 
10% Movement Speed
 for 1.5s after dealing the damage.
Cooldown:
 10s
Empowered Attack
Triggers on attack
Every 8 seconds, the next attack will be empowered, dealing 20-60 bonus 
adaptive
 damage (
) to anemy champions. Ranged champions deal 80% damage.
Chain Assault
Triggers on attack after hitting a target with an ability
Hitting an enemy champion with an active ability applies a mark to them, causing your next 2 attacks or active ability casts against them to deal bonus 
adaptive damage
 equal to (12-38 (
) + 
3% bonus 
 + 
1.5%
).
Cooldown:
 15s
Tyrant
Deal damage to low Health enemies
When damaging a champion below 50% Health, deal (20-70 (
) + 
6% bonus 
 + 
3% 
) bonus 
adaptive damage
.
Cooldown:
 10s
Hubris
Kills temporarily increase Attack Damage/Ability Power
Scoring a takedown against an enemy champion within 3 second(s) of damaging them grants (5 + 1 per champion kill you've scored) 
Adaptive Force
 for 30 second(s).
Eyeball Collection
Kills increase Attack Damage/Ability Power
Gains 
1.5
 or 
3
 after scoring a champion or epic monster takedown, stacking up to 8 times.
Ingenious Hunter
Kills increase Item Ability Haste
Gains 20 Item 
Ability Haste
. For each champion or epic monster takedown you score, gain an additional 5 Item 
Ability Haste
. Stacks up to 5 times.
Relentless Hunter
Kills grant out-of-combat Movement Speed
Gain 
10
 out-of-combat 
Movement Speed
. For each champion or epic monster takedown you score, gain 
2
 out-of-combat 
Movement Speed
. Stacks up to 5 times.
Zombie Ward
Vision control increases Attack Damage/Ability Power
Takedowns on enemy wards spawn a Zombie Ward in its place, granting vision of the surrounding area for 120 seconds. Additionally gain 
3
or 
6
(max 5 stacks). (Assists on enemy wards also grant stacks and spawn Zombie Wards.)
PRECISION
Brutal
Attacks deal on-hit damage
Attacks deal (
5
 + 
6% bonus 
+ 
3% 
) bonus 
adaptive
 damage to enemy champions.
Triumph
Increase damage when low in Health
Champion takedowns restore 
10% of lost health
 and 10% of maximum 
Mana
Energy
and grant 
35 Movement Speed
 for 2 second(s).
Battle Zeal
Increase damage during prolonged battles
Gain 1.4% stacking basic ability damage amplification every 1 second(s) while in combat with a champion. Stacks up to 3 times and only takes effect against enemy champions.
Last Stand
Increase damage when low in Health
When 
health is lower than 60%
, attacks launched at enemy champions deal 5-11% bonus 
adaptive
 damage.
Grants maximum bonus damage when Health is lower than 
30%
Cut Down
Deal more damage to high Health enemies
Your attacks deal 6.57% bonus 
adaptive
 damage to enemy champions with more than 60% Health.
Coup de Grace
Increase damage to low Health enemies
Your attacks deal 8% bonus 
adaptive
 damage to enemy champions with less than 
40% Health
.
Legend: Alacrity
Increase bonus Attack Speed
Gains 
3% Attack Speed
. Takedown monsters, enemy champions, or minions to gain up to an additional 
18% Attack Speed
.
Legend: Haste
Bonus Ability Haste
Gain 
0 Ability Haste
 at the start of the game. Taking down monsters, enemy champions, or minions grants additional Ability Haste bonuses. Total bonus is capped at 
15 Ability Haste
.
Legend: Bloodline
Increase Omnivamp
Gains 
1% Omnivamp 
. Takedown monsters, enemy champions, or minions to gain up to an additional 
7% Omnivamp 
.
RESOLVE
Demolish
Destroy turrets faster
Your third attack against a turret deals bonus 
physical damage
 (85 + 
28% max Health
 for melee champions; 50 + 
20% max Health
 for ranged champions).
Cooldown:
 30s
Font of Life
Team Heal
When your attacks or abilities hit an enemy champion, heal yourself and the lowest Health allied champion nearby.
Ally: Heals for 
1.5% of your max 
 + 
5% of your
You: Heal for 
1% of your max 
 + 
5% of your
Healing is 130% effective if you're a melee champion. (Does not trigger if you or nearby allies are at full Health, or if no allies are nearby.)
Cooldown:
 15s
Courage of the Colossus
Immobilize enemies to gain shields
Gains a 
shield that absorbs
 up to 
25-45 
(
) + 
1% of max Health
 for 3s when immobilizing an enemy champion.
Cooldown:
 18s
Unshakeable
Increase Armor, Magic Resist, and Slow Resist
Gain 3% 
Armor
 and 
Magic Resistance
. For every 1 enemy champion(s) nearby, gain an additional 2% 
Armor
 and 
Magic Resistance
. If the max number of enemy champions are nearby (max: 3), you also gain 
20% Slow Resist
.
Second Wind
Increase sustain
Gain 
5 Health
 every 5 seconds.
After taking damage from an enemy champion, 
regenerate 3 + (1.5% of your missing health) 
 over the next 5 seconds. This effect is doubled for melee champions.
Nullifying Orb
Grant a protective shield
If you take damage from a champion that causes you to fall below 35% of your max Health, gain a 
shield
 that 
absorbs up to 60-180
 (
) damage for 4s.
Cooldown:
 60s
Bone Plating
Anti-Burst Damage
When taking damage from a champion, the current and next 3 champion abilities or attacks against you and within 1.5s deal 
30-60
 (
) less damage.
Cooldown:
 40s
Overgrowth
Increase max Health
For every 3 enemy minions or 3 monster(s) killed nearby, permanently gain 
3 max Health
. Max Health can be increased indefinitely this way. Gain an additional 
3% max Health
 upon reaching 30 stacks.
Revitalize
Empowered heals and shields
Gains a 5% amplification effect when 
Healing
 or granting 
Shields
. If the target's Health is lower than 40%, the effect is amplified by an additional 10%. 
Perseverance
Increase survivability when crowd controlled
Gain 
10% Tenacity
. Gain 10-15 
Armor
 and 
Magic Resistance
 (
) for 1.5 seconds when mmobilized. Refresh duration time when immobilized multiple times.
SORCERY
Axiom Arcanist
Empowered Ultimate Ability
Your ultimate ability has 10% increased damage, 
healing
, and 
shielding
. (AoE damage is reduced to a 5% increase.)
Scoring a takedown on an enemy champion reduces your ultimate ability's remaining cooldown by 7%.
Manaflow Band
Increase Mana
Hitting an enemy champion with and ability or 
empowered
 attack permanently increases your 
max mana 
 by 
30
, up to 
300 mana.
Botanist
Empowered plant effects
When you destroy a plant, gain 
10 gold
 and empowered plant effects. Soulflowers near the turrets also grant additional bonuses.
Honeyfruit:
Heal
 is increased by 
20%
 when consumed.
Scryer's Bloom:
Vision granted
 lasts 20% longer when destroyed.
Blast Cone:
 Gain 
40% Movement Speed
 for 2.5 second(s) after the knockback.
Hextech Flashtraption
Gain short-range movement while Flash is on cooldown
While Flash is on cooldown, it is replaced by Hexflash. Dash a distance based on charge time (max 2s). Entering combat with enemy champions to trigger a 6-second cooldown. 
Cooldown:
 18s
Transcendence
Reduces ability cooldowns
Gain a bonus when reaching the following levels:
At level 1, gain 
5 Ability Haste
;
at level 5, gain bonus 
5 Ability Haste
;
at level 9, after Basic Ability hit the target, reduce 8% the ability's cooldown time.
Cooldown:
 8s
Celerity
Increase Movement Speed
Gain 
2% Movement Speed
. All 
Movement Speed
 bonuses on you are also increased by 
7%
.
Absolute Focus
Gain Attack Damage/Ability Power at high Health
While above 65% Health, gain a bonus 
2–20 Attack Damage
 (
) or 
2–30 Ability Power
 (
) (
Adaptive
).
Scorch
Abilities deal bonus damage
Damaging an enemy champion with an ability burns them, dealing 
21-49 bonus magic damage
 (
) after 1 seconds.
Cooldown:
 8s
Nimbus Cloak

## 6. SISTEMAS DE CAMPO 7.3 (+ ajustes 7.3a: Smite burn, Nexus, placas — ver §3b)

# Sistemas de campo - Wild Rift 7.3 (notas oficiales)

> Jungla/smite, torretas (7000 HP, placas permanentes, Crystalline Overgrowth), minions, Hand of Baron, Lifesteal nuevo stat.

Jungle Adjustments
We’re making a broad set of changes to the jungle this patch, with a few key goals: increase champion diversity, bring clear speeds closer together across different types of junglers, protect jungle resources from laners, and give non-carry junglers more ways to help their team win.
First, we’re shifting a significant portion of the bonus damage junglers deal to monsters with basic attacks and abilities into a persistent burn. This burn benefits from a wider range of stats, allowing fighters, mages, tanks, and other junglers to improve their clear speeds naturally through their builds. Tank junglers, for example, should no longer feel as pressured to build items like Sunfire Aegis just to keep up their clear.
We’re also adjusting the jungle economy. Monsters will grant less base Gold, with more of that Gold shifted into the bonus provided by Smite. At the same time, monsters will be tougher and deal more damage to non-junglers. Together, these changes should make jungle resources harder for laners to take while keeping them valuable for the jungler.
Monster levels will now scale based on the average level of both teams rather than game time. This should keep monster durability more consistent with the state of the match, instead of allowing them to become excessively tanky or squishy.
We’re also moving the jungle healing effect from casting Smite to killing monsters, aligning healing more closely with when junglers receive their Gold and experience.
Epic monsters are getting some attention too. We want major objectives to be worth fighting over without disappearing before teams have a chance to contest them, so we’re standardizing their durability and increasing Baron Nashor’s mid-game rewards. Alongside our turret and minion changes, securing an early Baron should give teams, especially those with non-carry junglers, a more reliable opportunity to turn that advantage into meaningful map pressure.
And finally, we’re giving junglers a little more control when it matters most: Smite is getting stronger. Smite will now upgrade twice as you consume reward stacks, eventually reaching one thousand four hundred damage. Combined with increased monster resistances, this should make objectives harder for non-junglers to steal and give junglers a bit more reliability in those high-pressure objective fights.
Smite Adjustments
- [New] Champions with Smite deal 30-225 (Scale with Level) + 10% Bonus Attack Damage + 12% Ability Power + 20% Bonus Armor + 20% Bonus Magic Resistance + 3% Bonus Health True damage. After you stop attacking, this damage continues up to 2 more times. Champions also heal for 5 - 35 each second, scaling with champion level.
- [Removed] Champions with Smite deal bonus ability and basic attack damage to monsters.
- [New] Non-epic monsters deal 50% damage to champions with Smite.
- [Removed] Casting Smite restores Health.
- [New] Killing a large monster restores 100–260 Health to the killer (scales with monster level, reaching the maximum at level 9).
Jungle Economy Adjustments
[Removed] Monster gold scaling.
Eco Protection adjustments:
- Champions with Smite gain 1 stack every 20 seconds. Consuming 1 stack when clearing a monster camp grants an additional 45 gold, stacking up to 3 times.
- Catch-up mechanic: when your team's total gold is below 90% of the enemy team's total gold and your own gold is less than or equal to 95% of your team's average gold, consuming 1 stack grants 70 gold.
Jungler minion penalty:
- Champions with Smite gain 30% - 100% of lane experience, increasing over time once per minute and reaching 100% at 15 minutes.
- If a jungler gains more than 40% as much gold from lanes as from monsters, gold and experience gained from lanes are reduced by 50%. This effect stacks with the previous rule and is removed at 12 minutes.
Lane champion jungling penalty:
- Champions without Smite gain only 50% - 80% experience from monsters, increasing over time once per minute and reaching 80% at 12 minutes.
Smite Upgrade Rules
- Initial damage: 600 true damage
- Upgrade Smite by consuming Eco-system Protection stacks.
- Consume 8 total stacks.
- Upgrade to 1000 true damage.
- Consume 20 total stacks.
- Upgrade to 1400 true damage.
- Afterward, gain 1 Eco-system Protection stack every 30 seconds.
- Gain 5% bonus Movement Speed in the jungle and river, increased to 10% while out of combat.
- Gain an additional 20 bonus gold from each jungle camp.
Jungle Monster Rules
Monster stat growth no longer increases with time and instead scales with the average level of all champions on the map.
Epic jungle monster stats:
- Elemental Dragons (levels 5 - 15):
- Health 4900 - 10900, Attack Damage 70, Armor 59 - 119, Magic Resistance 41 - 81
- Rift Herald (levels 5 - 15):
- Health 7100 - 11100, Attack Damage 100 - 200, Armor 79 - 139, Magic Resistance 52 - 82
- Summoned Rift Herald (levels 5 - 15):
- Health 5300 - 7300, Attack Damage 80 - 130, Armor 54 - 114, Magic Resistance 32 - 62
- Gold granted when the Summoned Rift Herald charges: 200 → 50
- Baron Nashor (levels 9 - 15):
- Health 14000 - 18500, Attack Damage 280 - 490, Armor 96 - 168, Magic Resistance 56 - 98
- Basic attacks and abilities that hit enemy champions apply a debuff that reduces Armor and Magic Resistance by 0.5, stacking up to 100 times and lasting 8 seconds. Basic attacks add 1 stack, and abilities add 2 stacks.
- Energy Surge Attack Damage ratio: 60% → 30%
- Corrosive Fluid Attack Damage ratio: 100% → 50%
- Sundering Breath Attack Damage ratio: 200% → 100%
- Spike Burst Attack Damage ratio: 100% → 50%
- Elder Dragon (levels 11 - 15): Health 19000 - 20200, Attack Damage 105, Armor 150 - 170, Magic Resistance 95 - 107
Jungle monster stats (levels 1 - 15): 
- Krugs:
- Health 1300 - 3050, Attack Damage 60 - 172, Armor 40, Magic Resistance 35
- Mini Krugs:
- Health 550 - 1560, Attack Damage 20 - 62, Armor 20, Magic Resistance 20
- Gromp:
- Health 1800 - 4390, Attack Damage 55 - 160, Armor 40, Magic Resistance 35
- Blue Sentinel:
- Health 2200 - 4650, Attack Damage 70 - 210, Armor 40, Magic Resistance 35
- Red Brambleback:
- Health 2200 - 4650, Attack Damage 70 - 210, Armor 40, Magic Resistance 35
- Crimson Raptor:
- Health 1000 - 2540, Attack Damage 20 - 55, Armor 40, Magic Resistance 35
- Raptors:
- Health 500 - 1270, Attack Damage 10 - 24, Armor 20, Magic Resistance 20
- Greater Murk Wolf:
- Health 1200 - 3230, Attack Damage 30 - 93, Armor 40, Magic Resistance 35
- Murk Wolves:
- Health 600 - 1510, Attack Damage 10 - 31, Armor 20, Magic Resistance 20
- Rift Scuttler:
- Health 1500 - 3600, Armor 40, Magic Resistance 40
- The first spawn has been moved to 1: 30.
New jungle monster traits:
- Krugs, Crimson Raptors, and Greater Murk Wolves deal bonus physical damage equal to 3% of the target's current Health on attack.
- Gromp, Red Brambleback, and Blue Sentinel deal bonus physical damage equal to 5% of the target's current Health on attack.
Battlefield system Adjustments
Turrets
This season, we’re making some changes to turrets to create a smoother transition out of the laning phase and make every push feel like meaningful progress.
First, all turrets will now have plating, and turret plating will no longer disappear at six minutes. We’re also increasing turret Health across the board. Previously, once plating disappeared, a single mistake could quickly turn a full-Health turret into rubble and abruptly bring the laning phase to an end. Keeping plating around longer should make that transition more gradual while giving you a consistent reward for pushing, even when you can’t take the entire turret.
The additional durability should also make it harder to take multiple plates in a single push, while creating more opportunities to chip away at turrets throughout the game.
We’re also introducing Crystalline Overgrowth, a new mechanic that gives every champion a way to make meaningful progress against turrets, even if they aren’t running Demolish or building specifically for split-pushing.
Over time, crystals will accumulate on turrets. When a champion attacks a turret, the accumulated crystals shatter and deal bonus True Damage based on how much Crystalline Overgrowth has built up. This damage doesn’t depend on the attacker’s stats, and you won’t need to hang around the turret for an extended period to take advantage of it.
Think of it as a mini push waiting for you. Whether you’re constantly pressuring a side lane or only find a brief window to sneak in a few attacks, Crystalline Overgrowth should help those moments make a meaningful dent in the turret.
Crystalline Overgrowth
- All attackable lane turrets are now affected by Crystalline Overgrowth.
- Turrets crystallize over time. A champion's first basic attack detonates all accumulated crystals, dealing True Damage.
- The higher the average level of the attacking team, the higher the crystal detonation damage.
- Cooldown: After a turret spawns, Crystalline Overgrowth has a 50-second cooldown. Once the cooldown ends, crystals begin to accumulate.
- Crystalline Overgrowth remains at its minimum damage for 30 seconds, then scales linearly over 160 seconds until reaching its maximum damage, where it remains indefinitely.
- Minimum damage: 2%–8.7% of the turret's maximum Health (based on the attacking team's level)
- Maximum damage: 3.3%–18.9% of the turret's maximum Health (based on the attacking team's level)
- If an enemy champion is near the turret at the 50-second mark, when Crystalline Overgrowth would normally activate, crystal growth is temporarily suppressed and will not appear. Once all enemy champions leave the area, the crystals will begin to appear and "fast-forward" to the stage they would have reached, making up for the suppressed progress. This is intended to prevent Crystalline Overgrowth from suddenly activating in the middle of a push.
- While the outer turret is still standing, the inner turret and inhibitor turret will not crystallize. Once the outer turret is destroyed, the inner turret begins crystallizing.
- When no minions are within turret range and the turret's damage reduction is active, the crystals cannot be detonated.
Turret Related Adjustments
Turret Adjustments
- All Turrets
- [New] All turrets take 20% increased damage from melee champions.
- Turret plating distribution: Outer turrets, inner turrets, and inhibitor turrets.
- Turret plating now persists permanently.
- Turret plates are tied to Health thresholds. A turret loses 1 plate whenever its Health falls below 90%, 75%, 55%, 30%, and 0%.
- [Removed] When an outer/inner turret is destroyed, the corresponding inner/inhibitor turret no longer gains a 30-second shield.
- [Removed] During the first 2 minutes of the game, Baron Lane and Mid Lane turrets no longer gain 50 bonus Armor and Magic Resist.
- [Removed] During the first 6 minutes of the game, outer turrets no longer gain Armor and Magic Resist based on their remaining Health.
- [Removed] During the first 5 minutes of the game, turrets no longer gain bonus stats when multiple enemy champions are within their attack range.
- [New] Starting at 5:00, outer turret Armor, Magic Resistance, and turret plate Gold rewards begin to decay, up to 4 times.
- Turret plate Gold: -10 every 30 seconds, down to a minimum of 100 Gold
- Armor and Magic Resist: -15 every 30 seconds, down to a minimum of 0
- Whenever a turret plate is destroyed, the turret gains 30 Armor and Magic Resist for 20 seconds. Destroying another plate refreshes the duration. During this time, the turret gains an additional 5 Armor and Magic Resist for each enemy champion within 850 range
- Turret Stats
- Health:
- Outer turret: 3000 → 7000
- Inner turret: 3000 → 4500
- Inhibitor turret: 3200 → 4250
- [Adjusted] Armor and Magic Resist: 60
- [Removed] Gold granted for destroying turrets
- [Adjusted] Turret Plating and Turret Rewards:
- Outer turret: 140 Gold per plate, 700 Gold total
- Inner and inhibitor turrets: 120 Gold per plate, 600 Gold total
- First turret: 150 bonus Gold
- Global bounty for destroying an outer turret: 50 Gold per player
- Global bounty for destroying an inner or inhibitor turret: 25 Gold per player
Battlefield Tempo Adjustments
As part of our broader jungle and objective changes, we’re also updating Hand of Baron to make empowered minion waves more impactful and give each minion type a clearer role when pushing. We’re changing the Attack Damage granted to empowered minions from a percentage increase to a flat value. This should make early Baron takes more rewarding while keeping the buff from scaling too heavily later in the game. Empowered minions will also now have a minimum Movement Speed, preventing powerful Slow effects from bringing Baron-empowered pushes to a crawl.
Hand of Baron
- Melee Minions:
- Reduced damage from champions: 50% - 70% (11:00 - 25:00)
- Reduced damage from minions: 80%
- Attack Damage increase: 10
- Reduced damage from turrets: 25%
- Caster Minion:
- Reduced damage from champions: 50% - 70% (11:00 - 25:00)
- Reduced damage from minions: 20%
- Attack Damage increase: 30
- Reduced damage from turrets: 25%
- Siege Minions:
- Reduced damage from champions: 30%
- Reduced damage from minions: 20%
- Attack Damage increase: 100
- Reduced damage from turrets: 25%
- Cannon Minions:
- Reduced damage from champions: 30%
- Reduced damage from minions: 20%
- Attack Damage increase: 100
- Reduced damage from turrets: 25%
- Super Minions:
- Super Minions are not affected by Hand of Baron.
- All Minions:
- Minions empowered by Hand of Baron now have a minimum Movement Speed of 3.3.
Minions 
Minions are also getting some updates this patch. We want teams that successfully break through an inhibitor turret to be better rewarded for maintaining pressure, allowing empowered waves to steadily build advantages and wear down the enemy team over time. We’re also changing the mid- and late-game minion acceleration effect from out-of-combat Movement Speed to persistent Movement Speed. This should help waves push more consistently later in the game and reduce awkward gaps between them.
Super Minion Aura
Super Minions empower nearby minions based on the number of enemy inhibitor turrets destroyed.
- 1 Turret:
- 35 Armor, 35 Magic Resistance
- 2 Turrets:
- 35 Armor, 35 Magic Resistance
- Attack Damage: 15%
- 3 Turrets:
- 35 Armor, 35 Magic Resistance
- Attack Damage: 40%
[Removed] Super Minions no longer benefit from the Super Minion Aura.
Minion Stats 
Super Minions
- Base Health: 800 → 1100
Cannon Minions
- Damage to structures: Reaches a maximum of 100% at 23:00 → Fixed at 84%
All Minions 
- [New] All minions deal 60% damage to champions.
- [New] Starting at 5:30, minions gain 25 Movement Speed every 150 seconds, up to 6 times.
- [Removed] Starting at 11:00, minions no longer gain 10% out-of-combat Movement Speed per minute.
- Minion experience range: 8 → 10
Minion Push Buffs
The team with the higher total level and a turret advantage in the lane gains a Minion Push Advantage: 
- [New] Bonus damage to minions: (5% + (5% × turret advantage in the lane)) × team average level advantage
- [New] Damage reduction against minions: 1 + (turret advantage in the lane × team average level advantage)
Lifesteal
We’re introducing Lifesteal, a new vamp stat that applies only to basic attacks, on-hit damage, and abilities treated as basic attacks. This gives marksmen a more focused source of sustain that rewards their basic attacks without allowing abilities to generate excessive healing. We also want vamp to remain a relatively scarce source of power. Some champions are defined by their access to strong sustain, and making similar levels of healing too easy for everyone to access can diminish that strength while creating difficult balance cases. Lifesteal gives us a clearer way to separate basic attack-focused sustain from other forms of vamp and reduce the overall availability of broad healing across the game.
- This stat has replaced the previous vamp effects on the following items. See the item sections for details: Mercurial Scimitar, Vampiric Scepter, Bloodthirster, Blade of the Ruined King, and Gunmetal Greaves.

## LIFESTEAL (nuevo stat)

## 7. TABLA OFICIAL DE ATTACK SPEED — 140 CAMPEONES (7.3, con overrides 7.3a marcados)

```csv
champion,Attack Speed Ratio,Base Attack Speed,Base Bonus Attack Speed,Attack Speed per Level
Garen,0.625,0.625,0.28,0.024
Aatrox,0.651,0.651,0.13,0.021
Lux,0.625,0.625,0.2,0.03
Amumu,0.638,0.638,0.25,0.024
Kayn,0.67,0.67,0.2,0.018
Rengar,0.667,0.667,0.2,0.023
Karma,0.625,0.625,0.2,0.0135
Nunu & Willump,0.625,0.625,0.28,0.0122
Wukong,0.625,0.625,0.28,0.028
Vayne,0.658,0.658,0.23,0.03
Ekko,0.625,0.625,0.28,0.031
Orianna,0.658,0.658,0.14,0.032
Diana,0.694,0.694,0.15,0.008
Zoe,0.625,0.625,0.2,0.021
Tryndamere,0.725,0.725,0.1,0.025
Xin Zhao,0.645,0.645,0.24,0.025
Kha'Zix,0.668,0.668,0.2,0.0185
Jinx,0.625,0.625,0.3,0.02
Hecarim,0.67,0.67,0.2,0.016
Yuumi,0.625,0.625,0.2,0.006
Braum,0.644,0.644,0.16,0.03
Jhin,0.625,0.625,0.06,0.032
Aurelion Sol,0.625,0.625,0.2,0.004
Syndra,0.625,0.625,0.2,0.015
Twisted Fate,0.651,0.651,0.15,0.016
Kai'Sa,0.644,0.644,0.17,0.022
Nilah,0.67,0.67,0.21,0.02
Morgana,0.625,0.625,0.2,0.005
Evelynn,0.667,0.667,0.2,0.012
Pantheon,0.658,0.658,0.22,0.02
Akali,0.625,0.625,0.28,0.02
Fiora,0.69,0.69,0.16,0.026
Blitzcrank,0.625,0.625,0.2,0.006
Seraphine,0.699,0.669,0.12,0.017
Mordekaiser,0.625,0.625,0.17,0.008
Annie,0.625,0.625,0.2,0.006
Yasuo,0.67,0.67,0.2,0.04
Ahri,0.625,0.625,0.2,0.02
Zed,0.651,0.651,0.23,0.024
Jax,0.638,0.638,0.15,0.03
Kayle,0.667,0.667,0.13,0.028
Lucian,0.638,0.638,0.25,0.028
Leona,0.625,0.625,0.2,0.021
Tristana,0.694,0.694,0.17,0.02
Teemo,0.69,0.69,0.09,0.03
Sona,0.644,0.644,0.17,0.016
Lulu,0.625,0.625,0.2,0.013
Shyvana,0.638,0.638,0.25,0.012
Vi,0.644,0.644,0.24,0.012
Xayah,0.658,0.658,0.22,0.034
Rakan,0.635,0.635,0.18,0.022
Twitch,0.679,0.679,0.18,0.03
Gwen,0.69,0.69,0.16,0.026
Camille,0.644,0.644,0.24,0.016
Viego,0.658,0.658,0.22,0.025
Volibear,0.7,0.7,0.05,0.014
Lee Sin,0.651,0.651,0.23,0.02
Corki,0.644,0.644,0.17,0.032
Kennen,0.69,0.69,0.09,0.028
Dr. Mundo,0.625,0.625,0.28,0.028
Zyra,0.625,0.625,0.2,0.02
Rammus,0.625,0.625,0.28,0.0185
Nasus,0.638,0.638,0.25,0.024
Miss Fortune,0.656,0.656,0.22,0.032
Zeri,0.625,0.625,0.28,0.024
Sett,0.625,0.625,0.17,0.01
Yone,0.625,0.625,0.28,0.032
Master Yi,0.679,0.679,0.18,0.018
Darius,0.625,0.625,0.17,0.008
Graves,0.7,0.7,0,0.021
Kindred,0.625,0.625,0.28,0.032
Maokai,0.695,0.695,0.15,0.029
Janna,0.625,0.625,0.2,0.022
Poppy,0.625,0.625,0.2,0.021
Draven,0.679,0.679,0.11,0.03
Gnar,0.625,0.625,0.2,0.015
Ashe,0.658,0.658,0.23,0.03
Zilean,0.625,0.625,0.2,0.017
Alistar,0.625,0.625,0.2,0.012
Ambessa,0.625,0.625,0.28,0.012
Malphite,0.638,0.638,0.25,0.04
Nidalee,0.638,0.638,0.18,0.024
Aurora,0.668,0.668,0.12,0.02
Fizz,0.658,0.658,0.22,0.022
Ziggs,0.656,0.656,0.14,0.014
Cho'Gath,0.625,0.625,0.28,0.008
Gragas,0.625,0.625,0.28,0.013
Vladimir,0.658,0.658,0.14,0.0165
Nami,0.644,0.644,0.17,0.02
Riven,0.625,0.625,0.28,0.022
Varus,0.658,0.658,0.22,0.03
Irelia,0.656,0.656,0.22,0.016
Katarina,0.658,0.658,0.22,0.018
Singed,0.625,0.625,0.28,0.016
Soraka,0.625,0.625,0.2,0.012
Ezreal,0.625,0.625,0.28,0.022
Galio,0.625,0.625,0.28,0.007
Akshan,0.4,0.4,0.67,0.04
Jayce,0.658,0.658,0.22,0.021
Urgot,0.625,0.625,0.2,0.031
Kassadin,0.64,0.64,0.25,0.027
Samira,0.658,0.658,0.14,0.03
Bard,0.658,0.658,0.14,0.015
Olaf,0.694,0.694,0.06,0.0326
Sivir,0.625,0.625,0.3,0.01
Milio,0.625,0.625,0.2,0.022
Lissandra,0.625,0.625,0.2,0.01
Kog'Maw,0.665,0.665,0.2,0.03
Caitlyn,0.625,0.625,0.2,0.025 (7.3a: era 0.04)
Rell,0.625,0.625,0.2,0.01
Skarner,0.625,0.625,0.28,0.005
Shen,0.651,0.651,0.23,0.0367
Brand,0.625,0.625,0.2,0.0185
Renekton,0.665,0.665,0.2,0.024
Veigar,0.625,0.625,0.2,0.014
Senna,0.3 (7.3a),0.3 (7.3a),1.1 (7.3a),0.025 (7.3a)
Pyke,0.667,0.667,0.13,0.021
Sion,0.679,0.679,0.18,0.006
Swain,0.625,0.625,0.2,0.012
Heimerdinger,0.625,0.625,0.2,0.01
Talon,0.625,0.625,0.28,0.025
Vel'Koz,0.625,0.625,0.2,0.01
Thresh,0.625,0.625,0.2,0.028
Warwick,0.638,0.638,0.25,0.012
Nautilus,0.612,0.612,0.2,0.0124
Fiddlesticks,0.625,0.625,0.2,0.012
Kalista,0.694,0.694,0.16,0.046
Lillia,0.625,0.625,0.28,0.016
Ornn,0.625,0.625,0.17,0.012
Ryze,0.625,0.625,0.2,0.018
Smolder,0.638,0.638,0.25,0.031
Mel,0.625,0.625,0.2,0.016
Rumble,0.644,0.644,0.24,0.016
Vex,0.625,0.625,0.2,0.01
Viktor,0.658,0.658,0.14,0.02
Taliyah,0.625,0.625,0.2,0.01
Yunara,0.65,0.65,0.23,0.032
Nocturne,0.721,0.721,0.11,0.024
K'Sante,0.625,0.625,0.28,0.021
Norra,0.625,0.625,0.2,0.012
```

### 7.2 Durabilidad 7.3

```csv
champion,Base Health,Base Armor,Armor per Level,Base Magic Resist,Health per Level
Garen,660 → 690,52 → 44,5.8 → 5,,
Aatrox,,,4.5 → 5,40 → 36,
Rengar,660 → 630,,,,128 → 136
Amumu,,,,,104 → 114
Nunu & Willump,690 → 630,,,,120 → 124
Ekko,630 → 650,,,,120 → 126
Kha’Zix,630 → 640,,,,120 → 128
Xin Zhao,690 → 650,,4.3 → 4.7,,120 → 130
Hecarim,,46 → 42,5 → 5.4,,120 → 130
Braum,690 → 630,52 → 46,,,120 → 136
Jhin,600 → 630,,,,
Evelynn,600 → 630,,,,
Akali,,,,,140 → 150
Pantheon,690 → 660,52 → 48,,,120 → 132
Fiora,650 → 630,46 → 42,4.3 → 4.8,,120 → 130
Blitzcrank,660 → 630,49 → 45,,,120 → 135
Jax,690 → 660,46 → 44,,,120 → 130
Vi,690 → 660,46 → 42,,,112 → 130
Rakan,660 → 640,49 → 42,,,112 → 120
Gwen,690 → 640,52 → 48,,,120 → 136
Camille,690 → 660,,,,128 → 132
Jarvan IV,690 → 660,,,,120 → 130
Viego,660 → 630,,,,128 → 138
Lee Sin,690 → 660,,,,120 → 132
Kennen,660 → 600,,,,120 → 130
Dr. Mundo,720 → 680,,,,112 → 120
Rammus,690 → 670,49 → 45,,,112 → 124
Zeri,630 → 600,,,,128 → 136
Master Yi,,,,,120 → 130
Yone,650 → 630,,,,120 → 130
Darius,650 → 660,52 → 45,,,144 → 148
Alistar,720 → 700,,,,
Aurora,,,,,120 → 132
Kassadin,630 → 650,,,,120 → 132
Graves,660 → 630,,,,128 → 136
Poppy,660 → 630,,,,128 → 136
Draven,630 → 650,,,,128 → 132
Malphite,,,,,120 → 130
Gragas,720 → 660,,,,120 → 140
Riven,690 → 660,46 → 43,,,120 → 125
Irelia,690 → 660,,,,128 → 138
Katarina,630 → 660,,,,
Skarner,690 → 660,,,,128 → 132
Shen,,,,,112 → 124
Galio,660 → 630,,,,144 → 148
Lissandra,,,,,120 → 130
Senna,600 → 570,,,,
Nautilus,720 → 690,,,,
Thresh,,,,,120 → 140
Ornn,720 → 690,,,,120 → 132
Nocturne,,,,,120 → 134
```

## 7b. WIN RATES DEL ROSTER (wr-meta · Diamond+ · las actualiza el vigía 2×/día)

# Win rates del roster — wr-meta (Meta Overview)

> Bucket: **Diamond +** · Datos wr-meta: **Updated 01 OCT 2026 UTC 00:00** · Refrescado por el vigía: 01/10/2026
> Fuente: `wr-meta.com/{id}-{champ}.html` (bloque Meta Overview) vía
> `model/check_patch.py` paso 4 — el MISMO proceso que busca parches nuevos (cron 2×/día
> en `patch-watch.yml`, o manual: `python3 wrlab.py winrates`).
> **Los callouts "Estado Meta Actual" de los reportes se toman de aquí** (TEMPLATE §A.1);
> alerta del vigía si un campeón se mueve ≥ 2 pts de win rate.

| Campeón | Rol | Tier | Win % | Pick % | Ban % | Tendencia | Confianza |
|---|---|---|---|---|---|---|---|
| Caitlyn | DUO | A | 50.44 | 25.95 | 27.38 | ↓ 10 | Confidence High |
| Cho'Gath | SOLO | A | 50.17 | 12.72 | 33.10 | ↓ 2 | Confidence High |
| Cho'Gath | JUNGLE | A | 50.41 | 8.64 | 33.10 | ↓ 3 | Confidence High |
| Diana | MID | B | 47.95 | 1.16 | 0.18 | ↓ 2 | Confidence Low |
| Diana | JUNGLE | A | 50.35 | 1.74 | 0.18 | ↑ 5 | Confidence Low |
| Heimerdinger | MID | A | 50.49 | 1.52 | 1.01 | ↓ 3 | Confidence Low |
| Jinx | DUO | A | 50.55 | 11.30 | 0.41 | 0 | Confidence High |
| Kalista | DUO | S | 51.12 | 4.65 | 4.19 | ↑ 1 | Confidence Med |
| Kalista | SOLO | S+ | 53.01 | 2.05 | 4.19 | ↑ 4 | Confidence Low |
| Karma | SUPPORT | A | 49.19 | 5.13 | 0.38 | ↓ 5 | Confidence Med |
| Malphite | SUPPORT | S+ | 51.51 | 7.30 | 46.65 | ↓ 2 | Confidence Med |
| Malphite | SOLO | S+ | 56.44 | 9.32 | 46.65 | 0 | Confidence High |
| Mordekaiser | SOLO | S | 50.87 | 10.83 | 27.69 | 0 | Confidence High |
| Norra | MID | A | 50.06 | 1.57 | 7.98 | ↑ 1 | Confidence Low |
| Rammus | JUNGLE | S+ | 56.81 | 5.42 | 5.84 | 0 | Confidence Med |
| Seraphine | SUPPORT | A | 49.30 | 6.88 | 0.96 | ↓ 1 | Confidence Med |
| Shyvana | JUNGLE | B | 46.14 | 3.76 | 1.45 | 0 | Confidence Med |
| Sivir | DUO | B | 48.08 | 3.45 | 0.05 | ↓ 1 | Confidence Med |
| Volibear | SOLO | B | 47.53 | 5.87 | 4.65 | ↓ 3 | Confidence Med |
| Volibear | JUNGLE | B | 47.97 | 2.51 | 4.65 | 0 | Confidence Low |
| Yunara | DUO | S | 50.91 | 18.06 | 22.13 | ↑ 1 | Confidence High |
| Yuumi | SUPPORT | A | 48.90 | 10.43 | 34.20 | ↓ 5 | Confidence High |

Roles wr-meta: SOLO = top (Baron Lane) · JUNGLE · MID · DUO = ADC (Dragon Lane) · SUPPORT.
Máquina: `champion_winrates.csv` (mismas filas) · BD: tabla `winrates` (`build_db.py`).
Dato de CONTEXTO meta (secundario): no cambia builds por sí solo — si un movimiento
coincide con un hotfix, el flujo es el de FRAMEWORK §E (triage/annotate).

## 8. BASE DE ÍTEMS 7.3 (compacta — OJO: Boots tier 3 = MISMO slot que su tier 2; Yun Tal y Death's Dance ya con valores 7.3a en el motor)

| Ítem | Oro | Stats | Categorías |
|---|---|---|---|
| Chempunk Chainsword | 2800 | +400 Max Health  /  +45 Attack Damage  /  +15 Ability Haste | FIGHTER ITEMS |
| Manamune | 2900 | +40 Attack Damage  /  +500 Max Mana  /  +15 Ability Haste | FIGHTER ITEMS; ASSASSIN ITEMS; MARKSMAN ITEMS |
| Muramana |  | +40 Attack Damage  /  +1200 Max Mana  /  +15 Ability Haste | FIGHTER ITEMS; ASSASSIN ITEMS; MARKSMAN ITEMS |
| Eclipse | 3000 | +65 Attack Damage  /  +20 Ability Haste | FIGHTER ITEMS |
| Sundered Sky | 3000 | +350 Max Health  /  +40 Attack Damage  /  +15 Ability Haste | FIGHTER ITEMS |
| Experimental Hexplate | 3000 | +400 Max Health  /  +35 Attack Damage  /  +20% Attack Speed | FIGHTER ITEMS |
| Maw of Malmortius | 3000 | +55 Attack Damage  /  +45 Magic Resistance  /  +10 Ability Haste | FIGHTER ITEMS; ASSASSIN ITEMS; MARKSMAN ITEMS |
| Black Cleaver | 3000 | +400 Max Health  /  +40 Attack Damage  /  +20 Ability Haste | FIGHTER ITEMS |
| Titanic Hydra | 3000 | +450 Max Health  /  +40 Attack Damage | FIGHTER ITEMS; DEFENSE ITEMS |
| Stridebreaker | 3100 | +400 Max Health  /  +40 Attack Damage  /  +25% Attack Speed | FIGHTER ITEMS |
| Goredrinker | 3100 | +350 Max Health  /  +40 Attack Damage  /  +15 Ability Haste | FIGHTER ITEMS |
| Mercurial Scimitar | 3100 | +45 Attack Damage  /  +12% Lifesteal  /  +40 Magic Resistance | FIGHTER ITEMS; ASSASSIN ITEMS; MARKSMAN ITEMS |
| Blade of the Ruined King | 3100 | +40 Attack Damage  /  +35% Attack Speed  /  +12% Lifesteal | FIGHTER ITEMS; MARKSMAN ITEMS |
| Serylda's Grudge | 3100 | +50 Attack Damage  /  +35% Armor Penetration  /  +15 Ability Haste | FIGHTER ITEMS; ASSASSIN ITEMS |
| Spear of Shojin | 3100 | +450 Max Health  /  +40 Attack Damage | FIGHTER ITEMS |
| Hullbreaker | 3100 | +400 Max Health  /  +50 Attack Damage | FIGHTER ITEMS |
| Overlord's Bloodmail | 3200 | +450 Max Health  /  +30 Attack Damage | FIGHTER ITEMS; DEFENSE ITEMS |
| Guardian Angel | 3200 | +45 Attack Damage  /  +40 Armor | FIGHTER ITEMS; ASSASSIN ITEMS; MARKSMAN ITEMS; DEFENSE ITEMS |
| Bloodthirster | 3200 | +75 Attack Damage  /  +15% Lifesteal | FIGHTER ITEMS; MARKSMAN ITEMS |
| Sterak's Gage | 3200 | +400 Max Health  /  +20% Tenacity | FIGHTER ITEMS; DEFENSE ITEMS |
| Death's Dance | 3200 | +50 Attack Damage  /  +45 Armor  /  +15 Ability Haste | FIGHTER ITEMS; DEFENSE ITEMS |
| Trinity Force | 3333 | +333 Max Health  /  +36 Attack Damage  /  +30% Attack Speed  /  +15 Ability Haste | FIGHTER ITEMS; MARKSMAN ITEMS |
| Divine Sunderer | 3400 | +425 Max Health  /  +25 Attack Damage  /  +25 Ability Haste | FIGHTER ITEMS |
| Serpent's Fang | 2800 | +50 Attack Damage  /  +10 Ability Haste | ASSASSIN ITEMS |
| Youmuu's Ghostblade | 3000 | +55 Attack Damage  /  +15 Armor Penetration  /  +15 Ability Haste  /  +4% Move Speed | ASSASSIN ITEMS |
| Duskblade of Draktharr | 3000 | +55 Attack Damage  /  +10 Ability Haste | ASSASSIN ITEMS |
| Edge of Night | 3000 | +250 Max Health  /  +50 Attack Damage | ASSASSIN ITEMS |
| The Collector | 3000 | +50 Attack Damage  /  +10 Armor Penetration  /  +25% Critical Rate | ASSASSIN ITEMS; MARKSMAN ITEMS |
| Fiendhunter Bolts | 2650 | +25% Critical Rate  /  +45% Attack Speed  /  +4% Move Speed | MARKSMAN ITEMS |
| Rapid Firecannon | 2650 | +25% Critical Rate  /  +40% Attack Speed  /  +4% Move Speed | MARKSMAN ITEMS |
| Runaan's Hurricane | 2650 | +40% Attack Speed  /  +25% Critical Rate  /  +4% Move Speed | MARKSMAN ITEMS |
| Phantom Dancer | 2650 | +25% Critical Rate  /  +40% Attack Speed  /  +7% Movement Speed | MARKSMAN ITEMS |
| Navori Quickblades | 2650 | +25% Critical Rate  /  +40% Attack Speed  /  +4% Move Speed | MARKSMAN ITEMS |
| Wit's End | 2800 | +50% Attack Speed  /  +45 Magic Resistance  /  +20% Tenacity | MARKSMAN ITEMS |
| Hexoptics C44 | 2900 | +55 Attack Damage  /  +25% Critical Rate | MARKSMAN ITEMS |
| Kraken Slayer | 2900 | +45 Attack Damage  /  +35% Attack Speed  /  +4% Move Speed | MARKSMAN ITEMS |
| Nashor's Tooth | 2900 | +50% Attack Speed  /  +80 Ability Power  /  +15 Ability Haste | MARKSMAN ITEMS; MAGIC ITEMS |
| Statikk Shiv | 3000 | +40 Attack Damage  /  +30% Attack Speed  /  +40 Ability Power  /  +4% Move Speed | MARKSMAN ITEMS; MAGIC ITEMS |
| Guinsoo's Rageblade | 3000 | +35 Attack Damage  /  +30% Attack Speed  /  +30 Ability Power | MARKSMAN ITEMS; MAGIC ITEMS |
| Mortal Reminder | 3000 | +35 Attack Damage  /  +30% Armor Penetration  /  +25% Critical Rate | MARKSMAN ITEMS |
| Essence Reaver | 3000 | +50 Attack Damage  /  +25% Critical Rate  /  +20 Ability Haste | MARKSMAN ITEMS |
| Immortal Shieldbow | 3000 | +55 Attack Damage  /  +25% Critical Rate | MARKSMAN ITEMS |
| Terminus | 3000 | +35 Attack Damage  /  +35% Attack Speed | MARKSMAN ITEMS |
| Stormrazor | 3000 | +50 Attack Damage  /  +25% Critical Rate  /  +20% Attack Speed | MARKSMAN ITEMS |
| Yun Tal Wildarrows | 3100 | +50 Attack Damage  /  +25% Attack Speed | MARKSMAN ITEMS |
| Galeforce | 3100 | +60 Attack Damage  /  +25% Critical Rate  /  +4% Move Speed | MARKSMAN ITEMS |
| Dominik's Regards | 3300 | +35 Attack Damage  /  +35% Armor Penetration  /  +25% Critical Rate | MARKSMAN ITEMS |
| Infinity Edge | 3400 | +75 Attack Damage  /  +25% Critical Rate | MARKSMAN ITEMS |
| Whispering Circlet | 2400 | +200 Max Health  /  +500 Max Mana  /  +50% Mana Regen  /  +8% Heal and Shield Strength | MAGIC ITEMS; SUPPORT ITEMS |
| Diadem of Songs |  | +200 Max Health  /  +1200 Max Mana  /  +50% Mana Regen  /  +8% Heal and Shield Strength | MAGIC ITEMS; SUPPORT ITEMS |
| Redemption | 2450 | +40 Ability Power  /  +50% Mana Regen  /  +10 Ability Haste  /  +8% Heal and Shield Strength | MAGIC ITEMS; SUPPORT ITEMS |
| Imperial Mandate | 2600 | +60 Ability Power  /  +50% Mana Regen  /  +20 Ability Haste | MAGIC ITEMS; SUPPORT ITEMS |
| Oceanid's Trident | 2600 | +200 Max Health  /  +80 Ability Power  /  +10 Ability Haste | MAGIC ITEMS; SUPPORT ITEMS |
| Morellonomicon | 2650 | +300 Max Health  /  +75 Ability Power  /  +15 Ability Haste | MAGIC ITEMS; SUPPORT ITEMS |
| Hextech Roketbelt | 2700 | +250 Max Health  /  +70 Ability Power  /  +20 Ability Haste | MAGIC ITEMS |
| Rylai's Crystal Scepter | 2700 | +350 Max Health  /  +65 Ability Power | MAGIC ITEMS |
| Rod of Ages | 2700 | +350 Max Health  /  +50 Ability Power  /  +400 Max Mana | MAGIC ITEMS |
| Horizon Focus | 2700 | +80 Ability Power  /  +25 Ability Haste | MAGIC ITEMS |
| Malignance | 2700 | +90 Ability Power  /  +500 Max Mana  /  +15 Ability Haste | MAGIC ITEMS |
| Stormsurge | 2800 | +90 Ability Power  /  +15 Magic Penetration  /  +6% Move Speed | MAGIC ITEMS |
| Blackfire Torch | 2800 | +80 Ability Power  /  +500 Maximum Mana  /  +20 Ability Haste | MAGIC ITEMS |
| Luden's Echo | 2800 | +100 Ability Power  /  +500 Max Mana  /  +10 Ability Haste | MAGIC ITEMS |
| Lich Bane | 2800 | +100 Ability Power  /  +10 Ability Haste  /  +5% Move Speed | MAGIC ITEMS |
| Bloodletter's Curse | 2900 | +350 Maximum Health  /  +65 Ability Power  /  +15 Ability Haste | MAGIC ITEMS |
| Banshee's Veil | 3000 | +105 Ability Power  /  +40 Magic Resistance | MAGIC ITEMS; DEFENSE ITEMS |
| Cryptbloom | 3000 | +75 Ability Power  /  +30% Magic Penetration  /  +20 Ability Haste | MAGIC ITEMS; SUPPORT ITEMS |
| Liandry's Torment | 3000 | +300 Max Health  /  +70 Ability Power | MAGIC ITEMS |
| Archangel's Staff | 3000 | +60 Ability Power  /  +500 Max Mana  /  +25 Ability Haste | MAGIC ITEMS |
| Seraph's Embrace |  | +60 Ability Power  /  +1200 Max Mana  /  +25 Ability Haste | MAGIC ITEMS |
| Cosmic Drive | 3000 | +300 Max Health  /  +70 Ability Power  /  +25 Ability Haste  /  +4% Move Speed | MAGIC ITEMS |
| Dusk and Dawn | 3100 | +300 Maximum Health  /  +20% Attack Speed  /  +60 Ability Power  /  +20 Ability Haste | MAGIC ITEMS |
| Infinity Orb | 3100 | +110 Ability Power  /  +15 Magic Penetration | MAGIC ITEMS |
| Riftmaker | 3100 | +350 Max Health  /  +70 Ability Power  /  +15 Ability Haste | MAGIC ITEMS |
| Zhonya's Hourglass | 3300 | +40 Armor  /  +110 Ability Power | MAGIC ITEMS; DEFENSE ITEMS |
| Rabadon's Deathcap | 3400 | +130 Ability Power | MAGIC ITEMS |
| Abyssal Mask | 2400 | +350 Max Health  /  +45 Magic Resistance  /  +10 Ability Haste | DEFENSE ITEMS; SUPPORT ITEMS |
| Zeke's Convergence | 2400 | +300 Max Health  /  +25 Armor  /  +25 Magic Resistance  /  +10 Ability Haste | DEFENSE ITEMS; SUPPORT ITEMS |
| Yordle Trap | 2400 | +200 Max Health  /  +20 Armor  /  +20 Magic Resistance  /  +15 Ability Haste | DEFENSE ITEMS; SUPPORT ITEMS |
| Knight's Vow | 2450 | +200 Max Health  /  +100% Health Regen  /  +40 Armor  /  +10 Ability Haste | DEFENSE ITEMS; SUPPORT ITEMS |
| Frozen Heart | 2550 | +80 Armor  /  +400 Max Mana  /  +20 Ability Haste | DEFENSE ITEMS; SUPPORT ITEMS |
| Mantle of the Twelfth Hour | 2550 | +600 Max Health  /  +20 Ability Haste | DEFENSE ITEMS; SUPPORT ITEMS |
| Locket of the Iron Solari | 2600 | +200 Max Health  /  +30 Armor  /  +30 Magic Resistance  /  +10 Ability Haste | DEFENSE ITEMS; SUPPORT ITEMS |
| Winter's Approach | 2600 | +500 Max Health  /  +500 Max Mana  /  +15 Ability Haste | DEFENSE ITEMS |
| Fimbulwinter |  | +500 Max Health  /  +1200 Max Mana  /  +15 Ability Haste | DEFENSE ITEMS |
| Radiant Virtue | 2650 | +300 Max Health  /  +30 Armor  /  +30 Magic Resistance  /  +10 Ability Haste | DEFENSE ITEMS; SUPPORT ITEMS |
| Thornmail | 2700 | +200 Max Health  /  +75 Armor | DEFENSE ITEMS; SUPPORT ITEMS |
| Dawnshroud | 2700 | +250 Max Health  /  +50 Armor  /  +30 Magic Resistance | DEFENSE ITEMS; SUPPORT ITEMS |
| Hollow Radiance | 2800 | +400 Max Health  /  +40 Magic Resistance  /  +15 Ability Haste | DEFENSE ITEMS |
| Randuin's Omen | 2800 | +400 Max Health  /  +75 Armor | DEFENSE ITEMS |
| Dead Man's Plate | 2800 | +350 Max Health  /  +70 Armor  /  +4% Movement Speed | DEFENSE ITEMS |
| Force of Nature | 2800 | +400 Max Health  /  +60 Magic Resistance  /  +5% Move Speed | DEFENSE ITEMS |
| Heartsteel | 3000 | +700 Max Health  /  +150% Health Regen  /  +20 Ability Haste | DEFENSE ITEMS |
| Kaenic Rookern | 2800 | +350 Max Health  /  +100% Health Regen  /  +85 Magic Resistance | DEFENSE ITEMS |
| Warmog's Armor | 2850 | +700 Max Health  /  +100% Health Regen  /  +20 Ability Haste | DEFENSE ITEMS |
| Gargoyle Stoneplate | 2900 | +200 Max Health  /  +45 Armor  /  +45 Magic Resistance  /  +10 Ability Haste | DEFENSE ITEMS |
| Sunfire Aegis | 2900 | +350 Max Health  /  +40 Armor  /  +15 Ability Haste | DEFENSE ITEMS |
| Unending Despair | 3000 | +300 Max Health  /  +40 Armor  /  +40 Magic Resistance  /  +10 Ability Haste | DEFENSE ITEMS |
| Iceborn Gauntlet | 3000 | +300 Max Health  /  +50 Armor  /  +250 Max Mana  /  +30 Ability Haste | DEFENSE ITEMS |
| Amaranth's Twinguard | 3200 | +300 Max Health  /  +50 Armor  /  +50 Magic Resistance | DEFENSE ITEMS |
| Black Mist Scythe | 0 | +10 Ability Haste | SUPPORT ITEMS |
| Bulwark of the Mountain | 0 | +175 Max Health  /  +10 Ability Haste | SUPPORT ITEMS |
| Echoes of Helia | 2400 | +200 Max Health  /  +40 Ability Power  /  +50% Mana Regen  /  +20 Ability Haste | SUPPORT ITEMS |
| Ardent Censer | 2400 | +50 Ability Power  /  +50% Mana Regen  /  +8% Heal and Shield Strength  /  +4% Move Speed. | SUPPORT ITEMS |
| Staff of Flowing Waters | 2400 | +50 Ability Power  /  +50% Mana Regen  /  +10 Ability Haste  /  +8% Heal and Shield Strength | SUPPORT ITEMS |
| Mikael's Blessing | 2500 | +300 Max Health  /  +50% Mana Regen  /  +15 Ability Haste  /  +9% Heal and Shield Strength | SUPPORT ITEMS |
| Shurelya's Battlesong | 2500 | +55 Ability Power  /  +50% Mana Regeneration  /  +20 Ability Haste  /  +4% Move Speed | SUPPORT ITEMS |
| Harmonic Echo | 2500 | +200 Max Health  /  +40 Ability Power  /  +50% Mana Regen  /  +20 Ability Haste | SUPPORT ITEMS |
| Gluttonous Greaves | 1000 | +45 Move Speed | Boots tier 2 |
| Berserker's Greaves | 1200 | +35% Attack Speed  /  +45 Move Speed | Boots tier 2 |
| Mercury's Treads | 1200 | +150 Max Health  /  +25 Magic Resistance  /  +30 Tenacity  /  +45 Move Speed | Boots tier 2 |
| Plated Steelcaps | 1200 | +150 Max Health  /  +20 Armor  /  +45 Move Speed | Boots tier 2 |
| Ionian Boots of Lucidity | 1000 | +50% Mana Regen  /  +15 Ability Haste  /  +45 Move Speed | Boots tier 2 |
| Boots of Mana | 1200 | +25 Ability Power  /  +8 Magic Penetration  /  +75% Mana Regeneration  /  +45 Move Speed | Boots tier 2 |
| Boots of Dynamism | 1200 | +15 Attack Damage  /  +10 Armor Penetration  /  +45 Move Speed | Boots tier 2 |
| Immortal Treds | 2000 | +45 Move Speed | Boots tier 3 |
| Gunmetal Greaves | 2200 | +50% Attack Speed  /  +45 Move Speed  /  +5% Lifesteal | Boots tier 3 |
| Chainlaced Crushers | 2200 | +150 Max Health  /  +30 Magic Resistance  /  +30% Tenacity  /  +45 Move Speed | Boots tier 3 |
| Armored Advance | 2200 | +150 Max Health  /  +30 Armor  /  +45 Move Speed | Boots tier 3 |
| Crimson Lucidity | 2000 | +75% Mana Regeneration  /  +25 Ability Haste  /  +45 Move Speed | Boots tier 3 |
| Spellslinger's Shoes | 2200 | +35 Ability Power  /  +18 Magic Penetration  /  +8% Magic Penetration  /  +100% Mana Regeneration  /  +45 Move Speed | Boots tier 3 |
| Armorcrusher Boots | 2200 | +25 Attack Damage  /  +12 Armor Penetration  /  +6% Armor Penetration  /  +45 Move Speed | Boots tier 3 |
| Quicksilver Sash | 1100 |  | Mid Tier Items |
| Seeker's Armguard | 1200 | +20 Armor  /  +35 Ability Power | Mid Tier Items |
| Vampiric Scepter | 1200 | +20 Attack Damage  /  +8% Lifesteal | Mid Tier Items |
| Zeal | 1400 | +15% Critical Rate  /  +15% Attack Speed | Mid Tier Items |
| Kircheis Shard | 800 | +20% Attack Speed | Mid Tier Items |
| Serrated Dirk | 1000 | +20 Attack Damage | Mid Tier Items |
| Recurve Bow | 900 | +20% Attack Speed | Mid Tier Items |
| B. F. Sword | 1500 | +40 Attack Damage | Mid Tier Items |
| Last Whisper | 1200 | +15 Attack Damage  /  +15% Armor Penetration | Mid Tier Items |
| Executioner's Calling | 800 | +15 Attack Damage | Mid Tier Items |
| Phage | 1000 | +150 Max Health  /  +15 Attack Damage | Mid Tier Items |
| Caulfield's Warhammer | 1200 | +25 Attack Damage  /  +10 Ability Haste | Mid Tier Items |
| Jaurim's Fist | 1100 | +175 Max Health  /  +15 Attack Damage | Mid Tier Items |
| Aether Wisp | 950 | +35 Ability Power  /  +4% Move Speed | Mid Tier Items |
| Lost Chapter | 1200 | +35 Ability Power  /  +200 Max Mana  /  +10 Ability Haste | Mid Tier Items |
| Fiendish Codex | 900 | +25 Ability Power  /  +10 Ability Haste | Mid Tier Items |
| Blasting Wand | 900 | +40 Ability Power | Mid Tier Items |
| Needlessly Large Rod | 1400 | +65 Ability Power | Mid Tier Items |
| Haunting Guise | 1300 | +200 Max Health  /  +30 Ability Power | Mid Tier Items |
| Sheen | 800 | +10 Ability Haste | Mid Tier Items |
| Oblivion Orb | 800 | +35 Ability Power | Mid Tier Items |
| Bami's Cinder | 1200 | +250 Max Health  /  +5 Ability Haste | Mid Tier Items |
| Spectre's Cowl | 1100 | +175 Max Health  /  +20 Magic Resistance | Mid Tier Items |
| Kindlegem | 1000 | +175 Max Health  /  +10 Ability Haste | Mid Tier Items |
| Giant's Belt | 1000 | +300 Max Health | Mid Tier Items |
| Warden's Mail | 1050 | +35 Armor | Mid Tier Items |
| Catalyst of Aeons | 1100 | +200 Max Health  /  +300 Max Mana | Mid Tier Items |
| Chain Vest | 900 | +40 Armor | Mid Tier Items |
| Bramble Vest | 1000 | +30 Armor | Mid Tier Items |
| Hexdrinker | 1200 | +20 Attack Damage  /  +20 Magic Resistance | Mid Tier Items |
| Negatron Cloak | 900 | +40 Magic Resistance | Mid Tier Items |
| Glacial Shroud | 1000 | +20 Armor  /  +150 Max Mana  /  +10 Ability Haste | Mid Tier Items |
| Winged Moonplate | 900 | +150 Max Health  /  +4% Move Speed | Mid Tier Items |
| Noonquiver | 1300 | +20 Attack Damage  /  +15% Critical Rate | Mid Tier Items |
| Hextech Alternator | 1100 | +45 Ability Power | Mid Tier Items |
| Mejai's Soulstealer | 1800 | +70 Max Health  /  +25 Ability Power | Mid Tier Items |
| Forbidden Idol | 700 | +25% Mana Regen  /  +6% Heal and Shield Strength | Mid Tier Items |
| Fated Ashes | 900 | +40 Ability Power | Mid Tier Items |
| Void Amethyst | 1000 | +20 Ability Power  /  +10% Magic Penetration | Mid Tier Items |
| Verdant Barrier | 1600 | +40 Ability Power  /  +25 Magic Resistance | Mid Tier Items |
| Pickaxe | 800 | +20 Attack Damage | Mid Tier Items |
| Heartbound Axe | 1200 | +20 Attack Damage  /  +15% Attack Speed | Mid Tier Items |
| Bandleglass Mirror | 900 | +20 Ability Power  /  +50% Mana Regen  /  +10 Ability Haste | Mid Tier Items |
| Boots of Speed | 400 | +25 Move Speed. | Basic Items |
| Long Sword | 500 | +12 Attack Damage | Basic Items |
| Brawler's Gloves | 500 | +10% Critical Rate | Basic Items |
| Dagger | 400 | +12% Attack Speed | Basic Items |
| Shimmering Spark | 500 | +50 Max Health | Basic Items |
| Tear of the Goddess | 500 | +200 Max Mana | Basic Items |
| Amplifying Tome | 500 | +20 Ability Power | Basic Items |
| Ruby Crystal | 500 | +150 Max Health | Basic Items |
| Cloth Armor | 500 | +20 Armor | Basic Items |
| Null-Magic Mantle | 500 | +20 Magic Resistance | Basic Items |
| Ring of Revelation | 300 | +5 Ability Haste | Basic Items |
| Relic Shield | 500 | +125 Max Health | Basic Items |
| Spectral Sickle | 500 | Quest: | Basic Items |
| Flash |  |  | Basic Items |
| Ghost |  |  | Basic Items |
| Heal |  |  | Basic Items |
| Barrier |  |  | Basic Items |
| Ignite |  |  | Basic Items |
| Exhaust |  |  | Basic Items |
| Smite |  |  | Basic Items |
| Cleanse |  |  | Basic Items |
| Teleport |  |  | Basic Items |

## 9. SPECS PRECARGADAS (13 campeones, notas 7.3a incluidas)

```python
# -*- coding: utf-8 -*-
"""
WR-LAB · Specs precargadas — lista de campeones del equipo (28-sep-2026, parche 7.3 + hotfix 7.3a)
====================================================================================
Datos: stats base de wr-meta.com (fichas en data/estructurada/campeones/*.md),
AS oficial del apéndice 7.3 (data/estructurada/champion_attack_speed_7.3.csv),
cambios 7.3 (cambios_campeones_7.3.md). dps_model.py convierte estos dicts en ChampSpec.

⚠️ CAMPOS PENDIENTES = verificar en juego antes de publicar un reporte:
   - attack_range no viene en wr-meta; marcado None donde no se pudo confirmar.
   - Volibear ad_growth: la página muestra "62 (56)" — growth real probablemente 3.5-5; VERIFICAR.
"""

SPECS = {
# ══════════════════════ PRINCIPALES DE DAÑO / CARRYS ══════════════════════
"yunara": dict(
    name="Yunara", roles=["ADC (Dragon)"], archetype="crit-aoe-hibrido",
    base_ad=58, ad_growth=3.0, base_as=0.65, as_ratio=0.65, base_bonus_as=0.23, as_per_lvl=0.032,
    ranged=True, attack_range=None,  # verificar (marksman; estimable ~575)
    self_as_buff=0.55,   # Q Spirit Unbound activo: +25/35/45/55% AS por 5s (consume cargas Unleash)
    aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0, uses_magnification=None,
    notes=("Pasiva Vow: críticos hacen +8% daño mágico extra (+8% por cada 100 AP — híbrida). "
           "Q activa: autos empoderadas +10-25 mágico on-hit y SPREAD físico 30% AD a cercanos; en "
           "Transcendent (R, 15s) el spread CRITEA si el auto crita → Runaan's+crítico sinérgico. "
           "7.3: pasiva 10%→8%; Q AS 25/35/45/55. Kraken 'Bring it Down' proca con su spread (nota oficial 7.3). "
           "Modelo: añadir término de spread como AoE condicional + on-hit mágico 10-25+20%AP."),
    model_terms_pending=["spread AoE con crit (Q activa/R)", "pasiva +8% mágico en críticos", "uptime de Q (~5s cada ~6 cargas)"]),

"kalista": dict(
    name="Kalista", roles=["ADC (Dragon)"], archetype="on-hit-ejecutor",
    base_ad=57, ad_growth=5.2, base_as=0.694, as_ratio=0.694, base_bonus_as=0.16, as_per_lvl=0.046,
    ranged=True, attack_range=None,  # verificar (~575)
    self_as_buff=0.0, aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0, uses_magnification=None,
    notes=("7.3: AD base 54→57, growth 5→5.2 (BUFF). AS por nivel 0.046 = el más alto del juego → "
           "escala AS 'gratis' (a lvl15 bonus de niveles ≈ +0.644). Pasiva Martial Poise: dash al atacar "
           "(kiting extremo; no puede atacar mientras se mueve... compensación). E Rend: stacks de lanza, "
           "detona % vida + slow, resetea con kill → ejecutor. Comunidad 7.3: Statikk Shiv 1.er ítem (energized on-hit). "
           "Modelo: término de E por ventana (stacks×AS) + reseteos. REPORTE COMPLETO: reportes/Kalista_WR_7.3_Build_Optimizada.md (build: Gunmetal+Guinsoo+WE+Terminus+BotRK+Runaan's)."),
    model_terms_pending=["E Rend por stack (ratios)", "uptime de dash (kiting = más DPS efectivo)", "Statikk bounce"]),

# ══════════════════════ JUNGLA / MID LANERS ══════════════════════
"diana": dict(
    name="Diana", roles=["Jungla", "Mid"], archetype="ap-assassin-AS (spellblade/Nashor)",
    base_ad=52, ad_growth=3.64, base_as=0.694, as_ratio=0.694, base_bonus_as=0.15, as_per_lvl=0.008,
    ranged=False, attack_range=None,
    self_as_buff=0.65,   # Moonsilver Blade: +30-100% AS 4s tras habilidad (uptime alto en combo; usar 0.65 conservador)
    aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0, uses_magnification=False,
    notes=("Pasiva: tras habilidad +30-100% AS 4s Y cada 3.er golpe = 20+15/nivel + 50% AP mágico en AoE. "
           "Ratio 0.694 alto + AS condicional enorme → Nashor's Tooth (7.3: 50% AS/80 AP) y Dusk and Dawn core; "
           "Infinity Orb (crítico de habilidades 20% vs <40% HP) synergiza con burst. Comunidad: Dusk and Dawn 1.º. "
           "Modelo: rotación Q→E→W→R + autos. REPORTE COMPLETO: reportes/Diana_WR_7.3_Build_Optimizada.md (hallazgo clave: Lethal Tempo > Empowerment; Nashor+D&D core)."),
    model_terms_pending=["rotación de habilidades (ratios AP)", "proc cada 3er golpe (AP)", "uptime real de Moonsilver"]),

"volibear": dict(
    name="Volibear", roles=["Jungla", "Top"], archetype="fighter-hibrido-AS",
    base_ad=62, ad_growth=None,  # ⚠️ wr-meta muestra "62 (56)" — VERIFICAR growth real antes de modelar
    base_as=0.7, as_ratio=0.7, base_bonus_as=0.05, as_per_lvl=0.014,
    ranged=False, attack_range=None,
    self_as_buff=0.25,   # The Relentless Storm: +5% AS por stack ×5 (dañar con auto/habilidad)
    aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0, uses_magnification=False,
    notes=("7.3 nerf: pasiva relámpago 11-80+40%AP → 12-68+40%AP (a 5 stacks las garras encienden = chain on-hit). "
           "W Frenzy: maul + AS/curación al morder marcado. Hibrido AD/AP: items = Dusk and Dawn/Terminus/híbridos AP-fighter. "
           "Modelo: on-hit de pasiva (40% AP) + autos; growth de AD pendiente de verificar."),
    model_terms_pending=["chain lightning pasiva (AP)", "W execute/heal", "verificar ad_growth"]),

"shyvana": dict(
    name="Shyvana", roles=["Jungla"], archetype="fighter-on-hit / AP-burst (dragón)",
    base_ad=62, ad_growth=4.6, base_as=0.638, as_ratio=0.638, base_bonus_as=0.25, as_per_lvl=0.012,
    ranged=False, attack_range=None,
    self_as_buff=0.0, aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0, uses_magnification=False,
    notes=("Q Twin Bite: doble golpe (100% + 20/40/60/80% AD) y los autos reducen su CD 0.5s → spellblade/on-hit. "
           "R dragon: stats bonus + E mejorada. Rutas: AD on-hit (BotRK/Guinsoo/Terminus — sin crit) o AP-burst de R. "
           "Modelo: Q como 'ataque doble' (aa_mult efectivo ~1.3-1.6 según rank con CD refund por AS alta)."),
    model_terms_pending=["Q doble golpe + refund", "EAP vs AD route", "stats de forma dragón"]),

"chogath": dict(
    name="Cho'Gath", roles=["Jungla", "Mid", "Top"], archetype="ap-tank",
    base_ad=62, ad_growth=4.0, base_as=0.625, as_ratio=0.625, base_bonus_as=0.28, as_per_lvl=0.008,
    ranged=False, attack_range=None,
    self_as_buff=0.0, aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0, uses_magnification=False,
    notes=("E Vorpal Spikes: autos liberan picos en cono (daño mágico + slow) = aa_aoe mágico condicional. "
           "R Feast: stacks permanentes de vida + execute de minions/monstruos → escala vida infinita (Heartsteel/FGO). "
           "Jungla 7.3: Smite-burn scalea con stats → tanques limpian bien (cambio sistémico). "
           "Modelo: AP tank — rotación Q/W/E + vida como stat de daño (R/Heartsteel); no modelo de autos."),
    model_terms_pending=["E cono mágico", "vida de Feast (HP como tanqueo+daño R)", "clear de jungla 7.3"]),

"mordekaiser": dict(
    name="Mordekaiser", roles=["Top", "Jungla"], archetype="ap-juggernaut",
    base_ad=54, ad_growth=3.5, base_as=0.625, as_ratio=0.625, base_bonus_as=0.17, as_per_lvl=0.008,
    ranged=False, attack_range=None,
    self_as_buff=0.0, aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0, uses_magnification=False,
    notes=("Pasiva Darkness Rise: 3 golpes → aura de daño mágico sostenido + MS (on-hit de aura). "
           "R Realm of Death: duelo 1v1 robando stats → win-con de equipo. Items AP-fighter (Riftmaker/Liandry/Rylai/FGO). "
           "Modelo: aura pasiva (AP) + Q spammable; sin crit, sin AS relevante."),
    model_terms_pending=["aura Darkness Rise (dps AP)", "Q ratios", "stat steal de R"]),

"malphite": dict(
    name="Malphite", roles=["Top", "Jungla", "Support"], archetype="ap-tank / armor-stack",
    base_ad=58, ad_growth=3.64, base_as=0.625, as_ratio=0.625, base_bonus_as=0.2, as_per_lvl=0.026,
    ranged=False, attack_range=None,
    self_as_buff=0.0, aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0, uses_magnification=False,
    notes=("Meta 7.3: WR 52.17%, BAN 21.89% — el tanque más respetado. Armadura = daño: W pasiva +25-40% armor, "
           "W activa cono 20-50+20%AD+20%ARMOR (primer golpe +40%/40%), E 60-210+45%AP+45%ARMOR + slow de AS 35-50%. "
           "P Granite Shield: 11% vida máx fuera de combate. Iceborn: campo crece con armadura. Base armor 49(+5) = 119 lvl15. "
           "TAMAÑO: solo de ítems (Gargoyle activo, Twinguard, Sterak's, Mantle) — ver metodologia/ESCALADO_DE_TAMANIO.md. "
           "Comunidad: Iceborn → Plated/Mercury T3 → Thornmail → Zeke's → Gargoyle; Grasp+Demolish+Second Wind+Overgrowth."),
    model_terms_pending=["W pasiva (% armor: ¿bonus o total? verificar)", "E slow-AS al DPS enemigo (defensa)", "R engage value"]),

# ══════════════════════ SOPORTES / MAGOS (modelo de autos NO aplica) ══════════════════════
"yuumi": dict(
    name="Yuumi", roles=["Support"], archetype="enchanter-attach",
    base_ad=50, ad_growth=3.64, base_as=0.625, as_ratio=0.625, base_bonus_as=0.2, as_per_lvl=0.006,
    ranged=True, attack_range=None, self_as_buff=0.0, aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0,
    notes=("CORREGIDO (verificado en ficha): en WR Yuumi SÍ compra botas (Ionian → Crimson Lucidity T3). "
           "Análisis por VALOR ALIADO: Heal&Shield Power × uptime de E/Q, maná. Attachada = intargeteable → CERO stats defensivos valen. "
           "Items 7.3 clave: Ardent Censer (2400g, +30% AS y +25 on-hit al aliado = +244 DPS a un ADC típico), "
           "Echoes of Helia, Staff of Flowing Waters, Redemption/Mikael's/Diadem. Best Friend: +8-11% HSP y bonus en Q/R. "
           "⚠️ 7.3a NERF: W Best Friend HSP 8-11+0.02%AP → 6-9+0.01%AP (E-shield ~339→338, build intacta). "
           "REPORTE COMPLETO: reportes/Yuumi_WR_7.3_Build_Optimizada.md"),
    model_terms_pending=["E heal/shield por punto de HSP", "Q daño poke", "economía de maná", "mejor portador (ADC aliado)"]),

"karma": dict(
    name="Karma", roles=["Support", "Mid"], archetype="enchanter-poke",
    base_ad=58, ad_growth=3.64, base_as=0.625, as_ratio=0.625, base_bonus_as=0.2, as_per_lvl=0.0135,
    ranged=True, attack_range=None, self_as_buff=0.0, aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0,
    notes=("Mantra (R) empodera Q/E/W: poke + shield/heal + MS. Support: HSP + haste (Echoes of Helia 2400, "
           "Ardent Censer, Staff of Flowing Waters, Shurelya's); Mid: AP poke (Luden's/Stormsurge/Horizon Focus). "
           "Uptime de E-Mantra = métrica clave (haste items). REPORTE COMPLETO: reportes/Karma_WR_7.3_Build_Optimizada.md (hallazgo: Imperial Mandate = +7% team dmg)."),
    model_terms_pending=["Q/RE daño", "E/RE escudo por HSP", "rotación con haste"]),

"seraphine": dict(
    name="Seraphine", roles=["Support", "Mid"], archetype="enchanter-mage",
    base_ad=52, ad_growth=3.64, base_as=0.699, as_ratio=0.699, base_bonus_as=0.12, as_per_lvl=0.017,
    ranged=True, attack_range=None, self_as_buff=0.0, aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0,
    notes=("Cada 3.ª habilidad = doble cast (pasiva) → haste es su stat multiplicador; W cura/escudo en AoE, "
           "E root, R charm en línea. Support: Echoes of Helia/Diadem/Ardent/Staff; Mid: AP + haste. "
           "Sinergia 7.3: Ardent Censer más barato (2400) y Echoes rehecho (chain 30/35%)."),
    model_terms_pending=["pasiva doble-cast (haste efectivo)", "W AoE heal/shield", "R setup de teamfight"]),

"heimerdinger": dict(
    name="Heimerdinger", roles=["Mid", "Support"], archetype="mage-zona (turrets)",
    base_ad=54, ad_growth=3.5, base_as=0.625, as_ratio=0.625, base_bonus_as=0.2, as_per_lvl=0.01,
    ranged=True, attack_range=None, self_as_buff=0.0, aa_mult=1.0, aa_aoe=False, crit_dmg_mod=1.0,
    notes=("Q turrets = su DPS real (escala AP; las torretas aplican on-hit?). Zona + waveclear: Liandry's/Rylai's/"
           "Cryptbloom; 7.3 relevantísimo: torretas ENEMIGAS con 7000 HP y cristales — su push de oleadas con "
           "turrets + Crystalline Overgrowth = presión de mapa única. Verificar si sus torretas detonan cristales."),
    model_terms_pending=["DPS de torretas (AP)", "E grenade setup", "push con minions 7.3"]),
}

# Roles repetidos (Diana/Cho'Gath) usan el mismo spec; la diferencia jungla/mid va en runas-summoners-orden de items
ROLE_VARIANTS = {
    "diana_jungla":  dict(base="diana",  summoners="Smite+Flash", runes="Lethal Tempo o Conqueror; jungla: Smite upgrades 600→1000→1400 (7.3)"),
    "diana_mid":     dict(base="diana",  summoners="Flash+Ignite/Barrier", runes="Lethal Tempo/Electrocute; First Strike greedy"),
    "chogath_jungla":dict(base="chogath", summoners="Smite+Flash", runes="Grasp/Aftershock-like; Feast stacks tempranas; burn de Smite scalea con HP (7.3)"),
    "chogath_mid":   dict(base="chogath", summoners="Flash+Ignite/TP", runes="Grasp; E-push; R execute"),
    "volibear_jungla":dict(base="volibear", summoners="Smite+Flash", runes="Lethal Tempo/Conqueror"),
    "volibear_top":  dict(base="volibear", summoners="Flash+Ignite/TP", runes="Conqueror/Grasp"),
}
```

## 10. MOTOR DE DPS (con validate_slots — ver Ley 0)

```python
# -*- coding: utf-8 -*-
"""
WR-LAB · Modelo de DPS generalizado — Wild Rift 7.3
====================================================
Motor matemático reutilizable: el mismo con el que se derivó la build de Jinx
(reportes/Jinx_WildRift_7.3_Build_Optimizada.md), parametrizado por campeón.

USO RÁPIDO
    python3 model/dps_model.py            # demo con Jinx: reproduce las tablas del reporte
    from dps_model import *               # como librería para otro campeón (ver §NUEVO CAMPEÓN)

CONVENIOS / SUPUESTOS (idénticos al reporte de Jinx):
    - SLOTS: Wild Rift = 6 slots TOTALES; las botas ocupan UNO. La mejora T2→T3 (min 10:00)
      ocurre EN EL MISMO SLOT: en una build final se lista la T3 (p.ej. Gunmetal), NUNCA
      T2+T3 como dos ítems. eval_build() valida esto automáticamente (validate_slots).
    - DPS pre-mitigación salvo que se pase armor>0.
    - LT y Alacrity a cargas máximas; buff propio de AS del campeón activo (p.ej. Pow-Pow x3).
    - Bala de Lethal Tempo escala con el AS bonus TOTAL (incluye base-bonus y niveles).
    - Los rayos de Runaan's NO heredan multiplicadores del autoataque del campeón (conservador).
    - Penetración % de ítems se SUMA (LDR 35 + Mortal 30 = 65).
    - Kraken promedia missing_hp% configurable (default 50%).
    - Magnification de C44 solo aplica si el campeón ataca a >=550 de rango (flag en spec).

FUENTES DE NÚMEROS: notas oficiales 7.3/7.2 + wr-meta.com 24-sep-2026 + HOTFIX 7.3a (29-sep-2026,
ver data/estructurada/cambios_7.3a.md). Items marcados "7.3a" ya incluyen el hotfix.
"""
from dataclasses import dataclass, field

# ---------------------------------------------------------------- constantes globales 7.3
AS_CAP        = 3.0      # 7.3: 2.5 -> 3.0
CRIT_DMG_BASE = 2.00     # 7.3: 175% -> 200%
CRIT_DMG_IE   = 2.30     # Infinity Edge
LT_MELEE_STACK, LT_RANGED_STACK = 0.08, 0.064   # 6 cargas
LT_BULLET_MIN, LT_BULLET_MAX    = 6, 24          # ranged 6-24 / melee 9-30 (aprox: usamos rango y mod)
LT_BULLET_SCALE = 0.0067                          # +0.67% por 1% de AS bonus (ranged; melee 1%)
ALACRITY_FULL   = 0.21                            # 3% + 18% (el ejemplo oficial de Caitlyn usa 18%)
KRAKEN_RANGED_L15, KRAKEN_MELEE_L15 = 168, 210
KRAKEN_MISSING_BONUS = 0.0075                     # +0.75% por 1% de vida faltante, máx +75%

# ---------------------------------------------------------------- spec de campeón
@dataclass
class ChampSpec:
    name: str
    base_ad: float          # AD nivel 1
    ad_growth: float        # AD por nivel
    base_as: float          # = Attack Speed Ratio en casi todos (apéndice oficial 7.3)
    as_ratio: float
    base_bonus_as: float    # "Base Bonus Attack Speed" del apéndice 7.3
    as_per_lvl: float       # "Attack Speed per Level" del apéndice 7.3
    ranged: bool = True
    attack_range: int = 575
    self_as_buff: float = 0.0        # AS bonusconditional en pelea (Jinx Pow-Pow x3 = 1.10)
    aa_mult: float = 1.0             # multiplicador del autoataque (Jinx cohetes = 1.12)
    aa_aoe: bool = False             # el auto golpea a varios (Jinx = True)
    aoe_max_targets: int = 4         # objetivo del splash que modelamos
    crit_dmg_mod: float = 1.0        # Jhin/Senna/Yasuo/Yone: 0.8-0.9 sobre el daño crítico
    uses_magnification: bool = False # True si siempre ataca a >=550 (Jinx con Fishbones)
    passive_burst_as: float = 0.0    # AS extra que rompe el cap (Get Excited 0.25) — informativo
    mana_pool_l1: float = 345; mana_growth: float = 49   # informativo (gestión de maná)
    notes: str = ""

CHAMPS = {
    "jinx": ChampSpec(
        name="Jinx", base_ad=58, ad_growth=4.0,          # 7.3: growth 4.5->4
        base_as=0.625, as_ratio=0.625, base_bonus_as=0.30, as_per_lvl=0.02,  # apéndice oficial 7.3
        ranged=True, attack_range=575,
        self_as_buff=1.10,           # Pow-Pow rank 4, 3 cargas
        aa_mult=1.12, aa_aoe=True,   # Fishbones 112% en área
        uses_magnification=True,     # rango cohetes 655-700 >= 550
        crit_dmg_mod=1.0, passive_burst_as=0.25,
        notes="W: 220+160%AD CD5s (~150 DPS extra, fuera del modelo). R: 450+120% bAD + 35% missing (7.3 nerf).",
    ),
    # ---- PLANTILLA para el próximo campeón (copiar y llenar desde data/estructurada/) ----
    # "nombre": ChampSpec(
    #     name="...", base_ad=?, ad_growth=?,            # cambios_campeones_7.3.md o wiki
    #     base_as=?, as_ratio=?, base_bonus_as=?, as_per_lvl=?,   # champion_attack_speed_7.3.csv
    #     self_as_buff=?,       # AS condicional de su kit (0 si no tiene)
    #     aa_mult=?, aa_aoe=?,  # modificadores del auto (1.0 default)
    #     crit_dmg_mod=?,       # 0.8 Jhin / 0.9 Yasuo-Yone-Senna / 1.0 resto
    #     uses_magnification=?, # True si su rango efectivo de pelea es >=550
    # ),
}

# ---------------------------------------------------------------- base de ítems (stats que importan al modelo)
@dataclass
class Item:
    key: str; gold: int; ad: float=0; ap: float=0; a_s: float=0; crit: float=0
    pen: float=0; ls: float=0; mr: float=0; armor: float=0; hp: float=0; ah: float=0; ms: float=0
    kraken: bool=False; magnification: bool=False; ie: bool=False
    runaan: bool=False; energized: float=0; onhit_flat: float=0
    onhit_pct_current: float=0; spellblade: float=0; giant_slayer: float=0
    execute_pct: float=0; comment: str=""

def I(key, gold, **kw): return Item(key=key, gold=gold, **kw)

ITEMS = {i.key: i for i in [
    # --- críticos / marksman (7.3) ---
    I("c44",       2900, ad=55, crit=25, magnification=True, comment="+0-10% dmg a distancia (max a 550); +100 rango post-takedown"),
    I("ie",        3400, ad=75, crit=25, ie=True, comment="crítico 200->230%"),
    I("runaan",    2650, a_s=40, crit=25, ms=4, runaan=True, comment="2 rayos 55% AD, critan y aplican on-hit"),
    I("ldr",       3300, ad=35, pen=35, crit=25, giant_slayer=12, comment="+12% vs >=1200 HP bonus"),
    I("mortal",    3000, ad=35, pen=30, crit=25, comment="Grievous Wounds 50%"),
    I("kraken",    2900, ad=45, a_s=35, ms=4, kraken=True, comment="cada 3er golpe 120-168 (rango) +missing HP"),
    I("rfc",       2650, a_s=40, crit=25, ms=4, energized=80, comment="Energized +80 mágico, +150 rango"),
    I("storm",     3000, ad=50, crit=25, a_s=20, energized=120, comment="Energized +120 mágico +45% MS"),
    I("bt",        3200, ad=75, ls=15, comment="overheal->escudo 165-345"),
    I("gale",      3100, ad=60, crit=25, ms=4, comment="dash+misiles 40-125+35% bAD (activo)"),
    I("shieldbow", 3000, ad=55, crit=25, comment="Lifeline: escudo 300-550 bajo 35% (70s)"),
    I("fiend",     2650, a_s=45, crit=25, ms=4, comment="20 ult haste; post-R 3 ataques +50%AS y crit garantizado (80% dmg crit; si ya critaba +15% true)"),
    I("collector", 3000, ad=50, pen=10, crit=25, execute_pct=5, comment="pen plana; ejecuta <5% (+25g)"),
    I("pd",        2650, a_s=40, crit=25, ms=7, comment="stacks 6%AS+1%MS x5; ya NO da AD en 7.3"),
    I("navori",    2650, a_s=40, crit=25, ms=4, comment="ataques -15% CDs básicos (validar mecánica)"),
    I("er",        3000, ad=50, crit=25, ah=20, spellblade=1.0, comment="Spellblade 135% AD base + 0-80 por crit (1.5s ICD)"),
    I("yuntal",    3100, ad=50, a_s=35, crit=25, comment="7.3a BUFF: AS 25->35; Flurry +35%AS CD25; crit 0->25% en 125 ataques"),
    I("manamune",  2900, ad=40, ah=15, comment="+2% mana como AD; Shock 1.5% mana (Muramana)"),
    # --- on-hit ---
    I("witsend",   2800, a_s=50, mr=45, onhit_flat=40, comment="+20% tenacidad"),
    I("terminus",  3000, ad=35, a_s=35, onhit_flat=30, pen=30, comment="stacks light/dark; pen cap 40%"),
    I("botrk",     3100, ad=40, a_s=30, ls=12, onhit_pct_current=6, comment="6% vida actual (min 15)"),
    I("guinsoo",   3000, ad=35, ap=30, a_s=30, onhit_flat=30, comment="cada 3er golpe aplica on-hit 2 veces"),
    I("statikk",   3000, ad=40, ap=40, a_s=30, ms=4, energized=60, comment="cadena 4-7 objetivos, aplica on-hit"),
    # --- defensa/utilidad ---
    I("scimitar",  3100, ad=45, mr=40, ls=12, comment="activo Quicksilver (CC cleanse)"),
    I("ga",        3200, ad=45, armor=40, comment="revivir"),
    I("maw",       3000, ad=55, mr=45, ah=10, comment="escudo vs daño mágico"),
    I("deathsdance",3300, ad=50, armor=45, ah=15, comment="7.3a: coste 3200->3300; Defy/Cauterize"),
    # --- botas (T1 / T2 / T3) ---
    # REGLA DE SLOTS: Wild Rift tiene 6 slots TOTALES y las botas ocupan UNO.
    # Las T3 son MEJORA EN EL MISMO SLOT de su T2 (disponibles desde el min 10:00), NO un ítem extra.
    # Convención del modelo: las listas de build = los 6 slots FINALES -> usar el nombre T3 (p.ej. "Gunmetal").
    # Los checkpoints tempranos usan la T2 (p.ej. "Berserker's"). NUNCA ambas en la misma lista.
    I("boots_speed",  400, comment="T1 base"),
    I("berserker", 1200, a_s=35, comment="T2 ADC; +45 MS; Blessed Blade 10 HP/golpe"),
    I("gunmetal",  2200, a_s=50, ls=5, comment="T3 de Berserker's (mismo slot, min 10:00, +1000g); +45 MS; Blessed 12/golpe; Noxian Gait 7% MS"),
    I("mercury_t", 1200, hp=150, mr=25, comment="T2; 30% tenacidad"),
    I("chainlaced",2200, hp=150, mr=30, comment="T3 de Mercury's (mismo slot); 30% tenacidad + escudo mágico"),
    I("plated",    1200, hp=150, armor=20, comment="T2; Block 10%"),
    I("armored_adv",2200, hp=150, armor=30, comment="T3 de Plated (mismo slot); Block 10% + escudo físico"),
    I("ionian",    1000, ah=15, comment="T2 caster"),
    I("crimson",   2000, ah=25, comment="T3 de Ionian (mismo slot); Noxian Haste"),
    I("boots_mana",1200, ap=25, comment="T2 AP (+8 pen plana)"),
    I("spellslinger",2200, ap=35, comment="T3 de Boots of Mana (mismo slot); +18 pen plana +8% pen; Big Bully"),
    I("boots_dynamism",1200, ad=15, pen=10, comment="T2 AD lethality"),
    I("armorcrusher",2200, ad=25, pen=12, comment="T3 de Dynamism (mismo slot); +6% pen; Cloudwalker"),
    I("gluttonous",1000, comment="T2 adaptive + omnivamp"),
    I("immortal_treads",2000, comment="T3 de Gluttonous (mismo slot); Now and Forever"),
]}

# ── Registro de botas y mapa de mejoras T2→T3 (MISMO SLOT) ──
BOOT_UPGRADES = {  # T3 -> T2 (misma familia, mismo slot)
    "gunmetal": "berserker", "chainlaced": "mercury_t", "armored_adv": "plated",
    "crimson": "ionian", "spellslinger": "boots_mana", "armorcrusher": "boots_dynamism",
    "immortal_treads": "gluttonous",
}
BOOTS_ALL = {"boots_speed"} | set(BOOT_UPGRADES.keys()) | set(BOOT_UPGRADES.values())
# alias legibles
ALIAS = {"C44":"c44","Hexoptics C44":"c44","IE":"ie","Infinity Edge":"ie","Runaan's":"runaan",
         "Runaan's Hurricane":"runaan","LDR":"ldr","Lord Dominik's":"ldr","Mortal Reminder":"mortal",
         "Kraken Slayer":"kraken","Kraken":"kraken","RFC":"rfc","Rapid Firecannon":"rfc",
         "Stormrazor":"storm","Bloodthirster":"bt","BT":"bt","Galeforce":"gale","Shieldbow":"shieldbow",
         "Fiendhunter":"fiend","Fiendhunter Bolts":"fiend","Collector":"collector","Phantom Dancer":"pd",
         "PD":"pd","Navori":"navori","Essence Reaver":"er","ER":"er","Yun Tal":"yuntal",
         "Wit's End":"witsend","WE":"witsend","Terminus":"terminus","BotRK":"botrk","Guinsoo":"guinsoo",
         "Statikk Shiv":"statikk","Mercurial Scimitar":"scimitar","Scimitar":"scimitar",
         "Guardian Angel":"ga","GA":"ga","Maw of Malmortius":"maw","Death's Dance":"deathsdance",
         "Berserker's Greaves":"berserker","Berserker's":"berserker","Gunmetal Greaves":"gunmetal",
         "Gunmetal":"gunmetal","Mercury's Treads":"mercury_t","Chainlaced Crushers":"chainlaced",
         "Plated Steelcaps":"plated","Armored Advance":"armored_adv","Ionian Boots":"ionian",
         "Ionian Boots of Lucidity":"ionian","Boots of Speed":"boots_speed",
         "Crimson Lucidity":"crimson","Crimson":"crimson","Boots of Mana":"boots_mana",
         "Spellslinger's Shoes":"spellslinger","Spellslinger's":"spellslinger",
         "Boots of Dynamism":"boots_dynamism","Armorcrusher Boots":"armorcrusher","Armorcrusher":"armorcrusher",
         "Gluttonous Greaves":"gluttonous","Immortal Treads":"immortal_treads","Immortal Treds":"immortal_treads"}

def validate_slots(items, final=True, strict=True):
    """
    VALIDADOR DE SLOTS — previene el error clásico 'Berserker's + Gunmetal como 2 ítems'.
    Reglas: (1) Wild Rift = 6 slots TOTALES; (2) las botas ocupan UNO; (3) la mejora T2→T3
    ocurre EN EL MISMO SLOT (min 10:00) y NO cuenta como ítem nuevo; (4) una build final
    = 1 botas + 5 ítems. Raises ValueError si la composición es ilegal.
    Devuelve (n_boots, n_items) normalizados.
    """
    keys = [resolve(x).key for x in items]
    boots = [k for k in keys if k in BOOTS_ALL]
    no_boots = [k for k in keys if k not in BOOTS_ALL]
    errs = []
    # misma familia T2+T3 a la vez = doble conteo del slot de botas
    for t3, t2 in BOOT_UPGRADES.items():
        if t3 in boots and t2 in boots:
            errs.append(f"'{t2}' y '{t3}' son el MISMO slot (T2→T3). Usa solo la T3 ('{t3}') en builds finales.")
    if len(boots) > 1 and not errs:
        errs.append(f"{len(boots)} botas distintas en la lista ({boots}) — solo existe 1 slot de botas.")
    if len(items) > 6:
        errs.append(f"{len(items)} entradas > 6 slots totales. ¿Contaste la mejora de botas como ítem aparte?")
    if final and not errs and len(items) != 6:
        errs.append(f"Build final con {len(items)} slots (deben ser 6 = 1 botas + 5 ítems). "
                    f"Si es un checkpoint temprano, llama con final=False.")
    if final and not errs and len(boots) != 1:
        errs.append("Toda build final necesita exactamente 1 botas (idealmente ya en su forma T3).")
    if errs and strict:
        raise ValueError("SLOTS ILEGALES:\n  - " + "\n  - ".join(errs))
    return len(boots), len(no_boots)

# ---- carga de specs precargadas (model/champspecs.py) ----
try:
    try:
        from champspecs import SPECS as _SPECS
    except ImportError:
        import os as _os, sys as _sys
        _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
        from champspecs import SPECS as _SPECS
    import dataclasses as _dc
    _defaults = {f.name: f.default for f in _dc.fields(ChampSpec)}
    for _k, _v in _SPECS.items():
        kw = {}
        for f in _dc.fields(ChampSpec):
            if f.name in _v and _v[f.name] is not None:
                kw[f.name] = _v[f.name]
            elif f.name not in _defaults or _defaults[f.name] is _dc.MISSING:
                kw[f.name] = 0 if f.type in ("float", "int", float, int) else ""
        # campos sin default obligatorio que falten -> 0 con aviso en notes
        for req in ("base_ad", "ad_growth", "base_as", "as_ratio", "base_bonus_as", "as_per_lvl"):
            kw.setdefault(req, 0.0)
        extra = {kk: vv for kk, vv in _v.items() if kk not in {f.name for f in _dc.fields(ChampSpec)}}
        if extra:
            kw["notes"] = kw.get("notes", "") + " || extra: " + "; ".join(f"{a}" for a in (extra.get("roles", []) + [extra.get("archetype", "")]))
        CHAMPS[_k] = ChampSpec(**kw)
except Exception as _e:   # el engine sigue funcionando solo con Jinx si falla la carga
    print(f"[dps_model] aviso: champspecs no cargado ({_e})")

def resolve(name): 
    return ITEMS[name] if name in ITEMS else ITEMS[ALIAS[name]]

# ---------------------------------------------------------------- núcleo matemático
def lvl_as_bonus(spec: ChampSpec, level: int) -> float:
    """AS bonus ganada por niveles (fórmula oficial 7.3): suma de as_per_lvl*(0.7+0.04*L), L=1..level-1."""
    return spec.as_per_lvl * sum(0.7 + 0.04*L for L in range(1, level))

def as_total(spec, items, level=15, lt=True, alacrity=ALACRITY_FULL, self_buff_on=True):
    ai = sum(resolve(x).a_s for x in items)/100.0
    lt_as = (LT_RANGED_STACK if spec.ranged else LT_MELEE_STACK)*6 if lt else 0
    B = (spec.base_bonus_as + lvl_as_bonus(spec, level) + ai + lt_as + alacrity
         + (spec.self_as_buff if self_buff_on else 0))
    raw = spec.base_as + spec.as_ratio * B
    return min(raw, AS_CAP), raw, B

def lt_bullet(spec, level, B):
    lo, hi = (6, 24) if spec.ranged else (9, 30)
    base = lo + (hi-lo)*(level-1)/14
    scale = LT_BULLET_SCALE if spec.ranged else 0.01
    return base * (1 + scale*B*100)

def eval_build(spec, items, level=15, targets=1, armor=0.0, tank=False,
               lt=True, alacrity=ALACRITY_FULL, missing_hp=50, enemy_hp=2200,
               self_buff_on=True, spellblade_uptime=1/1.5, validate=True, ad_extra=0.0):
    """Devuelve métricas de una build completa (lista de nombres/alias de ítems, botas incluidas).
    OJO: 'items' = SLOTS FINALES. Las botas ocupan 1 slot y su mejora T2→T3 es EN EL MISMO SLOT
    (usa el nombre T3, p.ej. 'Gunmetal'; NUNCA listes 'Berserker's'+'Gunmetal' juntos)."""
    if validate:
        validate_slots(items, final=(len(items) == 6))
    its = [resolve(x) for x in items]
    gold = sum(i.gold for i in its)
    ad   = spec.base_ad + spec.ad_growth*(level-1) + sum(i.ad for i in its) + ad_extra
    base_ad = spec.base_ad + spec.ad_growth*(level-1)
    crit = min(sum(i.crit for i in its), 100)/100.0
    pen  = min(sum(i.pen for i in its), 100)
    ls   = sum(i.ls for i in its)
    AS, raw_as, B = as_total(spec, items, level, lt, alacrity, self_buff_on)
    cdmg = (CRIT_DMG_IE if any(i.ie for i in its) else CRIT_DMG_BASE) * spec.crit_dmg_mod
    cmult = 1 + crit*(cdmg-1)
    magn = 1.10 if (spec.uses_magnification and any(i.magnification for i in its)) else 1.0
    amp  = 1 + (sum(i.giant_slayer for i in its)/100.0 if tank else 0)

    hit  = ad * spec.aa_mult * cmult * magn * amp
    d    = AS * hit
    for i in its:
        if i.kraken:
            base = (KRAKEN_RANGED_L15 if spec.ranged else KRAKEN_MELEE_L15) * (level/15)
            d += AS/3 * base * (1 + KRAKEN_MISSING_BONUS*missing_hp)
        if i.energized: d += AS/7 * i.energized
        if i.onhit_flat: d += AS * i.onhit_flat
        if i.onhit_pct_current: d += AS * max(15, i.onhit_pct_current/100*enemy_hp)  # sin cap vs campeones
        if i.spellblade: d += spellblade_uptime * (1.35*base_ad + 80*crit)
    bullet = AS * lt_bullet(spec, level, B) if lt else 0
    d += bullet

    aoe = 0.0
    if targets > 1:
        if spec.aa_aoe:
            aoe += hit * AS * (min(targets, spec.aoe_max_targets)-1)   # splash completo
        if any(i.runaan for i in its):
            aoe += AS * 0.55 * ad * cmult * amp * min(2, targets-1)   # 2 rayos (55% AD c/u)
    mit = 100/(100+armor*(1-pen/100)) if armor > 0 else 1.0
    heal = d*(ls/100)*mit
    keys = {resolve(x).key for x in items}
    if "gunmetal" in keys: heal += 12*AS      # Blessed Blade T3
    if "berserker" in keys: heal += 10*AS     # Blessed Blade T2

    return dict(gold=gold, AD=ad, AS=AS, raw_AS=raw_as, bonus_AS=B, crit=crit*100,
                crit_dmg=cdmg*100, pen=pen, dps1=d*mit, dpsN=(d+aoe)*mit,
                bullet=bullet, heal=heal, overcap=raw_as>AS_CAP)

def compare(spec, builds, level=15, scenarios=(("1v1",dict()),("3v3",dict(targets=3)),
            ("vs120arm",dict(armor=120)),("vsTanque",dict(armor=220,tank=True,enemy_hp=4500)))):
    rows = []
    for bname, items in builds.items():
        base = eval_build(spec, items, level)
        row = {"build": bname, "oro": base["gold"], "AD": round(base["AD"]),
               "AS": f"{base['AS']:.2f}" + ("*" if base["overcap"] else ""),
               "crit": round(base["crit"]), "pen": round(base["pen"]),
               "heal": round(base["heal"])}
        for sname, kw in scenarios:
            row[sname] = round(eval_build(spec, items, level, **kw)["dps1"] if sname!="3v3"
                               else eval_build(spec, items, level, **kw)["dpsN"])
        rows.append(row)
    return rows

# ---------------------------------------------------------------- demo: Jinx 7.3 (reproduce el reporte)
BUILDS_JINX = {
    "A2. Tu build viable (Ber+Kraken+RFC+Runaan+IE+BT)": ["Berserker's","Kraken","RFC","Runaan's","IE","BT"],
    "B. Meta comunidad (Gun+C44+Runaan+IE+LDR+Gale)":     ["Gunmetal","C44","Runaan's","IE","LDR","Galeforce"],
    "C. OPTIMA Kraken (Gun+C44+Runaan+IE+LDR+Kraken)":    ["Gunmetal","C44","Runaan's","IE","LDR","Kraken"],
    "D. OPTIMA BT (Gun+C44+Runaan+IE+LDR+BT)":            ["Gunmetal","C44","Runaan's","IE","LDR","BT"],
    "E. OPTIMA Scimitar (Gun+C44+Runaan+IE+LDR+Scim)":    ["Gunmetal","C44","Runaan's","IE","LDR","Scimitar"],
    "F. On-hit (Gun+Kraken+WE+Terminus+BotRK+Runaan)":    ["Gunmetal","Kraken","WE","Terminus","BotRK","Runaan's"],
}

if __name__ == "__main__":
    spec = CHAMPS["jinx"]
    print(f"=== WR-LAB · DPS {spec.name} nivel 15 (LT full, Alacrity full, {spec.notes[:40]}...) ===")
    print(f"{'BUILD':<52}{'oro':>6}{'AD':>5}{'AS':>6}{'crit':>5}{'pen':>4}{'1v1':>7}{'3v3':>8}{'vs120':>7}{'vsTanq':>8}{'heal':>6}")
    for row in compare(spec, BUILDS_JINX):
        print(f"{row['build']:<52}{row['oro']:>6}{row['AD']:>5}{row['AS']:>6}{row['crit']:>5}"
              f"{row['pen']:>4}{row['1v1']:>7}{row['3v3']:>8}{row['vs120arm']:>7}{row['vsTanque']:>8}{row['heal']:>6}")
    print("(* = AS cruda excede el tope 3.0)")
    print()
    print("=== Chequeo de leyes (Jinx) ===")
    _,raw,B = as_total(spec, ["Gunmetal","C44","Runaan's","IE","LDR","Kraken"])
    need = (AS_CAP/spec.base_as - 1) - (spec.base_bonus_as + lvl_as_bonus(spec,15) + LT_RANGED_STACK*6 + ALACRITY_FULL + spec.self_as_buff)
    print(f"AS de ítems necesaria para cap 3.0 exacto: {need*100:.1f}%  | build C cruda: {raw:.3f}")
    print(f"Con Get Excited (+{spec.passive_burst_as:.0%}): {spec.base_as*(1+B+spec.passive_burst_as):.3f} (rompe el cap por pasiva)")
```

## 10b. MOTOR SECUNDARIO — modelos batch (Kalista on-hit, Diana rotación, Yuumi/Karma valor-aliado, TAMAÑO)

```python
# -*- coding: utf-8 -*-
"""
WR-LAB · Análisis batch 2: Kalista (on-hit), Diana (AP rotación), Yuumi/Karma (soportes)
+ cálculos del apéndice de TAMAÑO (Cho'Gath/Malphite/Shyvana). Parche 7.3.
Todas las fuentes: data/estructurada/*. Supuestos declarados en cada bloque.
"""
CAP = 3.0

def as_kalista(items_as, lt=0.384, alac=0.21, guinsoo_stacks=False):
    B = 0.16 + 0.644 + items_as + lt + alac + (0.32 if guinsoo_stacks else 0)
    return min(0.694*(1+B), CAP), 0.694*(1+B), B

def mit_phys(dmg, armor, pen=0): return dmg * 100/(100+max(0, armor*(1-pen/100)))
def mit_magic(dmg, mr, pen_pct=0, pen_flat=0): return dmg * 100/(100+max(0, mr*(1-pen_pct/100)-pen_flat))

# ══════════════════════════════ KALISTA ══════════════════════════════
# E Rend no critica (sin mención de crit en ficha). W = 19% max HP / 8s por objetivo (condicional Oathsworn).
# Guinsoo: cada 3er ataque aplica on-hit 1 vez额外 -> flat on-hit x4/3. Terminus dark: 30% pen (3 hits).
# Statikk: Energized cada ~4 ataques (Kalista gana 5 stacks/ataque), 60 mágico + bounces con on-hit.
K_ITEMS = {
 'Gunmetal':   dict(g=2200, ad=0,  as_=50, ls=5),
 'Statikk':    dict(g=3000, ad=40, as_=30, ap=40, energized=60),
 'Guinsoo':    dict(g=3000, ad=35, as_=30, ap=30, wrath=30, double=True),
 'Terminus':   dict(g=3000, ad=35, as_=35, shadow=30, pen=30),
 'Runaan':     dict(g=2650, ad=0,  as_=40, bolts=2),
 'WitsEnd':    dict(g=2800, ad=0,  as_=50, onhit=40, mr=45),
 'BotRK':      dict(g=3100, ad=40, as_=30, pct=6, ls=12),
 'LDR':        dict(g=3300, ad=35, crit=25, pen=35, gs=12),
 'C44':        dict(g=2900, ad=55, crit=25),
 'IE':         dict(g=3400, ad=75, crit=25),
 'Kraken':     dict(g=2900, ad=45, as_=35),
}
def kalista(items, armor=120, mr=50, ehp=2200, targets=1, oathsworn=True, level=15):
    its = [K_ITEMS[i] for i in items]
    gold = sum(i['g'] for i in its)
    ad = 57 + 5.2*(level-1) + sum(i.get('ad',0) for i in its)
    as_i = sum(i.get('as_',0) for i in its)/100
    guin = any(i.get('double') for i in its)
    AS, raw, B = as_kalista(as_i, guinsoo_stacks=guin)
    pen = max([i.get('pen',0) for i in its] or [0])
    # on-hit por golpe (fis->mag separados)
    oh_mag = sum(i.get('wrath',0)+i.get('shadow',0)+i.get('onhit',0) for i in its)
    mult_double = 4/3 if guin else 1.0
    pct_cur = sum(i.get('pct',0) for i in its)/100
    # auto (físico) + on-hit (mágico) + BotRK (físico)
    auto_phys = AS*ad + AS*pct_cur*ehp*0.9  # vida actual ~90% de max en pelea
    auto_mag  = AS*oh_mag*mult_double
    # Energized Statikk (~cada 4 ataques)
    en = sum(i.get('energized',0) for i in its)
    auto_mag += AS/4*en if en else 0
    # E Rend: ciclo 7s, lanzas = AS*4 (+1 por Q)
    n = max(1, AS*4)
    e_dmg = 75 + 0.70*ad + n*(42 + 0.57*ad)
    e_dps = e_dmg/7
    q_dps = (265 + 1.10*ad)/6.5
    w_dps = 0.19*ehp/8 if oathsworn else 0
    lt_bullet = 24*(1+0.0067*B*100)
    lt_dps = AS*lt_bullet
    # mitigación
    dps_phys = mit_phys(auto_phys + e_dps + q_dps + AS*pct_cur*ehp*0, armor, pen)
    dps_mag  = mit_magic(auto_mag, mr)
    dps_true_w = mit_phys(w_dps, 0) if False else w_dps  # W es mágico
    dps_mag += mit_magic(w_dps, mr)
    # LT bala = adaptiva (física aquí)
    dps_phys += mit_phys(lt_dps, armor, pen)
    # AoE: Runaan bolts (0.55AD + on-hit completo) + Statikk bounces
    aoe = 0
    if targets > 1:
        bolts = sum(i.get('bolts',0) for i in its)
        per_bolt = 0.55*ad + oh_mag*mult_double + pct_cur*ehp*0.9
        aoe += mit_phys(AS*per_bolt*min(bolts, targets-1)*0.55/0.55, armor, pen)*0  # (simplificado abajo)
        aoe = AS*min(bolts, targets-1)*(mit_phys(0.55*ad + pct_cur*ehp*0.9, armor, pen) + mit_magic(oh_mag*mult_double, mr))
        if en: aoe += AS/4*en*4*mit_magic(1, mr)  # 4 bounces extra aprox
    total = dps_phys + dps_mag + (aoe if targets>1 else 0)
    return dict(gold=gold, AD=ad, AS=AS, raw=raw, pen=pen, e_hit=e_dmg,
                single=dps_phys+dps_mag, multi=total, aoe=aoe,
                heal=(dps_phys+dps_mag)*sum(i.get('ls',0) for i in its)/100)

print("="*118)
print("KALISTA nivel 15 (LT+Alacrity full; E cada 7s con ~AS×4 lanzas; W 19% maxHP/8s con Oathsworn)")
print("="*118)
K_BUILDS = {
 'K1 Comunidad (Statikk+Guinsoo+Term+Runaan+WE)': ['Gunmetal','Statikk','Guinsoo','Terminus','Runaan','WitsEnd'],
 'K2 BotRK (saca Statikk)':                       ['Gunmetal','BotRK','Guinsoo','Terminus','Runaan','WitsEnd'],
 'K3 LDR anti-tanque (saca Statikk)':             ['Gunmetal','LDR','Guinsoo','Terminus','Runaan','WitsEnd'],
 'K4 CRIT (descarte teórico)':                    ['Gunmetal','C44','IE','Runaan','LDR','Kraken'],
 'K5 Single-target (sin Runaan/Statikk)':         ['Gunmetal','BotRK','Guinsoo','Terminus','Kraken','WitsEnd'],
}
print(f"{'BUILD':<48}{'oro':>6}{'AD':>5}{'AS':>6}{'pen':>4}{'1v1':>7}{'3v3':>8}{'vsTanq':>8}{'E-hit':>7}")
for n, b in K_BUILDS.items():
    r1 = kalista(b); r3 = kalista(b, targets=3); rt = kalista(b, armor=220, mr=150, ehp=4500)
    print(f"{n:<48}{r1['gold']:>6}{r1['AD']:>5.0f}{r1['AS']:>6.2f}{r1['pen']:>4.0f}{r1['single']:>7.0f}{r3['multi']:>8.0f}{rt['single']:>8.0f}{r1['e_hit']:>7.0f}")
print("\nCheckpoint nivel 11 (2 items, Berserker's): ")
for n,b in {'Statikk+Guinsoo':['Statikk','Guinsoo'],'Guinsoo+WE':['Guinsoo','WitsEnd'],'Statikk+Runaan':['Statikk','Runaan'],'C44+Runaan(crit)':['C44','Runaan']}.items():
    r = kalista(['Gunmetal' if False else 'Statikk']+[] if False else b, level=11, armor=90, mr=40, ehp=1800)
    # sin botas T3 (aún no, min 10 ok sí -> usar Gunmetal si >=10min; nivel 11 ~ 12min: incluir Gunmetal)
    r = kalista(['Gunmetal']+b, level=11, armor=90, mr=40, ehp=1800)
    print(f"  {n:<22} AD={r['AD']:.0f} AS={r['AS']:.2f} 1v1={r['single']:.0f} 3v3={kalista(['Gunmetal']+b, level=11, armor=90, mr=40, ehp=1800, targets=3)['multi']:.0f}")

# ══════════════════════════════ DIANA ══════════════════════════════
# Rotación sostenida (10s) + burst combo. Moonsilver: +30-100% AS 4s tras habilidad (uptime ~85% en pelea -> prom 0.65 efectivo sostenido, 1.0 en burst).
# Cada 3er auto: 65 + 0.5AP mágico AoE. Q 195+0.7AP/5s; E 160+0.3AP (reset w/ Moonlight: 2 casts/ciclo); W 3x(65+0.2AP)+escudo; R 440+0.8AP.
D_ITEMS = {
 'Spellslinger': dict(g=2200, ap=35, pen_f=18, pen_p=8, ah=0),
 'Crimson':      dict(g=2000, ah=25),
 'DuskDawn':     dict(g=3100, ap=60, hp=300, as_=20, ah=20, sb=0.75),   # spellblade 75% base AD +10%AP + cura
 'Nashor':       dict(g=2900, ap=80, as_=50, ah=15, gnaw=1.0),           # on-hit 15+20% bonus AP
 'Rabadon':      dict(g=3400, ap=130),
 'InfinityOrb':  dict(g=3100, ap=110, pen_f=15, crit_exec=0.2),
 'Zhonyas':      dict(g=3300, ap=110, armor=40),
 'Cryptbloom':   dict(g=3000, ap=75, pen_p=30, ah=20),
 'VoidStaff':    dict(g=3000, ap=95, pen_p=40),
 'Luden':        dict(g=2800, ap=100, ah=10, echo=1.0),
 'Stormsurge':   dict(g=2800, ap=90, pen_f=15, squall=1.0),
 'Malignance':   dict(g=2700, ap=90, ah=15),
 'CosmicDrive':  dict(g=3000, ap=70, hp=300, ah=25),
}
# v1.8: añadidos desde items_7.3.csv (Torment/Hypershot/GW sin modelar en la rotación: conservador)
D_ITEMS.setdefault('Morello',      dict(g=2650, ap=75, hp=300, ah=15))
D_ITEMS.setdefault('Rylai',        dict(g=2700, ap=65, hp=350))
D_ITEMS.setdefault('HorizonFocus', dict(g=2700, ap=80, ah=25))
D_ITEMS.setdefault('Liandry',      dict(g=3000, ap=70, hp=300))

def diana(items, ap_extra=0, keystone='empower', mr=80, pen_note=None, level=15, fight=10.0, burst=False):
    its = [D_ITEMS[i] for i in items]
    gold = sum(i['g'] for i in its)
    ap = sum(i.get('ap',0) for i in its) + ap_extra
    base_ad = 52 + 3.64*(level-1)
    haste = sum(i.get('ah',0) for i in its) + (15 if 'Legend: Haste' in (pen_note or '') else 0)
    cdr = haste/(100+haste)
    as_i = sum(i.get('as_',0) for i in its)/100
    moons = 0.65
    B = 0.15 + 0.008*(level-1) + as_i + moons + (0.384 if keystone=='lt' else 0) + (0.21 if keystone=='lt' else 0)
    AS = min(0.694*(1+B), CAP)
    pen_f = sum(i.get('pen_f',0) for i in its); pen_p = max(i.get('pen_p',0) for i in its) if any('pen_p' in i for i in its) else 0
    mrm = max(0, mr*(1-pen_p/100)-pen_f)
    mitm = 100/(100+mrm)
    # --- habilidades en ventana de fight ---
    q_n = max(1, round(fight/(5*(1-cdr))))
    q = q_n*(195+0.7*ap)
    e_n = q_n + 1     # E resetea con Moonlight de cada Q (+1 inicial)
    e = e_n*(160+0.3*ap)
    w_n = max(1, round(fight/(8.5*(1-cdr))))
    w = w_n*3*(65+0.2*ap)
    r = (440+0.8*ap) if burst or fight>=8 else 0
    # --- autos ---
    gnaw = sum(i.get('gnaw',0) for i in its)
    auto_phys = AS*base_ad*fight
    auto_mag = AS*(gnaw*(15+0.2*ap))*fight
    proc3 = (AS*fight/3)*(65+0.5*ap)
    sb_n = int(fight/1.5) if any(i.get('sb') for i in its) else 0
    sb = sb_n*(0.75*sum(i.get('sb',0) for i in its)*base_ad + 0.10*ap)
    # echo Luden / squall
    echo = (75 + 0.08*ap)*max(1,int(fight/9)) if any(i.get('echo') for i in its) else 0
    squall = (125+0.1*ap)*max(1,int(fight/25*4)) if any(i.get('squall') for i in its) else 0  # ~1 cada 2.5s de dmg
    total_mag = (q+e+w+r+auto_mag+proc3+sb+echo+squall)*mitm
    total_phys = auto_phys*100/(100+60)  # autos físicos vs ~60 armadura
    # keystone
    kbonus = 0
    if keystone=='empower':
        proc_n = int(fight/4)                      # proc cada 3 hits, ICD 4s
        emp = proc_n*165*mitm                      # daño adaptivo del proc (late ~165)
        total = (total_mag+total_phys+emp)*1.08    # amp 8% (uptime ~casi todo el fight)
        return dict(gold=gold, AP=ap, AS=AS, dps=total/fight, mr_eff=mrm,
                    burst=(440+0.8*ap+195+0.7*ap+2*(160+0.3*ap)+3*(65+0.2*ap))*mitm)
    if keystone=='lt':
        bul = 24*(1+0.0067*B*100)*AS*fight*mitm
        total_phys += bul
    if keystone=='conq':
        total_phys += AS*fight*30*100/(100+60)*0.6   # ~30 adaptivo (AD) a uptime 60%
        total_mag *= 1.0                              # + omnivamp 9% (sustain, no DPS)
    return dict(gold=gold, AP=ap, AS=AS, dps=(total_mag+total_phys)/fight, burst=(440+0.8*ap+195+0.7*ap+2*(160+0.3*ap)+3*(65+0.2*ap))*mitm, mr_eff=mrm)

print()
print("="*118)
print("DIANA nivel 15 — DPS sostenido (fight 10s, vs 80 MR squishy) y burst combo completo (R+Q+E×2+W×3)")
print("="*118)
D_BUILDS = {
 'D1 Comunidad (D&D,Orb,Zhonya,Rabadon,Luden)':      ['Spellslinger','DuskDawn','InfinityOrb','Zhonyas','Rabadon','Luden'],
 'D2 Nashor híbrida (D&D,Nashor,Rabadon,Zhonya,Crypt)':['Spellslinger','DuskDawn','Nashor','Rabadon','Zhonyas','Cryptbloom'],
 'D3 Burst puro (Luden,Rabadon,Orb,Stormsurge,Zhonya)':['Spellslinger','Luden','Rabadon','InfinityOrb','Stormsurge','Zhonyas'],
 'D4 Anti-tanque (Void Staff)':                       ['Spellslinger','DuskDawn','Rabadon','VoidStaff','Zhonyas','Cryptbloom'],
}
for ks in ['empower','lt','conq']:
    print(f"\n-- Keystone: {ks.upper()} --")
    print(f"{'BUILD':<52}{'oro':>6}{'AP':>5}{'AS':>6}{'MR-ef':>6}{'DPS10s':>8}{'burst':>8}")
    for n,b in D_BUILDS.items():
        r = diana(b, keystone=ks)
        print(f"{n:<52}{r['gold']:>6}{r['AP']:>5.0f}{r['AS']:>6.2f}{r['mr_eff']:>6.0f}{r['dps']:>8.0f}{r['burst']:>8.0f}")
print("\nDiana vs tanque (180 MR): D1 vs D4")
for n,b in [('D1',D_BUILDS['D1 Comunidad (D&D,Orb,Zhonya,Rabadon,Luden)']),('D4',D_BUILDS['D4 Anti-tanque (Void Staff)'])]:
    r = diana(b, mr=180); print(f"  {n}: DPS={r['dps']:.0f} MR efectiva={r['mr_eff']:.0f}")

# ══════════════════════════════ YUUMI ══════════════════════════════
# v1.8: diccionario expandido desde data/estructurada/items_7.3.csv (stats oficiales).
# Pasivas no modeladas en yuumi()/karma() quedan como flag inerte (comentario por ítem):
# el modelo de valor-aliado consume AP/HSP/haste; las pasivas de daño/amp se declaran pero
# no puntúan (conservador).
Y_ITEMS = {
 'Scythe':     dict(g=0,    ah=10),
 'Mandate':      dict(g=2600, ap=60, ah=20, mandate=1),      # CC marca: +7% dmg aliado (amp de equipo, no HSP)
 'Stormsurge':   dict(g=2800, ap=90, ah=0,  squall=1),       # +15 pen mágica (pen no entra en e_shield/r_heal)
 'HarmonicEcho': dict(g=2500, ap=40, hp=200, ah=20, harmonic=1),  # cura post-cast no modelada (conservador)
 'Morello':      dict(g=2650, ap=75, hp=300, ah=15, gw=1),
 'Rylai':        dict(g=2700, ap=65, hp=350, slow=1),
 'HorizonFocus': dict(g=2700, ap=80, ah=25, hypershot=1),
 'Liandry':      dict(g=3000, ap=70, hp=300, torment=1),
 'Crimson':    dict(g=2000, ah=25),
 'Censer':     dict(g=2400, ap=50, hsp=8),
 'Echoes':     dict(g=2400, ap=40, hp=200, ah=20, siphon=1),
 'Staff':      dict(g=2400, ap=50, hsp=8, ah=10, rapids=1),
 'Redemption': dict(g=2450, ap=40, hsp=8, ah=10, redempt=1),
 'Mikael':     dict(g=2500, hp=300, hsp=9, ah=15, cleanse=1),
 'Diadem':     dict(g=2400, hp=200, hsp=8, diadem=1),
 'Locket':     dict(g=2600, hp=200, armor=30, mr=30, ah=10, locket=1),
 'Shurelya':   dict(g=2500, ap=55, ah=20, shurelya=1),
 'Zeke':       dict(g=2400, hp=300, armor=25, mr=25, ah=10, zeke=1),
 'YordleTrap': dict(g=2400, hp=200, armor=20, mr=20, ah=15, trap=1),
}
def yuumi(items, revitalize=True, bf=True, adc_as_base=2.6, adc_dmg_per_hit=330,
          w_flat=None, w_ap_pct=0.01):
    # 7.3a NERF: W Best Friend HSP 8/9/10/11 % + 0.02 %/AP → 6/7/8/9 % + 0.01 %/AP (rank 5).
    # w_flat=None → valor del parche vigente (9 attach / 6 sin attach). Para reproducir el
    # baseline publicado pre-7.3a (E=339): w_flat=11, w_ap_pct=0.0 (ver update_reports.params_yuumi).
    its = [Y_ITEMS[i] for i in items]
    gold = sum(i['g'] for i in its)
    ap = sum(i.get('ap',0) for i in its)
    if w_flat is None: w_flat = 9 if bf else 6
    hsp = sum(i.get('hsp',0) for i in its) + w_flat + w_ap_pct*ap + (5 if revitalize else 0)
    haste = sum(i.get('ah',0) for i in its)
    # E shield rank4: 170+0.4AP, multiplicado por (1+HSP%)
    e_shield = (170+0.4*ap)*(1+hsp/100)
    e_cd = 9*100/(100+haste)
    # R heal total (BF): 7 olas x (52+0.08AP) x (1+HSP)
    r_heal = 7*(52+0.08*ap)*(1+hsp/100)
    # Q on-hit aliado: 22+0.05AP (5s, Q cd5 -> uptime ~100%)
    q_onhit = 22+0.05*ap
    # Censer: +30% AS y +25 on-hit mágico al ADC; Q de Yuumi: +22+5%AP on-hit al aliado (uptime ~100%)
    censer = 'Censer' in items
    # +30% AS sobre AS total ~2.6 del carry => ~+11.5% DPS (30/260); on-hit y Q-onhit por golpe
    adc_dps_add = (0.115*adc_as_base*adc_dmg_per_hit if censer else 0)
    adc_dps_add += adc_as_base*(25 if censer else 0) + adc_as_base*q_onhit
    # Echoes/Diadem/Redemption throughput
    echo_val = 0.30*e_shield if any(i.get('siphon') for i in its) else 0
    diadem_hps = 0.008*(1200)*1.0 if any(i.get('diadem') for i in its) else 0  # 0.8% mana max/s ~9.6
    redempt_burst = 350*(1+hsp/100)*0 + 350 if any(i.get('redempt') for i in its) else 0
    return dict(gold=gold, AP=ap, HSP=hsp, haste=haste, e_shield=e_shield, e_cd=e_cd,
                r_heal=r_heal, q_onhit=q_onhit, adc_dps_add=adc_dps_add,
                shield_per_min=e_shield*(60/e_cd), echo_val=echo_val, diadem_hps=diadem_hps)

print()
print("="*118)
print("YUUMI — valor por build (E shield, R heal total, DPS añadido al ADC carry [AS 2.6, 330 dmg/golpe], escudo/min)")
print("="*118)
Y_BUILDS = {
 'Y1 Amp-ADC (Censer,Echoes,Staff,Redemption)': ['Scythe','Crimson','Censer','Echoes','Staff','Redemption'],
 'Y2 Heal engine (Echoes,Staff,Diadem,Redempt)': ['Scythe','Crimson','Echoes','Staff','Diadem','Redemption'],
 'Y3 Anti-dive (Mikael,Locket,Censer,Echoes)':   ['Scythe','Crimson','Mikael','Locket','Censer','Echoes'],
 'Y4 AP greedy (Censer,Staff,Echoes,Shurelya)':  ['Scythe','Crimson','Censer','Staff','Echoes','Shurelya'],
 'Y5 Zeke (para comps de engage)':              ['Scythe','Crimson','Zeke','Censer','Echoes','Staff'],
}
print(f"{'BUILD':<46}{'oro':>6}{'AP':>5}{'HSP%':>5}{'E-shield':>9}{'E-cd':>6}{'R-heal':>8}{'ADC+DPS':>8}{'shld/min':>9}")
for n,b in Y_BUILDS.items():
    r = yuumi(b)
    print(f"{n:<46}{r['gold']:>6}{r['AP']:>5.0f}{r['HSP']:>5.0f}{r['e_shield']:>9.0f}{r['e_cd']:>6.1f}{r['r_heal']:>8.0f}{r['adc_dps_add']:>8.0f}{r['shield_per_min']:>9.0f}")

# ══════════════════════════════ KARMA ══════════════════════════════
def karma(items, ap_extra=0, revitalize=True):
    its = [Y_ITEMS.get(i) or D_ITEMS.get(i) for i in items]
    gold = sum(i['g'] for i in its)
    ap = sum(i.get('ap',0) for i in its) + ap_extra
    haste = sum(i.get('ah',0) for i in its)
    hsp = sum(i.get('hsp',0) for i in its) + (5 if revitalize else 0)
    e_shield = (150+0.65*ap)*(1+hsp/100)
    e_mantra = (300+0.65*ap)*(1+hsp/100)
    e_cd = 7*100/(100+haste)
    q_dmg = (180+0.4*ap); q_mantra = (290+0.5*ap)+(160+0.5*ap)
    w_dmg = (110+0.4*ap)+(130+0.45*ap)
    r_dmg = 390+0.8*ap
    mantra_cad = 3  # casts por mantra
    casts_per_10s = 10/((6+7+15)/3*100/(100+haste))  # Q+E+W promedio
    mantras_10s = casts_per_10s/3
    return dict(gold=gold, AP=ap, HSP=hsp, haste=haste, e_shield=e_shield, e_mantra=e_mantra,
                e_cd=e_cd, q_mantra=q_mantra, mantras_10s=mantras_10s,
                dmg_10s=(casts_per_10s/3)*q_mantra + (casts_per_10s*2/3)*q_dmg*0.5)

KARMA_SUP = {
 'KS1 Mandate+Censer (team amp)':  ['Scythe','Crimson','Censer','Echoes','Staff','Redemption'],
 'KS2 Escudos puros':              ['Scythe','Crimson','Censer','Echoes','Staff','Mikael'],
 'KS3 Mandate (marcar +7% team)':  ['Scythe','Crimson','Censer','Echoes','Staff','Redemption'],
}
print()
print("="*118)
print("KARMA support — E shield / E-Mantra / cadencia de Mantras en 10s (con Imperial Mandate: +7% dmg team a marcados)")
print("="*118)
KB = {
 'KS1 Enchanter (Censer,Echoes,Staff,Redemption)': ['Scythe','Crimson','Censer','Echoes','Staff','Redemption'],
 'KS2 Mandate amp (Censer,Mandate*,Echoes,Staff)': ['Scythe','Crimson','Censer','Echoes','Staff','Redemption'],
}
print(f"{'BUILD':<50}{'oro':>6}{'AP':>5}{'HSP%':>5}{'E-shield':>9}{'E-Mantra':>9}{'E-cd':>6}{'mantras/10s':>12}")
for n,b in KB.items():
    r = karma(b)
    print(f"{n:<50}{r['gold']:>6}{r['AP']:>5.0f}{r['HSP']:>5.0f}{r['e_shield']:>9.0f}{r['e_mantra']:>9.0f}{r['e_cd']:>6.1f}{r['mantras_10s']:>12.1f}")
print("\nKARMA mid (comunidad):", end=" ")
rm = karma(['Spellslinger','Luden','Malignance','Rabadon','InfinityOrb','Zhonyas']) if False else None
# mid karma usa items AP puros:
items_mid = ['Spellslinger','Luden','Malignance','Rabadon','InfinityOrb','Zhonyas']
gold = sum(D_ITEMS[i]['g'] for i in items_mid); ap = sum(D_ITEMS[i].get('ap',0) for i in items_mid)
haste = sum(D_ITEMS[i].get('ah',0) for i in items_mid)
print(f"oro={gold} AP={ap:.0f} haste={haste} E-mantra shield={(300+0.65*ap)*(1.05):.0f} Q-mantra={(290+0.5*ap)+(160+0.5*ap):.0f}")

# ══════════════════════════════ TAMAÑO (SIZE) ══════════════════════════════
print()
print("="*118)
print("TAMAÑO — Cho'Gath Feast: HP bonus, rango y ejecucion R por stacks")
print("="*118)
print(f"{'stacks Feast':>12}{'HP bonus':>10}{'size +':>8}{'rango +':>9}{'R true dmg (AP150, HP items 1500)':>36}")
for st in [6, 10, 15, 22]:
    hp = st*160; size = min(6*st, 135); rng = min(7.7*st, 75)
    r_true = 600 + 0.5*150 + 0.10*(hp+1500)
    print(f"{st:>12}{hp:>10}{size:>7.0f}%{rng:>9.1f}{r_true:>36.0f}")
print()
print("MALPHITE armor-stacking (lvl 15, base armor 119):")
for combo, armor in [("Iceborn(50)+Thornmail(75)+Armored(30)", 119+155), ("+ W rank4 (+40% bonus armor)", 119+155+0.4*155), ("+ Gargoyle/Twinguard situacional", 119+155+62+50)]:
    e = 210+0.45*armor; w = 50+0.2*armor; w1 = 100+0.4*armor
    print(f"  armor~{armor:.0f} ({combo}): E={e:.0f} mág AoE | W golpe={w:.0f} | W primero={w1:.0f} | pasiva Granite={0.11*(690+130*14):.0f} escudo")
print()
print("GARGOYLE activo (escudo = 100 + 90% bonus HP) + SIZE:")
for bhp in [800, 1200, 1800, 2500]:
    print(f"  bonus HP {bhp}: escudo {100+0.9*bhp:.0f} (+aumento de tamaño 2.5s)")
print()
print("TWINGUARD Endurance (5 stacks): +20% size, +20% tenacidad, +30% armadura y +30% MR bonus")
for base_ar, base_mr in [(150,80),(250,120),(320,180)]:
    print(f"  con {base_ar} arm / {base_mr} MR -> {base_ar*1.3:.0f} arm / {base_mr*1.3:.0f} MR en pelea (mitigación {100/(100+base_ar)*100:.1f}% -> {100/(100+base_ar*1.3)*100:.1f}% dmg físico recibido)")
print()
print("HEARTSTEEL scaling (3.5% max HP de daño, 15% del daño como HP permanente, 20s CD/target):")
for hp in [2500, 3500, 5000, 7000]:
    dmg = 140+0.035*hp
    print(f"  con {hp} HP: golpe {dmg:.0f} -> +{0.15*dmg:.0f} HP permanente (por campeón cada 20s)")
```

## 10c. OPTIMIZADOR DE BUILDS (4 motores · búsqueda exhaustiva con Leyes 0-1-2-3 · presets de defensa/utilidad)

```python
# -*- coding: utf-8 -*-
"""
WR-LAB · optimize_build.py — optimizador exhaustivo de builds (v2: 4 motores)
=============================================================================
Busca la build ÓPTIMA de 6 slots (Ley 0) maximizando un objetivo ponderado
NORMALIZADO por escenario (cada escenario aporta en proporción, no en magnitud),
sujeto a presupuesto de oro y —en el motor de autos— a las Leyes 1 y 2 como podas.

MOTORES (adapters sobre los modelos del lab; el motor declara ítems, botas, escenarios y pesos):
    autos     dps_model.eval_build    → Jinx, Yunara, Sivir, Caitlyn… (crítico/on-hit del engine)
    onhit     analysis_batch2.kalista → Kalista (E Rend + Guinsoo doble on-hit)
    rotacion  analysis_batch2.diana   → Diana (y magos de rotación AP; keystone configurable)
    aliado    analysis_batch2.yuumi   → Yuumi/Karma (valor-aliado: escudo/cura/DPS-al-carry;
                                        slot de quest fijo + botas Crimson)

USO
    python3 model/optimize_build.py jinx                        # motor autos (default del campeón)
    python3 model/optimize_build.py jinx --crit-min 100 --pen-min 30 --validar
    python3 model/optimize_build.py kalista --validar           # ¿redescubre K2 BotRK?
    python3 model/optimize_build.py diana --keystone lt --validar
    python3 model/optimize_build.py yuumi --oro 13000 --validar
    python3 model/optimize_build.py jinx --motor autos --oro 15000 --top 5
    python3 model/optimize_build.py jinx --incluir "Gunmetal,C44,Runaan's,IE,LDR,Kraken,BT" --excluir ga

VALIDACIÓN CRUZADA (ROADMAP): con pesos default debe redescubrir la build C de Jinx
(pool del reporte), K2 de Kalista, D2-LT de Diana e Y1 de Yuumi — ver tests/test_optimize_build.py.

Búsqueda: DFS podado (oro; en autos también AS-cap y crit≤100 como podas estructurales,
y --crit-min/--pen-min como restricciones duras de hoja) + embudo re-puntuado con el
objetivo ponderado completo. Cero dependencias.
"""
import argparse, heapq, os, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "model"))
import dps_model as M
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import analysis_batch2 as B2

EPS_AS = 0.02          # tolerancia del tope de AS (Ley 2)

# ---------------------------------------------------------------- defensa y utilidad (v1.9)
# Fuentes: items_7.3.csv (valores oficiales) + comentarios del motor. Uptimes declarados:
# escudos condicionales (Lifeline/Ichorshield/Noxian) cuentan al 50-70 % (no están siempre).
ESCUDOS_FIS = {"bt": 255 * 0.5, "shieldbow": 425 * 0.5, "armored_adv": 75 * 0.7}
ESCUDOS_MAG = {"chainlaced": 75 * 0.7}      # Maw: valor recortado en la fuente → solo su MR cuenta
UTIL_FLAGS = {"ga": 300, "Zhonyas": 300, "scimitar": 150, "gale": 100,
              "immortal_treads": 100, "Redemption": 200, "Mikael": 200, "Locket": 150,
              "Shurelya": 100, "Zeke": 100}
BASE_DEF_FALLBACK = (650.0, 45.0, 35.0)     # hp/armor/mr nivel 1 (si no está en champion_base_stats.json)


def cargar_base_def(champ, nivel=15):
    """(hp, armor, mr) a nivel `nivel` desde data/estructurada/champion_base_stats.json.
    Formato fuente: '570 (104)' = base (crecimiento por nivel). Fallback genérico declarado."""
    import json, re as _re
    ruta = os.path.join(ROOT, "data", "estructurada", "champion_base_stats.json")
    try:
        with open(ruta, encoding="utf-8") as fh:
            db = json.load(fh)
        st = db[champ]["stats"]
        def num(clave):
            m = _re.match(r"([\d.]+)\s*\(([\d.]+)\)", st.get(clave, "").replace("\xa0", " "))
            if not m:
                return None
            return float(m.group(1)) + float(m.group(2)) * (nivel - 1)
        hp, ar, mr = num("heal"), num("armor"), num("magicresistance")   # 'heal' = Health (errata del scrape)
        if None in (hp, ar, mr):
            raise ValueError
        return hp, ar, mr
    except Exception:
        b = BASE_DEF_FALLBACK
        return (b[0] + 90 * (nivel - 1), b[1] + 3.5 * (nivel - 1), b[2] + 1.2 * (nivel - 1))


def ehp_y_util(keys_resueltas, base_def, heal_s):
    """EHP mixto (50 % físico / 50 % mágico, escudos condicionales ponderados) y utilidad
    (heal/s + banderas de activas). hechizo heurístico declarado: GA/Zhonyas 300, QSS 150…"""
    hp, armor, mr = base_def
    esc_f = esc_m = util = 0.0
    for k in keys_resueltas:
        it = M.ITEMS.get(k)
        if it is not None:
            hp += it.hp; armor += it.armor; mr += it.mr
        esc_f += ESCUDOS_FIS.get(k, 0.0)
        esc_m += ESCUDOS_MAG.get(k, 0.0)
        util += UTIL_FLAGS.get(k, 0.0)
    ehp = 0.5 * ((hp + esc_f) * (1 + armor / 100.0) + (hp + esc_m) * (1 + mr / 100.0))
    # heal/s se pondera ×0.25 para que no aplaste a las activas (heurístico declarado v1.9)
    return ehp, util + 0.25 * heal_s

# ---------------------------------------------------------------- motores
ESC_AUTOS = {
    "1v1":      (dict(),                                     "dps1"),
    "3v3":      (dict(targets=3),                            "dpsN"),
    "vs120":    (dict(armor=120),                            "dps1"),
    "vsTanque": (dict(armor=220, tank=True, enemy_hp=4500),  "dps1"),
}
PESOS_AUTOS = {"1v1": 0.30, "3v3": 0.30, "vs120": 0.20, "vsTanque": 0.20}

ESC_ONHIT = {
    "1v1":      (dict(), "single"),
    "3v3":      (dict(targets=3), "multi"),
    "vsTanque": (dict(armor=220, mr=150, ehp=4500), "single"),
}
PESOS_ONHIT = {"1v1": 0.35, "3v3": 0.45, "vsTanque": 0.20}

ESC_ROT = {
    "dps10s":  (dict(), "dps"),
    "burst":   (dict(), "burst"),
    "vs180mr": (dict(mr=180), "dps"),
}
PESOS_ROT = {"dps10s": 0.50, "burst": 0.30, "vs180mr": 0.20}

ESC_ALIADO = {
    "e_shield": (dict(), "e_shield"),
    "r_heal":   (dict(), "r_heal"),
    "adc_dps":  (dict(), "adc_dps_add"),
}
PESOS_ALIADO = {"e_shield": 0.35, "r_heal": 0.30, "adc_dps": 0.35}

# IE fuera del pool on-hit: batch2.kalista() NO modela críticos (la E Rend no critica y los
# autos critables no están en la fórmula) → IE aparecería como "AD barato" y su 25 % de crit
# valdría 0 en el score. En la realidad ese crit SÍ vale: excluirlo es la postura conservadora.
_K_NO_BOOT = [k for k in B2.K_ITEMS if k not in ("Gunmetal", "IE")]
_D_NO_BOOT = [k for k in B2.D_ITEMS if k not in ("Spellslinger", "Crimson")]
_Y_NO_BOOT = [k for k in B2.Y_ITEMS if k not in ("Crimson", "Scythe", "ionian")]

ENGINES = {
    "autos": dict(
        items=[k for k in M.ITEMS if k not in M.BOOTS_ALL and k != "boots_speed"],
        boots=list(M.BOOT_UPGRADES.keys()), fixed=[], n_elegir=5, oro_default=18000,
        escenarios=ESC_AUTOS, pesos=PESOS_AUTOS, podas_autos=True,
        eval_fn=lambda champ, combo, kw, opts: M.eval_build(M.CHAMPS[champ], combo, validate=False, **kw),
        base_fn=lambda champ, combo, opts: M.eval_build(M.CHAMPS[champ], combo, validate=False),
        gold_fn=lambda k: M.ITEMS[k].gold,
        requiere_spec=True,
    ),
    "onhit": dict(
        items=_K_NO_BOOT, boots=["Gunmetal"], fixed=[], n_elegir=5, oro_default=18000,
        escenarios=ESC_ONHIT, pesos=PESOS_ONHIT, podas_autos=False,
        eval_fn=lambda champ, combo, kw, opts: B2.kalista(combo, **kw),
        base_fn=lambda champ, combo, opts: B2.kalista(combo),
        gold_fn=lambda k: B2.K_ITEMS[k]["g"],
        requiere_spec=False,
    ),
    "rotacion": dict(
        items=_D_NO_BOOT, boots=["Spellslinger", "Crimson"], fixed=[], n_elegir=5, oro_default=18500,
        escenarios=ESC_ROT, pesos=PESOS_ROT, podas_autos=False,
        eval_fn=lambda champ, combo, kw, opts: B2.diana(combo, keystone=opts.get("keystone", "lt"), **kw),
        base_fn=lambda champ, combo, opts: B2.diana(combo, keystone=opts.get("keystone", "lt")),
        gold_fn=lambda k: B2.D_ITEMS[k]["g"],
        requiere_spec=False,
    ),
    "aliado": dict(
        items=_Y_NO_BOOT, boots=["Crimson"], fixed=["Scythe"], n_elegir=4, oro_default=13000,
        escenarios=ESC_ALIADO, pesos=PESOS_ALIADO, podas_autos=False,
        eval_fn=lambda champ, combo, kw, opts: B2.yuumi(combo, **kw),
        base_fn=lambda champ, combo, opts: B2.yuumi(combo),
        gold_fn=lambda k: B2.Y_ITEMS[k]["g"],
        requiere_spec=False,
    ),
}

MOTOR_POR_CAMPEON = {"kalista": "onhit", "diana": "rotacion", "yuumi": "aliado", "karma": "aliado"}

# Campeones cuyo arquetipo NO es representable por ningún motor del lab: optimizarlos
# con el motor de autos produce BASURA (bug reportado 29-sep: chogath "como ADC").
SIN_MOTOR = {
    "chogath":     "tanque AP (Feast) — el motor de autos no tiene sentido; ver metodologia/ESCALADO_DE_TAMANIO.md y el modelo de rotación (pendiente en batch2)",
    "mordekaiser": "juggernaut AP — requiere modelo de rotación + R (pendiente en batch2)",
    "heimerdinger": "mago de zona (torretas) — requiere modelo de DPS de torretas (pendiente)",
    "seraphine":   "enchanter-mage — modelo de valor-aliado/rotación (pendiente)",
    "malphite":    "tanque de escalado de armadura — ver ESCALADO_DE_TAMANIO.md",
}
# Campeones donde el motor elegido es una APROXIMACIÓN (aviso, no bloqueo)
MOTOR_AVISOS = {
    "yunara":   "motor autos NO modela su spread de Q ni la interacción de R con crítico — resultados aproximados",
    "shyvana":  "motor autos NO modela su Q doble golpe ni la forma dragón — resultados aproximados",
    "volibear": "motor autos NO modela su W ejecutor ni stacks de AS; ad_growth sin verificar (FUENTES.md) — resultados aproximados",
}


def motor_para(champ, override=None, quiet=False):
    if override:
        if champ in SIN_MOTOR and not quiet:
            print(f"⚠️ MOTOR FORZADO para {champ}: {SIN_MOTOR[champ]}.\n"
                  f"   Los resultados NO son válidos para publicar — solo exploración bajo tu responsabilidad.")
        return override
    if champ in SIN_MOTOR:
        sys.exit(f"❌ '{champ}' no tiene motor de optimización: {SIN_MOTOR[champ]}.\n"
                 f"   (Puedes forzar uno con --motor, bajo tu responsabilidad; o analizarlo a mano "
                 f"con el bundle completo en un chat externo.)")
    if champ in MOTOR_AVISOS and not quiet:
        print(f"⚠️ {champ}: {MOTOR_AVISOS[champ]}")
    return MOTOR_POR_CAMPEON.get(champ, "autos")


# ---------------------------------------------------------------- búsqueda
PRESETS = {"balanceado": (0.15, 0.15), "ofensivo": (0.0, 0.0), "defensivo": (0.30, 0.15)}


def optimizar(champ, motor=None, oro=None, top=10, pesos=None, excluir=(), incluir=None,
              solo_botas=None, embudo=400, nivel=15, verbose=True, crit_min=0, pen_min=0,
              keystone="lt", defensa=0.0, utilidad=0.0, preset=None):
    champ = champ.lower()
    motor = motor_para(champ, motor, quiet=not verbose)
    eng = ENGINES[motor]
    if preset:
        defensa, utilidad = PRESETS[preset]
    if motor == "aliado" and (defensa or utilidad):
        print("[aviso] motor aliado: la defensa propia no aplica (Yuumi attachada es intargeteable) "
              "— pesos de defensa/utilidad ignorados")
        defensa = utilidad = 0.0
    if eng["requiere_spec"] and champ not in M.CHAMPS:
        sys.exit(f"'{champ}' no tiene ChampSpec en dps_model.CHAMPS (motor autos). "
                 f"Especs: {sorted(M.CHAMPS)}")
    opts = {"keystone": keystone}
    oro = oro or eng["oro_default"]
    pesos = pesos or dict(eng["pesos"])
    escenarios = eng["escenarios"]
    falta = set(pesos) - set(escenarios)
    if falta:
        sys.exit(f"escenarios desconocidos para motor {motor}: {falta} (válidos: {list(escenarios)})")

    def resolver(x):
        """alias/nombre visible → clave del pool del motor."""
        x = x.strip()
        if eng is ENGINES["autos"]:
            try:
                return M.resolve(x).key
            except KeyError:
                return x.lower()
        for k in eng["items"] + eng["boots"] + eng["fixed"]:
            if k.lower() == x.lower():
                return k
        try:                                  # nombres visibles del vault ("Runaan's Hurricane")
            import update_reports as U
            for k in eng["items"] + eng["boots"] + eng["fixed"]:
                if U.resolver_clave(x, motor) == k:
                    return k
        except Exception:
            pass
        return x.lower()

    ex_keys = {resolver(x) for x in excluir if x}
    pool = [k for k in eng["items"] if k not in ex_keys]
    if incluir:
        inc = {resolver(x) for x in incluir if x.strip()}
        pool = [k for k in pool if k in inc]
    botas = list(eng["boots"])
    if solo_botas:
        wanted = {x.strip().lower() for x in solo_botas.split(",")}
        botas = [b for b in botas if b.lower() in wanted]
    if not botas:
        sys.exit("sin botas candidatas")
    fixed = list(eng["fixed"])
    n_elegir = eng["n_elegir"]

    gold = eng["gold_fn"]
    esc1 = max(pesos, key=pesos.get)
    kw1, met1 = escenarios[esc1]

    # podas estructurales del motor de autos (Ley 1/2 como cotas monótonas)
    if eng["podas_autos"]:
        spec = M.CHAMPS[champ]
        lt_as = (M.LT_RANGED_STACK if spec.ranged else M.LT_MELEE_STACK) * 6
        const_raw = spec.base_as + spec.as_ratio * (
            spec.base_bonus_as + M.lvl_as_bonus(spec, nivel) + lt_as + M.ALACRITY_FULL + spec.self_as_buff)
        as_por_item = {k: M.ITEMS[k].a_s / 100.0 for k in pool}
        crit_item = {k: M.ITEMS[k].crit for k in pool}
    oro_item = {k: gold(k) for k in pool}
    oro_min = min(oro_item.values()) if oro_item else 0
    orden = sorted(pool, key=lambda k: oro_item[k])
    idx = {k: i for i, k in enumerate(orden)}

    t0 = time.time()
    hojas = 0
    heap = []                                   # min-heap (score1, -oro, combo)
    eval_fn = eng["eval_fn"]

    def dfs(start, elegidos, g):
        nonlocal hojas
        faltan = n_elegir - len(elegidos)
        if g + faltan * oro_min > oro - oro_fijo:
            return
        if eng["podas_autos"]:
            if sum(crit_item[k] for k in elegidos) > 100:
                return
            ai = sum(as_por_item[k] for k in elegidos)
            if const_raw + spec.as_ratio * ai > M.AS_CAP + EPS_AS:
                return
        if faltan == 0:
            combo = ctx_botas + fixed + elegidos
            base = eng["base_fn"](champ, combo, opts)
            if eng["podas_autos"]:
                if base["crit"] < crit_min or base["pen"] < pen_min:
                    return
            hojas += 1
            r = eval_fn(champ, combo, kw1, opts) if kw1 else base
            s = r[met1]
            if len(heap) < embudo:
                heapq.heappush(heap, (s, -g, combo))
            elif s > heap[0][0]:
                heapq.heapreplace(heap, (s, -g, combo))
            return
        for k in orden[start:]:
            dfs(idx[k] + 1, elegidos + [k], g + oro_item[k])

    oro_fijo = sum(gold(k) for k in fixed)
    candidatos = []
    for b in botas:
        ctx_botas = [b]
        oro_save, oro = oro, oro - gold(b)
        dfs(0, [], 0)
        oro = oro_save
        candidatos.extend(heap)
        heap = []

    # pasada 2: objetivo ponderado NORMALIZADO por escenario (+ defensa/utilidad opcionales)
    base_def = cargar_base_def(champ, nivel) if (defensa or utilidad) else None
    brutos = []
    for s1, neg_g, combo in candidatos:
        det = {e: eval_fn(champ, combo, kw, opts)[m] for e, (kw, m) in escenarios.items()}
        base = eng["base_fn"](champ, combo, opts)
        ehp = util = 0.0
        if base_def is not None:
            keys = [M.resolve(c).key for c in combo] if eng is ENGINES["autos"] else list(combo)
            heal_s = base.get("heal", 0.0) if isinstance(base, dict) else 0.0
            ehp, util = ehp_y_util(keys, base_def, heal_s)
        brutos.append((combo, det, base, ehp, util))
    max_e = {e: max((d[e] for _, d, _, _, _ in brutos), default=1.0) or 1.0 for e in escenarios}
    max_ehp = max((x[3] for x in brutos), default=1.0) or 1.0
    max_util = max((x[4] for x in brutos), default=1.0) or 1.0
    finales = []
    for combo, det, base, ehp, util in brutos:
        off = sum(pesos.get(e, 0.0) * (det[e] / max_e[e]) for e in escenarios)
        score = (1 - defensa - utilidad) * off + defensa * (ehp / max_ehp) + utilidad * (util / max_util)
        finales.append((score, combo, det, base, ehp, util))
    finales.sort(key=lambda x: (-x[0], sum(gold(k) for k in x[1])))
    if verbose:
        print(f"[{champ}·{motor}] hojas legales: {hojas:,} · embudo: {len(candidatos)} · "
              f"{time.time()-t0:.1f}s · ≤{oro:,} g · nivel {nivel}")
    return finales[:top], hojas


def imprimir(finales, champ, motor, pesos, oro, con_def=False):
    eng = ENGINES[motor]
    gold = eng["gold_fn"]
    w = " · ".join(f"{e}:{p:g}" for e, p in sorted(pesos.items(), key=lambda x: -x[1]))
    print(f"\n=== TOP builds · {champ} ({motor}) · objetivo [{w}] · ≤{oro:,} g ===")
    cols = list(eng["escenarios"])
    print(f"{'#':>2} {'EFIC':>6} {'ORO':>6} " + " ".join(f"{c:>8}" for c in cols) + "  BUILD")
    tot_w = sum(pesos.values()) or 1.0
    if con_def:
        print(f"(columnas EHP/UTIL activas — pesos defensa/utilidad incluidos en EFIC)")
    for i, fila in enumerate(finales, 1):
        score, combo, det, base = fila[0], fila[1], fila[2], fila[3]
        ehp, util = (fila[4], fila[5]) if con_def else (0, 0)
        og = sum(gold(k) for k in combo)
        extra = f" {ehp/1000:>6.1f}k {util:>6.0f}" if con_def else ""
        print(f"{i:>2} {score/tot_w*100:>5.1f}% {og:>6} "
              + " ".join(f"{det[c]:>8.0f}" for c in cols)
              + extra + f"  {'+'.join(combo)}")


def validar(finales, champ, motor):
    """Compara el top-1 contra las builds publicadas del registro (mismo campeón)."""
    eng = ENGINES[motor]
    reg_path = os.path.join(ROOT, "data", "estructurada", "reportes_registry.json")
    if not os.path.exists(reg_path):
        print("⚠️ sin reportes_registry.json — corre update_reports.py baseline")
        return None
    import json
    with open(reg_path, encoding="utf-8") as fh:
        reg = json.load(fh)
    keys_pool = set(eng["items"]) | set(eng["boots"]) | set(eng["fixed"])

    def norm_keys(bk):
        out = []
        for k in bk:
            if k in keys_pool:
                out.append(k)
            elif eng is ENGINES["autos"]:
                try:
                    out.append(M.resolve(k).key)
                except KeyError:
                    out.append(k)
            else:
                hit = next((p for p in keys_pool if p.lower() == k.lower()), None)
                out.append(hit or k)
        return out

    pubs = []
    for f, e in reg["reportes"].items():
        if e["champion"] != champ or not e.get("build_keys"):
            continue
        bk = norm_keys(e["build_keys"])
        if all(k in keys_pool for k in bk):
            pubs.append((f, bk))
    if not pubs:
        print(f"⚠️ el registro no tiene build publicada compatible con el motor '{motor}' para {champ}")
        return None
    top1 = finales[0][1]
    ok_global = False
    for f, bk in pubs:
        mismo = sorted(bk) == sorted(top1)
        rank = next((i for i, f in enumerate(finales, 1) if sorted(f[1]) == sorted(bk)), None)
        ok_global |= mismo
        print(f"{'✅ REDISCUBIERTA' if mismo else '≠ DIVERGE'} · {f}: "
              f"top-1 {'==' if mismo else '≠'} publicada"
              + ("" if mismo else f" (publicada rankea #{rank} del top-{len(finales)} mostrado)"
                 if rank else " (publicada fuera del top mostrado — corre con --top mayor)")
              + f" · publicada: {'+'.join(bk)}")
    return ok_global


def parse_pesos(s):
    return {par.split(":")[0].strip(): float(par.split(":")[1]) for par in s.split(",")}


def main():
    ap = argparse.ArgumentParser(description="WR-LAB · optimizador exhaustivo de builds (4 motores)")
    ap.add_argument("champion")
    ap.add_argument("--motor", default=None, choices=list(ENGINES),
                    help="default: por campeón (kalista→onhit, diana→rotacion, yuumi/karma→aliado, resto→autos)")
    ap.add_argument("--oro", type=int, default=None, help="presupuesto (default por motor)")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--nivel", type=int, default=15)
    ap.add_argument("--pesos", default=None, help="p.ej. 1v1:0.5,3v3:0.5")
    ap.add_argument("--excluir", default="")
    ap.add_argument("--incluir", default=None)
    ap.add_argument("--botas", default=None)
    ap.add_argument("--keystone", default="lt", help="motor rotacion: lt|empower|conq")
    ap.add_argument("--embudo", type=int, default=400)
    ap.add_argument("--crit-min", type=float, default=0, help="Ley 1 dura (motor autos)")
    ap.add_argument("--pen-min", type=float, default=0, help="Ley 3 dura (motor autos)")
    ap.add_argument("--validar", action="store_true")
    ap.add_argument("--defensa", type=float, default=0.0, help="peso de EHP en el score (0-0.5)")
    ap.add_argument("--utilidad", type=float, default=0.0, help="peso de heal/activas en el score (0-0.5)")
    ap.add_argument("--preset", default=None, choices=list(PRESETS),
                    help="balanceado=70/15/15 ofensivo/defensivo (ver PRESETS)")
    args = ap.parse_args()

    ck = args.champion.lower()
    motor = motor_para(ck, args.motor)
    eng = ENGINES[motor]
    pesos = parse_pesos(args.pesos) if args.pesos else dict(eng["pesos"])
    oro = args.oro or eng["oro_default"]
    finales, hojas = optimizar(ck, motor=motor, oro=oro, top=args.top, pesos=pesos,
                               excluir=tuple(x for x in args.excluir.split(",") if x),
                               incluir=args.incluir.split(",") if args.incluir else None,
                               solo_botas=args.botas, embudo=args.embudo, nivel=args.nivel,
                               crit_min=args.crit_min, pen_min=args.pen_min,
                               keystone=args.keystone, defensa=args.defensa,
                               utilidad=args.utilidad, preset=args.preset)
    imprimir(finales, ck, motor, pesos, oro,
             con_def=bool(args.preset in ("balanceado", "defensivo") or args.defensa or args.utilidad))
    if args.validar:
        print()
        ok = validar(finales, ck, motor)
        if ok is False:
            sys.exit(2)


if __name__ == "__main__":
    main()
```

## 10d. BUSCADOR DE RUNAS (keystone × secundaria · valor marginal · supuestos declarados)

```python
# -*- coding: utf-8 -*-
"""
WR-LAB · optimize_runes.py — buscador de runas (ROADMAP módulo 3)
=================================================================
Puntúa combinaciones KEYSTONE × SECUNDARIA sobre una build dada, con el mismo
esquema del optimizador de builds: escenario por escenario, puntuación ponderada
NORMALIZADA y valor marginal contra el baseline del lab (Lethal Tempo + Alacrity).

Motores soportados (v1):
    autos      (dps_model.eval_build)     → Jinx, Yunara, Sivir, Caitlyn…
    rotacion   (analysis_batch2.diana)    → Diana y magos de rotación (keystones empower/lt/conq)
    onhit/aliado: PENDIENTES (los modelos batch no parametrizan suficientes runas — ver ROADMAP)

FUENTE DE VALORES: data/estructurada/runas_7.3.md (scrape de wr-meta; las notas oficiales
7.3 mandan para Lethal Tempo, ya dentro del motor). SUPUESTOS DECLARADOS (auditables):
    · Conqueror: 5 AD × 6 stacks = 30 AD con uptime 85 % en pelea sostenida (→ 25.5 efectivo)
      + 5 % omnivamp ranged a stacks llenos (va a la columna de sustain, no al DPS).
    · First Strike: +7 % verdadero 3 s cada 25 s → +0.84 % efectivo sostenido (+oro no modelado).
    · Electrocute: 210 (nivel 15) + 10 % AD por proc; **CD 25 s ASUMIDO** (la fuente está cortada
      en "Cooldown:") → verificar en juego antes de publicar conclusiones finas.
    · Coup de Grace: +8 % sobre el 25 % del tiempo de pelea con el objetivo <40 % HP → +2 %.
    · Cut Down: +6.57 % vs >60 % HP → completo en vsTanque, mitad en el resto.
    · Last Stand: 5-11 % bajo 60 % HP → promedio 5 % × ventana 50 % → +2.5 %.
    · Triumph / Legend: Bloodline: sustain/utilidad (columna propia, NO puntúan DPS).
    · Brutal / Sudden Impact / Battle Zeal / Gathering Storm: EXCLUIDOS del modelo v1
      (fuente rasgada sin números fiables / requieren flags por campeón / amplifican
      habilidades fuera del modelo de autos). Motivo registrado en EXCLUIDAS.

USO
    python3 model/optimize_runes.py jinx                       # build publicada del registro
    python3 model/optimize_runes.py jinx --build "Gunmetal,C44,Runaan's,IE,LDR,Kraken"
    python3 model/optimize_runes.py diana --build "Spellslinger,DuskDawn,Nashor,Rabadon,Zhonyas,Cryptbloom"
    python3 model/optimize_runes.py jinx --top 8

VALIDACIÓN: para Jinx debe ganar Lethal Tempo + Legend: Alacrity (conclusión del reporte);
para Diana (rotación), keystone LT (reporte: +30 % DPS sostenido vs Empowerment).
"""
import argparse, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "model"))
import dps_model as M
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import analysis_batch2 as B2
from optimize_build import ENGINES, PESOS_AUTOS, motor_para   # reutiliza motores/normalización

# ---------------------------------------------------------------- catálogo de runas (autos)
KEYSTONES_AUTOS = {
    "Lethal Tempo": dict(lt=True,
        notas="6.4 %/stack ranged + bala 6-24 · valores oficiales 7.3 YA en el motor"),
    "Conqueror": dict(ad_extra=25.5, omnivamp=0.05,
        notas="30 AD a 6 stacks × uptime 85 % = 25.5 · +5 % omnivamp (sustain)"),
    "First Strike": dict(true_amp=0.0084,
        notas="+7 % verdadero 3 s / CD 25 s = +0.84 % sostenido · +oro no modelado"),
    "Electrocute": dict(burst_ad_ratio=0.10, burst_flat=210, burst_cd=25,
        notas="210 + 10 % AD por proc · CD 25 s ASUMIDO (fuente cortada)"),
}
SECONDARIES_AUTOS = {
    "Legend: Alacrity": dict(alacrity=0.21, notas="+21 % AS (3+18 a full stacks) — motor oficial"),
    "Legend: Bloodline": dict(omnivamp=0.08, notas="+8 % omnivamp — sustain, no DPS"),
    "Coup de Grace": dict(cond_amp=0.08, ventana=0.25, notas="+8 % vs <40 % HP × ventana 25 %"),
    "Cut Down": dict(tank_amp=0.0657, otros_amp=0.0329, notas="+6.57 % vs >60 % HP (mitad fuera de vsTanque)"),
    "Last Stand": dict(cond_amp=0.05, ventana=0.50, notas="5-11 % bajo 60 % HP → 5 % × 50 %"),
    "Triumph": dict(utility=True, notas="10 % vida perdida por takedown + 35 MS — utilidad pura"),
}
EXCLUIDAS = {
    "Brutal": "fuente rasgada sin números fiables (verificar en juego)",
    "Sudden Impact": "requiere flag de dash por campeón (no está en ChampSpec)",
    "Battle Zeal": "amplifica habilidades — fuera del modelo de autos",
    "Legend: Haste": "AH de habilidades — solo aplica al motor rotación",
    "Grasp of the Undying": "sustain de melee — fuera del arquetipo autos ranged",
    "Summon Aery / Arcane Comet / Phase Rush / Ice Overlord": "keystones de mago/utilidad — fuera de autos",
}

ESC_AUTOS = ENGINES["autos"]["escenarios"]

# ---------------------------------------------------------------- catálogo (rotación)
KEYSTONES_ROT = {
    "Lethal Tempo": dict(ks="lt", notas="motor batch2: bala adaptativa + AS 38.4 %"),
    "Empowerment": dict(ks="empower", notas="motor batch2: proc 165 + amp 8 %, ICD 4 s"),
    "Conqueror": dict(ks="conq", notas="motor batch2: ~30 adaptivo uptime 60 % + omnivamp"),
}
SECONDARIES_ROT = {
    "Legend: Haste": dict(pen_note="Legend: Haste", notas="+15 AH (tope) — entra en diana()"),
    "— (sin secundaria modelada)": dict(pen_note=None, notas="baseline"),
}


def build_desde_registro(champ):
    reg_path = os.path.join(ROOT, "data", "estructurada", "reportes_registry.json")
    if not os.path.exists(reg_path):
        return None
    with open(reg_path, encoding="utf-8") as fh:
        reg = json.load(fh)
    for f, e in sorted(reg["reportes"].items()):
        if e["champion"] == champ and e.get("build_keys"):
            return e["build_keys"], f
    return None


def eval_par_autos(spec, build, ks, sec, esc_kw, met, nivel=15):
    """Valor del par (keystone, secundaria) para la métrica del escenario + sustain."""
    k, s = KEYSTONES_AUTOS[ks], SECONDARIES_AUTOS[sec]
    r = M.eval_build(spec, build, level=nivel, validate=False,
                     lt=k.get("lt", False), alacrity=s.get("alacrity", 0.0),
                     ad_extra=k.get("ad_extra", 0.0), **esc_kw)
    dps = r[met]
    armor = esc_kw.get("armor", 0.0)
    if k.get("true_amp"):                                   # First Strike: verdadero post-mitigación
        dps *= (1 + k["true_amp"])
    if k.get("burst_flat"):                                 # Electrocute: burst single-target mitigado / CD
        mit = 100 / (100 + armor * (1 - r["pen"] / 100)) if armor > 0 else 1.0
        dps += (k["burst_flat"] + k["burst_ad_ratio"] * r["AD"]) * mit / k["burst_cd"]
    if s.get("cond_amp"):                                   # CdG / Last Stand: ventana declarada
        dps *= (1 + s["cond_amp"] * s["ventana"])
    if s.get("tank_amp"):                                   # Cut Down
        dps *= (1 + (s["tank_amp"] if esc_kw.get("tank") else s["otros_amp"]))
    sustain = r["heal"] + r["dps1"] * (k.get("omnivamp", 0) + s.get("omnivamp", 0))
    return dps, sustain


def buscar_autos(champ, build, top=10, nivel=15, pesos=None):
    spec = M.CHAMPS[champ]
    pesos = pesos or dict(PESOS_AUTOS)
    grid = []
    for ks in KEYSTONES_AUTOS:
        for sec in SECONDARIES_AUTOS:
            det, sustains = {}, []
            for e, (kw, met) in ESC_AUTOS.items():
                d, sus = eval_par_autos(spec, build, ks, sec, kw, met, nivel)
                det[e] = d
                sustains.append(sus)
            grid.append({"ks": ks, "sec": sec, "det": det, "sustain": max(sustains)})
    max_e = {e: max(g["det"][e] for g in grid) or 1.0 for e in ESC_AUTOS}
    for g in grid:
        g["score"] = sum(pesos.get(e, 0) * (g["det"][e] / max_e[e]) for e in ESC_AUTOS)
    base = next(g for g in grid if g["ks"] == "Lethal Tempo" and g["sec"] == "Legend: Alacrity")
    for g in grid:
        g["marginal"] = (g["score"] / base["score"] - 1) * 100 if base["score"] else 0.0
    grid.sort(key=lambda g: (-g["score"], g["ks"]))
    return grid[:top], base


def buscar_rotacion(champ, build, top=10, keystone_build_kw=None):
    grid = []
    for ks_name, ks in KEYSTONES_ROT.items():
        for sec_name, sec in SECONDARIES_ROT.items():
            kw = {"keystone": ks["ks"]}
            if sec.get("pen_note"):
                kw["pen_note"] = sec["pen_note"]
            r = B2.diana(build, **kw)
            rt = B2.diana(build, mr=180, **kw)
            grid.append({"ks": ks_name, "sec": sec_name,
                         "det": {"dps10s": r["dps"], "burst": r["burst"], "vs180mr": rt["dps"]},
                         "sustain": 0.0})
    from optimize_build import PESOS_ROT
    max_e = {e: max(g["det"][e] for g in grid) or 1.0 for e in ("dps10s", "burst", "vs180mr")}
    for g in grid:
        g["score"] = sum(PESOS_ROT[e] * (g["det"][e] / max_e[e]) for e in max_e)
    base = next(g for g in grid if g["ks"] == "Lethal Tempo" and "sin secundaria" in g["sec"])
    for g in grid:
        g["marginal"] = (g["score"] / base["score"] - 1) * 100 if base["score"] else 0.0
    grid.sort(key=lambda g: -g["score"])
    return grid[:top], base


def main():
    ap = argparse.ArgumentParser(description="WR-LAB · buscador de runas (keystone × secundaria)")
    ap.add_argument("champion")
    ap.add_argument("--build", default=None, help="ítems coma-separados (default: publicada en el registro)")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--nivel", type=int, default=15)
    args = ap.parse_args()
    champ = args.champion.lower()
    motor = motor_para(champ)
    if motor not in ("autos", "rotacion"):
        sys.exit(f"motor '{motor}' aún sin soporte de runas (v1: autos y rotacion). Ver ROADMAP.")

    if args.build:
        build = [x.strip() for x in args.build.split(",")]
        origen = "CLI"
    else:
        reg = build_desde_registro(champ)
        if not reg:
            sys.exit("sin build publicada en el registro — pasa --build explícita")
        build, origen = reg
    if motor == "autos":
        build = [M.ALIAS.get(b, b) if b in M.ALIAS else b for b in build]
        M.validate_slots(build)
        grid, base = buscar_autos(champ, build, args.top, args.nivel)
        cols = list(ESC_AUTOS)
    else:
        grid, base = buscar_rotacion(champ, build, args.top)
        cols = ["dps10s", "burst", "vs180mr"]

    base_lbl = "vs baseline" if motor == "rotacion" else "vs LT+Alac"
    print(f"=== RUNAS · {champ} ({motor}) · build: {'+'.join(build)}  [{origen}] ===")
    print(f"{'#':>2} {'SCORE':>6} {base_lbl:>10} {'sustain':>8} " +
          " ".join(f"{c:>8}" for c in cols) + "  KEYSTONE × SECUNDARIA")
    for i, g in enumerate(grid, 1):
        print(f"{i:>2} {g['score']*100:>5.1f}% {g['marginal']:>+9.1f}% {g['sustain']:>8.0f} " +
              " ".join(f"{g['det'][c]:>8.0f}" for c in cols) +
              f"  {g['ks']} × {g['sec']}")
    lbl = ("Lethal Tempo × — (sin secundaria modelada)" if motor == "rotacion"
           else "Lethal Tempo × Legend: Alacrity")
    print(f"\nBaseline del lab: {lbl} = 0.0 % (columna '{base_lbl}' = valor marginal).")
    print("Supuestos declarados en el docstring del módulo; runas excluidas:")
    for r, mot in EXCLUIDAS.items():
        print(f"  · {r}: {mot}")


if __name__ == "__main__":
    main()
```

## 10e. SIMULADOR DE TIMINGS DE ORO (curvas derivadas de las Tablas B del vault)

```python
# -*- coding: utf-8 -*-
"""
WR-LAB · sim_timings.py — simulador de timings de oro (ROADMAP módulo 5 · v1.10)
================================================================================
Fecha los picos de poder de cualquier ruta de compra SIN inventar constantes de economía:
las curvas de oro por rol se DERIVAN de las Tablas B (y tablas de ruta) de los propios
reportes del vault — los "minuto típico" declarados por el autor son las anclas.

    Fuente de las curvas: anclas (minuto, oro acumulado) de reportes/*.md por rol
    (adc / support / jungla / mid / top). Interpolación lineal monótona; extrapolación
    final con pendiente ×0.85 (declive declarado). Sin anclas suficientes se usa la
    curva global (todos los roles). Los valores de minion/passive gold NO están en las
    notas oficiales 7.3 (no cambiaron) → el lab NO los inventa: la calibración es contra
    los reportes publicados (fuente secundaria declarada = estimaciones del autor).

USO
    python3 model/sim_timings.py --curvas                     # ver anclas y curvas por rol
    python3 model/sim_timings.py --reporte reportes/Jinx.md   # chequeo de consistencia
    python3 model/sim_timings.py --reporte reportes/Jinx.md --leave-one-out
        ↑ la curva se arma SIN el reporte auditado (validación honesta)
    python3 model/sim_timings.py --rol adc --build "Berserker's,Hexoptics C44,Terminus,Yun Tal,IE,LDR" --upgrade Gunmetal
        ↑ predice el minuto de cada compra para una ruta NUEVA (p.ej. la variante anti-tanques)

INTEGRACIÓN: menú wrlab.py (🧮 Análisis) · bundle §10e · FRAMEWORK §A paso 7 (curva de poder).
"""
import argparse, csv, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTES = os.path.join(ROOT, "reportes")
sys.path.insert(0, os.path.join(ROOT, "model"))
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import update_reports as U
import dps_model as M
import analysis_batch2 as B2

ROLES = ("adc", "support", "jungla", "mid", "top")
TOLERANCIA_S = 150          # |predicho − declarado| mayor que esto → fila marcada ⚠️
DECLIVE_FINAL = 0.85        # pendiente de extrapolación tras la última ancla (declarado)


# ---------------------------------------------------------------- parseo de rutas de compra
def _num(s):
    s = s.replace("\u00a0", " ").replace(",", "")
    m = re.search(r"(\d[\d\s]*)", s)
    return int(m.group(1).replace(" ", "")) if m else None


def _minutos(cell):
    """'~7:00–8:00'→7.5 · '~11:30 (post 10:00)'→11.5 · '0:00'→0.0 · sin minuto→None."""
    pares = re.findall(r"(\d{1,2}):(\d{2})", cell)
    if not pares:
        return None
    vals = [int(m) + int(s) / 60.0 for m, s in pares]
    if len(vals) >= 2 and ("–" in cell or "-" in cell.split("(", 1)[0] or "a " in cell.lower()):
        return (vals[0] + vals[-1]) / 2.0          # rango → punto medio
    return vals[0]


def parse_ruta(txt):
    """[(compra, oro_acum, minuto)] de la Tabla B o de la tabla de ruta con minutos."""
    seccion = None
    m = re.search(r"###\s+Tabla B(.*?)(?=\n###|\n## )", txt, re.S)
    if m:
        seccion = m.group(1)
    if seccion is None:                            # fallback: primera tabla con col minuto+oro
        for mm in re.finditer(r"((?:^\|.*\|\s*\n)+)", txt, re.M):
            bloque = mm.group(1)
            head = bloque.splitlines()[0].lower()
            if ("minuto" in head or "momento" in head) and ("oro" in head):
                seccion = bloque
                break
    if seccion is None:
        return []
    lineas = [l for l in seccion.splitlines() if l.strip().startswith("|")]
    if len(lineas) < 3:
        return []
    hdr = [c.strip().lower() for c in lineas[0].strip().strip("|").split("|")]
    try:
        i_oro = next(i for i, h in enumerate(hdr) if "oro" in h)
        i_min = next(i for i, h in enumerate(hdr) if "minuto" in h or "momento" in h)
    except StopIteration:
        return []
    i_item = 1 if len(hdr) > 2 else 0
    es_acum = "acum" in hdr[i_oro]
    filas, acum = [], 0
    for l in lineas[2:]:
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) <= max(i_oro, i_min) or set(c[0]) <= set("-: "):
            continue
        oro = _num(c[i_oro])
        if oro is None:
            continue
        if es_acum:
            acum = oro
        else:
            acum += oro
        t = _minutos(c[i_min])
        compra = re.sub(r"\*\*|⬆️", "", c[i_item]).strip()
        filas.append((compra, acum, t))
    return filas


# ---------------------------------------------------------------- roles y anclas
def rol_de(archivo, entry_rol=""):
    s = f"{entry_rol} {archivo}".lower()
    if "jungla" in s or "jungle" in s:
        return "jungla"
    if "support" in s or "soporte" in s:
        return "support"
    if "adc" in s or "dragon" in s or "marksman" in s:
        return "adc"
    if "barón" in s or "baron" in s or re.search(r"\btop\b", s):
        return "top"
    if "mid" in s:
        return "mid"
    return "mid"


def anclas_por_rol(excluir=None):
    """{rol: [(min, oro_acum), …]} desde todos los reportes del vault."""
    reg = {}
    reg_path = os.path.join(ROOT, "data", "estructurada", "reportes_registry.json")
    if os.path.exists(reg_path):
        with open(reg_path, encoding="utf-8") as fh:
            import json
            reg = json.load(fh)["reportes"]
    puntos = {r: [] for r in ROLES}
    detalle = {r: [] for r in ROLES}
    for f in sorted(os.listdir(REPORTES)):
        if not f.endswith(".md") or f == excluir:
            continue
        with open(os.path.join(REPORTES, f), encoding="utf-8") as fh:
            txt = fh.read()
        rol = rol_de(f, (reg.get(f) or {}).get("rol", ""))
        ruta = parse_ruta(txt)
        pts = [(t, o) for _, o, t in ruta if t is not None and o]
        if len(pts) >= 3:
            puntos[rol] += pts
            detalle[rol].append(f"{f} ({len(pts)})")
    glob = [p for r in ROLES for p in puntos[r]]
    return puntos, detalle, glob


def fit_curva(pts):
    """Interpolación lineal monótona: ordena por minuto y fuerza oro no-decreciente."""
    pts = sorted({(round(t, 2), o) for t, o in pts})
    out, last = [], -1
    for t, o in pts:
        o = max(o, last)
        if not out or t > out[-1][0]:
            out.append((t, o))
        else:
            out[-1] = (t, max(o, out[-1][1]))
        last = o
    return out


def oro_en(t, curva):
    if not curva:
        return 0.0
    if t <= curva[0][0]:
        return curva[0][1] * (t / curva[0][0]) if curva[0][0] else curva[0][1]
    for (t0, o0), (t1, o1) in zip(curva, curva[1:]):
        if t <= t1:
            return o0 + (o1 - o0) * (t - t0) / (t1 - t0)
    (t0, o0), (t1, o1) = curva[-2], curva[-1]
    gpm = (o1 - o0) / max(t1 - t0, 0.5) * DECLIVE_FINAL
    return o1 + gpm * (t - t1)


def minuto_para(oro, curva):
    """Inversa de oro_en: minuto en que el oro acumulado alcanza `oro`."""
    if not curva:
        return None
    if oro <= curva[0][1]:
        t0, o0 = curva[0]
        return t0 * (oro / o0) if o0 else 0.0
    for (t0, o0), (t1, o1) in zip(curva, curva[1:]):
        if oro <= o1:
            return t0 + (t1 - t0) * (oro - o0) / max(o1 - o0, 1)
    (t0, o0), (t1, o1) = curva[-2], curva[-1]
    gpm = (o1 - o0) / max(t1 - t0, 0.5) * DECLIVE_FINAL
    return t1 + (oro - o1) / gpm if gpm > 0 else None


def fmt_min(t):
    if t is None:
        return "—"
    return f"{int(t)}:{round((t - int(t)) * 60):02d}"


# ---------------------------------------------------------------- comandos
def precio(display):
    """oro de un ítem visible: motor autos → batch2 → CSV oficial."""
    k = U.resolver_clave(display, "autos")
    if k:
        try:
            return M.resolve(k).gold          # acepta alias ("LDR") y claves ("ldr")
        except KeyError:
            pass
    for dic, tipo in ((B2.K_ITEMS, "onhit"), (B2.D_ITEMS, "rotacion"), (B2.Y_ITEMS, "aliado")):
        k2 = U.resolver_clave(display, tipo)
        if k2 and k2 in dic:
            return dic[k2].get("g", 0)
    with open(os.path.join(ROOT, "data", "estructurada", "items_7.3.csv"),
              encoding="utf-8", newline="") as fh:
        for fila in csv.reader(fh):
            if fila and fila[0].lower() == display.lower():
                return _num(fila[1]) or 0
    return None


def cmd_curvas(args):
    puntos, detalle, glob = anclas_por_rol()
    print("=== CURVAS DE ORO POR ROL (derivadas de las Tablas B del vault) ===")
    print(f"{'ROL':<9} {'ANCLAS':>6}  REPORTES FUENTE")
    for r in ROLES:
        if puntos[r]:
            print(f"{r:<9} {len(puntos[r]):>6}  {', '.join(detalle[r])}")
        else:
            print(f"{r:<9} {0:>6}  (sin anclas — se usaría la curva global)")
    print(f"global    {len(glob):>6}")
    for r in ROLES:
        if puntos[r]:
            c = fit_curva(puntos[r])
            marcas = " ".join(f"{fmt_min(t)}→{o:,}" for t, o in c[::max(1, len(c)//6)])
            print(f"  {r:<8} {marcas}")


def cmd_reporte(args):
    archivo = os.path.basename(args.reporte)
    with open(os.path.join(REPORTES, archivo), encoding="utf-8") as fh:
        txt = fh.read()
    reg = {}
    reg_path = os.path.join(ROOT, "data", "estructurada", "reportes_registry.json")
    if os.path.exists(reg_path):
        import json
        with open(reg_path, encoding="utf-8") as fh:
            reg = json.load(fh)["reportes"]
    rol = rol_de(archivo, (reg.get(archivo) or {}).get("rol", ""))
    excluir = archivo if args.leave_one_out else None
    puntos, detalle, glob = anclas_por_rol(excluir=excluir)
    pts = puntos[rol] if len(puntos[rol]) >= 3 else glob
    fuente = f"rol {rol}" if len(puntos[rol]) >= 3 else "GLOBAL (rol sin anclas suficientes)"
    if excluir:
        fuente += f" · leave-one-out (sin {archivo})"
    curva = fit_curva(pts)
    ruta = parse_ruta(txt)
    print(f"=== TIMINGS · {archivo} · curva: {fuente} ({len(pts)} anclas) ===")
    print(f"{'#':>2} {'COMPRA':<44} {'ORO ACUM':>9} {'DECLARADO':>10} {'PREDICHO':>9} {'Δ':>7}")
    malas = 0
    for i, (compra, oro, t_dec) in enumerate(ruta, 1):
        t_pred = minuto_para(oro, curva)
        if t_dec is None or t_pred is None:
            d = ""
        else:
            ds = (t_pred - t_dec) * 60
            d = f"{ds:+.0f}s"
            if abs(ds) > TOLERANCIA_S:
                d += " ⚠️"
                malas += 1
        print(f"{i:>2} {compra[:44]:<44} {oro:>9,} {fmt_min(t_dec) if t_dec is not None else '—':>10} "
              f"{fmt_min(t_pred):>9} {d:>7}")
    print(f"\nFilas fuera de tolerancia (±{TOLERANCIA_S}s): {malas}/{len(ruta)}"
          + ("  ← ruta inconsistente con la economía del rol" if malas else "  ✅ ruta consistente"))


def cmd_build(args):
    puntos, _, glob = anclas_por_rol()
    pts = puntos[args.rol] if len(puntos.get(args.rol, [])) >= 3 else glob
    curva = fit_curva(pts)
    items = [x.strip() for x in args.build.split(",") if x.strip()]
    upgrades = [x.strip() for x in (args.upgrade or "").split(",") if x.strip()]
    print(f"=== RUTA NUEVA · rol {args.rol} · curva {'del rol' if pts is not glob else 'GLOBAL'} "
          f"({len(pts)} anclas) ===")
    acum, t_ant = 0, 0.0
    filas = []
    for it in items:
        g = precio(it)
        if g is None:
            print(f"  ⚠️ precio desconocido: '{it}' — fila omitida")
            continue
        acum += g
        t = minuto_para(acum, curva) or 0
        t = max(t, t_ant)
        filas.append((it, acum, t))
        t_ant = t
    for up in upgrades:                       # mejora T2→T3: +1 000 g, nunca antes de 10:00
        g = 1000
        acum += g
        t = max(minuto_para(acum, curva) or 0, t_ant, 10.0)
        filas.append((f"⬆️ {up} (mismo slot)", acum, t))
        t_ant = t
    print(f"{'COMPRA':<46} {'ORO ACUM':>9} {'MINUTO PREDICHO':>16}")
    for it, acum_, t in filas:
        print(f"{it[:46]:<46} {acum_:>9,} {fmt_min(t):>16}")
    if filas:
        print(f"\nPico final (6 slots): {fmt_min(filas[-1][2])} con {filas[-1][1]:,} g")
        print("(modelo continuo de oro: las compras reales ocurren en recalls — los picos "
              "tempranos son de referencia)")


def main():
    ap = argparse.ArgumentParser(description="WR-LAB · simulador de timings de oro (curvas del vault)")
    ap.add_argument("--curvas", action="store_true", help="ver anclas/curvas por rol")
    ap.add_argument("--reporte", default=None, help="chequear la Tabla B de un reporte publicado")
    ap.add_argument("--leave-one-out", action="store_true",
                    help="arma la curva SIN el reporte auditado (validación honesta)")
    ap.add_argument("--rol", default=None, choices=ROLES, help="rol para --build")
    ap.add_argument("--build", default=None, help="ítems coma-separados (nombres visibles)")
    ap.add_argument("--upgrade", default=None, help="botas T3 a mejorar tras min 10:00 (+1 000 g)")
    args = ap.parse_args()
    if args.reporte:
        cmd_reporte(args)
    elif args.build:
        if not args.rol:
            sys.exit("--build requiere --rol (adc/support/jungla/mid/top)")
        cmd_build(args)
    else:
        cmd_curvas(args)


if __name__ == "__main__":
    main()
```

<!-- generado por model/build_bundles.py · 02/10/2026 · lite · sha256(cuerpo)=d44e54afb94f9765 · NO editar a mano: editar las fuentes y regenerar -->
