import os
import json
from fastapi import FastAPI, HTTPException
from garminconnect import Garmin

# Inicjalizacja standardowego API zamiast MCP
app = FastAPI(
    title="Garmin API dla ChatGPT", 
    description="API do pobierania danych z Garmin Connect", 
    version="1.0.0"
)

def get_garmin_client():
    token_str = os.environ.get("GARMINTOKENS")
    if not token_str:
        raise ValueError("Brak GARMINTOKENS w środowisku Rendera!")
    
    import garth
    client = Garmin()
    
    try:
        garth.client.loads(token_str)
    except Exception:
        token_jwt = token_str
        if token_str.startswith("{"):
            try:
                token_jwt = json.loads(token_str).get("access_token", token_str)
            except Exception:
                pass
        
        class DummyToken:
            def __init__(self, jwt):
                self.access_token = jwt
                self.token_type = "Bearer"
                
        garth.client.oauth2_token = DummyToken(token_jwt)
        garth.client.domain = "garmin.com"
        
    try:
        profile = garth.client.get("connectapi", "/userprofile-service/socialProfile")
        client.display_name = profile.get("displayName")
        client.full_name = profile.get("fullName")
    except Exception as e:
        raise ValueError(f"Nie udało się pobrać profilu: {str(e)}")
        
    if not client.display_name:
        raise ValueError("Profil pobrany, ale nazwa (displayName) jest pusta!")
        
    return client

@app.get("/status")
def get_status():
    """Sprawdza status połączenia z kontem Garmin."""
    try:
        client = get_garmin_client()
        return {"status": "success", "message": f"Połączono: {client.full_name} ({client.display_name})"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/summary")
def get_user_summary(date_str: str):
    """Pobiera ogólne podsumowanie dnia (kroki, kalorie, tętno) dla daty YYYY-MM-DD."""
    try:
        client = get_garmin_client()
        return client.get_user_summary(date_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/activities")
def get_activities(start_date: str, end_date: str):
    """Pobiera listę treningów i aktywności w podanym zakresie dat YYYY-MM-DD."""
    try:
        client = get_garmin_client()
        return client.get_activities_by_date(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sleep")
def get_sleep_data(date_str: str):
    """Pobiera dane o śnie dla daty YYYY-MM-DD."""
    try:
        client = get_garmin_client()
        return client.get_sleep_data(date_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bodybattery")
def get_body_battery(date_str: str):
    """Pobiera dane Body Battery dla daty YYYY-MM-DD."""
    try:
        client = get_garmin_client()
        return client.get_body_battery(date_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trainingstatus")
def get_training_status(date_str: str):
    """Pobiera status treningowy dla daty YYYY-MM-DD."""
    try:
        client = get_garmin_client()
        return client.get_training_status(date_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/hrv")
def get_hrv_data(date_str: str):
    """Pobiera dane HRV dla daty YYYY-MM-DD."""
    try:
        client = get_garmin_client()
        return client.get_hrv_data(date_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))