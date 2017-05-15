""" Create certificate authority """
import os
import shutil
import argparse
from utils.openssl_api import openssl
from utils.file import write_to_file

def create_ca(cfg, force=False):
    """ Create certificate authority. """

    ca_key = "cakey.pem"
    ca_req = "careq.pem"
    ca_cert = "cacert.pem"
    ca_top = cfg.get("CA_TOP")

    ssleay_config = os.getenv('SSLEAY_CONFIG', '')

    if os.path.exists(ca_top) and not force:
        print('%s already exists. Exiting.' % ca_top)
        return
    if os.path.exists(ca_top) and force:
        shutil.rmtree(ca_top)

    os.makedirs(ca_top)
    os.makedirs("%s/certs" % ca_top)
    os.makedirs("%s/crl" % ca_top)
    os.makedirs("%s/newcerts" % ca_top)
    os.makedirs("%s/private" % ca_top)
    write_to_file("%s/index.txt" % ca_top, "")
    write_to_file("%s/crlnumber" % ca_top, "01")

    config_file = cfg.create_config_file(cfg.get("CA_DOMAIN"))
    print(openssl(["req", ssleay_config,
                   "-new", "-keyout %s/private/%s" % (ca_top, ca_key),
                   "-out %s/%s" % (ca_top, ca_req),
                   "-passout %(CAKEY_PASSPHRASE)s" % cfg.map, '-config %s' % config_file.name]))
    print(openssl(["ca -batch", ssleay_config, "-create_serial",
                   "-passin %(CAKEY_PASSPHRASE)s" % cfg.map,
                   "-out %s/%s" % (ca_top, ca_cert),
                   "-days %(CA_DAYS)s" % cfg.map, "-batch", "-keyfile",
                   "%s/private/%s" % (ca_top, ca_key), "-selfsign", "-extensions v3_ca",
                   "-infiles %s/%s" % (ca_top, ca_req)]))
    return

def parse_create_ca_args(cfg):
    """ Parse create_ca arguments."""

    parser = argparse.ArgumentParser(
        description='Create a new certificate authority.')
    parser.add_argument('create_ca')
    parser.add_argument(
        '-f', '--force', help='Force creation by deleting previous certificate authority folder.',
        action="store_true")

    args = parser.parse_args()
    create_ca(cfg, force=args.force)
    return
