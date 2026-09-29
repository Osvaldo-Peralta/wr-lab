# -*- coding: utf-8 -*-
"""
WR-LAB · tests del optimizador de builds (model/optimize_build.py, v2: 4 motores).

Protocolo de validación cruzada (dos niveles, honesto con las limitaciones del modelo):
  NIVEL 1 — candidates del reporte: la build publicada debe ganar ENTRE las candidatas
            que el propio reporte comparó (§8): Jinx C (búsqueda), Diana D2-LT, Yuumi Y1.
  NIVEL 2 — exploración completa: el optimizador puede superar al reporte (hallazgos:
            Yun Tal post-7.3a para Jinx, híbrido Statikk para Kalista, glass-cannon AP
            para Diana/Yuumi). Los modelos no puntúan defensa ni pasivas no modeladas
            (Zhonyas stasis, Echoes siphon, Redemption activo) → los hallazgos se
            DOCUMENTAN (ROADMAP §Hallazgos), no se auto-aplican a reportes publicados.
Ejecutar:  python3 -m unittest discover -s tests -v
"""
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import optimize_build as O
import dps_model as M

JINX_C = ["Gunmetal", "C44", "Runaan's", "IE", "LDR", "Kraken"]
POOL_JINX_REPORTE = ["Gunmetal", "Berserker's", "C44", "Runaan's", "IE", "LDR", "Kraken",
                     "BT", "Galeforce", "Scimitar", "RFC"]
KALISTA_K2 = ["Gunmetal", "Guinsoo", "WitsEnd", "Terminus", "BotRK", "Runaan"]
DIANA_CANDIDATAS = {          # §8 del reporte de Diana (keystone LT)
    "D1": ["Spellslinger", "DuskDawn", "InfinityOrb", "Zhonyas", "Rabadon", "Luden"],
    "D2": ["Spellslinger", "DuskDawn", "Nashor", "Rabadon", "Zhonyas", "Cryptbloom"],
    "D3": ["Spellslinger", "Luden", "Rabadon", "InfinityOrb", "Stormsurge", "Zhonyas"],
    "D4": ["Spellslinger", "DuskDawn", "Rabadon", "VoidStaff", "Zhonyas", "Cryptbloom"],
}
YUUMI_CANDIDATAS = {          # §8 del reporte de Yuumi (Y1-Y5)
    "Y1": ["Scythe", "Crimson", "Censer", "Echoes", "Staff", "Redemption"],
    "Y2": ["Scythe", "Crimson", "Echoes", "Staff", "Diadem", "Redemption"],
    "Y3": ["Scythe", "Crimson", "Mikael", "Locket", "Censer", "Echoes"],
    "Y4": ["Scythe", "Crimson", "Censer", "Staff", "Echoes", "Shurelya"],
    "Y5": ["Scythe", "Crimson", "Zeke", "Censer", "Echoes", "Staff"],
}


def puntuar_normalizado(champ, motor, candidatas, keystone="lt"):
    """Score del optimizador (ponderado normalizado) para una lista fija de builds."""
    eng = O.ENGINES[motor]
    pesos = eng["pesos"]
    dets = {}
    for nombre, build in candidatas.items():
        dets[nombre] = {e: eng["eval_fn"](champ, build, kw, {"keystone": keystone})[m]
                        for e, (kw, m) in eng["escenarios"].items()}
    max_e = {e: max(d[e] for d in dets.values()) for e in eng["escenarios"]}
    return {n: sum(pesos[e] * (d[e] / max_e[e]) for e in eng["escenarios"])
            for n, d in dets.items()}


