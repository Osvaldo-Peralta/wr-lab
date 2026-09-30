# -*- coding: utf-8 -*-
"""WR-LAB · tests del buscador de runas (model/optimize_runes.py).
Validación: reproduce las conclusiones de runas de los reportes (Jinx LT×Alacrity, Diana LT)."""
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import optimize_runes as R

JINX_C = ["Gunmetal", "C44", "Runaan's", "IE", "LDR", "Kraken"]
DIANA_D2 = ["Spellslinger", "DuskDawn", "Nashor", "Rabadon", "Zhonyas", "Cryptbloom"]


class TestRunasAutos(unittest.TestCase):
    def test_jinx_lt_alacrity_gana(self):
        """El reporte de Jinx concluyó LT + Alacrity: el grid completo debe confirmarlo."""
        grid, base = R.buscar_autos("jinx", JINX_C, top=24)
        self.assertEqual(grid[0]["ks"], "Lethal Tempo")
        self.assertEqual(grid[0]["sec"], "Legend: Alacrity")
        self.assertAlmostEqual(grid[0]["marginal"], 0.0, places=5)

    def test_conqueror_supera_a_first_strike_en_sostenido(self):
        """+25.5 AD efectivos pesan más que +0.84 % de amp en pelea de 10 s."""
        d_conq, _ = R.eval_par_autos(__import__("dps_model").CHAMPS["jinx"], JINX_C,
                                     "Conqueror", "Triumph", {}, "dps1")
        d_fs, _ = R.eval_par_autos(__import__("dps_model").CHAMPS["jinx"], JINX_C,
                                   "First Strike", "Triumph", {}, "dps1")
        self.assertGreater(d_conq, d_fs)

    def test_cut_down_solo_brilla_vs_tanque(self):
        spec = __import__("dps_model").CHAMPS["jinx"]
        d_tank_cd, _ = R.eval_par_autos(spec, JINX_C, "Lethal Tempo", "Cut Down",
                                        dict(armor=220, tank=True, enemy_hp=4500), "dps1")
        d_tank_al, _ = R.eval_par_autos(spec, JINX_C, "Lethal Tempo", "Legend: Alacrity",
                                        dict(armor=220, tank=True, enemy_hp=4500), "dps1")
        d_1v1_cd, _ = R.eval_par_autos(spec, JINX_C, "Lethal Tempo", "Cut Down", {}, "dps1")
        d_1v1_al, _ = R.eval_par_autos(spec, JINX_C, "Lethal Tempo", "Legend: Alacrity", {}, "dps1")
        margen_tanque = d_tank_cd / d_tank_al - 1
        margen_1v1 = d_1v1_cd / d_1v1_al - 1
        self.assertLess(margen_1v1, margen_tanque)      # Cut Down rinde más vs tanques

    def test_excluidas_documentadas(self):
        self.assertIn("Brutal", R.EXCLUIDAS)            # gate de calidad de datos
        self.assertGreaterEqual(len(R.EXCLUIDAS), 5)


class TestRunasRotacion(unittest.TestCase):
    def test_diana_lt_gana(self):
        """Reporte de Diana: LT supera a Empowerment (+30 % DPS sostenido)."""
        grid, base = R.buscar_rotacion("diana", DIANA_D2, top=6)
        self.assertEqual(grid[0]["ks"], "Lethal Tempo")
        emp = next(g for g in grid if g["ks"] == "Empowerment")
        self.assertGreater(grid[0]["det"]["dps10s"] / emp["det"]["dps10s"], 1.05)


if __name__ == "__main__":
    unittest.main(verbosity=2)
