# APÉNDICE — ESCALADO DE TAMAÑO (SIZE) en Wild Rift 7.3
### Cho'Gath · Malphite · Shyvana — qué es real, qué es fantasía y cómo se construye

> Investigación completa: todas las fuentes de tamaño del juego (grep exhaustivo de la BD de 186 ítems + fichas de campeones + notas 7.2/7.3). Fecha: 25/09/2026.

---

## 1. LA VERDAD INCÓMODA PRIMERO

**El tamaño, por sí solo, no da defensa.** No reduce daño, no da vida ni resistencias. Lo que hace:
1. **Hitbox más grande**: bloqueas skillshots con el cuerpo (peel real para tus carries) — pero también te vuelves más fácil de golpear (irrelevante si ya eres el tanque).
2. **Intimidación/legibilidad**: el enemigo percibe mal tus rangos de habilidad y su posicionamiento.
3. **EXCEPCIÓN ÚNICA de tu lista: en Cho'Gath el tamaño ES poder mecánico** (ver §3).

Cuando los jugadores dicen "escalar tamaño para ser underivable en teamfights", lo que realmente están escalando son los **paquetes de stats que vienen CON el tamaño**: vidas bonus, resistencias bonus ×1.3, tenacidad, escudos y curas. El tamaño es el indicador visual de que tu build de "ventanas de combate" está online. Y ahí está la clave matemática:

## 2. LAS 5 FUENTES DE TAMAÑO DEL JUEGO (7.3)

| Fuente | Coste | Tamaño | QUÉ MÁS DA (esto es lo que importa) | Tipo |
|---|---|---|---|---|
| **Amaranth's Twinguard** | 3200 | **+20 %** (5 stacks, 1 s c/u en combate) | +300 HP, 50/50 resist → **al máximo: +30 % armadura y +30 % MR y +20 % tenacidad** | Permanente en fight |
| **Gargoyle Stoneplate** | 2900 | +tamaño durante el activo | 200 HP, 45/45, **activo: escudo = 100 + 90 % de tu vida BONUS** (2.5 s, CD 60) | Activo (burst window) |
| **Sterak's Gage** | 3200 | +tamaño 8 s (al activar Lifeline) | 400 HP, 20 % tenacidad base, **+50 % de tu AD base como AD bonus**, Lifeline: escudo = 75 % de vida bonus (<35 % HP, CD 70) | Reactivo (<35 % HP) |
| **Mantle of the Twelfth Hour** | 2550 | +10 % por 5 s (<30 % HP) | **600 HP**, 20 AH, Lifeline: +200-300 HP, +10 % MS, +20 % tenacidad y **regenera 200-400 + 120 % armadura + 120 % MR** (CD 70) | Reactivo (<30 % HP) |
| **Feast de Cho'Gath** | gratis (R) | **+6 % por stack, cap +135 %** | +80/120/160 HP por stack, **+7.7 rango de ataque por stack (cap +75)**, +2.5 rango de R (cap +25), **anchura de E escala con tamaño** | Permanente, infinito* |

\* stacks de minions/monstruos no-épicos: cap 6; de campeones y épicos: **sin cap**.

**Interacción crítica:** Sterak's + Mantle + Twinguard + Gargoyle = **4 ventanas defensivas independientes** (2 reactivas por umbral de vida, 1 de combate prolongado, 1 activa). Bien temporizadas, un tanque pasa de "30 % HP" a "3000 de escudo + 30 % más resistencias + tenacidad 70 % + regen masiva" en 2 segundos. ESO es lo que el enemigo percibe como "imposible de matar" — no el modelo 3D más grande.

## 3. CHO'GATH — el único donde tamaño = daño (matemática completa)

Su R Feast convierte CADA stack en un compuesto de 5 stats. Con R rank 3 (+160 HP/stack):

| Stacks | HP bonus de Feast | Tamaño | Rango extra | R (true damage, con AP 150 y +1500 HP de ítems) |
|---|---|---|---|---|
| 6 (cap de minions) | +960 | +36 % | +46 | 921 |
| 10 | +1600 | +60 % | **+75 (cap)** | 985 |
| 15 | +2400 | +90 % | +75 | 1065 |
| 22 | **+3520** | **+132 %** | +75 | **1177** |

- **R = 600 + 50 % AP + 10 % de tu HP BONUS como daño VERDADERO** → cada ítem de vida double-dipea (tanqueo + ejecutor). A 22 stacks + Heartsteel, la R ejecuta ~1200 de daño verdadero.
- **E Vorpal Spikes: la anchura del cono escala con su tamaño** → a +132 % su E barre teamfights enteras.
- **Rango de ataque +75** = de melee a "casi ranged" (125→200): golpea desde fuera del alcance de muchos melee.
- **Heartsteel (3000g) es su mejor amigo**: golpe cada 20 s por campeón = 140 + 3.5 % vida máx, y **convierte 15 % del daño en HP permanente** → bola de nieve infinita que alimenta la R (+34 HP/proc a 2500 HP; +58 a 7000).
- **Ruta de build (preview del reporte futuro):** Chainlaced/Armored T3 → Heartsteel → Gargoyle → Twinguard → Liandry's/Cryptbloom (AP para R y E) → Mantle. Roles: jungla (Feast temprano con smite-kill de 1200 true vs monstruos) o mid/top.
- **Economía de stacks 7.3:** monstruos épicos más contestables (duración estándar, Baron mid-game buffeado) → cada épico = 1 stack sin cap. Prioriza dragones/herald aunque pierdas CS.

