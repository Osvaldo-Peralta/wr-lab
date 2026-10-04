# -*- coding: utf-8 -*-
"""WR-LAB · tests de exclusividades de ítems (Ley 3b · items_exclusivos.csv).
Fuente de la regla: verificación en juego del autor (03/10/2026) — LDR, Mortal Reminder
y Terminus no pueden convivir. El registro es escalable: estos tests validan el mecanismo,
no solo el grupo actual."""
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import dps_model as M
import optimize_build as O


class TestRegistro(unittest.TestCase):
    def test_grupo_pen_pct_cargado(self):
        grupos = dict(M.EXCLUSIVIDAD)
        self.assertIn("pen_pct", grupos)
        self.assertEqual(grupos["pen_pct"], {"ldr", "mortal", "terminus"})

    def test_csv_formato_escalable(self):
        import csv
        ruta = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "data", "estructurada", "items_exclusivos.csv")
        with open(ruta, encoding="utf-8", newline="") as fh:
            filas = list(csv.DictReader(fh))
        self.assertEqual(set(filas[0].keys()), {"grupo", "items", "fuente", "verificado"})
        self.assertTrue(all(f["fuente"] for f in filas))     # toda regla cita su fuente


class TestValidador(unittest.TestCase):
    def test_pares_ilegales_rechazados(self):
        for ilegal in (["Gunmetal", "C44", "Runaan's", "IE", "LDR", "Terminus"],
                       ["Gunmetal", "C44", "Runaan's", "IE", "Mortal Reminder", "Terminus"],
                       ["Gunmetal", "C44", "LDR", "Mortal Reminder", "Kraken", "IE"]):
            with self.assertRaises(ValueError, msg=str(ilegal)):
                M.validate_slots(ilegal)

    def test_legales_aceptadas(self):
        self.assertEqual(M.validate_slots(["Gunmetal", "C44", "Runaan's", "IE", "LDR", "Kraken"]), (1, 5))
        self.assertEqual(M.validate_slots(["Gunmetal", "C44", "Runaan's", "IE", "Terminus", "Kraken"]), (1, 5))

    def test_claves_batch2_toleradas(self):
        v = M.violaciones_exclusividad(["Gunmetal", "Terminus", "LDR", "Guinsoo", "BotRK", "Runaan"])
        self.assertEqual(v[0][0], "pen_pct")


class TestOptimizadorLimpio(unittest.TestCase):
    def test_jinx_pool_completo_sin_pares_ilegales(self):
        finales, _ = O.optimizar("jinx", top=8, crit_min=100, pen_min=30, verbose=False)
        for f in finales:
            self.assertEqual(M.violaciones_exclusividad(f[1]), [], f[1])

    def test_kalista_sin_terminus_mas_ldr(self):
        finales, _ = O.optimizar("kalista", top=6, verbose=False)
        for f in finales:
            claves = {c.lower() for c in f[1]}
            self.assertFalse({"terminus", "ldr"} <= claves, f[1])

    def test_golden_C_intacta(self):
        """La build C publicada (un solo ítem de pen) no se afecta."""
        r = M.eval_build(M.CHAMPS["jinx"], ["Gunmetal", "C44", "Runaan's", "IE", "LDR", "Kraken"])
        self.assertEqual(round(r["dps1"]), 3042)


class TestLint(unittest.TestCase):
    def test_build_ilegal_es_error(self):
        import lint_reportes as L
        import tempfile
        mini = """---
tags:
  - ADC
version: 1
Status: Beta
---
**Parche:** 7.3

### Tabla A — BUILD FINAL

| Slot | Ítem | Oro | Rol |
|---|---|---|---|
| 1 (botas) | **Berserker's Greaves → ⬆️ Gunmetal Greaves** | 2 200 | x |
| 2 | **Hexoptics C44** | 2 900 | x |
| 3 | **Infinity Edge** | 3 400 | x |
| 4 | **Lord Dominik's Regards** | 3 300 | x |
| 5 | **Terminus** | 3 000 | x |
| 6 | **Kraken Slayer** | 2 900 | x |

## 0. RESUMEN
"""
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as fh:
            fh.write(mini)
            ruta = fh.name
        try:
            _, errs, _ = L.lint_archivo(ruta, L.nombres_items_oficiales(), "7.3a")
            self.assertTrue(any("exclusividad" in e for e in errs), errs)
        finally:
            os.unlink(ruta)


if __name__ == "__main__":
    unittest.main(verbosity=2)
