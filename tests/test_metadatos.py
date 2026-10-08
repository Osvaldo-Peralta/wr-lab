# -*- coding: utf-8 -*-
"""WR-LAB · tests del estándar de metadatos v1.15 (estandarizar_metadatos.py + diccionario)."""
import os, re, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import estandarizar_metadatos as E
import update_reports as U

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REP = os.path.join(ROOT, "reportes")
REQUERIDAS = [k for k in E.CANON if k not in ("patch", "variant", "archetype")]


def archivos(pub=True):
    d = REP if pub else os.path.join(REP, "_auto")
    return [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith(".md")]


class TestEstandar(unittest.TestCase):
    def test_todos_los_publicados_canonicos(self):
        for ruta in archivos():
            txt = open(ruta, encoding="utf-8").read()
            fm = U.parse_frontmatter(txt)
            for k in REQUERIDAS:
                self.assertIn(k, fm, f"{os.path.basename(ruta)}: falta {k}")
            self.assertNotIn("rol", fm, f"{os.path.basename(ruta)}: 'rol' debe ser 'role'")
            self.assertIn(fm.get("generate"), ("manual", "auto"), ruta)
            self.assertIn(fm.get("mode"), ("sr", "aram"), ruta)

    def test_jinx_v15_normalizado(self):
        fm = U.parse_frontmatter(open(os.path.join(REP, "Jinx.md"), encoding="utf-8").read())
        self.assertEqual(fm["role"], "adc")
        self.assertEqual(fm["verification"], "AL_DIA")
        self.assertEqual(fm["verified_patch"], "7.3a")
        self.assertEqual(fm["generate"], "manual")
        self.assertEqual(fm["published_at"], "2026-10-04")
        self.assertEqual(fm["version"], "1.5")

    def test_idempotente(self):
        reg = U.cargar_registro().get("reportes", {})
        for ruta in archivos():
            f = os.path.basename(ruta)
            nuevo, notas = E.estandarizar(f, ruta, reg)
            actual = open(ruta, encoding="utf-8").read()
            self.assertEqual(nuevo, actual, f"{f} no canónico: {notas}")

    def test_auto_en_espera(self):
        # v1.15.2: el vault puede no embarcar reportes/_auto (derivados
        # regenerables; decisión del autor 08/10). Ausencia ≠ estándar roto.
        if not os.path.isdir(os.path.join(REP, "_auto")):
            self.skipTest("el vault no embarca reportes/_auto")
        for ruta in archivos(pub=False):
            fm = U.parse_frontmatter(open(ruta, encoding="utf-8").read())
            self.assertEqual(fm["Status"], "Espera de verificación", ruta)
            self.assertEqual(fm["generate"], "auto", ruta)
            self.assertEqual(fm["verification"], "pending", ruta)

    def test_diccionario_cubre_el_canon(self):
        d = open(os.path.join(ROOT, "deploy", "DICCIONARIO_METADATOS.md"), encoding="utf-8").read()
        for k in E.CANON:
            self.assertIn(f"`{k}`", d, f"el diccionario no documenta '{k}'")


if __name__ == "__main__":
    unittest.main(verbosity=2)
