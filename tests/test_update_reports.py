# -*- coding: utf-8 -*-
"""
WR-LAB · tests del actualizador de reportes (model/update_reports.py).
Cubren: golden numbers por modelo, parseo de Tabla A, triage del hotfix 7.3a
(caso de aceptación: Yuumi NO se regenera), idempotencia de la anotación,
rúbrica de veredictos y orden de parches.
Ejecutar:  python3 -m unittest discover -s tests -v
"""
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import update_reports as U
import dps_model as M


class TestGoldenPorModelo(unittest.TestCase):
    """Los hooks del actualizador deben reproducir los números publicados en los reportes."""

    @classmethod
    def setUpClass(cls):
        cls.reg = U.construir_registro()

    def entry(self, champ):
        for f, e in self.reg["reportes"].items():
            if e["champion"] == champ:
                return e
        self.fail(f"sin reporte para {champ}")

    def test_jinx_publicado(self):
        m = U.hook_jinx(self.entry("jinx")["build_keys"])
        self.assertEqual(round(m["dps1"]), 3042)      # canónico del motor (tests/test_model.py)
        self.assertEqual(round(m["dps3"]), 10551)

    def test_kalista_publicado(self):
        m = U.hook_kalista(self.entry("kalista")["build_keys"])
        self.assertEqual(round(m["dps1"]), 1262)      # reporte: 1v1 vs 120 arm/50 MR
        self.assertEqual(round(m["dps3"]), 2612)
        self.assertEqual(round(m["e_hit"]), 2387)

    def test_diana_publicado(self):
        m = U.hook_diana(self.entry("diana")["build_keys"])
        self.assertEqual(round(m["dps10s"]), 971)     # reporte: DPS sostenido D2-LT
        self.assertEqual(round(m["burst"]), 1792)

    def test_yuumi_publicado_pre73a(self):
        """Con los parámetros pre-7.3a (W flat 11, sin término AP) se reproduce el publicado E=339/R=651."""
        e = self.entry("yuumi")
        pre = U.hook_yuumi(e["build_keys"], params={"w_flat": 11, "w_ap_pct": 0.0})
        self.assertEqual(round(pre["e_shield"]), 339)
        self.assertEqual(round(pre["r_heal"]), 651)
        self.assertEqual(round(pre["adc_dps_add"]), 244)

    def test_yuumi_actual_post73a(self):
        """El motor ya trae el nerf 7.3a aplicado (W rank5 = 9 + 0.01/AP → E ≈ 338)."""
        e = self.entry("yuumi")
        act = U.hook_yuumi(e["build_keys"])
        self.assertLess(act["e_shield"], 339)
        self.assertAlmostEqual(act["e_shield"], 338.3, delta=0.5)


class TestParseoReportes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = U.construir_registro()

    def test_cinco_reportes_parseados(self):
        self.assertEqual(len(self.reg["reportes"]), 5)

    def test_builds_de_seis_con_una_botas(self):
        boots = {"Gunmetal Greaves", "Berserker's Greaves", "Spellslinger's Shoes",
                 "Crimson Lucidity", "Ionian Boots", "Boots of Mana"}
        for f, e in self.reg["reportes"].items():
            self.assertEqual(len(e["build_display"]), 6, f)
            self.assertEqual(sum(1 for b in e["build_display"] if b in boots), 1, f)

    def test_jinx_pasa_validate_slots(self):
        e = [x for x in self.reg["reportes"].values() if x["champion"] == "jinx"][0]
        self.assertEqual(M.validate_slots(e["build_keys"]), (1, 5))   # Ley 0

    def test_sin_items_por_resolver(self):
        for f, e in self.reg["reportes"].items():
            if e.get("hook"):
                self.assertEqual(e["sin_resolver"], [], f)


class TestTriage73a(unittest.TestCase):
    """Caso de aceptación del autor: Yuumi 7.3a → nerf simbólico, NO regenerar."""

    @classmethod
    def setUpClass(cls):
        cls.reg = U.construir_registro()
        cls.patch, cls.cs, cls.res = U.triage_todos(cls.reg, patch="7.3a")
        cls.por_nombre = {t["champion"]: t for t in cls.res}

    def test_parseo_del_diff(self):
        self.assertIn("Yuumi", self.cs["champions"])
        self.assertIn("Hwei", self.cs["champions"])
        self.assertTrue(any("Yun Tal" in i for i in self.cs["items"]))
        self.assertGreaterEqual(len(self.cs["sistemas"]), 3)
        self.assertGreaterEqual(len(self.cs["lab_notes"]), 5)

    def test_yuumi_no_se_regenera(self):
        t = self.por_nombre["Yuumi"]
        self.assertEqual(t["veredicto"], "ANOTAR")
        self.assertIsNotNone(t["directo"])
        self.assertTrue(t["cuantificado"])
        self.assertLess(t["delta_max"], U.UMBRAL_ANOTAR)      # 1.4 % < 2 %
        self.assertAlmostEqual(t["delta_max"], 1.43, delta=0.1)

    def test_yuumi_delta_de_resultado_no_de_input(self):
        """El HSP cae 5 % (input) pero el veredicto lo deciden escudo/cura (−1.4 %)."""
        t = self.por_nombre["Yuumi"]
        self.assertAlmostEqual(t["delta_input"]["HSP"], -5.0, delta=0.2)
        self.assertLess(t["delta_max"], 2.0)

    def test_ningun_reporte_regenera_o_revisa(self):
        for t in self.res:
            self.assertEqual(t["veredicto"], "ANOTAR", t["archivo"])

    def test_jinx_sistema_de_siege_detectado(self):
        t = self.por_nombre["Jinx"]
        self.assertTrue(any("Placas" in s or "placa" in s.lower() for s in t["sistemas"]))
        self.assertEqual(t["delta_max"], 0.0)

    def test_kalista_yuntal_como_variante(self):
        t = self.por_nombre["Kalista"]
        self.assertTrue(any("Yun Tal" in v for v in t["items_variantes"]))
        self.assertEqual(t["items_build"], [])


