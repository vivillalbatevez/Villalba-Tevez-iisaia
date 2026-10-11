"""Endpoint POST /api/analyze-room: foto -> propuesta de plano (aproximada).

Config por entorno:
    GEMINI_API_KEY      clave de Gemini API (sin ella: 503 provider_not_configured)
    VISION_MODEL        modelo con visión (default: gemini-3.8-flash)
  MAX_IMAGE_BYTES     tamaño máximo (default 8 MiB)
  FRONTEND_DIR        carpeta con index.html a servir en "/" (default ../frontend)
  CORS_ORIGINS        orígenes permitidos separados por coma (opcional)
La imagen solo vive en memoria durante la petición; nunca se guarda ni se loguea.
"""
import base64, json, os
from pathlib import Path
from typing import List, Literal, Optional

import httpx
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, ValidationError

FurnitureType = Literal["sofa", "mesa", "silla", "estante", "cama", "planta", "tv"]  # = FURNITURE_TYPES del editor
ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp"}
MAGIC = {"image/jpeg": lambda b: b[:3] == b"\xff\xd8\xff", "image/png": lambda b: b[:8] == b"\x89PNG\r\n\x1a\n",
         "image/webp": lambda b: b[:4] == b"RIFF" and b[8:12] == b"WEBP"}


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str):
        self.status, self.code, self.message = status, code, message


class ProviderError(Exception):
    pass


class Furniture(BaseModel):
    type: FurnitureType
    x: float = Field(ge=0, le=1)          # centro, proporción del ancho del ambiente
    y: float = Field(ge=0, le=1)          # centro, proporción de la profundidad
    width: float = Field(gt=0, le=1)
    depth: float = Field(gt=0, le=1)
    rotation_deg: float = Field(ge=-360, le=360)  # horario, vista cenital
    confidence: float = Field(ge=0, le=1)


class ProviderResult(BaseModel):
    furniture: List[Furniture]
    warnings: List[str] = []


class Calibration(BaseModel):
    status: Literal["uncalibrated", "user_provided"]
    width_m: Optional[float] = None


class RoomAnalysis(BaseModel):
    furniture: List[Furniture]
    warnings: List[str]
    calibration: Calibration


PROMPT = (
    "Analizá la foto de una habitación y proponé una vista cenital aproximada. Respondé SOLO JSON: "
    '{"furniture":[{"type","x","y","width","depth","rotation_deg","confidence"}],"warnings":[str]}. '
    "type solo puede ser: sofa, mesa, silla, estante, cama, planta, tv; ignorá cualquier otro objeto y mencionalo en warnings. "
    "x,y,width,depth son proporciones 0..1 del ambiente visible; rotation_deg horaria; confidence 0..1. "
    "No inventes muebles ocultos ni partes no visibles; avisá en warnings de oclusiones, baja confianza o elementos sin clasificar. "
    "Las medidas son estimadas: no afirmes dimensiones reales."
)


async def analyze_with_provider(image: bytes, mime: str) -> dict:
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise ApiError(503, "provider_not_configured", "El servicio de análisis no está configurado (falta GEMINI_API_KEY).")
    model = os.getenv("VISION_MODEL", "gemini-3.8-flash")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    body = {
        "contents": [{"parts": [
            {"text": PROMPT},
            {"inlineData": {"mimeType": mime, "data": base64.b64encode(image).decode()}},
        ]}],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0.1, "maxOutputTokens": 2000},
    }
    try:
        async with httpx.AsyncClient(timeout=45) as c:
            r = await c.post(url, json=body, headers={"x-goog-api-key": key})
        r.raise_for_status()
        parts = r.json()["candidates"][0]["content"]["parts"]
        text = "".join(part.get("text", "") for part in parts)
        return json.loads(text)
    except (httpx.HTTPError, ValueError, KeyError, TypeError) as e:
        raise ProviderError(type(e).__name__)  # solo el tipo: nunca contenido de la imagen


app = FastAPI(title="Modelador Espacial Rápido")
if os.getenv("CORS_ORIGINS"):
    app.add_middleware(CORSMiddleware, allow_origins=os.getenv("CORS_ORIGINS").split(","), allow_methods=["POST"])


@app.exception_handler(ApiError)
async def _api_error(_, e: ApiError):
    return JSONResponse(status_code=e.status, content={"error": {"code": e.code, "message": e.message}})


@app.post("/api/analyze-room", response_model=RoomAnalysis)
async def analyze_room(image: UploadFile = File(...), known_width_m: Optional[float] = Form(None)):
    if image.content_type not in ALLOWED_MIME:
        raise ApiError(400, "invalid_file_type", "Formato no admitido: usá JPG, PNG o WebP.")
    if known_width_m is not None and not (0 < known_width_m <= 100):
        raise ApiError(422, "invalid_calibration", "La medida conocida debe estar entre 0 y 100 metros.")
    limit = int(os.getenv("MAX_IMAGE_BYTES", 8 * 1024 * 1024))
    data = await image.read(limit + 1)
    if len(data) > limit:
        raise ApiError(413, "file_too_large", f"La imagen supera el máximo de {limit // (1024 * 1024)} MB.")
    if not data or not MAGIC[image.content_type](data):
        raise ApiError(422, "image_unreadable", "No se pudo interpretar la imagen: el archivo no coincide con su formato.")
    try:
        result = ProviderResult(**await analyze_with_provider(data, image.content_type))
    except ProviderError:
        raise ApiError(502, "provider_failure", "El proveedor de visión falló. Probá de nuevo en un momento.")
    except (ValidationError, TypeError):
        raise ApiError(502, "provider_failure", "El proveedor devolvió una respuesta inválida.")
    cal = Calibration(status="user_provided", width_m=known_width_m) if known_width_m else Calibration(status="uncalibrated")
    return RoomAnalysis(furniture=result.furniture, warnings=result.warnings, calibration=cal)


_front = Path(os.getenv("FRONTEND_DIR", Path(__file__).parent.parent / "frontend"))
if _front.is_dir():
    app.mount("/", StaticFiles(directory=_front, html=True), name="frontend")
