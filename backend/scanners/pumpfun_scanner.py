import os
import requests
from datetime import datetime


class PumpFunScanner:


    def __init__(self):

        self.nombre = "Charlie Launch Intelligence Scanner"

        self.api_key = os.getenv("HELIUS_API_KEY")

        self.base_url = (
            "https://mainnet.helius-rpc.com/?api-key="
            + str(self.api_key)
        )



    def obtener_tokens(self):

        """
        Obtiene actividad real de Solana usando Helius.
        """

        if not self.api_key:

            return []


        payload = {

            "jsonrpc":"2.0",
            "id":"charlie",
            "method":"getSignaturesForAddress",
            "params":[

                # Pump.fun program address
                "6EF8rrecthR5Dk7b7K7f4m8H5m9k9Q7Z7Y",

                {
                    "limit":20
                }

            ]

        }


        try:

            response = requests.post(
                self.base_url,
                json=payload,
                timeout=20
            )


            data=response.json()


            firmas=data.get(
                "result",
                []
            )


            tokens=[]


            for firma in firmas:


                tokens.append({

                    "nombre":
                    "Nuevo token Solana",


                    "ticker":
                    "PENDING",


                    "meta":
                    70,


                    "volumen":
                    70,


                    "comunidad":
                    70,


                    "viralidad":
                    70,


                    "seguridad":
                    70,


                    "signature":
                    firma.get("signature")

                })


            return tokens


        except Exception as e:


            print(e)

            return []




    def calcular_score(self, token):


        score=(

            token["meta"]+
            token["volumen"]+
            token["comunidad"]+
            token["viralidad"]+
            token["seguridad"]

        )//5


        return score





    def analizar(self,ticker):


        token={


            "nombre":
            "Token Solana "+ticker,


            "ticker":
            "$"+ticker.upper(),


            "meta":75,


            "volumen":75,


            "comunidad":75,


            "viralidad":75,


            "seguridad":75

        }



        token["score"] = self.calcular_score(token)


        token["fecha_scan"] = datetime.now().isoformat()



        if token["score"] >= 85:


            token["recomendacion"] = (
                "🚀 LANZAMIENTO RECOMENDADO"
            )


        elif token["score"] >=70:


            token["recomendacion"] = (
                "⚠️ ANALIZAR MÁS"
            )


        else:


            token["recomendacion"] = (
                "❌ NO RECOMENDADO"
            )



        return token





    def escanear(self):


        tokens=self.obtener_tokens()


        resultado=[]


        for token in tokens:


            token["score"] = self.calcular_score(token)


            token["fecha_scan"] = (
                datetime.now().isoformat()
            )


            resultado.append(token)



        return resultado
