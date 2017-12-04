import requests

class GLEIF:

    api_param = 'lei'

    def __init__(self, api_version='v1'):
        GLEIF.api_version = api_version
        GLEIF.api_url = f'https://leilookup.gleif.org/api/{api_version}/leirecords'
        self.lei_list = []

    def request(self, lei_list):
        return self.process_leis(lei_list)

    def process_leis(self, lei_list):
        chunk_size = 50
        output = []

        for i in range(0, len(lei_list), chunk_size):
            # the API needs comma separated list of LEIs
            leis_to_process = ','.join(lei_list[i:i+chunk_size])

            # make the actual request
            payload = {GLEIF.api_param: leis_to_process}
            request = requests.get(GLEIF.api_url, params=payload)

            output += request.json()

        return output
