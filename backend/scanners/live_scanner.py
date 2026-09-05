import requests
import os
import re



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

        """
        Aquí irá la conexión directa Pump.fun.
        El scanner principal actualmente usa mercado activo.
        """

        return []







    def escanear_mercado(self):


        tokens = []


        try:


            # Escaneo amplio Solana
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


                info = pair.get(
                    "info",
                    {}
                )


                mint = base.get(
                    "address"
                )


                if not mint:

                    continue



                nombre = base.get(
                    "name",
                    ""
                )


                ticker = base.get(
                    "symbol",
                    ""
                )



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
                    self.buscar_original(
                        mint,
                        pair.get("url")
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








    def buscar_original(
        self,
        mint,
        dex_url
    ):


        # enlace Pump.fun del token
        if mint:

            return (
                "https://pump.fun/"
                + mint
            )


        return dex_url








    def analizar_meta(
        self,
        token
    ):


        texto = (

            str(
                token.get("nombre","")
            )
            +
            " "
            +
            str(
                token.get("ticker","")
            )

        ).lower()



        metas = {


            "ai":
            [
                "ai",
                "agent",
                "gpt",
                "bot",
                "neural"
            ],


            "gaming":
            [
                "game",
                "gaming",
                "play",
                "meta"
            ],


            "animal":
            [
                "dog",
                "cat",
                "frog",
                "ape"
            ],


            "viral":
            [
                "meme",
                "pepe",
                "doge",
                "elon"
            ]

        }



        encontrada = "meme"



        for categoria,palabras in metas.items():


            for palabra in palabras:


                if palabra in texto:

                    encontrada = categoria



        return encontrada







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



        # volumen actual

        if volumen >= 1000000:

            score += 35

        elif volumen >= 100000:

            score += 25

        elif volumen >= 10000:

            score += 15





        # liquidez

        if liquidez >= 100000:

            score += 25

        elif liquidez >= 10000:

            score += 15





        # identidad

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




        # meta actual

        meta = self.analizar_meta(
            token
        )


        token["meta"] = meta



        if meta in [
            "ai",
            "gaming",
            "viral"
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



            if excluir and token.get(
                "mint"
            ) == excluir:

                continue





            token["score"] = self.analizar_score(
                token
            )



            candidatos.append(
                token
            )





        candidatos.sort(

            key=lambda x: (

                x.get(
                    "score",
                    0
                ),

                x.get(
                    "volumen",
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
