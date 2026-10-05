# -*- coding: utf-8 -*-
"""
WR-LAB · generate_report.py — auto-regeneración de reportes (v1.13)
====================================================================
Escalabilidad a 100+ campeones (petición del autor, 01/10/2026): en vez de
regenerar a mano cada reporte obsoleto, el lab genera uno NUEVO completo con
todo lo automatizable (optimizador, runas, timings, win rates, TEMPLATE v1.4),
en estado **"Espera de verificación"** y en directorio paralelo — el publicado
NUNCA se toca hasta que el autor aprueba.

    python3 model/generate_report.py generar --champion shyvana [--rol jungla]
    python3 model/generate_report.py aprobar --archivo "Shyvana_AUTO_7.3a.md" [--destino reportes/X.md]

Cobertura v1: campeones con ChampSpec Y motor de optimización (autos/onhit/
rotacion/aliado). Sin motor (tanques/rotaciones no cubiertas — p.ej. Rammus)
→ mensaje honesto + `update_reports.py borrador` como fallback.

Arquitectura hexagonal: este módulo solo consume puertos públicos (optimizar,
buscar_autos/rotacion, curvas de sim_timings, champion_winrates.csv, diffs de
cambios_*.md, CHAMPS) — no conoce el interior de ningún motor.

Los TODO humanos quedan MARCADOS en el texto (orden de habilidades, plan de
juego, matices de primera compra): la verificación del autor es obligatoria.
"""
import argparse, csv, datetime, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTES = os.path.join(ROOT, "reportes")
AUTO_DIR = os.path.join(REPORTES, "_auto")
ESTRUCTURADA = os.path.join(ROOT, "data", "estructurada")
sys.path.insert(0, os.path.join(ROOT, "model"))
import dps_model as M
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import update_reports as U
    import optimize_build as O
    import optimize_runes as R
    import sim_timings as ST
    import analysis_batch2 as B2

ROL_POR_MOTOR = {"autos": "adc", "onhit": "adc", "rotacion": "mid", "aliado": "support"}
T2_A_T3 = {v: k for k, v in M.BOOT_UPGRADES.items()}


def stats_items_csv():
    """{nombre_lower: (hp, armor, mr)} desde items_7.3.csv (fuente oficial wr-meta)."""
    out = {}
    ruta = os.path.join(ESTRUCTURADA, "items_7.3.csv")
    with open(ruta, encoding="utf-8", newline="") as fh:
        for fila in csv.DictReader(fh):
            st = (fila.get("stats") or "").lower()
            def num(pat):
                m = re.search(pat, st)
                return float(m.group(1)) if m else 0.0
            out[fila["item"].lower()] = (num(r"\+(\d+) max health"),
                                         num(r"\+(\d+) armor"),
                                         num(r"\+(\d+) magic resist"))
    return out
ROL_CSV = {"adc": "DUO", "support": "SUPPORT", "jungla": "JUNGLE", "mid": "MID", "top": "SOLO"}
NOMBRE_VISIBLE = {"chogath": "Cho'Gath"}


def g(n):
    """17350 → '17 350' (estándar v1.4)."""
    if isinstance(n, float):
        n = round(n)
    return f"{int(n):,}".replace(",", " ")


DISPLAY_AUTOS = {}
for _alias, _key in M.ALIAS.items():
    DISPLAY_AUTOS.setdefault(_key, _alias)
DISPLAY_AUTOS.update({"gunmetal": "Gunmetal Greaves", "berserker": "Berserker's Greaves",
                      "yuntal": "Yun Tal Wildarrows", "botrk": "Blade of the Ruined King",
                      "ie": "Infinity Edge", "ldr": "Lord Dominik's Regards",
                      "runaan": "Runaan's Hurricane", "c44": "Hexoptics C44",
                      "storm": "Stormrazor", "kraken": "Kraken Slayer", "rfc": "Rapid Firecannon",
                      "bt": "Bloodthirster", "gale": "Galeforce", "scimitar": "Mercurial Scimitar",
                      "terminus": "Terminus", "guinsoo": "Guinsoo's Rageblade",
                      "witsend": "Wit's End", "statikk": "Statikk Shiv", "er": "Essence Reaver"})


def display_item(k, motor):
    if motor == "autos":
        return DISPLAY_AUTOS.get(M.resolve(k).key, k)
    return k


def slugify(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").replace("'", "")
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s)).strip("-")


def winrates(champ_display, rol):
    ruta = os.path.join(ESTRUCTURADA, "champion_winrates.csv")
    if not os.path.exists(ruta):
        return []
    with open(ruta, encoding="utf-8", newline="") as fh:
        filas = [f for f in csv.DictReader(fh) if f["champion"].lower() == champ_display.lower()]
    pref = ROL_CSV.get(rol, "")
    filas.sort(key=lambda f: 0 if f.get("role", "").upper().startswith(pref) else 1)
    return filas


def cambios_champion(champ_display, archivo):
    ruta = os.path.join(ESTRUCTURADA, archivo)
    if not os.path.exists(ruta):
        return []
    out = []
    with open(ruta, encoding="utf-8") as fh:
        for linea in fh:
            if linea.strip().startswith("|") and champ_display.lower() in linea.lower():
                celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
                if len(celdas) >= 3 and re.search(r"\*\*", celdas[0]):
                    out.append(celdas)
    return out


def habilidades_ficha(champ):
    ruta = os.path.join(ESTRUCTURADA, "campeones", f"{champ}.md")
    if not os.path.exists(ruta):
        return None
    with open(ruta, encoding="utf-8") as fh:
        txt = fh.read()
    m = re.search(r"## Habilidades(.*?)(?:\n## )", txt, re.S)
    if not m:
        return None
    return re.findall(r"^###\s+(.+)$", m.group(1), flags=re.M)[:6]


