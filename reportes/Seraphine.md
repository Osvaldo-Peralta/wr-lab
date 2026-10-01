---
tags:
  - Soporte
version: 1
Status: Beta
---
**Fecha del análisis:** 27 de septiembre de 2026  

---

<!-- WRLAB-VERIF:7.3a:START — generado por model/update_reports.py · no editar a mano -->
> [!NOTE] ✅ SIN IMPACTO Verificación automática (30/09/2026) — **NO requiere regeneración — hotfix 7.3a**
> **Cambios directos a Seraphine:** ninguno en 7.3a.
> **Modelo:** sin hook cuantitativo (sin modelo cuantitativo para este campeón/arquetipo) → triage por intersección (champion/ítems/sistemas). Métricas publicadas sin cambios medibles.
> **Build publicada:** no extraíble automáticamente del formato del vault → triage cualitativo (intersección champion/ítems/sistemas).
> **Veredicto:** ✅ SIN IMPACTO — build, ruta de compra y veredictos siguen vigentes; este bloque es la constancia de verificación.
<!-- WRLAB-VERIF:7.3a:END -->

## 0. RESUMEN EJECUTIVO

Seraphine en el parche 7.3 se consolida como un **Soporte-Mago Híbrido (Enchanter-Caster)**. Su valor no reside en el DPS sostenido de autoataques (su AD es bajo, ~52 base), sino en la **eficacia de sus habilidades escaladas por AP**, su capacidad de **curación/escudo masivo vía Mantra (R)** y el control de zona con **Slow/Silence**.

### Tabla de Orden de Compra (Build Estándar Soporte/Mid)

