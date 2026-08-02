import os
import json
from fastmcp import FastMCP
from garminconnect import Garmin

mcp = FastMCP("Garmin MCP")

def get_garmin_client():
    token_str = os.environ.get("GARMINTOKENS")
    if not token_str:
        raise ValueError("Brak GARMINTOKENS w środowisku Rendera!")
    
    import garth
    
    try:
        garth.client.loads(token_str)
        client = Garmin()
        client.login()
        return client
    except Exception:
        garth.client.token = token_str
        client = Garmin()
        return client

@mcp.tool()
def status() -> str:
    """Sprawdza status połączenia z kontem Garmin."""
    try:
        client = get_garmin_client()
        return f"Połączono pomyślnie! Zalogowany użytkownik: {client.get_full_name()}"
    except Exception as e:
        return f"Błąd połączenia: {str(e)}"

@mcp.tool()
def get_user_summary(date_str: str) -> str:
    """Pobiera ogólne podsumowanie dnia (kroki, spalone kalorie, tętno) dla daty YYYY-MM-DD."""
    try:
        client = get_garmin_client()
        stats = client.get_user_summary(date_str)
        return json.dumps(stats, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_activities(start_date: str, end_date: str) -> str:
    """Pobiera listę treningów i aktywności w podanym zakresie dat YYYY-MM-DD."""
    try:
        client = get_garmin_client()
        activities = client.get_activities_by_date(start_date, end_date)
        return json.dumps(activities, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_sleep_data(date_str: str) -> str:
    """Pobiera szczegółowe dane o śnie (fazy snu, ocena) dla daty YYYY-MM-DD."""
    try:
        client = get_garmin_client()
        sleep_data = client.get_sleep_data(date_str)
        return json.dumps(sleep_data, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_body_battery(date_str: str) -> str:
    """Pobiera dane Body Battery (poziom energii, ładowanie/rozładowanie) dla daty YYYY-MM-DD."""
    try:
        client = get_garmin_client()
        bb_data = client.get_body_battery(date_str)
        return json.dumps(bb_data, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_training_status(date_str: str) -> str:
    """Pobiera status treningowy (VO2Max, obciążenie, gotowość) dla daty YYYY-MM-DD."""
    try:
        client = get_garmin_client()
        status_data = client.get_training_status(date_str)
        return json.dumps(status_data, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_hrv_data(date_str: str) -> str:
    """Pobiera dane HRV (zmienność rytmu zatokowego) dla daty YYYY-MM-DD."""
    try:
        client = get_garmin_client()
        hrv = client.get_hrv_data(date_str)
        return json.dumps(hrv, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"