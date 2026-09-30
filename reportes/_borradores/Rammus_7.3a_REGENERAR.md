---
tags:
  - BORRADOR
version: 0.1
Status: Borrador
champion: Rammus
patch: "7.3a"
---
# ⚠️ BORRADOR DE REGENERACIÓN — Rammus (7.3a) · generado 30/09/2026 por update_reports.py

> [!DANGER] Por qué existe este borrador
> El reporte publicado `Rammus.md` recibió veredicto **❌ REGENERAR** contra 7.3a:
> cambio directo a inputs del spec (AD/AS/defensas base o growth).
> **Cambio directo:** Armor base 45→**40** · W bonus armor 45/50/55/60→**30/40/50/60 %**

## 1. DATOS NUEVOS DEL PARCHE (fuente: data/estructurada/cambios_7.3a.md)

| Entidad | Tipo | Cambio |
|---|---|---|
| **Rammus** | NERF | Armor base 45→**40** · W bonus armor 45/50/55/60→**30/40/50/60 %** |
| (sistema) | — | Smite burn vs monstruos: 30–198/s → **22–162/s** → Jungla early más lenta → Diana jungla: Nashor's 1.º aún más correcto; Shyvana/Volibear/Cho'Gath jungla: clear early −15-20 % |

## 2. FICHA BASE (datos del lab)
- **AS oficial (7.3, overrides 7.3a marcados):** `Rammus, 0.625, 0.625, 0.28, 0.0185`
- **Durabilidad (cambios 7.3):** `Rammus, 690 → 670, 49 → 45, , , 112 → 124`
- **ChampSpec:** NO existe en `model/champspecs.py` — crearlo desde el apéndice AS de las notas oficiales + wiki (FRAMEWORK §A paso 2)

## 3. CÓMO REGENERAR (flujo FRAMEWORK §A de 10 pasos)

1. Actualizar el spec/datos con los valores de §1 (fuente primaria: notas oficiales 7.3a).
2. Re-derivar candidatos: crear primero el ChampSpec (paso 2 de FRAMEWORK §A) y luego `python3 model/optimize_build.py rammus --validar --top 8`; si el arquetipo no es de autos, comparar candidatas con analysis_batch2.
   Verificar también a mano contra las candidatas del reporte original (§8).
3. Rellenar el esqueleto TEMPLATE (§B) abajo, o generar el reporte completo en un chat
   externo con el bundle `WR-LAB_completo.md`.
4. Sustituir `reportes/Rammus.md` por la versión nueva (o decidir mantenerla con el
   bloque ❌ visible), luego:
   `python3 model/update_reports.py baseline && python3 model/update_reports.py annotate --patch 7.3a --apply`
5. `python3 model/build_bundles.py && python3 -m unittest discover -s tests` y commit.

## 4. ESQUELETO DEL REPORTE NUEVO (TEMPLATE v1.4 §B)

```markdown
---
tags: [ ... ]
version: 1.0
Status: Borrador
champion: {Nombre}
patch: "7.3"
---
**Fecha del análisis:** {dd/mm/aaaa}
**Parche:** 7.3 (21-sep-2026)
**Rol principal:** {rol}
**Arquetipo:** {arquetipo con 1 línea descriptiva}
**Enfoque:** {tesis de la build en 1-2 líneas con números}

> [!NOTE]
> **Estado Meta Actual (Diamond+, {fecha}):**
> Win Rate {X} % | Pick Rate {X} % | Ban {X} % | Tendencia {↑/↓} | Rol: {roles}.

> [!TIP]
> **Variante principal:** {slot que cambia + trade-off numérico}.

---

## 0. RESUMEN EJECUTIVO

### Tabla A — BUILD FINAL
| Slot | Ítem | Oro | Rol en la build |
|------|------|-----|-----------------|
| 1 (botas) | **{T2} → ⬆️ {T3}** (min 10:00, MISMO slot) | {g} | {stats clave} |
| 2..6 | **{ítem}** | {g} | {stats + pasiva en 1 línea} |

> **Oro total: {N} g** · {AD/AP} {X} · {AS/haste} {X} · {Crit/pen/HSP} {X} · {sustain}

### Tabla B — Ruta de compra cronológica
| # | Compra | Oro acum. | Minuto típico |
|---|--------|-----------|---------------|
| 1 | {start} | 500 | 0:00 |
| … | {componentes} → **{ítem completo}** | {acum} | ~{mm:ss} |
| k | ⬆️ **{T3}** (mismo slot, +1 000 g) | {acum} | ~{13:00} |

### Runas · Hechizos · Habilidades
| Categoría | Elección |
|-----------|----------|
| Keystone | **{runa}** ({números}) |
| {Árbol} 2..4 | **{runa}** ({números}) |
| Secundaria | **{runa A}** ({caso}) / **{runa B}** ({caso}) |
| Hechizos | **{X + Y}** |
| Skills | **{orden}** (R en 5/9/13) |

### Resultado del modelo ({condiciones})
| Escenario | {DPS/Valor} |
|-----------|-----|
| **1v1** (pre-mitigación) | **{N}** |
| **3v3** | **{N}** |
| **vs 120 armadura / MR** | **{N}** |
| **vs Tanque** | **{N}** |
| {sustain/heal/shields} | **{N}** |

> **Titular:** {comparación estelar con % vs la alternativa más común}.

---

## 1. CONTEXTO DEL CAMPEÓN EN ESTE PARCHE
### 1.1 Cambios directos (Rammus) — tabla Stat/Habilidad | Antes | Ahora | Impacto
### 1.2 Cambios sistémicos que le afectan — tabla Sistema | Cambio | Efecto
### 1.3 ¿Sus habilidades escalan con crítico/{stat clave}? — respuesta + implicación

---

## 2. FICHA MATEMÁTICA (spec)
| Parámetro | Valor | Fuente |   (+ líneas de cálculo en negrita: AD lvl 15, bonus fijo, etc.)

---

## 3. MODELO Y FÓRMULAS
```
