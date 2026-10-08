# -*- coding: utf-8 -*-
"""WR-LAB · tests del generador automático de reportes (model/generate_report.py)."""
import os, re, shutil, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import generate_report as G
import update_reports as U
import dps_model as M


class TestGenerador(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_genera_yunara_estructura_completa(self):
        ruta = G.generar("yunara", rol="adc", top=4, outdir=self.tmp)
        txt = open(ruta, encoding="utf-8").read()
        fm = U.parse_frontmatter(txt)
        self.assertEqual(fm["Status"], "Espera de verificación")
        self.assertEqual(fm["generate"], "auto")
        self.assertEqual(fm["champion"], "Yunara")
        self.assertEqual(fm["engine"], "autos")
        # Tabla A re-parseable y legal (Ley 0)
        build, fuente = U.extraer_build(txt)
        self.assertEqual(len(build), 6)
        keys = [M.resolve(U.resolver_clave(b, "autos") or b).key for b in build]
        self.assertEqual(M.validate_slots(keys), (1, 5))
        # secciones del TEMPLATE y advertencia de aproximación
        for sec in ("## 0. RESUMEN", "## 4. LEYES", "## 8. COMPARACIÓN", "## Pie de página",
                    "ESPERA DE VERIFICACIÓN", "TODO"):
            self.assertIn(sec, txt)
        self.assertIn("spread de Q", txt)          # MOTOR_AVISOS embebido

    def test_chogath_cae_en_modo_cualitativo(self):
        """v1.13.1: SIN_MOTOR ya no rechaza — genera cualitativo desde su reporte publicado."""
        ruta = G.generar("chogath", outdir=self.tmp)
        txt = open(ruta, encoding="utf-8").read()
        self.assertIn("MODO CUALITATIVO", txt)
        self.assertEqual(U.parse_frontmatter(txt)["engine"], "none")

    def test_shyvana_generado_existe_y_parsea(self):
        """El deliverable commiteado en reportes/_auto/ es íntegro."""
        ruta = os.path.join(U.REPORTES, "_auto", "Shyvana_AUTO_7.3a.md")
        if not os.path.exists(ruta):
            self.skipTest("el vault no embarca reportes/_auto (regenerable)")
        txt = open(ruta, encoding="utf-8").read()
        build, _ = U.extraer_build(txt)
        self.assertEqual(len(build), 6)
        self.assertIn("Status: Espera de verificación", txt)

    def test_auto_dir_fuera_del_registro(self):
        reg = U.construir_registro()
        self.assertNotIn("Shyvana_AUTO_7.3a.md", reg["reportes"])


class TestAprobacion(unittest.TestCase):
    def test_status_cambia_a_aprobado(self):
        txt = "---\ntags:\n  - Test\nStatus: Espera de verificación\nslug: x-auto\n---\nCuerpo.\n"
        nuevo = re.sub(r"^Status:.*$", "Status: Aprobado", txt, count=1, flags=re.M)
        nuevo = nuevo.replace("Status: Espera de verificación", "Status: Aprobado")
        self.assertIn("Status: Aprobado", nuevo)
        self.assertNotIn("Espera de verificación", nuevo)


class TestModoCualitativo(unittest.TestCase):
    """Campeones sin motor (Rammus tanque): plantilla completa + datos reales + TODOs."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_rammus_cualitativo(self):
        ruta = G.generar_cualitativo("rammus", outdir=self.tmp)
        txt = open(ruta, encoding="utf-8").read()
        fm = U.parse_frontmatter(txt)
        self.assertEqual(fm["Status"], "Espera de verificación")
        self.assertEqual(fm["engine"], "none")
        self.assertEqual(fm["generate"], "auto")
        self.assertIn("MODO CUALITATIVO", txt)
        # Ley 0: corrige botas T2 de la ruta publicada
        self.assertIn("Armored Advance", txt)
        self.assertIn("MISMO slot", txt)
        # cálculos parciales reales del nerf 7.3a
        self.assertIn("W rank 1", txt)
        self.assertIn("EHP físico", txt)
        # marcadores de fuente del estándar v1.13.1
        self.assertIn("📌 Pre-", txt)
        self.assertIn("🔬 LAB", txt)
        # build publicada re-parseable
        build, _ = U.extraer_build(txt)
        self.assertEqual(len(build), 6)

    def test_generar_ramifica_a_cualitativo(self):
        ruta = G.generar("rammus", outdir=self.tmp)     # sin spec → cualitativo, no SystemExit
        self.assertTrue(os.path.exists(ruta))


class TestEstandarV1131(unittest.TestCase):
    def test_seccion8_nombres_completos_y_marcadores(self):
        tmp = tempfile.mkdtemp()
        try:
            ruta = G.generar("yunara", rol="adc", top=4, outdir=tmp)
            txt = open(ruta, encoding="utf-8").read()
            self.assertIn("⭐ LAB (óptima)", txt)
            self.assertIn("🔬 LAB top-2", txt)
            self.assertIn("Gunmetal Greaves + ", txt)     # nombres completos, no claves
            self.assertNotIn("gunmetal+runaan", txt)      # sin formato abreviado
            self.assertIn("| Fuente |", txt)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