## 4. MALPHITE — la "armadura es daño" (y por qué lo banean 21.9 %)

Meta actual: **WR 52.17 %, ban 21.89 %** — el tanque más respetado del parche. Su kit convierte armadura en TODO:
- Base armor **49 (+5/nivel) = 119 a nivel 15** (la más alta de tu roster).
- **W pasiva:** +25/30/35/40 % de armadura extra; **W activa:** golpes en cono 20-50 + 20 % AD + **15 % armadura (7.3a; era 20 %)** (primer golpe: 40-100 + 40 % AD + **40 % armadura**).
- **E:** 60-210 + 45 % AP + **40 % armadura (7.3a; era 45 %)** AoE + **slow de AS 35-50 %** (anti-ADC duro: −50 % AS a una Jinx/Kalista enemiga = −40 % de su DPS).
- **Iceborn Gauntlet:** el campo de hielo **crece con tu armadura** (AoE de slow permanente).
- P Granite Shield: **11 % de vida máx** como escudo fuera de combate (con 3500 HP = 385 gratis cada 6 s).

**Números de la ruta armor-stack (nivel 15):**

| Etapa | Armadura | E (mágico AoE) | W golpe sostenido | W primer golpe | Escudo pasiva |
|---|---|---|---|---|---|
| Iceborn+Thornmail+Armored Advance | ~274 | 320 | 91 | 210 | 276 |
| + W rank 4 (+40 % bonus armor) | ~336 | 344 | 100 | 234 | 276 |
| + Gargoyle/Twinguard situacional | ~386 | **364** | **108** | **254** | 276+ |

> [!WARNING]
> **7.3a (29-sep-2026) nerfeó a Malphite:** ratio de armadura de W 20→15 %, de E 45→40 % y R CD 75/70/65→85/80/75 s.
> La tabla de arriba YA refleja el hotfix. Su identidad armor-stack sobrevive (sigue siendo el tanque con más ban),
> pero su pico de daño y la frecuencia de su wombo bajaron ~5-8 % / +10 s de CD.

**El tamaño en Malphite:** solo viene de ítems (Gargoyle activo + Twinguard + Sterak's si va fighter). NO tiene tamaño innato — su fantasía de "gigante" es 100 % armadura. Build comunidad validada: **Iceborn → Plated/Mercury's T3 → Thornmail → Zeke's → Gargoyle** (runas Grasp+Demolish+Second Wind+Overgrowth). Ajustes del modelo: vs comps AD puras, **Armored Advance** sobre Thornmail 2.º; Twinguard como 6.º capstone (con su uptime de combate permanente es el ítem de tamaño más consistente del juego). Zeke's potencia a tus carries AP (Diana/Yunara) con su R.

## 5. SHYVANA — tamaño condicional + Sterak's

- Forma dragón de la R: verificar en juego si modifica hitbox (la ficha no lista tamaño; en la transformación PC sí crece visualmente).
- Su ruta de tamaño real es **Sterak's Gage**: Heavy Handed le da **+50 % de su AD base como AD bonus** (62+4.6×14 = 126 base → **+63 AD**) + Lifeline (75 % de vida bonus como escudo) + tamaño/tenacidad 8 s al activarse — perfecto para su patrón de dive (entra, baja de 35 %, escudo + tamaño + sigue pegando).
- Preview de build (reporte completo pendiente): Gunmetal/Plated T3 → **Dusk and Dawn** (comunidad 1.º) → BotRK/Terminus (on-hit) o Rabadon's/Nashor's (AP R-burst) → Sterak's → Gargoyle/Wit's End.
- Con Shyvana el tamaño es cosmetic-utility (peel/intimidación en plena pelea); su "no-mueras" viene del escudo de Sterak's + W (Burnout) + curas de Dusk and Dawn.

## 6. CÓMO INTEGRAR ESTO EN SUS REPORTES COMPLETOS (protocolo)

Cuando pidas el reporte de Cho'Gath, Malphite o Shyvana, el análisis añadirá:
1. **Columna "ventanas de supervivencia"** por build: cuántos segundos de efectividad extra suman Sterak's/Mantle/Gargoyle/Twinguard y con qué CD (la métrica real detrás del "tamaño").
2. **EHP efectivo en ventana** (vida × multiplicador de mitigación con Twinguard al máximo + escudos), no solo EHP estático.
3. Para Cho'Gath: **curva de stacks por minuto** (minions cap 6 + épicos + campeones) y el execute de R resultante en cada punto de la partida.
4. Regla de compra: **Twinguard cuando las fights duran 5+ s** (5 stacks = 5 s), **Gargoyle cuando te burstean en <2 s** (activo inmediato), **Sterak's para fighters que bucean**, **Mantle para tanques que ya tienen 600 HP de base y sufren execute**.

## 7. FUENTES

Grep de "size/tamaño" sobre los 186 ítems de `items_7.3.csv` y las 12 fichas de campeones · notas oficiales 7.3 (Mantle: HP 200→600 y Twinguard: +300 HP base, rework de resistencias) · fichas wr-meta de Cho'Gath (R Feast completo), Malphite (W/E ratios de armadura) y Shyvana. Discrepancia registrada: el texto "Gains 9 Armor (25/30/35/40 %)" de la W de Malphite es ambiguo (¿9 + % del bonus o % del total?) — modelado como % del bonus (conservador), verificar en juego.
