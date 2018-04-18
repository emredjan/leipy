import leipy
import csv

def test_lei_name():

    with open('example_lei.csv', 'r') as f:
        reader = csv.reader(f)
        l_list = [i[0] for i in reader]

    g = leipy.GLEIF(api_version='v1')

    raw_output, results, results_df = g.request(l_list)

    assert isinstance(raw_output, list)
    assert 'KS Projekt GmbH' in [raw_output[i]['Entity']['LegalName']['$'] for i in range(len(raw_output))]
    assert 'Rimatzki Baugeschäft GmbH' in [raw_output[i]['Entity']['LegalName']['$'] for i in range(len(raw_output))]
    assert len(raw_output) <= len(l_list)
    assert len(raw_output[0]) >= 3