# -*- coding: utf-8 -*-
"""WR-LAB · tests de model/runas_wr.py — la legalidad de runas WR como estándar (v1.21).

Reglas confirmadas in-game por el autor (18/10/2026):
  L1 = 1 keystone + 3 runas + 1 secundaria (5 slots exactos).
  L2 = las 3 runas son del ÁRBOL DEL KEYSTONE, una por cada fila (1, 2 y 3).
  L3 = ≤1 runa por fila dentro del árbol principal (contenida en L2).
  L4 = la secundaria es de CUALQUIER OTRO árbol, nunca del principal.

Los sets-spec son los ejemplos reales del autor: páginas legales publicadas
(Yuumi agresiva = Aery + Manaflow Band + Transcendence + Scorch | Revitalize;
Jinx = Lethal Tempo + Brutal + Legend: Alacrity + Cut Down | Bone Plating),
secundarias alternativas legales (Sudden Impact / Cut Down / Second Wind en vez
de Revitalize) e ilegales (el set del motor batch5 v1.20 —runas de 3 árboles—;
secundaria del árbol principal; fila repetida; 4 y 6 slots; runas removidas).
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import runas_wr as R

YUUMI_PUBLICADA = ["Aery", "Manaflow Band", "Transcendence", "Scorch", "Revitalize"]
MOTOR_BATCH5_V120 = ["Electrocute", "Cheap Shot", "Transcendence", "Coup de Grace", "Gathering Storm"]


class TestSetsSpec(unittest.TestCase):
    def test_yuumi_publicada_legal(self):
        """La build publicada de Yuumi agresiva (autor, in-game): LEGAL."""
        ok, motivos = R.es_legal_pagina(YUUMI_PUBLICADA)
        self.assertTrue(ok, motivos)
        # alias del md antiguo
        ok2, m2 = R.es_legal_pagina(["Summon Aery", "Manaflow Band", "Transcendence", "Scorch", "Revitalize"])
        self.assertTrue(ok2, m2)

    def test_yuumi_variantes_de_fila_legal(self):
        """Cualquier opción de cada fila Sorcery mantiene la página legal."""
        for f1 in ("Axiom Arcanist", "Botanist", "Hexflash"):
            ok, motivos = R.es_legal_pagina(["Aery", f1, "Transcendence", "Scorch", "Revitalize"])
            self.assertTrue(ok, (f1, motivos))
        ok, motivos = R.es_legal_pagina(["Aery", "Hexflash", "Celerity", "Ixtali Seedjar", "Perseverance"])
        self.assertTrue(ok, motivos)

    def test_jinx_publicada_legal(self):
        ok, motivos = R.es_legal_pagina(
            ["Lethal Tempo", "Brutal", "Legend: Alacrity", "Cut Down", "Bone Plating"])
        self.assertTrue(ok, motivos)

    def test_secundaria_de_cualquier_otro_arbol_legal(self):
        """Ejemplos textuales del autor: en lugar de Revitalize pueden ser
        Sudden Impact (Domination), Cut Down (Precision) o Second Wind (Resolve)."""
        for sec in ("Sudden Impact", "Cut Down", "Second Wind", "Revitalize", "Triumph", "Overgrowth"):
            pagina = YUUMI_PUBLICADA[:4] + [sec]
            ok, motivos = R.es_legal_pagina(pagina)
            self.assertTrue(ok, (sec, motivos))

    def test_motor_batch5_v120_ilegal(self):
        """CORRECCIÓN 18/10: el set del motor batch5 (dado 'legal' por la DB v1.20)
        viola L2 — Transcendence (Sorcery) y Coup de Grace (Precision) no son del
        árbol del keystone Electrocute (Domination)."""
        ok, motivos = R.es_legal_pagina(MOTOR_BATCH5_V120)
        self.assertFalse(ok)
        self.assertTrue(any("L2" in m for m in motivos), motivos)

    def test_electrocute_con_secundaria_del_keystone_ilegal(self):
        ok, motivos = R.es_legal_pagina(
            ["Electrocute", "Axiom Arcanist", "Transcendence", "Gathering Storm", "Cheap Shot"])
        self.assertFalse(ok)
        self.assertTrue(any("L2" in m for m in motivos), motivos)
        self.assertTrue(any("L4" in m for m in motivos), motivos)

    def test_secundaria_del_arbol_principal_ilegal(self):
        """Gathering Storm es Sorcery f3 (no Inspiration como decía la DB v1.20):
        con keystone Aery viola L4."""
        ok, motivos = R.es_legal_pagina(["Aery", "Manaflow Band", "Transcendence", "Scorch", "Gathering Storm"])
        self.assertFalse(ok)
        self.assertTrue(any("L4" in m for m in motivos), motivos)

    def test_fila_repetida_en_arbol_principal_ilegal(self):
        ok, motivos = R.es_legal_pagina(["Aery", "Manaflow Band", "Axiom Arcanist", "Transcendence", "Revitalize"])
        self.assertFalse(ok)
        self.assertTrue(any("L2" in m or "L3" in m for m in motivos), motivos)

    def test_dos_resolve_dos_sorcery_ilegal(self):
        ok, motivos = R.es_legal_pagina(
            ["Grasp of the Undying", "Bone Plating", "Overgrowth", "Manaflow Band", "Scorch"])
        self.assertFalse(ok)  # Manaflow Band (Sorcery) entre las 3 runas de Resolve: L2
        self.assertTrue(any("L2" in m for m in motivos), motivos)

    def test_cuatro_slots_ilegal(self):
        """La lectura que originó el caos v1.20: la ficha del autor lista las
        OPCIONES de cada fila; los slots reales son 5, no 4 ni 6."""
        ok, motivos = R.es_legal_pagina(["Summon Aery", "Manaflow Band", "Scorch", "Revitalize"])
        self.assertFalse(ok)
        self.assertTrue(any("L1" in m for m in motivos), motivos)

    def test_chogath_seis_runas_ilegal(self):
        """Deuda conocida de los reportes tanque (6 slots): se corrige en otra iteración."""
        ok, motivos = R.es_legal_pagina(
            ["Grasp of the Undying", "Demolish", "Second Wind", "Overgrowth",
             "Transcendence", "Axiom Arcanist"])
        self.assertFalse(ok)
        self.assertTrue(any("L1" in m for m in motivos), motivos)


class TestReglas(unittest.TestCase):
    def test_control_legal(self):
        ok, motivos = R.es_legal(
            "Lethal Tempo", ["Brutal", "Legend: Alacrity", "Cut Down"], "Bone Plating")
        self.assertTrue(ok, motivos)

    def test_filas_1_1_2_ilegal(self):
        ok, motivos = R.es_legal(
            "Lethal Tempo", ["Brutal", "Triumph", "Cut Down"], "Bone Plating")
        self.assertFalse(ok)  # Brutal y Triumph: Precision f1 ×2 → filas [1,1,2]
        self.assertTrue(any("L2" in m for m in motivos), motivos)

    def test_pagina_domination_completa_legal(self):
        ok, motivos = R.es_legal(
            "Electrocute", ["Cheap Shot", "Tyrant", "Relentless Hunter"], "Transcendence")
        self.assertTrue(ok, motivos)

    def test_runa_removida_ilegal(self):
        ok, motivos = R.es_legal_pagina(
            ["Electrocute", "Cheap Shot", "Tyrant", "Ingenious Hunter", "Transcendence"])
        self.assertFalse(ok)
        self.assertTrue(any("L1" in m for m in motivos), motivos)


class TestDB(unittest.TestCase):
    """La DB replica el layout in-game confirmado por el autor (18/10)."""

    def test_filas_sorcery_confirmadas(self):
        self.assertEqual(R.ficha("Aery"), ("Sorcery", 0))
        self.assertEqual(R.ficha("Axiom Arcanist"), ("Sorcery", 1))
        self.assertEqual(R.ficha("Manaflow Band"), ("Sorcery", 1))
        self.assertEqual(R.ficha("Botanist"), ("Sorcery", 1))
        self.assertEqual(R.ficha("Hexflash"), ("Sorcery", 1))
        self.assertEqual(R.ficha("Transcendence"), ("Sorcery", 2))
        self.assertEqual(R.ficha("Celerity"), ("Sorcery", 2))
        self.assertEqual(R.ficha("Absolute Focus"), ("Sorcery", 2))
        self.assertEqual(R.ficha("Scorch"), ("Sorcery", 3))
        self.assertEqual(R.ficha("Nimbus Cloak"), ("Sorcery", 3))
        self.assertEqual(R.ficha("Gathering Storm"), ("Sorcery", 3))
        self.assertEqual(R.ficha("Ixtali Seedjar"), ("Sorcery", 3))

    def test_resolve_fila3_confirmada(self):
        for runa in ("Overgrowth", "Revitalize", "Perseverance"):
            self.assertEqual(R.ficha(runa), ("Resolve", 3), runa)

    def test_keystones_por_arbol(self):
        esperados = {"Electrocute": "Domination", "Dark Harvest": "Domination",
                     "Lethal Tempo": "Precision", "Fleet Footwork": "Precision",
                     "Conquistador": "Precision", "Grasp": "Resolve", "Guardian": "Resolve",
                     "Aery": "Sorcery", "Arcane Comet": "Sorcery", "Phase Rush": "Sorcery",
                     "First Strike": "Inspiration", "Ice Overlord": "Inspiration"}
        for nombre, arbol in esperados.items():
            ficha = R.ficha(nombre)
            self.assertIsNotNone(ficha, nombre)
            self.assertEqual(ficha, (arbol, 0), nombre)


if __name__ == "__main__":
    unittest.main(verbosity=2)
