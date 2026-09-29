# TEMPLATE + GUÍA DE ESTILO — Reportes WR-LAB (estándar v1.4)

> **Este archivo es la ley visual de los reportes.** Todo reporte nuevo (o re-estilizado) DEBE seguir
> esta estructura y convenciones al pie de la letra. Referencia canónica viva:
> `reportes/Jinx_WildRift_7.3_Build_Optimizada.md`.
> Regla de oro: cada afirmación lleva número, cada número lleva supuesto, cada supuesto está en §3/§10.

---

## A. GUÍA DE ESTILO (convenciones obligatorias)

### A.1 Estructura general
1. **Frontmatter YAML** (compatible Obsidian/Quartz):
   ```yaml
   ---
   tags:
     - {ROL}          # ADC / Support / Jungla / Mid / Top
     - {CLASE}        # Marksman / Enchanter / Assassin / Fighter / Mage / Tank
     - {ARQUETIPO}    # Crítico / On-hit / AP-Burst / etc.
     - {LANE}         # Bot-Lane / etc.
   version: X.Y
   Status: Borrador | Aprobado
   champion: {Nombre}
   patch: "7.3"
   ---
   ```
2. **Bloque de metadatos** (inmediato, en negritas, una línea por campo):
   `**Fecha del análisis:**` · `**Parche:**` · `**Rol principal:**` · `**Arquetipo:**` · `**Enfoque:**` (1-2 líneas: la tesis de la build).
