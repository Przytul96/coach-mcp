import os
import json
from datetime import datetime, timedelta
from fastmcp import FastMCP
from garminconnect import Garmin

mcp = FastMCP("Garmin Coach")
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
    """Generuje listę dat pomiędzy start_date a end_date (max 31 dni dla danych wellness)."""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end - start
    
    if delta.days < 0:
        raise ValueError("start_date nie może być późniejsze niż end_date.")
    if delta.days > 31:
        raise ValueError("Zakres dla danych wellness ograniczony do 31 dni w jednym zapytaniu.")
        
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
    """Pobiera listę aktywności w BEZWZGLĘDNYM zakresie dat YYYY-MM-DD (brak limitu dni dla aktywności)."""
    try:
        client = get_garmin_client()
        activities = client.get_activities_by_date(start_date, end_date)
        return json.dumps(activities, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_user_summary_history(start_date: str, end_date: str) -> str:
    """Pobiera ogólne podsumowanie dnia w zakresie YYYY-MM-DD (max 31 dni)."""
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

@mcp.tool()
def get_activity_laps(activity_id: str) -> str:
    """Pobiera szczegółowe dane poszczególnych okrążeń (laps/splits) dla konkretnej aktywności po jej activity_id. Zawiera moc, HR, czas i dystans dla każdego okrążenia."""
    try:
        client = get_garmin_client()
        laps = client.get_activity_splits(activity_id)
        return json.dumps(laps, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"

@mcp.tool()
def get_activity_timeline(activity_id: str, start_minute: int = 0, end_minute: int = 20) -> str:
    """
    Pobiera surowe, sekundowe próbki danych z treningu (moc, tętno, kadencja).
    UWAGA: Aby nie przekroczyć limitu tokenów, narzędzie wymusza podanie zakresu minutowego (start_minute, end_minute).
    """
    try:
        client = get_garmin_client()
        details = client.get_activity_details(activity_id)

        if not details or "activityDetailMetrics" not in details:
            return "Brak surowych danych sekundowych dla tej aktywności."

        metrics = details["activityDetailMetrics"]
        desc = details.get("metricDescriptors", [])

        # Zbuduj słownik indeksów dla odpowiednich kolumn danych
        keys = {d["key"]: d.get("metricsIndex", d.get("index")) for d in desc}

        idx_time = keys.get("sumElapsedDuration", 0) # Czas w sekundach
        idx_hr = keys.get("directHeartRate")
        idx_power = keys.get("directPower")
        idx_cad = keys.get("directBikeCadence") or keys.get("directRunCadence")

        start_sec = start_minute * 60
        end_sec = end_minute * 60

        filtered_data = []
        for m in metrics:
            vals = m["metrics"]
            if not vals or len(vals) <= idx_time: continue

            t = vals[idx_time]
            if t is None: continue

            # Zbieraj punkty tylko ze wskazanego przedziału czasowego
            if start_sec <= t <= end_sec:
                point = {"t": t}
                if idx_hr is not None and len(vals) > idx_hr and vals[idx_hr] is not None: 
                    point["hr"] = vals[idx_hr]
                if idx_power is not None and len(vals) > idx_power and vals[idx_power] is not None: 
                    point["pow"] = vals[idx_power]
                if idx_cad is not None and len(vals) > idx_cad and vals[idx_cad] is not None: 
                    point["cad"] = vals[idx_cad]
                
                filtered_data.append(point)

            if t > end_sec:
                break # Koniec przedziału - przerywamy pętlę, by oszczędzać zasoby

        return json.dumps(filtered_data, ensure_ascii=False)
    except Exception as e:
        return f"Błąd: {str(e)}"