class TestRubrica(unittest.TestCase):
    """Veredictos sintéticos: spec-input → REGENERAR; ítem de build → REVISAR."""

    @classmethod
    def setUpClass(cls):
        cls.reg = U.construir_registro()
        cls.jinx_file = [f for f, e in cls.reg["reportes"].items() if e["champion"] == "jinx"][0]
        cls.jinx = cls.reg["reportes"][cls.jinx_file]

    def _cs(self, champions=None, items=None):
        return {"champions": champions or {}, "items": items or {}, "sistemas": [],
                "lab_notes": {}, "raw": "sintetico"}

    def test_spec_input_regenerar(self):
        cs = self._cs(champions={"Jinx": {"tipo": "BUFF", "detalles": "AD growth 4.0→4.5"}})
        t = U.triage_reporte(self.jinx_file, self.jinx, cs, "9.9z")
        self.assertEqual(t["veredicto"], "REGENERAR")

    def test_item_de_build_revisar(self):
        cs = self._cs(items={"Kraken Slayer": {"tipo": "NERF", "detalles": "proc 120-168→110-150"}})
        t = U.triage_reporte(self.jinx_file, self.jinx, cs, "9.9z")
        self.assertEqual(t["veredicto"], "REVISAR")
        self.assertIn("Kraken Slayer", t["items_build"])

    def test_directo_sin_cuantificar_revisar(self):
        cs = self._cs(champions={"Jinx": {"tipo": "NERF", "detalles": "W daño 220→200"}})
        t = U.triage_reporte(self.jinx_file, self.jinx, cs, "9.9z")
        self.assertEqual(t["veredicto"], "REVISAR")   # conservador: sin parser pre/post

    def test_parche_irrelevante_sin_impacto(self):
        cs = self._cs(champions={"Hwei": {"tipo": "NERF", "detalles": "pasiva 33→30"}})
        t = U.triage_reporte(self.jinx_file, self.jinx, cs, "9.9z")
        self.assertEqual(t["veredicto"], "SIN_IMPACTO")


class TestAnotacion(unittest.TestCase):
    TXT = ("---\nchampion: Test\n---\n"
           "**Fecha del análisis:** 01/01/2030\n\n"
           "> [!NOTE]\n> Meta.\n\n## 0. RESUMEN\n")

    def test_insercion_antes_del_primer_callout(self):
        bloque = "<!-- WRLAB-VERIF:9.9z:START -->\n> [!NOTE] x\n<!-- WRLAB-VERIF:9.9z:END -->"
        out = U.insertar_bloque(self.TXT, bloque, "9.9z")
        self.assertLess(out.index("WRLAB-VERIF:9.9z:START"), out.index("> [!NOTE]\n> Meta."))

    def test_idempotencia_byte_a_byte(self):
        bloque = "<!-- WRLAB-VERIF:9.9z:START -->\n> [!NOTE] x\n<!-- WRLAB-VERIF:9.9z:END -->"
        u1 = U.insertar_bloque(self.TXT, bloque, "9.9z")
        u2 = U.insertar_bloque(u1, bloque, "9.9z")
        u3 = U.insertar_bloque(u2, bloque, "9.9z")
        self.assertEqual(u1, u2)
        self.assertEqual(u2, u3)

    def test_multiparche_no_se_pisa(self):
        b1 = "<!-- WRLAB-VERIF:9.8z:START -->\n> [!NOTE] a\n<!-- WRLAB-VERIF:9.8z:END -->"
        b2 = "<!-- WRLAB-VERIF:9.9z:START -->\n> [!NOTE] b\n<!-- WRLAB-VERIF:9.9z:END -->"
        out = U.insertar_bloque(self.TXT, b1, "9.8z")
        out = U.insertar_bloque(out, b2, "9.9z")
        self.assertIn("9.8z:END", out)
        self.assertIn("9.9z:END", out)
        self.assertLess(out.index("9.8z:END"), out.index("9.9z:START"))


class TestUtilidades(unittest.TestCase):
    def test_orden_de_parches(self):
        self.assertLess(U.patch_key("7.3"), U.patch_key("7.3a"))
        self.assertLess(U.patch_key("7.3a"), U.patch_key("7.3b"))
        self.assertLess(U.patch_key("7.3z"), U.patch_key("7.4"))

    def test_expandir_nombre_compuesto(self):
        self.assertEqual(U.expandir_nombre_item("Crown/Diadem of Songs"),
                         ["Crown of Songs", "Diadem of Songs"])

    def test_ultimo_parche_es_73a(self):
        p, ruta = U.ultimo_parche_hotfix()
        self.assertEqual(p, "7.3a")
        self.assertTrue(ruta.endswith("cambios_7.3a.md"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
