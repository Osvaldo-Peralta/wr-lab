# -*- coding: utf-8 -*-
"""
WR-LAB · tests — suite de regresión del modelo (unittest, sin dependencias).
Ejecutar:  python3 -m unittest discover -s tests -v     (desde la raíz del lab)
"""
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import dps_model as M

class TestAttackSpeedFormula(unittest.TestCase):
    def test_caitlyn_oficial_pre73a(self):
        """Ejemplo oficial de las notas 7.3: Caitlyn lvl15 + Alacrity 18% + Berserker's = 1.48125."""
        c = M.ChampSpec(name="Caitlyn", base_ad=60, ad_growth=4.2, base_as=0.625,
                        as_ratio=0.625, base_bonus_as=0.28, as_per_lvl=0.04)
        B = c.base_bonus_as + M.lvl_as_bonus(c, 15) + 0.18 + 0.35
        self.assertAlmostEqual(c.base_as + c.as_ratio * B, 1.48125, places=5)

    def test_caitlyn_post73a(self):
        """7.3a bajó su growth a 0.025 → esperado 1.35 en las mismas condiciones."""
        c = M.ChampSpec(name="Caitlyn", base_ad=60, ad_growth=4.2, base_as=0.625,
                        as_ratio=0.625, base_bonus_as=0.28, as_per_lvl=0.025)
        B = c.base_bonus_as + M.lvl_as_bonus(c, 15) + 0.18 + 0.35
        self.assertAlmostEqual(c.base_as + c.as_ratio * B, 1.35, places=4)

    def test_as_cap(self):
        """El tope 3.0 se aplica y Get Excited se reporta por separado."""
        j = M.CHAMPS["jinx"]
        _, raw, _ = M.as_total(j, ["Gunmetal", "Runaan's", "RFC", "Kraken"])
        self.assertGreater(raw, M.AS_CAP)

class TestValidateSlots(unittest.TestCase):
    def test_build_valida(self):
        self.assertEqual(M.validate_slots(["Gunmetal","C44","Runaan's","IE","LDR","Kraken"]), (1, 5))

    def test_bug_doble_botas(self):
        """El bug histórico: Berserker's + Gunmetal como ítems separados."""
        with self.assertRaises(ValueError):
            M.validate_slots(["Statikk Shiv","Berserker's","Gunmetal","Guinsoo","BotRK","Terminus"])

    def test_siete_slots(self):
        with self.assertRaises(ValueError):
            M.validate_slots(["Berserker's","Gunmetal","C44","Runaan's","IE","LDR","Kraken"])

    def test_final_sin_botas(self):
        with self.assertRaises(ValueError):
            M.validate_slots(["C44","Runaan's","IE","LDR","Kraken","BT"])

    def test_checkpoint_parcial_ok(self):
        M.validate_slots(["Berserker's","C44","Runaan's"], final=False)  # no debe lanzar

class TestGoldenNumbers(unittest.TestCase):
    """Números canónicos del reporte de Jinx (no deben driftar sin razón documentada)."""
    def test_jinx_build_C(self):
        r = M.eval_build(M.CHAMPS["jinx"], ["Gunmetal","C44","Runaan's","IE","LDR","Kraken"])
        self.assertEqual(round(r["dps1"]), 3042)
        self.assertEqual(round(r["crit"]), 100)
        self.assertAlmostEqual(r["AS"], 2.83, places=2)

    def test_jinx_build_usuario(self):
        r = M.eval_build(M.CHAMPS["jinx"], ["Berserker's","Kraken","RFC","Runaan's","IE","BT"])
        self.assertEqual(round(r["dps1"]), 2556)

    def test_73a_yuntal_buff_aplicado(self):
        self.assertEqual(M.ITEMS["yuntal"].a_s, 35)   # 7.3a: 25 → 35

    def test_73a_deathsdance_coste(self):
        self.assertEqual(M.ITEMS["deathsdance"].gold, 3300)  # 7.3a: 3200 → 3300

class TestSpecs(unittest.TestCase):
    def test_roster_completo(self):
        esperados = {"jinx","kalista","diana","yuumi","karma","yunara","volibear","shyvana",
                     "chogath","mordekaiser","seraphine","heimerdinger","malphite"}
        self.assertTrue(esperados <= set(M.CHAMPS.keys()))

    def test_kalista_as_oficial(self):
        k = M.CHAMPS["kalista"]
        self.assertAlmostEqual(k.as_per_lvl, 0.046)
        self.assertAlmostEqual(k.base_ad + k.ad_growth*14, 129.8, places=1)

if __name__ == "__main__":
    unittest.main(verbosity=2)
