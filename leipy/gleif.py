import requests

class GLEIF:

    gleif_api_version = 'v1'
    gleif_api_url = f'https://leilookup.gleif.org/api/{gleif_api_version}/leirecords'
    gleif_api_param = 'lei'

    def __init__(self, lei_list):
        self.lei_list = lei_list

    def process_leis(self):
        chunk_size = 50
        for i in range(0, len(self.lei_list), chunk_size):
            # the API needs comma separated list of LEIs
            leis_to_process = ','.join(self.lei_list[i:i+chunk_size])

            # make the actual request
            payload = {GLEIF.gleif_api_param: leis_to_process}
            request = requests.get(GLEIF.gleif_api_url, params=payload)

            return request.json()
