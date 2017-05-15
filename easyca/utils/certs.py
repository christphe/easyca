""" Certificates utility methods. """

import re
from utils.openssl_api import openssl
from utils.date import format_date

def get_cert_from_file(cert_file):
    """ Return certificate information from cert_file. """

    raw_subject = openssl(["x509", "-subject", "-noout", "-in %s" % cert_file])
    raw_date = openssl(["x509", "-enddate", "-noout", "-in %s" % cert_file])

    date = format_date(re.search('^.*=(.*)', raw_date).group(1))

    domain_name = re.search('CN=(.*)/', raw_subject).group(1)

    return {
        "domain_name": domain_name,
        "date": date
    }
    