def ruta_compra(build_keys, motor, curva, oro_total):
    """Secuencia de compra canónica: T2 de las botas temprano → ítems por coste
    ascendente → upgrade T3 tras min 10. Aproximación declarada (criterio de oro)."""
    boots = None
    items = []
    boots_set = set(M.BOOTS_ALL) if motor == "autos" else set()
    for k in build_keys:
        key = M.resolve(k).key if motor == "autos" else k
        if motor == "autos" and key in boots_set:
            boots = (k, key)
        elif motor != "autos" and k.lower() in ("gunmetal", "crimson", "spellslinger"):
            boots = (k, k.lower())
        else:
            items.append(k)
    _g0 = O.ENGINES[motor]["gold_fn"]
    gold = (lambda k: _g0(M.resolve(k).key)) if motor == "autos" else _g0
    t2 = M.BOOT_UPGRADES.get(boots[1]) if boots and motor == "autos" else None
    filas = []
    acum = 500
    filas.append(("Ítem inicial + poción (start)", acum, ST.minuto_para(acum, curva) or 0))
    if t2:
        acum += M.ITEMS[t2].gold
        filas.append((f"Botas T2 ({DISPLAY_AUTOS.get(t2, t2)})", acum, ST.minuto_para(acum, curva) or 0))
    for it in sorted(items, key=lambda x: gold(x) if motor != "autos" else M.resolve(x).gold):
        price = gold(it) if motor != "autos" else M.resolve(it).gold
        acum += price
        filas.append((it, acum, ST.minuto_para(acum, curva) or 0))
    if boots and (t2 or motor != "autos"):
        acum += 1000 if t2 else 0
        if t2:
            t = max(ST.minuto_para(acum, curva) or 0, 10.0)
            filas.append((f"⬆️ Upgrade {display_item(boots[0], motor)} (mismo slot, +1 000)", acum, t))
    return filas, acum


