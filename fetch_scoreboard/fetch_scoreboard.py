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
                tick_num = response.json().get('currentRound', 1)
            except:
                tick_num = 1  # Fallback al primo tick

        # Fetch della scoreboard
        url = f"http://10.10.0.1/api/scoreboard/chart/{tick_num}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Verifica che abbia la struttura attesa
        if 'teams' not in data or 'rounds' not in data:
            raise ValueError("Formato scoreboard non valido: mancano 'teams' o 'rounds'")

        # Trasforma i dati nel formato atteso dal backend
        transformed_data = {
            'teams': [],
            'rounds': data['rounds']
        }

        # Ordina i team per punteggio dell'ultimo round disponibile
        teams_with_scores = []
        for team in data['teams']:
            if team.get('nop', False) or team.get('guest', False):
                continue  # Salta team NOP e guest
            
            scores = team.get('score', [])
            last_score = scores[-1] if scores else 0
            teams_with_scores.append({
                'name': team['shortname'],
                'score': last_score,
                'scores': scores
            })

        # Ordina per punteggio decrescente
        teams_with_scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Aggiungi i team ordinati ai dati trasformati
        for team in teams_with_scores:
            transformed_data['teams'].append({
                'name': team['name'],
                'score': team['score'],
                'scores': team['scores']
            })

        # Salva in Redis
        r = redis.Redis(host="localhost", port=6379, db=1)
        r.set("scoreboard_data", json.dumps(transformed_data))
        
        print(f"✅ Scoreboard aggiornata (tick {tick_num}, {len(transformed_data['teams'])} team)")
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
