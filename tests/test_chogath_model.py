# -*- coding: utf-8 -*-
"""WR-LAB · tests de model/chogath_model.py (batch4, motor rotación-tanque).

Cubre: compatibilidad Wild Rift de TODO el pool (items_7.3.csv), exclusividad
Immolate (A10/Ley 3b extendida), controles de Ley 4, robustez de la óptima
(cuarteto Unending+Gargoyle+Twinguard+FoN) y coherencia de la curva de stacks.
"""
import csv
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import chogath_model as C

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPT = ("ArmoredAdvance", ["Heartsteel", "ForceOfNature", "Gargoyle", "UnendingDespair", "Twinguard"])


class TestCompatWR(unittest.TestCase):
    def test_pool_completo_existe_en_items_73(self):
        """Indicación del autor: nada de ítems de desktop. Todo key del motor
        debe mapear a un nombre QUE EXISTA en items_7.3.csv."""
        with open(os.path.join(ROOT, "data", "estructurada", "items_7.3.csv"), newline="", encoding="utf-8") as fh:
            oficiales = {r["item"].lower() for r in csv.DictReader(fh)}
        for key, nombre in C.NOMBRES_OFICIALES.items():
            self.assertIn(key, {**C.ITEMS, **C.BOOTS, **C.BOOTS_T2}, f"key huérfana: {key}")
            self.assertIn(nombre.lower(), oficiales, f"{nombre} ({key}) no existe en WR 7.3")
        for key in list(C.ITEMS) + list(C.BOOTS) + list(C.BOOTS_T2):
            self.assertIn(key, C.NOMBRES_OFICIALES, f"key sin nombre oficial: {key}")


class TestInvariantes(unittest.TestCase):
    def test_exclusividad_immolate(self):
        self.assertFalse(C.exclusivo_ok(["Sunfire", "HollowRadiance"]))
        self.assertTrue(C.exclusivo_ok(["Sunfire", "Heartsteel"]))

    def test_eval_optima_coherente(self):
        r = C.evaluate(OPT[0], OPT[1])
        self.assertGreater(r["maxHP"], 7000)
        self.assertGreater(r["ehp_window"], r["maxHP"] * 3)     # la ventana multiplica al HP
        self.assertLessEqual(r["size"], 2.35 + 1e-9)             # cap de tamaño Feast + Twinguard
        self.assertGreater(r["r_exec"], 1000)
        self.assertGreater(r["hps"], 100)                        # Anguish + Grasp

    def test_tamano_es_consecuencia_no_objetivo(self):
        """Indicación del autor: gigante derretible NO es óptimo. El tanque puro
        (más HP) debe perder VENT y score contra la óptima balanceada."""
        puro = C.evaluate("ArmoredAdvance", ["Heartsteel", "Twinguard", "Gargoyle", "Warmog", "Randuin"])
        opt = C.evaluate(OPT[0], OPT[1])
        self.assertGreater(puro["maxHP"], opt["maxHP"])
        self.assertGreater(opt["ehp_window"], puro["ehp_window"])
        self.assertGreater(opt["dps_fighter"], puro["dps_fighter"])

    def test_ley4_controles_ad_peores(self):
        base = list(OPT[1])
        r_opt = C.evaluate(OPT[0], base)
        for ctrl in ("Sterak", "OverlordBlood", "BlackCleaver"):
            cb = base[:4] + [ctrl]
            r = C.evaluate(OPT[0], cb)
            mx = {k: max(r_opt[k], r[k]) for k in C.PESOS}
            self.assertGreater(
                C.composite(r_opt, mx), C.composite(r, mx),
                f"Ley 4: {ctrl} no perdió contra la óptima")

    def test_curva_stacks_monotona(self):
        hps = [C.evaluate(OPT[0], OPT[1], S=s)["maxHP"] for s in (0, 6, 15, 22)]
        self.assertEqual(hps, sorted(hps))
        self.assertGreater(hps[-1] - hps[0], 2000)   # Feast es el escalado real


class TestOptimize(unittest.TestCase):
    def test_optimize_pool_reducido_devuelve_legales(self):
        pool = ["Heartsteel", "UnendingDespair", "Twinguard", "Gargoyle", "ForceOfNature",
                "Warmog", "Randuin", "KaicRookern", "Sunfire"]
        top, mx, n = C.optimize(pool, ["ArmoredAdvance", "Chainlaced"], oro=17250, top=4)
        self.assertGreater(n, 50)
        self.assertEqual(len(top), 4)
        for sc, bk, cb, r in top:
            self.assertEqual(len(cb), 5)                       # Ley 0: 1 bota + 5
            self.assertTrue(C.exclusivo_ok(cb))
            self.assertLessEqual(r["gold"], 17250)
        scores = [t[0] for t in top]
        self.assertEqual(scores, sorted(scores, reverse=True))


if __name__ == "__main__":
    unittest.main(verbosity=2)
