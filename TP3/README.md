# Modelador Espacial Rápido

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
