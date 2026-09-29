# -*- coding: utf-8 -*-
"""
WR-LAB · tests del optimizador de builds (model/optimize_build.py).
Validación cruzada exigida por el ROADMAP: dentro del pool de candidatos del reporte
de Jinx y con las Leyes 1 y 3 como restricciones, el optimizador debe REDISCUBRIR
la build C publicada (Gunmetal+C44+Runaan's+IE+LDR+Kraken).
Ejecutar:  python3 -m unittest discover -s tests -v
"""
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import optimize_build as O
import dps_model as M

JINX_C = ["Gunmetal", "C44", "Runaan's", "IE", "LDR", "Kraken"]
POOL_REPORTE = ["Gunmetal", "Berserker's", "C44", "Runaan's", "IE", "LDR", "Kraken",
                "BT", "Galeforce", "Scimitar", "RFC"]


class TestValidacionCruzada(unittest.TestCase):
    def test_redescubre_jinx_C(self):
        """ROADMAP: 'debe redescubrir la build C de Jinx' (pool del reporte + Leyes 1 y 3)."""
        finales, hojas = O.optimizar("jinx", oro=18000, top=3, crit_min=100, pen_min=30,
                                     incluir=POOL_REPORTE, verbose=False)
        self.assertGreater(hojas, 0)
        top1 = finales[0][1]
        self.assertEqual(sorted(M.resolve(x).key for x in top1),
                         sorted(M.resolve(x).key for x in JINX_C))
        base = finales[0][3]
        self.assertEqual(round(base["dps1"]), 3042)      # golden number del reporte
        self.assertEqual(base["gold"], 17350)

    def test_ley0_estructural(self):
        """Toda build devuelta pasa validate_slots (1 botas T3 + 5 ítems)."""
        finales, _ = O.optimizar("jinx", oro=18000, top=5, incluir=POOL_REPORTE, verbose=False)
        for score, combo, det, base in finales:
            self.assertEqual(M.validate_slots(combo), (1, 5))
            self.assertLessEqual(base["gold"], 18000)

    def test_restricciones_de_ley_duras(self):
        """--crit-min/--pen-min se respetan en TODAS las builds devueltas."""
        finales, _ = O.optimizar("jinx", oro=18000, top=5, crit_min=100, pen_min=30,
                                 verbose=False)
        for score, combo, det, base in finales:
            self.assertGreaterEqual(base["crit"], 100)
            self.assertGreaterEqual(base["pen"], 30)

    def test_pool_completo_no_peor_que_publicada(self):
        """Con el pool completo post-7.3a, el óptimo no pierde contra la build publicada
        (documenta que el buff de Yun Tal expandió la frontera óptima)."""
        finales, hojas = O.optimizar("jinx", oro=18000, top=5, crit_min=100, pen_min=30,
                                     verbose=False)
        self.assertGreater(hojas, 20000)                 # búsqueda realmente exhaustiva
        mejor = finales[0]
        # eficiencia normalizada del top-1 ≥ la de la publicada bajo la misma normalización
        max_e = {e: max(d[e] for _, _, d, _ in finales) for e in O.ESCENARIOS}
        det_c = {e: M.eval_build(M.CHAMPS["jinx"], JINX_C, validate=False, **kw)[met]
                 for e, (kw, met) in O.ESCENARIOS.items()}
        eff_c = sum(O.PESOS_DEFAULT[e] * det_c[e] / max(max_e[e], det_c[e]) for e in O.ESCENARIOS)
        self.assertGreaterEqual(mejor[0] + 1e-9, eff_c)


if __name__ == "__main__":
    unittest.main(verbosity=2)
