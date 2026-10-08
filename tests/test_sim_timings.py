# -*- coding: utf-8 -*-
"""
WR-LAB · tests del simulador de timings de oro (model/sim_timings.py).
Las curvas se derivan de las Tablas B del vault — estos tests validan el parseo
(ambos formatos de tabla), la monotonía de las curvas, la predicción leave-one-out
y la ruta nueva (variante anti-tanques de Jinx).
Ejecutar:  python3 -m unittest discover -s tests -v
"""
import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import sim_timings as S

REP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reportes")


def texto(nombre):
    with open(os.path.join(REP, nombre), encoding="utf-8") as fh:
        return fh.read()


class TestParseoRutas(unittest.TestCase):
    def test_jinx_tabla_b_acumulativa(self):
        ruta = S.parse_ruta(texto("Jinx.md"))
        self.assertGreaterEqual(len(ruta), 8)
        self.assertEqual(ruta[0][1], 500)                 # Long Sword start
        self.assertEqual(ruta[0][2], 0.0)
        self.assertEqual(ruta[-1][1], 17350)              # oro total de la build C
        self.assertAlmostEqual(ruta[-1][2], 20.0, delta=1.1)   # v1.5 del autor: ~20:00

    TABLA_B_ACUM = """### Tabla B — Ruta de compra

| # | Compra | Oro acum. | Minuto típico |
|---|---|---|---|
| 1 | Long Sword + Poción | 500 | 0:00 |
| 2 | Berserker's Greaves | 1 700 | ~4:30 |
| 3 | **Nashor's Talons** | 3 400 | ~7:00 |
| 4 | Cierre de build | 14 950 | ~17:30 |
"""

    TABLA_POR_ITEM = """### Tabla B — Ruta

| Compra | Oro | Minuto |
|---|---|---|
| Ítem 1 | 2 900 | 4:00 |
| Ítem 2 | 1 200 | 6:00 |
| Ítem 3 | 1 000 | 7:00 |
| Ítem 4 | 2 650 | 10:00 |
| Ítem 5 | 3 400 | 14:00 |
| Ítem 6 | 3 300 | 17:00 |
"""

    TABLA_SIN_MINUTOS = """### Tabla B — Ruta

| Compra | Oro acum. |
|---|---|
| Ítem 1 | 2 900 |
| Ítem 2 | 4 100 |
"""

    def test_sivir_ruta_por_item_sintetiza_acumulado(self):
        """v1.15.2: fixture sintética (oro POR ÍTEM) — el parser debe acumular.
        Antes atado a la Tabla B de Sivir: cuando el autor la rehízo, rompió."""
        ruta = S.parse_ruta(self.TABLA_POR_ITEM)
        self.assertGreaterEqual(len(ruta), 5)
        oros = [o for _, o, _ in ruta]
        self.assertEqual(max(oros), sum([2900, 1200, 1000, 2650, 3400, 3300]))  # 14 450

    def test_diana_jungla_rango_de_minutos(self):
        """v1.15.2: fixture sintética — ancla de minuto por ítem y oro exactos."""
        ruta = S.parse_ruta(self.TABLA_B_ACUM)
        t_nashor = next(t for c, o, t in ruta if "Nashor" in c and o == 3400)
        self.assertAlmostEqual(t_nashor, 7.0, delta=0.01)

    def test_kalista_sin_minutos_no_aporta_anclas(self):
        """v1.15.2: tabla sin columna de minuto → parse_ruta no inventa anclas."""
        ruta = S.parse_ruta(self.TABLA_SIN_MINUTOS)
        self.assertTrue(all(t is None for _, _, t in ruta) or ruta == [])

    def test_rutas_del_vault_monotonas(self):
        """Invariante real sobre el vault vivo: el oro acumulado de toda Tabla B
        parseada crece monótono (y los minutos también). Aguanta cualquier
        reescritura de guías mientras la tabla sea una ruta cronológica."""
        for f in sorted(os.listdir(REP)):
            if not f.endswith(".md"):
                continue
            ruta = S.parse_ruta(texto(f))
            oros = [o for _, o, _ in ruta]
            # solo el ORO acumulado es monótono: los minutos NO (las filas de
            # upgrade tipo "⬆️ Gunmetal" viven en su slot, no en su minuto)
            self.assertEqual(oros, sorted(oros), f)


