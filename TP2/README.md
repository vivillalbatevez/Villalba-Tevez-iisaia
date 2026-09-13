# API para Control de Stock de un Kiosco

Especificacion OpenAPI 3.0.0 para gestionar kioscos, productos, inventario y movimientos de stock.

## Archivo principal

- [openapi.yaml](openapi.yaml): definicion completa de la API.

## Servidor

```text
https://api.kiosco.local/v1
```

## Recursos y endpoints

### Kioscos

- `GET /kioscos`: lista todos los kioscos.
- `POST /kioscos`: crea un kiosco.

### Productos

- `GET /kioscos/{kioscoId}/productos`: lista los productos de un kiosco.
- `POST /kioscos/{kioscoId}/productos`: crea un producto.
- `GET /kioscos/{kioscoId}/productos/{productoId}`: obtiene un producto.
- `DELETE /kioscos/{kioscoId}/productos/{productoId}`: elimina un producto.

El listado de productos admite el filtro opcional `categoria`.

### Movimientos de stock

- `GET /kioscos/{kioscoId}/productos/{productoId}/movimientos`: consulta el historial.
- `POST /kioscos/{kioscoId}/productos/{productoId}/movimientos`: registra un movimiento y actualiza el stock.

Los tipos de movimiento permitidos son `INGRESO`, `VENTA` y `AJUSTE`.

## Schemas principales

- `Kiosco`: representa un kiosco existente.
- `KioscoInput`: datos necesarios para crear un kiosco.
- `Producto`: representa un producto con su stock actual.
- `ProductoInput`: datos necesarios para crear un producto.
- `MovimientoStock`: movimiento registrado, con fecha e identificador.
- `MovimientoStockInput`: datos necesarios para registrar un movimiento.
- `ErrorResponse`: formato comun para informar errores.

## Respuestas documentadas

- `200 OK`: lecturas exitosas.
- `201 Created`: creacion exitosa de kioscos, productos y movimientos.
- `204 No Content`: eliminacion exitosa de un producto.
- `400 Bad Request`: datos de entrada invalidos o incompletos.
- `404 Not Found`: kiosco o producto inexistente.
- `409 Conflict`: venta rechazada por stock insuficiente.

## Validacion local

Con Python y PyYAML instalados, desde la raiz del repositorio:

```powershell
python -c "import yaml; yaml.safe_load(open('TP2/openapi.yaml', encoding='utf-8')); print('YAML valido')"
```
