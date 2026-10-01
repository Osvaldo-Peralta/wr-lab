# -*- coding: utf-8 -*-
"""
WR-LAB · tests de win rates (model/check_patch.py paso 4 + integraciones v1.11).
Cubren: parser del bloque Meta Overview (fixture sintético + snapshot real commiteado),
CSV/MD deterministas, umbral de drift, actualizar_winrates() con red simulada
(monkeypatch, sin llamadas reales), lint del callout meta, menú/CLI y §7b del bundle.
Ejecutar:  python3 -m unittest discover -s tests -v
"""
import csv, io, json, os, re, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "model"))
import check_patch as CP

FIXTURE = """<html><body>
<div id="wrCnFsSnapWrap">
  <div class="wr-cn-fs">
  <div class="wr-cn-fs-sub">
    <select class='wr-cn-fs-bucket-select'><option value="1" selected>Diamond +</option><option value="2">Master +</option></select>
    <span class="wr-cn-fs-src">Updated: <b>01 OCT 2026 UTC 00:00</b></span>
  </div>
  <div id="wrCnFsBox"><div class='wr-cn-fs-carousel' data-count='2'><div class='wr-cn-fs-viewport'><div class='wr-cn-fs-track'>
      <div class='wr-cn-fs-slide'>
        <div class='wr-cn-fs-row'>
          <div class='wr-cn-fs-row-head'>
            <div class='wr-cn-fs-role'><i class="demo-icon support-duoicon-"></i><span>SUPPORT</span></div>
            <div class='wr-cn-fs-tier'><img class="wr-tier-ico" src="/t/B.svg" alt="B"><span class='wr-badge wr-conf-high'>Confidence High</span></div>
          </div>
          <div class='wr-cn-fs-metrics'>
            <div class='wr-cn-fs-m'><span class='k'>Win:</span> <span class='v text-green'>52.10%</span></div>
            <div class='wr-cn-fs-m'><span class='k'>Pick:</span> <span class='v'>9.10%</span></div>
            <div class='wr-cn-fs-m'><span class='k'>Ban:</span> <span class='v text-red'>30.00%</span></div>
            <div class='wr-cn-fs-m'><span class='k'>Trend:</span> <span class='v'><span class='wr-cn-trend wr-trend-up'>↑ 3</span></span></div>
          </div>
        </div>
      </div>
      <div class='wr-cn-fs-slide'>
        <div class='wr-cn-fs-row'>
          <div class='wr-cn-fs-row-head'>
            <div class='wr-cn-fs-role'><i class="demo-icon mid-icon-"></i><span>mid</span></div>
            <div class='wr-cn-fs-tier'><img class="wr-tier-ico" src="/t/A.svg" alt="A"><span class='wr-badge wr-conf-medium'>Confidence Medium</span></div>
          </div>
          <div class='wr-cn-fs-metrics'>
            <div class='wr-cn-fs-m'><span class='k'>Win:</span> <span class='v'>47.55%</span></div>
            <div class='wr-cn-fs-m'><span class='k'>Pick:</span> <span class='v'>2.20%</span></div>
            <div class='wr-cn-fs-m'><span class='k'>Ban:</span> <span class='v'>5.00%</span></div>
            <div class='wr-cn-fs-m'><span class='k'>Trend:</span> <span class='v'><span class='wr-cn-trend wr-trend-down'>↓ 2</span></span></div>
          </div>
        </div>
      </div>
  </div></div></div>
</div>
</body></html>"""


