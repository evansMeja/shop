import requests
import json
def generate_acces_token():
    url = 'https://api.lulusms.com/v4/live/Login'
    body = {'UserName':'0740664839','Password':'36973233#Evans'}
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(body), headers=headers)
    return r.json()['Token']