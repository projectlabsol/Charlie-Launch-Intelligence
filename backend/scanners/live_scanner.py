import requests
import time


class LiveScanner:


    def __init__(self):

        self.dex_url = (
            "https://api.dexscreener.com/latest/dex/search?q=solana"
        )

        self.ultimo_mint = None





    def escanear_pumpfun(self):

        return []






    def escanear_mercado(self):


        tokens = []


        try:

            response = requests.get(
                self.dex_url,
                timeout=20
            )


            data = response.json()


            pairs = data.get(
                "pairs",
                []
            )



            bloqueados = [
                "SOL",
                "USDC",
                "USDT",
                "WETH",
                "WBTC"
            ]



            for pair in pairs:


                base = pair.get(
                    "baseToken",
                    {}
                )


                symbol = base.get(
                    "symbol",
                    ""
                )


                if symbol.upper() in bloqueados:

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




                socials = info.get(
                    "socials",
                    []
                )


                for social in socials:

                    if social.get("type") in [
                        "twitter",
                        "x"
                    ]:

                        token["x"] = social.get(
                            "url"
                        )



                websites = info.get(
                    "websites",
                    []
                )


                if websites:

                    token["web"] = websites[0].get(
                        "url"
                    )



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
                "Scanner error:",
                e
            )



        return tokens







    def detectar_meta(
        self,
        token
    ):


        texto = (
            token.get("nombre","")
            +
            " "
            +
            token.get("ticker","")
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

        elif volumen >= 10000:

            score += 20



        if liquidez >= 100000:

            score += 30

        elif liquidez >= 10000:

            score += 20

        else:

            score += 10




        if token.get("imagen"):

            score += 10



        if token.get("x"):

            score += 10



        if token.get("web"):

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
                if t.get("mint") != excluir
            ]



        if not tokens:

            return {

                "mensaje":
                "Sin oportunidades"

            }



        tokens.sort(
            key=lambda x:(
                x.get("score",0),
                x.get("volumen24h",0),
                x.get("liquidez",0)
            ),
            reverse=True
        )



        elegido = tokens[0]


        self.ultimo_mint = elegido["mint"]


        return elegido
