import requests
import os
import random



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
                "WETH"
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


                    "nombre":
                    nombre,


                    "ticker":
                    ticker,


                    "mint":
                    mint,


                    "imagen":
                    info.get(
                        "imageUrl"
                    ),



                    "volumen":
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
                "meme",
                "pepe",
                "doge",
                "elon"
            ]

        }



        for categoria,palabras in categorias.items():

            for palabra in palabras:

                if palabra in texto:

                    return categoria



        return "Meme"









    def analizar_score(
        self,
        token
    ):


        score = 0



        volumen = token.get(
            "volumen",
            0
        )


        liquidez = token.get(
            "liquidez",
            0
        )



        if volumen >= 1000000:

            score += 35

        elif volumen >= 100000:

            score += 25

        elif volumen >= 10000:

            score += 15



        if liquidez >= 100000:

            score += 25

        elif liquidez >= 10000:

            score += 15

        elif liquidez >= 5000:

            score += 10





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



        candidatos = []



        for token in tokens:


            if excluir and token.get("mint") == excluir:

                continue



            token["score"] = self.analizar_score(
                token
            )



            if token["score"] >= 50:

                candidatos.append(
                    token
                )





        candidatos.sort(

            key=lambda x: (

                x["score"],
                x["volumen"],
                x["liquidez"]

            ),

            reverse=True

        )



        if candidatos:


            # toma entre las mejores 5 para variar resultados

            mejores = candidatos[:5]


            return random.choice(
                mejores
            )




        return {

            "mensaje":
            "No se encontraron oportunidades"

        }
