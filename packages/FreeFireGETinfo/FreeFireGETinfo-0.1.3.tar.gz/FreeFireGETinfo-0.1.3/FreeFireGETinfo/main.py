import requests
import json
import os

def main(UID, REGION):
    API_URL = f'http://freefireapi.com.br/api/search_id?id={UID}&region={REGION}'
    RESPONSE = requests.get(API_URL)
    API_DATA = json.loads(RESPONSE.text)
    print(API_DATA)
