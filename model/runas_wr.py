# -*- coding: utf-8 -*-
"""WR-LAB · model/runas_wr.py — LEGALIDAD DE RUNAS WILD RIFT (v1.21, 18/10/2026)

Reglas del cliente de WR confirmadas por el autor (18/10/2026, verificación
in-game) — CORRECCIÓN de la v1.20, que permitía las 3 runas de árboles mixtos:

  L1 · Una página = 1 KEYSTONE + 3 RUNAS + 1 SECUNDARIA (5 slots exactos).
  L2 · Las 3 runas son DEL ÁRBOL DEL KEYSTONE (el árbol principal), una por
       cada fila: filas 1, 2 y 3, sin repetir fila.
  L3 · (contenida en L2) dentro del árbol principal, ≤1 runa por fila.
  L4 · La SECUNDARIA es de CUALQUIER OTRO árbol — nunca del principal.
       No importa su fila: puede ser Revitalize, Second Wind (Resolve),
       Sudden Impact (Domination), Cut Down (Precision)...

EJEMPLO CANÓNICO (build publicada de Yuumi agresiva, LEGAL, verificada in-game
por el autor):
    Aery (keystone Sorcery) · Manaflow Band (Sorcery f1) · Transcendence
    (Sorcery f2) · Scorch (Sorcery f3) · Revitalize (secundaria Resolve).

FUENTE DE LA DB: data/estructurada/runas_7.3.md (wr-meta 24-sep-2026). El
ORDEN de lista de cada sección del md coincide con las filas del cliente
(confirmado por el autor para SORCERY: f1 Axiom/Manaflow/Botanist/Hexflash ·
f2 Transcendence/Celerity/Absolute Focus · f3 Scorch/Nimbus Cloak/Gathering
Storm/Ixtal Seedjar; y para RESOLVE f3 = Overgrowth/Revitalize/Perseverance).
Las filas de DOMINATION/PRECISION/RESOLVE f1-f2 se infieren del mismo orden
del md: PENDIENTES de verificación in-game (marcadas abajo). Gathering Storm e
Ixtal Seedjar: el md está truncado tras Nimbus Cloak; se completan con la
confirmación in-game del autor (18/10). Inspiration: el md no llega a listar
sus menores (hueco de datos declarado).

CAMBIO DE POSTURA vs v1.20: el set del motor batch5 (Electrocute + Cheap Shot +
Transcendence + Coup de Grace | Gathering Storm) es ILEGAL bajo L2 —las 3 runas
deben ser del árbol del keystone (Domination) y Transcendence/Coup de Grace no
lo son—. La v1.20 lo daba legal por una DB errónea (keystones y filas mal
mapeadas, p.ej. Gathering Storm figuraba como Inspiration). Los reportes que
citen ese set deben corregirse.

La base de datos es codificación del lab (cliente WR 7.3b); si un set LEGAL
verificado en juego la contradice, la fuente manda: se ajusta la DB, nunca la
regla.
"""

# (árbol, fila) · fila 0 = keystone
RUNAS = {
    # ── KEYSTONES ──
    # Domination
    "Electrocute": ("Domination", 0), "Dark Harvest": ("Domination", 0),
    "Empowerment": ("Domination", 0),          # orden del md (bloque Domination); confirmar in-game
    # Precision
    "Lethal Tempo": ("Precision", 0), "Fleet Footwork": ("Precision", 0),
    "Conqueror": ("Precision", 0),
    # Resolve
    "Grasp of the Undying": ("Resolve", 0), "Guardian": ("Resolve", 0),
    # Sorcery
    "Aery": ("Sorcery", 0), "Arcane Comet": ("Sorcery", 0), "Phase Rush": ("Sorcery", 0),
    # Inspiration
    "First Strike": ("Inspiration", 0), "Ice Overlord": ("Inspiration", 0),

    # ── DOMINATION (filas inferidas del orden del md — CONFIRMAR in-game) ──
    "Cheap Shot": ("Domination", 1), "Sudden Impact": ("Domination", 1),
    "Empowered Attack": ("Domination", 1), "Chain Assault": ("Domination", 1),
    "Tyrant": ("Domination", 2), "Hubris": ("Domination", 2),
    "Eyeball Collection": ("Domination", 2),
    "Relentless Hunter": ("Domination", 3), "Zombie Ward": ("Domination", 3),
    # Ingenious Hunter: REMOVIDA en 7.3 (ver runas_7.3.md, cabecera) → no equipa.

    # ── PRECISION (filas inferidas del orden del md — CONFIRMAR in-game) ──
    "Brutal": ("Precision", 1), "Triumph": ("Precision", 1), "Battle Zeal": ("Precision", 1),
    "Last Stand": ("Precision", 2), "Cut Down": ("Precision", 2), "Coup de Grace": ("Precision", 2),
    "Legend: Alacrity": ("Precision", 3), "Legend: Haste": ("Precision", 3),
    "Legend: Bloodline": ("Precision", 3),

    # ── RESOLVE (filas inferidas del orden del md; f3 CONFIRMADA por el autor) ──
    "Demolish": ("Resolve", 1), "Font of Life": ("Resolve", 1),
    "Courage of the Colossus": ("Resolve", 1), "Unshakeable": ("Resolve", 1),
    "Second Wind": ("Resolve", 2), "Nullifying Orb": ("Resolve", 2), "Bone Plating": ("Resolve", 2),
    "Overgrowth": ("Resolve", 3), "Revitalize": ("Resolve", 3), "Perseverance": ("Resolve", 3),

    # ── SORCERY (filas CONFIRMADAS in-game por el autor, 18/10) ──
    "Axiom Arcanist": ("Sorcery", 1), "Manaflow Band": ("Sorcery", 1),
    "Botanist": ("Sorcery", 1), "Hextech Flashtraption": ("Sorcery", 1),
    "Transcendence": ("Sorcery", 2), "Celerity": ("Sorcery", 2), "Absolute Focus": ("Sorcery", 2),
    "Scorch": ("Sorcery", 3), "Nimbus Cloak": ("Sorcery", 3),
    "Gathering Storm": ("Sorcery", 3), "Ixtal Seedjar": ("Sorcery", 3),

    # ── INSPIRATION: el md 7.3 no lista menores (archivo truncado). Hueco de
    # datos declarado: cualquier menor Inspiration dará "fuera de la DB". ──
}

