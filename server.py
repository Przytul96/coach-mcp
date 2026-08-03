import os
import json
import garth
from fastmcp import FastMCP

mcp = FastMCP("Garmin MCP")

def init_garth():
    token_str = os.environ.get("GARMINTOKENS")
    if not token_str:
        raise ValueError("Brak GARMINTOKENS w środowisku Rendera!")
    
    token_clean = token_str.strip().strip('"')

    # 1. Próba natywnego wczytania (dla pełnych sesji)
    try:
        garth.client.loads(token_clean)
        return
    except Exception:
        pass

    # 2. Wyciągnięcie aktywnego tokena Bearer
    if token_clean.startswith("{"):
        try:
            data = json.loads(token_clean)
            if "oauth2_token" in data and isinstance(data["oauth2_token"], dict):
                token_clean = data["oauth2_token"].get("access_token", token_clean)
            else:
                token_clean = data.get("access_token", token_clean)
        except Exception:
            pass

    # Tworzymy kompletny obiekt OAuth2Token spełniający w 100% schemat walidacji garth
    garth.client.configure(domain="garmin.com")
    garth.client.oauth2_token = garth.http.OAuth2Token(
        scope="read write",
        jti="",
        access_token=token_clean,
        token_type="Bearer",
        refresh_token="",
        refresh_token_expires_in=0,
        refresh_token_expires_at=0,
        expires_in=86400,
        expires_at=2000000000
    )

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