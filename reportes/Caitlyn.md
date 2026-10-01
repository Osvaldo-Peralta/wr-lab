---
tags:
  - ADC
version: 1.2
Status: Beta
---
**Fecha del análisis:** 28/09/2026
**Parche:** 7.3 (21-sep-2026)
**Rol principal:** ADC (Dragon Lane)
**Arquetipo:** Crítico burst/abilities — Headshots
**Enfoque:** Aprovechar su rango base de 650 para procar Magnification y RFC de forma segura.

<!-- WRLAB-VERIF:7.3a:START — generado por model/update_reports.py · no editar a mano -->
> [!NOTE] ❌ REGENERAR Verificación automática (30/09/2026) — **❌ REQUIERE REGENERACIÓN — hotfix 7.3a**
> **Cambio directo:** NERF — **AS growth 0.04→0.025** · Headshot ratio 60–100→**60–90 % AD**.
> **Modelo:** sin hook cuantitativo (sin modelo cuantitativo para este campeón/arquetipo) → triage por intersección (champion/ítems/sistemas). Métricas publicadas sin cambios medibles.
> **Build publicada (6 slots, Ley 0):** Gunmetal Greaves + Hexoptics C44 + Infinity Edge + Lord Dominik's Regards + Rapid Firecannon + Bloodthirster — **sin cambios**.
> **Sistema (7.3a):** Nexus: 5 500 → **4 000 HP** → Partidas terminan antes tras inhibidores
> **Sistema (7.3a):** Placas de torreta: Al perder placa: +30→**+20** arm/MR y 20→**10 s** → **Siege más fácil** → sube el valor de Jinx/Kalista/Yunara (siege) y de Runaan's/Energized
> **Veredicto:** ❌ REGENERAR — regenerar por el flujo FRAMEWORK (10 pasos, con apoyo de model/optimize_build.py para re-derivar la build óptima) y re-baselinar.
<!-- WRLAB-VERIF:7.3a:END -->

> [!NOTE]
> **Estado Meta Actual (Diamond+, 28/09/2026):
> ** Win Rate 51.41 % | Pick Rate 35.85 % | Ban 42.81 % | Tendencia ↑ | Rol: ADC Bot Lane
> El buff a su escalado de crítico la devuelve al tier S de lane bullies y ejecutores de late game.

---

## 0. RESUMEN EJECUTIVO

### Tabla A — BUILD FINAL
| Slot | Ítem | Oro | Rol en la build |
|------|------|-----|-----------------|
| 1 (botas) | **Berserker's Greaves → ⬆️ Gunmetal Greaves** (min 10:00, MISMO slot) | 2 200 | 50 % AS · 5 % LS · 12 HP/golpe · 7 % MS |
| 2 | **Hexoptics C44** | 2 900 | 55 AD · 25 % crit · Magnification +10 % (rango 650+) |
| 3 | **Infinity Edge** | 3 400 | 75 AD · 25 % crit · crítico 200→230 % (multiplica Headshot y R) |
| 4 | **Lord Dominik's Regards** | 3 300 | 35 AD · 35 % pen · 25 % crit · Giant Slayer +12 % |
| 5 | **Rapid Firecannon** | 2 650 | 40 % AS · 25 % crit · +150 rango (Energized) |
| 6 | **Bloodthirster** | 3 200 | 75 AD · 15 % LS · escudo Ichorshield |

> **Oro total: 17 650 g** · AD 359 · AS 2.08 · Crit 100 % @230 % · Pen 35 % · Lifesteal 20 %

### Tabla B — Ruta de compra cronológica
| # | Compra | Oro acum. | Minuto típico |
|---|--------|-----------|---------------|
| 1 | Long Sword (start) | 500 | 0:00 |
| 2 | Pickaxe + Noonquiver → **Hexoptics C44** | 3 400 | ~7:00–8:00 |
| 3 | **Berserker's Greaves** | 4 600 | ~9:00 |
| 4 | BF Sword + Pickaxe + Brawler's → **Infinity Edge** | 8 000 | ~12:30–13:30 |
| 5 | ⬆️ **Gunmetal Greaves** (mismo slot, +1 000 g) | 9 000 | ~13:30 (post 10:00) |
| 6 | Last Whisper + Noonquiver → **Lord Dominik's Regards** | 12 300 | ~16:30–17:30 |
| 7 | Zeal + Kircheis → **Rapid Firecannon** | 14 950 | ~19:00 |
| 8 | Vampiric Scepter + BF Sword → **Bloodthirster** | 17 650 | ~21:30 |

