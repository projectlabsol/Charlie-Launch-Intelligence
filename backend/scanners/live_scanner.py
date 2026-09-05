import requests
import os

from backend.engine.relaunch_engine import RelaunchEngine



class LiveScanner:


    def __init__(self):

        self.helius_key = os.getenv(
            "HELIUS_API_KEY"
        )


        self.helius_rpc = (
            "https://mainnet.helius-rpc.com/?api-key="
            + str(self.helius_key)
        )


        self.engine = RelaunchEngine()





    def escanear_pumpfun(self):

        # Próxima conexión directa Pump.fun
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



                token["meta"] = self.analizar_meta(
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



        categorias = {


            "AI":
            [
                "ai",
                "agent",
                "gpt",
                "bot"
            ],


            "Gaming":
            [
                "game",
                "gaming",
                "play"
            ],


            "Animal":
            [
                "dog",
                "cat",
                "frog",
                "ape"
            ],


            "Viral":
            [
                "pepe",
                "meme",
                "doge",
                "elon"
            ]

        }



        for meta,palabras in categorias.items():

            for palabra in palabras:

                if palabra in texto:

                    return meta



        return "Meme"







    def analizar_score(
        self,
        token
    ):


        return self.engine.evaluar(
            token
        )["score"]







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



        candidatos = []



        for token in tokens:


            if excluir and token.get(
                "mint"
            ) == excluir:

                continue



            token = self.engine.evaluar(
                token
            )


            if token["score"] >= 50:

                candidatos.append(
                    token
                )





        candidatos.sort(
            key=lambda x:(
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





        if candidatos:

            return candidatos[0]



        return {

            "mensaje":
            "No se encontraron oportunidades"

        }
