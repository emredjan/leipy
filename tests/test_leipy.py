from leipy import GLEIF

import csv
with open('example_lei.csv', 'r') as f:
    reader = csv.reader(f)
    l_list = [i[0] for i in reader]

def test_lei_name():
    g = GLEIF(l_list)

    output = g.process_leis()

    assert isinstance(output, list)
    assert 'KS Projekt GmbH' in [output[i]['Entity']['LegalName']['$'] for i in range(len(output))]
    assert 'Rimatzki Baugeschäft GmbH' in [output[i]['Entity']['LegalName']['$'] for i in range(len(output))]
    assert len(output) == len(g.lei_list)
    assert len(output[0]) >= 3