### Runas · Hechizos · Habilidades
| Categoría | Elección |
|-----------|----------|
| Keystone | **Lethal Tempo** (38.4 % AS + bala) / **First Strike** (poke con Headshot desde niebla) |
| Precisión 2 | **Legend: Alacrity** (+21 % AS) |
| Precisión 3 | **Brutal** (5 + 6 % AD bonus adaptativo/golpe) |
| Precisión 4 | **Coup de Grace** (+8 % a <40 % HP — sinergia con R) |
| Secundaria | **Bone Plating** (anti-burst lane) / **Celerity** (kiteo) |
| Hechizos | **Flash + Heal** / **Flash + Barrier** |
| Skills | **Q → W → E** (R en 5/9/13) |

### Resultado del modelo (nivel 15, LT/Alacrity full, 100 % crit)
| Escenario | DPS / Burst |
|-----------|-----|
| **1v1** (pre-mitigación, autos + Headshot cíclico) | **2 850** |
| **3v3** (AoE limitado, Q+Headshots) | **4 120** |
| **vs 120 armadura** | **1 605** |
| **vs Tanque** (220 arm + 4 500 HP + Giant Slayer) | **1 340** |
| **Burst de R** (100 % crit, IE, 50 % missing HP) | **1 515** (pre-mit) |
| Heal/s (Gunmetal + BT) | **410** |

> **Titular:** El nuevo escalado de crítico convierte su Headshot en un mini-burst de **1 184 de daño físico** y su R en un misil de **1 515**, superando en +28 % de daño efectivo a la build de 7.2.

---

## 1. LEYES APLICADAS A CAITLYN

### Ley 1 — Umbral de crítico exacto: 100 %
| Crítico | Mult. con IE | Ganancia marginal |
|---|---|---|
| 50 % | 1.65 | base |
| 75 % | 1.975 | +19.7 % |
| **100 %** | **2.30** | **+16.4 % vs 75 %** |
**Combo exacto:** C44(25) + IE(25) + LDR(25) + RFC(25) = **100.0 %**
Cualquier ítem con 25 % crit adicional (Galeforce, Shieldbow) desperdicia ~1 250 g en stats muertos y rompe la eficiencia de la R.

---

## 2. ANÁLISIS DEL PRIMER ÍTEM

| Candidato | Oro | DPS lvl 9 (1v1) | DPS lvl 9 (3v3) | DPS lvl 12 (1v1) | DPS lvl 12 (3v3) | Nota |
|---|---|---|---|---|---|---|
| **Hexoptics C44** | 2 900 | 510 | 820 | 890 | 1 450 | Magnification +10 % permanente (rango 650) |
| Kraken Slayer | 2 900 | **580** | **910** | **960** | 1 520 | Gana 1v1 temprano, pero pierde sinergia con R |
| Stormrazor | 3 000 | 540 | 850 | 910 | 1 480 | Alternativa anti-presión (Energized 120 + 45 % MS) |

**Veredicto:** **C44 primero.** Kraken gana el duelo de autos planos (+14 %), pero Caitlyn no es un ADC de autos planos. C44 multiplica su Headshot y su R gracias al AD plano y Magnification, además de permitirle pokear desde arbustos con First Strike de forma segura.

---

## 3. BUILD FINAL RANURA POR RANURA

| Slot | Ítem | Justificación matemática |
|---|---|---|
| Botas | **Berserker's → Gunmetal** | +15 % AS sobre T2 por 1 000 g; +5 % LS; 12 HP/golpe. Estrictamente dominante. |
| 1 | **Hexoptics C44** (2 900) | 55 AD + Magnification +10 % permanente. Su rango base 650 garantiza el máximo bono. |
| 2 | **Infinity Edge** (3 400) | A 100 % crit, el salto 200→230 % multiplica Headshot (+30 % AD extra) y R (+9 % mult global). |
| 3 | **Lord Dominik's Regards** (3 300) | Cierra 100 % crit exacto + 35 % pen + Giant Slayer. Obligatorio vs el meta de tanques. |
| 4 | **Rapid Firecannon** (2 650) | +150 rango (llega a 800). Permite detonar cristales de torreta y procar Headshots desde la niebla. |
| 5 | **Bloodthirster** (3 200) | 75 AD + 15 % LS. Sustain para sobrevivir a los dives post-lane. |

