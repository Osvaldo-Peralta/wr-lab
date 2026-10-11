# -*- coding: utf-8 -*-
"""WR-LAB · model/fichas_analiticas.py (v1.15.3) — fichas analíticas del roster.

Genera/actualiza `data/estructurada/fichas_analiticas/<slug>.md` para cada
campeón del roster del lab (WINRATE_ROSTER ∪ registro de reportes).

Diseño anti-desfase (lección del incidente 09/10):
  · Las secciones de DATOS (meta CSV, stats base, AS 7.3/7.3a, cambios de
    parche, leyes por arquetipo) se rellenan SOLO desde archivos del lab →
    re-correr el generador tras un patch-watch refresca la ficha entera.
  · La prosa curada (tesis, kit, palancas, curva) vive en el dict PROSA de este
    módulo: es la fuente editorial humana, y el generador la inserta tal cual.
  · Idempotente: mismo input → mismo output (salvo fecha de generación).

Uso:  python3 model/fichas_analiticas.py            # todo el roster
      python3 model/fichas_analiticas.py senna jinx  # solo algunos
"""
import csv
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = os.path.join(ROOT, "data", "estructurada")
OUT = os.path.join(E, "fichas_analiticas")
sys.path.insert(0, os.path.join(ROOT, "model"))
import check_patch as CP  # noqa: E402
import update_reports as U  # noqa: E402

PATCH_LABEL = "7.3+7.3a"

