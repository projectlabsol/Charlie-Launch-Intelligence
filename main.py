from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.scanners.live_scanner import LiveScanner


app = FastAPI(
    title="Charlie Launch Intelligence API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


scanner = LiveScanner()



@app.get("/")
def inicio():

    return {
        "estado": "Charlie Launch Intelligence activo"
    }



@app.get("/ranking")
def ranking():

    return scanner.escanear()



@app.get("/recomendar")
def recomendar_lanzamiento():

    token = scanner.recomendar()

    return {
        "recomendacion": token
    }



@app.get("/siguiente")
def siguiente():

    token = scanner.recomendar()

    return {
        "recomendacion": token
    }
