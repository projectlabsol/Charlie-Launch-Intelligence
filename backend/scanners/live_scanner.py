import requests
import random


class LiveScanner:


    def __init__(self):

        self.urls = [
            "https://api.dexscreener.com/latest/dex/search?q=pump",
            "https://api.dexscreener.com/latest/dex/search?q=memecoin",
            "https://api.dexscreener.com/latest/dex/search?q=solana"
        ]



    def escanear_pumpfun(self):

        return []



    def escanear_mercado(self):

        tokens = []
        vistos = set()


        for url in self.urls:

            try:

                data = requests.get(
                    url,
                    timeout=20
                ).json()


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


                    if mint in vistos:
                        continue


                    vistos.add(mint)



                    ticker = base.get(
                        "symbol",
                        ""
                    )


                    if ticker.upper() in [
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
                            ""
                        ),

                        "ticker":
                        ticker,

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

                        "web":
                        None,

                        "x":
                        None
                    }



                    for s in info.get(
                        "socials",
                        []
                    ):

                        if s.get("type") in [
                            "twitter",
                            "x"
                        ]:

                            token["x"] = s.get(
                                "url"
                            )



                    token["score"] = self.calcular_score(
                        token
                    )


                    token["meta"] = "Meme"



                    tokens.append(
                        token
                    )


            except Exception as e:

                print(e)



        return tokens




    def calcular_score(
        self,
        token
    ):


        score = 0


        if token["volumen24h"] >= 1000000:

            score += 40

        elif token["volumen24h"] >= 100000:

            score += 30

        else:

            score += 20



        if token["liquidez"] >= 100000:

            score += 30

        elif token["liquidez"] >= 10000:

            score += 20

        else:

            score += 10



        if token.get("imagen"):

            score += 10


        if token.get("x"):

            score += 10


        return min(score,100)




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



        if not tokens:

            return {
                "mensaje":
                "Sin oportunidades"
            }



        tokens.sort(
            key=lambda x:x["score"],
            reverse=True
        )


        mejores = tokens[:20]


        return random.choice(
            mejores
        )
