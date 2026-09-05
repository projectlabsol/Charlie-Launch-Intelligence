import os
import requests
from datetime import datetime


class PumpFunScanner:

    def __init__(self):

        self.nombre = "Charlie Launch Intelligence"

        self.helius_key = os.getenv("HELIUS_API_KEY")

        self.rpc = (
            "https://mainnet.helius-rpc.com/?api-key="
            + str(self.helius_key)
        )


    def obtener_tokens(self):

        if not self.helius_key:
            return []


        pumpfun_program = "6EF8rrecthR5Dk7b7K7F6Y7F6D6"


        payload = {

            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": [
                pumpfun_program,
                {
                    "limit": 100
                }
            ]

        }


        try:

            response = requests.post(
                self.rpc,
                json=payload,
                timeout=30
            )

            data = response.json()

            firmas = data.get("result", [])


            tokens = []


            for firma in firmas:

                tokens.append({

                    "nombre": "PumpFun Token",

                    "ticker": "UNKNOWN",

                    "signature": firma.get(
                        "signature"
                    ),

                    "meta": 70,

                    "volumen": 70,

                    "comunidad": 70,

                    "viralidad": 70,

                    "seguridad": 70

                })


            return tokens


        except Exception as e:

            print(
                "Error PumpFun:",
                e
            )

            return []



    def calcular_score(self, token):

        score = (

            token["meta"] +
            token["volumen"] +
            token["comunidad"] +
            token["viralidad"] +
            token["seguridad"]

        ) / 5


        return int(score)



    def escanear(self):

        tokens = self.obtener_tokens()

        resultado = []


        for token in tokens:

            token["score"] = self.calcular_score(token)

            token["fecha_scan"] = datetime.now().isoformat()


            if token["score"] >= 85:

                token["recomendacion"] = (
                    "🚀 RELANZAMIENTO POTENCIAL"
                )

            elif token["score"] >= 70:

                token["recomendacion"] = (
                    "⚠️ ANALIZAR"
                )

            else:

                token["recomendacion"] = (
                    "❌ DESCARTAR"
                )


            resultado.append(token)


        return resultado



    def analizar(self, ticker):

        tokens = self.escanear()


        for token in tokens:

            if token["ticker"] == ticker.upper():

                return token


        return {

            "ticker": ticker,

            "score": 0,

            "recomendacion":
            "Token no encontrado"

        }
