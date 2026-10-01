#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WR-LAB · wrlab.py — CLI unificado + menú interactivo (ROADMAP módulo 1 · v1.9)
===============================================================================
Un solo punto de entrada para TODO el laboratorio. Dos modos:

INTERACTIVO (menú escalable — sin argumentos):
    python3 wrlab.py
    → menú numerado por secciones; cada acción pide solo los parámetros que necesita.
    → para añadir funcionalidades nuevas: registrar una entrada en MENU (abajo).

NO INTERACTIVO (scripts/CI/chat externo):
    python3 wrlab.py estado                  # salud local: check reportes + bundles + lint
    python3 wrlab.py watch                   # vigía de parches + win rates (red; exit 1 si hay cambios)
    python3 wrlab.py winrates                # refresca SOLO las win rates (wr-meta, Diamond+)
    python3 wrlab.py hotfix 7.3b             # CICLO COMPLETO §E pasos 7-8 (con confirmación)
    python3 wrlab.py triage|refresh|borrador|annotate|baseline [--patch X] [--apply]
    python3 wrlab.py optimize <champ> [flags de optimize_build…]
    python3 wrlab.py runes <champ> [flags de optimize_runes…]
    python3 wrlab.py lint [--strict] [--solo X.md]
    python3 wrlab.py tests | bundles | db | motor | git
"""
import os, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable or "python3"


def run(*cmd, check=False):
    """Ejecuta un comando del lab (cwd = raíz) con salida en vivo. Devuelve exit code."""
    print(f"\n$ {' '.join(cmd)}\n" + "─" * 72)
    r = subprocess.run(list(cmd), cwd=ROOT)
    print("─" * 72 + f"\n[exit {r.returncode}]")
    if check and r.returncode != 0:
        sys.exit(r.returncode)
    return r.returncode


def py(script, *args):
    return run(PY, os.path.join("model", script), *args)


def preguntar(mensaje, default=None):
    if not sys.stdin.isatty():
        if default:
            return default
        sys.exit(f"falta parámetro ({mensaje}) y stdin no es interactivo — pásalo como argumento")
    d = f" [{default}]" if default else ""
    r = input(f"{mensaje}{d}: ").strip()
    return r or (default or "")


# ---------------------------------------------------------------- acciones
def acc_estado(_=None):
    ok = True
    ok &= py("update_reports.py", "check") == 0
    ok &= py("build_bundles.py", "--check") == 0
    py("lint_reportes.py")                     # informativo, no rompe el estado
    print("\nEstado general:", "✅ TODO EN ORDEN" if ok else "❌ HAY PENDIENTES (ver arriba)")
    return 0 if ok else 1


def acc_hotfix(patch=None):
    patch = patch or preguntar("Parche del hotfix (ej. 7.3b)", "7.3b")
    print(f"""
CICLO COMPLETO de hotfix {patch} (FRAMEWORK §E pasos 7-8).
⚠️ ANTES de continuar, los pasos 1-6 deben estar hechos (datos nuevos aplicados a
   data/estructurada/, motor y specs; diff estructurado cambios_{patch}.md escrito).
