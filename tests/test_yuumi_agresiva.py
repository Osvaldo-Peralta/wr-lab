# -*- coding: utf-8 -*-
"""WR-LAB · tests de Yuumi agresiva v2.1 (model/yuumi_agresiva_model.py).

Invariantes de la re-derivación batch5 + corrección de runas 18/10 que publica
reportes/Yuumi.md v2.1: la página de runas es la PUBLICADA por el autor (Aery +
Manaflow Band + Transcendence + Scorch | Revitalize) y es LEGAL (runas_wr v1.21,
L1-L4); el set batch5 v1.20 (Electrocute mixto) queda ILEGAL; el presupuesto es
de support (13 000 g) y el sacrificio vs el baseline enchanter está acotado
(declarado en [!DANGER]).
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import runas_wr as R
import yuumi_agresiva_model as YA

OPTIMA = ["Scythe", "Spellslinger", "Mandate", "Horizon", "Malignance", "Stormsurge"]
RUNAS = ["Aery", "Manaflow Band", "Transcendence", "Scorch", "Revitalize"]
RUNAS_BATCH5_V120 = ["Electrocute", "Cheap Shot", "Transcendence", "Coup de Grace", "Gathering Storm"]


class TestYuumiAgresiva(unittest.TestCase):
    def test_pagina_de_runas_legal(self):
        """La página publicada en Yuumi.md v2.1 pasa L1-L4 (verificada in-game por el autor)."""
        ok, motivos = R.es_legal_pagina(RUNAS)
        self.assertTrue(ok, motivos)

    def test_set_batch5_v120_ilegal(self):
        """Regresión: la DB v1.20 daba legal este set; con las reglas corregidas no lo es."""
        ok, motivos = R.es_legal_pagina(RUNAS_BATCH5_V120)
        self.assertFalse(ok)
        self.assertTrue(any("L2" in m for m in motivos), motivos)

    def test_presupuesto_support(self):
        """Óptima = 13 000 g exactos: convención quest 0 g + botas + 4."""
        oro = sum(YA.ITEMS[i]["g"] for i in OPTIMA)
        self.assertEqual(oro, 13000)

    def test_sacrificio_acotado_vs_baseline(self):
        """El [!DANGER] de Yuumi.md: la protección propia NO colapsa aunque la aliada sí."""
        a = YA.ally(OPTIMA)  # defaults = página publicada (Aery | Revitalize)
        self.assertGreaterEqual(a["e_shield"], 350.0)    # v2.1: 367 · baseline Y1: 354
        self.assertGreaterEqual(a["r_heal"], 600.0)      # v2.1: 662 · baseline Y1: 672 → −2 %
        self.assertGreaterEqual(a["adc_dps_add"], 90.0)  # suelo declarado vs Y1 (248)

    def test_dano_de_la_tabla_publicada(self):
        """Cifras del resumen v2.1: Q-hit ≈ 501 y R-burst ≈ 2 785 (tolerancia 1 %)."""
        d = YA.damage(OPTIMA)  # defaults = keystone Aery, minors manaflow/transc/scorch, sec. Revitalize
        self.assertAlmostEqual(d["q_dmg"], 501, delta=5)
        self.assertAlmostEqual(d["r_dmg"], 2785, delta=28)

    def test_optima_sigue_siendo_la_misma(self):
        """La corrección de runas NO cambia la build óptima (el search es de ítems)."""
        scored, _ = YA.optimize(YA.PESOS_AGRESIVA, top=1, label="test")
        self.assertEqual(list(scored[0][1]), OPTIMA)


if __name__ == "__main__":
    unittest.main(verbosity=2)
