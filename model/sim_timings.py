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
