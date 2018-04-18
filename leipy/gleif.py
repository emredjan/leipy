"""
Wrapper for GLEIF public API to get LEI details.
Includes definitions for main GLEIF class as well as the LEI_Output helper.
Used by instantiating a GLEIF class and running its 'request' method.
"""

import requests
from dateutil.parser import parse

class GLEIF:
    """
    Main wrapper class for GLEIF public API
    Different list of LEIs can be processed by different instances
    """
    def __init__(self, api_version='v1'):
        """
        Initialize the API URL by the api version.

        Parameters
        ----------

        api_version: str
            Set the requested api version.
            Only the default 'v1' is valid for now.
        """

        self._api_url = 'https://leilookup.gleif.org/api/{0}/leirecords'.format(api_version)

    def request(self, lei_list, return_dataframe=False):
        """
        Handle the API results and return the requested output.

        Parameters
        ----------

        lei_list: str or list-like
            LEIs to be processed. Accepts single LEI as str or list of LEIs

        return_dataframe: bool
            Whether to return the results optionally as a pandas DataFrame in
            addition to the raw output and results class. Always false if a 
            single LEI is entered.

        Returns
        -------
        output: list of dicts, raw output json from API
        lei_result: results as class, 
        output_df: (optional) pandas DataFrame of results
        """

        if isinstance(lei_list, str):
            if len(lei_list) != 20:
                print('Invalid LEI entered. See documentation')
                return None, None, None
            lei_list = [lei_list]

        output = self._process_request(lei_list)

        lei_result = LEI_Output(output)

        if len(lei_list) == 1:
            return_dataframe = False 

        if return_dataframe:
            try:
                import pandas as pd

                output_df = pd.DataFrame({
                    'lei': lei_result.lei,
                    'legal_name': lei_result.legal_name,
                    'country_legal': lei_result.country_legal,
                    'country_hq': lei_result.country_hq,
                    'status': lei_result.status,
                    'date_initial_reg': lei_result.date_initial_reg,
                    'date_last_updated': lei_result.date_last_updated,
                    'date_next_renewal': lei_result.date_next_renewal,
                    'lei_reg_status': lei_result.lei_reg_status
                })

                return output, lei_result, output_df

            except ImportError:
                print('No pandas found, dataframe output disabled.')
            except:
                print('Error creating pandas DataFrame, dataframe output disabled.')

        return output, lei_result, None

    def _process_request(self, lei_list):
        """
        Process the API request and return the raw output.

        Parameters
        ----------

        lei_list: list-like
            LEIs to be processed. Accepts list of LEIs

        Returns
        -------
        output: list of dicts, raw output json from API
        """

        api_param = 'lei'
        chunk_size = 50
        output = []

        for i in range(0, len(lei_list), chunk_size):
            # the API needs comma separated list of LEIs
            leis_to_process = ','.join(lei_list[i:i + chunk_size])

            # make the actual request
            payload = {api_param: leis_to_process}

            try:
                request = requests.get(self._api_url, params=payload)
                output += request.json()
            except requests.exceptions.ConnectionError:
                # TODO: add better error handling
                print('Error connecting to host!')

        return output

class LEI_Output:
    """
    Helper class for results. Common LEI fields can be accessed as instance members
    after request has been made.
    """

    def __init__(self, output):
        """
        Take the raw output from API and assign commonly used fields to instance variables.

        Parameters
        ----------

        output: list of dicts, raw output from API
        """

        if len(output) == 1:
            self.lei = output[0].get('LEI').get('$')
            self.legal_name = output[0].get('Entity').get('LegalName').get('$')
            self.country_legal = output[0].get('Entity').get('LegalAddress').get('Country').get('$')
            self.country_hq = output[0].get('Entity').get('HeadquartersAddress').get('Country').get('$')
            self.status = output[0].get('Entity').get('EntityStatus').get('$')
            self.date_initial_reg = parse(output[0].get('Registration').get('InitialRegistrationDate').get('$'))
            self.date_last_updated = parse(output[0].get('Registration').get('LastUpdateDate').get('$'))
            self.date_next_renewal = parse(output[0].get('Registration').get('NextRenewalDate').get('$'))
            self.lei_reg_status = output[0].get('Registration').get('RegistrationStatus').get('$')

        else:
            self.lei = [o.get('LEI').get('$') for o in output]
            self.legal_name = [o.get('Entity').get('LegalName').get('$') for o in output]
            self.country_legal = [o.get('Entity').get('LegalAddress').get('Country').get('$') for o in output]
            self.country_hq = [o.get('Entity').get('HeadquartersAddress').get('Country').get('$') for o in output]
            self.status = [o.get('Entity').get('EntityStatus').get('$') for o in output]
            self.date_initial_reg = [parse(o.get('Registration').get('InitialRegistrationDate').get('$')) for o in output]
            self.date_last_updated = [parse(o.get('Registration').get('LastUpdateDate').get('$')) for o in output]
            self.date_next_renewal = [parse(o.get('Registration').get('NextRenewalDate').get('$')) for o in output]
            self.lei_reg_status = [o.get('Registration').get('RegistrationStatus').get('$') for o in output]
