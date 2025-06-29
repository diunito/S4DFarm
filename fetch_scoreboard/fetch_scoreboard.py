#!/usr/bin/env python3

import requests
import redis
import json

try:
    response = requests.get("http://10.10.0.1/api/scoreboard", timeout=5)
    response.raise_for_status()
    data = response.json()

    r = redis.Redis(host="localhost", port=6379, db=1)
    r.set("scoreboard_data", json.dumps(data))
    print("✅ Scoreboard aggiornata.")
except Exception as e:
    print(f"❌ Errore nel fetch della scoreboard: {e}")