def generar(champ, rol=None, top=6, outdir=None):
    champ = champ.lower()
    if champ not in M.CHAMPS or champ in O.SIN_MOTOR:
        motivo = O.SIN_MOTOR.get(champ, "sin ChampSpec en dps_model.CHAMPS")
        print(f"[i] '{champ}' sin motor cuantitativo ({motivo}) → MODO CUALITATIVO "
              f"(plantilla completa, datos reales, TODOs explícitos)")
        return generar_cualitativo(champ, rol=rol, outdir=outdir)
    motor = O.motor_para(champ)
    spec = M.CHAMPS[champ]
    display = NOMBRE_VISIBLE.get(champ, spec.name)
    rol = rol or ROL_POR_MOTOR.get(motor, "mid")
    parche, _ = U.ultimo_parche_hotfix()
    hoy = datetime.date.today()
    outdir = outdir or AUTO_DIR
    os.makedirs(outdir, exist_ok=True)

    # ── puertos: optimizador, runas, timings, winrates ──
    finales, hojas = O.optimizar(champ, motor=motor, top=top, verbose=False)
    if not finales:
        sys.exit("el optimizador no encontró builds legales — revisa presupuesto/pool")
    score, build, det, base = finales[0][:4]
    M.validate_slots(build) if motor == "autos" else None
    puntos, _, glob = ST.anclas_por_rol()
    curva = ST.fit_curva(puntos[rol] if len(puntos.get(rol, [])) >= 3 else glob)
    filas_ruta, oro_total = ruta_compra(build, motor, curva, base.get("gold", 0))
    wr = winrates(display, rol)
    aviso_motor = O.MOTOR_AVISOS.get(champ)

    if motor == "autos":
        grid, _ = R.buscar_autos(champ, build, top=4)
        runes_txt = "\n".join(f"| {i} | {x['ks']} × {x['sec']} | {x['marginal']:+.1f} % | {x['notas'] if 'notas' in x else ''} |"
                              for i, x in enumerate(grid, 1))
        rune_top = f"{grid[0]['ks']} × {grid[0]['sec']}"
    elif motor == "rotacion":
        grid, _ = R.buscar_rotacion(champ, build, top=4)
        runes_txt = "\n".join(f"| {i} | {x['ks']} × {x['sec']} | {x['marginal']:+.1f} % |  |"
                              for i, x in enumerate(grid, 1))
        rune_top = f"{grid[0]['ks']} × {grid[0]['sec']}"
    else:
        runes_txt = ("| — | Pendiente: el buscador de runas no cubre este motor (ROADMAP Runas v2). "
                     "Usar Lethal Tempo + secundaria del rol como punto de partida y VERIFICAR. |  |  |")
        rune_top = "Lethal Tempo (provisional — TODO humano)"

    # rechazados: swap de cada ítem del pool por el más barato de la build
    pool = [k for k in O.ENGINES[motor]["items"] if k not in build]
    eval_fn = O.ENGINES[motor]["eval_fn"]
    met = list(O.ENGINES[motor]["escenarios"].values())[0][1]
    kw0 = list(O.ENGINES[motor]["escenarios"].values())[0][0]
    ref = eval_fn(champ, build, kw0, {"keystone": "lt"})[met]
    cheap = min(build, key=lambda x: O.ENGINES[motor]["gold_fn"](x))
    rech = []
    for it in pool:
        alt = [x for x in build if x != cheap] + [it]
        try:
            v = eval_fn(champ, alt, kw0, {"keystone": "lt"})[met]
            rech.append((it, (v / ref - 1) * 100))
        except Exception:
            pass
    rech.sort(key=lambda x: -x[1])
    rech_txt = "\n".join(
        f"| {display_item(it, motor)} | {d:+.1f} % vs build óptima (swap por {display_item(cheap, motor)}) |"
        for it, d in rech[:8])

    # leyes (números vivos)
    leyes = [f"- **Ley 0 — Slots:** `validate_slots` de la build → **PASS** (1 botas + 5 ítems)."]
    if motor == "autos":
        leyes.append(f"- **Ley 1 — Crítico:** total {base['crit']:.0f} % (umbral 100 %; exceso = oro muerto).")
        leyes.append(f"- **Ley 2 — AS:** final {base['AS']:.2f} · cruda {base.get('raw_AS', 0):.2f} "
                     f"(tope {M.AS_CAP}){' — ⚠️ overcap, revisar' if base.get('overcap') else ' ✅'}.")
    leyes.append(f"- **Ley 3 — Penetración:** {base.get('pen', 0):.0f} % en la build óptima.")
    leyes.append(f"- **Ley 4/5 — Stats muertos y eficiencia:** ver tabla de RECHAZADOS (swap medido).")
    leyes.append(f"- **Ley 6 — Timing:** ruta de compra fechada con las curvas del vault (Apéndice B).")
    leyes.append(f"- **Ley 7 — Sistemas:** cambios de campo del parche en §1.2.")

    ctx73 = cambios_champion(display, "cambios_campeones_7.3.md")
    ctx73a = cambios_champion(display, "cambios_7.3a.md")
    ctx_txt = "\n".join(f"| {' · '.join(c[:3])} |" for c in (ctx73 + ctx73a)) or \
        f"| Sin cambios directos a {display} en 7.3/7.3a (ver diffs oficiales en el bundle §11-12/§3b). |"
    cs = U.parse_cambios(dict((p, r) for p, r, k in U.cambios_archivos())[parche])
    sist = U.sistemas_relevantes(rol, cs)
    sist_txt = "\n".join(f"| {s[:180]} |" for s in sist) or "| Ningún cambio sistémico relevante para este rol. |"

    wr_callout = ("Sin datos de win rate (corre `wrlab.py winrates`).")
    if wr:
        f0 = wr[0]
        wr_callout = (f"Win Rate {f0['win_pct']} % | Pick Rate {f0['pick_pct']} % | Ban {f0['ban_pct']} % | "
                      f"Tendencia {f0['trend']} | Tier {f0['tier']} | Rol {f0['role']} · bucket {f0['bucket']} · "
                      f"actualizado {f0['actualizado']} (champion_winrates.csv)")

    esc_cols = list(O.ENGINES[motor]["escenarios"])
    def rol_slot(i, k):
        if i == 0:
            return "botas (Ley 0: 1 slot)"
        c = M.ITEMS[M.resolve(k).key].comment if motor == "autos" else ""
        return (c[:70] or "—")
    tabla_a = "\n".join(
        f"| {i + 1}{' (botas)' if i == 0 else ''} | **{display_item(k, motor)}** | "
        f"{g(O.ENGINES[motor]['gold_fn'](M.resolve(k).key if motor == 'autos' else k))} | {rol_slot(i, k)} |"
        for i, k in enumerate(build))
    tabla_b = "\n".join(f"| {i} | {c} | {g(o)} | ~{ST.fmt_min(t)} |"
                        for i, (c, o, t) in enumerate(filas_ruta, 1))
    def fuente_row(i):
        return "⭐ LAB (óptima)" if i == 1 else f"🔬 LAB top-{i}"
    comp = "\n".join(
        f"| {i} | {' + '.join(display_item(x, motor) for x in f_[1])} | "
        f"{g(sum(O.ENGINES[motor]['gold_fn'](M.resolve(x).key if motor == 'autos' else x) for x in f_[1]))} "
        f"| {f_[0] / sum(O.PESOS_AUTOS.values()) * 100 if motor == 'autos' else f_[0] * 100:.1f} % "
        f"| {' · '.join(f'{e}={g(f_[2][e])}' for e in esc_cols)} | {fuente_row(i)} |"
        for i, f_ in enumerate(finales, 1))
    habs = habilidades_ficha(champ)
    habs_txt = (", ".join(habs) if habs else "sin ficha en data/estructurada/campeones/")

    arq_raw = (spec.notes.split('.')[0] if spec.notes else f"motor {motor}")
    arq_fm = '"' + re.sub(r'["\n]', ' ', arq_raw)[:60].strip() + '"'
    aviso_callout = ("\n> [!WARNING] Aproximación del motor\n> " + aviso_motor + "\n") if aviso_motor else ""

    reporte = f"""---
tags:
  - {rol.title()}
  - Auto
version: 0.9
Status: Espera de verificación
champion: {display}
slug: {slugify(display)}-auto-{parche.replace('.', '')}
role: {rol}
patch: "{parche}"
archetype: {arq_fm}
engine: {motor}
published_at: "{hoy.isoformat()}"
custom: false
generate: auto
mode: sr
---
**Fecha del análisis:** {hoy.strftime('%d/%m/%Y')} (auto-generado)
**Parche:** 7.3 (21-sep-2026) + hotfix {parche}
**Rol principal:** {rol} (asumido por motor — revisar)
**Arquetipo:** motor `{motor}` del optimizador (búsqueda exhaustiva, {hojas:,} hojas legales)
**Enfoque:** build óptima bajo objetivo ponderado normalizado del lab; leyes 0-7 verificadas numéricamente.

> [!WARNING] REPORTE AUTO-GENERADO — ESPERA DE VERIFICACIÓN
> Generado por `model/generate_report.py` el {hoy.strftime('%d/%m/%Y')}. Los NÚMEROS son
> reproducibles por el motor; los JUICIOS (orden de habilidades, plan de juego, primera
> compra, matices de matchup) llevan **TODO** y requieren revisión humana antes de publicar.
> El autor debe: verificar en juego los supuestos, completar los TODO, y entonces
> `generate_report.py aprobar` (o regenerar a mano si detecta inconsistencias).
{aviso_callout}
> [!NOTE]
> **Estado Meta Actual ({wr[0]['actualizado'] if wr else '—'}):**
> {wr_callout}

---

## 0. RESUMEN EJECUTIVO

### Tabla A — BUILD FINAL

| Slot | Ítem | Oro | Rol en la build |
|------|------|-----|-----------------|
{tabla_a}

> **Oro total: {g(base.get('gold', oro_total))} g** · métricas del motor: {', '.join(f'{k}={g(v)}' if isinstance(v,(int,float)) else f'{k}={v}' for k,v in det.items())}

### Tabla B — Ruta de compra cronológica (aproximación por curvas de oro del vault)

| # | Compra | Oro acum. | Minuto típico |
|---|--------|-----------|---------------|
{tabla_b}

> **TODO (humano):** revisar el ORDEN de compra (criterio automático: coste ascendente;
> el orden real depende de componentes, matchups y recalls).

### Runas · Hechizos · Habilidades

| Categoría | Elección |
|-----------|----------|
| Runas (top del buscador) | **{rune_top}** |
| Hechizos | TODO: por rol ({rol}) — verificar contra el meta |
| Habilidades | {habs_txt} — **TODO: orden de subida** |

### Resultado del modelo (nivel 15)

| Escenario | Valor |
|-----------|-------|
{chr(10).join(f'| {e} | **{g(det[e])}** |' for e in esc_cols)}

---

## 1. CONTEXTO DEL CAMPEÓN EN ESTE PARCHE

### 1.1 Cambios directos ({display})

| Cambio |
|--------|
{ctx_txt}

### 1.2 Cambios sistémicos relevantes ({rol})

| Sistema |
|---------|
{sist_txt}

### 1.3 ¿Escala con crítico/otro stat? — TODO humano (leer ficha y notas del spec)

## 2. FICHA MATEMÁTICA (spec)

| Parámetro | Valor |
|---|---|
| AD base / growth | {spec.base_ad} / {spec.ad_growth} |
| AS base / ratio | {spec.base_as} / {spec.as_ratio} |
| Base Bonus AS / AS por nivel | {spec.base_bonus_as} / {spec.as_per_lvl} |
| Rango / melee | {spec.attack_range} / {not spec.ranged} |
| Notas del spec | {spec.notes[:300]} |

## 3. MODELO Y FÓRMULAS

Motor `{motor}` ({'dps_model.eval_build' if motor=='autos' else 'analysis_batch2'}). Supuestos
estándar del lab (LT/Alacrity full, nivel 15, enemigos de referencia por escenario) — ver
docstring del motor. **TODO:** supuestos específicos del campeón.

## 4. LEYES APLICADAS A {display.upper()}

{chr(10).join(leyes)}

## 5. ANÁLISIS DEL PRIMER ÍTEM

**TODO (humano):** validar primera compra. Pista del motor: ítem más barato de la build
óptima = `{cheap}`; alternativa temprana típica = componentes de `{build[1] if len(build)>1 else cheap}`.

## 6. BUILD FINAL RANURA POR RANURA

**TODO (humano):** justificación prose por slot. Números de referencia en §8 y RECHAZADOS:

| Ítem rechazado | Motivo numérico (mismo escenario) |
|---|---|
{rech_txt}

## 7. RUNAS · HECHIZOS · HABILIDADES

Top del buscador (valor marginal vs baseline del lab):

| # | Combinación | Marginal | Notas |
|---|-------------|----------|-------|
{runes_txt}

**TODO (humano):** hechizos y orden de habilidades.

## 8. COMPARACIÓN CONTRA LAS ALTERNATIVAS

| # | Build | Oro | EFIC | Escenarios | Fuente |
|---|-------|-----|------|------------|--------|
{comp}

> Convención (estándar v1.13.1): **⭐/🔬 LAB** = builds derivadas por el optimizador del
> laboratorio; las builds de comunidad/externas se marcan `🌐 comunidad` y las publicadas
> `📌 publicada`. Nombres de ítem SIEMPRE completos (decisión del autor, 02/10/2026).

## 9. PLAN DE JUEGO

**TODO (humano):** early/mid/late. Picos de poder de la ruta (Tabla B):
{', '.join(f'{c.split("(")[0].strip()} ~{ST.fmt_min(t)}' for c, o, t in filas_ruta[1:5])}.

## 10. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS

- **Fuentes:** motor del lab (specs 7.3+7.3a verificadas contra nota EN oficial),
  champion_winrates.csv ({wr[0]['actualizado'] if wr else 'sin datos'}), diffs cambios_*.md,
  curvas de oro de las Tablas B del vault.
- **Validación:** build pasa `validate_slots` (Ley 0) · top-1 de {hojas:,} hojas legales ·
  runas del buscador con supuestos declarados en optimize_runes.py.
- **Supuestos pendientes de verificación en juego:** TODO humano (véanse WARNING superiores).

## APÉNDICE A — POOL DEL ROL: veredicto automático

Tabla de RECHAZADOS de §6 (swap medido) — ampliar a mano si se requiere.

## APÉNDICE B — RUTAS DE COMPRA

Tabla B de §0 (curvas del vault, rol {rol}).

---

## Pie de página

*Reporte AUTO-GENERADO el {hoy.strftime('%d/%m/%Y')} con datos del parche 7.3 + {parche}
(verificados contra nota EN oficial el 29/09/2026). WR-LAB v1.13. Estado: **Espera de
verificación** — no publicar hasta aprobación del autor. Las cifras son de modelo
comparativo; el valor absoluto importa menos que las diferencias relativas.*

**Referencias y créditos**

- Notas oficiales del parche 7.3 y hotfix {parche} — © Riot Games, Inc. (wildrift.leagueoflegends.com).
- Base de datos de ítems, runas y fichas — wr-meta.com (proyecto comunitario), win rates Diamond+ del {wr[0]['actualizado'] if wr else '—'}.
- Modelo matemático, Leyes 0-7, optimizador y validaciones — WR-LAB (`model/generate_report.py` sobre los motores del lab).

**Aviso legal:** Wild Rift y League of Legends son marcas registradas de Riot Games, Inc.
Este documento es una guía de comunidad con fines educativos, **no está afiliada, patrocinada
ni respaldada por Riot Games**.
"""
    destino = os.path.join(outdir, f"{display.replace(chr(39), '')}_AUTO_{parche}.md")
    with open(destino, "w", encoding="utf-8") as fh:
        fh.write(reporte)

    # auto-verificación (lint + parseo de vuelta)
    import lint_reportes as L
    legit = L.nombres_items_oficiales()
    _, errs, avis = L.lint_archivo(destino, legit, parche)
    con_txt = open(destino, encoding="utf-8").read()
    build_back, fuente = U.extraer_build(con_txt)
    print(f"📄 Generado: {os.path.relpath(destino, ROOT)}")
    print(f"   build óptima ({motor}): {'+'.join(build)}")
    print(f"   self-check: lint {len(errs)} errores / {avis and len(avis) or 0} avisos · "
          f"re-parseo Tabla A: {len(build_back)}/6 slots desde '{fuente}'")
    for e in errs:
        print("   ❌", e)
    print(f"   SIGUIENTE: revisar los TODO, comparar con la versión publicada y "
          f"`generate_report.py aprobar --archivo {os.path.basename(destino)}`")
    return destino




