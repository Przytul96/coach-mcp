import os
from fastmcp import FastMCP
from garminconnect import Garmin

# Utworzenie serwera FastMCP
mcp = FastMCP("Garmin MCP")

def get_garmin_client():
    token = os.environ.get("GARMINTOKENS")
    if not token:
        raise ValueError("Brak zmiennej GARMINTOKENS w środowisku!")
    
    client = Garmin()
    # Logujemy się wyłącznie przy użyciu tokena (bez hasła/emaila!)
    client.login(token)
    return client


@mcp.tool()
def status() -> str:
    try:
        client = get_garmin_client()
        return f"Połączono pomyślnie z Garmin! Zalogowany użytkownik: {client.get_full_name()}"
    except Exception as e:
        return f"Błąd połączenia: {e}"


@mcp.tool()
def get_user_summary(date_str: str) -> str:
    """Pobiera podsumowanie dnia dla podanej daty (YYYY-MM-DD)."""
    try:
        client = get_garmin_client()
        stats = client.get_user_summary(date_str)
        return str(stats)
    except Exception as e:
        return f"Błąd pobierania danych: {e}"