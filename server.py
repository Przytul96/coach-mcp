import os
import garth
from garminconnect import Garmin
from fastmcp import FastMCP

# Utworzenie serwera MCP, zeby FastMCP nie zgłaszał błędu
mcp = FastMCP("Garmin MCP")

email = os.environ.get("GARMIN_EMAIL")
password = os.environ.get("GARMIN_PASSWORD")

if email and password:
    try:
        print("\n==========================================", flush=True)
        print("=== PROBA LOGOWANIA NA RENDERZE ===", flush=True)
        client = Garmin(email, password)
        client.login()
        
        # Garth przechowuje aktywną sesję w garth.client
        token_b64 = garth.client.dumps()
        print("=== OTO TWOJ POPRAWNY TOKEN (SKOPIUJ GO) ===", flush=True)
        print(token_b64, flush=True)
        print("==========================================\n", flush=True)
    except Exception as e:
        print(f"Blad logowania: {e}", flush=True)


@mcp.tool()
def status() -> str:
    return "OK"