class TestJinxAutos(unittest.TestCase):
    def test_redescubre_C_en_pool_del_reporte(self):
        """NIVEL 1 (búsqueda): pool del reporte + Leyes 1/3 duras → top-1 == build C."""
        finales, hojas = O.optimizar("jinx", oro=18000, top=3, crit_min=100, pen_min=30,
                                     incluir=POOL_JINX_REPORTE, verbose=False)
        self.assertGreater(hojas, 0)
        self.assertEqual(sorted(M.resolve(x).key for x in finales[0][1]),
                         sorted(M.resolve(x).key for x in JINX_C))
        self.assertEqual(round(finales[0][3]["dps1"]), 3042)

    def test_ley0_y_presupuesto(self):
        finales, _ = O.optimizar("jinx", oro=18000, top=5, incluir=POOL_JINX_REPORTE, verbose=False)
        for score, combo, det, base in finales:
            self.assertEqual(M.validate_slots(combo), (1, 5))
            self.assertLessEqual(base["gold"], 18000)

    def test_restricciones_de_ley_duras(self):
        finales, _ = O.optimizar("jinx", oro=18000, top=5, crit_min=100, pen_min=30, verbose=False)
        for score, combo, det, base in finales:
            self.assertGreaterEqual(base["crit"], 100)
            self.assertGreaterEqual(base["pen"], 30)

    def test_pool_completo_no_peor_que_publicada(self):
        """NIVEL 2: post-7.3a la frontera óptima se expande (Yun Tal buffeada); el óptimo
        del pool completo no pierde contra la publicada en eficiencia normalizada."""
        finales, hojas = O.optimizar("jinx", oro=18000, top=5, crit_min=100, pen_min=30,
                                     verbose=False)
        self.assertGreater(hojas, 20000)
        det_c = {e: M.eval_build(M.CHAMPS["jinx"], JINX_C, validate=False, **kw)[m]
                 for e, (kw, m) in O.ESC_AUTOS.items()}
        max_e = {e: max([det_c[e]] + [d[e] for _, _, d, _ in finales]) for e in O.ESC_AUTOS}
        eff_c = sum(O.PESOS_AUTOS[e] * det_c[e] / max_e[e] for e in O.ESC_AUTOS)
        self.assertGreaterEqual(finales[0][0] + 1e-9, eff_c)


class TestKalistaOnHit(unittest.TestCase):
    def test_K2_en_top3_con_margen_minimo(self):
        """NIVEL 2: el híbrido Statikk supera a K2 por <1.5 % (ruido del modelo: el valor
        defensivo de Wit's End — MR/tenacidad — no está en la fórmula)."""
        finales, hojas = O.optimizar("kalista", top=6, verbose=False)
        combos = [sorted(c) for _, c, _, _ in finales]
        self.assertIn(sorted(KALISTA_K2), combos)
        rank = combos.index(sorted(KALISTA_K2)) + 1
        self.assertLessEqual(rank, 3)
        self.assertLess(finales[0][0] - finales[rank - 1][0], 0.015)

    def test_IE_excluido_por_modelo(self):
        """batch2.kalista no modela críticos → IE fuera del pool (conservador)."""
        finales, _ = O.optimizar("kalista", top=10, verbose=False)
        for _, combo, _, _ in finales:
            self.assertNotIn("IE", combo)


class TestDianaRotacion(unittest.TestCase):
    def test_D2_gana_entre_las_candidatas_del_reporte(self):
        """NIVEL 1: con los pesos del motor, D2-LT es la mejor de D1-D4 (§8 del reporte)."""
        scores = puntuar_normalizado("diana", "rotacion", DIANA_CANDIDATAS)
        self.assertEqual(max(scores, key=scores.get), "D2")
        for otra in ("D1", "D3", "D4"):
            self.assertGreater(scores["D2"], scores[otra])

    def test_busqueda_estructural(self):
        finales, hojas = O.optimizar("diana", top=3, verbose=False)
        self.assertGreater(hojas, 100)
        for _, combo, det, base in finales:
            self.assertEqual(len(combo), 6)
            self.assertIn(combo[0], ("Spellslinger", "Crimson"))   # 1 botas (Ley 0)


class TestYuumiAliado(unittest.TestCase):
    def test_Y1_gana_entre_las_candidatas_del_reporte(self):
        """NIVEL 1: Y1 (Censer/Echoes/Staff/Redemption) es la mejor de Y1-Y5 (§8)."""
        scores = puntuar_normalizado("yuumi", "aliado", YUUMI_CANDIDATAS)
        self.assertEqual(max(scores, key=scores.get), "Y1")

    def test_slots_fijos_de_support(self):
        """Motor aliado: quest (Scythe) fija + botas Crimson + 4 elegibles = 6 slots."""
        finales, hojas = O.optimizar("yuumi", top=5, verbose=False)
        self.assertGreater(hojas, 0)
        for _, combo, _, _ in finales:
            self.assertEqual(len(combo), 6)
            self.assertIn("Crimson", combo)
            self.assertIn("Scythe", combo)


if __name__ == "__main__":
    unittest.main(verbosity=2)
