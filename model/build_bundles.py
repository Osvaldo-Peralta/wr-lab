# -*- coding: utf-8 -*-
"""
WR-LAB · build_bundles.py — regenerador de los bundles portables (v1.7)
========================================================================
Los bundles (WR-LAB_lite.md / WR-LAB_completo.md) son ARTEFACTOS DERIVADOS:
se ensamblan SIEMPRE desde las fuentes del lab (metodologia/, data/estructurada/,
model/, tests/, reportes/). Nunca se editan a mano: editar la fuente y regenerar.

    python3 model/build_bundles.py            # regenera ambos bundles
    python3 model/build_bundles.py --check    # CI: falla si los bundles están desfasados
    python3 model/build_bundles.py --lite     # solo el lite

Contenido:
    LITE      = preámbulo + §1-§10c  (metodología, fuentes, datos 7.3/7.3a, runas, sistemas,
                tabla AS 140, ítems compactos, specs, motor, batch2, optimizador)  → análisis
                de campeones en chats externos.
    COMPLETO  = LITE + §11-§18       (diffs oficiales 7.3, fichas de los campeones del equipo,
                reportes publicados del vault, ítems con pasivas, ROADMAP, tests, actualizador
                de reportes e infraestructura)  → respaldo total del laboratorio.

Reglas de ensamblado (idénticas al bundle histórico):
    · documentos .md → tal cual bajo su encabezado de sección;
    · .csv → fence ```csv literal;
    · .py  → fence ```python literal;
    · fichas/reportes → separados por '---';
    · tabla compacta de ítems (§8) → markdown con stats separados por ' / '.
"""
import argparse, csv, datetime, hashlib, io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = os.path.join(ROOT, "data", "estructurada")
PATCH_LABEL = "7.3+7.3a"


def leer(*ruta):
    with open(os.path.join(ROOT, *ruta), encoding="utf-8") as fh:
        return fh.read().rstrip("\n")


def fence(lenguaje, contenido):
    return f"```{lenguaje}\n{contenido.rstrip(chr(10))}\n```"


def csv_literal(rel):
    return fence("csv", leer(*rel.split("/")))


def csv_a_md(rel, columnas=None, pipes_a="/"):
    """CSV → tabla markdown (las '|' internas de las celdas se vuelven ' / ')."""
    with open(os.path.join(ROOT, *rel.split("/")), encoding="utf-8", newline="") as fh:
        filas = list(csv.reader(fh))
    if not filas:
        return ""
    hdr = columnas or filas[0]
    n = len(hdr)
    out = ["| " + " | ".join(hdr) + " |", "|" + "---|" * n]
    for fila in filas[1:]:
        celdas = [(c or "").replace("|", f" {pipes_a} ").strip() for c in fila[:n]]
        celdas += [""] * (n - len(celdas))
        out.append("| " + " | ".join(celdas) + " |")
    return "\n".join(out)


def multi_archivos(dirrel, orden=None):
    """Concatena los .md de un directorio separados por '---'."""
    d = os.path.join(ROOT, *dirrel.split("/"))
    nombres = sorted(f for f in os.listdir(d) if f.endswith(".md"))
    if orden:
        nombres.sort(key=lambda f: (orden.index(f) if f in orden else 99, f))
    partes = []
    for f in nombres:
        with open(os.path.join(d, f), encoding="utf-8") as fh:
            partes.append(fh.read().rstrip("\n"))
    return "\n\n---\n\n".join(partes), len(nombres)


def specs_count():
    sys.path.insert(0, os.path.join(ROOT, "model"))
    from champspecs import SPECS
    return len(SPECS) + (0 if "jinx" in SPECS else 1)


def as_csv_rows(rel):
    with open(os.path.join(ROOT, *rel.split("/")), encoding="utf-8", newline="") as fh:
        return max(0, len(list(csv.reader(fh))) - 1)


# ---------------------------------------------------------------- preámbulo
def preambulo(kind, fecha):
    return f"""> ## ⚠️ LEY 0 — SLOTS (leer antes de proponer CUALQUIER build)
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

> ## 🔥 ESTADO DE DATOS: parche {PATCH_LABEL} — hotfix 7.3a LIBERADO (29-sep-2026) e integrado
> Los cambios de 7.3a (nerfs a Hwei/Malphite/Caitlyn/Senna/Yuumi/Rammus/Syndra; buffs a Samira/Tristana/
> Draven/Viego; Yun Tal AS 35 %; Diadem/Circlet nerf; Death's Dance 3 300; Smite burn −; Nexus 4 000;
> placas −resist) están en §3b y YA aplicados a specs, motor y apéndices de este bundle.
> **✅ Verificado contra la nota EN oficial de 7.3a** (publicada 29-sep-2026): todos los números del
> diff CN aplicado al lab coinciden con la fuente primaria (registro en §3, data/FUENTES.md).
> Sin páginas 7.3b/7.4 al 29-sep-2026.

# ⚗️ WR-LAB PORTABLE ({kind}) — Wild Rift {PATCH_LABEL} · {fecha}
"""


