# DESPLIEGUE — Quartz 5 + GitHub Pages (sitio de guías)

**Sitio:** https://osvaldo-peralta.github.io/GuiasWildRift/
**Repo:** github.com/Osvaldo-Peralta/GuiasWildRift (Quartz **5.0.0**, config en YAML, no .ts)
**Diagnóstico:** 25/09/2026 — explorer lateral y graph view rotos.

## Causa raíz (cadena de evidencia)

1. `quartz.config.yaml` → `baseUrl: morningstar-wildrift.github.io/quartz` ❌ (valor de la plantilla original; el repo NO es fork de Osvaldo — se copió con ese baseUrl ajeno).
2. El build inyecta ese baseUrl en el HTML: `<body data-slug="index" data-basepath="/quartz">` y `og:url = https://morningstar-wildrift.github.io/quartz/index`.
3. El JS cliente (chunks `static/scripts/script-4/12`) calcula TODAS las rutas internas así:
   - basepath = `document.body.dataset.basepath` → espera `/quartz`
   - slug actual = `window.location.pathname` sin barras → en la realidad es `GuiasWildRift/...`
   - hrefs de nodos = `basepath + "/" + slug` → generan `/quartz/jinx` (404)
4. Consecuencia: el **explorer** (árbol de archivos hidratado por JS desde `static/contentIndex.json`) y el **graph** (canvas que resuelve el nodo actual por slug) no pueden reconciliar pathname real vs basepath → menú inoperativo y gráfico en blanco. El router SPA tampoco navega.
5. Descartado en el diagnóstico: assets CSS/JS cargan 200 con MIME correcto; `contentIndex.json` existe (17 slugs); las páginas anidadas usan rutas relativas con profundidad correcta (`../static/...`); el workflow deploy.yml es correcto tal cual.

## Arreglo (1 línea)

```yaml
# quartz.config.yaml
configuration:
  baseUrl: osvaldo-peralta.github.io/GuiasWildRift   # sin protocolo, sin slash final, casing exacto del repo
```

Push a `main` → el workflow reconstruye → verificar:
- [ ] `view-source:` de la home: `data-basepath="/GuiasWildRift"`
- [ ] Explorer: carpetas expanden y los links navegan sin recarga (SPA)
- [ ] Graph: nodos visibles, hover/click funcionan
- [ ] Búsqueda (Ctrl+K) navega bien
- [ ] `og:url` apunta a osvaldo-peralta.github.io/GuiasWildRift/...

## Notas de mantenimiento

- **Preview local** (`npx quartz build --serve`): si el graph/explorer fallan localmente tras el cambio, es por el baseUrl de Pages; para probar local usa temporalmente `localhost:8080`. La fuente de verdad es el build de Actions.
- **analytics: plausible** con ese baseUrl inyecta un data-domain inválido (inofensivo pero ruidoso). Si no tienes cuenta Plausible: quita el bloque o pon `analytics: null` según el esquema v5.
- **Workflow (deploy.yml):** correcto. Mejora opcional de velocidad: agregar `cache: npm` en setup-node. `fetch-depth: 0` es NECESARIO (el plugin created-modified-date usa git) — no quitarlo.
- El plugin `content-index` genera `static/contentIndex.json` + sitemap + RSS: tras arreglar baseUrl, el RSS/sitemap también apuntarán al dominio correcto (compartir links con OG cards funcionará).
- **Regla del lab:** cada vez que el sitio se mueva (rename de repo, dominio personalizado con CNAME), actualizar baseUrl en el mismo commit.
