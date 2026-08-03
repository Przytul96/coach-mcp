import os
import json
import garth
from fastmcp import FastMCP
from garminconnect import Garmin

mcp = FastMCP("Garmin MCP")

def get_garmin_client():
    token_str = os.environ.get("GARMINTOKENS")
    if not token_str:
        raise ValueError("Brak GARMINTOKENS w środowisku Rendera!")
    
    # 1. Ładowanie tokena bezpośrednio do garth
    try:
        garth.client.loads(token_str)
    except Exception as e:
        raise ValueError(f"Nieprawidłowy format GARMINTOKENS: {str(e)}")
    
    # 2. Inicjalizacja Garmin Connect z użyciem załadowanej sesji garth
    client = Garmin()
    client.garth = garth.client
    
    # 3. Pobranie nazwy użytkownika do weryfikacji połączenia
    try:
        profile = garth.client.get("connectapi", "/userprofile-service/socialProfile")
        client.display_name = profile.get("displayName")
        client.full_name = profile.get("fullName")
    except Exception as e:
        raise ValueError(f"Nie udało się pobrać profilu Garmina (błąd autoryzacji): {str(e)}")
        
    return client

@mcp.tool()
def status() -> str:
    """Sprawdza status połączenia z kontem Garmin."""
    try:
        client = get_garmin_client()
        return f"Połączono pomyślnie! Zalogowany użytkownik: {client.full_name} ({client.display_name})"
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