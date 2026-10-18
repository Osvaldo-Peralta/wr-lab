# -*- coding: utf-8 -*-
"""WR-LAB · model/refresh_winrates.py (v1.19) — refresca SOLO los win rates del
callout meta de cada reporte desde data/estructurada/champion_winrates.csv
(el CSV lo mantiene el vigía 2×/día). Tarea 2 del autor (14/10/2026):
"de todas las guías solo modificarás el win rate; el resto intacto".

Reglas:
  · Solo toca líneas del callout `> [!NOTE]` que contiene "Estado Meta".
  · Cada segmento "Win Rate X %" toma su rol de la etiqueta que lo precede
    (SUPPORT/DUO/SOLO/JUNGLE/MID) o del frontmatter del reporte.
  · Actualiza Win Rate, Pick Rate, Ban, Tendencia y la fecha (Diamond+, DD/MM/AAAA).
  · Sin fila CSV para el campeón → no toca e informa. Idempotente.

Uso:  python3 model/refresh_winrates.py [--apply] [--solo X.md]
"""
import argparse
import csv
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTES = os.path.join(ROOT, "reportes")
CSV = os.path.join(ROOT, "data", "estructurada", "champion_winrates.csv")
ROL_CSV = {"adc": "DUO", "support": "SUPPORT", "jungla": "JUNGLE", "mid": "MID", "top": "SOLO"}
ETIQUETAS = ["SUPPORT", "DUO", "SOLO", "JUNGLE", "MID"]
MESES = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
         "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12}


def leer_csv():
    out = {}
    with open(CSV, newline="", encoding="utf-8") as fh:
        for f in csv.DictReader(fh):
            out[(f["champion"], f["role"])] = f
    return out


def parse_fm(txt):
    m = re.match(r"^---\n(.*?)\n---\n", txt, re.S)
    return dict(re.findall(r"^(\w+):\s*(.*)$", m.group(1), re.M)) if m else {}


def fecha_csv(fila):
    m = re.match(r"(\d{2})\s+([A-Z]+)\s+(\d{4})", fila.get("actualizado") or fila.get("updated_utc") or "")
    return f"{m.group(1)}/{meses[m.group(2)]}/{m.group(3)}" if m else None


def refrescar_linea(linea, filas, rol_default):
    # fecha del callout (una sola por línea, con la fila del rol default o la primera)
    f0 = filas.get((rol_default)) or next(iter(filas.values()))
    fc = fecha_csv(f0)
    if fc:
        linea = re.sub(r"(Diamond\+,\s*)\d{2}/\d{2}/\d{4}", lambda m: f"{m.group(1)}{fc}", linea, count=1)
    partes = re.split(r"(?=(?:SUPPORT|DUO|SOLO|JUNGLE|MID)[\s·:]*)", linea)
    out = []
    for pt in partes:
        rol = next((e for e in ETIQUETAS if pt.lstrip().startswith(e)), rol_default)
        fila = filas.get(rol)
        if fila and "Win Rate" in pt:
            trend = fila["trend"].replace(" ", "")
            pt = re.sub(r"(Win Rate\s*)[\d.]+(\s*%)", lambda m: f"{m.group(1)}{fila['win_pct']}{m.group(2)}", pt)
            pt = re.sub(r"(Pick Rate\s*)[\d.]+(\s*%)", lambda m: f"{m.group(1)}{fila['pick_pct']}{m.group(2)}", pt)
            pt = re.sub(r"(Ban\s*)[\d.]+(\s*%)", lambda m: f"{m.group(1)}{fila['ban_pct']}{m.group(2)}", pt)
            pt = re.sub(r"(Tendencia\s*)([^\s|·]+)", lambda m: f"{m.group(1)}{trend}", pt)
        out.append(pt)
    return "".join(out)


def refrescar(txt, filas, rol_default):
    lineas = txt.split("\n")
    in_note = meta = False
    n = 0
    for i, l in enumerate(lineas):
        if l.startswith("> [!NOTE]"):
            in_note, meta = True, False
            continue
        if in_note:
            if not l.startswith(">"):
                in_note = False
                continue
            if "Estado Meta" in l:
                meta = True
            if meta and "Win Rate" in l:
                nueva = refrescar_linea(l, filas, rol_default)
                if nueva != l:
                    lineas[i] = nueva
                    n += 1
    return "\n".join(lineas), n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--solo", default=None)
    args = ap.parse_args()
    csv_all = leer_csv()
    for f in sorted(os.listdir(REPORTES)):
        if not f.endswith(".md") or (args.solo and f != args.solo):
            continue
        txt = open(os.path.join(REPORTES, f), encoding="utf-8").read()
        fm = parse_fm(txt)
        champ = (fm.get("champion") or os.path.splitext(f)[0]).strip("'")
        rol = ROL_CSV.get(fm.get("role", ""), "DUO")
        filas = {r: fila for (c, r), fila in csv_all.items() if c.lower() == champ.lower()}
        if not filas:
            print(f"=  {f}: sin fila CSV para {champ}")
            continue
        nuevo, n = refrescar(txt, filas, rol)
        if n:
            verbo = "✍️ " if args.apply else "→  "
            print(f"{verbo}{f}: {n} línea(s) de win rate refrescadas" + ("" if args.apply else " (dry-run)"))
            if args.apply:
                open(os.path.join(REPORTES, f), "w", encoding="utf-8").write(nuevo)
        else:
            print(f"=  {f}: callout ya al día (o sin callout meta)")


if __name__ == "__main__":
    main()
