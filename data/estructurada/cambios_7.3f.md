# HOTFIX 7.3f — Cambios completos (publicado: 11-nov-2026, 10:00 UTC)

> **Fuente:** notas oficiales EN (wildrift.leagueoflegends.com/en-us/news/game-updates/wild-rift-patch-notes-7-3f/), leídas directamente el 12-nov-2026.
> **Estado en el lab:** APLICADO (v1.23) a `items_7.3.csv`, `analysis_batch2.py`, `chogath_model.py`, `chogath_jungla.py`, `senna_model.py`, `yuumi_agresiva_model.py` y `champspecs.py`. Base previa: 7.3+7.3a+7.3b+7.3d (v1.22).
> **Formato:** igual que `cambios_7.3d.md` (insumo de `update_reports.py`).

## REGISTRO DE 7.3c Y 7.3e (sin impacto en Summoner's Rift)

| Parche | Fecha | Contenido | Acción en el lab |
|---|---|---|---|
| 7.3c | 21-oct-2026 | Solo **AAA ARAM** (augments y modificadores de daño de modo) | Excluido (el lab es solo SR) |
| 7.3e | 04-nov-2026 | Solo **AAA ARAM** (augments K/DA, Star Guardian, Minion…) | Excluido |
| 7.3f | 11-nov-2026 | Balance de SR (10 campeones, 10 ítems), Sylas, jungla/Smite, ajustes de augments ARAM | **Aplicar** (abajo) |

El estado de datos pasa a **7.3+7.3a+7.3b+7.3d+7.3f** (7.3c y 7.3e sin cambios de SR).

## CAMPEONES

| Campeón | Tipo | Cambio |
|---|---|---|
| **Sylas** | NUEVO | Campeón nuevo. Las notas no traen stats: **sin datos en el lab** (AS, stats base, win rates, specs) hasta extraerlos de wr-meta |
| **Kalista** | NERF | Pierce (Q): daño base 70/135/200/265→**30/110/190/270** |
| **Viktor** | MIXTO | Siphon Power: inicial 45/60/75/90+30 % AP→**50/70/90/110+40 % AP**. Hextech Ray: inicial 75/120/165/210+30 % AP→**70/115/160/205+40 % AP**; Blastquake 30/70/110/150+60 % AP→**20/60/100/140+75 % AP**. Arcane Storm: ratio AP DoT 40→**35 %** |
| **Shen** | NERF | Stand United: CD 110/100/90→**120/110/100 s**; escudo base 170/340/510→**160/260/360** |
| **Irelia** | MIXTO | Ionian Fervor: AS 3–17 %→**11–25 %** (por nivel); daño 25–150+30 % AD bonus→**10–80+20 % AD bonus**. Bladesurge: ratio AD 65→**80 %**; curación 11/14/17/20 %→**9/11/13/15 %** AD |
| **Graves** | BUFF | Armadura base 36→**40**; armadura/nivel 4.5→**5** |
| **Akshan** | BUFF | Resistencia mágica base 30→**34** |
| **Lucian** | BUFF | Lightslinger: 2.º disparo ratio AD 40/50/60→**45/55/65 %**. Piercing Light: ratio AD bonus 100→**120 %** |
| **Rumble** | BUFF | Junkyard Titan: ratio AP del daño mágico de autos 20→**25 %**. The Equalizer: daño 700/1050/1400+200 % AP→**800/1200/1600+220 % AP** |
| **Kassadin** | NERF | Resistencia mágica base 38→**34**. Force Pulse: ratio AP 60→**50 %** |
| **Yasuo** | BUFF | Armadura/nivel 4.3→**5.2**. Sweeping Blade: daño base 70/80/90/100→**70/90/110/130** |

## ÍTEMS (aplicar a items_7.3.csv y a los motores)

