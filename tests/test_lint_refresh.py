# -*- coding: utf-8 -*-
"""
WR-LAB · tests de las herramientas de calidad de reportes:
linter (model/lint_reportes.py), refresh y borrador (update_reports.py).
Ejecutar:  python3 -m unittest discover -s tests -v
"""
import os, sys, types, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import update_reports as U
import lint_reportes as L

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REP = os.path.join(ROOT, "reportes")


class TestLinter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.legit = L.nombres_items_oficiales()

    def lint(self, nombre):
        return L.lint_archivo(os.path.join(REP, nombre), self.legit, "7.3a")

    def test_jinx_sin_errores(self):
        _, errs, _ = self.lint("Jinx.md")
        self.assertEqual(errs, [])

    def test_build_no_extraible_es_error(self):
        for f in ("Heimerdinger.md", "Volibear.md"):   # Seraphine v1.2 (Modo Agresiva) ya parsea
            _, errs, _ = self.lint(f)
            self.assertTrue(any("no extraíble" in e for e in errs), f)

    def test_slot_situacional_es_aviso_no_error(self):
        _, errs, avis = self.lint("Sivir.md")
        self.assertEqual(errs, [])
        self.assertTrue(any("situacional" in a for a in avis))

    def test_item_alucinado_detectado(self):
        mini = """---
tags:
  - Test
version: 1
Status: Beta
---
**Fecha del análisis:** 29/09/2026
**Parche:** 7.3 (21-sep-2026)
**Rol principal:** Support

### Tabla A — BUILD FINAL

| Slot | Ítem | Oro | Rol |
|---|---|---|---|
| 1 (botas) | **Ionian Boots → ⬆️ Crimson Lucidity** | 2 000 | x |
| 2 | **Bastion of Spirits** | 2 600 | ítem inventado |
| 3 | **Ardent Censer** | 2 400 | x |
| 4 | **Echoes of Helia** | 2 400 | x |
| 5 | **Staff of Flowing Waters** | 2 400 | x |
| 6 | **Redemption** | 2 450 | x |

## 0. RESUMEN
"""
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as fh:
            fh.write(mini)
            ruta = fh.name
        try:
            _, errs, _ = L.lint_archivo(ruta, self.legit, "7.3a")
            self.assertTrue(any("Bastion of Spirits" in e for e in errs))
        finally:
            os.unlink(ruta)


class TestRefresh(unittest.TestCase):
    TXT = ("""---
champion: Yuumi
---
## 0. RESUMEN

### Resultado del modelo (nivel 15)

| Métrica | Valor |
|---|---|
| Escudo E | **339** |
| Cura R | **651** (+excedente) |
| Escudo/min | ~3 953 |

> Titular dentro de la sección.

---

## 1. CONTEXTO

Texto fuera de la sección con 339 y 651 que NO debe cambiar.
""")

    def test_refresh_reemplaza_en_seccion_y_no_fuera(self):
        delta = {"e_shield": -1.4, "r_heal": -1.4, "shield_per_min": -1.4}
        pre = {"e_shield": 338.8, "r_heal": 650.7, "shield_per_min": 3952.7}
        post = {"e_shield": 334.0, "r_heal": 641.4, "shield_per_min": 3896.2}
        nuevo, cambios = U.refresh_texto(self.TXT, delta, pre, post)
        self.assertTrue(cambios)
        seccion = nuevo.split("## 1. CONTEXTO")[0]
        self.assertIn("**334**", seccion)
        self.assertIn("**641**", seccion)
        self.assertIn("3 896", seccion)                      # espacio de miles preservado
        # dentro de la sección TODO número reproducible se actualiza (incluido el titular)…
        self.assertIn("Titular dentro de la sección.", nuevo)
        self.assertNotIn("339", seccion.split("### Resultado del modelo")[1])
        # …pero fuera de la sección no se toca nada
        self.assertIn("Texto fuera de la sección con 339 y 651 que NO debe cambiar.", nuevo)

    def test_refresh_vault_actual_no_toca_nada(self):
        """En el vault de hoy: Δ 0 (Jinx/Kalista/Diana) o no reproducible 1:1 (Yuumi poke)."""
        reg = U.cargar_registro()
        patch, cs, res = U.triage_todos(reg, patch="7.3a")
        tocables = 0
        for t in res:
            if not t.get("delta") or not any(abs(v) >= 0.05 for v in t["delta"].values()):
                continue
            with open(os.path.join(REP, t["archivo"]), encoding="utf-8") as fh:
                txt = fh.read()
            _, cambios = U.refresh_texto(txt, t["delta"], t["pre"], t["post_cons"])
            tocables += len(cambios)
        self.assertEqual(tocables, 0)


class TestBorrador(unittest.TestCase):
    def test_borradores_73a_existen_y_contienen_datos(self):
        d = os.path.join(REP, "_borradores")
        args = types.SimpleNamespace(patch="7.3a", cmd="borrador")
        import contextlib, io
        with contextlib.redirect_stdout(io.StringIO()):
            U.cmd_borrador(args)                      # idempotente: los regenera
        cat = open(os.path.join(d, "Caitlyn_7.3a_REGENERAR.md"), encoding="utf-8").read()
        ram = open(os.path.join(d, "Rammus_7.3a_REGENERAR.md"), encoding="utf-8").read()
        self.assertIn("BORRADOR DE REGENERACIÓN", cat)
        self.assertIn("AS growth 0.04→0.025", cat)
        self.assertIn("0.025 (7.3a: era 0.04)", cat)          # fila del CSV oficial
        self.assertIn("ESQUELETO DEL REPORTE NUEVO", cat)
        self.assertIn("BORRADOR DE REGENERACIÓN", ram)
        self.assertTrue("45→" in ram or "Armor" in ram)

    def test_baseline_ignora_borradores(self):
        reg = U.construir_registro()
        self.assertNotIn("_borradores", reg["reportes"])
        self.assertEqual(len(reg["reportes"]), 17)


if __name__ == "__main__":
    unittest.main(verbosity=2)
