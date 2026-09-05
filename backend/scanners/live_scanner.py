import requests
import random


class LiveScanner:


    def __init__(self):

        self.urls = [
            "https://api.dexscreener.com/latest/dex/search?q=pump",
            "https://api.dexscreener.com/latest/dex/search?q=memecoin",
            "https://api.dexscreener.com/latest/dex/search?q=solana"
        ]

        self.vistos = set()





    def escanear_pumpfun(self):

        return []







    def escanear_mercado(self):


        tokens = []


        for url in self.urls:


            try:


                response = requests.get(
                    url,
                    timeout=20
                )


                data = response.json()


                for pair in data.get("pairs", []):


                    base = pair.get(
                        "baseToken",
                        {}
                    )


                    mint = base.get(
                        "address"
                    )


                    if not mint:

                        continue



                    if mint in self.vistos:

                        continue



                    symbol = base.get(
                        "symbol",
                        ""
                    )


                    if symbol.upper() in [
                        "SOL",
                        "USDC",
                        "USDT",
                        "WETH",
                        "WBTC"
                    ]:

                        continue



                    info = pair.get(
                        "info",
                        {}
                    )



                    token = {

                        "nombre":
                        base.get(
                            "name",
                            "Unknown"
                        ),


                        "ticker":
                        symbol,


                        "mint":
                        mint,


                        "imagen":
                        info.get(
                            "imageUrl"
                        ),


                        "volumen24h":
                        float(
                            pair.get(
                                "volume",
                                {}
                            ).get(
                                "h24",
                                0
                            )
                        ),


                        "liquidez":
                        float(
                            pair.get(
                                "liquidity",
                                {}
                            ).get(
                                "usd",
                                0
                            )
                        ),


                        "original":
                        "https://pump.fun/" + mint,


                        "dex":
                        pair.get(
                            "url"
                        ),


                        "web":
                        None,


                        "x":
                        None

                    }





                    for website in info.get(
                        "websites",
                        []
                    ):


                        if website.get(
                            "url"
                        ):

                            token["web"] = website["url"]

                            break





                    for social in info.get(
                        "socials",
                        []
                    ):


                        if social.get(
                            "type"
                        ) in [
                            "twitter",
                            "x"
                        ]:


                            token["x"] = social.get(
                                "url"
                            )

                            break





                    token["meta"] = self.detectar_meta(
                        token
                    )


                    token["score"] = self.calcular_score(
                        token
                    )


                    tokens.append(
                        token
                    )



            except Exception as e:

                print(
                    "Scanner:",
                    e
                )



        return tokens







    def detectar_meta(
        self,
        token
    ):


        texto = (

            token.get(
                "nombre",
                ""
            )
            +
            " "
            +
            token.get(
                "ticker",
                ""
            )

        ).lower()



        if any(x in texto for x in [
            "ai",
            "agent",
            "gpt",
            "bot"
        ]):

            return "AI"



        if any(x in texto for x in [
            "dog",
            "cat",
            "frog",
            "ape"
        ]):

            return "Animal"



        if any(x in texto for x in [
            "game",
            "gaming",
            "play"
        ]):

            return "Gaming"



        if any(x in texto for x in [
            "pepe",
            "meme",
            "elon"
        ]):

            return "Viral"



        return "Meme"








    def calcular_score(
        self,
        token
    ):


        score = 0



        volumen = token.get(
            "volumen24h",
            0
        )


        liquidez = token.get(
            "liquidez",
            0
        )



        if volumen >= 1000000:

            score += 40

        elif volumen >= 100000:

            score += 30

        elif volumen >= 50000:

            score += 20



        if liquidez >= 100000:

            score += 30

        elif liquidez >= 10000:

            score += 20



        if token.get(
            "imagen"
        ):

            score += 10



        if token.get(
            "x"
        ):

            score += 10



        if token.get(
            "web"
        ):

            score += 10



        return min(
            score,
            100
        )








    def recomendar(
        self,
        excluir=None
    ):


        tokens = self.escanear_mercado()



        if excluir:

            tokens = [

                t for t in tokens

                if t["mint"] != excluir

            ]



        tokens = [

            t for t in tokens

            if t["volumen24h"] >= 50000

            and t["liquidez"] >= 10000

        ]



        if not tokens:

            return {

                "mensaje":
                "Sin oportunidades"

            }



        tokens.sort(

            key=lambda x:(

                x["score"],

                x["volumen24h"],

                x["liquidez"]

            ),

            reverse=True

        )



        elegido = random.choice(
            tokens[:10]
        )


        self.vistos.add(
            elegido["mint"]
        )


        return elegido