3. **Callouts Obsidian** (en este orden, tras los metadatos):
   - `> [!NOTE]` **Estado Meta Actual ({rango}, {fecha}):** Win Rate X % | Pick Rate X % | Ban X % | Tendencia ↑↓ | Rol. → **OBLIGATORIO** (datos de wr-meta/fichas).
   - `> [!TIP]` Variante principal en 2-3 líneas (qué slot cambia, qué se gana/pierde con números). → OBLIGATORIO si existe variante.
   - `> [!DANGER]` Solo en **builds personalizadas de escenario** (ej. Yuumi agresiva, Cho'Gath tamaño): declarar el sacrificio con números ("sacrifica ~X % de Y a cambio de ~Z % más de W").
   - `> [!WARNING]` Datos pendientes de verificar en juego (rangos, mecánicas ambiguas).
4. Separador `---` entre TODAS las secciones numeradas.

### A.2 Encabezados
- Secciones: `## N. TÍTULO EN MAYÚSCULAS` (N = 0…10, fijos, ver §B). Apéndices: `## APÉNDICE A — ...`.
- Subsecciones: `### N.M Título en oración`.
- NUNCA inventar secciones fuera del esqueleto; si una no aplica al arquetipo, dejarla con su número y una nota de adaptación (ej. "§5 — No aplica: el primer ítem de support es la quest").

### A.3 Números y formato
- **Miles con espacio fino:** `2 900`, `17 350 g`, `1 250 g` (NUNCA `2900` ni `2,900`).
- **Porcentajes con espacio:** `25 %`, `100 %`, `+47.9 %`. Decimales con punto: `2.83`, `49.82 %`.
- DPS y oro como enteros; deltas con signo: `+19 %`, `−22 %` (minus U+2212 preferida).
- Ítems y runas en **negrita** en tablas y en primera aparición; habilidades en _cursiva_ o **Q/W/E/R**.
- Veredictos con emoji + número SIEMPRE: ✅ Core/6.º default · ⚠️ Situacional/niche · ❌ Rechazado (motivo numérico).
- Tablas > prosa. Prosa solo para veredictos, notas críticas y plan de juego (bullets con **lead en negrita**).
- Fórmulas y rutas de compra en bloques de código ``` ```.
- Flecha de mejora de botas: `⬆️` + texto "(min 10:00, MISMO slot)".

### A.4 Ley 0 en las tablas (no negociable)
- **Tabla A (Build final):** exactamente **6 filas** = 1 fila de botas (`Berserker's → ⬆️ Gunmetal (min 10:00, MISMO slot)`) + 5 ítems. Columnas: `Slot | Ítem | Oro | Rol en la build`.
- **Tabla B (Ruta de compra):** cronológica, puede tener 7+ filas porque incluye la mejora ⬆️ y los componentes. Columnas: `# | Compra | Oro acum. | Minuto típico`. Incluir **componentes** ("Pickaxe + Noonquiver → **Hexoptics C44**") y **oro acumulado**.
- Toda build publicada pasa `validate_slots()` y se declara en §10 ("Validación del modelo").

### A.5 Adaptaciones por arquetipo
| Arquetipo | §3 Modelo | §0 Resultado del modelo | §5 Primer ítem |
|---|---|---|---|
| ADC crítico / on-hit | DPS autos + procs | DPS 1v1 / 3v3 / vs armadura / vs tanque / heal | Sí (checkpoints 9/12) |
| AP rotación (Diana, mid) | Burst combo + DPS 10 s | DPS sostenido / burst / vs MR | Sí (orden de core) |
| Soportes (Yuumi/Karma) | **Valor-aliado**: escudos, curas, buffs | Escudo E / cura R / **DPS+ al carry** / amp de equipo | No aplica (quest) — declarar |
| Tanques (Cho'Gath/Malphite) | EHP + ventanas + execute R | EHP, mitigación, daño de utilidad | Sí (componente de vida/armadura) |

### A.6 Pie de página (OBLIGATORIO, estructura fija)
```markdown
---

## Pie de página

*Reporte generado el {dd/mm/aaaa} con datos del parche {X.X} ({fecha parche}). WR-LAB v{n}. Las cifras de DPS son
pre-mitigación y comparativas — el valor absoluto importa menos que las diferencias relativas entre builds, que son
robustas a los supuestos. Si Riot publica un {X.X}a/b (hotfix), regenerar datos antes de publicar.*

**Referencias y créditos**

- Notas oficiales del parche {X.X} ({fecha}) y {anteriores relevantes} — © Riot Games, Inc. (wildrift.leagueoflegends.com). {qué aporta}.
- Base de datos de ítems, runas y fichas de campeón — wr-meta.com (proyecto comunitario de JLVD DEV), sincronizada al {fecha}. {qué aporta}.
- Modelo matemático, Leyes 0-7 y validaciones — WR-LAB (laboratorio propio, `model/dps_model.py`), construido sobre las fuentes anteriores.

**Aviso legal:** Wild Rift y League of Legends son marcas registradas de Riot Games, Inc. Este documento es una guía
de comunidad con fines educativos, **no está afiliado, patrocinado ni respaldado por Riot Games**. Los nombres de
ítems, campeones y estadísticas pertenecen a sus respectivos dueños. El análisis y las conclusiones son trabajo
original del autor apoyado en WR-LAB.

---
```

### A.7 Nomenclatura de archivo (vault/sitio)
`{Campeón} — Wild Rift Build Optimizada.md` (título H1 NO se repite en el cuerpo si el frontmatter lleva `champion:`; el H1 lo pone Quartz). Para el lab: `reportes/{Campeón}_WR_{patch}_Build_Optimizada.md`.

---

## B. ESQUELETO CANÓNICO (copiar y llenar)

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
### 1.1 Cambios directos ({champion}) — tabla Stat/Habilidad | Antes | Ahora | Impacto
### 1.2 Cambios sistémicos que le afectan — tabla Sistema | Cambio | Efecto
### 1.3 ¿Sus habilidades escalan con crítico/{stat clave}? — respuesta + implicación

---

## 2. FICHA MATEMÁTICA (spec)
| Parámetro | Valor | Fuente |   (+ líneas de cálculo en negrita: AD lvl 15, bonus fijo, etc.)

---

## 3. MODELO Y FÓRMULAS
```{fórmulas del motor adaptadas al campeón}```
### Supuestos específicos — bullets

---

## 4. LEYES APLICADAS A {CHAMPION}
### Ley 0 — Slots (siempre: declarar 1 botas + 5 ítems y validate_slots PASS)
### Ley 1..7 — solo las que aplican al arquetipo, con tabla/cálculo por ley

---

## 5. ANÁLISIS DEL PRIMER ÍTEM
| Candidato | Oro | DPS lvl 9 1v1 | lvl 9 3v3 | lvl 12 1v1 | lvl 12 3v3 | Nota |
**Veredicto:** {con números y cruce de curvas}. **Nota crítica:** {mitos corregidos}.

---

## 6. BUILD FINAL RANURA POR RANURA
| Slot | Ítem | Justificación matemática |
### Matriz del último slot (situacional)
| Situación | Ítem | Coste | Impacto medido |
### RECHAZADOS (con motivo numérico)
| Ítem | Motivo del rechazo |

---

## 7. RUNAS · HECHIZOS · HABILIDADES
### Keystone: {nombre} — bullets con números + **Alternativas:** en cursiva con caso de uso
### Secundarias — tabla Slot | Runa | Valor estimado
### Hechizos: {X + Y} — por qué
### Orden de habilidades — **{A → B → C}** + bullet por habilidad

---

## 8. COMPARACIÓN CONTRA LAS ALTERNATIVAS
### Tabla maestra ({nivel}, {condiciones})
| Build | Oro | {stats} | 1v1 | 3v3 | vs 120 | vs Tanque | {sustain} |
### Desglose multiplicativo de la diferencia — tabla Factor | Multiplicador | Contribución

---

## 9. PLAN DE JUEGO
### Early (0:00 – 9:00) / ### Mid (9:00 – 16:00) / ### Late (16:00+)
— bullets con **lead en negrita** y números/tiempos
### Reglas del parche que cambian el macro — tabla Regla | Impacto

---

## 10. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS
### Fuentes primarias (mandan) — tabla
### Fuentes secundarias — tabla
### Discrepancias detectadas y resolución — tabla
### Supuestos del modelo (declarados) — bullets
### Contexto meta ({fecha}) — párrafo con cautela de muestra
### Validación del modelo — bullets: `validate_slots(...) → PASS` + test de Caitlyn (1.48125)

---

## APÉNDICE A — POOL DE ÍTEMES DEL ROL: veredicto para {champion}
| Ítem (oro) | Veredicto | Nota |

---

## APÉNDICE B — RUTAS DE COMPRA
```{DEFAULT / SNOWBALL / ANTI-PRESIÓN / VS … en bloque de código con ⬆️ y minutos}```

---

## Pie de página
{estructura fija de A.6}
```

---

## C. CHECKLIST ANTES DE PUBLICAR (Status: Borrador → Aprobado)

- [ ] Frontmatter completo (tags rol/clase/arquetipo/lane, version, Status, champion, patch).
- [ ] Metadatos + callout [!NOTE] con meta real (WR/pick/ban/tendencia + fecha).
- [ ] Tabla A = 6 filas exactas (1 botas con ⬆️ + 5 ítems); Tabla B con componentes y oro acumulado.
- [ ] `validate_slots()` en PASS declarado en §10.
- [ ] Números con espacio de miles (`2 900`) y `%` con espacio (`25 %`) en TODO el documento.
- [ ] Secciones 0-10 + Apéndices A/B + Pie de página presentes, en orden, con `---` entre ellas.
- [ ] Todo ✅/⚠️/❌ acompañado de número.
- [ ] Discrepancias de fuentes declaradas (notas oficiales > wr-meta).
- [ ] Hotfix verificado (¿7.3a/b?) antes de pasar a Status: Aprobado.
- [ ] Pie de página con referencias Riot/wr-meta/WR-LAB + aviso legal.