class TestParserWinrates(unittest.TestCase):
    def test_fixture_dos_roles(self):
        rows = CP.parsear_winrates("yuumi", FIXTURE.encode("utf-8"))
        self.assertEqual(len(rows), 2)
        r = rows[0]
        self.assertEqual((r["champion"], r["role"], r["tier"]), ("Yuumi", "SUPPORT", "B"))
        self.assertEqual(r["win_pct"], "52.10")
        self.assertEqual(r["pick_pct"], "9.10")
        self.assertEqual(r["ban_pct"], "30.00")
        self.assertEqual(r["trend"], "↑ 3")
        self.assertEqual(r["confidence"], "Confidence High")
        self.assertEqual(r["bucket"], "Diamond +")
        self.assertEqual(r["updated_utc"], "01 OCT 2026 UTC 00:00")
        self.assertEqual((rows[1]["role"], rows[1]["win_pct"], rows[1]["tier"]),
                         ("MID", "47.55", "A"))

    def test_display_chogath(self):
        rows = CP.parsear_winrates("chogath", FIXTURE.encode("utf-8"))
        self.assertEqual(rows[0]["champion"], "Cho'Gath")

    def test_snapshot_real_committeado(self):
        """El snapshot de Cho'Gath (data/raw/campeones/) tiene SOLO+JUNGLE con los
        números que citan sus reportes (51.20/50.78 al 24-sep)."""
        ruta = os.path.join(ROOT, "data", "raw", "campeones", "chogath.html")
        if not os.path.exists(ruta):
            self.skipTest("snapshot raw no presente")
        rows = CP.parsear_winrates("chogath", open(ruta, "rb").read())
        self.assertEqual([r["role"] for r in rows], ["SOLO", "JUNGLE"])
        for r in rows:
            self.assertTrue(0.0 < float(r["win_pct"]) < 100.0)
            self.assertTrue(r["tier"])
            self.assertIn("2026", r["updated_utc"])
        self.assertEqual({r["win_pct"] for r in rows}, {"51.20", "50.78"})

    def test_sin_bloque_devuelve_vacio(self):
        self.assertEqual(CP.parsear_winrates("x", b"<html>sin widget</html>"), [])


class TestSalidas(unittest.TestCase):
    def setUp(self):
        self.filas = CP.parsear_winrates("yuumi", FIXTURE.encode("utf-8"))
        for f in self.filas:
            f["actualizado"] = "2026-10-01"

    def test_csv_determinista_y_crlf(self):
        t1 = CP.winrates_csv_text(self.filas)
        self.assertEqual(t1, CP.winrates_csv_text(self.filas))
        self.assertIn("\r\n", t1)                        # como el resto de CSVs del lab
        rows = list(csv.DictReader(io.StringIO(t1)))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["champion"], "Yuumi")
        self.assertEqual(rows[1]["role"], "MID")
        self.assertEqual(rows[0]["actualizado"], "2026-10-01")

    def test_md_con_tabla_y_leyenda_de_roles(self):
        md = CP.winrates_md_text(self.filas)
        self.assertIn("# Win rates del roster", md)
        self.assertIn("| Yuumi | SUPPORT | B | 52.10 |", md)
        self.assertIn("SOLO = top", md)
        self.assertIn("champion_winrates.csv", md)
        self.assertEqual(CP.winrates_md_text([]), "")


class TestDrift(unittest.TestCase):
    def fila(self, champ, role, win):
        return {"champion": champ, "role": role, "win_pct": win, "bucket": "Diamond +"}

    def test_delta_mayor_umbral_alerta(self):
        f = self.deltas([self.fila("Jinx", "DUO", "50.55")], {"Jinx|DUO": 48.0})
        self.assertEqual(len(f), 1)
        self.assertIn("WIN RATE Jinx (DUO", f[0])
        self.assertIn("+2.55", f[0])

    def test_delta_menor_umbral_no_alerta(self):
        self.assertEqual(self.deltas([self.fila("Jinx", "DUO", "50.55")], {"Jinx|DUO": 49.8}), [])

    def test_campeon_nuevo_no_alerta(self):
        self.assertEqual(self.deltas([self.fila("Norra", "MID", "49.0")], {}), [])

    def deltas(self, filas, prev):
        return CP.deltas_winrate(filas, prev)