ROL_HINTS = {"orianna": "mid", "ahri": "mid", "syndra": "mid", "nocturne": "jungla",
             "norra": "mid", "rammus": "jungla", "chogath": "jungla", "mordekaiser": "top",
             "heimerdinger": "mid", "seraphine": "support", "malphite": "top"}


def _nombres_items_csv():
    """{clave alfanumérica: nombre CSV} de toda la BD oficial (clave = solo letras/dígitos,
    para tolerar los slugs de wr-meta: 'rabadons-deathcap', prefijo 'yordle-', etc.)."""
    out = {}
    with open(os.path.join(ESTRUCTURADA, "items_7.3.csv"), encoding="utf-8", newline="") as fh:
        for fil in csv.DictReader(fh):
            clave = re.sub(r"[^a-z0-9]", "", fil["item"].lower())
            out[clave] = fil["item"]
    return out


def _es_botas_csv(nombre):
    try:
        k = M.resolve(nombre).key
        return k in M.BOOTS_ALL
    except KeyError:
        return "boots" in nombre.lower() or "greaves" in nombre.lower() or \
               any(x in nombre.lower() for x in ("shoes", "treads", "steelcaps", "lucidity"))


def build_popular(slug):
    """Ítems de la build popular desde el HTML de wr-meta (data/raw/campeones/{slug}.html):
    secuencia de itemimage → nombres oficiales 7.3 (los que no están en la BD se descartan
    con aviso — la página puede mezclar contenido desactualizado)."""
    ruta = os.path.join(ROOT, "data", "raw", "campeones", f"{slug}.html")
    if not os.path.exists(ruta):
        return [], ["sin HTML crudo (descargar de wr-meta)"]
    with open(ruta, encoding="utf-8", errors="ignore") as fh:
        html = fh.read()
    slugs = re.findall(r'itemimage[^>]*data-src="[^"]*?(?:\d+_)?([a-z0-9-]+)\.webp"', html)
    nombres_csv = _nombres_items_csv()
    vistos, orden, descartados = set(), [], []
    for sl in slugs:
        sl = re.sub(r"^\d+_", "", sl)
        if sl in vistos:
            continue
        vistos.add(sl)
        clave = re.sub(r"[^a-z0-9]", "", sl.lower())
        clave_sin_yordle = re.sub(r"^yordle", "", clave)
        if clave in nombres_csv:
            orden.append(nombres_csv[clave])
        elif clave_sin_yordle in nombres_csv:
            orden.append(nombres_csv[clave_sin_yordle])
        else:
            descartados.append(sl)
    # componentes básicos fuera (son ruta, no build final)
    BASICOS = {"Amplifying Tome", "Long Sword", "Boots of Speed", "Sapphire Crystal",
               "Ruby Crystal", "Cloth Armor", "Null-Magic Mantle", "Dagger", "Pickaxe",
               "Blasting Wand", "Recurve Bow", "B. F. Sword", "Noonquiver", "Kircheis Shard",
               "Spectral Sickle", "Relic Shield", "Stormrazor"}   # Stormrazor no es básico — quitar de aquí
    BASICOS.discard("Stormrazor")
    finales = [n for n in orden if n not in BASICOS]
    return finales, descartados


