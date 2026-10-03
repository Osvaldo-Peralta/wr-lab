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
# 7c. Para cada ❌ REGENERAR (el publicado NO se toca):
#    con spec+motor  → python3 model/generate_report.py generar --champion <c>
#                      (reporte completo en reportes/_auto/, Status 'Espera de verificación';
#                       el autor revisa TODOs/números y decide: aprobar o regenerar a mano)
#    sin motor       → python3 model/update_reports.py borrador --patch <X.Xx> (esqueleto)
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
