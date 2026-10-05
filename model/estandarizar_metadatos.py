# -*- coding: utf-8 -*-
"""
WR-LAB · estandarizar_metadatos.py — frontmatter canónico de TODOS los reportes (v1.15)
========================================================================================
Aplica el estándar de metadatos pedido por el autor (base: el reporte auto-generado
de Shyvana) a reportes/*.md y reportes/_auto/*.md. Diccionario de campos:
deploy/DICCIONARIO_METADATOS.md · contrato: deploy/CONTRATO_MARKDOWN_FRONTEND.md §1.

REGLAS:
    · Solo frontmatter — el cuerpo NO se toca (byte-idéntico, con assert).
    · Conserva claves desconocidas (las appende al final) y los tags tal cual.
    · Normaliza: 'rol:' → 'role:' · completa derivables (champion/slug/role/patch/
      archetype/engine/published_at/custom/variant) · defaults (custom: false,
      generate: manual, mode: sr) · verification/verified_patch/updated_at desde
      reportes_registry.json (solo reportes publicados; los _auto van "pending").
    · Orden canónico de claves (legibilidad en el sitio y diffs estables).
    · Idempotente; dry-run por defecto, --apply escribe.

Uso:  python3 model/estandarizar_metadatos.py [--apply] [--solo X.md]
"""
import argparse, datetime, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTES = os.path.join(ROOT, "reportes")
sys.path.insert(0, os.path.join(ROOT, "model"))
import contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import update_reports as U
    import backfill_frontmatter as B

CANON = ["tags", "version", "Status", "champion", "slug", "role", "variant", "patch",
         "archetype", "engine", "custom", "generate", "mode", "published_at", "updated_at",
         "verification", "verified_patch"]
QUOTE = {"patch", "published_at", "updated_at", "verified_patch", "archetype"}


def _parse_fm_crudo(bloque):
    """(tags_lines, {k: v}, orden_originales) preservando el bloque de tags tal cual."""
    tags_lines, kv, unknown_order = [], {}, []
    in_tags = False
    for lin in bloque.splitlines():
        if re.match(r"^tags:\s*$", lin):
            in_tags = True
            tags_lines.append(lin)
            continue
        if in_tags:
            if re.match(r"^\s+-\s+", lin):
                tags_lines.append(lin)
                continue
            in_tags = False
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", lin)
        if m:
            kv[m.group(1)] = m.group(2).strip()
            unknown_order.append(m.group(1))
    return tags_lines, kv, unknown_order


def _fmt(k, v):
    if v is None or v == "":
        return None
    v = str(v)
    if k in QUOTE and not (v.startswith('"') and v.endswith('"')):
        v = v.replace('"', "'")
        return f'{k}: "{v}"'
    return f"{k}: {v}"


def estandarizar(archivo, ruta, registry):
    with open(ruta, encoding="utf-8") as fh:
        txt = fh.read()
    m = re.match(r"^---\n(.*?)\n---(\n?)", txt, re.S)
    if not m:
        return txt, ["SIN FRONTMATTER — omitido"]
    tags_lines, kv, _ = _parse_fm_crudo(m.group(1))

    # normalizaciones
    notas = []
    if "rol" in kv and "role" not in kv:
        kv["role"] = kv.pop("rol")
        notas.append("rol→role")
    elif "rol" in kv:
        kv.pop("rol")
        notas.append("rol duplicado eliminado")

    # derivables ausentes (misma lógica del backfill, sobre el texto actual)
    fm_simple = dict(kv)
    derivados = B.derivar(archivo, txt, registry)
    for k, v in derivados.items():
        if k not in kv:
            kv[k] = v
            notas.append(f"+{k}")
    kv.setdefault("custom", "false")
    kv.setdefault("generate", "manual")
    kv.setdefault("mode", "sr")

    # verificación desde el registro (solo publicados)
    es_auto = os.path.basename(os.path.dirname(ruta)) == "_auto"
    entry = registry.get(archivo) or {}
    uv = entry.get("ultima_verificacion")
    if not es_auto:
        if uv:
            kv["verification"] = uv.get("veredicto", "")
            kv["verified_patch"] = uv.get("patch", "")
            fecha = uv.get("fecha", "")
            d = re.match(r"(\d{2})/(\d{2})/(\d{4})", fecha or "")
            kv["updated_at"] = f"{d.group(3)}-{d.group(2)}-{d.group(1)}" if d else \
                datetime.date.today().isoformat()
        else:
            kv.setdefault("verification", "pending")
            kv.setdefault("updated_at", datetime.date.today().isoformat())
    else:
        kv["verification"] = "pending"
        kv["updated_at"] = datetime.date.today().isoformat()

    # reconstrucción en orden canónico (+ desconocidas al final)
    lineas = list(tags_lines) if tags_lines else ["tags: []"]
    if "tags" not in kv:
        pass
    for k in CANON:
        if k == "tags":
            continue
        if k in kv:
            lin = _fmt(k, kv[k])
            if lin:
                lineas.append(lin)
    extras = [k for k in kv if k not in CANON and k != "tags"]
    for k in extras:
        lineas.append(_fmt(k, kv[k]))
        notas.append(f"clave desconocida conservada: {k}")

    nuevo_fm = "\n".join(lineas)
    nuevo = f"---\n{nuevo_fm}\n---{m.group(2)}" + txt[m.end():]
    # seguridad: cuerpo intacto
    assert nuevo.split("\n---\n", 1)[1] == txt.split("\n---\n", 1)[1], f"cuerpo alterado en {archivo}"
    return nuevo, notas


def main():
    ap = argparse.ArgumentParser(description="WR-LAB · frontmatter canónico (estándar Shyvana)")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--solo", default=None)
    args = ap.parse_args()

    reg = {}
    try:
        reg = U.cargar_registro().get("reportes", {})
    except SystemExit:
        print("[aviso] sin registro — verification/updated_at quedarán 'pending'/hoy")

    total = 0
    for carpeta, usa_reg in ((REPORTES, True), (os.path.join(REPORTES, "_auto"), False)):
        if not os.path.isdir(carpeta):
            continue
        for f in sorted(os.listdir(carpeta)):
            if not f.endswith(".md") or (args.solo and f != args.solo):
                continue
            ruta = os.path.join(carpeta, f)
            nuevo, notas = estandarizar(f, ruta, reg if usa_reg else {})
            with open(ruta, encoding="utf-8") as fh:
                actual = fh.read()
            if nuevo == actual:
                print(f"=  {f:<44} ya canónico")
                continue
            total += 1
            print(f"{'✍️ ' if args.apply else '── '}{f:<44} {', '.join(notas) or 'reordenado'}")
            if args.apply:
                with open(ruta, "w", encoding="utf-8") as fh:
                    fh.write(nuevo)
    print(f"\n{'Aplicado' if args.apply else 'Dry-run'}: {total} archivos. Orden canónico: "
          f"{' · '.join(CANON)}")


if __name__ == "__main__":
    main()
