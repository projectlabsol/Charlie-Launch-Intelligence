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

        # Próxima integración directa Pump.fun

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


                base = pair.get(
                    "baseToken",
                    {}
                )


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
                    base.get(
                        "symbol",
                        "UNKNOWN"
                    ),


                    "mint":
                    base.get(
                        "address"
                    ),


                    "imagen":
                    info.get(
                        "imageUrl"
                    ),


                    "web":
                    [],


                    "x":
                    None,


                    "volumen":
                    pair.get(
                        "volume",
                        {}
                    ).get(
                        "h24",
                        0
                    ),


                    "liquidez":
                    pair.get(
                        "liquidity",
                        {}
                    ).get(
                        "usd",
                        0
                    ),


                    "original":
                    pair.get(
                        "url"
                    )

                }



                # Extraer web y redes sociales

                for item in info.get(
                    "websites",
                    []
                ):

                    if item.get("url"):

                        token["web"].append(
                            item["url"]
                        )



                for social in info.get(
                    "socials",
                    []
                ):

                    if social.get("type") == "twitter":

                        token["x"] = social.get(
                            "url"
                        )



                tokens.append(
                    token
                )



        except Exception as e:

            print(
                "Dex error:",
                e
            )



        return tokens





    def analizar_score(self, token):

        score = 0



        volumen = float(
            token.get(
                "volumen",
                0
            )
        )


        liquidez = float(
            token.get(
                "liquidez",
                0
            )
        )



        if volumen >= 100000:

            score += 30

        elif volumen >= 10000:

            score += 20




        if liquidez >= 50000:

            score += 25

        elif liquidez >= 5000:

            score += 15




        if token.get(
            "imagen"
        ):

            score += 10



        if len(
            token.get(
                "web",
                []
            )
        ) > 0:

            score += 15




        if token.get(
            "x"
        ):

            score += 10




        if token.get(
            "nombre"
        ):

            score += 5



        if token.get(
            "ticker"
        ):

            score += 5



        return min(
            score,
            100
        )






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



        # Filtrar oportunidades reales

        candidatos = []


        for token in tokens:


            if token["score"] >= 60:

                candidatos.append(
                    token
                )



        candidatos.sort(
            key=lambda x:x.get(
                "score",
                0
            ),
            reverse=True
        )



        if candidatos:


            return candidatos[0]



        return {

            "mensaje":
            "No se encontraron oportunidades"

        }
