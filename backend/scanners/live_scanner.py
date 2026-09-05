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


        # memoria temporal
        self.mostrados = set()





    def escanear_pumpfun(self):

        # Próxima integración directa Pump.fun

        return []







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



                mint = base.get(
                    "address"
                )



                if not mint:

                    continue




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
                    ) == "twitter":


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



        if volumen >= 100000:

            score += 35

        elif volumen >= 10000:

            score += 20

        elif volumen >= 1000:

            score += 10





        if liquidez >= 50000:

            score += 30

        elif liquidez >= 5000:

            score += 20

        elif liquidez >= 1000:

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



            # evitar moneda actual

            if excluir and token["mint"] == excluir:

                continue




            # evitar monedas ya vistas

            if token["mint"] in self.mostrados:

                continue





            token["score"] = self.analizar_score(
                token
            )



            if token["score"] >= 60:

                candidatos.append(
                    token
                )






        candidatos.sort(
            key=lambda x:(
                x["score"],
                x["volumen"],
                x["liquidez"]
            ),
            reverse=True
        )





        if candidatos:


            elegido = candidatos[0]


            self.mostrados.add(
                elegido["mint"]
            )


            return elegido






        return {

            "mensaje":
            "No se encontraron oportunidades"

        }
