# -*- coding: utf-8 -*-
"""
WR-LAB · tests del CLI unificado + menú (wrlab.py).
Validan el registro de acciones (escalabilidad), el render del menú y el cableado
de extremo a extremo con un par de smoke-tests por subprocess.
Ejecutar:  python3 -m unittest discover -s tests -v
"""
import os, subprocess, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import wrlab


class TestRegistroMenu(unittest.TestCase):
    def test_estructura_bien_formada(self):
        flat = wrlab.acciones_planas()
        self.assertGreaterEqual(len(flat), 12)
        etiquetas = [lbl for lbl, _ in flat]
        self.assertEqual(len(etiquetas), len(set(etiquetas)), "etiquetas duplicadas en el menú")
        for lbl, fn in flat:
            self.assertTrue(callable(fn), lbl)
            self.assertTrue(lbl.strip())

    def test_menu_texto_renderiza(self):
        t = wrlab.menu_texto()
        for seccion in ("ESTADO", "CICLO DE HOTFIX", "ANÁLISIS", "ARTEFACTOS"):
            self.assertIn(seccion, t)
        self.assertIn("0. Salir", t)

    def test_comandos_no_interactivos_cubren_el_ciclo(self):
        for cmd in ("estado", "watch", "hotfix", "triage", "refresh", "borrador",
                    "annotate", "baseline", "optimize", "runes", "timings", "lint",
                    "tests", "bundles", "db", "motor", "git", "menu"):
            self.assertIn(cmd, wrlab.COMANDOS, cmd)


class TestSmokeSubprocess(unittest.TestCase):
    def _wrlab(self, *args, stdin=""):
        return subprocess.run([sys.executable, os.path.join(ROOT, "wrlab.py"), *args],
                              cwd=ROOT, input=stdin, capture_output=True, text=True, timeout=180)

    def test_sin_args_y_sin_tty_no_cuelga(self):
        r = self._wrlab()
        self.assertEqual(r.returncode, 0)
        self.assertIn("stdin no es una terminal", r.stdout)

    def test_comando_desconocido_da_usage(self):
        r = self._wrlab("inexistente")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("comando desconocido", r.stderr + r.stdout)

    def test_estado_extremo_a_extremo(self):
        """'estado' encadena update_reports check + bundles --check + lint → todo en verde."""
        r = self._wrlab("estado")
        self.assertEqual(r.returncode, 0, r.stdout[-2000:])
        self.assertIn("TODO EN ORDEN", r.stdout)

    def test_lint_solo_un_archivo(self):
        r = self._wrlab("lint", "--solo", "Jinx.md")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Jinx.md", r.stdout)

    def test_menu_in_process_selecciona_accion_y_sale(self):
        """Menú driveado in-process: elige la acción 'Motor de DPS — demo Jinx', vuelve y sale."""
        import builtins, contextlib, io
        from unittest import mock
        flat = wrlab.acciones_planas()
        idx = next(i for i, (lbl, _) in enumerate(flat, 1) if "Motor de DPS" in lbl)
        respuestas = iter([str(idx), "", "0"])           # acción → Enter (volver) → salir
        buf = io.StringIO()
        with mock.patch.object(builtins, "input", lambda *_: next(respuestas)), \
                contextlib.redirect_stdout(buf):
            rc = wrlab.menu()
        out = buf.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("Motor de DPS", out)                 # la acción se lanzó desde el menú
        self.assertGreaterEqual(out.count("menú principal"), 2)  # …y el bucle volvió a pintar el menú


if __name__ == "__main__":
    unittest.main(verbosity=2)
