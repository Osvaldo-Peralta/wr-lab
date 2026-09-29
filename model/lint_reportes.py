# -*- coding: utf-8 -*-
"""
WR-LAB · lint_reportes.py — validador/linter de reportes (vault y chats externos)
=================================================================================
Revisa cada .md de reportes/ contra los estándares del lab y detecta la deriva
típica de reportes generados en chats externos:

ERRORES (rompen la integrabilidad con el lab):
    · sin frontmatter YAML o sin Status
    · build final no extraíble (ninguna tabla de 6 slots reconocible)
    · build extraída viola la Ley 0 (≠6 slots, 0 o 2+ botas)
    · ÍTEM INEXISTENTE en la base oficial items_7.3.csv (alucinaciones tipo
      "Bastion of Spirits", "Sorcerer's Shoes", "Aurora Guard")

AVISOS (estilo/completitud v1.4, no bloquean):
    · sin 'champion:'/'patch:' en frontmatter (el lab los deriva del archivo)
    · sin línea **Rol principal:** · sin **Parche:** declarado
    · sin bloque WRLAB-VERIF del último hotfix (correr update_reports.py annotate)
    · pie de página / referencias ausentes · números de 4+ dígitos sin espacio de miles

Uso:
    python3 model/lint_reportes.py                 # tabla informativa (exit 0)
    python3 model/lint_reportes.py --strict        # exit 1 si hay ERRORES (para CI/gate)
    python3 model/lint_reportes.py --solo Jinx.md  # un archivo
"""
import argparse, csv, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTES = os.path.join(ROOT, "reportes")
sys.path.insert(0, os.path.join(ROOT, "model"))
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import update_reports as U


def nombres_items_oficiales():
    """Set normalizado de TODO nombre de ítem legítimo (CSV oficial + alias del motor
    + sinónimos del actualizador + diccionarios batch2)."""
    legit = set()
    with open(os.path.join(ROOT, "data", "estructurada", "items_7.3.csv"),
              encoding="utf-8", newline="") as fh:
        for fila in csv.reader(fh):
            if fila and fila[0] and fila[0].lower() != "item":
                legit.add(U._norm(fila[0]))
    import dps_model as M
    import analysis_batch2 as B2
    for a in list(M.ALIAS) + list(M.ITEMS):
        legit.add(U._norm(a))
    for s in U.SINONIMOS:
        legit.add(U._norm(s))
    for dic in (B2.K_ITEMS, B2.D_ITEMS, B2.Y_ITEMS):
        for k in dic:
            legit.add(U._norm(k))
    # formas T2/T3 y nombres compuestos frecuentes ya cubiertos por ALIAS/SINONIMOS
    return legit


def lint_archivo(path, legit, ultimo_patch):
    archivo = os.path.basename(path)
    with open(path, encoding="utf-8") as fh:
        txt = fh.read()
    errores, avisos = [], []
    fm = U.parse_frontmatter(txt)

    if not fm:
        errores.append("sin frontmatter YAML (--- … ---)")
    else:
        if not fm.get("Status"):
            errores.append("frontmatter sin 'Status'")
        if not fm.get("champion"):
            avisos.append("frontmatter sin 'champion:' (el lab lo deriva del nombre de archivo)")
        if not fm.get("patch"):
            avisos.append("frontmatter sin 'patch:' (se usa la línea **Parche:**)")

    if not re.search(r"\*\*Rol principal:\*\*", txt):
        avisos.append("sin línea **Rol principal:** (tags del frontmatter como fallback)")
    pd = U.parche_declarado(fm, txt)
    if not pd:
        avisos.append("sin parche declarado (**Parche:** o patch: en frontmatter)")

    build, fuente = U.extraer_build(txt)
    if not build:
        errores.append("build final no extraíble (ninguna tabla de 6 slots con header de slot)")
    else:
        if len(build) != 6:
            errores.append(f"la build extraída tiene {len(build)} slots (Ley 0: 6)")
        n_boots = sum(1 for b in build if _es_botas(b, legit))
        if n_boots != 1:
            errores.append(f"Ley 0: {n_boots} botas en la build extraída (debe ser exactamente 1)")
        PLACEHOLDERS = ("situacional", "flexible", "según matchup", "segun matchup")
        for b in build:
            if any(p in b.lower() for p in PLACEHOLDERS):
                avisos.append(f"slot con ítem situacional ('{b}') — la build final v1.4 lista un ítem concreto + matriz situacional aparte")
            elif not _item_legitimo(b, legit):
                errores.append(f"ÍTEM INEXISTENTE en items_7.3.csv: '{b}' (¿alucinación o nombre viejo?)")
        if fuente != "Tabla A":
            avisos.append(f"build extraída de '{fuente}' (no Tabla A estándar v1.4)")

    if ultimo_patch and f"WRLAB-VERIF:{ultimo_patch}:START" not in txt:
        avisos.append(f"sin bloque de verificación {ultimo_patch} (update_reports.py annotate --apply)")
    if not re.search(r"^## Pie de página", txt, re.M):
        avisos.append("sin '## Pie de página' (referencias Riot/wr-meta/WR-LAB + aviso legal)")
    resumen = re.search(r"(>\s+\*\*Oro total[^\n]+)", txt)
    if resumen and re.search(r"(?<![\d ])\d{4,}(?![\d ])", resumen.group(1)):
        avisos.append("números de 4+ dígitos sin espacio de miles en el resumen (estándar v1.4: '17 350 g')")
    return archivo, errores, avisos


