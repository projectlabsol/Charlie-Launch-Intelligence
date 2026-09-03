from engine.charlie_engine import CharlieEngine
from scanners.pumpfun_scanner import PumpFunScanner


scanner = PumpFunScanner()
engine = CharlieEngine()


tokens = scanner.escanear()


for token in tokens:
    token["seguridad"] = 75
    token["comunidad"] = token.get("comunidad", 0)


resultado = engine.recomendar(tokens)


print("=== CHARLIE LAUNCH INTELLIGENCE ===")
print("TOKEN RECOMENDADO:")
print(resultado)
