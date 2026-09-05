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
        "estado":
        "Charlie Launch Intelligence activo"
    }





@app.get("/recomendar")
def recomendar_lanzamiento(
    excluir: str = None
):


    token = scanner.recomendar(
        excluir
    )


    return {

        "recomendacion":
        token

    }





@app.get("/ranking")
def ranking():


    tokens = scanner.escanear_mercado()


    for token in tokens:

        token["score"] = scanner.analizar_score(
            token
        )


    tokens.sort(
        key=lambda x:(
            x.get("score",0),
            x.get("volumen24h",0),
            x.get("liquidez",0)
        ),
        reverse=True
    )


    return tokens





@app.get("/analizar/{ticker}")
def analizar_token(
    ticker:str
):


    tokens = scanner.escanear_mercado()


    for token in tokens:


        if token.get("ticker","").upper() == ticker.upper():

            token["score"] = scanner.analizar_score(
                token
            )


            return token



    return {

        "ticker":
        ticker,

        "score":
        0,

        "mensaje":
        "Token no encontrado"

    }
