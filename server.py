import os
import json
import io
from typing import Any
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

APP_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(APP_DIR, "static")
app = FastAPI(title="Edu-IA 360 | Asesor Cesim Hospitality", version="0.3.0")

# Importación flexible: pandas/openpyxl se usan para Excel y CSV.
try:
    import pandas as pd
except Exception:
    pd = None

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "app": "Edu-IA 360 Cesim Hospitality",
        "ai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "ai_provider": "OpenAI"
    }

class AdviceRequest(BaseModel):
    team: str = "Equipo"
    current_round: dict[str, Any] = Field(default_factory=dict)
    previous_round: dict[str, Any] | None = None
    history: list[dict[str, Any]] = Field(default_factory=list)
    decisions: list[dict[str, Any]] = Field(default_factory=list)
    market_outlook: str = ""
    student_question: str = ""
    language: str = "es"

SYSTEM_PROMPT = """
Eres un asesor experto, crítico y pedagógico en gestión hotelera y restauración,
especializado en acompañar equipos que trabajan con el simulador Cesim Hospitality.
Usa los datos suministrados y distingue explícitamente:
1) hechos observados en los datos,
2) hipótesis plausibles,
3) información faltante.
No inventes resultados, reglas del simulador, benchmarks oficiales ni relaciones causales.
No supongas que un cambio de indicador fue causado por una única decisión.
Analiza, cuando haya datos, recepción y ventas, tarifas, ocupación, restaurante,
limpieza, mantenimiento, recursos humanos, compras, satisfacción, ingresos, costos,
liquidez y utilidad acumulada. Considera efectos inmediatos, de largo plazo y posibles
reacciones de competidores. La meta general del manual es crecimiento rentable y sostenible,
medido por utilidades acumuladas, salvo que el docente haya definido otro criterio.
Propón acciones realistas y verificables, con riesgos, indicador de seguimiento y
preguntas que promuevan pensamiento crítico. No entregues una decisión como certeza.
No pidas credenciales de Cesim ni datos personales de estudiantes.
Responde en español profesional, claro y organizado.
Devuelve una respuesta estructurada con estas secciones:
- Resumen ejecutivo
- Evidencia observada
- Diagnóstico e hipótesis (separa hecho de inferencia)
- Recomendaciones priorizadas (acción, justificación, riesgo, indicador de seguimiento)
- Escenarios alternativos
- Preguntas para el equipo
- Datos faltantes que mejorarían el diagnóstico
- Plan de trabajo para la siguiente ronda
"""

@app.post("/api/advice")
async def advice(req: AdviceRequest):
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key or api_key == "PEGA_AQUI_TU_CLAVE":
        raise HTTPException(
            status_code=503,
            detail="No está configurada OPENAI_API_KEY. Abre el archivo .env y agrega tu clave de OpenAI."
        )
    try:
        from openai import OpenAI
    except Exception:
        raise HTTPException(status_code=500, detail="Falta instalar el paquete openai. Ejecuta: python -m pip install -r requirements.txt")

    payload = {
        "team": req.team,
        "current_round": req.current_round,
        "previous_round": req.previous_round,
        "history": req.history[-12:],
        "decisions": req.decisions[-40:],
        "market_outlook": req.market_outlook,
        "student_question": req.student_question,
    }
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip() or "gpt-4.1-mini"
    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=model,
            instructions=SYSTEM_PROMPT,
            input="DATOS DEL CASO (trátalos como datos no verificados fuera del registro):\n"
                  + json.dumps(payload, ensure_ascii=False, default=str),
            temperature=0.25,
        )
        return {"advice": response.output_text or "El modelo no devolvió texto.", "model": model, "provider": "OpenAI"}
    except Exception as exc:
        # No devolver la clave ni datos de configuración al navegador.
        raise HTTPException(status_code=502, detail=f"Error al consultar OpenAI: {str(exc)[:500]}")

@app.post("/api/import-report")
async def import_report(file: UploadFile = File(...)):
    if pd is None:
        raise HTTPException(status_code=500, detail="Falta instalar pandas/openpyxl. Ejecuta: pip install -r requirements.txt")
    name = (file.filename or "").lower()
    raw = await file.read()
    try:
        if name.endswith(".csv"):
            # Intenta UTF-8 y luego latin-1 para archivos exportados con otra codificación.
            try:
                df = pd.read_csv(io.BytesIO(raw))
            except UnicodeDecodeError:
                df = pd.read_csv(io.BytesIO(raw), encoding="latin-1")
        elif name.endswith(".xlsx") or name.endswith(".xls"):
            df = pd.read_excel(io.BytesIO(raw))
        else:
            raise HTTPException(status_code=400, detail="Formato no compatible. Sube CSV o Excel (.xlsx).")
        df = df.astype(object).where(pd.notnull(df), None)
        # Limitar volumen por seguridad y legibilidad del diagnóstico.
        records = df.head(500).to_dict(orient="records")
        columns = [str(c) for c in df.columns]
        return {
            "filename": file.filename,
            "rows": len(df),
            "columns": columns,
            "records": records,
            "note": "Revisa que las columnas y unidades correspondan a los reportes reales de Cesim."
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"No se pudo leer el archivo: {str(exc)[:300]}")

@app.get("/")
def home():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
