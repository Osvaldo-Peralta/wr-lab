# -*- coding: utf-8 -*-
"""WR-LAB · tests de model/runas_wr.py — la legalidad de runas WR como estándar.

Los sets-spec son los ejemplos reales del autor (16/10/2026): dos legales
(Jinx publicada; motor agresivo de Yuumi verificado en cliente por el autor y
un amigo) y cuatro ilegales (Yuumi publicada de 4 runas; el set de Electrocute
con secundaria del árbol del keystone —el que midió CDs imposibles en juego—;
el 2 Resolve + 2 Sorcery de la regla; y los 6 slots de los reportes tanque).
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "model"))
import runas_wr as R


class TestSetsSpec(unittest.TestCase):
    def test_jinx_publicada_legal(self):
        ok, motivos = R.es_legal_pagina(
            ["Lethal Tempo", "Brutal", "Legend: Alacrity", "Cut Down", "Bone Plating"])
        self.assertTrue(ok, motivos)

    def test_motor_yuumi_agresiva_legal(self):
        """Verificado en cliente por el autor y su amigo (16/10): sí se equipa."""
        ok, motivos = R.es_legal_pagina(
            ["Electrocute", "Cheap Shot", "Transcendence", "Coup de Grace", "Gathering Storm"])
        self.assertTrue(ok, motivos)

    def test_yuumi_publicada_cuatro_runas_ilegal(self):
        ok, motivos = R.es_legal_pagina(["Summon Aery", "Manaflow Band", "Scorch", "Revitalize"])
        self.assertFalse(ok)
        self.assertTrue(any("L1" in m for m in motivos), motivos)

    def test_electrocute_con_secundaria_del_keystone_ilegal(self):
        """El set que midió CDs imposibles: secundaria Domination con keystone Domination."""
        ok, motivos = R.es_legal_pagina(
            ["Electrocute", "Axiom Arcanist", "Transcendence", "Gathering Storm", "Cheap Shot"])
        self.assertFalse(ok)
        self.assertTrue(any("L4" in m for m in motivos), motivos)

    def test_dos_resolve_dos_sorcery_ilegal(self):
        ok, motivos = R.es_legal_pagina(
            ["Grasp of the Undying", "Bone Plating", "Overgrowth", "Manaflow Band", "Scorch"])
        self.assertFalse(ok)  # secundaria Sorcery con runas Sorcery (L4)
        self.assertTrue(any("L4" in m for m in motivos), motivos)

    def test_chogath_seis_runas_ilegal(self):
        """Deuda conocida de los reportes tanque (6 slots): se corrige en otra iteración."""
        ok, motivos = R.es_legal_pagina(
            ["Grasp of the Undying", "Demolish", "Second Wind", "Overgrowth",
             "Transcendence", "Axiom Arcanist"])
        self.assertFalse(ok)
        self.assertTrue(any("L1" in m for m in motivos), motivos)


class TestReglas(unittest.TestCase):
    def test_fila_global_duplicada_ilegal(self):
        ok, motivos = R.es_legal(
            "Lethal Tempo", ["Brutal", "Triumph", "Cut Down"], "Bone Plating")
        self.assertFalse(ok)  # Dominación r1 (Brutal) y Precisión r1 (Triumph): filas 1,1,3 (L2)
        self.assertTrue(any("L2" in m for m in motivos), motivos)

    def test_control_legal(self):
        ok, motivos = R.es_legal(
            "Lethal Tempo", ["Brutal", "Legend: Alacrity", "Cut Down"], "Bone Plating")
        self.assertTrue(ok, motivos)

    def test_mismo_arbol_misma_fila_ilegal(self):
        ok, motivos = R.es_legal(
            "Electrocute", ["Cheap Shot", "Brutal", "Transcendence"], "Bone Plating")
        self.assertFalse(ok)
        self.assertTrue(any("L3" in m for m in motivos), motivos)  # Domination fila 1 ×2
        self.assertTrue(any("L2" in m for m in motivos), motivos)  # y filas [1,1,2]


if __name__ == "__main__":
    unittest.main(verbosity=2)
