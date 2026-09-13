# **OpenAPI para control de stock**

[https://gemini.google.com/app/806faecad05b0945](https://gemini.google.com/app/806faecad05b0945)

*User prompt: Actúa como un arquitecto de software backend. Genera el código completo de un archivo openapi.yaml (versión 3.0.0) para una "API para control de stock de un kiosco". Define los siguientes Schemas en components: Producto: id (uuid), nombre (string), categoria (string), precio (number/double), stockActual (integer/int32), fechaActualizacion (string/date-time). Todos requeridos excepto fechaActualizacion. MovimientoStock: id (uuid), tipo (string, enum: \[INGRESO, VENTA, AJUSTE\]), cantidad (integer/int32), motivo (string), fecha (string/date-time). Todos requeridos excepto motivo. KioscoInput y ProductoInput para usar en los POST (sin los IDs generados por el servidor).*

Response: I will now generate the complete OpenAPI 3.0.0 specification file for the Kiosk Stock Control API, including all requested schemas, paths, and components.

I have successfully generated the OpenAPI 3.0.0 specification file for your kiosk stock control API, structured with all required schemas (Producto, MovimientoStock, ProductoInput, and an additional input schema for movimientos), clean paths, parameter definitions, and proper use of enums and data formats.

---

*User prompt: Genera los siguientes endpoints respetando estrictamente esta jerarquía de paths y methods: Kioscos: GET /kioscos y POST /kioscos Productos: GET /kioscos/{kioscoId}/productos, POST /kioscos/{kioscoId}/productos, GET /kioscos/{kioscoId}/productos/{productoId} y DELETE /kioscos/{kioscoId}/productos/{productoId} Movimientos: GET /kioscos/{kioscoId}/productos/{productoId}/movimientos y POST /kioscos/{kioscoId}/productos/{productoId}/movimientos*

Response: I will now update the OpenAPI specification to incorporate the new hierarchical path structure with kiosks, scoped products, and stock movements, including the requested endpoints and schemas.

I have successfully updated the OpenAPI specification file. The endpoints now strictly follow your requested hierarchical path structure (/kioscos, /kioscos/{kioscoId}/productos, /kioscos/{kioscoId}/productos/{productoId}, and /kioscos/{kioscoId}/productos/{productoId}/movimientos), and include all required request inputs and response schemas.

---

*User prompt: Respuestas (Responses) que debes documentar obligatoriamente: 200 OK para lecturas exitosas y 201 Created para todos los POST. 400 Bad Request si el body enviado en un POST no cumple con los schemas (ej. faltan campos). 404 Not Found en los endpoints con {id} si el kiosco o producto no existe. 409 Conflict específicamente en el POST de movimientos, describiendo que ocurre si se intenta realizar una VENTA con cantidad superior al stockActual.*

Response: I will now update the OpenAPI specification file to include all required HTTP response status codes (200, 201, 400, 404, and specifically 409 Conflict for insufficient stock during a sale) across the endpoints.

I have successfully updated the OpenAPI specification file with all requested responses: 200 OK for reads, 201 Created for POSTs, 400 Bad Request for invalid payloads, 404 Not Found for missing resources, and 409 Conflict specifically detailed on the stock movement endpoint for attempting sales exceeding current inventory levels.

---