class TestActualizarWinrates(unittest.TestCase):
    """Integración con red simulada: monkeypatch de CP.get + rutas a tmpdir."""

    @classmethod
    def setUpClass(cls):
        cls._get, cls._pausa = CP.get, CP.PAUSA_ENTRE_PETICIONES
        cls._csv, cls._md = CP.WINRATES_CSV, CP.WINRATES_MD
        CP.PAUSA_ENTRE_PETICIONES = 0

    @classmethod
    def tearDownClass(cls):
        CP.get, CP.PAUSA_ENTRE_PETICIONES = cls._get, cls._pausa
        CP.WINRATES_CSV, CP.WINRATES_MD = cls._csv, cls._md

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        CP.WINRATES_CSV = os.path.join(self.tmp.name, "champion_winrates.csv")
        CP.WINRATES_MD = os.path.join(self.tmp.name, "champion_winrates.md")
        self.paginas = 0
        def fake_get(url, t=25):
            if "sitemap.xml" in url:
                return 200, b"<urlset><loc>https://wr-meta.com/999-faker.html</loc></urlset>"
            self.paginas += 1
            return 200, FIXTURE.encode("utf-8")
        CP.get = fake_get

    def tearDown(self):
        CP.get = self._get
        self.tmp.cleanup()

    def _run(self, state):
        findings = []
        n_ch, n_filas = CP.actualizar_winrates(state, findings, quiet=True)
        return state, findings, n_ch, n_filas

    def test_escribe_csv_md_y_state(self):
        state = {"winrates": {}, "wrmeta_ids": {}}
        state, findings, n_ch, n_filas = self._run(state)
        self.assertGreaterEqual(n_ch, 17)             # roster + campeones del registro
        self.assertEqual(n_filas, n_ch * 2)           # 2 roles por campeón (fixture)
        self.assertTrue(os.path.exists(CP.WINRATES_CSV))
        self.assertTrue(os.path.exists(CP.WINRATES_MD))
        rows = list(csv.DictReader(open(CP.WINRATES_CSV, encoding="utf-8")))
        self.assertEqual(len(rows), n_filas)
        self.assertEqual(findings, [])                # primera siembra: sin alertas
        self.assertIn("Jinx|SUPPORT", state["winrates"])
        self.assertEqual(state["winrates_meta"]["bucket"], "Diamond +")

    def test_idempotente_sin_datos_nuevos(self):
        state = {"winrates": {}, "wrmeta_ids": {}}
        self._run(state)
        antes_csv = open(CP.WINRATES_CSV, "rb").read()
        antes_md = open(CP.WINRATES_MD, "rb").read()
        state2 = {"winrates": dict(state["winrates"]), "wrmeta_ids": {}}
        _, findings, _, _ = self._run(state2)
        self.assertEqual(open(CP.WINRATES_CSV, "rb").read(), antes_csv)   # sin reescritura
        self.assertEqual(open(CP.WINRATES_MD, "rb").read(), antes_md)
        self.assertEqual(findings, [])

    def test_drift_genera_finding_sin_reescribir_si_valores_iguales(self):
        state = {"winrates": {}, "wrmeta_ids": {}}
        self._run(state)
        antes = open(CP.WINRATES_CSV, "rb").read()
        state["winrates"]["Jinx|SUPPORT"] = 40.0      # simula un salto de +12.1 pts
        _, findings, _, _ = self._run(state)
        self.assertTrue(any("WIN RATE Jinx (SUPPORT" in f for f in findings))
        # la fixture no cambió → el CSV NO se reescribe (el finding sale del state,
        # y el archivo solo se toca cuando los valores reales difieren)
        self.assertEqual(open(CP.WINRATES_CSV, "rb").read(), antes)

    def test_roster_incluye_registro(self):
        roster = CP.roster_winrates()
        for c in ("jinx", "caitlyn", "norra", "chogath", "malphite"):
            self.assertIn(c, roster)

    def test_ids_conocidos_cubren_roster(self):
        self.assertEqual([c for c in CP.roster_winrates() if c not in CP.WRMETA_IDS], [])


