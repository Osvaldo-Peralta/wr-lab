# -*- coding: utf-8 -*-
"""
WR-LAB · tests del actualizador de reportes (model/update_reports.py).
Cubren: golden numbers por modelo (hooks), parseo del vault (16 reportes, formatos
mixtos: Tabla v1.4 / tablas BUILD FINAL / alias en paréntesis / rutas descartadas),
triage del hotfix 7.3a sobre el set real (Caitlyn/Rammus ❌, Yuumi ⚠️, resto ✅),
rúbrica sintética, idempotencia de anotación, AL_DIA y orden de parches.
Ejecutar:  python3 -m unittest discover -s tests -v
"""
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import update_reports as U
import dps_model as M

JINX_C = ["Gunmetal", "C44", "Runaan's", "IE", "LDR", "Kraken"]
KALISTA_K2 = ["Gunmetal", "Guinsoo", "WitsEnd", "Terminus", "BotRK", "Runaan"]
DIANA_D2 = ["Spellslinger", "DuskDawn", "Nashor", "Rabadon", "Zhonyas", "Cryptbloom"]
YUUMI_Y1 = ["Scythe", "Crimson", "Censer", "Echoes", "Staff", "Redemption"]


class TestGoldenPorModelo(unittest.TestCase):
    """Los hooks reproducen los números canónicos publicados (nivel de unidad, sin registro)."""

    def test_jinx(self):
        m = U.hook_jinx(JINX_C)
        self.assertEqual(round(m["dps1"]), 3042)
        self.assertEqual(round(m["dps3"]), 10551)

    def test_kalista(self):
        m = U.hook_kalista(KALISTA_K2)
        self.assertEqual(round(m["dps1"]), 1262)
        self.assertEqual(round(m["dps3"]), 2612)
        self.assertEqual(round(m["e_hit"]), 2387)

    def test_diana(self):
        m = U.hook_diana(DIANA_D2)
        self.assertEqual(round(m["dps10s"]), 971)
        self.assertEqual(round(m["burst"]), 1792)

    def test_yuumi_pre73a_reproduce_publicado(self):
        pre = U.hook_yuumi(YUUMI_Y1, params={"w_flat": 11, "w_ap_pct": 0.0})
        self.assertEqual(round(pre["e_shield"]), 339)
        self.assertEqual(round(pre["r_heal"]), 651)
        self.assertEqual(round(pre["adc_dps_add"]), 244)

    def test_yuumi_post73a_en_el_motor(self):
        act = U.hook_yuumi(YUUMI_Y1)
        self.assertAlmostEqual(act["e_shield"], 338.3, delta=0.5)


class TestRegistroVault(unittest.TestCase):
    """Parseo del set real de 16 reportes del vault (formatos mixtos)."""

    @classmethod
    def setUpClass(cls):
        cls.reg = U.construir_registro()
        cls.entradas = cls.reg["reportes"]

    def entry(self, archivo):
        return self.entradas[archivo]

    def test_16_reportes(self):
        self.assertEqual(len(self.entradas), 16)

    def test_champions_derivados_del_nombre(self):
        self.assertEqual(self.entry("Yunana.md")["champion_display"], "Yunara")     # errata de archivo
        self.assertEqual(self.entry("Cho'Gath - Titán del Barón.md")["champion_display"], "Cho'Gath")
        self.assertEqual(self.entry("Volibear Pesadilla.md")["champion_display"], "Volibear")
        self.assertEqual(self.entry("Diana - Mid.md")["champion_display"], "Diana")

    def test_jinx_build_c_con_hooks(self):
        e = self.entry("Jinx.md")
        self.assertEqual(e["hook"], "hook_jinx")
        self.assertEqual(e["build_keys"], JINX_C)
        self.assertEqual(round(e["metricas"]["dps1"]), 3042)
        self.assertEqual(M.validate_slots(e["build_keys"]), (1, 5))   # Ley 0

    def test_kalista_fallback_con_alias_parentetico(self):
        """Kalista.md no usa Tabla A; 'Bloodthirster (BotRK)' debe resolver a BotRK (K2)."""
        e = self.entry("Kalista.md")
        self.assertEqual(e["hook"], "hook_kalista")
        self.assertEqual(sorted(e["build_keys"]), sorted(KALISTA_K2))
        self.assertEqual(round(e["metricas"]["dps1"]), 1262)

    def test_diana_dos_archives_cuantitativos(self):
        for f in ("Diana - Jungla.md", "Diana - Mid.md"):
            e = self.entry(f)
            self.assertEqual(e["hook"], "hook_diana", f)
            self.assertIsNotNone(e["metricas"], f)

    def test_yuumi_poke_hybrid_con_hook_tras_expansion(self):
        """v1.8: Y_ITEMS expandido desde items_7.3.csv → la build poke-híbrida ya es cuantificable."""
        e = self.entry("Yuumi.md")
        self.assertEqual(e["hook"], "hook_yuumi")
        self.assertEqual(e["sin_resolver"], [])
        self.assertEqual(round(e["metricas"]["AP"]), 230)      # AP de la build (fuente: CSV oficial)
        self.assertLess(e["metricas"]["e_shield"], 339)        # sacrifica escudo vs Y1 clásica (~305)

    def test_reportes_sin_build_extraible(self):
        for f in ("Heimerdinger.md", "Rammus.md", "Seraphine.md"):
            self.assertEqual(self.entry(f)["hook"], None, f)

    def test_rutas_no_confundidas_con_build(self):
        """Sivir/Yunara: la tabla con columna 'Minuto' es ruta de compra, no build final."""
        e = self.entry("Sivir.md")
        if e["build_display"]:                            # si parseó la tabla BUILD FINAL (§2)
            self.assertNotIn("⬆️ Gunmetal Greaves", e["build_display"])


