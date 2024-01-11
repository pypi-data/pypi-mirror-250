import requests
import json
import configparser
import pkg_resources
import os

config = configparser.ConfigParser()
config.read_string(pkg_resources.resource_string(__name__, 'config/config.ini').decode())
api_link = os.environ.get('API_LINK', config.get('API', 'API_LINK'))
def main(UID, REGION):
    API_URL = f'{api_link}?id={UID}&region={REGION}'
    print(API_URL)
    RESPONSE = requests.get(API_URL)
    API_DATA = json.loads(RESPONSE.text)
    print(API_DATA)
    
    
    
if __name__ == "__main__":
    main()
    