class TestIntegracionLab(unittest.TestCase):
    def test_wrlab_expone_winrates(self):
        sys.path.insert(0, ROOT)
        import wrlab
        self.assertIn("winrates", wrlab.COMANDOS)
        etiquetas = [lbl for lbl, _ in wrlab.acciones_planas()]
        self.assertTrue(any("win rates" in e.lower() for e in etiquetas))
        self.assertEqual(len(etiquetas), len(set(etiquetas)))

    def test_bundle_lleva_seccion_7b(self):
        import build_bundles as BB
        if not os.path.exists(os.path.join(ROOT, "data", "estructurada", "champion_winrates.csv")):
            self.skipTest("win rates aún no sembradas (corre: wrlab.py winrates)")
        for kind in ("LITE", "COMPLETO"):
            txt = BB.generar(kind)
            self.assertIn("## 7b. WIN RATES DEL ROSTER", txt)
            self.assertIn("| Campeón | Rol | Tier | Win % |", txt)
            problemas, n_as, n_items, _ = BB.validar(txt, kind)
            self.assertEqual(problemas, [])
            self.assertEqual((n_as, n_items), (140, 186))

    def test_lint_avisa_callout_desactualizado(self):
        import lint_reportes as L
        ruta_csv = os.path.join(ROOT, "data", "estructurada", "champion_winrates.csv")
        if not os.path.exists(ruta_csv):
            self.skipTest("win rates aún no sembradas")
        with open(ruta_csv, encoding="utf-8", newline="") as fh:
            jinx = [r for r in csv.DictReader(fh) if r["champion"] == "Jinx"]
        self.assertTrue(jinx)
        actual = float(jinx[0]["win_pct"])
        legit = L.nombres_items_oficiales()
        plantilla = """---
tags:
  - Test
version: 1
Status: Beta
---
**Fecha del análisis:** 01/10/2026
**Parche:** 7.3a (29-sep-2026)
**Rol principal:** ADC (Dragon Lane)

> [!NOTE]
> **Estado Meta Actual (Diamond+, 01/10/2026):**
> Win Rate {wr} % | Pick Rate 10.00 % | Ban 1.00 %

### Tabla A — BUILD FINAL
| Slot | Ítem | Oro | Rol |
|---|---|---|---|
| 1 (botas) | **Berserker's Greaves → ⬆️ Gunmetal Greaves** | 2 200 | x |
| 2 | **Hexoptics C44** | 2 900 | x |
| 3 | **Infinity Edge** | 3 400 | x |
| 4 | **Lord Dominik's Regards** | 3 300 | x |
| 5 | **Rapid Firecannon** | 2 650 | x |
| 6 | **Bloodthirster** | 3 200 | x |

## 0. RESUMEN
"""
        with tempfile.TemporaryDirectory() as d:
            # desactualizado a propósito (−15 pts) → aviso
            p1 = os.path.join(d, "Jinx.md")
            open(p1, "w", encoding="utf-8").write(plantilla.format(wr=f"{actual - 15:.2f}"))
            _, errs, avis = L.lint_archivo(p1, legit, "7.3a")
            self.assertEqual(errs, [])
            self.assertTrue(any("callout meta desactualizado" in a for a in avis), avis)
            # al día (±0.5 pts) → sin ese aviso
            p2 = os.path.join(d, "Jinx.md")
            open(p2, "w", encoding="utf-8").write(plantilla.format(wr=f"{actual + 0.5:.2f}"))
            _, errs2, avis2 = L.lint_archivo(p2, legit, "7.3a")
            self.assertEqual(errs2, [])
            self.assertFalse(any("callout meta desactualizado" in a for a in avis2), avis2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
