import requests
import json

class BrumBrum():
    def __init__(self, API_KEY, API_VERSION = 2):
        self.API_KEY = API_KEY
        self.API_VERSION = API_VERSION
        self.committedMatrices = []

    def get_sync_matrix(self, origins, destinations):
        url = f"https://api.tomtom.com/routing/matrix/{self.API_VERSION}?key={self.API_KEY}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "origins": origins,
            "destinations": destinations,
            "options": {}
        }
        r = requests.post(url, json=payload, headers=headers)

        if r.status_code == 200:
            return r.text
        else:
            return "Erroreeeee"
    
    def async_matrix_submission(self, origins, destinations):
        pass
    
    def get_async_matrix_status(self, jobID):
        pass
    
    def get_async_matrix(self, jobID):
        pass
    
    def geocode(self, address, return_type = "json", full_res = False):
        #to check if "address" is a single string or a list of addresses
        addresses = []
        if isinstance(address, str):
            addresses.append(address)
        else:
            addresses = address

        #coordinates list
        coordinates_list = []
        
        #list with the full responses, returned if full_res = True
        full_res_list = []

        #flag to check if all the addresses have been geocoded
        all_found = True
        for adrs in addresses:
            #split by "," and clean from spaces
            broken_address = [p.strip() for p in adrs.split(",")]
            #substitute divide by %20 to match url format
            adrs_url_format = "%20".join(broken_address)
            url = f"https://api.tomtom.com/search/{self.API_VERSION}/geocode/{adrs_url_format}.{return_type}?key={self.API_KEY}"
            req = requests.get(url)
            body = json.loads(req.text)
            #if something went wrong for the current request, put a None in the coords list
            if req.status_code != 200:
                coordinates_list.append(None)
                all_found = False
            #else look for the coords
            else:
                numResults = body["summary"]["totalResults"]

                #if the result is ambigous, return None in the position of the address
                if numResults != 1:
                  coordinates_list.append(None)
                  all_found = False

                #else return the coords
                else:
                  position = body["results"][0]["position"]
                  latlng = (position["lat"], position["lon"])
                  coordinates_list.append(latlng)
            
            #save the full response only if needed
            if full_res:
                full_res_list.append(body)

        res = {}
        res["all_found"] = all_found
        res["coords"] = coordinates_list
        res["responses"] = full_res_list
        
        return res