class TestParserUnidades(unittest.TestCase):
    def test_celda_bold_con_flecha_interna(self):
        self.assertEqual(U._nombre_de_celda("**Berserker's Greaves → ⬆️ Gunmetal Greaves** (min 10:00)"),
                         "Gunmetal Greaves")

    def test_celda_sin_bold(self):
        self.assertEqual(U._nombre_de_celda("Guinsoo's Rageblade"), "Guinsoo's Rageblade")

    def test_resolver_alias_parentetico(self):
        self.assertEqual(U.resolver_clave("Bloodthirster (BotRK)", "onhit"), "BotRK")

    def test_resolver_full_name_autos(self):
        self.assertEqual(U.resolver_clave("Lord Dominik's Regards", "autos"), "LDR")

    def test_mencionado_sin_falsos_positivos(self):
        tl = U._norm("Esta build usa Rabadon's Deathcap y Zhonya's Hourglass.")
        self.assertIsNone(U._mencionado(tl, "Death's Dance"))       # 'death' ⊄ 'deathcap' por \b
        self.assertIsNotNone(U._mencionado(U._norm("Consideré Death's Dance y la descarté."),
                                           "Death's Dance"))

    def test_expandir_nombre_compuesto(self):
        self.assertEqual(U.expandir_nombre_item("Crown/Diadem of Songs"),
                         ["Crown of Songs", "Diadem of Songs"])

    def test_orden_de_parches(self):
        self.assertLess(U.patch_key("7.3"), U.patch_key("7.3a"))
        self.assertLess(U.patch_key("7.3a"), U.patch_key("7.3b"))
        self.assertLess(U.patch_key("7.3z"), U.patch_key("7.4"))


