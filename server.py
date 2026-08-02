import os
import garth
from garminconnect import Garmin

email = os.environ.get("GARMIN_EMAIL")
password = os.environ.get("GARMIN_PASSWORD")

if email and password:
    try:
        print("\n==========================================")
        print("=== PROBA LOGOWANIA NA RENDERZE ===")
        client = Garmin(email, password)
        client.login()
        token_b64 = garth.client.dumps()
        print("=== OTO TWOJ POPRAWNY TOKEN (SKOPIUJ GO) ===")
        print(token_b64)
        print("==========================================\n")
    except Exception as e:
        print(f"Blad logowania: {e}")