INTRO = {
    "LITE": """> Laboratorio de builds matemáticas en UN archivo. Adjunta o pega este archivo en cualquier
> herramienta/IA y pide: "Usando WR-LAB, genera el análisis nivel-Jinx para {CAMPEÓN},
> siguiendo el ESTÁNDAR VISUAL v1.4 de TEMPLATE_REPORTE.md".
> Versión completa (reportes del vault, fichas, diffs, infraestructura): WR-LAB_completo.md""",
    "COMPLETO": """> Laboratorio COMPLETO en UN archivo: respaldo total del proyecto (todo lo del LITE +
> diffs oficiales 7.3, fichas de los 11 campeones del equipo, reportes publicados con su
> verificación de hotfix, tests e infraestructura). Adjunta este archivo en cualquier
> herramienta/IA y pide: "Usando WR-LAB, genera el análisis nivel-Jinx para {CAMPEÓN},
> siguiendo el ESTÁNDAR VISUAL v1.4 de TEMPLATE_REPORTE.md".""",
}


# ---------------------------------------------------------------- secciones
def secciones_comunes():
    n_specs = specs_count()
    n_as = as_csv_rows("data/estructurada/champion_attack_speed_7.3.csv")
    hotfixes = sorted(f for f in os.listdir(E) if re.match(r"^cambios_\d+\.\d+[a-z]?\.md$", f))
    secs = [
        ("1", "METODOLOGÍA (Ley 0 + las 7 Leyes + flujo)", leer("metodologia", "FRAMEWORK.md")),
        ("1b", "APÉNDICE: ESCALADO DE TAMAÑO (Cho'Gath/Malphite/Shyvana) — actualizado a 7.3a",
         leer("metodologia", "ESCALADO_DE_TAMANIO.md")),
        ("2", "TEMPLATE + GUÍA DE ESTILO (estándar visual obligatorio v1.4)",
         leer("metodologia", "TEMPLATE_REPORTE.md")),
        ("3", "FUENTES Y REGLAS DE VERIFICACIÓN", leer("data", "FUENTES.md")),
    ]
    for i, hf in enumerate(hotfixes):
        patch = re.match(r"^cambios_(\d+\.\d+[a-z]?)\.md$", hf).group(1)
        secs.append((f"3{'bcdefg'[i] if i else 'b'}",
                     f"HOTFIX {patch} — DIFF COMPLETO (APLICADO A ESTE BUNDLE)",
                     leer("data", "estructurada", hf)))
    secs += [
        ("4", "MECÁNICA OFICIAL DE ATTACK SPEED (7.3) + TEST DE CAITLYN",
         leer("data", "estructurada", "mecanica_attack_speed_7.3.md")),
        ("5", "RUNAS (cambios 7.3 + valores)",
         leer("data", "estructurada", "cambios_runas_7.3.md")
         + "\n\n### 5.2 Runas completas\n\n" + leer("data", "estructurada", "runas_7.3.md")),
        ("6", f"SISTEMAS DE CAMPO 7.3 (+ ajustes 7.3a: Smite burn, Nexus, placas — ver §3b)",
         leer("data", "estructurada", "sistemas_campo_7.3.md")),
        ("7", f"TABLA OFICIAL DE ATTACK SPEED — {n_as} CAMPEONES (7.3, con overrides 7.3a marcados)",
         csv_literal("data/estructurada/champion_attack_speed_7.3.csv")
         + "\n\n### 7.2 Durabilidad 7.3\n\n"
         + csv_literal("data/estructurada/champion_durability_7.3.csv")),
    ]
    if os.path.exists(os.path.join(E, "champion_winrates.md")):
        secs.append(("7b", "WIN RATES DEL ROSTER (wr-meta · Diamond+ · las actualiza el vigía 2×/día)",
                     leer("data", "estructurada", "champion_winrates.md")))
    secs += [
        ("8", "BASE DE ÍTEMS 7.3 (compacta — OJO: Boots tier 3 = MISMO slot que su tier 2; "
              "Yun Tal y Death's Dance ya con valores 7.3a en el motor)",
         csv_a_md("data/estructurada/items_7.3.csv",
                  columnas=["Ítem", "Oro", "Stats", "Categorías"])),
        ("8b", "EXCLUSIVIDADES DE ÍTEMS (no pueden convivir en la misma build — validado por "
               "validate_slots/optimizador/lint; escalable: 1 fila = 1 grupo)",
         csv_literal("data/estructurada/items_exclusivos.csv")),
        ("9", f"SPECS PRECARGADAS ({n_specs} campeones, notas 7.3a incluidas)",
         fence("python", leer("model", "champspecs.py"))),
        ("10", "MOTOR DE DPS (con validate_slots — ver Ley 0)",
         fence("python", leer("model", "dps_model.py"))),
        ("10b", "MOTOR SECUNDARIO — modelos batch (Kalista on-hit, Diana rotación, Yuumi/Karma "
                "valor-aliado, TAMAÑO)",
         fence("python", leer("model", "analysis_batch2.py"))),
        ("10c", "OPTIMIZADOR DE BUILDS (4 motores · búsqueda exhaustiva con Leyes 0-1-2-3 · "
                "presets de defensa/utilidad)",
         fence("python", leer("model", "optimize_build.py"))),
        ("10d", "BUSCADOR DE RUNAS (keystone × secundaria · valor marginal · supuestos declarados)",
         fence("python", leer("model", "optimize_runes.py"))),
        ("10e", "SIMULADOR DE TIMINGS DE ORO (curvas derivadas de las Tablas B del vault)",
         fence("python", leer("model", "sim_timings.py"))),
        ("10f", "GENERADOR DE REPORTES (auto-regeneración con Status 'Espera de verificación' + aprobación)",
         fence("python", leer("model", "generate_report.py"))),
    ]
    return secs


