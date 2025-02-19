import requests
import json
from config import load_config

# Load Config
host_ip, host_port, player_id = load_config()


def get_player_status(cmd):
    try:
        url = f'http://{host_ip}:{host_port}/jsonrpc.js'
        headers = {'Content-Type': 'application/json'}
        data = {"id": 1, "method": "slim.request", "params": [player_id, cmd]}
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        return None, response.json()
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}", None


def extract_result_field(result, field, default="N/A"):
    return result.get('result', {}).get(field, default)

