# -*- coding: utf-8 -*-
"""WR-LAB · tests del backfill de frontmatter (Fase 1 migración — contrato de datos)."""
import os, re, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import backfill_frontmatter as B
import update_reports as U

REP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reportes")


class TestDerivacion(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(B.slugify("Cho'Gath - Titán del Barón.md"), "chogath-titan-del-baron")
        self.assertEqual(B.slugify("Volibear Pesadilla.md"), "volibear-pesadilla")
        self.assertEqual(B.slugify("Diana - Mid.md"), "diana-mid")
        self.assertEqual(B.slugify("Jinx.md"), "jinx")

    def test_fecha_iso_dos_formatos(self):
        a = "**Fecha del análisis:** 27/09/2026 · Variante añadida el 29/09/2026"
        b = "**Fecha del análisis:** 26-sep-2026"
        self.assertEqual(B.fecha_iso(a), "2026-09-27")   # primera fecha, no la del apéndice
        self.assertEqual(B.fecha_iso(b), "2026-09-26")

    def test_procesar_idempotente_y_cuerpo_intacto(self):
        txt = ("---\ntags:\n  - Test\nversion: 1\nStatus: Beta\n---\n"
               "**Fecha del análisis:** 01/10/2026\n**Parche:** 7.3 (21-sep-2026)\n"
               "**Rol principal:** ADC (Dragon Lane)\n**Arquetipo:** Crítico AoE\n\n## 0. RESUMEN\n")
        nuevo, añadidos = B.procesar("Prueba.md", txt, {})
        self.assertIn("champion: Prueba", "\n".join(nuevo.splitlines()[:12]))
        self.assertIn('patch: "7.3"', nuevo)
        self.assertIn("role: adc", nuevo)
        self.assertIn("archetype: Crítico AoE", nuevo)
        self.assertIn("## 0. RESUMEN", nuevo)
        self.assertEqual(nuevo.split("\n---\n", 1)[1], txt.split("\n---\n", 1)[1])  # cuerpo intacto
        otro, mas = B.procesar("Prueba.md", nuevo, {})
        self.assertEqual(mas, [])                            # segunda pasada: nada


class TestEstadoVault(unittest.TestCase):
    def test_todos_con_claves_del_contrato(self):
        archivos = [f for f in sorted(os.listdir(REP)) if f.endswith(".md")]
        self.assertEqual(len(archivos), 16)
        for f in archivos:
            with open(os.path.join(REP, f), encoding="utf-8") as fh:
                txt = fh.read()
            fm = U.parse_frontmatter(txt)
            for clave in ("champion", "slug", "role", "engine", "Status", "version"):
                self.assertIn(clave, fm, f"{f}: falta {clave}")
            self.assertIn(fm["role"], ("adc", "support", "jungla", "mid", "top"), f)

    def test_jinx_patch_preservado(self):
        with open(os.path.join(REP, "Jinx.md"), encoding="utf-8") as fh:
            fm = U.parse_frontmatter(fh.read())
        self.assertEqual(fm["patch"], "7.3a")        # existente: NO se modificó
        self.assertEqual(fm["version"], "1.4")

    def test_yunana_champion_canonico(self):
        with open(os.path.join(REP, "Yunana.md"), encoding="utf-8") as fh:
            fm = U.parse_frontmatter(fh.read())
        self.assertEqual(fm["champion"], "Yunara")   # canónico, no la errata del archivo
