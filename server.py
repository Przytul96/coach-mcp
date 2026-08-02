import os
import json
import base64
from fastmcp import FastMCP
from garminconnect import Garmin
import garth

mcp = FastMCP("Garmin MCP")

def get_garmin_client():
    token_str = os.environ.get("GARMINTOKENS")
    if not token_str:
        raise ValueError("Brak GARMINTOKENS w środowisku!")
    
    # Próba załadowania zrzutu sesji garth
    try:
        garth.client.loads(token_str)
        client = Garmin()
        client.login()
        return client
    except Exception:
        # Jeśli podano surowy token/JWT, logujemy sesję bezpośrednio w garth
        garth.client.token = token_str
        client = Garmin()
        return client

@mcp.tool()
def status() -> str:
    try:
        client = get_garmin_client()
        # Wywołujemy proste zapytanie sprawdzające status sesji
        profile = client.get_user_summary("2026-08-02")
        return "Połączono pomyślnie z Garmin Connect! Integracja działa."
    except Exception as e:
        return f"Błąd połączenia z Garmin: {str(e)}"

@mcp.tool()
def get_user_summary(date_str: str) -> str:
    """Pobiera podsumowanie dnia dla podanej daty (YYYY-MM-DD)."""
    try:
        client = get_garmin_client()
        stats = client.get_user_summary(date_str)
        return json.dumps(stats, ensure_ascii=False)
    except Exception as e:
        return f"Błąd pobierania danych: {str(e)}"