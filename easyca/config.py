""" Configuration methods. """
import json
import tempfile


def load_config(config_file_name='ca.cfg'):
    """ Load config from file. """

    with open(config_file_name) as config_file:
        return json.load(config_file)
    return


def create_config_file(cfg, domain_name):
    """ Create a configuration file based on the configuration values passed. """

    cfile = tempfile.NamedTemporaryFile(mode='w', delete=False)
    print(cfile.name)
    cfile.write('RANDFILE               = $ENV::HOME/.rnd\n')
    cfile.write('\n')
    cfile.write('[ ca ]\n')
    cfile.write('default_ca = CA_default\n')
    cfile.write('\n')
    cfile.write('[ CA_default ]\n')
    cfile.write('default_bits           = 2048\n')
    cfile.write('distinguished_name     = distinguished_name\n')
    cfile.write('attributes             = attributes\n')
    cfile.write('prompt                 = no\n')
    cfile.write('policy                 = policy_strict\n')
    cfile.write('\n')
    cfile.write('[ policy_strict ]\n')
    cfile.write('countryName             = match\n')
    cfile.write('stateOrProvinceName     = match\n')
    cfile.write('organizationName        = match\n')
    cfile.write('organizationalUnitName  = optional\n')
    cfile.write('commonName              = supplied\n')
    cfile.write('emailAddress            = optional\n')
    cfile.write('\n')
    cfile.write('[ req ]\n')
    cfile.write('default_bits           = 2048\n')
    cfile.write('distinguished_name     = req_distinguished_name\n')
    cfile.write('attributes             = req_attributes\n')
    cfile.write('prompt                 = no\n')
    cfile.write('default_md          = sha256\n')
    cfile.write('\n')
    cfile.write('[ req_distinguished_name ]\n')
    cfile.write('C                      = %s\n' % cfg["CA_COUNTRY"])
    cfile.write('ST                     = %s\n' % cfg["CA_STATE"])
    cfile.write('L                      = %s\n' % cfg["CA_LOCALITY"])
    cfile.write('O                      = %s\n' % cfg["CA_ORGANIZATION_NAME"])
    cfile.write('OU                     = %s\n' % cfg["CA_ORGANIZATION_UNIT_NAME"])
    cfile.write('CN                     = %s\n' % domain_name)
    cfile.write('emailAddress           = webmaster@%s\n' % domain_name)
    cfile.write('\n')
    cfile.write('[ req_attributes ]\n')
    if cfg["CA_CHALLENGE_PASSWORD"] != None and cfg["CA_CHALLENGE_PASSWORD"] != '':
        cfile.write('challengePassword              = %s\n' % cfg["CA_CHALLENGE_PASSWORD"])
    cfile.close()
    return cfile