| Ítem | Cambio |
|---|---|
| **Luden's Echo** | Discordic Echo: primer proyectil 75+8 % AP→**80+9 % AP**; proyectiles siguientes 20+1.2 % AP→**22.5+1.4 % AP** |
| **Rod of Ages** | Precio 2 700→**2 600**. Eternity: reembolso de maná 15→**20 %**. Veteran: HP por stack 15→**20**, maná por stack 30→**40** |
| **Lich Bane** | Velocidad de movimiento 5→**6 %**. Spellblade: ratio AP 45→**50 %** |
| **Morellonomicon** | Precio 2 650→**2 550** |
| **Hextech Rocketbelt** | Precio 2 700→**2 650**; vida 250→**300**. Protobelt: daño 100+10 % AP→**110+15 % AP** |
| **Liandry's Torment** | AP 70→**60** |
| **Bulwark of the Mountain** | Soulcast: oro por minuto 75→**60** |
| **Black Mist Scythe** | Soulcast: oro por minuto 75→**60** |
| **Eclipse** | AD 65→**60** |
| **Goredrinker** | AD 40→**45**; vida 350→**400** |

## MAPA Y SISTEMAS

| Sistema | Cambio |
|---|---|
| **Smite** | Daño base de quemadura 22–162→**18–158**; ratio de armadura bonus 25→**20 %**; ratio de resistencia mágica bonus 25→**20 %** |
| **Conservation** | Oro 40→**30**; oro cuando vas perdiendo 65→**55** |
| **Jungla** | Clear temprano más lento (sobre todo junglers tanque); sin cifras adicionales en la nota |
| **ARAM** | Ajustes a 12 augments y un bug fix de Battle Arsenal: excluidos del lab |

## APLICADO EN EL LAB

- `items_7.3.csv`: los 10 ítems de arriba. Luden's Echo: el texto base de wr-meta («140 + 15 %… hasta 3 enemigos») estaba desactualizado frente a las notas oficiales 7.3/7.3f; se reescribió con la mecánica oficial (80+9 % AP al objetivo principal y hasta 5 cercanos, +22.5+1.4 % AP por cada objetivo menos).
- **Filas que estaban atrasadas respecto a notas anteriores** (el motor ya las tenía bien; el CSV no): Yun Tal AS 25→35 % y Flurry 35 %/25 s (7.3a) · Death's Dance 3 200→3 300 (7.3a) · Blade of the Ruined King AS 35→30 % (7.3) · Tear of the Goddess 500→400 (7.3) · Warmog's umbral 950→1 250 (7.3b) · Whispering Circlet y Diadem Harmony 0.5→0.25 % (7.3a) · Statikk Shiv +7 stacks por auto (7.3b).
- Motores: `analysis_batch2.py` (Luden 80+9 %, Morello 2 550, Liandry 60 AP) · `chogath_model.py` (Liandry, Morello, Rod of Ages 2 600 con Veteran 200 HP/400 maná a 10 stacks) · `chogath_jungla.py` (burn de Smite 18–158) · `senna_model.py` (Morello, Liandry) · `yuumi_agresiva_model.py` (Roketbelt 2 650/300 HP, Protobelt 110+15 %, Liandry, Morello, Luden +5/+1 pt y +2.5/+0.2 pt por objetivo).
- `champspecs.py`: nota de Kalista con el nerf de Pierce (no entra en el DPS sostenido).
- `check_patch.py`: la lista de páginas candidatas del vigía ahora arranca en 7-3g (la anterior nunca probó 7-3d/e/f).
- Campeones: los cambios de stats base (Graves, Akshan, Kassadin, Yasuo) y de kit no se reflejan en CSV porque `champion_durability_7.3.csv` solo lista los cambios de 7.3 y se regenera desde la fuente; quedan documentados aquí.

## EXCLUSIVIDADES NUEVAS (v1.23)

Registradas en `items_exclusivos.csv` (aplican en `validate_slots`, optimizador, linter y generador):

