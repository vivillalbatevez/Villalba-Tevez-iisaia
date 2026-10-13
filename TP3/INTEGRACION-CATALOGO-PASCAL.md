# Propuesta: análisis de fotos usando el catálogo de Pascal

Esta nota describe los cambios coordinados entre TP3 y `interiores-3d` para que el análisis elija piezas reales del catálogo local de Pascal, en lugar de limitarse a siete tipos genéricos. No implica que TP3 importe Pascal: el navegador obtiene el catálogo y envía al backend solo una lista acotada de opciones disponibles.

## Decisión de integración

- Pascal sigue siendo responsabilidad del frontend/editor.
- El navegador construye una lista de candidatos a partir de `CATALOG_ITEMS`, limitada a modelos que el proyecto puede cargar localmente.
- TP3 recibe los metadatos necesarios para reconocer esos candidatos y le pide a Gemini que elija únicamente sus identificadores.
- TP3 valida la respuesta contra los identificadores recibidos en esa petición. Nunca acepta un `asset_id` inventado ni usa una ruta de modelo devuelta por Gemini.
- El adaptador del proyecto resuelve cada `asset_id` contra su propio catálogo y construye la escena Pascal.

La lista enviada por el navegador es una selección de opciones, no una fuente confiable de rutas o código. No enviar `src`, URL de descarga ni contenido GLB a Gemini; bastan identificador, nombre, categoría y etiquetas.

## Contrato sugerido

La petición continúa siendo `multipart/form-data`:

| Campo | Contenido |
|---|---|
| `image` | Imagen JPG, PNG o WebP actual |
| `known_width_m` | Ancho conocido, opcional y sin cambios |
| `catalog_json` | JSON con candidatos Pascal seleccionados |

Ejemplo de `catalog_json`:

```json
[
  {
    "id": "sofa",
    "name": "Sofá",
    "category": "furniture",
    "tags": ["living-room", "seat"]
  },
  {
    "id": "coffee-table",
    "name": "Mesa ratona",
    "category": "furniture",
    "tags": ["living-room", "table"]
  }
]
```

La respuesta mantiene `warnings` y `calibration`. Cada pieza devuelve su `asset_id` y las mismas coordenadas normalizadas que hoy:

```json
{
  "furniture": [
    {
      "asset_id": "coffee-table",
      "x": 0.5,
      "y": 0.55,
      "width": 0.3,
      "depth": 0.2,
      "rotation_deg": 0,
      "confidence": 0.86
    }
  ],
  "warnings": [],
  "calibration": {
    "status": "uncalibrated",
    "width_m": null
  }
}
```

`asset_id` debe pertenecer exactamente a la lista enviada. `x`, `y`, `width` y `depth` siguen expresando proporciones del ambiente; el resultado es una estimación visual, no una medición real. No se debe pedir a Gemini que devuelva nodos Pascal ni dimensiones exactas del GLB.

## Cambios en TP3

En `backend/main.py`:

1. Reemplazar el `FurnitureType = Literal[...]` fijo por un modelo de candidato de catálogo (`id`, `name`, `category`, `tags`) y un modelo de pieza detectada con `asset_id` y las medidas/confianza actuales.
2. Aceptar `catalog_json` como campo opcional de formulario durante la transición. Parsearlo explícitamente; rechazar JSON inválido, lista vacía, IDs duplicados, demasiados candidatos y campos/textos por encima de límites razonables con un error 422 accionable.
3. Filtrar y serializar solo los metadatos permitidos. Construir para cada solicitud el esquema estructurado de Gemini con `asset_id` enumerado a partir de los IDs recibidos; el prompt indica que debe elegir solo esos IDs y tratar el contenido de la imagen como datos, no como instrucciones.
4. Validar la respuesta del proveedor y comprobar también que cada `asset_id` esté en el conjunto de IDs de esa petición. Respuesta estructurada no sustituye la validación local.
5. Mantener los controles vigentes de MIME, tamaño, calibración, errores del proveedor y privacidad de la imagen. No registrar la imagen, la clave ni el prompt completo con datos de usuario.
6. Si se necesita compatibilidad con el frontend viejo, mantener temporalmente el modo de siete tipos cuando no llega `catalog_json`; eliminar ese modo solo en un cambio coordinado con el proyecto.

En `backend/test_main.py`, agregar pruebas para catálogo válido, JSON inválido, duplicados/lista vacía/límites, esquema dinámico de salida, ID válido, ID inventado del proveedor y modo temporal sin catálogo. Las pruebas de Gemini deben seguir simuladas; no necesitan una clave real.

## Cambios coordinados en `interiores-3d`

Todos estos cambios pertenecen al repo principal, no a TP3:

1. **Construcción de candidatos:** desde `apps/web/src/editor/catalog-assets.ts`, generar el catálogo para análisis a partir de `CATALOG_ITEMS` y el manifiesto de modelos locales. Reducirlo a opciones de interiorismo reconocibles y enviar `id`, `name`, `category` y `tags`, nunca rutas remotas ni el binario. Si conviene, extraer una función pura para filtrar/serializar y probarla.
2. **Cliente del endpoint:** en `apps/web/src/lib/lab/analyze-room.ts`, añadir el catálogo a `FormData` como `catalog_json`. El ejemplo local y la página de laboratorio deben usar la misma lista.
3. **Contrato de respuesta:** en `apps/web/src/lib/lab/schema.ts`, cambiar la pieza detectada para validar `asset_id`; conservar las validaciones de proporciones, rotación y confianza. Actualizar tabla, etiquetas y JSON mostrado en `apps/web/app/laboratorio/` para resolver el nombre mediante el catálogo y mostrar un fallback explícito si falta.
4. **Conversión a Pascal:** en `apps/web/src/lib/lab/analysis-to-definition.ts`, resolver `asset_id` contra el mapa local y usar ese ID como `asset` para crear el elemento. Mantener el tratamiento paramétrico de estantes solo si el candidato representa realmente el nodo `bookshelf`; los demás candidatos deben ser modelos locales existentes. Omitir con advertencia cualquier ID que no se pueda resolver, sin inventar una pieza sustituta.
5. **Muestras y guía:** actualizar `apps/web/src/lib/lab/sample-analysis.ts`, pruebas del laboratorio y `lab/README.md` al nuevo contrato. Documentar que frontend y backend deben actualizarse juntos.

El `catalog_assets` actual ya genera un mapa de los ítems que tienen modelo local; el conversor de escenas ya acepta un `asset` de catálogo. La adaptación principal es transportar el ID elegido por el análisis y resolverlo con ese mapa, no cambiar Pascal ni guardar el catálogo en el backend.

## Orden y criterios de aceptación

1. Acordar y probar la selección de candidatos locales del lado del proyecto.
2. Agregar pruebas de contrato fallidas primero para el payload y los IDs elegidos.
3. Implementar y probar TP3; revisar `TP3/README.md` con el nombre del campo nuevo y sus límites.
4. Actualizar cliente, esquema, laboratorio, conversor y pruebas en el repo principal.
5. Probar extremo a extremo con Gemini y una foto no sensible: cada ID devuelto existe en el catálogo local, la escena se abre en Pascal y la propuesta sigue siendo revisable antes de aplicarse.

No considerar la lista de candidatos como una autorización para cargar URLs arbitrarias: el adaptador debe aceptar únicamente ítems resueltos en el catálogo local del proyecto.