ALIAS = {
    "Summon Aery": "Aery", "Aery (Summon Aery)": "Aery",
    "Grasp": "Grasp of the Undying", "Grasp of Undying": "Grasp of the Undying",
    "Conquistador": "Conqueror", "Electrocutar": "Electrocute",
    "Cosecha Oscura": "Dark Harvest", "Flota": "Fleet Footwork",
    "Guardián": "Guardian", "Primer Golpe": "First Strike",
    "Fase Rush": "Phase Rush", "Comet": "Arcane Comet",
    "Hexflash": "Hextech Flashtraption", "Ixtali Seedjar": "Ixtal Seedjar",
    "Alacrity": "Legend: Alacrity",
    "Legend: Tenacity": "Legend: Haste",  # 7.3: renombrada (runas_7.3.md, cabecera)
    # nombres que NO existen / fueron REMOVIDOS en 7.3 → None (la página no equipa):
    "Ingenious Hunter": None, "Press the Attack": None, "Predator": None,
    "Aftershock": None, "Glacial Augment": None, "Magical Boots": None,
    "Taste of Blood": None, "Treasure Hunter": None, "Ultimate Hunter": None,
    "Unflinching": None,
}
REMOVIDAS = {n for n, v in ALIAS.items() if v is None}

ARBOLES = ("Domination", "Precision", "Resolve", "Sorcery", "Inspiration")


def norm(nombre):
    n = str(nombre).strip()
    return ALIAS[n] if n in ALIAS else n


def ficha(nombre):
    """(árbol, fila) o None. fila 0 = keystone; None = fuera de DB/removida."""
    n = norm(nombre)
    if n is None:
        return None
    return RUNAS.get(n)


def es_removida(nombre):
    """True si el nombre mapea a una runa removida/inexistente en 7.3."""
    return norm(nombre) is None


def es_legal(keystone, runas3, secundaria):
    """(ok, motivos[]) según L1-L4 (reglas corregidas 18/10/2026)."""
    motivos = []
    ks = ficha(keystone)
    if ks is None or ks[1] != 0:
        extra = " (removida/inexistente en 7.3)" if es_removida(keystone) else ""
        motivos.append(f"L1: keystone inválido o no es keystone: {keystone}{extra}")
        return False, motivos
    arbol_ks = ks[0]
    if len(runas3) != 3:
        motivos.append(
            f"L1: una página legal = 1 keystone + 3 runas + 1 secundaria (5 slots); "
            f"se listaron {len(runas3)} runas")
        return False, motivos

    rs = []
    for r in runas3:
        f = ficha(r)
        if f is None:
            extra = " (removida/inexistente en 7.3)" if es_removida(r) else ""
            motivos.append(f"L1: runa fuera de la DB: {r}{extra}")
        elif f[1] == 0:
            motivos.append(f"L1: {r} es keystone; no puede ir entre las 3 runas")
        else:
            rs.append((r, f))
    sc = ficha(secundaria) if secundaria is not None else None
    if sc is None:
        extra = " (removida/inexistente en 7.3)" if secundaria is not None and es_removida(secundaria) else ""
        motivos.append(f"L1: secundaria fuera de la DB: {secundaria}{extra}")
    elif sc[1] == 0:
        motivos.append(f"L4: la secundaria no puede ser keystone: {secundaria}")
    if motivos:
        return False, motivos

    # L2 — las 3 runas, del árbol del keystone, una por fila (1, 2, 3)
    ajenas = [(n, f) for n, f in rs if f[0] != arbol_ks]
    if ajenas:
        motivos.append(
            f"L2: las 3 runas deben ser del árbol del keystone ({arbol_ks}); "
            f"ajenas: {[(n, f'{f[0]} f{f[1]}') for n, f in ajenas]}")
    filas = sorted(f[1] for n, f in rs if f[0] == arbol_ks)
    if not ajenas and filas != [1, 2, 3]:
        motivos.append(
            f"L2/L3: las 3 runas del árbol {arbol_ks} deben ocupar las filas 1, 2 y 3 "
            f"sin repetir fila: filas ocupadas {filas}")

    # L4 — secundaria de cualquier OTRO árbol (nunca del principal)
    if sc[0] == arbol_ks:
        motivos.append(
            f"L4: la secundaria ({secundaria}, {sc[0]}) es del árbol principal ({arbol_ks}); "
            "debe ser de cualquier otro árbol")
    return (len(motivos) == 0), motivos


def es_legal_pagina(nombres5):
    """Atajo: [keystone, runa1, runa2, runa3, secundaria]."""
    if len(nombres5) != 5:
        return False, [f"L1: esperados 5 slots (1 keystone + 3 runas + 1 secundaria), recibidos {len(nombres5)}"]
    return es_legal(nombres5[0], nombres5[1:4], nombres5[4])
