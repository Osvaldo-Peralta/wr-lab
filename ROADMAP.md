# ROADMAP — WR-LAB como proyecto de software

**Estado actual (v1.5):** repo git local versionado · BD SQLite derivada · suite de tests · CI + vigilante de parches (GitHub Actions) · datos 7.3+7.3a.

## Ya disponible

| Capacidad | Dónde | Estado |
|---|---|---|
| Control de versiones | git local (tags por versión del lab) | ✅ listo para `git remote add origin … && git push` |
| Base de datos | `data/wrlab.db` (SQLite) vía `model/build_db.py` | ✅ se reconstruye desde los .md/.csv en segundos |
| Tests de regresión | `tests/test_model.py` (unittest, sin dependencias) | ✅ golden numbers de Jinx + slots + fórmula AS + overrides 7.3a |
| Vigía de parches | `model/check_patch.py` + `.github/workflows/patch-watch.yml` (cron 2×/día) | ✅ detecta: cambios en la página 7.3, aparición de 7.3a/7.4, nuevas entradas de changelog en wr-meta |
| CI | `.github/workflows/ci.yml` (tests + rebuild BD en cada push) | ✅ |
| Motor de DPS + validador | `model/dps_model.py` (`validate_slots`, `eval_build`, `compare`) | ✅ |

## Módulos propuestos (prioridad × esfuerzo)

1. **`wrlab` CLI unificado** (bajo esfuerzo, alto valor)
   `python -m wrlab update | analyze <champ> | db rebuild | test | bundle | watch`
   — envolver los scripts actuales en un solo punto de entrada con argparse.

2. **Optimizador de builds** (medio, MUY alto valor)
   Búsqueda exhaustiva/branch-and-bound sobre el pool de ítems del rol maximizando
   `dpsN` sujeto a: 6 slots, Ley 0 (1 botas), Ley 1 (crit ≤ umbral), Ley 2 (AS ≤ cap+ε),
   presupuesto de oro por minuto. Entrada: ChampSpec + escenarios; salida: top-N builds
   con desglose multiplicativo. Validación cruzada contra los reportes existentes
   (debe "redescubrir" la build C de Jinx y la K2 de Kalista).

3. **Buscador de runas** (bajo) — misma lógica sobre keystones×secundarias con valor marginal por escenario.

4. **Sincronizador con el sitio Quartz** (bajo-medio)
   `wrlab sync-vault <ruta-del-vault>`: copia reportes + fichas con frontmatter, genera
   índice `Guias.md`, respeta la nomenclatura del vault y hace commit en ese repo.
   Publicar = `git push` del vault (su workflow de Pages ya funciona).

5. **Simulador de timings de oro** (medio) — curva de oro de ADC/support/jungla por minuto
   (datos 7.3: minions, placas con decaimiento, jungle eco) para fechar los picos de cada
   ruta con precisión en vez de "~13:00".

6. **Matriz de matchups** (alto) — EHP/DPS efectivo cruzado entre builds (p.ej. "¿mi Jinx
   full contra un Chainlaced+Randuin?"), usando las tablas de mitigación ya existentes.

7. **Backup externo de la BD** (bajo) — el repo en GitHub YA es el backup (texto + db commiteada);
   opcional: export nocturno de `wrlab.db` a release assets vía Actions.

## Decisiones de arquitectura (por qué así)

- **Texto plano como fuente de verdad, SQLite como índice:** los .md/.csv viajan en los bundles
  portables (cualquier chat/IA los consume sin tooling); la BD da consultas rápidas y es reconstruible.
  Nunca al revés (una BD opaca rompería la portabilidad que ya resolvimos).
- **Sin dependencias de terceros:** todo stdlib (urllib, sqlite3, unittest, csv). Cero `pip install`,
  cero superficie de rotura. `requirements.txt` existe pero está vacío a propósito.
- **Golden tests:** los números canónicos de los reportes están fijados en tests; cualquier cambio de
  datos que los mueva falla en CI y obliga a documentar el porqué (como el override 7.3a de Caitlyn).
- **El vigía no actualiza solo:** detecta y avisa (exit 1 + step summary). La actualización real sigue
  el protocolo FRAMEWORK §E porque requiere criterio (discrepancias, overrides, re-validación).

## Para ponerlo en GitHub (una vez, ~3 minutos)

```bash
# en tu máquina, dentro de la carpeta wr-lab descargada/copiada:
git remote add origin https://github.com/Osvaldo-Peralta/wr-lab.git   # repo nuevo, privado o público
git push -u origin main --tags
# GitHub Actions corre ci.yml en el push y patch-watch.yml 2×/día.
```
