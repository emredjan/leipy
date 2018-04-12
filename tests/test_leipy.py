import leipy
import csv

def test_lei_name():

    with open('example_lei.csv', 'r') as f:
        reader = csv.reader(f)
        l_list = [i[0] for i in reader]

    g = leipy.GLEIF(api_version='v1')

    output = g.request(l_list)

    assert isinstance(output, list)
    assert 'KS Projekt GmbH' in [output[i]['Entity']['LegalName']['$'] for i in range(len(output))]
    assert 'Rimatzki Baugeschäft GmbH' in [output[i]['Entity']['LegalName']['$'] for i in range(len(output))]
    assert len(output) <= len(l_list)
    assert len(output[0]) >= 3