# ─────────────────────────── PROSA CURADA POR CAMPEÓN ───────────────────────────
# t=tesis · rol=lectura de roles · kit=bullets de kit/escalado · cur=curva de poder
# pal=palancas de sobreexplotación · sin=sinergias/counters · leyes=leyes que gobiernan
# build=dirección de build · rango=attack range · critmod=mod de crit del kit (o None)
PROSA = {
    "ahri": dict(t="Assassin-mage de picks: charme + burst móvil; el ult de 3 dashes la hace imposible de fijar.",
        rol="Mid. Pick-comp: gana con charm landeados, no con waveclear.",
        kit=["Charme (E) = setup de todo el burst; falla E, falla el trade.", "Ult con 3 dashes + kill reset: movilidad defensiva y offensiva.", "Q ida/vuelta con daño verdadero en el regreso: poke barato.", "W orbitales: burst de cercana sin skillshot."],
        cur="Pico 2-ítems (Luden/Shadowflame); decae vs frontlines tanque.",
        pal=["Charme → Q+W+auto con pasiva de MS para reposicionar.", "Ult como herramienta de escape aunque no haya kill.", "Roam lateral con MS de pasiva tras 2 hits."],
        sin="Sinergia con junglas de CC (setup de charme); counter de asesinos de dash (poppy-like) y QSS temprano.",
        leyes=["Ley de burst: el combo debe matar al carry en 2.5 s o retirarse.", "Sin crit: AP pura; Leyes 0/3 aplican a su build de pen mágica."],
        build="Luden/Shadowflame → horizon u odio eterno vs tanques; zapatos sorc → cap genio.", rango=550, critmod=None),
    "caitlyn": dict(t="Marksman de asedio y trampas: el rango más largo base del juego convierte la lane en zona prohibida.",
        rol="ADC. Lane-dominance: gana el draft de posición, no el DPS race.",
        kit=["Rango base 625 (750 con ult pasiva de headshot): asedio de torreta temprano.", "Trampas (W) en embudos: root + headshot garantizado.", "Q de línea: poke y waveclear; E = dash de kiting con slow.", "Headshots: auto cargado que proca on-hit doble."],
        cur="Fuerte 0-14 (lane + 2 piezas); decae relativo late vs hypercarries.",
        pal=["Trampas en entradas de jungle y detrás de minions de asedio.", "Headshot a torre: placas sin exposición.", "Q+E como unitario de escape si flashean sobre ti."],
        sin="Morgana/Lux support (root → trampa garantizada); counter de draven/ejecutores de inmovilidad.",
        leyes=["Ley 1 estricta: crit 100 % con 4 piezas.", "Ley 6: C44/IE en checkpoints de oro de lane ganada."],
        build="Gunmetal + C44 + Runaan + IE + LDR; Galeforce vs dive.", rango=625, critmod=None),
    "chogath": dict(t="Tanque AP de escalado infinito: Feast convierte kills/objectivos en HP permanente que ningún item iguala.",
        rol="Top o Jungla. Frontline que amenaza carries con ejecuciones reales.",
        kit=["Feast (R): ejecución de vida + stack de HP permanente (escalado infinito).", "Rupture (Q) knockup + W silencio: cadena de CC en área.", "E: autos en cono con daño mágico % vida: waveclear y pelea.", "Pasiva de regen al matar unidades: sostenibilidad de lane."],
        cur="Lento early; imparable 3+ stacks de Feast con 2 ítems de HP.",
        pal=["Feast a monstruos épicos y minions de asedio: stacks sin kills.", "Q sobre el dash enemigo (predictivo de patrón).", "E activado para tradear: cono > auto simple."],
        sin="Sinergia con engages lentos (Amumu-like); counter de ejecutores de %vida (Vayne-like) y grievous temprano.",
        leyes=["Tanque AP: Leyes de slots igual; el 'DPS' es %vida → pen mágica y HP multiplican.", "Ley 0 aplica; Ley 1 no (sin crit)."],
        build="Cinturón gigante → sunfire/iceborn por rol; zapatos según CC enemigo.", rango=175, critmod=None),
    "diana": dict(t="Assassin-jungla de burst lunar: el dash al objetivo con root hace que su combo no falle una vez dentro.",
        rol="Jungla o Mid. Dive-comp: entra una vez, decide la pelea.",
        kit=["Q lunar marca → E dash reseteado sobre marcados: entrada garantizada.", "W escudo + orbitales que detonan: trades y clear.", "R pull en área + daño: teamfight win si entras segundo.", "Pasiva de autos con daño mágico en arco: clear y burst."],
        cur="Pico 2-3 ítems; cae si el enemigo estira la pelea 30+ s.",
        pal=["Entrar post-CC aliado: R segundo, no primero.", "Q antes de entrar: el reset de E es tu seguro de vida.", "Clear con W+pasiva: rutas de 4 camps."],
        sin="Follow-up de engages (Malphite-like); counter de zealots de QSS y peel duro.",
        leyes=["AP burst: shadowflame/cap genio; pen mágica según frontline (Ley 3 análoga).", "Ley 0 en builds; sin crit."],
        build="Nashor/cinturón → shadowflame → cap genio o odio vs tanques.", rango=150, critmod=None),
    "heimerdinger": dict(t="Mago de asedio con torretas: convierte zonas en territorio propio y gana guerras de objetivo estático.",
        rol="Mid. Zone-control: el dragón/herald se pelea en su terreno.",
        kit=["Torretas (Q): daño persistente que escala con AP y se potenciaban en zona.", "Granada (E) stun en área + carga torretas: setup.", "W cohetes en cono: burst a quemarropa o poke lejano.", "R ult de torreta gigante o upgrade de kit: objetivo-toma."],
        cur="Fuerte desde 2 ítems en objetivos estáticos; débil en pelea móvil.",
        pal=["Torretas en arbustos de río: visión + daño gratis.", "E sobre el path de escape, no al centro.", "Push lateral con torretas mientras el equipo agrupa."],
        sin="Comps de siege (caitlyn-like); counter de asesinos de dash que borran torretas.",
        leyes=["AP de zona: haste + AP bruto; sin crit.", "Ley 0 en builds de 6 slots como todos."],
        build="Luden → shadowflame → cap genio; liandry vs comps de HP.", rango=550, critmod=None),
    "jinx": dict(t="Hypercarry de resets: cada takedown regala MS+AS y convierte una kill en teamfight ganada.",
        rol="ADC. Escalado puro: protegerla 20 min = ganar.",
        kit=["Q intercambiable: minigun AS o cohete AoE (112 % AD, splash).", "Pasiva Get Excited: +140 % MS y AS por 6 s tras takedown/objectivo.", "W slow + reveal; E trampas root en área.", "R global con daño por missing HP: ejecución cross-map."],
        cur="Débil 0-8; imparable 3+ piezas con pow-pow activo.",
        pal=["Cohete en teamfight, minigun en 1v1/objetivos.", "Trampas en embudos de retirada propia.", "R a carries bajos cross-map: oro y reset de pasiva."],
        sin="Enchanter supports (lulu/yuumi-like) que la dejan viva al reset; counter de dive instantáneo.",
        leyes=["Ley 1: crit 100 % exacto (C44+Runaan+IE+LDR).", "Ley 2: AS cap 3.0 alcanzable con pow-pow+LT.", "Ley 3b: pen única."],
        build="Gunmetal + C44 + Runaan + IE + LDR + Kraken (estándar v1.5 del reporte).", rango=575, critmod=None),
    "kalista": dict(t="Marksman de kiting infinito: el dash por auto permite reposicionarse en cada golpe si respetas el ritmo.",
        rol="ADC. Skill-expression: el techo de ejecución más alto del rol.",
        kit=["Pasiva de dash por auto: kiting perpetuo si mueves tras cada attack.", "Lanzas (E) acumulables: slow + extracción con reset al matar.", "W pacto con aliado: daño bonus sincronizado y visión.", "R guarda al support: engage/disengage dual."],
        cur="Fuerte desde 2 piezas si el jugador mantiene el ritmo de dash.",
        pal=["E reset en minions/monstruos: poke gratuito en lane.", "R al support engage: pick garantizado.", "Dash lateral, no hacia atrás: mantiene DPS."],
        sin="Supports de engage (leona-like) por el pacto y la R; counter de CC puntual que rompe el ritmo.",
        leyes=["On-hit/crit híbrido: Ley 1 con umbral según build.", "Ley 0 estricta."],
        build="Gunmetal + Blade/Runaan según comp + IE + pen; on-hit vs tanques.", rango=550, critmod=None),
    "karma": dict(t="Enchanter de poke y shields: el mantra de 2 cargas convierte cada habilidad en dos efectos.",
        rol="Support (y mid niche). Flex-pick: se adapta al comp enemigo.",
        kit=["Q con mantra = doble lanza + explosión: poke y waveclear.", "E escudo con mantra = área + MS: engage/disengage de equipo.", "W root retardado con daño: zone control.", "Pasiva de haste por auto: spameo sostenido."],
        cur="Pico de impacto medio-juego; decae si el juego se estira a carry-scaling.",
        pal=["Mantra en E para engages, en Q para poke de sieje.", "Escudo pre-mitigación de burst enemigo (timing > tamaño).", "Poke de lane con Q+auto para stacks de pasiva."],
        sin="Carries de poke (varus/caitlyn-like); counter de engages duros que ignoran shields.",
        leyes=["Support: valor-aliado (escudo×haste); sin crit.", "Ley 0 en builds de utility."],
        build="Crimson → echo/moonstone → censer/redemption según carry.", rango=525, critmod=None),
    "malphite": dict(t="Tanque de anti-AD absoluto: su armadura escalada convierte builds físicas en daño decorativo.",
        rol="Top o Support. Draft-win vs comps físicos.",
        kit=["Pasiva de escudo por %max HP que regenera fuera de combate.", "Q roba AS: debuff doble (tu daño + su DPS menor).", "E ground slam: daño reducido por tu armadura + AS down en área.", "R engage global imparable: el pick más limpio del juego."],
        cur="Item-spike por pieza de armadura; pico con 2-3 piezas vs AD.",
        pal=["R sobre el carry AD con follow-up aliado: no lo gastes en poke.", "E en cada teamfight: el AS-down gana trades gratis.", "Q al hypercarry enemigo antes del engage."],
        sin="Follow-ups de área (yasmal/aoe-mages); counter de AP burst y pen mágica.",
        leyes=["Tanque: HP+armor multiplican su E; sin crit.", "Ley 0; presupuesto de tanque ≠ DPS."],
        build="Iceborn/sunfire → thornmail → fuerza natural vs AP.", rango=125, critmod=None),
    "mordekaiser": dict(t="Juggernaut de duelos en reino muerto: su R crea un 1v1 obligatorio donde siempre gana.",
        rol="Top. Split-push que el enemigo no puede ignorar ni contestar 1v1.",
        kit=["R: secuestra al objetivo a un reino 1v1 (stats robadas).", "Q de 3 hits con daño creciente: duelo y clear.", "W armadura acumulable que detona en heal/damage.", "E pull: mantiene al objetivo en su zona de muerte."],
        cur="Fuerte 1-2 ítems en duelos; teamfight depende de R bien usado.",
        pal=["R al carry sin escape o al que gana tu 1v1 siempre.", "W antes del trade largo: la detonación cierra kills.", "Push lateral: el reino muerto hace al split invulnerable a ganks 1v1."],
        sin="Comps sin peel duro; counter de cleansers (QSS) y campeones de rango sostenido.",
        leyes=["AP juggernaut: liandry/rimland por HP; sin crit.", "Ley 0."],
        build="Riftmaker/liandry → demonic → spirit visage según daño enemigo.", rango=175, critmod=None),
    "nocturne": dict(t="Jungla de presión global: su R apaga el mapa y convierte cada ult en un pick asegurado.",
        rol="Jungla. Tempo-comp: objetivos tomados bajo oscuridad.",
        kit=["R global de ceguera de visión + dash a campeón: pick cross-map.", "Q de estela: MS y AD en camino (kiting y chase).", "W spell-shield: bloquea el CC que lo pararía.", "E miedo: disuasión de pelea y clear de camps."],
        cur="Pico medio-juego con 2-3 piezas de on-hit/lethalidad.",
        pal=["R sobre objetivos sin escape en lados opuestos del mapa.", "W contra el CC conocido del enemigo (timing).", "Clear rápido con Q+E: invade post-6."],
        sin="Comps de sieje bajo visión reducida; counter de guardianes de zona y cleansers.",
        lethal=True,
        leyes=["On-hit/lethalidad: Ley 1 con umbral de crit según build.", "Ley 3b en pen física."],
        build="Gunmetal/blade → on-hit (wit's/terminus-like del pool) o lethalidad según comp.", rango=125, critmod=None),
    "norra": dict(t="Artillera de Yordle con mortero: daño en área y control de zona a distancia absurda.",
        rol="Mid. Siege-mage: waveclear y zone-denial de objetivos.",
        kit=["Q mortero en área grande: waveclear y poke de sieje.", "W trampa/slow de zona: control de embudos.", "E escudo/dash defensivo con daño.", "R mega-mortero global en zona: objetivo-toma y teamfight."],
        cur="Pico 2-3 ítems de AP+ hache; sostenida en sieje.",
        pal=["R en objetivos épicos antes del engage: zona negada.", "Q sobre la ola + campeones: value doble.", "W en retiradas propias del equipo."],
        sin="Comps de sieje lento; counter de engages rápidos que cierran su distancia.",
        leyes=["AP de zona: haste+AP; sin crit.", "Ley 0."],
        build="Luden → shadowflame → cap genio; morellonomicon vs heal.", rango=550, critmod=None),
    "orianna": dict(t="Maga de control de área con la bola: el posicionamiento de la esfera es su skill real.",
        rol="Mid. Teamfight-comp: su R de shockwave define peleas.",
        kit=["Q mueve la bola: todo el kit opera desde su posición.", "W área de daño/MS alrededor de la bola.", "E escudo al aliado que porta la bola + daño en camino.", "R shockwave en la bola: el engage/peel más grande del juego."],
        cur="Escalado AP clásico; pico 3 ítems con teamfight ganada por R.",
        pal=["Bola en el frontline propio antes del engage enemigo.", "E sobre el diver aliado: escudo + daño de regreso.", "R con 3+ objetivos o al carry sin posición."],
        sin="Frontlines que agrupan enemigos (amumu/malphite-like); counter de asesinos de burst inmediato.",
        leyes=["AP: luden/cap; hache para spameo de Q.", "Ley 0; sin crit."],
        build="Luden → horizon/cap → zhonya si dive.", rango=525, critmod=None),
    "ornn": dict(t="Tanque herrero: mejora ítems aliados y crea engages de área con fuelle y fragua.",
        rol="Top. Utility-tank: valor de equipo por encima del propio.",
        kit=["Pasiva: forja ítems para aliados (oro extra convertido en stats).", "Q grieta + W fuelle de fragua: knock-up encadenado.", "E dash que rebate en terreno: reposiciona peleas.", "R de carnero global: engage de área con 2 llamadas."],
        cur="Valor desde 1-2 ítems; la mejora de ítems aliados escala con el juego.",
        pal=["Mejora el ítem del carry en cada back (value compuesto).", "W sobre el Q landeado: knock-up asegurado.", "R de segunda llamada como peel, no solo engage."],
        sin="Carries que agradecen mejoras (IE/Runaan mejorados); counter de ranged kiting sin melee check.",
        leyes=["Tanque utility: sin crit; presupuesto de HP/armor.", "Ley 0."],
        build="Iceborn/sunfire → thornmail → visionary para mejoras aliadas.", rango=175, critmod=None),
    "rammus": dict(t="Bola de armadura con taunt: el anti-AD personificado que convierte tu armadura en su daño.",
        rol="Jungla. Counter-pick de comps físicos; ganks de taunt asegurado.",
        kit=["Q bola: MS masiva para ganks y objetivos; knock-up al llegar.", "W bola defensiva: armadura que refleja daño de autos.", "E taunt puntual: obliga autos sobre ti (protege carries).", "R salto en área: engage de zona con daño por armadura."],
        cur="Fuerte desde 1-2 piezas de armadura; decae vs AP.",
        pal=["Gank con Q+E: el taunt hace el resto.", "W activo en cada trade de autos.", "R en torretas/objetivos: zona negada."],
        sin="Comps AD enemigos (draft-win); counter de AP mages y kiting de rango.",
        leyes=["Tanque de armadura: su daño escala con armor (único).", "Ley 0; sin crit."],
        build="Iceborn/thornmail → sunfire → fuerza natural tardía.", rango=125, critmod=None),
    "senna": dict(t="Artillera de asedio con escalado infinito de Niebla: AD y crit gratis permanentes que reescriben la Ley 1.",
        rol="Support S+ (valor-aliado + asedio) y DUO S+ (DPS medido por motor).",
        kit=["Pasiva Niebla: +1.25 AD y +10 % crit/20 stacks; overcap → 35 % vamp.", "Relic Cannon: auto hitscan con on-hit +20 % AD y wind-up largo.", "Q línea que cura aliados y daña (−1 s CD por auto).", "W root en área con truco de minion moribundo; E camuflaje de equipo; R global de escudo+ejecución."],
        cur="Débil early (570 HP, AS 0.63); asedio imparable 14+ min con 90-140 stacks.",
        pal=["No lasthear como support: wraiths garantizados de minions ajenos.", "W + minion moribundo = root instantáneo desde 1 300.", "R triple: ejecución + escudo pre-engage + Niebla global.", "Q a través de ola/torreta: value sin exposición."],
        sin="Jhin/J4 (roots encadenados); counter de dive instantáneo (blitz/malphite).",
        leyes=["Ley 1 UMBRAL BLANDO: 50 % crit de ítems + 50 % gratis; overcap → vamp (no oro muerto).", "Ley 2 no vinculante (techo AS 1.44).", "Ley 3: BotRK sustituye pen vs tanques (current-health)."],
        build="Support: Crimson+ER+Censer+Cleaver+Echo+GA · DUO: óptima del motor (ver reporte).", rango=625, critmod=0.9),
    "seraphine": dict(t="Enchanter de cadena: cada habilidad se duplica y encadena CC/curas en área creciente.",
        rol="Support. Teamfight-comp: su valor crece con la duración de la pelea.",
        kit=["Pasiva de notas duplicadas: cada 3.ª habilidad se repite con notas de daño/cura.", "Q daño en área que escala por nota: poke sostenido.", "W escudo+cura en área con MS: sustain de pelea.", "E slow/root en cadena: setup de picks.", "R encantamiento en línea larga: engage o peel masivo."],
        cur="Pico medio-juego con 2-3 piezas de utility; decae vs burst inmediato.",
        pal=["R desde flanco: la línea larga atrapa 3+.", "W antes del burst enemigo, no después.", "Notas de pasiva en lane: Q+auto duplicado."],
        sin="Comps de pelea larga (hypercarries); counter de engages de 1 botón.",
        leyes=["Support valor-aliado: heal/shield power + haste.", "Ley 0; sin crit."],
        build="Crimson → moonstone/echo → censer/redemption.", rango=525, critmod=None),
    "shyvana": dict(t="Dragón juggernaut de transform: clear monstruoso y teamfights como drake gigante.",
        rol="Jungla. Farm-to-scale: objetivos épicos como motor de poder.",
        kit=["Pasiva de daño a monstruos + stacks por drake cazado: escala con objetivos.", "Q doble golpe + reset de auto: duelo y clear.", "W aura de daño + MS: kiting y clear en movimiento.", "E marca de daño %vida: execute blando.", "R transform a dragón: HP + ranged attacks + knock-up."],
        cur="Clear elite early; pico 2-3 ítems híbridos con drakes stackeados.",
        pal=["Drakes = stats gratis: prioriza objetivos sobre ganks.", "W activo en movimiento entre camps (clear rodante).", "R como engage o como peel: knock-up de área."],
        sin="Comps que estiran peleas; counter de kiting extremo y grievous temprano.",
        leyes=["Híbrida AD/AP: build según stack de drakes (motor cualitativo).", "Ley 0."],
        build="Blade/sunfire híbrido → on-hit o AP según transformación dominante.", rango=125, critmod=None),
    "sivir": dict(t="Marksman de rebotes y oleadas: el waveclear más rápido del juego convertido en presión de mapa.",
        rol="ADC. Tempo-comp: su R de MS global crea engages propios.",
        kit=["Q bumerán con daño doble: poke y clear.", "W rebotes en cadena: clear instantáneo y teamfight AoE.", "E spell-shield: bloqueo gratuito de habilidad clave (y maná).", "R MS en área global: el engage de equipo más barato."],
        cur="Pico de clear 2 piezas; teamfight con W+R desde 3.",
        pal=["E sobre el engage enemigo conocido (maná + tempo).", "R para iniciar o para responder dives.", "Push lateral con Q+W: torretas sin pelea."],
        sin="Comps de engage propio (malphite/ornn-like); counter de poke que quiebra su positioning.",
        leyes=["Ley 1 estricta crit; Ley 3b pen.", "Ley 6: checkpoints de clear."],
        build="Gunmetal + C44/Runaan + IE + LDR; RFC en sieje.", rango=500, critmod=None),
    "syndra": dict(t="Maga de burst por esferas: el daño escala con el tiempo de lane acumulado en orbes.",
        rol="Mid. Burst-comp: ejecuta carries con combo completo.",
        kit=["Esferas acumuladas: todo el kit consume/produce orbes (escalado por minutos).", "Q create + W grab/throw: burst de zona.", "E knockback que empuja esferas: stun en línea.", "R ejecución con todas las esferas: el unitario más grande del mid."],
        cur="Escalado por stacks de pasiva; pico 3 ítems con R de 6+ esferas.",
        pal=["Acumula esferas antes del all-in (no gastes Q gratis).", "E con 2-3 esferas delante: stun de área.", "R solo con execute garantizado: sin desperdicio."],
        sin="Junglas de follow-up burst; counter de cleansers y spell-shields.",
        leyes=["AP burst: shadowflame/cap; pen mágica vs frontline.", "Ley 0."],
        build="Luden/shadowflame → horizon → cap genio; zhonya vs dive.", rango=550, critmod=None),
    "volibear": dict(t="Juggernaut de tormentas: dives de torre gratuitos con R y duelos de on-hit sostenido.",
        rol="Top o Jungla. Frontline que amenaza carries con E de execute blando.",
        kit=["Pasiva de on-hit en área creciente: pelea sostenida y clear.", "Q dash con stun: engage y chase.", "W mordisco doble con execute blando y heal.", "E rayo en zona: daño + escudo propio.", "R transform: HP + rango + dive de torreta sin daño."],
        cur="Fuerte 1-2 ítems; R hace objetivos tempranos casi gratis.",
        pal=["R bajo torreta enemiga: dive sin castigo.", "W segundo mordisco como execute en duelos.", "E sobre tu posición al ser kiteado: escudo + zona."],
        sin="Comps de dive coordinado; counter de kiting de rango y grievous.",
        leyes=["Juggernaut on-hit: blade/wit's del pool; sin crit.", "Ley 0."],
        build="Blade → sunfire/iceborn → spirit visage; gunmetal si on-hit puro.", rango=150, critmod=None),
    "xayah": dict(t="Marksman de plumas recuperables: el auto-positioning de sus plumas crea burst y raíz a voluntad.",
        rol="ADC. Self-peel único: su R la hace intargetable y recupera plumas.",
        kit=["Pasiva: habilidades dejan plumas; E las召回 con daño creciente y root con 3+.", "Q lanza plumas en línea; W AS+daño bonus al auto al campeón.", "R intargetable + abanico de plumas: el mejor self-peel del rol.", "Plumas persisten en el suelo: zoning permanente."],
        cur="Pico 2-3 ítems de crit; root de E hace duelos ganables.",
        pal=["E tras R: root garantizado de 5 plumas.", "Plumas en embudos: zona de root permanente.", "W en objetivos: el AS bonus es tu burst window."],
        sin="Rakan-like/peel supports; counter de cleaners de plumas y dives por detrás.",
        leyes=["Ley 1 estricta; Ley 3b.", "Ley 6 checkpoints de crit."],
        build="Gunmetal + C44/Runaan + IE + LDR; Galeforce vs dive duro.", rango=525, critmod=None),
    "yunara": dict(t="Marksman híbrida de tormentas: crítico + on-hit mágico con movilidad de viento.",
        rol="ADC. Nuevo arquetipo del lab: spread de Q y crítico interactúan (aproximado).",
        kit=["Q de abanico con spread que escala con AS/crit (modelado aproximado).", "W dash de viento con slow: kiting y reposición.", "E escudo/amp de on-hit por ventana.", "R tormenta en área: zone-denial de teamfight."],
        cur="Escalado doble (crit+on-hit): pico 3 piezas.",
        pal=["Dash lateral con W tras cada rafaga.", "R en objetivos: la zona fuerza fights a tu favor.", "On-hit y crit se apilan: builds híbridas legales."],
        sin="Enchanters de AS (censer); counter de burst inmediato que cierra su ventana.",
        leyes=["Ley 1 con umbral híbrido; Ley 3b en pen física.", "Spread de Q NO modelado exacto (⚠️ declarado)."],
        build="Gunmetal + on-hit/crit mixto según comp (motor autos).", rango=550, critmod=None),
    "yuumi": dict(t="Enchanter-parásita: valor-aliado puro sin posición propia; el carry ES tu posición.",
        rol="Support. Hypercarry-comp: multiplica al aliado, no existe sola.",
        kit=["W anexión al aliado: stats compartidas y untargetable.", "Q proyectil dirigido desde el aliado: poke y slows.", "E heal+MS en anexión: sustain de lane.", "R páginas de knock-up en área: peel/engage desde el carry."],
        cur="Valor desde 1-2 piezas de heal/shield power; escala con el carry.",
        pal=["Cambio de carry en pelea (W hop): valor doble.", "R sobre el dive enemigo, no al inicio.", "Q desde arbustos/aliados para poke sin riesgo."],
        sin="Hypercarries de AS (jinx/yunara); counter de burst que mata al carry anfitrión.",
        leyes=["Support valor-aliado: moonstone/censer; sin crit ni DPS propio.", "Ley 0 en builds de utility."],
        build="Crimson → moonstone → censer/redemption; hose de heal-shield power.", rango=425, critmod=None),
}

