import requests # for API request
import pandas as pd # for csv reading and excel output
from datetime import date, timedelta


# find the reporting date
yesterday = date.today() - timedelta(1)
yesterday = yesterday.strftime('%Y%m%d')


# declare filenames
filename_gbi_lei = f'reports/00_gbi_lei_data.csv'
filename_xlsx_output = f'reports/LEI_Status_{yesterday}.xlsx'


# gbi customer list
try:
    gbi_lei = pd.read_csv(filename_gbi_lei)
except:
    print('\nInvalid File (GBI_LEI)!\n')
    quit()

# ignore closed customers    
gbi_lei = gbi_lei[gbi_lei.ACCOUNT_OFFICER != 9999].reset_index(drop=True)


print('\nQuerying GLEIF database..')


# setup for API request
gleif_api_version = 'v1'
gleif_api_url = f'https://leilookup.gleif.org/api/{gleif_api_version}/leirecords'
gleif_api_param = 'lei'
gleif_list = []
gbi_unique_lei = gbi_lei.GBI_CUS_LEI.unique()

# GLEIF API has request limit of 200, process in chunks of 50 to be safe
chunk_size = 50
for i in range(0, len(gbi_unique_lei), chunk_size):
    # the API needs comma separated list of LEIs
    lei_list = ','.join(gbi_unique_lei[i:i+chunk_size])
    
    # make the actual request
    payload = {gleif_api_param: lei_list}
    r = requests.get(gleif_api_url, params=payload)
    
    if r.status_code != requests.codes.ok:
        print(r.status_code + '\nInvalid request!')
        quit()
    
    output = r.json()
    # append the related data from the output
    gleif_list += [{'LEI': o['LEI']['$'],
                    'InitialRegistrationDate': o['Registration']['InitialRegistrationDate']['$'][:10],
                    'LastUpdateDate': o['Registration']['LastUpdateDate']['$'][:10],
                    'NextRenewalDate': o['Registration']['NextRenewalDate']['$'][:10],
                    'RegistrationStatus': o['Registration']['RegistrationStatus']['$'],
                   } for o in output]

# create dataframe from the API output
gleif_lei = pd.DataFrame(gleif_list, columns=['LEI',
                                              'InitialRegistrationDate',
                                              'LastUpdateDate',                       
                                              'NextRenewalDate',
                                              'RegistrationStatus'])

print('\nChecking against GBI LEI list..')
    
# left join GBI list with GLEIF list, 
df = gbi_lei.merge(gleif_lei, how='left', left_on='GBI_CUS_LEI', right_on='LEI')


# convert date fields to proper 'datetime64[ns]' format
from functools import partial
# get rid of repetitive parameters in to_datetime function with a partial
to_ymd = partial(pd.to_datetime, format='%Y-%m-%d', errors='ignore')

df['InitialRegistrationDate'] = to_ymd(df['InitialRegistrationDate'])
df['LastUpdateDate'] = to_ymd(df['LastUpdateDate'])
df['NextRenewalDate'] = to_ymd(df['NextRenewalDate'])

lei_validity = {'ANNULLED': 'Invalid!',
                'DUPLICATE': 'Invalid!',
                'ISSUED': 'Valid',
                'LAPSED': 'Valid',
                'MERGED': 'Invalid!',
                'PENDING_AR': 'Valid',
                'PENDING_TR': 'Valid',
                'RETIRED': 'Invalid!'}

df['LEIValid'] = df['RegistrationStatus'].map(lei_validity)
                                               
df = df[['GBI_CUS_LEI', 'LEIValid', 'CUSTOMER_LIABILITY', 'CUSTOMER_CODE', 'NAME_1', 
         'ACCOUNT_OFFICER', 'LEI', 'InitialRegistrationDate', 'LastUpdateDate', 
         'NextRenewalDate', 'RegistrationStatus']]
                                               
print('\nWriting xlsx...')

# xlsxwriter object for correct date formatting
writer = pd.ExcelWriter(filename_xlsx_output,
                        engine='xlsxwriter',
                        datetime_format='dd/mm/yyyy',
                        date_format='dd/mm/yyyy')

# write to excel with proper formatting
df.to_excel(writer, 
            sheet_name='LEI Status', 
            index=False,
            freeze_panes=(1, 0))

print('\nDone.')
