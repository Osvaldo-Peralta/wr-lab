# -*- coding: utf-8 -*-
"""WR-LAB · tests de los motores batch4 de campeones (yunara/xayah/chogath_jungla).

Compatibilidad Wild Rift por construcción (todo key resuelve a un ítem de
items_7.3.csv), reproducción de cifras publicadas (Xayah ±2 %), leyes de
builds (crit exacto / pen mínima / Ley 3b) y las dos derivaciones que el
motor jungla debe sostener: clear/épicos mejores que la óptima de top, y
score jungla mayor para la óptima de jungla.
"""
import csv
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import dps_model as M  # noqa: F401  (resolve oficial; importar antes no contamina: estos motores son autocontenidos)
import yunara_model as Y
import xayah_model as X
import chogath_model as CG
import chogath_jungla as CJ

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YUN_OPT = ["gunmetal", "ie", "runaan", "ldr", "yuntal", "botrk"]
XAY_OPT = ["gunmetal", "ie", "runaan", "ldr", "yuntal", "botrk"]
JG_OPT = ("Chainlaced", ["Heartsteel", "Sunfire", "Liandry", "Riftmaker", "UnendingDespair"])
TOP_OPT = ("ArmoredAdvance", ["Heartsteel", "ForceOfNature", "Gargoyle", "UnendingDespair", "Twinguard"])


class TestCompatWR(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(ROOT, "data", "estructurada", "items_7.3.csv"), newline="", encoding="utf-8") as fh:
            cls.oficiales = {r["item"].lower() for r in csv.DictReader(fh)}

    def _checa(self, mod):
        for k in list(mod.ITEMS) + list(mod.BOOTS):
            nombre = M.resolve(k)
            cand = {k.lower(), nombre.key.lower()}
            cand |= {a.lower() for a, v in M.ALIAS.items() if v == nombre.key}
            self.assertTrue(cand & self.oficiales, f"{k} no mapea a ningún ítem de WR 7.3")

    def test_yunara_pool_wr(self):
        self._checa(Y)

    def test_xayah_pool_wr(self):
        self._checa(X)


class TestXayah(unittest.TestCase):
    def test_reproduce_publicada(self):
        t = X.totals(XAY_OPT, scenario="1v1")["total"]
        self.assertAlmostEqual(t, 3146, delta=63)   # ±2 %

    def test_leyes_en_optima(self):
        crit = sum(X.ITEMS[k]["crit"] for k in XAY_OPT)
        pen = sum(X.ITEMS[k]["pen"] for k in XAY_OPT)
        self.assertEqual(crit, 100)                # Ley 1 exacta
        self.assertGreaterEqual(pen, 30)           # Ley 3
        self.assertLessEqual(sum(1 for k in XAY_OPT if X.ITEMS[k].get("pen_pct_group")), 1)  # 3b


class TestYunara(unittest.TestCase):
    def test_optima_leyes(self):
        crit = sum(Y.ITEMS[k]["crit"] for k in YUN_OPT)
        self.assertEqual(crit, 100)
        self.assertGreaterEqual(sum(Y.ITEMS[k]["pen"] for k in YUN_OPT), 30)

    def test_botrk_gana_supervivencia_a_kraken(self):
        b = Y.metrics(["gunmetal", "ie", "runaan", "ldr", "yuntal", "botrk"])
        k = Y.metrics(["gunmetal", "ie", "runaan", "ldr", "yuntal", "kraken"])
        self.assertGreater(b["surv"], k["surv"])
        self.assertGreater(b["heal"], k["heal"])

    def test_c44_primero_revertido(self):
        """Checkpoint lvl 9: BotRK 1.º mide más que C44 1.º (veredicto v1.2 revertido)."""
        botrk = Y.metrics(["berserker", "botrk"], level=9)["1v1"]
        c44 = Y.metrics(["berserker", "c44"], level=9)["1v1"]
        self.assertGreater(botrk, c44)


class TestChogathJungla(unittest.TestCase):
    def test_jungla_optima_clear_y_epicos_mejor_que_top(self):
        j = CJ.jg_metrics(*JG_OPT)
        t = CJ.jg_metrics(*TOP_OPT)
        self.assertLess(j["t_clear"], t["t_clear"])      # segundos: jungla óptima cleara antes
        self.assertLess(j["ttk_dragon"], t["ttk_dragon"])  # y toma dragón antes
        self.assertGreater(j["dps_fighter"], t["dps_fighter"])

    def test_score_jungla_prefiere_la_derivation_jungla(self):
        j = CJ.jg_metrics(*JG_OPT)
        t = CJ.jg_metrics(*TOP_OPT)
        mx = {k: max(j[k], t[k]) for k in CJ.PESOS_JG}
        self.assertGreater(CG.composite(j, mx, CJ.PESOS_JG), CG.composite(t, mx, CJ.PESOS_JG))

    def test_clear_con_immolate_mejor_que_sin(self):
        con = CJ.jg_metrics("Chainlaced", ["Sunfire", "Liandry", "Riftmaker", "UnendingDespair", "Heartsteel"])
        sin = CJ.jg_metrics("Chainlaced", ["ForceOfNature", "Liandry", "Riftmaker", "UnendingDespair", "Heartsteel"])
        self.assertLess(con["t_clear"], sin["t_clear"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