# ─────────────────────────── fuentes de datos ───────────────────────────
def leer_winrates():
    out = {}
    with open(os.path.join(E, "champion_winrates.csv"), newline="", encoding="utf-8") as fh:
        for fila in csv.DictReader(fh):
            out.setdefault(fila["champion"].lower(), []).append(fila)
    return out


def leer_stats():
    with open(os.path.join(E, "champion_base_stats.json"), encoding="utf-8") as fh:
        return json.load(fh)


def leer_as():
    out = {}
    with open(os.path.join(E, "champion_attack_speed_7.3.csv"), newline="", encoding="utf-8") as fh:
        for fila in csv.DictReader(fh):
            out[fila["champion"].lower()] = fila
    return out


def cambios_parche(nombre):
    """Cambios directos desde los diffs del lab (7.3/7.3a): filas de tabla
    '| **Champ** ⚠️ | TIPO | detalle |' y bullets que mencionen al campeón."""
    hits = []
    for fn in ("cambios_campeones_7.3.md", "cambios_7.3a.md", "cambios_items_7.3.md", "cambios_runas_7.3.md"):
        ruta = os.path.join(E, fn)
        if not os.path.exists(ruta):
            continue
        txt = open(ruta, encoding="utf-8").read()
        for m in re.finditer(
            rf"(?im)^\|\s*\*\*{re.escape(nombre)}\*\*[^|]*\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|", txt):
            linea = f"{fn.replace('cambios_', '').replace('.md', '')} · {m.group(1)}: {m.group(2)}"
            if linea not in hits:
                hits.append(linea)
    return hits[:6]


