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

        # Pendiente conexión directa Pump.fun API
        return []





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


                info = pair.get(
                    "info",
                    {}
                )


                nombre = base.get(
                    "name",
                    ""
                )


                ticker = base.get(
                    "symbol",
                    ""
                )


                if ticker.upper() in bloqueados:
                    continue



                mint = base.get(
                    "address"
                )


                if not mint:
                    continue



                token = {


                    "nombre": nombre,


                    "ticker": ticker,


                    "mint": mint,


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
                    pair.get(
                        "url"
                    ),


                    "web": None,


                    "x": None

                }



                websites = info.get(
                    "websites",
                    []
                )


                if websites:

                    token["web"] = websites[0].get(
                        "url"
                    )



                socials = info.get(
                    "socials",
                    []
                )


                for social in socials:

                    if social.get(
                        "type"
                    ) in [
                        "twitter",
                        "x"
                    ]:

                        token["x"] = social.get(
                            "url"
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






    def analizar_meta(
        self,
        token
    ):


        texto = (

            str(token.get("nombre",""))
            +
            " "
            +
            str(token.get("ticker",""))

        ).lower()



        if any(x in texto for x in [
            "ai",
            "agent",
            "gpt",
            "bot"
        ]):

            return "AI"



        if any(x in texto for x in [
            "game",
            "gaming",
            "play"
        ]):

            return "Gaming"



        if any(x in texto for x in [
            "dog",
            "cat",
            "frog",
            "ape"
        ]):

            return "Animal"



        if any(x in texto for x in [
            "pepe",
            "meme",
            "doge",
            "elon"
        ]):

            return "Viral"



        return "Meme"







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



        # Momentum

        if volumen > 1000000:

            score += 35

        elif volumen > 100000:

            score += 25

        elif volumen > 10000:

            score += 15



        # Liquidez

        if liquidez > 100000:

            score += 25

        elif liquidez > 10000:

            score += 15



        # Identidad

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

            score += 5



        meta = self.analizar_meta(
            token
        )


        token["meta"] = meta



        if meta in [
            "AI",
            "Gaming",
            "Viral"
        ]:

            score += 15



        token["score"] = min(
            score,
            100
        )


        return token["score"]








    def recomendar(self):


        tokens = []


        tokens.extend(
            self.escanear_pumpfun()
        )


        tokens.extend(
            self.escanear_mercado()
        )



        for token in tokens:

            self.analizar_score(
                token
            )



        tokens.sort(
            key=lambda x: (
                x.get(
                    "score",
                    0
                ),
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
