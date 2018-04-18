# LEIPY

A python wrapper / client for GLEIF public API. Suggestions, requests, contributions welcome.

(I started this as a hobby / learning project, so it's rough around the edges. If you are looking for a better solution, check out [pygleif](https://github.com/ggravlingen/pygleif))

## Dependencies

1. Python >= 3.4
2. [requests](http://docs.python-requests.org/en/master/): For API requests
3. [dateutil](https://dateutil.readthedocs.io/en/stable/): For correctly parsing dates as datetime objects
4. [pandas](https://pandas.pydata.org/): Optional, for returning output as DataFrame 

## Usage

Import, instantiate and make the request:

```python
from leipy import GLEIF

gleif = GLEIF(api_version='v1')

raw_output, results, results_df = gleif.request(
    ['HWUPKR0MPOU8FGXBT394','7ZW8QJWVPR4P1J1KQY45'], 
    return_dataframe=True
)
```

After that, you can access the raw output from the API, results as a class with easy to access instance members, and results as a pandas DataFrame

#### Raw output example

```python
[{'LEI': {'$': 'HWUPKR0MPOU8FGXBT394'},
  'Entity': {'LegalName': {'$': 'Apple Inc.'},
   'LegalAddress': {'Line1': {'$': 'C/O C T Corporation System'},
    'Line2': {'$': '818 West 7th Street'},
    'Line3': {'$': 'Suite 930'},
    'City': {'$': 'Los Angeles'},
    'Region': {'$': 'US-CA'},
    'Country': {'$': 'US'},
    'PostalCode': {'$': '90017'}},
   'HeadquartersAddress': {'Line1': {'$': '1 Infinite Loop'},
    'City': {'$': 'Cupertino'},
    'Region': {'$': 'US-CA'},
    'Country': {'$': 'US'},
    'PostalCode': {'$': '95014'}},
   'BusinessRegisterEntityID': {'@register': 'RA000598', '$': 'C0806592'},
   'LegalJurisdiction': {'$': 'US'},
   'LegalForm': {'$': 'INCORPORATED'},
   'EntityStatus': {'$': 'ACTIVE'}},
  'Registration': {'InitialRegistrationDate': {'$': '2012-06-06T15:53:00.000Z'},
   'LastUpdateDate': {'$': '2017-12-12T21:19:00.000Z'},
   'RegistrationStatus': {'$': 'ISSUED'},
   'NextRenewalDate': {'$': '2018-12-13T00:31:00.000Z'},
   'ManagingLOU': {'$': 'EVK05KS7XY1DEII3R011'},
   'ValidationSources': {'$': 'FULLY_CORROBORATED'}}},
 {'LEI': {'$': '7ZW8QJWVPR4P1J1KQY45'},
  'Entity': {'LegalName': {'$': 'Google LLC'},
   'LegalAddress': {'Line1': {'$': 'C/O Corporation Service Company'},
    'Line2': {'$': '251 Little Falls Drive'},
    'City': {'$': 'Wilmington'},
    'Region': {'$': 'US-DE'},
    'Country': {'$': 'US'},
    'PostalCode': {'$': '19808'}},
   'HeadquartersAddress': {'Line1': {'$': '1600 Amphitheatre Parkway'},
    'City': {'$': 'Mountain View'},
    'Region': {'$': 'US-CA'},
    'Country': {'$': 'US'},
    'PostalCode': {'$': '94043'}},
   'BusinessRegisterEntityID': {'@register': 'RA000602', '$': '3582691'},
   'LegalJurisdiction': {'$': 'US'},
   'LegalForm': {'$': 'LIMITED LIABILITY COMPANY'},
   'EntityStatus': {'$': 'ACTIVE'}},
  'Registration': {'InitialRegistrationDate': {'$': '2012-06-06T15:52:00.000Z'},
   'LastUpdateDate': {'$': '2018-03-28T17:00:00.000Z'},
   'RegistrationStatus': {'$': 'ISSUED'},
   'NextRenewalDate': {'$': '2018-08-17T18:10:00.000Z'},
   'ManagingLOU': {'$': 'EVK05KS7XY1DEII3R011'},
   'ValidationSources': {'$': 'FULLY_CORROBORATED'}}}]
```

#### Results class example

```python
>>> print(results.legal_name)
['Apple Inc.', 'Google LLC']

>>> print(results.lei_reg_status)
['ISSUED', 'ISSUED']

>>> print(results.date_last_updated)
[datetime.datetime(2017, 12, 12, 21, 19, tzinfo=tzutc()),
 datetime.datetime(2018, 3, 28, 17, 0, tzinfo=tzutc())]
```

#### Results DataFrame example

```python
>>>results_df
```

| |country_hq|country_legal|date_initial_reg|date_last_updated|date_next_renewal|legal_name|lei|lei_reg_status|status|
|-|----------|-------------|----------------|-----------------|-----------------|----------|---|--------------|------|
|0	|US	|US	|2012-06-06 15:53:00+00:00	|2017-12-12 21:19:00+00:00	|2018-12-13 00:31:00+00:00	|Apple Inc.	|HWUPKR0MPOU8FGXBT394	|ISSUED	|ACTIVE|
|1	|US	|US	|2012-06-06 15:52:00+00:00	|2018-03-28 17:00:00+00:00	|2018-08-17 18:10:00+00:00	|Google LLC	|7ZW8QJWVPR4P1J1KQY45	|ISSUED	|ACTIVE|