def secciones_completo():
    fichas, n_fichas = multi_archivos("data/estructurada/campeones")
    reportes, n_reportes = multi_archivos("reportes")
    return [
        ("11", "CAMBIOS DE CAMPEONES 7.3 (diff oficial)",
         leer("data", "estructurada", "cambios_campeones_7.3.md")),
        ("12", "CAMBIOS DE ÍTEMS 7.3 (diff oficial)",
         leer("data", "estructurada", "cambios_items_7.3.md")),
        ("13", f"FICHAS COMPLETAS DE CAMPEONES ({n_fichas} fichas)", fichas),
        ("14", f"REPORTES PUBLICADOS DEL VAULT ({n_reportes} archivos — con bloques de "
               f"verificación WRLAB-VERIF generados por update_reports.py)", reportes),
        ("15", "BASE DE ÍTEMS COMPLETA (pasivas + tips)",
         csv_literal("data/estructurada/items_7.3.csv")),
        ("16", "ROADMAP DEL PROYECTO (módulos futuros)", leer("ROADMAP.md")),
        ("17", "TESTS DE REGRESIÓN (suite completa)",
         "\n\n".join(fence("python", leer("tests", t)) for t in sorted(
             f for f in os.listdir(os.path.join(ROOT, "tests")) if f.endswith(".py")))),
        ("17b", "ACTUALIZADOR DE REPORTES (triage de hotfixes — Regla de Oro v1.6)",
         fence("python", leer("model", "update_reports.py"))),
        ("18", "INFRAESTRUCTURA (CLI unificado wrlab.py + extract_data · build_db · check_patch · "
               "parse_champs · lint_reportes)",
         fence("python", leer("wrlab.py"))
         + "\n\n" + fence("python", leer("model", "lint_reportes.py"))
         + "\n\n" + fence("python", leer("model", "backfill_frontmatter.py"))
         + "\n\n" + fence("python", leer("model", "estandarizar_metadatos.py"))
         + "\n\n" + fence("python", leer("model", "extract_data.py"))
         + "\n\n" + fence("python", leer("model", "build_db.py"))
         + "\n\n" + fence("python", leer("model", "check_patch.py"))
         + "\n\n" + fence("python", leer("model", "parse_champs.py"))),
    ]


def generar(kind, fecha=None):
    fecha = fecha or datetime.date.today().strftime("%d/%m/%Y")
    secs = secciones_comunes() + (secciones_completo() if kind == "COMPLETO" else [])
    partes = [preambulo(kind, fecha), INTRO[kind], ""]
    for label, titulo, cuerpo in secs:
        partes.append(f"## {label}. {titulo}\n\n{cuerpo.rstrip()}\n")
    texto = "\n".join(partes).rstrip("\n") + "\n"
    # posdata de integridad
    sha = hashlib.sha256(texto.encode()).hexdigest()[:16]
    texto += (f"\n<!-- generado por model/build_bundles.py · {fecha} · {kind.lower()} · "
              f"sha256(cuerpo)={sha} · NO editar a mano: editar las fuentes y regenerar -->\n")
    return texto


