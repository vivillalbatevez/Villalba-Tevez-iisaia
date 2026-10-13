# Modelador Espacial Rápido

<<<<<<< HEAD
`POST /api/analyze-room` devuelve una propuesta neutral para integrarse con otros editores: posiciones
y tamaños normalizados entre 0 y 1, giro, confianza y advertencias. Si recibe el campo opcional
`catalog_json`, Gemini elige identificadores de la lista permitida y la aplicación los resuelve a piezas
del editor. Sin ese campo, se conserva el contrato anterior de siete tipos genéricos. TP3 no devuelve
un grafo de Pascal ni recibe rutas o archivos de modelos.

`catalog_json` debe ser un arreglo JSON de 1 a 100 opciones con `id`, `name`, `category` y `tags`
opcionales. El tamaño total máximo es 64 KB; cada ID debe ser único. No se aceptan propiedades adicionales
como `src` o URLs. Las opciones se usan solo durante esa solicitud y no se almacenan.

=======
>>>>>>> 718d31a2a94a0e4bc7c0a2070706df2b3a09ac24
El análisis de fotos usa Gemini API. Google AI Studio ofrece un nivel gratuito
con cuotas y modelos disponibles sujetos a cambios. La clave se guarda en el
backend; nunca la pongas en el HTML ni la subas al repositorio.

En PowerShell, desde `TP3`:

```powershell
cd backend
pip install -r requirements.txt
$env:GEMINI_API_KEY = "TU_CLAVE_DE_GOOGLE_AI_STUDIO"
# Opcional: el modelo por defecto es gemini-3.8-flash
# $env:VISION_MODEL = "gemini-3.8-flash"
python -m uvicorn main:app --port 8000
```

Abrí `http://localhost:8000`. Para ejecutar las pruebas, en otra terminal:

```powershell
cd TP3/backend
python -m pytest -q
```

Creá la clave en [Google AI Studio](https://aistudio.google.com/apikey). El
nivel gratuito tiene límites de uso que pueden cambiar; consultá los
[precios y cuotas actuales](https://ai.google.dev/gemini-api/docs/pricing).
En el tier gratuito Google puede usar el contenido enviado para mejorar sus
productos, según sus términos. No envíes fotos sensibles o privadas.