- **spellblade** — Trinity Force, Divine Sunderer, Essence Reaver, Lich Bane, Dusk and Dawn, Iceborn Gauntlet. Confirmado por el autor para Divine Sunderer + Iceborn Gauntlet; el resto de pares, por analogía (misma pasiva), pendientes de confirmar en juego.
- **tear_of_the_goddess** — Tear of the Goddess, Manamune/Muramana, Archangel's Staff/Seraph's Embrace, Winter's Approach/Fimbulwinter. Texto oficial del ítem: «solo puedes llevar un ítem Tear of the Goddess a la vez».
- **immolate** — Hollow Radiance, Sunfire Aegis (supuesto A10 de Cho'Gath, ahora centralizado).

Candidatos sin confirmar (NO aplican): `items_exclusivos_candidatos.csv` (Lifeline, Energized, Annul, Terminus↔«Void Staff»/Cryptbloom, Icy, Eternity, Madness, Momentum, Thorns, ítems de soporte). Ninguna build publicada del lab viola los grupos aplicados ni los candidatos.

## DISCREPANCIAS A REGISTRAR EN data/FUENTES.md

1. **Sylas:** campeón nuevo sin datos (AS, stats, win rates).
2. **Luden's Echo:** el modelo `yuumi_agresiva_model.py` usa «(140+15 % AP)+3×(20+1.2 % AP)» como single-focus; la nota oficial 7.3 describe 75+8 % AP al objetivo principal más 20+1.2 % AP por cada objetivo menos (hasta 5). Se aplicaron solo los deltas de 7.3f sobre la estructura existente; la discrepancia es previa.
3. **Smite, ratio de armadura/RM bonus:** la nota oficial dice 25→20 %; `chogath_jungla.py` ya usaba 20 % antes de 7.3f. Confirmar qué reflejaba ese valor.
4. **Terminus:** su texto dice «Void Staff»; ese ítem no existe en la base 7.3 (probable renombre a Cryptbloom).
5. **Minions/jungla:** la nota 7.3f no trae cifras de la ralentización del clear.

## IMPACTO EN REPORTES/SPECS DEL LAB (triage 7.3f: 12 sin regeneración · 9 revisión acotada · 0 regeneración completa)

| Archivo | Exposición | Veredicto |
|---|---|---|
| `Cho'Gath - Titán de la Jungla` | Liandry −10 AP, Smite burn 18–158. Con `chogath_model` y `chogath_jungla`: la óptima no cambia; la build publicada de jungla mantiene su score (0.662) y DPS −0.7 %; sube la tasa de clear 0.1–0.2 s | ⚠️ REVISAR (cuantificado: Δ < 1 %, sin cambio de build) |
| `Cho'Gath - Titán del Barón` | Rod of Ages 2 600 con Veteran más fuerte, Liandry −10 AP: build publicada 0.680→0.682 y 100 g más barata | ✅ ANOTAR |
| `Heimerdinger`, `Mordekaiser`, `Ornn` | Liandry −10 AP en la build final; sin modelo cuantitativo (estimación aritmética: −10 AP sobre ~450–600 AP → ≤ −2 %) | ⚠️ REVISAR |
| `Nocturne` | Eclipse −5 AD en la build final (sin modelo de Eclipse; ≈ −1.2 % de DPS por ~−1.7 % de AD) | ⚠️ REVISAR |
| `Kalista` | Pierce nerf directo: solo recorta rangos bajos (rango 4: 265→270), sin impacto a nivel 15; no modelado | ⚠️ REVISAR |
| `Senna`, `Seraphine`, `Yuumi` | Black Mist Scythe: −15 g/min de Soulcast (≈ −225 g a los 15', ~1.7 % del oro de la build) | ⚠️ REVISAR |
| `Diana` (×2), `Norra`, `Rammus`, `Volibear` (×2) | Ítems de variantes/rechazados y cambios sistémicos de jungla | ✅ ANOTAR |
| `Caitlyn`, `Jinx`, `Sivir`, `Xayah`, `Yunara` | Sin ítems ni campeones tocados | ✅ SIN_IMPACTO |

## CHECKLIST (FRAMEWORK §E)

1. ✅ Notas 7.3f leídas de la fuente oficial (12-nov-2026). Pendiente: guardar `data/raw/patch73f.txt` y re-descargar `wrmeta_items.html` (red fuera del sandbox).
2. ✅ Datos y motores (ver arriba).
3. ⏳ `python3 wrlab.py winrates` (los win rates del CSV son del 29-oct) y extraer los datos de Sylas.
4. ✅ Este archivo en `data/estructurada/`; falta anotar 7.3c/7.3d/7.3e/7.3f en `data/FUENTES.md`.
5. ✅ Triage/refresh/annotate/baseline ejecutados.
6. ✅ Tests, bundles y BD regenerados.
7. ✅ Vigía: candidatos ampliados.
