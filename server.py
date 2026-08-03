import os
import json
from fastmcp import FastMCP
from garminconnect import Garmin

mcp = FastMCP("Garmin MCP")
_garmin_client = None

def get_garmin_client():
    global _garmin_client
    if _garmin_client is not None:
        return _garmin_client

    email = os.environ.get("GARMIN_EMAIL")
    password = os.environ.get("GARMIN_PASSWORD")
    
    if not email or not password:
        raise ValueError("Brak zmiennych GARMIN_EMAIL lub GARMIN_PASSWORD na Renderze!")
        
    try:
        client = Garmin(email, password)
        client.login()
        _garmin_client = client
        return client
    except Exception as e:
        raise ValueError(f"Błąd logowania bezpośrednio z Rendera: {str(e)}")

@mcp.tool()
def status() -> str:
    """Sprawdza status połączenia z kontem Garmin."""
    try:
        client = get_garmin_client()
        return f"Połączono pomyślnie! Zalogowany użytkownik: {client.full_name} ({client.display_name})"
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_user_summary(date_str: str) -> str:
    """Pobiera ogólne podsumowanie dnia (kroki, tętno) dla daty YYYY-MM-DD."""
    try:
        client = get_garmin_client()
        stats = client.get_user_summary(date_str)
        return json.dumps(stats, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_activities(start_date: str, end_date: str) -> str:
    """Pobiera listę aktywności w podanym zakresie dat YYYY-MM-DD."""
    try:
        client = get_garmin_client()
        activities = client.get_activities_by_date(start_date, end_date)
        return json.dumps(activities, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_sleep_data(date_str: str) -> str:
    """Pobiera dane o śnie dla daty YYYY-MM-DD."""
    try:
        client = get_garmin_client()
        sleep_data = client.get_sleep_data(date_str)
        return json.dumps(sleep_data, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_body_battery(date_str: str) -> str:
    """Pobiera dane Body Battery dla daty YYYY-MM-DD."""
    try:
        client = get_garmin_client()
        bb_data = client.get_body_battery(date_str)
        return json.dumps(bb_data, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_training_status(date_str: str) -> str:
    """Pobiera status treningowy dla daty YYYY-MM-DD."""
    try:
        client = get_garmin_client()
        status_data = client.get_training_status(date_str)
        return json.dumps(status_data, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_hrv_data(date_str: str) -> str:
    """Pobiera dane HRV dla daty YYYY-MM-DD."""
    try:
        client = get_garmin_client()
        hrv = client.get_hrv_data(date_str)
        return json.dumps(hrv, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"