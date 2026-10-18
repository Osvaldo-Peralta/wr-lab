# -*- coding: utf-8 -*-
"""WR-LAB · model/runas_wr.py — LEGALIDAD DE RUNAS WILD RIFT (v1.20, 16/10/2026)

Regla del cliente de WR confirmada por el autor (16/10/2026) y validada contra
sets reales equipados en juego (tests/test_runas_wr.py):

  L1 · Una página = 1 keystone + 3 runas + 1 runa secundaria (5 exactas).
  L2 · Las 3 runas ocupan las FILAS 1, 2 y 3 (una por fila, sin repetir fila).
  L3 · Dentro de un mismo árbol, una runa por fila como máximo (aplica a las 5).
  L4 · La SECUNDARIA debe ser de un árbol que NO usen ni el keystone ni las 3
       runas. (Por eso "Electrocute … secundaria Cheap Shot" es ilegal —el set
       que midió CDs imposibles en juego— y "Electrocute … secundaria Gathering
       Storm" —Inspiration— sí es legal y está verificado en cliente.)

La base de datos de árboles/filas es codificación del lab (cliente WR 7.3b);
si un set LEGAL verificado en juego la contradice, la fuente manda: se ajusta
la DB, nunca la regla.
"""

# (árbol, fila) · fila 0 = keystone
RUNAS = {
    # ── Precisión ──
    "Lethal Tempo": ("Precision", 0), "Conqueror": ("Precision", 0),
    "Fleet Footwork": ("Precision", 0), "Press the Attack": ("Precision", 0),
    "Triumph": ("Precision", 1),
    "Legend: Alacrity": ("Precision", 2), "Legend: Haste": ("Precision", 2),
    "Legend: Bloodline": ("Precision", 2), "Legend: Tenacity": ("Precision", 2),
    "Coup de Grace": ("Precision", 3), "Cut Down": ("Precision", 3),
    "Last Stand": ("Precision", 3),
    # ── Dominación ──
    "Electrocute": ("Domination", 0), "Dark Harvest": ("Domination", 0),
    "Brutal": ("Domination", 1), "Cheap Shot": ("Domination", 1),
    "Taste of Blood": ("Domination", 2), "Zombie Ward": ("Domination", 2),
    "Treasure Hunter": ("Domination", 3), "Ultimate Hunter": ("Domination", 3),
    # ── Hechicería ──
    "Summon Aery": ("Sorcery", 0), "Aery": ("Sorcery", 0),
    "Arcane Comet": ("Sorcery", 0), "Phase Rush": ("Sorcery", 0),
    "Manaflow Band": ("Sorcery", 1), "Nullifying Orb": ("Sorcery", 1),
    "Transcendence": ("Sorcery", 2),
    "Scorch": ("Sorcery", 3),
    # ── Inspiración ──
    "First Strike": ("Inspiration", 0), "Glacial Augment": ("Inspiration", 0),
    "Hextech Flashtraption": ("Inspiration", 1), "Magical Boots": ("Inspiration", 1),
    "Axiom Arcanist": ("Inspiration", 2),
    "Gathering Storm": ("Inspiration", 3),
    # ── Resolución ──
    "Grasp of the Undying": ("Resolve", 0), "Aftershock": ("Resolve", 0),
    "Bone Plating": ("Resolve", 1), "Second Wind": ("Resolve", 1),
    "Demolish": ("Resolve", 2), "Overgrowth": ("Resolve", 2),
    "Revitalize": ("Resolve", 3), "Unflinching": ("Resolve", 3),
}
ALIAS = {"Aery": "Summon Aery", "Grasp": "Grasp of the Undying",
         "Alacrity": "Legend: Alacrity", "Comet": "Arcane Comet"}


def norm(nombre):
    n = nombre.strip()
    return ALIAS.get(n, n)


def ficha(nombre):
    return RUNAS.get(norm(nombre))


def es_legal(keystone, runas3, secundaria):
    """(ok, motivos[]) según L1-L4."""
    motivos = []
    ks = ficha(keystone)
    rs = [ficha(r) for r in runas3]
    sc = ficha(secundaria)
    if ks is None or ks[1] != 0:
        motivos.append(f"keystone inválido o no es keystone: {keystone}")
    if len(runas3) != 3 or sc is None:
        motivos.append("una página legal = 1 keystone + 3 runas + 1 secundaria (L1)")
        return False, motivos
    if any(r is None for r in rs):
        malos = [n for n, r in zip(runas3, rs) if r is None]
        motivos.append(f"runas fuera de la DB: {malos}")
        return False, motivos
    if sc[1] == 0:
        motivos.append(f"la secundaria no puede ser keystone: {secundaria}")
    filas = [r[1] for r in rs]
    if sorted(filas) != [1, 2, 3]:
        motivos.append(f"las 3 runas deben ocupar filas 1, 2 y 3 sin repetir (L2): {filas}")
    vistas = {}
    for nombre, fr in [(keystone, ks)] + list(zip(runas3, rs)) + [(secundaria, sc)]:
        if not fr or fr[1] == 0:
            continue
        k = (fr[0], fr[1])
        if k in vistas:
            motivos.append(f"árbol {fr[0]} fila {fr[1]} duplicada: {vistas[k]} y {nombre} (L3)")
        vistas[k] = nombre
    arboles_runas = {r[0] for r in rs} | ({ks[0]} if ks else set())
    if sc[0] in arboles_runas:
        motivos.append(
            f"la secundaria ({secundaria}, {sc[0]}) debe ser de un árbol no usado por "
            f"keystone ni runas (L4): {sorted(arboles_runas)}")
    return (len(motivos) == 0), motivos


def es_legal_pagina(nombres5):
    """Atajo: [keystone, runa1, runa2, runa3, secundaria]."""
    if len(nombres5) != 5:
        return False, [f"L1: esperados 5 slots, recibidos {len(nombres5)}"]
    return es_legal(nombres5[0], nombres5[1:4], nombres5[4])
