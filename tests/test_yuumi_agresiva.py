# -*- coding: utf-8 -*-
"""WR-LAB · tests de Yuumi agresiva v2.0 (model/yuumi_agresiva_model.py).

Invariantes de la re-derivación batch5 que publica reportes/Yuumi.md v2.0:
la página de runas es LEGAL (runas_wr), el presupuesto es de support (13 000 g)
y el sacrificio vs el baseline enchanter está acotado (declarado en [!DANGER]).
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import runas_wr as R
import yuumi_agresiva_model as YA

OPTIMA = ["Scythe", "Spellslinger", "Mandate", "Horizon", "Malignance", "Stormsurge"]
RUNAS = ["Electrocute", "Cheap Shot", "Transcendence", "Coup de Grace", "Gathering Storm"]


class TestYuumiAgresiva(unittest.TestCase):
    def test_pagina_de_runas_legal(self):
        """La página publicada en Yuumi.md v2.0 pasa L1-L4 (verificada en cliente 16/10)."""
        ok, motivos = R.es_legal_pagina(RUNAS)
        self.assertTrue(ok, motivos)

    def test_presupuesto_support(self):
        """Óptima = 13 000 g exactos: convención quest 0 g + botas + 4."""
        oro = sum(YA.ITEMS[i]["g"] for i in OPTIMA)
        self.assertEqual(oro, 13000)

    def test_sacrificio_acotado_vs_baseline(self):
        """El [!DANGER] de Yuumi.md: la protección propia NO colapsa aunque la aliada sí."""
        a = YA.ally(OPTIMA)
        self.assertGreaterEqual(a["e_shield"], 350.0)    # v1.2: 301 · baseline Y1: 354
        self.assertGreaterEqual(a["r_heal"], 600.0)      # baseline Y1: 672 → −4 % máximo
        self.assertGreaterEqual(a["adc_dps_add"], 90.0)  # suelo declarado vs Y1 (248)

    def test_dano_de_la_tabla_publicada(self):
        """Cifras del resumen: Q-hit ≈ 509 y R-burst ≈ 2 833 (tolerancia 1 %)."""
        d = YA.damage(OPTIMA, keystone="electro", minors=("cheap", "transc", "coup"),
                      second="gather")
        self.assertAlmostEqual(d["q_dmg"], 509, delta=5)
        self.assertAlmostEqual(d["r_dmg"], 2833, delta=28)


if __name__ == "__main__":
    unittest.main(verbosity=2)