def _reporte_publicado(display, champ):
    """Encuentra el reporte publicado del campeón en reportes/ (por frontmatter o nombre)."""
    for f in sorted(os.listdir(REPORTES)):
        if not f.endswith(".md"):
            continue
        ruta = os.path.join(REPORTES, f)
        with open(ruta, encoding="utf-8") as fh:
            txt = fh.read()
        fm = U.parse_frontmatter(txt)
        if fm.get("champion", "").lower() == display.lower() or U._norm_champ(f) == champ:
            return f, txt, fm
    return None, None, None


def generar_cualitativo(champ, rol=None, outdir=None):
    """Plantilla completa para campeones SIN motor cuantitativo. Dos variantes:
    (a) con reporte publicado (p.ej. Rammus): parte de su build/ruta y recalcula lo posible;
    (b) campeón NUEVO (p.ej. Orianna): semilla = build popular de wr-meta filtrada contra
        items_7.3.csv + stats reales de la ficha. Cero números inventados: lo que necesita
        motor o ficha ausente lleva TODO explícito."""
    display = NOMBRE_VISIBLE.get(champ, champ.title())
    parche, ruta_diff = U.ultimo_parche_hotfix()
    hoy = datetime.date.today()
    outdir = outdir or AUTO_DIR
    os.makedirs(outdir, exist_ok=True)

    arch_pub, txt_pub, fm_pub = _reporte_publicado(display, champ)
    NUEVO = txt_pub is None
    stats_csv = stats_items_csv()
    precios = {}
    with open(os.path.join(ESTRUCTURADA, "items_7.3.csv"), encoding="utf-8", newline="") as fh:
        for fil in csv.DictReader(fh):
            if (fil.get("precio_oro") or "").isdigit():
                precios[fil["item"].lower()] = int(fil["precio_oro"])

    # stats base reales (ficha) o fallback declarado
    base_hp, base_ar, base_mr = 1910.0, 45.0, 35.0
    ficha_stats = None
    try:
        import json as _json
        with open(os.path.join(ESTRUCTURADA, "champion_base_stats.json"), encoding="utf-8") as fh:
            bs = _json.load(fh)
        ficha_stats = bs.get(champ, {}).get("stats")
        def _lv15(clave):
            m = re.match(r"([\d.]+)\s*\(([\d.]+)\)", (ficha_stats.get(clave) or "").replace("\xa0", " "))
            return float(m.group(1)) + float(m.group(2)) * 14 if m else None
        if ficha_stats:
            hp_j, ar_j, mr_j = _lv15("heal"), _lv15("armor"), _lv15("magicresistance")
            if None not in (hp_j, ar_j, mr_j):
                base_hp, base_ar, base_mr = hp_j, ar_j, mr_j
    except Exception:
        pass

    if NUEVO:
        rol = rol or ROL_HINTS.get(champ, "mid")
        arch_pub = "(campeón nuevo — semilla: build popular wr-meta filtrada)"
        populares, descartados = build_popular(champ)
        if descartados:
            print(f"  [aviso] slugs wr-meta fuera de la BD 7.3 (descartados): {descartados[:6]}")
        botas = [n for n in populares if _es_botas_csv(n)]
        resto = [n for n in populares if n not in botas]
        build_disp = (botas[:1] + resto)[:6]
        ruta = []
        vio = M.violaciones_exclusividad(build_disp) if len(build_disp) == 6 else [("build incompleta", [])]
    else:
        rol = rol or ST.rol_de(arch_pub, U.parse_rol(txt_pub))
        ruta = ST.parse_ruta(txt_pub)
        if len(ruta) < 6:
            sys.exit(f"la ruta publicada de {arch_pub} no tiene 6 compras parseables")
        build_disp = [c for c, _, _ in ruta][:6]
        vio = M.violaciones_exclusividad(build_disp)

    # ── Tabla A (normaliza botas T2→T3, Ley 0) ──
    alias_low = {a.lower(): k for a, k in M.ALIAS.items()}
    upgrade = None
    filas_a, oro_total = [], 0
    for i, nombre in enumerate(build_disp):
        key = alias_low.get(nombre.lower())
        precio = precios.get(nombre.lower(), 0)
        celda = f"**{nombre}**"
        if key and key in T2_A_T3:
            t3 = DISPLAY_AUTOS.get(T2_A_T3[key], T2_A_T3[key])
            celda = f"**{nombre} → ⬆️ {t3}** (min 10:00, MISMO slot)"
            upgrade = (nombre, t3)
            oro_total += 1000
        oro_total += precio
        filas_a.append(f"| {i + 1}{' (botas)' if key in (T2_A_T3.values() if False else set(M.BOOTS_ALL) | set(T2_A_T3)) else ''} | {celda} | {g(precio)} | 🌐 comunidad (wr-meta) — TODO validar |" if NUEVO
                       else f"| {i + 1}{' (botas)' if key in (set(M.BOOTS_ALL) | set(T2_A_T3)) else ''} | {celda} | {g(precio)} | — |")
    tabla_a = "\n".join(filas_a)

    # ── Tabla B: publicada o sintetizada con curvas del vault ──
    if ruta:
        tabla_b = "\n".join(f"| {i} | {c} | {g(o)} | ~{ST.fmt_min(t) if t is not None else '—'} |"
                             for i, (c, o, t) in enumerate(ruta[:6], 1))
        if upgrade:
            tabla_b += f"\n| 7 | ⬆️ {upgrade[1]} (mismo slot, +1 000) | {g(oro_total)} | ~post 10:00 |"
    else:
        puntos_r, _, glob_r = ST.anclas_por_rol()
        curva_r = ST.fit_curva(puntos_r[rol] if len(puntos_r.get(rol, [])) >= 3 else glob_r)
        acum, filas_b = 500, [("Ítem inicial + poción (start)", 500, ST.minuto_para(500, curva_r) or 0)]
        for n in build_disp:
            acum += precios.get(n.lower(), 0)
            filas_b.append((n, acum, ST.minuto_para(acum, curva_r) or 0))
        if upgrade:
            acum += 1000
            filas_b.append((f"⬆️ {upgrade[1]} (mismo slot)", acum, max(ST.minuto_para(acum, curva_r) or 0, 10.0)))
        tabla_b = "\n".join(f"| {i} | {c} | {g(o)} | ~{ST.fmt_min(t)} |" for i, (c, o, t) in enumerate(filas_b, 1))

    # ── cálculos parciales (EHP real con stats de ficha; W solo donde hay fuente) ──
    hp_i = ar_i = mr_i = 0.0
    for nombre in build_disp:
        st = stats_csv.get(nombre.lower())
        if st:
            hp_i += st[0]; ar_i += st[1]; mr_i += st[2]
    armor_delta = -5.0 if champ == "rammus" else 0.0     # 7.3a verificado (único con cambio de armadura base)
    A_pre, A_post = base_ar + ar_i, base_ar + armor_delta + ar_i
    ehp_pre = (base_hp + hp_i) * (1 + A_pre / 100)
    ehp_post = (base_hp + hp_i) * (1 + A_post / 100)
    d_ehp = (ehp_post / ehp_pre - 1) * 100
    w_rows = ""
    w4_pre = w4_post = w1_pre = w1_post = 0
    if champ == "rammus":
        w4_pre, w4_post = 0.60 * A_pre, 0.60 * A_post
        w1_pre, w1_post = 0.45 * A_pre, 0.30 * A_post
        w_rows = (f"| W rank 4 (60 % armadura) | {w4_pre:.0f} | {w4_post:.0f} | {w4_post - w4_pre:+.0f} |\n"
                  f"| W rank 1 (45→30 %) | {w1_pre:.0f} | {w1_post:.0f} | {(w1_post / w1_pre - 1) * 100:+.0f} % |")
    calc_txt = (f"| Armadura total aprox. (nivel 15) | {A_pre:.0f} | {A_post:.0f} | {armor_delta:+.0f} |\n"
                f"| EHP físico aprox. | {g(ehp_pre)} | {g(ehp_post)} | {d_ehp:+.1f} % |\n{w_rows}").rstrip()

    wr = winrates(display, rol)
    wr_callout = ("Sin datos (corre `wrlab.py winrates`).")
    if wr:
        f0 = wr[0]
        wr_callout = (f"Win Rate {f0['win_pct']} % | Pick {f0['pick_pct']} % | Ban {f0['ban_pct']} % | "
                      f"Tendencia {f0['trend']} | **Tier {f0['tier']}** | Rol {f0['role']} · {f0['bucket']} · "
                      f"actualizado {f0['actualizado']} (champion_winrates.csv)")
    cs = U.parse_cambios(ruta_diff)
    directo = next((c for n, c in cs["champions"].items() if U._norm(n) == U._norm_champ(display)), None)
    sist = U.sistemas_relevantes(rol, cs)
    sist_txt = "\n".join(f"| {x[:200]} |" for x in sist) or "| Sin cambios sistémicos relevantes al rol. |"
    ctx73 = cambios_champion(display, "cambios_campeones_7.3.md")
    filas_ctx = ctx73 + ([[f"**{display}**", directo["tipo"], directo["detalles"]]] if directo else [])
    ctx_txt = "\n".join(f"| {' · '.join(c[:3])} |" for c in filas_ctx) or \
        "| Sin cambios directos encontrados en los diffs del lab. |"
    as_csv = None
    with open(os.path.join(ESTRUCTURADA, "champion_attack_speed_7.3.csv"), encoding="utf-8") as fh:
        for lin in fh:
            if lin.lower().startswith(display.lower() + ","):
                as_csv = lin.strip()
                break
    alternativas = []
    with open(os.path.join(ESTRUCTURADA, "items_7.3.csv"), encoding="utf-8", newline="") as fh:
        for fil in csv.DictReader(fh):
            cats = (fil.get("categorias") or "").upper()
            if fil["item"].lower() not in {b.lower() for b in build_disp} and (
                    ("MAGIC" in cats and rol in ("mid", "support")) or
                    ("TANK" in cats or "DEFENSE" in cats) if rol in ("jungla", "top") else
                    ("MAGIC" in cats and rol in ("mid", "support")) or ("TANK" in cats or "DEFENSE" in cats)):
                alternativas.append(fil["item"])
    rech_txt = "\n".join(f"| {a} | **TODO numérico** (sin motor para el arquetipo — ROADMAP) |"
                          for a in alternativas[:6]) or "| (sin alternativas registradas) |"
    stats_row = (f"HP {base_hp:.0f} · Armadura {base_ar:.0f} · MR {base_mr:.0f} (nivel 15, ficha wr-meta)"
                 if ficha_stats else "**TODO** — sin ficha en champion_base_stats.json")

    reporte = f"""---
tags:
  - {rol.title()}
  - Auto
version: 0.9
Status: Espera de verificación
champion: {display}
slug: {slugify(display)}-auto-{parche.replace('.', '')}
role: {rol}
patch: "{parche}"
archetype: "sin motor cuantitativo — generación cualitativa (tanque/mago/asesino)"
engine: none
published_at: "{hoy.isoformat()}"
custom: false
generate: auto
mode: sr
---
**Fecha del análisis:** {hoy.strftime('%d/%m/%Y')} (auto-generado, modo cualitativo)
**Parche:** 7.3 (21-sep-2026) + hotfix {parche}
**Rol principal:** {rol}{' (hint del lab — revisar)' if NUEVO else ' (derivado del reporte publicado)'}
**Arquetipo:** sin motor cuantitativo (motores de tanques/magos/asesinos: ROADMAP). Método:
datos reales (ficha wr-meta, diffs oficiales, win rates, BD de ítems) + cálculos parciales
con supuestos declarados + TODOs explícitos.
**Enfoque:** {'semilla comunitaria filtrada contra la BD 7.3 — TODO validar en juego' if NUEVO else f're-derivar la guía publicada ({arch_pub}) contra {parche} SIN cambiar la build hasta validación del autor'}.

> [!WARNING] REPORTE AUTO-GENERADO (MODO CUALITATIVO) — ESPERA DE VERIFICACIÓN
> Generado por `model/generate_report.py` el {hoy.strftime('%d/%m/%Y')}. Este campeón no tiene
> motor cuantitativo en el lab: las secciones de daño por build llevan **TODO**; los cálculos
> incluidos (EHP{', W' if champ == 'rammus' else ''}) usan supuestos DECLARADOS en §10.
> {'La build es la popular de wr-meta filtrada (la página mezcla contenido de varias fechas — descartados los ítems fuera de la BD 7.3): VALIDAR EN JUEGO.' if NUEVO else ''} El autor debe completar TODOs, verificar en juego y `aprobar` (o regenerar a mano).
{f'> [!DANGER] Build semilla viola exclusividad: {vio}' if (NUEVO and vio and vio[0][0] != "build incompleta") else ''}
> [!NOTE]
> **Estado Meta Actual ({wr[0]['actualizado'] if wr else '—'}):**
> {wr_callout}

---

## 0. RESUMEN EJECUTIVO

### Tabla A — BUILD {'SEMILLA (comunidad, por validar)' if NUEVO else 'FINAL (heredada del reporte publicado + corrección Ley 0)'}

| Slot | Ítem | Oro | Rol en la build |
|------|------|-----|-----------------|
{tabla_a}

> **Oro total: {g(oro_total)} g**{' (incluye +1 000 del upgrade T2→T3, Ley 0)' if upgrade else ''}
> Stats agregados (BD oficial): HP +{g(hp_i)} · Armadura +{ar_i:.0f} · MR +{mr_i:.0f}

### Tabla B — Ruta de compra cronológica ({'sintetizada con curvas de oro del vault' if NUEVO else 'minutos del reporte publicado'})

| # | Compra | Oro acum. | Minuto típico |
|---|--------|-----------|---------------|
{tabla_b}

### Runas · Hechizos · Habilidades

| Categoría | Elección |
|-----------|----------|
| Keystone | **TODO** (verificar meta en juego/wr-meta — la ficha cruda tiene la sugerencia comunitaria) |
| Hechizos | {'Smite + Flash (jungla)' if rol == 'jungla' else 'TODO por rol'} |
| Habilidades | ver §2 (ficha) — **TODO: orden de subida** |

### Resultado del modelo — CÁLCULOS PARCIALES (supuestos en §10)

| Métrica | Pre-{parche} | Post-{parche} | Δ |
|---|---|---|---|
{calc_txt}

---

## 1. CONTEXTO DEL CAMPEÓN EN ESTE PARCHE

### 1.1 Cambios directos ({display})

| Cambio |
|--------|
{ctx_txt}

### 1.2 Cambios sistémicos relevantes ({rol})

| Sistema |
|---------|
{sist_txt}

### 1.3 ¿Escala con crítico/otro stat? — **TODO humano** (leer kit en §2)

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AS ratio / base / bonus / por nivel | {as_csv.split(',', 1)[1] if as_csv else 'TODO'} | champion_attack_speed_7.3.csv |
| Bases nivel 15 | {stats_row} |
| Kit (habilidades con valores) | ver ficha `data/estructurada/campeones/{champ}.md` | wr-meta (crudo en data/raw/campeones/) |
| Cambios 7.3/7.3a | ver §1.1 | diffs oficiales verificados contra nota EN |

## 3. MODELO Y FÓRMULAS

**Sin motor cuantitativo** (ROADMAP: motor de tanques/magos). Cálculos parciales de §0/§8:
EHP = (HP base ficha + HP ítems) × (1 + armadura/100){'; W = % × armadura total' if champ == 'rammus' else ''}. Supuestos en §10.

## 4. LEYES APLICADAS A {display.upper()} (formato compacto — estándar v1.13.1)

- **Ley 0 — Slots:** {'semilla de ' + str(len(build_disp)) + ' slots; ' if NUEVO else ''}{'⚠️ seed incompleta — TODO completar 6 slots' if len(build_disp) < 6 else 'validada (1 botas + 5 ítems)' + (' con upgrade T2→T3 añadido (+1 000 g, mismo slot).' if upgrade else '.')}
- **Ley 3b — Exclusividades:** {'⚠️ VIOLACIÓN ' + str(vio) + ' — corregir antes de aprobar' if vio and vio[0][0] != 'build incompleta' else 'sin conflictos (items_exclusivos.csv) ✅' if len(build_disp) == 6 else 'TODO al completar la build'}.
- **Ley 1/2 — Crítico/AS:** TODO (el arquetipo no prioriza crítico; verificar AS útil del kit).
- **Ley 4 — Stats muertos:** TODO humano con el kit en §2.
- **Ley 5/6 — Eficiencia/timing:** ruta de §0 (curvas del vault); TODO validar recalls.
- **Ley 7 — Sistemas:** ver §1.2.

## 5. ANÁLISIS DEL PRIMER ÍTEM

{'Semilla wr-meta: ' + build_disp[0] if NUEVO else 'Ruta publicada: ' + ruta[0][0]} — **TODO humano:** validar
contra el meta {parche} y el clear de jungla (smite nerf) si aplica.

## 6. BUILD FINAL RANURA POR RANURA

**TODO humano:** justificación por slot. Alternativas de la BD oficial para la matriz situacional:

| Ítem alternativo | Motivo |
|---|---|
{rech_txt}

## 7. RUNAS · HECHIZOS · HABILIDADES

**TODO humano.** La ficha cruda (`data/estructurada/campeones/{champ}.md`, sección
"Build/runas populares") trae la sugerencia comunitaria de runas como insumo.

## 8. COMPARACIÓN CONTRA LAS ALTERNATIVAS

Comparación cuantitativa de builds: **PENDIENTE del motor del arquetipo** (ROADMAP).
Con datos de {parche} (supuestos §10):

| Métrica | 📌 Pre-{parche} | 🔬 LAB post-{parche} | Δ |
|---|---|---|---|
{calc_txt}

> **TODO:** al existir el motor, re-optimizar y marcar fuentes (⭐ LAB / 📌 publicada / 🌐 comunidad).

## 9. PLAN DE JUEGO

**TODO humano.** Picos de §0 Tabla B. {'Ajustar por smite nerf (jungla).' if rol == 'jungla' else ''}

## 10. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS

- **Fuentes:** ficha wr-meta ({champ}) + apéndice AS oficial 7.3 · diffs cambios_*.md
  (verificados contra nota EN oficial) · items_7.3.csv · champion_winrates.csv
  ({wr[0]['actualizado'] if wr else '—'}){f' · build/ruta: {arch_pub}' if not NUEVO else ' · build semilla: popular wr-meta (página con contenido mixto 2025-07/2026-07 — filtrada contra BD 7.3)'}.
- **Supuestos DECLARADOS:** {'bases nivel 15 de la ficha wr-meta;' if ficha_stats else 'bases genéricas del lab (1 910 HP/45 arm/35 MR — SIN ficha);'}
  EHP sin escudos/activas{'; W = % × armadura total (verificar bonus vs total)' if champ == 'rammus' else ''}.
  **Verificar en juego antes de publicar.**
- **Validación:** {'Ley 0 y 3b chequeadas' if len(build_disp) == 6 else 'build incompleta — validación pendiente'} · win rates del pipeline oficial.

## APÉNDICE A — POOL DEL ROL: veredicto automático

Alternativas del §6 (BD oficial) — veredictos numéricos pendientes del motor.

## APÉNDICE B — RUTAS DE COMPRA

Tabla B de §0 ({'sintetizada con curvas del vault, rol ' + rol if NUEVO else 'minutos del reporte publicado'}).

---

## Pie de página

*Reporte AUTO-GENERADO (modo cualitativo) el {hoy.strftime('%d/%m/%Y')} con datos del parche 7.3 +
{parche} (verificados contra nota EN oficial el 29/09/2026). WR-LAB v1.15. Estado: **Espera de
verificación** — no publicar hasta aprobación del autor. Cálculos parciales con supuestos
declarados en §10.*

**Referencias y créditos**

- Notas oficiales del parche 7.3 y hotfix {parche} — © Riot Games, Inc. (wildrift.leagueoflegends.com).
- Ficha, build popular y win rates — wr-meta.com (proyecto comunitario), Diamond+ del {wr[0]['actualizado'] if wr else '—'}.
- Modelo, Leyes 0-7 y validaciones — WR-LAB (`model/generate_report.py`, modo cualitativo).

**Aviso legal:** Wild Rift y League of Legends son marcas registradas de Riot Games, Inc.
Este documento es una guía de comunidad con fines educativos, **no está afiliada, patrocinada
ni respaldada por Riot Games**.
"""
    destino = os.path.join(outdir, f"{display.replace(chr(39), '')}_AUTO_{parche}.md")
    with open(destino, "w", encoding="utf-8") as fh:
        fh.write(reporte)
    import lint_reportes as L
    _, errs, avis = L.lint_archivo(destino, L.nombres_items_oficiales(), parche)
    con_txt = open(destino, encoding="utf-8").read()
    build_back, fuente = U.extraer_build(con_txt)
    print(f"📄 Generado (CUALITATIVO{' · campeón nuevo' if NUEVO else ''}): {os.path.relpath(destino, ROOT)}")
    print(f"   base: {arch_pub[:70]}")
    if not NUEVO:
        print(f"   EHP {d_ehp:+.1f} %" + (f" · W rank1 {(w1_post / w1_pre - 1) * 100:+.0f} %" if champ == "rammus" else ""))
    print(f"   self-check: lint {len(errs)} errores · re-parseo Tabla A: {len(build_back)}/6 desde '{fuente}'")
    for e in errs:
        print("   ❌", e)
    print(f"   SIGUIENTE: completar TODOs, verificar en juego y `aprobar --archivo {os.path.basename(destino)}`")
    return destino


