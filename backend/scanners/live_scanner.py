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


        try:

            url = (
                "https://frontend-api.pump.fun/coins"
                "?offset=0&limit=50"
                "&sort=created_timestamp"
                "&order=DESC"
            )


            response = requests.get(
                url,
                timeout=20
            )


            data = response.json()



            for item in data:


                mint = item.get(
                    "mint"
                )


                if not mint:
                    continue



                tokens.append({

                    "nombre":
                    item.get(
                        "name",
                        ""
                    ),


                    "ticker":
                    item.get(
                        "symbol",
                        ""
                    ),


                    "mint":
                    mint,


                    "imagen":
                    item.get(
                        "image_uri"
                    ),


                    "volumen24h":
                    0,


                    "liquidez":
                    0,


                    "original":
                    "https://pump.fun/" + mint,


                    "dex":
                    None,


                    "web":
                    None,


                    "x":
                    None

                })



        except Exception as e:

            print(
                "PumpFun error:",
                e
            )


        return tokens








    def escanear_mercado(self):


        tokens = []


        try:


            url = (
                "https://api.dexscreener.com/latest/dex/search?q=solana"
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


                base = pair.get(
                    "baseToken",
                    {}
                )


                ticker = base.get(
                    "symbol",
                    ""
                )


                if ticker.upper() in [
                    "SOL",
                    "USDC",
                    "USDT",
                    "WBTC",
                    "WETH"
                ]:

                    continue



                mint = base.get(
                    "address"
                )


                if not mint:
                    continue



                info = pair.get(
                    "info",
                    {}
                )



                tokens.append({

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


                    "dex":
                    pair.get(
                        "url"
                    ),


                    "web":
                    None,


                    "x":
                    None

                })


        except Exception as e:

            print(
                "Dex error:",
                e
            )


        return tokens








    def analizar_score(
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



        if volumen > 1000000:

            score += 40

        elif volumen > 100000:

            score += 25

        elif volumen > 10000:

            score += 15



        if liquidez > 100000:

            score += 30

        elif liquidez > 10000:

            score += 15



        if token.get(
            "imagen"
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



        tokens = [
            x for x in tokens
            if x["score"] >= 40
        ]



        tokens.sort(
            key=lambda x: (
                x["score"],
                x.get(
                    "volumen24h",
                    0
                ),
                x.get(
                    "liquidez",
                    0
                )
            ),
            reverse=True
        )



        if tokens:

            return tokens[0]



        return {

            "mensaje":
            "No se encontraron oportunidades"

        }
