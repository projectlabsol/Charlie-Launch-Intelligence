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


        # Programa oficial Pump.fun
        pumpfun_program = (
            "6EF8rrecthR5Dk7b7K7F6Y7F6D6"
        )


        payload = {

            "jsonrpc":"2.0",

            "id":1,

            "method":"getSignaturesForAddress",

            "params":[

                pumpfun_program,

                {
                    "limit":50
                }

            ]

        }


        try:

            r = requests.post(
                self.rpc,
                json=payload,
                timeout=20
            )


            data = r.json()


            firmas = data.get(
                "result",
                []
            )


            tokens=[]


            for item in firmas:


                tokens.append({

                    "nombre":
                    "Nuevo token Pump.fun",


                    "ticker":
                    "UNKNOWN",


                    "meta":75,

                    "volumen":75,

                    "comunidad":75,

                    "viralidad":75,

                    "seguridad":75,


                    "signature":
                    item.get("signature")

                })


            return tokens


        except Exception as e:

            print(e)

            return []




    def calcular_score(self, token):


        return int(

            (

            token["meta"]+
            token["volumen"]+
            token["comunidad"]+
            token["viralidad"]+
            token["seguridad"]

            ) / 5

        )





    def escanear(self):


        tokens = self.obtener_tokens()


        resultado=[]


        for token in tokens:


            token["score"] = self.calcular_score(token)


            token["fecha_scan"] = (
                datetime.now().isoformat()
            )


            if token["score"] >=85:

                token["recomendacion"] = (
                    "🚀 LANZAMIENTO RECOMENDADO"
                )

            elif token["score"] >=70:

                token["recomendacion"] = (
                    "⚠️ ANALIZAR"
                )

            else:

                token["recomendacion"] = (
                    "❌ NO RECOMENDADO"
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

            "score":0,

            "recomendacion":
            "Token no encontrado"

        }