class TestCurvas(unittest.TestCase):
    def test_anclas_por_rol(self):
        puntos, detalle, glob = S.anclas_por_rol()
        self.assertGreaterEqual(len(glob), 20)            # el vault aporta anclas de sobra
        self.assertGreaterEqual(len(puntos["adc"]), 3)
        self.assertGreaterEqual(len(puntos["jungla"]), 3)
        self.assertGreaterEqual(len(puntos["support"]), 3)

    def test_curvas_monotonas(self):
        puntos, _, _ = S.anclas_por_rol()
        for rol, pts in puntos.items():
            if not pts:
                continue
            c = S.fit_curva(pts)
            ts = [t for t, _ in c]
            os_ = [o for _, o in c]
            self.assertEqual(ts, sorted(ts), rol)
            self.assertEqual(os_, sorted(os_), rol)

    def test_rol_detection(self):
        self.assertEqual(S.rol_de("Jinx.md", "ADC (Dragon Lane)"), "adc")
        self.assertEqual(S.rol_de("Diana - Jungla.md", "Jungla (preferente) / Mid"), "jungla")
        self.assertEqual(S.rol_de("Cho'Gath - Titán del Barón.md", ""), "top")
        self.assertEqual(S.rol_de("Yuumi.md", "Support (Bot Lane)"), "support")


class TestPrediccion(unittest.TestCase):
    def test_leave_one_out_jinx(self):
        """Sin las anclas de Jinx, la curva ADC predice su pico final (17 350 g) cerca de ~21 min."""
        puntos, _, glob = S.anclas_por_rol(excluir="Jinx.md")
        pts = puntos["adc"] if len(puntos["adc"]) >= 3 else glob
        curva = S.fit_curva(pts)
        t = S.minuto_para(17350, curva)
        self.assertIsNotNone(t)
        self.assertGreaterEqual(t, 17.0)
        self.assertLessEqual(t, 25.0)

    def test_ruta_nueva_variante_antitanques(self):
        """Variante 7.3a (C44+Terminus+YunTal+IE+LDR, upgrade Gunmetal): 17 900 g acumulados,
        tiempos crecientes y pico final razonable."""
        puntos, _, glob = S.anclas_por_rol()
        curva = S.fit_curva(puntos["adc"] if len(puntos["adc"]) >= 3 else glob)
        items = ["Berserker's Greaves", "Hexoptics C44", "Terminus", "Yun Tal", "Infinity Edge",
                 "Lord Dominik's Regards"]
        acum, t_ant, filas = 0, 0.0, []
        for it in items:
            g = S.precio(it)
            self.assertIsNotNone(g, it)
            acum += g
            t = max(S.minuto_para(acum, curva) or 0, t_ant)
            filas.append((it, acum, t))
            t_ant = t
        acum += 1000                                       # ⬆️ Gunmetal (mismo slot, min ≥10)
        t_fin = max(S.minuto_para(acum, curva) or 0, t_ant, 10.0)
        self.assertEqual(acum, 17900)
        ts = [t for _, _, t in filas] + [t_fin]
        self.assertEqual(ts, sorted(ts))                   # monótono
        self.assertGreaterEqual(t_fin, 19.0)
        self.assertLessEqual(t_fin, 26.0)

    def test_precio_desde_el_motor(self):
        self.assertEqual(S.precio("Hexoptics C44"), 2900)
        self.assertEqual(S.precio("Yun Tal"), 3100)
        self.assertEqual(S.precio("Gunmetal Greaves"), 2200)


if __name__ == "__main__":
    unittest.main(verbosity=2)
