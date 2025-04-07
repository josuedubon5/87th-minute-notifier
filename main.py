import requests
import time
from datetime import datetime

# API keys and tokens
API_FOOTBALL_KEY = "4903862a832206775e6a26332ace6bfc"
PUSHOVER_TOKEN = "aopb13c1uqxxwxwbtptmzxb9rsq5m3"
PUSHOVER_USER_KEY = "uxixd9y1o7mzhxu5xo4p7meyqoowem"

# Only check games in leagues that are on DraftKings
LEAGUE_IDS = [
    39, 140, 78, 61, 135, 71, 94, 179, 88, 203,
    197, 134, 144, 119, 2, 4, 1, 305, 253, 262,
    307, 113, 103
]

# Store notified match IDs to avoid duplicate alerts
notified_matches = set()

def send_notification(message):
    url = "https://api.pushover.net/1/messages.json"
    data = {
        "token": PUSHOVER_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": message,
    }
    requests.post(url, data=data)

def check_matches():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {"x-apisports-key": API_FOOTBALL_KEY}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error fetching data:", response.status_code)
        return

    data = response.json()
    fixtures = data.get("response", [])

    for fixture in fixtures:
        fixture_id = fixture["fixture"]["id"]
        league_id = fixture["league"]["id"]
        status = fixture["fixture"]["status"]["elapsed"]
        home = fixture["teams"]["home"]["name"]
        away = fixture["teams"]["away"]["name"]

        if league_id in LEAGUE_IDS and status is not None:
            if 87 <= status <= 90 and fixture_id not in notified_matches:
                message = f"87' Alert: {home} vs {away} ⚽️"
                send_notification(message)
                notified_matches.add(fixture_id)
                print(f"Sent: {message}")

def main():
    print("⏱️ Starting 87th-minute match checker...")
    while True:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking live matches...")
        try:
            check_matches()
        except Exception as e:
            print("Error:", e)
        time.sleep(30)

if __name__ == "__main__":
    main()