def _es_botas(nombre, legit):
    n = U._norm(nombre)
    import dps_model as M
    botas_norm = {U._norm(a) for a, k in M.ALIAS.items() if k in M.BOOTS_ALL}
    botas_norm |= {U._norm(k) for k in M.BOOTS_ALL}
    botas_norm |= {U._norm(x) for x in ("crimson lucidity", "gunmetal greaves", "spellslinger's shoes",
                                        "chainlaced crushers", "armored advance", "armorcrusher boots",
                                        "immortal treads", "ionian boots", "berserker's greaves",
                                        "mercury's treads", "plated steelcaps", "boots of mana",
                                        "boots of dynamism", "gluttonous greaves", "boots of speed")}
    return n in botas_norm


def _item_legitimo(nombre, legit):
    n = U._norm(nombre)
    if n in legit:
        return True
    base = U._norm(re.sub(r"\s*\(.*?\)\s*", " ", nombre))     # sin paréntesis
    if base in legit:
        return True
    m = re.search(r"\(([^)]+)\)", nombre)                      # alias entre paréntesis
    if m and U._norm(m.group(1)) in legit:
        return True
    for v in U.expandir_nombre_item(nombre):                   # nombres compuestos
        if U._norm(v) in legit:
            return True
    return False


def main():
    ap = argparse.ArgumentParser(description="WR-LAB · linter de reportes del vault")
    ap.add_argument("--strict", action="store_true", help="exit 1 si hay ERRORES")
    ap.add_argument("--solo", default=None, help="solo estos archivos (coma-separados)")
    args = ap.parse_args()

    legit = nombres_items_oficiales()
    ultimo_patch = U.ultimo_parche_hotfix()[0]
    solo = set(args.solo.split(",")) if args.solo else None
    total_e = total_a = 0
    filas = []
    for f in sorted(os.listdir(REPORTES)):
        if not f.endswith(".md") or (solo and f not in solo):
            continue
        archivo, errs, avis = lint_archivo(os.path.join(REPORTES, f), legit, ultimo_patch)
        total_e += len(errs)
        total_a += len(avis)
        filas.append((archivo, errs, avis))

    print(f"=== LINT de {len(filas)} reportes (ítems oficiales: {len(legit)} nombres; "
          f"último hotfix: {ultimo_patch}) ===")
    for archivo, errs, avis in filas:
        estado = "❌" if errs else ("⚠️ " if avis else "✅")
        print(f"{estado} {archivo:<44} {len(errs)} errores · {len(avis)} avisos")
        for e in errs:
            print(f"     ERROR: {e}")
        for a in avis:
            print(f"     aviso: {a}")
    print(f"\nTotal: {total_e} errores · {total_a} avisos en {len(filas)} reportes.")
    if args.strict and total_e:
        sys.exit(1)


if __name__ == "__main__":
    main()
