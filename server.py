import os
import json
from datetime import datetime, timedelta
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
        raise ValueError(f"Błąd logowania: {str(e)}")

def generate_date_range(start_date: str, end_date: str) -> list:
    """Generuje listę dat pomiędzy start_date a end_date (max 31 dni)."""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end - start
    
    if delta.days < 0:
        raise ValueError("start_date nie może być późniejsze niż end_date.")
    if delta.days > 31:
        raise ValueError("Zakres dat ograniczony do 31 dni, aby uniknąć blokady konta Garmin.")
        
    return [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(delta.days + 1)]

@mcp.tool()
def status() -> str:
    """Sprawdza status połączenia z kontem Garmin."""
    try:
        client = get_garmin_client()
        return f"Połączono pomyślnie! Zalogowany użytkownik: {client.full_name} ({client.display_name})"
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
def get_user_summary_history(start_date: str, end_date: str) -> str:
    """Pobiera ogólne podsumowanie dnia (kroki, tętno) w zakresie YYYY-MM-DD (max 31 dni)."""
    try:
        client = get_garmin_client()
        dates = generate_date_range(start_date, end_date)
        data = {d: client.get_user_summary(d) for d in dates}
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_sleep_history(start_date: str, end_date: str) -> str:
    """Pobiera dane o śnie dla zakresu dat YYYY-MM-DD (max 31 dni)."""
    try:
        client = get_garmin_client()
        dates = generate_date_range(start_date, end_date)
        data = {d: client.get_sleep_data(d) for d in dates}
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_body_battery_history(start_date: str, end_date: str) -> str:
    """Pobiera dane Body Battery dla zakresu dat YYYY-MM-DD (max 31 dni)."""
    try:
        client = get_garmin_client()
        dates = generate_date_range(start_date, end_date)
        data = {d: client.get_body_battery(d) for d in dates}
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_training_status_history(start_date: str, end_date: str) -> str:
    """Pobiera status treningowy dla zakresu dat YYYY-MM-DD (max 31 dni)."""
    try:
        client = get_garmin_client()
        dates = generate_date_range(start_date, end_date)
        data = {d: client.get_training_status(d) for d in dates}
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_hrv_history(start_date: str, end_date: str) -> str:
    """Pobiera dane HRV dla zakresu dat YYYY-MM-DD (max 31 dni)."""
    try:
        client = get_garmin_client()
        dates = generate_date_range(start_date, end_date)
        data = {d: client.get_hrv_data(d) for d in dates}
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"