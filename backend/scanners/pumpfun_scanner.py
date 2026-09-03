import requests
from datetime import datetime


class PumpFunScanner:

    def __init__(self):
        self.nombre = "Pump.fun Scanner"


    def obtener_tokens(self):

        # Aquí conectaremos la API/fuente real de Pump.fun
        tokens = [
            {
                "nombre": "Nuevo Meme AI",
                "ticker": "$NMAI",
                "edad": "10 minutos",
                "meta": 90,
                "volumen": 85,
                "comunidad": 80,
                "viralidad": 88,
                "seguridad": 75
            }
        ]

        return tokens


    def escanear(self):

        tokens = self.obtener_tokens()

        for token in tokens:
            token["fecha_scan"] = datetime.now().isoformat()

        return tokens
