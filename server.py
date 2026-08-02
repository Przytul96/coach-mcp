import os
import json
from fastmcp import FastMCP
from garminconnect import Garmin, garth

mcp = FastMCP("Garmin MCP")

def get_garmin_client():
    token_str = os.environ.get("GARMINTOKENS")
    if not token_str:
        raise ValueError("Brak GARMINTOKENS w środowisku!")
    
    # Próba załadowania tokenów do wbudowanej sesji garth
    try:
        garth.client.loads(token_str)
        client = Garmin()
        client.login()
        return client
    except Exception:
        # Jeśli podano surowy token, przypisujemy go bezpośrednio
        garth.client.token = token_str
        client = Garmin()
        return client

@mcp.tool()
def status() -> str:
    try:
        client = get_garmin_client()
        return f"Połączono pomyślnie z Garmin Connect! Użytkownik: {client.get_full_name()}"
    except Exception as e:
        return f"Błąd połączenia: {str(e)}"

@mcp.tool()
def get_user_summary(date_str: str) -> str:
    """Pobiera podsumowanie dnia dla podanej daty (YYYY-MM-DD)."""
    try:
        client = get_garmin_client()
        stats = client.get_user_summary(date_str)
        return json.dumps(stats, ensure_ascii=False)
    except Exception as e:
        return f"Błąd pobierania danych: {str(e)}"