### Matriz del último slot (situacional)
| Situación | Ítem | Coste | Impacto medido |
|---|---|---|---|
| **Default (sustain)** | **Bloodthirster** | 3 200 | 410 HP/s + escudo Ichorshield |
| CC duro + AP | Mercurial Scimitar | 3 100 | QSS + 40 MR + 12 % LS |
| Burst AD / asesinos | Guardian Angel | 3 200 | Revivir (sin crit desperdiciado) |
| 3+ Tanques / Curación | Mortal Reminder | 3 000 | Reemplaza LDR; mantiene 100 % crit + GW 50 % |

---

## 4. RUNAS · HECHIZOS · HABILIDADES

### Keystone: Lethal Tempo / First Strike
- **Lethal Tempo:** Para composiciones donde necesitas DPS sostenido en teamfights largos. La bala escala con su AS bonus intrínseco (0.84).
- **First Strike:** La opción de **poke y lane bully**. Iniciar combate con un Headshot desde arbusto/niebla otorga +7 % de daño verdadero y oro extra. Sinergia brutal con su rango.
### Secundarias
| Slot | Runa | Valor estimado |
|---|---|---|
| Precisión | **Legend: Alacrity** | +21 % AS → Headshots más frecuentes |
| Precisión/Dom | **Brutal** | 5 + 6 % AD bonus ≈ +45 DPS constante |
| Precisión | **Coup de Grace** | +8 % a <40 % HP — convierte su R en ejecución garantizada |
| Resolve | **Bone Plating** | Anti-burst lane (Draven/Lucian) |

### Hechizos: Flash + Heal / Barrier
Caitlyn es estática en peleas. Barrier es preferible en Diamond+ contra comps de burst mágico (ej. Syndra, Diana).

### Orden de habilidades
**Q → W → E** · R en 5/9/13.
- Q max: waveclear y poke principal.
- W segunda: más cargas y duración de trampas para controlar objetivos y river.
- E última: el slow fue nerfeado a 1 s, su valor es puramente defensivo (red de seguridad).

---

## 5. COMPARACIÓN CONTRA LAS ALTERNATIVAS

### Tabla maestra (nivel 15, 100 % crit, vs 120 arm)
| Build | Oro | AD | AS | Crit | Pen | 1v1 | Burst R | vs Tanque |
|---|---|---|---|---|---|---|---|---|
| **ÓPTIMA C44 (propuesta)** | 17 650 | 359 | 2.08 | 100 % | 35 % | **1 605** | **1 515** | **1 340** |
| Meta 7.2 (sin escalado crit) | 17 200 | 340 | 2.25 | 75 % | 35 % | 1 240 | 980 | 1 020 |
| Ruta Lethality (Armorcrusher) | 16 800 | 385 | 1.45 | 0 % | 40 % | 1 450 | 1 100 | 650 |

---

## 6. PLAN DE JUEGO

### Early (0:00 – 9:00)
- **Start:** Long Sword (500 g).
- **Lvl 1:** Q para pushear y llegar a lvl 2 primero. Coloca W en los arbustos de la river o en el carril para restringir movimiento.
- **Headshots:** Farmea con autos, guarda el Headshot para el trade con el support enemigo o el ADC.
- **Bajo presión:** Si te divean, usa E (90 Caliber Net) + Q en el aire para el combo rápido.

### Mid (9:00 – 16:00)
- **Min 10:00:** mejora Berserker's → **Gunmetal Greaves** (+1 000 g, mismo slot).
- **Pico 1 (C44 + IE, ~13 min):** Tu Headshot ahora hace ~800 de daño pre-mitigación. Busca picks con W + R.
- **Cristales:** cada ~50 s la torreta acumula cristales. Con RFC (800 de rango), dispara un auto desde la niebla para detonar **~1 300 de daño verdadero** y retrocede. Es presión gratuita.

### Late (16:00+)
- **Posicionamiento:** 800 de rango con RFC. Nunca entres en el radio de los engages enemigos.
- **Teamfight:** Coloca W en las entradas de la jungla o alrededor de objetivos (Baron/Dragon). Si alguien pisa, **R + Headshot** = baja instantánea de squishies.
- **Contra-ventana:** enemigos con Chainlaced Crushers (30 % tenacidad) reducen el impacto de tu W, pero tu R sigue siendo imparable.

---

## 7. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS

### Fuentes primarias (mandan)
| Fuente | Acceso | Qué aporta |
|---|---|---|
| Notas oficiales 7.3 (21/09/2026) | wildrift.leagueoflegends.com | Sistema crit 200/230 %, escalado de Headshot/R, AS cap 3.0, apéndice AS |
| Notas oficiales 7.2 | wildrift.leagueoflegends.com | Fin encantamientos, botas T2/T3, min 10:00 |

### Discrepancias detectadas y resolución
| Tema | Fuente A | Fuente B | Resolución |
|---|---|---|---|
| **Base Bonus AS** | Apéndice final: **0.2** | Sección Caitlyn y ejemplo oficial: **0.28** | **Mandan la sección específica y el ejemplo oficial (0.28).** El apéndice tiene errata conocida. |
| Lethal Tempo (ranged) | wr-meta: 4.8 % | Notas 7.3: **6.4 %** | Mandan las notas oficiales |

---

## APÉNDICE A — POOL DE ÍTEMES DEL ROL: veredicto para Caitlyn

| Ítem (oro) | Veredicto | Nota |
|---|---|---|
| Hexoptics C44 (2 900) | ✅ Core 1 | Magnification +10 % permanente (rango 650) |
| Infinity Edge (3 400) | ✅ Core 2 | Multiplica Headshot y R |
| Lord Dominik's Regards (3 300) | ✅ Core 3 | Pen 35 % + GS |
| Rapid Firecannon (2 650) | ✅ Core 4 | +150 rango = 800 de alcance seguro |
| Bloodthirster (3 200) | ✅ 6.º default | Sustain + AD plano |
| Mortal Reminder (3 000) | ✅ Reemplaza LDR vs curación | Mantiene 100 % crit |
| Guardian Angel (3 200) | ✅ 6.º vs AD burst | Revivir |
| Mercurial Scimitar (3 100) | ✅ 6.º vs CC | QSS + MR |
| Galeforce (3 100) | ❌ | 25 % crit muerto |
| Essence Reaver (3 000) | ❌ | Spellblade < multiplicador de IE |
| The Collector (3 000) | ❌ | Pen plana ineficiente en late |
| Manamune (2 900) | ❌ | Sin problemas de maná |

---

## APÉNDICE B — RUTAS DE COMPRA

```text
DEFAULT (máximo burst y control):
LS → Pickaxe/Noonquiver → C44 (7-8') → Berserker's (9') → IE (12-13')
→ ⬆️ Gunmetal T3 (13:30') → LDR (17') → RFC (19') → BT (21')

ANTI-PRESIÓN (lane difícil / poke enemigo):
LS → Stormrazor (8') → Berserker's → C44 → ⬆️ Gunmetal → IE → LDR → BT

VS 3+ TANQUES / CURACIÓN:
Default pero LDR → Mortal Reminder (mantiene 100 % crit + GW 50 %)

VS CC DURO / BURST AP:
Default pero BT → Mercurial Scimitar / Guardian Angel
```

---

## Pie de página

*Reporte generado el 28/09/2026 con datos del parche 7.3 (21/09/2026). WR-LAB v1.4. Las cifras de DPS son pre-mitigación y comparativas — el valor absoluto importa menos que las diferencias relativas entre builds, que son robustas a los supuestos. Si Riot publica un 7.3a/b (hotfix), regenerar datos antes de publicar.*

**Referencias y créditos**
- Notas oficiales del parche 7.3 (21/09/2026) y 7.2 (08/07/2026) — © Riot Games, Inc. (wildrift.leagueoflegends.com). Fuente primaria de todos los cambios sistémicos, escalado de crítico en habilidades, apéndice de Attack Speed y valores de ítems modificados.
- Base de datos de ítems, runas y fichas de campeón — wr-meta.com (proyecto comunitario de JLVD DEV), sincronizada al 24/09/2026. Fuente secundaria para stats no tocados por el parche.
- Modelo matemático, Leyes 0-7 y validaciones — WR-LAB (laboratorio propio), construido sobre las fuentes anteriores.

**Aviso legal:** Wild Rift y League of Legends son marcas registradas de Riot Games, Inc. Este documento es una guía de comunidad con fines educativos, **no está afiliado, patrocinado ni respaldado por Riot Games**. Los nombres de ítems, campeones y estadísticas pertenecen a sus respectivos dueños. El análisis y las conclusiones son trabajo original del autor apoyado en WR-LAB.