def ficha(slug, win, stats, as_tab, hoy):
    p = PROSA[slug]
    nombre = stats.get(slug, {}).get("name") or CP.DISPLAY.get(slug, slug.title())
    filas = win.get(slug, [])
    meta = " · ".join(
        f"{f['role']} {f['tier']} WR {f['win_pct']} % (pick {f['pick_pct']} %, ban {f['ban_pct']} %, {f['confidence']})"
        for f in filas) or "sin filas en el CSV del vigía todavía"
    st = stats.get(slug, {}).get("stats", {})
    def val(x):
        return x if x not in (None, "", "?") else "— (fuera del JSON del lab: ver wiki/ficha del autor)"
    ad = val(st.get("attackdamage")); hp = val(st.get("heal") or st.get("health"))
    arm = val(st.get("armor")); mr = val(st.get("magicresistance"))
    asf = as_tab.get(nombre.lower()) or as_tab.get(slug)
    as_line = (f"ratio {asf['Attack Speed Ratio']} · base {asf['Base Attack Speed']} · "
               f"BBA {asf['Base Bonus Attack Speed']} · growth {asf['Attack Speed per Level']}") if asf else "sin fila en el apéndice AS 7.3"
    cambios = cambios_parche(nombre)
    sec1 = ("\n".join(f"- {c}" for c in cambios) if cambios
            else "- Sin cambios directos en 7.3/7.3a: su balance vive en cambios sistémicos (crit 200 %, AS cap 3.0, torretas 7 000 HP).")
    crit = f"{p['critmod']}× (kit)" if p.get("critmod") else "1.0× (estándar)"
    leyes = "\n".join(f"- {l}" for l in p["leyes"])
    kit = "\n".join(f"- {k}" for k in p["kit"])
    pal = "\n".join(f"{i}. **{t}**" for i, t in enumerate(p["pal"], 1))
    return f"""---
tags: [wrlab, ficha, {slug}]
version: auto-1.0
Status: derivada (datos del lab {hoy})
champion: {nombre}
patch: "{PATCH_LABEL}"
---

# ⚗️ WR-LAB · FICHA ANALÍTICA — {nombre.upper()} (Wild Rift {PATCH_LABEL})

**Generada:** {hoy} por `model/fichas_analiticas.py` · prosa curada v1 · datos del lab en vivo
**Roles:** {p['rol']}
**Arquetipo lab:** {p.get('arq', 'ver tesis')} · `crit_dmg_mod` {crit}
**Tesis:** {p['t']}

> [!NOTE]
> **Estado meta (wr-meta Diamond+, vigía {filas[0]['actualizado'] if filas else '—'}):** {meta}.

---

## 1. QUÉ LE HIZO ESTE PARCHE

{sec1}

## 2. FICHA MATEMÁTICA (datos del lab)

| Parámetro | Valor | Fuente |
|---|---|---|
| AD base (growth) | {ad} | champion_base_stats.json |
| HP base (growth) | {hp} | champion_base_stats.json |
| Armadura / RM | {arm} / {mr} | champion_base_stats.json |
| AS 7.3 | {as_line} | champion_attack_speed_7.3.csv |
| Rango de ataque | {p['rango']} | prosa curada (verificar wiki si se usa en motor) |
| Crit mod del kit | {crit} | tabla de arquetipos lab |

## 3. KIT Y ESCALADO

{kit}

## 4. CURVA DE PODER Y LECTURA DE ROLES

- {p['cur']}
- {p['rol']}

## 5. PALANCAS DE SOBREEXPLOTACIÓN

{pal}

**Sinergias/counters:** {p['sin']}

## 6. LEYES QUE LA GOBIERNAN

{leyes}

## 7. DIRECCIÓN DE BUILD

- {p['build']}
- Pool y veredictos por ítem: ver `reportes/` si existe guía del campeón, o derivar con `optimize_build.py {slug}` si tiene spec en `dps_model.CHAMPS`.

## 8. PENDIENTES DE VERIFICACIÓN

- [ ] Rangos/valores de kit citados de prosa: contrastar con wiki oficial antes de usar en motor.
- [ ] Si se escribe reporte: correr `optimize_build.py {slug}` (requiere spec) y `update_reports.py triage/annotate`.

---

## Pie de página
Fuentes: WR-LAB v1.15.3 (winrates del vigía, apéndices oficiales 7.3, diffs de parche) + prosa curada del autor.
Documento no oficial; Wild Rift es marca de Riot Games.
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    hoy = U.datetime.date.today().isoformat()
    win, stats, as_tab = leer_winrates(), leer_stats(), leer_as()
    roster = sorted(CP.roster_winrates())
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if args:
        roster = [r for r in roster if r in args] or args
    for slug in roster:
        if slug not in PROSA:
            print(f"⚠️ {slug}: sin prosa curada en PROSA — saltado (agregala al dict)")
            continue
        txt = ficha(slug, win, stats, as_tab, hoy)
        with open(os.path.join(OUT, f"{slug}.md"), "w", encoding="utf-8") as fh:
            fh.write(txt)
    print(f"✔ {len(roster)} fichas en {os.path.relpath(OUT, ROOT)}")


if __name__ == "__main__":
    main()
