class CharlieEngine:

    def __init__(self):
        self.nombre = "Charlie Engine"

    def calcular_score(self, token):

        score = 0

        score += token.get("meta", 0) * 0.30
        score += token.get("volumen", 0) * 0.25
        score += token.get("comunidad", 0) * 0.20
        score += token.get("viralidad", 0) * 0.15
        score += token.get("seguridad", 0) * 0.10

        return round(score, 2)


    def recomendar(self, tokens):

        ranking = []

        for token in tokens:
            token["charlie_score"] = self.calcular_score(token)
            ranking.append(token)

        ranking.sort(
            key=lambda x: x["charlie_score"],
            reverse=True
        )

        return ranking[0]
