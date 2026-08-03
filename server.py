import os
import json
import garth
from fastmcp import FastMCP

mcp = FastMCP("Garmin MCP")

def init_garth():
    token_str = os.environ.get("GARMINTOKENS")
    if not token_str:
        raise ValueError("Brak GARMINTOKENS w środowisku Rendera!")
    
    # Ładowanie sesji base64 z wygenerowanego ciągu
    garth.client.loads(token_str)

@mcp.tool()
def status() -> str:
    """Sprawdza status połączenia z kontem Garmin."""
    try:
        init_garth()
        profile = garth.client.get("connectapi", "/userprofile-service/socialProfile")
        return f"Połączono pomyślnie! Zalogowany użytkownik: {profile.get('fullName')} ({profile.get('displayName')})"
    except Exception as e:
        return f"Błąd połączenia: {str(e)}"

@mcp.tool()
def get_user_summary(date_str: str) -> str:
    """Pobiera ogólne podsumowanie dnia dla daty YYYY-MM-DD."""
    try:
        init_garth()
        path = f"/usersummary-service/usersummary/daily/{date_str}"
        data = garth.client.get("connectapi", path)
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_activities(start_date: str, end_date: str) -> str:
    """Pobiera listę treningów i aktywności w podanym zakresie dat YYYY-MM-DD."""
    try:
        init_garth()
        path = f"/activitylist-service/activities/search/activities?startDate={start_date}&endDate={end_date}"
        data = garth.client.get("connectapi", path)
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_sleep_data(date_str: str) -> str:
    """Pobiera szczegółowe dane o śnie dla daty YYYY-MM-DD."""
    try:
        init_garth()
        path = f"/wellness-service/wellness/dailySleepData/{date_str}"
        data = garth.client.get("connectapi", path)
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_body_battery(date_str: str) -> str:
    """Pobiera dane Body Battery dla daty YYYY-MM-DD."""
    try:
        init_garth()
        path = f"/wellness-service/wellness/bodyBattery/reports/daily?startDate={date_str}&endDate={date_str}"
        data = garth.client.get("connectapi", path)
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_training_status(date_str: str) -> str:
    """Pobiera status treningowy dla daty YYYY-MM-DD."""
    try:
        init_garth()
        path = f"/metrics-service/metrics/trainingstatus/aggregated/{date_str}"
        data = garth.client.get("connectapi", path)
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_hrv_data(date_str: str) -> str:
    """Pobiera dane HRV dla daty YYYY-MM-DD."""
    try:
        init_garth()
        path = f"/hrv-service/hrv/{date_str}"
        data = garth.client.get("connectapi", path)
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"