from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.scanners.pumpfun_scanner import PumpFunScanner


app = FastAPI(
    title="Charlie Launch Intelligence API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


scanner = PumpFunScanner()


@app.get("/")
def inicio():
    return {
        "estado": "Charlie Launch Intelligence activo"
    }


@app.get("/ranking")
def ranking():
    return scanner.escanear()


@app.get("/analizar/{ticker}")
def analizar_token(ticker: str):
    return scanner.analizar(ticker)


@app.get("/recomendar")
def recomendar_lanzamiento():

    tokens = scanner.escanear()

    recomendados = []

    for token in tokens:
        if token.get("score", 0) >= 85:
            recomendados.append({
                "token": token["nombre"],
                "ticker": token["ticker"],
                "decision": "LANZAMIENTO RECOMENDADO",
                "score": token["score"]
            })

    return {
        "cantidad": len(recomendados),
        "recomendaciones": recomendados
    }
