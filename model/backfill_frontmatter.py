# -*- coding: utf-8 -*-
"""
WR-LAB · backfill_frontmatter.py — Fase 1 de la migración (contrato de datos)
=============================================================================
Añade al frontmatter de los reportes las claves del CONTRATO_MARKDOWN_FRONTEND.md
que falten, derivándolas de fuentes YA existentes del lab (nombre de archivo,
líneas de metadatos, reportes_registry.json):

    champion · slug · role · patch · archetype · engine · published_at

REGLAS DE SEGURIDAD (paso pequeño y reversible):
    · SOLO añade claves ausentes — nunca modifica ni reordena las existentes
      (tags/version/Status quedan intactos; el frontend mapea Status→status).
    · NUNCA toca el cuerpo del reporte (byte-idéntico fuera del frontmatter).
    · Idempotente: correrlo dos veces no cambia nada la segunda.
    · Dry-run por defecto; --apply escribe.

Uso:
    python3 model/backfill_frontmatter.py            # dry-run: qué añadiría
    python3 model/backfill_frontmatter.py --apply    # escribe
    python3 model/backfill_frontmatter.py --solo Jinx.md
"""
import argparse, os, re, sys, datetime, contextlib, io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTES = os.path.join(ROOT, "reportes")
sys.path.insert(0, os.path.join(ROOT, "model"))
with contextlib.redirect_stdout(io.StringIO()):
    import update_reports as U
    import sim_timings as ST

MESES = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "apr": 4, "may": 5, "jun": 6,
         "jul": 7, "ago": 8, "aug": 8, "sep": 9, "set": 9, "oct": 10, "nov": 11, "dic": 12, "dec": 12}


def slugify(nombre_archivo):
    import unicodedata
    s = re.sub(r"\.md$", "", nombre_archivo).lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")   # sin acentos
    s = s.replace("'", "")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)


def fecha_iso(txt):
    m = re.search(r"\*\*Fecha del análisis:\*\*[^\n]*?(\d{1,2})/(\d{1,2})/(\d{4})", txt)
    if m:
        d, mo, y = m.groups()
        return f"{y}-{int(mo):02d}-{int(d):02d}"
    m = re.search(r"\*\*Fecha del análisis:\*\*[^\n]*?(\d{1,2})[- ]([A-Za-zñ]{3})[-.](\d{4})", txt)
    if m:
        d, mon, y = m.groups()
        mo = MESES.get(mon.lower()[:3])
        if mo:
            return f"{y}-{mo:02d}-{int(d):02d}"
    # formato largo español: "26 de septiembre de 2026"
    m = re.search(r"(\d{1,2}) de ([a-z]+) de (\d{4})", txt, re.I)
    if m:
        d, mon, y = m.groups()
        mo = MESES.get(mon.lower()[:3])
        if mo:
            return f"{y}-{mo:02d}-{int(d):02d}"
    return None


def derivar(archivo, txt, registry):
    """Claves del contrato derivables para este reporte (solo las ausentes se propondrán)."""
    fm = U.parse_frontmatter(txt)
    entry = registry.get(archivo, {})
    rol_texto = U.parse_rol(txt)
    out = {}
    out["champion"] = U.champ_desde_archivo(archivo, fm, txt)
    out["slug"] = slugify(archivo)
    out["role"] = ST.rol_de(archivo, rol_texto)
    p = U.parche_declarado(fm, txt)
    if p:
        out["patch"] = p
    m = re.search(r"\*\*Arquetipo:\*\*\s*([^\n]+)", txt)
    if m:
        out["archetype"] = m.group(1).strip().rstrip("·").strip()
    modelo = entry.get("modelo")
    out["engine"] = modelo if modelo in ("autos", "onhit", "rotacion", "aliado") else "none"
    f = fecha_iso(txt)
    if f:
        out["published_at"] = f
    # v1.1: custom (tag) y variant (sufijo del nombre de archivo)
    tags_bajos = " ".join(re.findall(r"^\s+-\s+(.+)$", txt.split("---")[1], flags=re.M)).lower()
    if "custom" in tags_bajos or "personalizado" in tags_bajos:
        out["custom"] = "true"
    champ_norm = U._norm_champ(out["champion"])
    base = slugify(archivo)
    if base.startswith(champ_norm) and len(base) > len(champ_norm):
        variante = base[len(champ_norm):].strip("-")
        if variante:
            out["variant"] = variante
    return out


def procesar(archivo, txt, registry):
    """Devuelve (nuevo_txt, añadidos) — añade solo claves ausentes, al final del frontmatter."""
    m = re.match(r"^---\n(.*?)\n---(\n?)", txt, re.S)
    if not m:
        return txt, []
    fm = U.parse_frontmatter(txt)
    derivados = derivar(archivo, txt, registry)
    faltan = {k: v for k, v in derivados.items() if k not in fm}
    if not faltan:
        return txt, []
    # patch y published_at entre comillas (convención del vault)
    lineas = []
    for k, v in faltan.items():
        if k in ("patch", "published_at", "custom", "variant", "generate", "mode"):
            lineas.append(f'{k}: "{v}"')
        else:
            lineas.append(f"{k}: {v}")
    nuevo_fm = m.group(1) + "\n" + "\n".join(lineas)
    nuevo = f"---\n{nuevo_fm}\n---{m.group(2)}" + txt[m.end():]
    return nuevo, sorted(faltan)


def main():
    ap = argparse.ArgumentParser(description="WR-LAB · backfill del frontmatter (contrato Fase 1)")
    ap.add_argument("--apply", action="store_true", help="escribir (default: dry-run)")
    ap.add_argument("--solo", default=None, help="solo estos archivos (coma-separados)")
    args = ap.parse_args()

    reg = {}
    try:
        reg = U.cargar_registro().get("reportes", {})
    except SystemExit:
        print("[aviso] sin registro — engine se derivará como 'none'; corre update_reports.py baseline")

    solo = set(args.solo.split(",")) if args.solo else None
    total = 0
    for f in sorted(os.listdir(REPORTES)):
        if not f.endswith(".md") or (solo and f not in solo):
            continue
        ruta = os.path.join(REPORTES, f)
        with open(ruta, encoding="utf-8") as fh:
            txt = fh.read()
        nuevo, añadidos = procesar(f, txt, reg)
        if not añadidos:
            print(f"=  {f:<40} completo")
            continue
        # verificación de seguridad: cuerpo intacto
        cuerpo_viejo = txt.split("\n---\n", 1)[1] if "\n---\n" in txt else ""
        cuerpo_nuevo = nuevo.split("\n---\n", 1)[1] if "\n---\n" in nuevo else ""
        assert cuerpo_viejo == cuerpo_nuevo, f"¡cuerpo modificado en {f}! — aborto"
        total += len(añadidos)
        print(f"{'✍️ ' if args.apply else '── '}{f:<40} +{len(añadidos)}: {', '.join(añadidos)}")
        if args.apply:
            with open(ruta, "w", encoding="utf-8") as fh:
                fh.write(nuevo)
    print(f"\n{'Aplicado' if args.apply else 'Dry-run'}: {total} claves "
          f"{'añadidas' if args.apply else 'se añadirían'}.")
    if args.apply and total:
        print("Siguiente paso: python3 model/lint_reportes.py && python3 -m unittest discover -s tests "
              "&& python3 model/build_bundles.py && commit")


if __name__ == "__main__":
    main()
