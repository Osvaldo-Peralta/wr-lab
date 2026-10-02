# Plan de acción por etapas: Migración a Vercel + Next.js con backend de comunidad separado

**Versión:** 1.0
**Fecha:** 30 de septiembre de 2026
**Repositorios involucrados:**
- Laboratorio: [Osvaldo-Peralta/wr-lab](https://github.com/Osvaldo-Peralta/wr-lab)
- Guías actuales: [Osvaldo-Peralta/GuiasWildRift](https://github.com/Osvaldo-Peralta/GuiasWildRift)
- Nuevo frontend: `wr-guides-web` (por crear)
- Nuevo backend: `wr-guides-api` (por crear)

---

## 1. Principios rectores

1. **Separación de responsabilidades:** cada repositorio y servicio tiene una única responsabilidad clara.
2. **WR-LAB no se toca:** el laboratorio sigue siendo el motor de análisis; no se convierte en backend.
3. **Markdown sigue siendo la fuente editorial:** Obsidian y los archivos `.md` no se abandonan.
4. **Migración incremental:** no se reescribe todo de golpe; se valida cada fase antes de avanzar.
5. **Solo planes gratuitos:** Vercel Hobby y Supabase Free son suficientes para el alcance actual.
6. **La base de datos almacena estado, no contenido:** los reportes siguen viviendo en Markdown; Supabase guarda vistas, likes, usuarios y eventos.
7. **Backend desacoplado:** las funciones de comunidad viven en un repositorio separado, no dentro del frontend.

---

## 2. Arquitectura objetivo

```
                         ┌──────────────────┐
                         │      WR-LAB      │
                         │  Python / modelos│
                         │  validaciones    │
                         │  datos           │
                         └────────┬─────────┘
                                  │
                           Markdown generado
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   repositorio2   │
                         │  (frontend)      │
                         │  Next.js         │
                         │  SSG / SSR       │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
              Vercel        wr-guides-api   Vercel Analytics
              (Hobby)       (backend)       (Hobby)
                    │             │
                    │             ▼
                    │         Supabase
                    │         (Free)
                    │             │
                    │             ▼
                    │         PostgreSQL
                    │
                    ▼
              GitHub Pages
              (se retira)
```

**Tres repositorios + una base de datos:**

| Componente | Repositorio / Servicio | Responsabilidad |
|---|---|---|
| Análisis | `wr-lab` | Generar conocimiento y reportes Markdown |
| Frontend | `wr-guides-web` (nuevo) | Renderizar Markdown y exponer la experiencia de usuario |
| Backend | `wr-guides-api` (nuevo) | Gestionar likes, guardados, comentarios, usuarios |
| Base de datos | Supabase (Free) | Almacenar vistas, likes, usuarios y eventos |
| Hosting frontend | Vercel (Hobby) | Desplegar Next.js |
| Hosting backend | Vercel (Hobby) | Desplegar API de comunidad |

> **Regla de oro:** WR-LAB produce conocimiento. Next.js produce experiencia. El backend produce estado. Supabase almacena estado.

---

## 3. Límites de los planes gratuitos (a tener en cuenta)

### Vercel Hobby (Free)
- **Uso:** personal, no comercial. Proyectos sin fines de lucro encajan perfectamente.
- **Ancho de banda (Fast Data Transfer):** 100 GB/mes.
- **Function Invocations:** 1 millón/mes.
- **Build minutes:** 6,000/mes.
- **Despliegues por día:** 100.
- **Proyectos:** 200.

> **Alerta:** si se superan los límites, Vercel pausa las funciones hasta el siguiente ciclo de 30 días. No hay cobro automático.

### Supabase Free
- **Base de datos:** 500 MB.
- **Almacenamiento de archivos:** 1 GB.
- **Ancho de banda (egress):** 5 GB/mes.
- **Usuarios activos mensuales (MAU):** 50,000.
- **Edge Function invocations:** 500,000/mes.
- **Proyectos activos:** máximo 2.
- **Pausa automática:** después de 7 días de inactividad.
- **Row Level Security (RLS):** disponible y recomendado para todas las tablas.

> **Alerta:** el proyecto se pausa tras 7 días sin actividad. Se puede mitigar con un cron ligero o con uso regular durante el desarrollo.

---

## 4. Fases de ejecución

### Fase 0 — Congelar lo que ya funciona

**Objetivo:** asegurar que WR-LAB y el pipeline actual de Quartz no se rompan durante la migración.

**Tareas:**
1. Confirmar que `wr-lab` sigue generando reportes correctamente.
2. Confirmar que `GuiasWildRift` sigue desplegando en GitHub Pages sin cambios.
3. Documentar el estado actual del frontmatter de los reportes (campos como `champion`, `patch`, `role`, `version`, etc.).
4. Identificar qué componentes de Quartz se reutilizarán conceptualmente (layout, navegación, estilos) y cuáles se reemplazarán por componentes de Next.js.

**Entregable:** informe breve de estado actual y lista de componentes reutilizables.

**Riesgo:** bajo. No se modifica nada.

---

### Fase 1 — Definir el contrato de datos entre WR-LAB y el frontend

**Objetivo:** establecer explícitamente qué metadatos acompañan a cada reporte Markdown.

**Tareas:**
1. Revisar el frontmatter actual de los reportes en `wr-lab/reportes/`.
2. Definir un esquema mínimo de metadatos que Next.js consumirá para:
   - Listar guías por campeón, rol, parche.
   - Generar rutas (`/guias/jinx`, `/guias/caitlyn`, etc.).
   - Alimentar componentes dinámicos (vistas, likes).
3. Documentar el contrato en un archivo `CONTRATO_MARKDOWN_FRONTEND.md`.

**Ejemplo de frontmatter:**

```yaml
---
champion: Jinx
slug: jinx
role: ADC
patch: "7.3"
version: "1.4"
status: approved
archetype: crit-aoe
published_at: 2026-09-29
---
```

**Entregable:** documento de contrato de datos.

**Riesgo:** bajo. Solo es definición, no implementación.

---

### Fase 2 — Crear el repositorio del nuevo frontend (prototipo local)

**Objetivo:** construir un prototipo de Next.js que replique visualmente el sitio actual de Quartz, leyendo los mismos Markdown.

**Tareas:**
1. Crear un nuevo repositorio: `wr-guides-web`.
2. Inicializar un proyecto Next.js (App Router) con TypeScript.
3. Configurar la lectura de archivos Markdown desde una carpeta `content/`.
4. Implementar rutas dinámicas: `app/guias/[slug]/page.tsx`.
5. Renderizar el Markdown con un parser (p. ej. `remark` + `rehype`).
6. Replicar la estructura visual básica: cabecera, navegación, bloques de build, tablas.

**Importante:** en esta fase **no** se añaden likes ni vistas. El objetivo es solo reproducir la experiencia actual.

**Entregable:** prototipo local funcional (`npm run dev`).

**Riesgo:** medio. Puede requerir ajustes de estilos, pero no afecta al sitio en producción.

---

### Fase 3 — Crear el repositorio del backend (capa de servicios)

**Objetivo:** construir una API separada que gestione las funciones de comunidad.

**Tareas:**
1. Crear un nuevo repositorio: `wr-guides-api`.
2. Inicializar un proyecto Next.js (API Routes) o Express/Fastify según preferencia.
3. Definir los endpoints iniciales:

```
GET  /api/guides              # Listar guías con metadatos
GET  /api/guides/:slug        # Obtener metadatos de una guía
POST /api/guides/:slug/view   # Registrar vista
POST /api/guides/:slug/like   # Registrar like
GET  /api/guides/:slug/stats  # Obtener vistas y likes agregados
```

4. Configurar la conexión con Supabase (variables de entorno).
5. Implementar la lógica de identificación anónima (cookie con UUID) para vistas y likes.
6. Asegurar que un mismo visitante no pueda dar más de un like por guía.

**Entregable:** API funcional en local.

**Riesgo:** medio. Requiere coordinación entre frontend y Supabase, pero es acotado.

---

### Fase 4 — Configurar Supabase (esquema mínimo)

**Objetivo:** crear la base de datos que almacenará el estado dinámico.

**Tareas:**
1. Crear un proyecto en Supabase (plan Free).
2. Definir el esquema inicial:

```sql
-- Tabla de guías (referencia ligera, no contenido)
guides (
  id          bigint primary key,
  slug        text unique not null,
  champion    text,
  role        text,
  patch       text,
  published_at timestamp
);

-- Tabla de vistas
guide_views (
  id          bigint primary key,
  guide_id    bigint references guides(id),
  visitor_id  text,          -- identificador anónimo (cookie)
  created_at  timestamp default now()
);

-- Tabla de likes (anónimos en V1)
guide_likes (
  id          bigint primary key,
  guide_id    bigint references guides(id),
  visitor_id  text,          -- identificador anónimo (cookie)
  created_at  timestamp default now(),
  UNIQUE(guide_id, visitor_id)
);
```

3. Habilitar **Row Level Security (RLS)** en todas las tablas.
4. Crear políticas de acceso:
   - `guide_views`: inserción permitida para cualquiera; lectura solo para administradores.
   - `guide_likes`: inserción permitida para cualquiera; lectura agregada permitida para todos.
5. Sembrar la tabla `guides` con los slugs y metadatos de los reportes actuales.

**Entregable:** base de datos configurada y accesible desde el backend.

**Riesgo:** medio. La configuración de RLS debe ser cuidadosa, pero el plan Free es suficiente.

---

### Fase 5 — Conectar frontend con backend

**Objetivo:** integrar el frontend de Next.js con la API de comunidad.

**Tareas:**
1. Configurar la URL del backend como variable de entorno en el frontend (`NEXT_PUBLIC_API_URL`).
2. Implementar llamadas `fetch()` desde los componentes de Next.js hacia la API.
3. Mostrar en cada guía:

```
┌────────────────────────────────────────┐
│ Jinx — Build Optimizada                │
│                                        │
│ 👁️ 1,284 vistas       ❤️ 87 likes      │
│                                        │
│             [ ❤️ Me gusta ]            │
└────────────────────────────────────────┘
```

4. Implementar la lógica de identificación anónima (cookie con UUID) desde el frontend.
5. Registrar la vista al cargar la página y el like al hacer clic.

**Entregable:** funcionalidad de vistas y likes operativa en local.

**Riesgo:** medio. Requiere coordinación entre frontend y backend.

---

### Fase 6 — Desplegar frontend y backend en Vercel

**Objetivo:** llevar ambos proyectos a producción en Vercel (plan Hobby).

**Tareas:**
1. Conectar `wr-guides-web` a Vercel.
2. Configurar el proyecto (framework: Next.js, build command, output).
3. Conectar `wr-guides-api` a Vercel como proyecto separado.
4. Configurar variables de entorno en ambos proyectos (Supabase URL, keys, etc.).
5. Realizar el primer despliegue.
6. Comparar el sitio nuevo (`nuevo-dominio.vercel.app`) con el sitio antiguo (`osvaldo-peralta.github.io/GuiasWildRift`).
7. Mantener GitHub Pages activo como respaldo durante un periodo de transición.

**Entregable:** frontend y backend en Vercel funcionando con el contenido actual.

**Riesgo:** medio-bajo. Si algo falla, GitHub Pages sigue operativo.

---

### Fase 7 — Analytics con Vercel

**Objetivo:** empezar a medir el tráfico antes de introducir más funcionalidades interactivas.

**Tareas:**
1. Activar Vercel Web Analytics en el proyecto frontend.
2. Configurar eventos personalizados si se desea (p. ej. `guide_view`).
3. Identificar:
   - Páginas más visitadas.
   - Campeones más consultados.
   - Dispositivos y países de origen.

**Entregable:** panel de analytics accesible desde Vercel.

**Riesgo:** bajo. Es una capa de medición, no afecta al contenido.

---

### Fase 8 — Dashboard privado y siguientes pasos

**Objetivo:** visualizar los datos recogidos y planificar la evolución.

**Tareas:**
1. Crear una ruta protegida `/admin` en el frontend (inicialmente con una contraseña simple o Vercel Password Protection).
2. Mostrar métricas agregadas:

```
┌──────────────────────────────────────────┐
│ WR Guides Analytics                      │
├──────────────────────────────────────────┤
│ 👁️ Total views            12,481         │
│ ❤️ Total likes               823         │
│                                          │
│ Campeón       Views       Likes          │
│ Jinx          3,421       281            │
│ Caitlyn       2,812       193            │
│ Diana         1,983       141            │
│ Yuumi         1,202        89            │
└──────────────────────────────────────────┘
```

3. Evaluar la incorporación de:
   - **V2:** cuentas de usuario (Supabase Auth), likes asociados a usuario, favoritos.
   - **V3:** comentarios, historial de builds, builds favoritas.
   - **V4:** dashboard avanzado, estadísticas por parche, experimentos.

**Entregable:** dashboard funcional y hoja de ruta para V2–V4.

**Riesgo:** bajo. Es una capa de visualización sobre datos ya existentes.

---

## 5. Qué NO hacer

- **No meter una base de datos dentro de WR-LAB.** El laboratorio debe seguir siendo exclusivamente analítico.
- **No convertir Quartz en una aplicación completa.** Si se empieza a añadir autenticación, perfiles, comentarios y API dentro de Quartz, es señal de que ya se necesita Next.js.
- **No abandonar Markdown.** El contenido sigue siendo Markdown; la base de datos solo almacena estado dinámico.
- **No migrar todo de golpe.** Cada fase debe validarse antes de pasar a la siguiente.
- **No mezclar frontend y backend en un solo repositorio.** La separación permite escalar y mantener cada capa de forma independiente.

---

## 6. Checklist de decisión antes de empezar

- [ ] ¿WR-LAB sigue funcionando sin cambios?
- [ ] ¿El frontmatter de los reportes es consistente y suficiente para el frontend?
- [ ] ¿El prototipo de Next.js replica fielmente el sitio actual?
- [ ] ¿El backend maneja correctamente la identificación anónima?
- [ ] ¿Vercel Hobby cubre las necesidades de tráfico y funciones?
- [ ] ¿Supabase Free cubre el volumen de datos esperado?
- [ ] ¿Se ha habilitado RLS en todas las tablas?
- [ ] ¿Existe un plan de contingencia si Supabase se pausa por inactividad?
- [ ] ¿GitHub Pages se mantiene como respaldo durante la transición?

---

## 7. Resumen de plazos estimados (referencial)

| Fase | Duración estimada | Dependencias |
|---|---|---|
| Fase 0 — Congelar | 1 día | Ninguna |
| Fase 1 — Contrato de datos | 1–2 días | Fase 0 |
| Fase 2 — Prototipo Next.js | 3–5 días | Fase 1 |
| Fase 3 — Backend (API) | 3–5 días | Fase 1 |
| Fase 4 — Supabase | 2–3 días | Fase 3 |
| Fase 5 — Conectar frontend y backend | 2–3 días | Fases 2, 3, 4 |
| Fase 6 — Despliegue en Vercel | 1–2 días | Fase 5 |
| Fase 7 — Analytics | 1 día | Fase 6 |
| Fase 8 — Dashboard | 2–4 días | Fase 7 |

---

## 8. Conclusión

La migración a Vercel + Supabase no implica abandonar Quartz ni WR-LAB. Implica **separar la capa de publicación estática de la capa de aplicación interactiva**. Quartz sigue siendo útil para el sitio actual; Next.js será el nuevo frontend; el backend (`wr-guides-api`) gestionará las funciones de comunidad; Supabase será el estado; WR-LAB seguirá siendo el motor de conocimiento.

Con los planes gratuitos de Vercel y Supabase, el proyecto tiene margen suficiente para validar la nueva arquitectura sin coste alguno. El siguiente paso inmediato es ejecutar la **Fase 0** y la **Fase 1** para tener el contrato de datos listo antes de escribir la primera línea de Next.js.