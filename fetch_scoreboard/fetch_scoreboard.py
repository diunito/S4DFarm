#!/usr/bin/env python3

import requests
import redis
import json
import sys

def fetch_scoreboard(tick_num=None):
    """
    Fetch della scoreboard dal nuovo endpoint /api/scoreboard/chart/{tick_num}
    e salvataggio in Redis per l'uso da parte del backend S4DFarm.
    """
    try:
        # Se non specificato, prova a ottenere l'ultimo tick disponibile
        if tick_num is None:
            # Prima prova a ottenere il tick corrente da un endpoint generico
            try:
                response = requests.get("http://10.10.0.1/api/status", timeout=5)
                tick_num = response.json().get('currentRound', 1) - 1
            except:
                tick_num = 1  # Fallback al primo tick

        # Fetch della scoreboard
        url = f"http://10.10.0.1/api/scoreboard/table/{tick_num}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Verifica che abbia la struttura attesa
        if 'scoreboard' not in data:
            raise ValueError("Formato scoreboard non valido: manca 'scoreboard'")

        # Trasforma i dati nel formato atteso dal backend
        transformed_data = {
            'teams': []
        }

        # Ordina i team per posizione nella scoreboard
        scoreboard = data['scoreboard']
        for team_data in scoreboard:
            # Salta team NOP e guest
            if team_data.get('nop', False) or team_data.get('guest', False):
                continue
                
            transformed_data['teams'].append({
                'name': team_data['shortname'],
                'score': team_data['score'],
                'position': team_data['position']
            })

        print(f"✅ Scoreboard aggiornata (tick {tick_num}, {len(transformed_data['teams'])} team)")
        # Salva in Redis
        r = redis.Redis(host="localhost", port=6379, db=1)
        r.set("scoreboard_data", json.dumps(transformed_data))
        
        return True

    except requests.exceptions.RequestException as e:
        print(f"❌ Errore di rete nel fetch della scoreboard: {e}")
        return False
    except ValueError as e:
        print(f"❌ Errore nel formato della scoreboard: {e}")
        return False
    except Exception as e:
        print(f"❌ Errore generico nel fetch della scoreboard: {e}")
        return False

if __name__ == "__main__":
    tick_num = None
    if len(sys.argv) > 1:
        try:
            tick_num = int(sys.argv[1])
        except ValueError:
            if sys.argv[1] == "current":
                tick_num = "current"
            else:
                print("❌ Numero tick non valido")
                sys.exit(1)
    
    success = fetch_scoreboard(tick_num)
    sys.exit(0 if success else 1)
