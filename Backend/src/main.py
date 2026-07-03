from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# import base64
from Backend.src.disease_identification import predict_disease
from Backend.src.fertilizer_recomendation import recommend_fertilizer
import argparse
import uvicorn
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
import os
import sys
from fastapi.responses import (
    FileResponse
)
from Backend.src.LLM import gemini_response
load_dotenv()
app = FastAPI(title="ARNA Backend")
PORT = int(os.environ.get("PORT", 8000))
# const port = process.env.PORT || 4000 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────────────────────
# PLUG YOUR MODELS HERE
# ─────────────────────────────────────────────────────────────
def resourcePath(relativePath):
    try:
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")
    return os.path.join(basePath, relativePath)



# disease_model = load_disease_model()
# rag_pipeline = load_rag_pipeline()
# llm = load_llm()

# ─────────────────────────────────────────────────────────────
# ENDPOINT 1: /analyze  (image → disease + fertilizer)
# ─────────────────────────────────────────────────────────────

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
   
    image_bytes = await file.read()

   
    disease,confidence=predict_disease(image_bytes)
    fertilizer=recommend_fertilizer(disease)

    # await file.read()  # consume file — remove when using real model

    # ── DUMMY RESPONSE — replace with your model output ──────
    return {
        "disease": disease,          # string: disease label
        "confidence": confidence,               # string: High / Medium / Low
        "fertilizer": fertilizer,    # string: fertilizer name only
    }


# ─────────────────────────────────────────────────────────────
# ENDPOINT 2: /chat  (message + history → reply)
# ─────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    # history: list = []     # [{"role": "user"/"assistant", "content": "..."}]
    # disease_context: str = ""   # pass detected disease so chat knows context

@app.post("/chat")
async def chat(body: ChatRequest):
   
    print(body.message)
    summary=gemini_response(body.message)
    # ── DUMMY RESPONSE — replace with your RAG + LLM output ──
    return {
        "reply": summary
    }


@app.get("/health")
def health():
    return {"status": "ok"}

_frontend_dir = resourcePath("Backend/src/frontend")
_static_dir = os.path.join(_frontend_dir, "static")

# Guard the mount so the app doesn't crash on startup (e.g. on Render) if the
# built frontend hasn't been copied into place yet.
if os.path.isdir(_static_dir):
    app.mount("/static", StaticFiles(directory=_static_dir), name="static")


@app.get("/{path_name:path}")
async def catch_all(path_name: str):
    index_path = os.path.join(_frontend_dir, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    return {"detail": "Frontend build not found. API is running at /analyze, /chat, /health."}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="ML tool",
        epilog="Developed by CR Rao AIMSCS",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Hostname to run the server on (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=PORT,
        help="Port to run the server on (default: 8000)",
    )

    args = parser.parse_args()
    uvicorn.run(
        app,
        host=args.host,
        port=args.port,
        log_level=None,
        # reload=True,
    )