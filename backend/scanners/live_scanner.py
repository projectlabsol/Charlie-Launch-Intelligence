import requests
import os


class LiveScanner:

    def __init__(self):

        self.helius_key = os.getenv(
            "HELIUS_API_KEY"
        )

        self.helius_rpc = (
            "https://mainnet.helius-rpc.com/?api-key="
            + str(self.helius_key)
        )


    def escanear_pumpfun(self):

        tokens = []

        # Aquí conectaremos Pump.fun real

        return tokens



    def escanear_mercado(self):

        tokens = []

        try:

            url = (
                "https://api.dexscreener.com/latest/dex/search?q=pump"
            )

            response = requests.get(
                url,
                timeout=20
            )

            data = response.json()

            pairs = data.get(
                "pairs",
                []
            )


            for pair in pairs:

                tokens.append({

                    "nombre":
                    pair.get("baseToken", {}).get("name"),

                    "ticker":
                    pair.get("baseToken", {}).get("symbol"),

                    "mint":
                    pair.get("baseToken", {}).get("address"),

                    "volumen":
                    pair.get("volume", {}).get("h24",0),

                    "liquidez":
                    pair.get("liquidity", {}).get("usd",0),

                    "url":
                    pair.get("url")

                })


        except Exception as e:

            print(
                "Dex error:",
                e
            )


        return tokens



    def analizar_score(self, token):

        score = 0


        if float(token.get("volumen",0)) > 10000:
            score += 30


        if float(token.get("liquidez",0)) > 5000:
            score += 20


        if token.get("nombre"):
            score += 10


        if token.get("ticker"):
            score += 10


        return score



    def recomendar(self):

        tokens = []

        tokens.extend(
            self.escanear_pumpfun()
        )

        tokens.extend(
            self.escanear_mercado()
        )


        for token in tokens:

            token["score"] = self.analizar_score(
                token
            )


        tokens.sort(
            key=lambda x:x.get("score",0),
            reverse=True
        )


        if len(tokens) > 0:

            return tokens[0]


        return {
            "mensaje":
            "No se encontraron oportunidades"
        }
