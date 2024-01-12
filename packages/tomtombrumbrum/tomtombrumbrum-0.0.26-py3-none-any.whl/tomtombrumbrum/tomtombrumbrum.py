import requests
import json

class BrumBrum():
    def __init__(self, API_KEY):
        self.API_KEY = API_KEY
        self.committedMatrices = []

    def get_sync_matrix(self, origins, destinations):
        pass
    
    def async_matrix_submission(self, origins, destinations):
        pass
    
    def get_async_matrix_status(self, jobID):
        pass
    
    def get_async_matrix(self, jobID):
        pass

api_key = ''


async_matrix_submission = f'https://api.tomtom.com/routing/matrix/2/async?key={api_key}'
async_matrix_status = 'https://api.tomtom.com/routing/matrix/2/async/{id}?key={api_key}'
async_matrix_download = 'https://api.tomtom.com/routing/matrix/2/async/{id}result?key={api_key}'

sync_matrix_sub = f'https://api.tomtom.com/routing/matrix/2?key={api_key}'


headers = {'Content-Type': 'application/json'}
payload = {
  "origins": [
    {
      "point": { "latitude": 46.43088, "longitude": 12.37725 }
    }
  ],
  "destinations": [
    {
      "point": { "latitude": 46.45337034530504, "longitude": 12.391396748057382 }
    }
  ],
  "options": {
      "travelMode": "pedestrian"
    }
}

res = requests.post(sync_matrix_sub, json=payload, headers=headers)
print(res.text)