def validar(texto, kind):
    """Chequeos de integridad del bundle generado (fallan duro si falta contenido)."""
    motor = leer("model", "dps_model.py")
    problemas = []
    if motor[:2000] not in texto:
        problemas.append("el motor dps_model.py no está embebido íntegro")
    if "def validate_slots" not in texto:
        problemas.append("falta validate_slots")
    n_as = as_csv_rows("data/estructurada/champion_attack_speed_7.3.csv")
    for champ in ("Garen", "Aatrox", "Nunu & Willump"):
        if champ not in texto:
            problemas.append(f"tabla AS incompleta (falta {champ})")
    with open(os.path.join(E, "items_7.3.csv"), encoding="utf-8", newline="") as fh:
        n_items = max(0, len(list(csv.reader(fh))) - 1)
    if texto.count("| 2900 |") < 1:
        problemas.append("tabla compacta de ítems vacía")
    reportes = sorted(f for f in os.listdir(os.path.join(ROOT, "reportes")) if f.endswith(".md"))
    if kind == "COMPLETO":
        for f in reportes:
            cuerpo = leer("reportes", f)
            if cuerpo[:2000] not in texto or cuerpo[-500:].rstrip() not in texto:
                problemas.append(f"reporte ausente o truncado: {f}")
        # Regla v1.15.1: solo los reportes que NO declaran cubrir el hotfix actual
        # necesitan bloque WRLAB-VERIF (los AL_DIA por frontmatter no lo llevan).
        # Antes se exigía 1 bloque por reporte → rompía al publicar guías nuevas
        # verificadas de origen (incidente CI 08/10 con Xayah/Nocturne/Ornn).
        import update_reports as _U
        hotfix = _U.ultimo_parche_hotfix()[0]
        exigen_bloque = 0
        for f in reportes:
            txt_rep = leer("reportes", f)
            fm = _U.parse_frontmatter(txt_rep)
            pd = _U.parche_declarado(fm, txt_rep)
            if not (pd and _U.patch_key(pd) >= _U.patch_key(hotfix)):
                exigen_bloque += 1
        n_verif = len(re.findall(r"WRLAB-VERIF:[\d.]+[a-z]?:(START|END)", texto)) // 2
        if n_verif < exigen_bloque:
            problemas.append(f"solo {n_verif} bloques WRLAB-VERIF para {exigen_bloque} reportes que lo exigen")
        for ficha in sorted(os.listdir(os.path.join(E, "campeones"))):
            if ficha.endswith(".md"):
                primera = leer("data", "estructurada", "campeones", ficha).splitlines()[0]
                if primera not in texto:
                    problemas.append(f"ficha ausente: {ficha}")
    return problemas, n_as, n_items, len(reportes)


def main():
    ap = argparse.ArgumentParser(description="WR-LAB · regenerador de bundles portables")
    ap.add_argument("--check", action="store_true",
                    help="no escribe: falla (exit 1) si los bundles del repo están desfasados")
    ap.add_argument("--lite", action="store_true", help="solo WR-LAB_lite.md")
    ap.add_argument("--completo", action="store_true", help="solo WR-LAB_completo.md")
    ap.add_argument("--fecha", default=None, help="fecha del encabezado (dd/mm/aaaa)")
    args = ap.parse_args()

    kinds = []
    if args.lite:
        kinds = ["LITE"]
    elif args.completo:
        kinds = ["COMPLETO"]
    else:
        kinds = ["LITE", "COMPLETO"]

    fallo = False
    for kind in kinds:
        archivo = os.path.join(ROOT, f"WR-LAB_{kind.lower()}.md")
        texto = generar(kind, args.fecha)
        problemas, n_as, n_items, n_rep = validar(texto, kind)
        if problemas:
            fallo = True
            print(f"❌ {kind}: bundle íntegro NO confirmado:")
            for p in problemas:
                print("   -", p)
            continue
        if args.check:
            actual = open(archivo, encoding="utf-8").read() if os.path.exists(archivo) else ""
            # --check compara ignorando fecha/posdata (líneas volátiles)
            def norm(t):
                t = re.sub(r"\d{2}/\d{2}/\d{4}", "<FECHA>", t)
                return re.sub(r"sha256\(cuerpo\)=[0-9a-f]+", "sha=<X>", t)
            if norm(actual) != norm(texto):
                fallo = True
                print(f"❌ {kind}: {os.path.basename(archivo)} DESFASADO respecto a las fuentes "
                      f"— corre 'python3 model/build_bundles.py'")
            else:
                print(f"✅ {kind}: al día ({len(texto):,} bytes · AS {n_as} · ítems {n_items} · reportes {n_rep})")
        else:
            with open(archivo, "w", encoding="utf-8") as fh:
                fh.write(texto)
            sha = hashlib.sha256(texto.encode()).hexdigest()[:12]
            print(f"✍️  {os.path.basename(archivo)}: {len(texto):,} bytes · sha256 {sha} · "
                  f"AS {n_as} campeones · {n_items} ítems · {n_rep} reportes")
    sys.exit(1 if fallo else 0)


if __name__ == "__main__":
    main()
