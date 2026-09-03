from datetime import datetime


class PumpFunScanner:


    def __init__(self):

        self.nombre = "Pump.fun Scanner"



    def obtener_tokens(self):

        tokens = [

            {
                "nombre": "Future AI Meme",
                "ticker": "$FAIM",
                "meta": 95,
                "volumen": 90,
                "comunidad": 85,
                "viralidad": 92,
                "seguridad": 80
            },

            {
                "nombre": "Animal Viral",
                "ticker": "$ANV",
                "meta": 88,
                "volumen": 82,
                "comunidad": 90,
                "viralidad": 85,
                "seguridad": 84
            }

        ]

        return tokens



    def calcular_score(self, token):

        score = (

            token["meta"] +
            token["volumen"] +
            token["comunidad"] +
            token["viralidad"] +
            token["seguridad"]

        ) // 5


        return score




    def analizar(self, ticker):

        ticker = ticker.upper()


        token = {

            "nombre": "Token analizado " + ticker,

            "ticker": "$" + ticker,

            "meta": 90,

            "volumen": 85,

            "comunidad": 88,

            "viralidad": 90,

            "seguridad": 82

        }


        token["score"] = self.calcular_score(token)

        token["fecha_scan"] = datetime.now().isoformat()


        if token["score"] >= 85:

            token["recomendacion"] = "🚀 LANZAMIENTO RECOMENDADO"

        elif token["score"] >= 70:

            token["recomendacion"] = "⚠️ ANALIZAR MÁS"

        else:

            token["recomendacion"] = "❌ NO RECOMENDADO"



        return token




    def escanear(self):


        resultado = []


        for token in self.obtener_tokens():


            token["score"] = self.calcular_score(token)

            token["fecha_scan"] = datetime.now().isoformat()


            resultado.append(token)


        return resultado
