from leipy import GLEIF

def test_lei_name():
    g = GLEIF(['261700K5E45DJCF5Z735'])

    output = g.process_leis()

    assert output[0]['Entity']['LegalName']['$'] == 'APIR SYSTEMS LIMITED'