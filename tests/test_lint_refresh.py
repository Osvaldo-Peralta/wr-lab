# -*- coding: utf-8 -*-
"""
WR-LAB · tests de las herramientas de calidad de reportes:
linter (model/lint_reportes.py), refresh y borrador (update_reports.py).
Ejecutar:  python3 -m unittest discover -s tests -v
"""
import os, re, sys, types, unittest
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

    MINI_SIN_TABLA = """---
tags:
  - Test
version: 1
Status: Beta
champion: Prueba
slug: prueba
role: mid
patch: "7.3"
---
**Fecha del análisis:** 01/10/2026
**Parche:** 7.3 (21-sep-2026)
**Rol principal:** Mid

## 0. RESUMEN
Build narrada en prosa, sin tabla de 6 slots reconocible.
"""

    MINI_SITUACIONAL = """---
tags:
  - Test
version: 1
Status: Beta
champion: Prueba
slug: prueba2
role: support
patch: "7.3"
---
**Fecha del análisis:** 01/10/2026
**Parche:** 7.3 (21-sep-2026)
**Rol principal:** Support

### Tabla A — BUILD FINAL

| Slot | Ítem | Oro | Rol |
|---|---|---|---|
| 1 (botas) | **Ionian Boots → ⬆️ Crimson Lucidity** | 1 000 | x |
| 2 | **Ardent Censer** | 2 400 | x |
| 3 | **Echoes of Helia** | 2 400 | x |
| 4 | **Staff of Flowing Waters** | 2 400 | x |
| 5 | **Redemption** | 2 450 | x |
| 6 | **Guardian Angel (situacional)** | 3 000 | x |

## 0. RESUMEN
"""

    def _lint_texto(self, txt):
        """v1.15.2: los estándares del linter se prueban con fixtures sintéticas,
        no con guías del vault (antes Heimerdinger/Sivir: cuando el autor las
        corregía, el test rompía por mejorar el contenido)."""
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8") as fh:
            fh.write(txt)
            ruta = fh.name
        try:
            return L.lint_archivo(ruta, self.legit, "7.3a")
        finally:
            os.unlink(ruta)

    def test_build_no_extraible_es_error(self):
        _, errs, _ = self._lint_texto(self.MINI_SIN_TABLA)
        self.assertTrue(any("no extraíble" in e for e in errs))

    def test_slot_situacional_es_aviso_no_error(self):
        _, errs, avis = self._lint_texto(self.MINI_SITUACIONAL)
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
    """v1.15.2: el comportamiento de cmd_borrador se prueba con un vault
    sintético (fixture histórica de Rammus pre-7.3a, que sí triagea REGENERAR)
    y contra el vault real con esperado DERIVADO del triage actual — nunca con
    listas congeladas (Rammus se corrigió y el test rompía por eso)."""

    FIX = os.path.join(ROOT, "tests", "fixtures", "Rammus_pre73a.md")

    def _correr_en(self, rep_dir, reg_path):
        import shutil, contextlib, io, types, json
        viejos = (U.REPORTES, U.REGISTRY)
        U.REPORTES, U.REGISTRY = rep_dir, reg_path
        try:
            reg = U.construir_registro()
            with open(reg_path, "w", encoding="utf-8") as fh:
                json.dump(reg, fh, ensure_ascii=False)
            with contextlib.redirect_stdout(io.StringIO()):
                U.cmd_borrador(types.SimpleNamespace(patch="7.3a", cmd="borrador"))
            return sorted(os.listdir(os.path.join(rep_dir, "_borradores")))
        finally:
            U.REPORTES, U.REGISTRY = viejos

    def test_sintetico_regenerar_genera_esqueleto(self):
        import tempfile, shutil
        tmp = tempfile.mkdtemp(prefix="wrlab-borr-")
        try:
            shutil.copy(self.FIX, os.path.join(tmp, "Rammus.md"))
            archivos = self._correr_en(tmp, os.path.join(tmp, "reg.json"))
            self.assertEqual(archivos, ["Rammus_7.3a_REGENERAR.md"])
            ram = open(os.path.join(tmp, "_borradores", archivos[0]), encoding="utf-8").read()
            self.assertIn("BORRADOR DE REGENERACIÓN", ram)
            self.assertIn("ESQUELETO DEL REPORTE NUEVO", ram)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_vault_genera_solo_lo_pendiente(self):
        import shutil
        reg = U.construir_registro()
        _, _, res = U.triage_todos(reg, patch="7.3a")
        esperados = sorted(
            re.sub(r"\.md$", "", t["archivo"]).replace(" ", "_") + "_7.3a_REGENERAR.md"
            for t in res if t["veredicto"] == "REGENERAR")
        d = os.path.join(REP, "_borradores")
        shutil.rmtree(d, ignore_errors=True)
        import tempfile
        tmpreg = os.path.join(tempfile.mkdtemp(prefix="wrlab-reg-"), "reg.json")
        try:
            # NUNCA tocar el REGISTRY real: el construido carece de metricas/
            # ultima_verificacion y dejaría el vault "sin verificar" (incidente 08/10)
            archivos = self._correr_en(REP, tmpreg)
            self.assertEqual(archivos, esperados)
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def test_baseline_ignora_borradores(self):
        reg = U.construir_registro()
        self.assertNotIn("_borradores", reg["reportes"])
        self.assertNotIn("_auto", reg["reportes"])
        # v1.15.2: el tamaño lo dicta el directorio (el vault crece con guías nuevas)
        n_md = len([f for f in os.listdir(REP) if f.endswith(".md")])
        self.assertEqual(len(reg["reportes"]), n_md)


if __name__ == "__main__":
    unittest.main(verbosity=2)
