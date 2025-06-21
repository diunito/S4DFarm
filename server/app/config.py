import os
import json
from datetime import datetime
import requests

CCIT_SERVER="10.10.0.1"

def make_team_dict(file):
    try:
        print("opening {} to get teams json".format(file))
        with open(file, 'r') as f:
            teams = json.load(f)
            return {'{} ({})'.format(team['shortname'], str(team['id'])): os.environ.get('TEAM_FORMAT', '10.60.{}.1').format(str(team['id'])) for team in teams}
    except FileNotFoundError:
        print("using default team scheme")
        return {'Team #{}'.format(i): os.environ.get('TEAM_FORMAT', '10.60.{}.1').format(i)
              for i in range(1, int(os.environ.get('TEAM_NUM', 45)) + 1)}

def get_team_dict_from_id():
    try:
        general_info = requests.get(f"http://{CCIT_SERVER}/api/status", timeout=5).json()
    except Exception as e:
        print(f"Could not fetch general info from {CCIT_SERVER}: {e}")
        exit(1)

    teams = general_info.get("teams", [])
    if not teams:
        print("No teams found")
        exit(1)

    # Costruisci il dizionario: nome_sanitizzato → IP
    team_dict = {
        team["name"].replace('"', '').replace("'", '') : f"10.60.{team['id']}.1"
        for team in teams
    }

    return team_dict

def get_team_dict():
    try:
        general_info = requests.get(f"http://{CCIT_SERVER}/api/status", timeout=5).json()
    except Exception as e:
        print(f"Could not fetch general info from {CCIT_SERVER} {e}")
        exit(1)

    teams = general_info.get("teams", [])
    if not teams:
        print("No teams found")
        exit(1)

    # Costruisci il dizionario name -> host
    team_dict = {team["name"]: team["host"] for team in teams}

    return team_dict

CONFIG = {
    'DEBUG':os.environ.get('DEBUG', 'True'),
    # Don't forget to remove the old database (flags.sqlite) before each competition.

    # The clients will run sploits on TEAMS and
    # fetch FLAG_FORMAT from sploits' stdout.

    #IGNORED_TEAMS = [0]
    #'TEAMS': {  f"{team['shortname']}" : '10.60.{}.1'.format(team["teamId"])
    #                for team in requests.get(url="http://10.10.0.1/api/scoreboard/table/1", timeout=1).json()["scoreboard"]
    #                if not team["teamId"] in IGNORED_TEAMS },
    # curl http://10.10.0.1/api/scoreboard/table/1

    'TEAMS': get_team_dict_from_id(),
    'FLAG_FORMAT': os.environ.get('FLAG_FORMAT', r'[A-Z0-9]{31}='),

    # This configures how and where to submit flags.
    # The protocol must be a module in protocols/ directory.
    # (Default values are there just for reference)

    'SYSTEM_PROTOCOL': os.environ.get('SYSTEM_PROTOCOL', 'ccit_http'),
    # HOST, PORT, TOKEN for tcp
    'SYSTEM_HOST': os.environ.get('SYSTEM_HOST', '10.10.0.10'),
    'SYSTEM_PORT': int(os.environ.get('SYSTEM_PORT', 8080)),
    'TEAM_TOKEN': os.environ.get('TEAM_TOKEN', 'your_secret_token'),
    # URL, TOKEN for http
    'SYSTEM_URL': os.environ.get('SYSTEM_URL', 'http://10.10.0.1:8080/flags'),
    'SYSTEM_TOKEN': os.environ.get('SYSTEM_TOKEN', 'your_secret_token'),
    'HTTP_TIMEOUT': float(os.environ.get('HTTP_TIMEOUT', 30)),
    # usable for both http and tcp (handling http/tcp is in the single scripts)
    'SYSTEM_ID_FLAGS_IP': os.environ.get('SYSTEM_ID_FLAGS_IP', '10.10.0.1'),
    'SYSTEM_ID_FLAGS_PORT': os.environ.get('SYSTEM_ID_FLAGS_PORT', '8081'),

    # 'SYSTEM_PROTOCOL': 'ructf_tcp',
    # 'SYSTEM_HOST': '127.0.0.1',
    # 'SYSTEM_PORT': 31337,

    # 'SYSTEM_PROTOCOL': 'ructf_http',
    # 'SYSTEM_URL': 'http://monitor.ructfe.org/flags',
    # 'SYSTEM_TOKEN': 'your_secret_token',

    # 'SYSTEM_PROTOCOL': 'volgactf',
    # 'SYSTEM_HOST': '127.0.0.1',

    # 'SYSTEM_PROTOCOL': 'forcad_tcp',
    # 'SYSTEM_HOST': '127.0.0.1',
    # 'SYSTEM_PORT': 31337,
    # 'TEAM_TOKEN': 'your_secret_token',

    # 'SYSTEM_PROTOCOL': 'ccit_http',
    # 'SYSTEM_HOST': '127.0.0.1',
    # 'SYSTEM_PORT': 4444,
    # 'SYSTEM_TOKEN': 'CHANGE_ME',
    # 'SYSTEM_URL': 'http://10.10.0.1:8080/flags',

    # The server will submit not more than SUBMIT_FLAG_LIMIT flags
    # every SUBMIT_PERIOD seconds. Flags received more than
    # FLAG_LIFETIME seconds ago will be skipped.
    'SUBMIT_FLAG_LIMIT': int(os.environ.get('SUBMIT_FLAG_LIMIT', 100)),
    'SUBMIT_PERIOD': float(os.environ.get('SUBMIT_PERIOD', 5)),
    'FLAG_LIFETIME': float(os.environ.get('FLAG_LIFETIME', 60)),

    # A/D time informations
    'TICK_DURATION': float(os.environ.get('TICK_DURATION', 120)),
    'START_TIME' : round(datetime.strptime(os.environ.get('START_TIME', '2024-07-03T16:00:00+02:00'), '%Y-%m-%dT%H:%M:%S%z').timestamp()),
    'END_TIME' : round(datetime.strptime(os.environ.get('END_TIME', '2024-07-03T19:02:00+02:00'), '%Y-%m-%dT%H:%M:%S%z').timestamp()),

    # Password for the web interface. You can use it with any login.
    # This value will be excluded from the config before sending it to farm clients.
    'SERVER_PASSWORD': os.environ.get('SERVER_PASSWORD', '1234'),

    # Use authorization for API requests
    'ENABLE_API_AUTH': bool(os.environ.get('ENABLE_API_AUTH', "false").lower() == "true"), # bool() just to be sure
    'API_TOKEN': os.environ.get('API_TOKEN', 'Tok3N'),

    # Custom library folder (for example containing custom python modules)
    # This path will be added by start_sploit.py
    # to $PYTHONPATH (for python scripts)
    # and to $LIBPATH (for bash scripts)
    'LIBPATH': os.environ.get('LIBPATH', ''),
    'TIMEZONE': 'Europe/Rome',
}

