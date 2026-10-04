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
        for f in finales:
            self.assertEqual(M.validate_slots(f[1]), (1, 5))
            self.assertLessEqual(f[3]["gold"], 18000)

    def test_restricciones_de_ley_duras(self):
        finales, _ = O.optimizar("jinx", oro=18000, top=5, crit_min=100, pen_min=30, verbose=False)
        for f in finales:
            self.assertGreaterEqual(f[3]["crit"], 100)
            self.assertGreaterEqual(f[3]["pen"], 30)

    def test_pool_completo_no_peor_que_publicada(self):
        """NIVEL 2: post-7.3a la frontera óptima se expande (Yun Tal buffeada); el óptimo
        del pool completo no pierde contra la publicada en eficiencia normalizada."""
        finales, hojas = O.optimizar("jinx", oro=18000, top=5, crit_min=100, pen_min=30,
                                     verbose=False)
        self.assertGreater(hojas, 20000)
        det_c = {e: M.eval_build(M.CHAMPS["jinx"], JINX_C, validate=False, **kw)[m]
                 for e, (kw, m) in O.ESC_AUTOS.items()}
        max_e = {e: max([det_c[e]] + [f[2][e] for f in finales]) for e in O.ESC_AUTOS}
        eff_c = sum(O.PESOS_AUTOS[e] * det_c[e] / max_e[e] for e in O.ESC_AUTOS)
        self.assertGreaterEqual(finales[0][0] + 1e-9, eff_c)


class TestKalistaOnHit(unittest.TestCase):
    def test_K2_en_top3_con_margen_minimo(self):
        """NIVEL 2: el híbrido Statikk supera a K2 por <1.5 % (ruido del modelo: el valor
        defensivo de Wit's End — MR/tenacidad — no está en la fórmula)."""
        finales, hojas = O.optimizar("kalista", top=6, verbose=False)
        combos = [sorted(f[1]) for f in finales]
        self.assertIn(sorted(KALISTA_K2), combos)
        rank = combos.index(sorted(KALISTA_K2)) + 1
        self.assertLessEqual(rank, 3)
        self.assertLess(finales[0][0] - finales[rank - 1][0], 0.015)

    def test_IE_excluido_por_modelo(self):
        """batch2.kalista no modela críticos → IE fuera del pool (conservador)."""
        finales, _ = O.optimizar("kalista", top=10, verbose=False)
        for f in finales:
            self.assertNotIn("IE", f[1])


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
        for f in finales:
            self.assertEqual(len(f[1]), 6)
            self.assertIn(f[1][0], ("Spellslinger", "Crimson"))   # 1 botas (Ley 0)


class TestYuumiAliado(unittest.TestCase):
    def test_Y1_gana_entre_las_candidatas_del_reporte(self):
        """NIVEL 1: Y1 (Censer/Echoes/Staff/Redemption) es la mejor de Y1-Y5 (§8)."""
        scores = puntuar_normalizado("yuumi", "aliado", YUUMI_CANDIDATAS)
        self.assertEqual(max(scores, key=scores.get), "Y1")

    def test_slots_fijos_de_support(self):
        """Motor aliado: quest (Scythe) fija + botas Crimson + 4 elegibles = 6 slots."""
        finales, hojas = O.optimizar("yuumi", top=5, verbose=False)
        self.assertGreater(hojas, 0)
        for f in finales:
            self.assertEqual(len(f[1]), 6)
            self.assertIn("Crimson", f[1])
            self.assertIn("Scythe", f[1])


if __name__ == "__main__":
    unittest.main(verbosity=2)


