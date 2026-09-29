# HOTFIX 7.3a — Cambios completos (despliegue: 29-sep-2026, 09:30–12:00 CN)

> **Fuente:** notas oficiales del servidor chino (lolm.qq.com, docid 15413436308828016227) vía traducción
> comunitaria (r/wildrift, archivado en `data/raw/patch73a_cn_en.txt`). El sitio oficial EN aún no publica
> página propia de 7.3a (verificado 28/09: 404); la página de notas 7.3 no fue modificada.
> **Estado en el lab:** datos aplicados donde aplica; pendientes de re-verificación contra la nota EN oficial
> cuando se publique (protocolo §E de FRAMEWORK).

## RESUMEN DE INTENCIÓN (traducción del intro oficial)

"Ajustes de balance a campeones e ítems selectos — reforzando a los de bajo rendimiento y devolviendo a
niveles razonables las elecciones dominantes. Ralentización moderada del ritmo de clear de jungla early-mid
y menor resistencia contra split-push/siege continuo. Ajustes a Augments y campeones de ARAM por feedback."

## CAMPEONES

| Campeón | Tipo | Cambios |
|---|---|---|
| **Hwei** | NERF | Pasiva: 33–333 + 33 % AP → **40–285 + 30 % AP** · (1-1) Fire: 50/90/130/170 + 75 % AP → **50/85/120/155 + 70 % AP** · (1-2) amp por vida faltante: 150/200/250/300 % → **100/150/200/250 %** · (4) detonación: 250/350/450 + 75 % → **200/300/400 + 70 % AP** |
| **Samira** | BUFF | HP growth 128→**136** · armor growth 5→**5.5** · MR growth 1.4→**2** · pasiva melee ratios ~×1.65 · Flair 110→**125 % AD** · R por tiro 40→**50 % AD** |
| **Rammus** | NERF | Armor base 45→**40** · W bonus armor 45/50/55/60→**30/40/50/60 %** |
| **Malphite** ⚠️lab | NERF | W ratio de armadura 20→**15 %** · E ratio de armadura 45→**40 %** · R CD 75/70/65→**85/80/75 s** |
| **Tristana** | BUFF | Q AS 50/75/100/125→**60/80/100/120 %** · W CD 22/20/18/16→**20/18/16/14** · E base 80/100/120/140→**80/110/140/170**, ratio 100→**120 %**, amp crit 40→**50 %**, amp daño crit 40→**50 %** |
| **Draven** | BUFF | Q 80-110→**90-120 % AD** · W AS 20-35→**25-40 %** · R 130→**150 % AD** |
| **Caitlyn** ⚠️apéndice | NERF | **AS growth 0.04→0.025** · Headshot ratio 60–100→**60–90 % AD** |
| **Senna** ⚠️apéndice | AJUSTE | AS ratio/base 0.4→**0.3** · Base Bonus AS 0.6→**1.1** · AS growth 0.05→**0.025** · la AS bonus reduce menos el wind-up |
| **Syndra** | NERF | Nodos de pasiva 40/60/80/100/120→**50/75/100/125/150** · W ratio 60→**50 %** · slow fijo **25 %** |
| **Swain** | AJUSTE | Pasiva heal 3–4.5 %+0.5 % AP→**4.5–6 % + 0.2 % AP** · E return ratio 25→**40 % AP** |
| **Yuumi** ⚠️lab | NERF | W Best Friend HSP: 8/9/10/11 % + 0.02 % AP → **6/7/8/9 % + 0.01 % AP** |
| **Viego** | BUFF | Q pasiva 2-5→**3-6 %** · crit ratio 80→**85 %** · R crit scaling 50→**70 %** |

## ÍTEMS

| Ítem | Tipo | Cambios |
|---|---|---|
| **Yun Tal Wildarrows** ⚠️lab | BUFF | AS 25→**35 %** · Flurry: +25→**35 % AS**, CD 20→**25 s** |
| **Whispering Circlet** | NERF | Harmonize HSP: 0.5→**0.25 % del maná máx** |
| **Crown/Diadem of Songs** ⚠️lab | NERF | Harmonize HSP: 0.5→**0.25 % del maná máx** ("deja de ser BiS de enchanter; vuelve opcional-situacional") |
| **Death's Dance** | NERF | Coste 3 200→**3 300 g** |

## MAPA Y SISTEMAS

| Sistema | Cambio | Impacto en el lab |
|---|---|---|
| **Smite burn vs monstruos** | 30–198/s → **22–162/s** | Jungla early más lenta → Diana jungla: Nashor's 1.º aún más correcto; Shyvana/Volibear/Cho'Gath jungla: clear early −15-20 % |
| **Nexus** | 5 500 → **4 000 HP** | Partidas terminan antes tras inhibidores |
| **Placas de torreta** | Al perder placa: +30→**+20** arm/MR y 20→**10 s** | **Siege más fácil** → sube el valor de Jinx/Kalista/Yunara (siege) y de Runaan's/Energized |
| ARAM (Augments + Fiddle/Nasus) | varios | Fuera del alcance SR del lab |

## IMPACTO EN REPORTES/SPECS DEL LAB (estado 28/09)

| Archivo | Impacto | Acción |
|---|---|---|
| `reportes/Yuumi_*` | HSP de W: −2 pts y mitad del término AP → E-shield 339→~338 (−0.3 %), R-heal 651→~648. **Build y veredictos intactos** (Censer sigue siendo el rey) | Anotado [!WARNING] en el reporte |
| `metodologia/ESCALADO_DE_TAMANIO.md` | Malphite: E con 336 armor pasa de 361→**344**; W golpe 117→**100**; R cada 85 s | Tabla corregida + nota |
| `champion_attack_speed_7.3.csv` | Filas Caitlyn (0.04→0.025 por nivel) y Senna (0.3/0.3/1.1/0.025) | Corregidas con marca 7.3a |
| `model/dps_model.py` ITEMS | Yun Tal AS 25→35; Death's Dance 3300 | Aplicado |
| `reportes/Kalista_*` | Yun Tal buffeada sigue RECHAZADA para Kalista (sin on-hit, ramp de crit); para **Yunara** (reporte externo) es buff relevante → re-verificar ese reporte | Anotado |
| `reportes/Diana_*` | Smite burn −18 % → clear early más lento (refuerza Nashor's 1.º en jungla) | Anotado |
| `reportes/Jinx_*` | Placas más blandas + Nexus 4000 → siege Jinx MEJORA; ningún cambio directo a Jinx | Anotado |
| Reportes externos (Yunara/Cho'Gath/Shyvana hechos en otro chat) | Yunara: Yun Tal buff + placas (revisar 1.er ítem) · Cho'Gath: smite nerf jungla · Shyvana: smite nerf | Marcar para revisión en su próxima regeneración |
| FRAMEWORK test de Caitlyn | El ejemplo oficial (1.48125) usaba growth 0.04 (pre-7.3a); con 0.025 el resultado esperado a lvl15 con Alacrity+Berserker's es **1.35** | Test actualizado con ambos valores |