| # | Ítem (Español / Inglés) | Oro Acumulado | Minuto Típico | Justificación Clave |
|:-:|:------------------------|:-------------:|:-------------:|:--------------------|
| 1 | Botas de Maná → Zapatos de Hechicera (*Boots of Mana -> Spellslinger's Shoes*) | 1200 - 1500 | 8:00 | Regeneración de maná crítica para spameo de habilidades. El upgrade añade AH/AP. |
| 2 | Lamento Ahogado (*Morellonomicon*) | 3000 | 12:00 | Penetración mágica + Grievous Wounds (anti-cura). Core defensivo/ofensivo vs tanques curativos. |
| 3 | Sombrero Mortal (*Deathcap*) o Tormento de Liandry (*Liandry's Anguish*) | 3900 - 4200 | 16:00 | **Deathcap**: Máximo burst si van ganando. **Liandry**: Daño persistente vs tanques con mucha vida. *Recomendado: Deathcap para impacto inmediato en teamfights.* |
| 4 | Bastón de Ánimas (*Bastion of Spirits*) / Ardent Censer | 2600 | 20:00 | Escudo masivo para proteger al carry tras usar R/Q. Si el carry es on-hit (Vayne/Kog'Maw), usar **Ardent Censer**. |
| 5 | Reloj de Arena de Zhonya (*Zhonya's Hourglass*) | 3500 | 24:00 | Supervivencia ante asesinos/burst. Activa el efecto de Mantra en aliados cercanos sin morir. |
| 6 | Varita Vieja de Nashor (*Nashor's Tooth*) [Solo Mid/Hybrid] O **Guardián de la Aurora** (*Aurora Guard*) / **Cetro de Cristal de Rylai** (*Rylai's Crystal Scepter*) | 3000+ | 28:00 | **Mid:** Nashor permite autos con AP on-hit. **Sup:** Rylai/Aurora para CC extra y supervivencia extrema. *Para soporte puro: Rylai's.* |

**Total Oro Estimado:** ~17,000 - 18,000 oro (dependiendo de la ruta de botas y upgrades).

**Runas Recomendadas:**
*   **Keystone:** **Cometa Arcano** (*Arcane Comet*) para poke seguro, o **Invocar Aery** (*Summon Aery*) si buscas escudos/daño constante a larga distancia. **Conquistador** es viable solo en rol Mid agresivo, pero pierde consistencia en soporte.
*   **Secundarias:** **Brújula Inspiritu** (*Inspire*) para AH temprano, o **Calzado Mágico** (*Magical Footwear*) si vas botas más tarde.
*   **Hechizos de Invocador:** **Flash + Ignite** (Mid/Burst) o **Flash + Exhaust** (Support/Utility).

**Orden de Habilidades:** Maxear **Q (Song of Sorrow)** primero para clear/poke, luego **E (High Note)** para slow/movilidad, y **W (Surround Sound)** último (el punto de talento en nivel 6 potencia todas). La pasiva **Mantra (R)** es prioritaria en niveles 6, 11, 16.

---

## 1. CONTEXTO DEL CAMPEÓN EN ESTE PARCHE (7.3)

### Cambios Directos e Indirectos
*   **Botas Tier 3 (Min 10:00):** Las botas evolucionan automáticamente o mediante componente. Para Seraphine, **Spellslinger's Shoes** (upgrade de Boots of Mana) es crucial porque proporciona **Ability Haste (AH)** y **AP**, mejorando la rotación de habilidades potenciadas por R.
*   **Grievous Wounds (Heridas Graves):** Con el nerfeo de la cura general y el aumento de sustain en muchos carries/tanques, **Morellonomicon** se vuelve casi obligatorio como segundo item para negar curas pasivas y activas.

### ¿Escalan sus habilidades con algo específico?
*   **Q, W, E:** Escalan puramente con **AP**.
*   **Pasiva (Chorus Effect):** Amplifica el efecto de Q/E/W cuando se usan dentro del área de R (Mantra).
    *   Q-Mantra: Mayor rango y daño AoE.
    *   E-Mantra: Slow más fuerte y silencio breve.
    *   W-Mantra: Curación/Escudo masivo en área.
*   **Autoataques:** Escalan con AD bajo. Solo relevantes para last-hitting minions o harass mínimo. **Ignorar cualquier ítem que dé AD/Crítico/AS como prioridad.**

---

## 2. FICHA MATEMÁTICA (SPEC)

Basado en `data/estructurada/campeones/seraphine.md` y apéndice oficial 7.3:

| Stat | Valor Nivel 1 | Growth por Nivel | Valor Nivel 15 (Sin Items) | Nota |
|:-----|:--------------:|:-----------------:|:--------------------------:|:-----|
| **AD Base** | 52 | 3.64 | 102.6 | Irrelevante para build core. |
| **HP Base** | 600 | 112 | 2168 | Muy frágil. Necesita shields/vida. |
| **ARM Base** | 34 | 4.71 | 100 | Baja resistencia física. |
| **MR Base** | 36 | 1.20 | 52.8 | Resistencia mágica decente inicial. |
| **MS Base** | 360 | 0 | 360 | Lenta sin botas/activos. |
| **AS Ratio** | 0.699 | N/A | N/A | **No usar.** Su daño no depende de esto. |
| **Mana Base** | 435 | 49 | 1121 | Alto consumo. Requiere gestión/maná items. |
| **Range** | 550 | N/A | 550 | Rango corto para ser mago. Posicionamiento clave. |

**Modificadores de Kit (Estimación de Ratios AP):**
*   **Q (Song of Sorrow):** ~60% AP por hit (hasta 3 hits). Total potencial ~180% AP.
*   **W (Surround Sound):** Escudo/Cura basado en % HP max + AP ratio (~40-60% AP).
*   **E (High Note):** Silencio/Slow. Daño bajo, utilidad alta. ~30% AP.
*   **R (Light Chorus):** Daño inicial + amplificación de efectos. El daño directo es moderado, pero el **valor utilitario** (slow/silencio/curación extra) es infinito si aciertas el area.

**Arquetipo:** `enchanter-mage` (Soporte de Area Control & Sustain).

---

## 3. MODELO DE DAÑO Y UTILIDAD (DERIVACIÓN)

Dado que Seraphine no es un DPS tradicional, modelamos **"Impacto por Rotación"** (Daño + Utilidad efectiva en 5 segundos de teamfight).

### Supuestos del Modelo:
1.  **Rotación Óptima:** R (Mantra activo) -> Q (potenciado) -> E (potenciado) -> W (potenciado) -> Autos básicos mientras dura el slow.
2.  **Cooldown Reduction (CDR):** Objetivo 40-45% AH para lanzar R cada ~60-70s y Q/E/W constantemente.
3.  **Uptime de Mantra:** Se asume que R está disponible y se usa en el 80% de las peleas importantes (gracias a AH).
4.  **Penetración Mágica:** Se calcula contra enemigos con 50 MR promedio. Morellonomicon da 20% pen fija. Void Staff (si fuera necesario) daría 40%. Dado su rol, **Morelli** suele bastar combinado con alto AP bruto.

### Comparativa de Builds (Nivel 15, Full Items)

| Build | Componentes Principales | AP Bruto | AH (%) | Vida/Escudo Est. | Impacto Teamfight (Score 1-10) | Comentario |
|:------|:-----------------------|:--------:|:------:|:----------------:|:------------------------------:|:-----------|
| **A. Meta Burst (Recomendada)** | Spellslinger, Morelli, Deathcap, Zhonya, Rylai, Sorcerer's Shoes (o upgrade) | ~380 | 45% | Medio-Alto | **9.5** | Maximiza daño de Q-E y supervivencia con Zhonya. Rylai añade slow permanente post-Q. |
| **B. Sustain Puro** | Spellslinger, Morelli, Shurelya's, Ardent Censer, Redemption, Banshee's Veil | ~250 | 30% | Alto | 7.0 | Menos daño personal, más buff al equipo. Ideal si tu ADC es Vayne/Jinx (on-hit). |
| **C. Hybrid Mid (Agresiva)** | Sorcerer's Shoes, Luden's Echo, Deathcap, Zhonya, Shadowflame, Void Staff | ~420 | 40% | Bajo | 8.5 | Mucho poke y burst. Riesgosa en soporte, viable en Mid lane contra magos frágiles. |
| **D. Anti-Tank (Late Game)** | Spellslinger, Morelli, Liandry's, Deathcap, Zhonya, Spirit Visage | ~350 | 35% | Alto | 8.0 | Liandry quema tanques. Spirit Visage aumenta tu propia cura/escudo. Mejor vs composiciones muy defensivas. |

**Análisis Multiplicativo (Build A vs B):**
*   La Build A tiene un **+52% de AP efectivo** sobre la B.
*   El daño de Q-Mantra escala linealmente con AP. Un salto de 250 a 380 AP representa un aumento de ~130 puntos de daño por hit de Q (x3 hits = 390 daño extra instantáneo).
*   La utilidad de Rylai (slow adicional) mantiene a los enemigos en el área de tu E-Mantra (silencio), aumentando el tiempo de exposición a tu daño y al de tu equipo.

---

## 4. SELECCIÓN DE ÍTEMES (POOL ANALYSIS)

### ✅ Núcleo Obligatorio
1.  **Zapatos de Hechicera (*Spellslinger's Shoes*):** Única opción seria. Proporciona AH y AP. Evitar Ionian (demasiado riesgo) o Plated (innecesario para caster).
2.  **Lamento Ahogado (*Morellonomicon*):** Esencial por la penetración mágica y las Heridas Graves. En 7.3, con la meta de sustain, omitirlo es jugar con desventaja.

### 🟡 Situacionales (Slot 3-4)
3.  **Sombrero Mortal (*Deathcap*):** Si tienes >300 AP antes de comprarlo, este item multiplica tu daño drásticamente. Es el capstone de daño.
4.  **Tormento de Liandry (*Liandry's Anguish*):** Si el enemigo tiene >3 tanques con >2500 HP. El quemado porcentual supera al flat damage de Deathcap en peleas largas.
5.  **Ardiente Incensario (*Ardent Censer*):** **SOLO** si tu ADC es Vayne, Kog'Maw, Twitch o Zeri (On-Hit). Potencia sus autos con tu W/Q. De lo contrario, inútil para ti.
6.  **Shurelya's Battlesong:** Si necesitas iniciar peleas o escapar rápidamente. El MS activo es valioso para reposicionar tu R.

### 🔵 Defensa / Utilidad Final (Slot 5-6)
7.  **Reloj de Arena de Zhonya (*Zhonya's Hourglass*):** La mejor defensa para casters. Te salva de Assassin dives (Akali, Talon, Zed) y permite usar tus skills sin morir.
8.  **Cetro de Cristal de Rylai (*Rylai's Crystal Scepter*):** Excelente para mantener el control de zona. El slow se aplica con Q y E, facilitando que tu equipo siga atacando.
9.  **Velo de la Banshee (*Banshee's Veil*):** Contra mucho CC puntual (Malphite ult, Leona stun). Bloquea una habilidad importante.
10. **Redención:** Curación global y daño en área. Bueno para objetivos neutrales (Baron/Dragon fights).

### ❌ Evitar Absolutamente
*   **Filo Infinito (*Infinity Edge*), Runaan's Hurricane, Kraken Slayer:** No escalan con su kit. Desperdicio de oro.
*   **Guinsoo's Rageblade:** Aunque da AP, su foco es AS/On-Hit. Seraphine no hace suficientes autos para justificarlo frente a un item de AP puro.
*   **Ítems de Vida pura (Heartsteel, Sunfire):** No aportan AP suficiente para que sus habilidades sean relevantes.

---

## 5. ANÁLISIS DEL PRIMER ÍTEM Y TIMING

**Inicio de Partida:**
*   **Item Start:** *Ancient Coin* (Soporte) o *Doran's Ring* (Mid).
*   **Consumibles:** 2 Health Potions + 1 Control Ward (Soporte) / Corrupting Potion (Mid).

**Primer Recall (Objetivo: 1200-1400 Oro):**
*   Comprar **Botas de Maná (*Boots of Mana*)** + *Amplifying Tome*.
*   *Justificación:* El maná es vital para no quedarse seco en la fase de laning intentando pokear con Q. Las botas permiten volver rápido a línea.

**Segundo Item Completo (Minuto 10-12):**
*   Completar **Zapatos de Hechicera (*Spellslinger's Shoes*)** o ir directo a **Morellonomicon** si las botas están completas.
*   *Nota:* En 7.3, el upgrade de botas es automático o barato. Prioriza tener el componente de AP (Needlessly Large Rod) listo para Morelli.

**Timing de Poder (Power Spike):**
*   **Nivel 6 (R disponible):** Tu primer gran spike. La combinación R+E+Q puede matar a un squishy o salvar a un aliado.
*   **Minuto 14-16 (Morelli + Deathcap parcial):** Aquí es donde tu daño empieza a doler realmente. Antes de esto, eres utility pura. Después, eres una amenaza letal.

---

## 6. MATRIZ SITUACIONAL DEL ÚLTIMO SLOT

| Escenario Enemigo | Último Slot Recomendado | Razón Matemática/Táctica |
|:------------------|:------------------------|:-------------------------|
| **Muchos Asesinos (Zed, Akali, Talon)** | **Zhonya's Hourglass** | Inmunidad 2.5s. Permite esperar a que pase su combo y luego contraatacar con R+W. |
| **Tanques Altos HP (Ornn, Malphite, Shen)** | **Liandry's Anguish** o **Void Staff** | Liandry si ya tienes Deathcap. Void Staff si tienen mucha MR (>100). El % de vida actual de Liandry ignora la armadura/vida plana. |
| **Mucho CC Chain (Leona, Nautilus, Amumu)** | **Mercury's Treads** (reemplazar botas) + **Banshee's Veil** | Limpieza de CC y bloqueo de iniciación. Prioriza la supervivencia para poder soltar tu R. |
| **Tu Equipo necesita Buffs (ADC On-Hit)** | **Ardent Censer** | Transforma tu W/Q en un multiplicador de DPS para tu carry. El valor de equipo supera al tuyo individual. |
| **Juego Largo / Late Game Extremo** | **Spirit Visage** o **Rabadon's Deathcap** (segunda copia imposible, así que **Shadowflame**) | Spirit Visage aumenta tu propia cura/escudo un 30%, haciéndote inmolable. Shadowflame penetra escudos mágicos. |

---

## 7. RUNAS Y HECHIZOS DETALLADOS

### Opción A: Soporte Estándar (Control & Poke)
*   **Keystone:** **Cometa Arcano (*Arcane Comet*)**.
    *   *Sinergia:* Tu Q dispara 3 proyectiles. Cada uno puede activar el cometa si estás lejos. Fácil proc.
*   **Rama Inspiración:** **Calzado Mágico** (oro gratis) + **Entrega Futura** (item gratis a los 15 min).
*   **Rama Brujería:** **Absorción de Vida** (sustain en lane) + **Truco Sucio** (penetración mágica tras usar summoner spell).
*   **Hechizos:** Flash + Ignite (para asegurar kills en level 2-3 con Q+E) o Flash + Exhaust (para defender al ADC).

### Opción B: Soporte Defensivo / Anti-Dive
*   **Keystone:** **Guardia Avanzada (*Guardian*)** o **Restricción (*Unsealed Spellbook*)**.
    *   *Guardian:* Escudo cuando un aliado cercano recibe daño. Combina bien con tu W.
*   **Rama Determinación:** **Fortaleza** + **Overgrowth** (vida extra) o **Revitalizar**.
*   **Hechizos:** Flash + Heal (si tu support no lo trae) o Flash + Cleanse (vs mucho CC).

### Opción C: Mid Lane Agresivo
*   **Keystone:** **Electrocutar (*Electrocute*)**.
    *   *Combo:* Q(1)-E(2)-Auto(3) = Electrocute proc rápido.
*   **Rama Inspración:** **Golpe Bajísimo** (burst extra) + **Paquete de Gafas** (visión).
*   **Hechizos:** Flash + Ignite.

---

## 8. PLAN DE JUEGO (EARLY / MID / LATE)

### Early Game (Minutos 0-8)
*   **Lane Phase:** Usa **Q** para pokear cuando el enemigo intente farmear. Mantén la distancia. No entres en cuerpo a cuerpo.
*   **Gestión de Maná:** No spammees Q sin objetivo. Cada Q cuesta maná significativo.
*   **Objetivo:** Sobrevivir, llegar a nivel 6, controlar visión con wards.
*   **Level 2 Combo:** Si tienes Ignite, Q -> Auto -> E (slow) -> Auto -> Ignite. Puede forzar flash o conseguir kill si el enemigo está mal posicionado.

### Mid Game (Minutos 8-15)
*   **Rotaciones:** Acompaña a la jungla o al midlaner. Tu **R** es una herramienta de gank poderosa.
*   **Teamfights Pequeñas (2v2, 3v3):** Intenta atrapar a 2+ enemigos con tu **R**. Luego lanza **E** (silencio) para evitar que usen skills defensivas, y **Q** para daño. Usa **W** para curarte o al aliado en peligro.
*   **Objetivos:** Ayuda a tomar Dragones/Heraldos. Tu clear speed con Q es decente.

### Late Game (Minutos 15+)
*   **Posicionamiento:** Quédate detrás de tu frontline/tanque. Tu rango es corto (550). Si te acercas demasiado, muere.
*   **Prioridad de Skills:**
    1.  **R:** Úsala para iniciar o responder a un engage enemigo.
    2.  **E:** Silencia al carry enemigo o al asesino que te salta.
    3.  **Q:** Daño AoE mientras están silenciados/lentos.
    4.  **W:** Cura de emergencia para ti o tu ADC.
*   **Zhonya's Play:** Si te saltan, activa Zhonya inmediatamente después de soltar R+E. Espera a que pase el burst y luego sigue atacando o huyendo.

---

## 9. VERIFICACIONES, DISCREPANCIAS Y SUPUESTOS

*   **Fuentes Primarias:** Notas oficiales WR 7.3 (21-Sep-2026). Estadísticas base de Seraphine confirmadas en wr-meta.com (24-Sep-2026).
*   **Discrepancias:** Ninguna crítica encontrada en el kit de Seraphine respecto a versiones anteriores inmediatas, excepto los ajustes globales de ítems (precios de Morelli/Zhonya estables).
*   **Supuestos del Modelo:**
    *   Se asume que el jugador tiene buena puntería con R (Light Chorus). Una R fallida reduce el impacto de la build en un 40-50%.
    *   Se asume que los enemigos no compran *Ether Wisp* o *Banshee's* tempranamente contra ti. Si lo hacen, prioriza **Void Staff** sobre Deathcap.
    *   El daño de autoataque se considera ruido (negligible) en comparación con el daño de habilidades.
*   **Contexto Meta:** Seraphine tiene un Win Rate de ~49.8% en Diamond+ como Soporte. Es un pick sólido pero requiere coordinación con el equipo para maximizar el valor de su R. No es un carry independiente.

---

## APÉNDICE A — POOL DE ÍTEMES PARA SERAPHINE (VEREDICTO)

| Ítem | Veredicto | Razón |
|:-----|:---------:|:------|
| **Spellslinger's Shoes** | ✅ CORE | AH + AP esencial. |
| **Morellonomicon** | ✅ CORE | Pen Mag + Grievous Wounds. |
| **Deathcap** | ✅ OPTIMAL | Multiplicador de AP puro. |
| **Zhonya's Hourglass** | ✅ DEFENSE | Supervivencia ante burst. |
| **Rylai's Crystal Scepter** | ⚠️ SITUATIONAL | Buen slow extra, pero menos AP que Deathcap. |
| **Liandry's Anguish** | ⚠️ SITUATIONAL | Solo vs tanques muy gordos. |
| **Ardent Censer** | ⚠️ SITUATIONAL | Solo con ADC On-Hit. |
| **Shurelya's** | ⚠️ SITUATIONAL | Para engages/disengages rápidos. |
| **Void Staff** | ❌ TARDÍO | Solo si >3 enemigos tienen MR alta. |
| **Infinity Edge** | ❌ EVITAR | Sin sinergia. |
| **Kraken Slayer** | ❌ EVITAR | Sin sinergia. |
| **Nashor's Tooth** | ❌ EVITAR (Sup) | Solo viable en Mid híbrido muy específico. |

---

*Reporte generado el 27/09/2026 con datos del parche 7.3. Modelo WR-LAB aplicado a arquetipo Enchanter-Mage.*