class TestDefensaUtilidad(unittest.TestCase):
    """Modelo de defensa/utilidad v1.9 (EHP mixto + activas + sustain ponderado)."""

    def test_ehp_botas_magicas(self):
        bd = O.cargar_base_def("jinx")
        e_gun, _ = O.ehp_y_util(["gunmetal", "c44", "runaan", "ie", "ldr", "kraken"], bd, 186)
        e_chain, _ = O.ehp_y_util(["chainlaced", "c44", "runaan", "ie", "ldr", "kraken"], bd, 186)
        self.assertGreater(e_chain, e_gun)          # +150 HP +30 MR + escudo mágico

    def test_util_bt_sobre_kraken(self):
        bd = O.cargar_base_def("jinx")
        _, u_c = O.ehp_y_util(["gunmetal", "c44", "runaan", "ie", "ldr", "kraken"], bd, 186)
        _, u_d = O.ehp_y_util(["gunmetal", "c44", "runaan", "ie", "ldr", "bt"], bd, 594)
        self.assertGreater(u_d, u_c)                # Ichorshield + lifesteal alto

    def test_ga_aporta_utilidad(self):
        bd = O.cargar_base_def("jinx")
        _, u_sin = O.ehp_y_util(["gunmetal", "c44", "runaan", "ie", "ldr", "kraken"], bd, 186)
        _, u_ga = O.ehp_y_util(["gunmetal", "c44", "runaan", "ie", "ldr", "ga"], bd, 180)
        self.assertGreater(u_ga, u_sin + 200)       # bandera Resurrect (300)

    def test_preset_balanceado_habilita_defensivos(self):
        """Con 15 % EHP + 15 % utilidad, al menos una build del top lleva ítem defensivo/activa."""
        finales, _ = O.optimizar("jinx", oro=18000, top=8, crit_min=100, pen_min=30,
                                 preset="balanceado", verbose=False)
        # post-exclusividad (v1.14): la utilidad la domina el sustain (BotRK/BT) — el preset
        # debe seguir sacando a superficie ítems defensivos O de sustain con EHP/UTIL activos
        defensivos = {"ga", "scimitar", "shieldbow", "maw", "chainlaced", "armored_adv",
                      "immortal_treads", "deathsdance", "botrk", "bt"}
        claves = [[M.resolve(c).key for c in f[1]] for f in finales]
        self.assertTrue(any(defensivos & set(k) for k in claves),
                        f"ningún defensivo/sustain en el top: {claves}")
        self.assertTrue(all(f[4] > 0 for f in finales))     # columna EHP calculada

    def test_default_ofensivo_golden_intacto(self):
        """Sin pesos de defensa (default), el ranking no cambia: C sigue siendo top-1."""
        finales, _ = O.optimizar("jinx", oro=18000, top=1, crit_min=100, pen_min=30,
                                 incluir=POOL_JINX_REPORTE, preset="ofensivo", verbose=False)
        self.assertEqual(sorted(M.resolve(x).key for x in finales[0][1]),
                         sorted(M.resolve(x).key for x in JINX_C))


class TestMotorPorArquetipo(unittest.TestCase):
    """Bug reportado 29-sep: 'optimize chogath' lo trataba como ADC. Ahora los arquetipos
    sin motor se rechazan con guía, y las aproximaciones avisan."""

    def test_chogath_rechazado(self):
        with self.assertRaises(SystemExit):
            O.optimizar("chogath", verbose=False)

    def test_mordekaiser_rechazado(self):
        with self.assertRaises(SystemExit):
            O.optimizar("mordekaiser", verbose=False)

    def test_forzar_motor_permitido_bajo_responsabilidad(self):
        finales, _ = O.optimizar("chogath", motor="autos", top=1, verbose=False,
                                 incluir=["gunmetal", "c44", "runaan", "ie", "ldr", "kraken"])
        self.assertEqual(len(finales[0][1]), 6)

    def test_yunara_aproximado_funciona(self):
        finales, _ = O.optimizar("yunara", top=1, verbose=False,
                                 incluir=["gunmetal", "c44", "runaan", "ie", "ldr", "kraken"])
        self.assertEqual(len(finales[0][1]), 6)
        self.assertEqual(M.validate_slots(finales[0][1]), (1, 5))
