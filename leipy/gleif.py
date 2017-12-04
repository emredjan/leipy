import requests

class GLEIF:

    api_version = 'v1'
    api_url = f'https://leilookup.gleif.org/api/{api_version}/leirecords'
    api_param = 'lei'

    def __init__(self, lei_list):
        self.lei_list = lei_list

    def process_leis(self):
        chunk_size = 50
        output = []
        
        for i in range(0, len(self.lei_list), chunk_size):
            # the API needs comma separated list of LEIs
            leis_to_process = ','.join(self.lei_list[i:i+chunk_size])

            # make the actual request
            payload = {GLEIF.api_param: leis_to_process}
            request = requests.get(GLEIF.api_url, params=payload)

            output += request.json()
        
        return output