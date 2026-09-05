class RelaunchEngine:


    def __init__(self):
        pass



    def calcular_score(self, token):

        score = 0


        volumen = float(
            token.get(
                "volumen24h",
                0
            )
        )


        liquidez = float(
            token.get(
                "liquidez",
                0
            )
        )



        if volumen >= 1000000:
            score += 30

        elif volumen >= 100000:
            score += 20

        elif volumen >= 10000:
            score += 10



        if liquidez >= 100000:
            score += 25

        elif liquidez >= 10000:
            score += 15



        if token.get("imagen"):
            score += 10



        if token.get("x"):
            score += 10



        if token.get("web"):
            score += 5



        meta = token.get(
            "meta",
            "Meme"
        )


        if meta in [
            "AI",
            "Gaming",
            "Viral"
        ]:

            score += 20



        return min(
            score,
            100
        )




    def evaluar(self, token):

        token["score"] = self.calcular_score(
            token
        )

        return token