class TestTriage73aVault(unittest.TestCase):
    """Triage real del hotfix 7.3a sobre los 16 reportes del vault."""

    @classmethod
    def setUpClass(cls):
        cls.reg = U.construir_registro()
        cls.patch, cls.cs, cls.res = U.triage_todos(cls.reg, patch="7.3a")
        cls.por = {t["archivo"]: t for t in cls.res}

    def test_caitlyn_regenerar(self):
        """7.3a nerfeó su AS growth (input del spec) → el reporte 7.3 debe regenerarse."""
        self.assertEqual(self.por["Caitlyn.md"]["veredicto"], "REGENERAR")

    def test_rammus_regenerar(self):
        """7.3a nerfeó su armadura base (input del spec)."""
        self.assertEqual(self.por["Rammus.md"]["veredicto"], "REGENERAR")

    def test_yuumi_anotar_cuantificado(self):
        """v1.8: con el diccionario expandido, el nerf de la poke-híbrida se mide: Δ conservador
        −1.7 % (< 2 %) → ✅ ANOTAR. (Con AP 230, el término 0.01 %/AP casi neutraliza el nerf.)"""
        t = self.por["Yuumi.md"]
        self.assertEqual(t["veredicto"], "ANOTAR")
        self.assertTrue(t["cuantificado"])
        self.assertLess(t["delta_max"], U.UMBRAL_ANOTAR)
        self.assertAlmostEqual(t["delta_max"], 1.72, delta=0.15)

    def test_jinx_al_dia(self):
        """Jinx.md v1.4 declara patch 7.3a en frontmatter → ⏩ AL_DIA (sin bloque ni triage)."""
        t = self.por["Jinx.md"]
        self.assertEqual(t["veredicto"], "AL_DIA")
        self.assertTrue(any("7.3a" in r for r in t["razones"]))

    def test_sivir_anotar_con_variantes_y_sistemas(self):
        """Sivir declara 7.3 → se tria: Yun Tal en sus variantes + sistemas de siege (rol ADC)."""
        t = self.por["Sivir.md"]
        self.assertEqual(t["veredicto"], "ANOTAR")
        self.assertTrue(any("Yun Tal" in v for v in t["items_variantes"]))
        self.assertTrue(t["sistemas"])                    # placas/Nexus

    def test_kalista_cuantitativo(self):
        t = self.por["Kalista.md"]
        self.assertEqual(t["delta_max"], 0.0)
        self.assertNotEqual(t["veredicto"], "REGENERAR")

    def test_balance_general(self):
        verdictos = [t["veredicto"] for t in self.res]
        self.assertEqual(verdictos.count("REGENERAR"), 2)      # Caitlyn + Rammus (inputs del spec)
        self.assertEqual(verdictos.count("REVISAR"), 0)        # Yuumi ya es cuantificable (v1.8)
        self.assertEqual(len(self.res), 16)

    def test_al_dia_si_el_reporte_ya_cubre_el_parche(self):
        """Un reporte con patch declarado ≥ 7.3a no se tria (⏩ AL_DIA)."""
        reg = U.construir_registro()
        f = "Jinx.md"
        reg["reportes"][f]["parche_declarado"] = "7.3+7.3a"
        t = U.triage_reporte(f, reg["reportes"][f], self.cs, "7.3a")
        self.assertEqual(t["veredicto"], "AL_DIA")


class TestRubricaSintetica(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = U.construir_registro()
        cls.jinx_file = "Jinx.md"
        cls.jinx = cls.reg["reportes"][cls.jinx_file]

    def _cs(self, champions=None, items=None):
        return {"champions": champions or {}, "items": items or {}, "sistemas": [],
                "lab_notes": {}, "raw": "sintetico"}

    def test_spec_input_regenerar(self):
        cs = self._cs(champions={"Jinx": {"tipo": "BUFF", "detalles": "AD growth 4.0→4.5"}})
        self.assertEqual(U.triage_reporte(self.jinx_file, self.jinx, cs, "9.9z")["veredicto"],
                         "REGENERAR")

    def test_item_de_build_revisar(self):
        cs = self._cs(items={"Kraken Slayer": {"tipo": "NERF", "detalles": "proc 120-168→110-150"}})
        t = U.triage_reporte(self.jinx_file, self.jinx, cs, "9.9z")
        self.assertEqual(t["veredicto"], "REVISAR")
        self.assertIn("Kraken Slayer", t["items_build"])

    def test_directo_sin_cuantificar_revisar(self):
        cs = self._cs(champions={"Jinx": {"tipo": "NERF", "detalles": "W daño 220→200"}})
        self.assertEqual(U.triage_reporte(self.jinx_file, self.jinx, cs, "9.9z")["veredicto"],
                         "REVISAR")

    def test_parche_irrelevante_sin_impacto(self):
        cs = self._cs(champions={"Hwei": {"tipo": "NERF", "detalles": "pasiva 33→30"}})
        self.assertEqual(U.triage_reporte(self.jinx_file, self.jinx, cs, "9.9z")["veredicto"],
                         "SIN_IMPACTO")


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
        self.assertLess(out.index("9.8z:END"), out.index("9.9z:START"))

    def test_reportes_del_vault_bloque_o_al_dia(self):
        """Cada reporte del vault tiene bloque WRLAB-VERIF:7.3a O declara patch ≥ 7.3a (AL_DIA)."""
        import glob
        for ruta in glob.glob(os.path.join(U.REPORTES, "*.md")):
            with open(ruta, encoding="utf-8") as fh:
                txt = fh.read()
            fm = U.parse_frontmatter(txt)
            pd = U.parche_declarado(fm, txt)
            al_dia = pd and U.patch_key(pd) >= U.patch_key("7.3a")
            self.assertTrue("WRLAB-VERIF:7.3a:START" in txt or al_dia,
                            f"{os.path.basename(ruta)}: ni bloque ni patch declarado ≥7.3a")


class TestUtilidades(unittest.TestCase):
    def test_ultimo_parche_es_73a(self):
        p, ruta = U.ultimo_parche_hotfix()
        self.assertEqual(p, "7.3a")
        self.assertTrue(ruta.endswith("cambios_7.3a.md"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
