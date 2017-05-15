""" Configuration methods. """
import json
import tempfile


class Config():
    """ Configuration class. """

    def __init__(self):
        self.map = {}

    def load(self, config_file_name='ca.cfg'):
        """ Load config from file. """

        with open(config_file_name) as config_file:
            self.map = json.load(config_file)

    def get(self, key):
        """ Return config value defined by key. """
        return self.map[key]

    def create_config_file(self, domain_name):
        """ Create a configuration file based on the configuration values passed. """

        cfile = tempfile.NamedTemporaryFile(mode='w', delete=False)
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
        cfile.write('default_md             = sha256\n')
        cfile.write('\n')
        cfile.write('[ req_distinguished_name ]\n')
        cfile.write('C                      = %(CA_COUNTRY)s\n' % self.map)
        cfile.write('ST                     = %(CA_STATE)s\n' % self.map)
        cfile.write('L                      = %(CA_LOCALITY)s\n' % self.map)
        cfile.write(
            'O                      = %(CA_ORGANIZATION_NAME)s\n' % self.map)
        cfile.write(
            'OU                     = %(CA_ORGANIZATION_UNIT_NAME)s\n' % self.map)
        cfile.write('CN                     = %s\n' % domain_name)
        cfile.write('emailAddress           = webmaster@%s\n' % domain_name)
        cfile.write('\n')
        cfile.write('[ req_attributes ]\n')
        if self.get("CA_CHALLENGE_PASSWORD") != None and self.get("CA_CHALLENGE_PASSWORD") != '':
            cfile.write(
                'challengePassword              = %(CA_CHALLENGE_PASSWORD)s\n' % self.map)
        cfile.close()
        return cfile