Acciones: triage → refresh --apply → borrador → annotate --apply → baseline
          → tests → bundles → BD → check""")
    if input("¿Continuar? (s/N): ").strip().lower() not in ("s", "sí", "si"):
        print("Cancelado.")
        return 0
    p = ["--patch", patch]
    codes = [py("update_reports.py", "triage", *p),
             py("update_reports.py", "refresh", *p, "--apply"),
             py("update_reports.py", "borrador", *p),
             py("update_reports.py", "annotate", *p, "--apply"),
             py("update_reports.py", "baseline"),
             run(PY, "-m", "unittest", "discover", "-s", "tests"),
             py("build_bundles.py"),
             py("build_db.py"),
             py("update_reports.py", "check")]
    print("\nResumen de códigos:", codes)
    print("→ Falta: revisar borradores en reportes/_borradores/, decidir reemplazos y hacer commit/push.")
    return 0 if all(c == 0 for c in codes) else 1


def acc_optimize(args=None):
    champ = (args or [None])[0] or preguntar("Campeón (jinx, yunara, kalista, diana, yuumi…)", "jinx")
    extra = (args or [])[1:]
    return py("optimize_build.py", champ, *extra)


def acc_runes(args=None):
    champ = (args or [None])[0] or preguntar("Campeón (motor autos o rotacion)", "jinx")
    extra = (args or [])[1:]
    return py("optimize_runes.py", champ, *extra)


def acc_git(_=None):
    run("git", "status", "-sb")
    run("git", "log", "--oneline", "-6")
    run("git", "tag", "-l")
    print("\nPara publicar:  git push origin main --tags   (requiere tus credenciales)")
    return 0


# ---------------------------------------------------------------- menú (registro escalable)
MENU = [
    ("📊 ESTADO", [
        ("Salud del lab (reportes verificados + bundles al día + lint)", lambda _: acc_estado()),
        ("Vigía de parches + win rates — ¿hotfix nuevo? (red)", lambda _: py("check_patch.py")),
        ("Actualizar win rates del roster (wr-meta · Diamond+)", lambda _: py("check_patch.py", "--winrates-only")),
        ("Estado git (status/log/tags)", acc_git),
    ]),
    ("🔥 CICLO DE HOTFIX (FRAMEWORK §E)", [
        ("CICLO COMPLETO: triage→refresh→borrador→annotate→baseline→tests→bundles→BD→check", acc_hotfix),
        ("Solo triage (ver impacto por reporte)", lambda _: py("update_reports.py", "triage")),
        ("Solo refresh --apply (números reproducibles in-place)", lambda _: py("update_reports.py", "refresh", "--apply")),
        ("Solo borrador (esqueletos de ❌ REGENERAR)", lambda _: py("update_reports.py", "borrador")),
        ("Solo annotate --apply (bloques WRLAB-VERIF)", lambda _: py("update_reports.py", "annotate", "--apply")),
        ("Solo baseline (re-sellar registro)", lambda _: py("update_reports.py", "baseline")),
    ]),
    ("🧮 ANÁLISIS", [
        ("Optimizador de builds (4 motores, leyes, presets defensa/utilidad)", acc_optimize),
        ("Buscador de runas (keystone × secundaria, valor marginal)", acc_runes),
        ("Simulador de timings de oro (curvas del vault)", lambda _: py("sim_timings.py", "--curvas")),
        ("Motor de DPS — demo Jinx (validación del engine)", lambda _: py("dps_model.py")),
        ("Lint de reportes del vault", lambda _: py("lint_reportes.py")),
    ]),
    ("📦 ARTEFACTOS", [
        ("Regenerar bundles portables (lite + completo)", lambda _: py("build_bundles.py")),
        ("Reconstruir BD SQLite (wrlab.db)", lambda _: py("build_db.py")),
        ("Tests completos (unittest discover)", lambda _: run(PY, "-m", "unittest", "discover", "-s", "tests")),
    ]),
]

COMANDOS = {   # modo no interactivo
    "estado": lambda a: acc_estado(),
    "watch": lambda a: py("check_patch.py", *a),
    "winrates": lambda a: py("check_patch.py", "--winrates-only", *a),
    "hotfix": lambda a: acc_hotfix(a[0] if a else None),
    "triage": lambda a: py("update_reports.py", "triage", *a),
    "refresh": lambda a: py("update_reports.py", "refresh", *a),
    "borrador": lambda a: py("update_reports.py", "borrador", *a),
    "annotate": lambda a: py("update_reports.py", "annotate", *a),
    "baseline": lambda a: py("update_reports.py", "baseline", *a),
    "check": lambda a: py("update_reports.py", "check"),
    "optimize": lambda a: acc_optimize(a),
    "runes": lambda a: acc_runes(a),
    "timings": lambda a: py("sim_timings.py", *a),
    "lint": lambda a: py("lint_reportes.py", *a),
    "tests": lambda a: run(PY, "-m", "unittest", "discover", "-s", "tests"),
    "bundles": lambda a: py("build_bundles.py", *a),
    "db": lambda a: py("build_db.py"),
    "motor": lambda a: py("dps_model.py"),
    "git": acc_git,
    "menu": lambda a: menu(),
}


def menu_texto():
    lineas = ["", "⚗️  WR-LAB · menú principal  (parche vigente: 7.3+7.3a · Wild Rift)",
              "=" * 62]
    n = 1
    for seccion, acciones in MENU:
        lineas.append(f"\n{seccion}")
        for label, _fn in acciones:
            lineas.append(f"  {n:>2}. {label}")
            n += 1
    lineas.append(f"\n   0. Salir")
    lineas.append("=" * 62)
    return "\n".join(lineas)


def acciones_planas():
    flat = []
    for _, acciones in MENU:
        flat.extend(acciones)
    return flat


def menu():
    flat = acciones_planas()
    while True:
        print(menu_texto())
        try:
            sel = input("\nOpción: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if sel in ("0", "q", "salir", ""):
            return 0
        if not sel.isdigit() or not (1 <= int(sel) <= len(flat)):
            print("⚠️ opción no válida")
            continue
        label, fn = flat[int(sel) - 1]
        print(f"\n▶ {label}")
        try:
            fn(None)
        except SystemExit as e:              # los scripts del lab usan sys.exit
            print(f"[exit {e.code}]")
        except (EOFError, KeyboardInterrupt):
            print("\n(interrumpido)")
        try:
            input("\n— Enter para volver al menú —")
        except (EOFError, KeyboardInterrupt):
            return 0


def main():
    if len(sys.argv) > 1:
        cmd, resto = sys.argv[1], sys.argv[2:]
        if cmd not in COMANDOS:
            print(__doc__)
            sys.exit(f"comando desconocido: '{cmd}' (válidos: {', '.join(COMANDOS)})")
        sys.exit(COMANDOS[cmd](resto) or 0)
    if not sys.stdin.isatty():
        print(__doc__)
        print("(stdin no es una terminal — usa un subcomando, o ejecuta en una terminal para el menú)")
        sys.exit(0)
    sys.exit(menu())


if __name__ == "__main__":
    main()
