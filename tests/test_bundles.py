# -*- coding: utf-8 -*-
"""
WR-LAB · tests de los bundles portables (model/build_bundles.py).
Los bundles son ARTEFACTOS DERIVADOS: estos tests garantizan que los .md de la raíz
están sincronizados con las fuentes (si alguien edita una fuente y no regenera, CI falla).
Ejecutar:  python3 -m unittest discover -s tests -v
"""
import os, re, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import build_bundles as BB


def _norm(t):
    t = re.sub(r"\d{2}/\d{2}/\d{4}", "<FECHA>", t)
    return re.sub(r"sha256\(cuerpo\)=[0-9a-f]+", "sha=<X>", t)


class TestBundlesSincronizados(unittest.TestCase):
    def test_lite_al_dia(self):
        with open(os.path.join(BB.ROOT, "WR-LAB_lite.md"), encoding="utf-8") as fh:
            disco = fh.read()
        self.assertEqual(_norm(disco), _norm(BB.generar("LITE")),
                         "WR-LAB_lite.md desfasado — corre: python3 model/build_bundles.py")

    def test_completo_al_dia(self):
        with open(os.path.join(BB.ROOT, "WR-LAB_completo.md"), encoding="utf-8") as fh:
            disco = fh.read()
        self.assertEqual(_norm(disco), _norm(BB.generar("COMPLETO")),
                         "WR-LAB_completo.md desfasado — corre: python3 model/build_bundles.py")


class TestContenidoBundles(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lite = BB.generar("LITE")
        cls.completo = BB.generar("COMPLETO")

    def test_integridad_lite(self):
        problemas, n_as, n_items, _ = BB.validar(self.lite, "LITE")
        self.assertEqual(problemas, [])
        self.assertEqual(n_as, 140)                      # los 140 campeones del apéndice oficial
        self.assertEqual(n_items, 186)

    def test_integridad_completo(self):
        problemas, _, _, n_rep = BB.validar(self.completo, "COMPLETO")
        self.assertEqual(problemas, [])
        self.assertEqual(n_rep, len([f for f in os.listdir(os.path.join(BB.ROOT, "reportes")) if f.endswith(".md")]))

    def test_modulos_nuevos_embebidos(self):
        for modulo in ("model/optimize_build.py", "model/update_reports.py",
                       "model/analysis_batch2.py", "model/optimize_runes.py",
                       "model/sim_timings.py"):
            fuente = open(os.path.join(BB.ROOT, *modulo.split("/")), encoding="utf-8").read()
            self.assertIn(fuente[:1500], self.completo, f"{modulo} no embebido íntegro")
        # el lite trae el optimizador (herramienta de análisis) pero no la infraestructura
        self.assertIn("optimize_build", self.lite)
        self.assertNotIn("def cmd_baseline", self.lite)

    def test_reportes_con_verificacion_en_el_completo(self):
        m = re.search(r"^## 14\. REPORTES.*?(?=^## 15\.)", self.completo, re.S | re.M)
        self.assertIsNotNone(m, "sección §14 no encontrada")
        n = len(re.findall(r"WRLAB-VERIF:7\.3a:START", m.group(0)))
        # esperan bloque todos los reportes que NO declaran patch ≥ 7.3a (los AL_DIA no llevan)
        import sys as _sys
        _sys.path.insert(0, os.path.join(BB.ROOT, "model"))
        import update_reports as U
        esperan = 0
        for f in sorted(os.listdir(os.path.join(BB.ROOT, "reportes"))):
            if not f.endswith(".md"):
                continue
            with open(os.path.join(BB.ROOT, "reportes", f), encoding="utf-8") as fh:
                txt = fh.read()
            pd = U.parche_declarado(U.parse_frontmatter(txt), txt)
            if not (pd and U.patch_key(pd) >= U.patch_key("7.3a")):
                esperan += 1
        self.assertEqual(n, esperan)


if __name__ == "__main__":
    unittest.main(verbosity=2)