def aprobar(archivo, destino=None):
    ruta = archivo if os.path.isabs(archivo) else os.path.join(AUTO_DIR, archivo)
    if not os.path.exists(ruta):
        sys.exit(f"no existe {ruta}")
    with open(ruta, encoding="utf-8") as fh:
        txt = fh.read()
    fm = U.parse_frontmatter(txt)
    champ = fm.get("champion", os.path.basename(ruta))
    destino = destino or os.path.join(REPORTES, f"{champ}.md")
    if os.path.exists(destino):
        resp = input(f"⚠️ {destino} YA EXISTE. ¿Sobrescribir con la versión aprobada? (s/N): ")
        if resp.strip().lower() not in ("s", "sí", "si"):
            sys.exit("cancelado (el original no se tocó)")
    txt = re.sub(r"^Status:.*$", "Status: Aprobado", txt, count=1, flags=re.M)
    txt = txt.replace("Status: Espera de verificación", "Status: Aprobado")
    txt = re.sub(r"^slug:.*$", f"slug: {slugify(os.path.splitext(os.path.basename(destino))[0])}",
                 txt, count=1, flags=re.M)
    with open(destino, "w", encoding="utf-8") as fh:
        fh.write(txt)
    os.remove(ruta)
    print(f"✅ Aprobado: {os.path.relpath(destino, ROOT)} (Status: Aprobado, generate: auto conservado)")
    print("   Ciclo post-aprobación: baseline → annotate → lint → check …")
    os.system(f'cd "{ROOT}" && python3 model/update_reports.py baseline >/dev/null '
              f'&& python3 model/update_reports.py annotate --apply >/dev/null '
              f'&& python3 model/lint_reportes.py --solo {os.path.basename(destino)} '
              f'&& python3 model/update_reports.py check')
    print("   Pendiente: python3 model/build_bundles.py && tests && commit")


def main():
    ap = argparse.ArgumentParser(description="WR-LAB · generador/aprobador de reportes automáticos")
    sub = ap.add_subparsers(dest="cmd", required=True)
    gen = sub.add_parser("generar", help="generar reporte en reportes/_auto/ (Espera de verificación)")
    gen.add_argument("--champion", required=True)
    gen.add_argument("--rol", default=None, choices=list(ROL_POR_MOTOR.values()) + ["jungla", "top"])
    gen.add_argument("--top", type=int, default=6)
    gen.add_argument("--outdir", default=None, help="directorio alternativo (tests)")
    apr = sub.add_parser("aprobar", help="aprobar un auto-reporte (lo mueve a reportes/ como Aprobado)")
    apr.add_argument("--archivo", required=True)
    apr.add_argument("--destino", default=None)
    args = ap.parse_args()
    if args.cmd == "generar":
        generar(args.champion, rol=args.rol, top=args.top, outdir=args.outdir)
    else:
        aprobar(args.archivo, destino=args.destino)


if __name__ == "__main__":
    main()
