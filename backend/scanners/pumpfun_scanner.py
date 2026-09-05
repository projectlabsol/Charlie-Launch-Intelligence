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


    def obtener_transacciones(self):

        if not self.helius_key:
            return []


        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": [
                "11111111111111111111111111111111",
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

            return data.get(
                "result",
                []
            )


        except Exception as e:

            print(
                "Helius error:",
                e
            )

            return []



    def obtener_tokens(self):

        transacciones = self.obtener_transacciones()

        tokens = []


        for tx in transacciones:

            tokens.append({

                "nombre":
                "Token Solana detectado",

                "ticker":
                "UNKNOWN",

                "signature":
                tx.get("signature"),

                "meta":
                70,

                "volumen":
                70,

                "comunidad":
                70,

                "viralidad":
                70,

                "seguridad":
                70

            })


        return tokens



    def calcular_score(self, token):

        return int(
            (
                token["meta"] +
                token["volumen"] +
                token["comunidad"] +
                token["viralidad"] +
                token["seguridad"]
            ) / 5
        )



    def escanear(self):

        tokens = self.obtener_tokens()

        resultado = []


        for token in tokens:

            token["score"] = self.calcular_score(token)

            token["fecha_scan"] = (
                datetime.now().isoformat()
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
