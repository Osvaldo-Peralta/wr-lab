# -*- coding: utf-8 -*-
"""WR-LAB · tests de model/senna_model.py (batch3, recuperado del chat del autor
el 11/10/2026 e integrado en v1.16.1).

Ojo con el ORDEN de imports: optimize_build primero (congela sus pools
genéricos) y senna_model después (registra sus ítems SUP en M.ITEMS). El test
de no-contaminación verifica justo eso.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import optimize_build as OB  # noqa: F401  (import deliberado ANTES que senna_model)
import dps_model as M
import senna_model as SM

DUO_OPT = ["gunmetal", "runaan", "kraken", "terminus", "botrk", "ie"]
SUP_OPT = ["gunmetal", "scythe", "censer", "echoes", "cleaver", "er"]


class TestSennaModel(unittest.TestCase):
    def test_sup_no_contamina_pools_genericos(self):
        """Los ítems support de Senna no pueden colarse en optimize_build de
        otros campeones (filtro SENNA-SUP, incidente de diseño 11/10)."""
        for k in ("cleaver", "censer", "harmonic", "scythe", "echoes"):
            self.assertNotIn(k, OB.ENGINES["autos"]["items"])

    def test_eval_invariantes_duo(self):
        r = SM.eval_senna(DUO_OPT, mist=110, role="duo")
        self.assertGreater(r["dps1"], 1000)
        self.assertLessEqual(r["crit_eff"], 100)          # cap duro
        self.assertEqual(r["crit"], 100)                  # 50 ítems + 50 Niebla (110 stacks)
        self.assertEqual(r["pen"], 30)                    # Terminus, sin LDR/Mortal
        self.assertGreater(r["q_heal_hps"], 0)            # la Q cura siempre algo

    def test_eval_invariantes_support(self):
        r = SM.eval_senna(SUP_OPT, mist=140, role="support")
        self.assertGreater(r["q_heal_hps"], 40)           # valor-aliado real
        self.assertGreater(r["r_shield"], 400)            # escudo R con 140 de Niebla
        self.assertGreater(r["adc_dps_add"], 100)         # Censer con uptime pleno

    def test_builds_publicadas_legales(self):
        self.assertEqual(M.validate_slots(DUO_OPT), (1, 5))   # Ley 0
        self.assertEqual(M.validate_slots(SUP_OPT), (1, 5))   # quest en slot propio
        self.assertTrue(SM.legales(DUO_OPT))                  # Terminus solo en su grupo
        self.assertFalse(SM.legales(["gunmetal", "ldr", "terminus", "botrk", "ie", "runaan"]))  # Ley 3b

    def test_optimizar_support_top_consistente(self):
        fin, hojas, _ = SM.optimizar_senna("support", top=3, embudo=60)
        self.assertGreater(hojas, 1000)
        self.assertEqual(len(fin), 3)
        scores = [f[0] for f in fin]
        self.assertEqual(scores, sorted(scores, reverse=True))  # top ordenado
        for _, combo, _, _, base in fin:
            self.assertEqual(M.validate_slots(combo), (1, 5))   # toda hoja es legal


if __name__ == "__main__":
    unittest.main(verbosity=2)
