# HOTFIX 7.3b — Cambios completos (despliegue: 15-oct-2026)

> **Fuente:** notas oficiales EN (wildrift.leagueoflegends.com/…/wild-rift-patch-notes-7-3b/,
> publicadas el 14/10/2026, obtenidas directamente por el vigía y esta integración).
> **Estado en el lab:** datos aplicados en items_7.3.csv, runas_7.3.md, specs y motores (v1.19).
> **Sin cambios de summoner spells ni de Smite** (verificación tarea 3 del autor 14/10).

## RESUMEN DE INTENCIÓN
Ayuda a campeones que no encontraban pie en el meta nuevo, recorte a los que
sobrerrendían (Hwei, Senna, Yunara, Nocturne), herramientas de snowball para
asesinos (ítems y runas), y ajuste de jungla (raptors más duros).

## CAMPEONES

| Campeón | Tipo | Cambio |
|---|---|---|
| **Volibear** | BUFF | Q Frenzied Maul: ratio AD 100→**110 %**; empower AD 160→**176 %**; empower heal por vida faltante 5/6/7/8 → **5/8/11/14 %** |
| **Jhin** | BUFF | Pasiva Whisper: crit estándar 80→**85 %**; %vida faltante 11-25 % (cap lvl 15) → 11.5-25 % (**cap lvl 10**) |
| **Tryndamere** | BUFF | Pasiva: crit por fury 0.3-0.5 % (por nivel) → **0.5 %** plano; E: 80/120/160/200 +100 % bAD → **80/130/180/230 +110 % bAD** |
| **Yasuo** | BUFF | Pasiva: crit estándar 90→**95 %**; escudo 77-529 → **77-630** por nivel |
| **Hwei** | NERF | Pasiva: 40-285 +30 % AP → **30-280 +25 % AP**; W escudo inicial 60/80/100/120 +35 % AP → **50/70/90/110 +30 % AP**; escudo máx 108/128/148/168 +71 % AP → **98/118/138/158 +60 % AP**; W daño bonus 30/40/50/60 → **20/30/40/50**; Q Crushing Maw: rango 7.5→**7**, daño 70/120/170/220 +70 % AP → **60/110/160/210 +60 % AP** |
| **Nocturne** | NERF | HP por nivel 134→**128**; Q Duskbringer: AD 20/30/40/50 → **10/25/40/55**, base 70/125/180/235 → **60/115/170/225**; R CD 110/90/70 → **120/100/80 s** |
| **Yunara** | NERF | Q Cultivation: daño pasivo y activo 10/15/20/25 → **5/10/15/20**; R CD 70/60/50 → **70/65/60 s** |
| **Senna** | NERF | Pasiva: crit estándar 90→**80 %**; AD por stack de Niebla 1.25→**0.9**; Q base 50/80/110/140 → **30/60/90/120** |

## ÍTEMS (aplicados a items_7.3.csv)

| Ítem | Cambio |
|---|---|
| Youmuu's Ghostblade | precio 3 000 → **2 900** |
| Locket of the Iron Solari | precio 2 600 → **2 500**; HP 200 → **300** |
| Thornmail | precio 2 700 → **2 850** |
| Warmog's Armor | umbral Warmog's Heart 900 → **1 250** HP bonus |
| Statikk Shiv | precio 3 000 → **2 900**; stacks energized por auto 5 → **7** |
| Yun Tal Wildarrows | precio 3 100 → **3 000** |

## RUNAS (aplicadas a runas_7.3.md)

| Runa | Cambio |
|---|---|
| Electrocute | daño 40-210 → **60-210** (+10 % bAD +5 % AP igual) |
| Cheap Shot | CD 7 → **5 s** |
| Grasp of the Undying | daño 3.3 % → **3.0 %** HP máx; growth +10 → **+8** HP por proc |
| Aery | escudo 25-120 → **20-100** (+10 % bAD +5 % AP igual) |

## JUNGLA / OTROS

| Sistema | Cambio |
|---|---|
| Crimson Raptor | HP base 1 000 → **1 100**; HP/nivel 110 → **125** |
| Raptor | HP base 500 → **550**; HP/nivel 55 → **65** |
| Bugfix Yun Tal | "AS effect occasionally triggered incorrectly" → el uptime de Flurry modelado (50 %) queda como convención conservadora |
| ARAM | cambios de modo excluidos del lab (solo SR) |
