import requests
from dateutil.parser import parse

class GLEIF:

    api_param = 'lei'

    def __init__(self, api_version='v1'):
        GLEIF.api_version = api_version
        GLEIF.api_url = f'https://leilookup.gleif.org/api/{api_version}/leirecords'
        self.lei_list = []

    def request(self, lei_list, return_dataframe=False):
        if isinstance(lei_list, str):
            lei_list = [lei_list]

        output = self.process_request(lei_list)

        if len(lei_list) == 1:
            return_dataframe = False    

            GLEIF.lei = output[0]['LEI']['$']
            GLEIF.legal_name = output[0]['Entity']['LegalName']['$']
            GLEIF.country_legal = output[0]['Entity']['LegalAddress']['Country']['$']
            GLEIF.country_hq = output[0]['Entity']['HeadquartersAddress']['Country']['$']
            GLEIF.status = output[0]['Entity']['EntityStatus']['$']
            GLEIF.date_initial_reg = parse(output[0]['Registration']['InitialRegistrationDate']['$'])
            GLEIF.date_last_updated = parse(output[0]['Registration']['LastUpdateDate']['$'])
            GLEIF.date_next_renewal = parse(output[0]['Registration']['NextRenewalDate']['$'])
            GLEIF.lei_reg_status = output[0]['Registration']['RegistrationStatus']['$']
        else:
            GLEIF.lei = [o['LEI']['$'] for o in output]
            GLEIF.entity_name = [o['Entity']['LegalName']['$'] for o in output]
            GLEIF.country_legal = [o['Entity']['LegalAddress']['Country']['$'] for o in output]
            GLEIF.country_hq = [o['Entity']['HeadquartersAddress']['Country']['$'] for o in output]
            GLEIF.status = [o['Entity']['EntityStatus']['$'] for o in output]
            GLEIF.date_initial_reg = [parse(o['Registration']['InitialRegistrationDate']['$']) for o in output]
            GLEIF.date_last_updated = [parse(o['Registration']['LastUpdateDate']['$']) for o in output]
            GLEIF.date_next_renewal = [parse(o['Registration']['NextRenewalDate']['$']) for o in output]
            GLEIF.lei_reg_status = [o['Registration']['RegistrationStatus']['$'] for o in output]

        if return_dataframe:
            try:
                import pandas as pd

                output_df = pd.DataFrame({
                    'lei': GLEIF.lei,
                    'entity_name': GLEIF.entity_name,
                    'country_legal': GLEIF.country_legal,
                    'country_hq': GLEIF.country_hq,
                    'status': GLEIF.status,
                    'date_initial_reg': GLEIF.date_initial_reg,
                    'date_last_updated': GLEIF.date_last_updated,
                    'date_next_renewal': GLEIF.date_next_renewal,
                    'lei_reg_status': GLEIF.lei_reg_status
                })

                return output, output_df

            except ImportError:
                print('No pandas found, dataframe output disabled.')
            except:
                print('Error creating pandas DataFrame, dataframe output disabled. ')

        return output

    def process_request(self, lei_list):
        chunk_size = 50
        output = []

        for i in range(0, len(lei_list), chunk_size):
            # the API needs comma separated list of LEIs
            leis_to_process = ','.join(lei_list[i:i + chunk_size])

            # make the actual request
            payload = {GLEIF.api_param: leis_to_process}

            try:
                request = requests.get(GLEIF.api_url, params=payload)
                output += request.json()
            except requests.exceptions.ConnectionError:
                # TODO: add better error handling
                print('Error connecting to host!')

        return output
