""" Create certificate. """
import argparse
import os
import shutil

from utils.shell import call
from utils.openssl_api import openssl

def create_cert(cfg, domain_name, force=False):
    """ Create a new certificate for domain name. """

    repl = {"t" : cfg.get("CA_TOP"), "d": domain_name}
    repl["cd"] = '%(t)s/certs/%(d)s' % repl

    if os.path.exists(repl["cd"]) and not force:
        print('%s already exists. Exiting.' % domain_name)
        return
    if os.path.exists(repl["cd"]) and force:
        shutil.rmtree(repl["cd"])
    os.mkdir(repl["cd"])

    config_file = cfg.create_config_file(domain_name)
    print(openssl(['req', '-new', '-nodes', '-keyout',
                   '%(cd)s/%(d)s.key' % repl,
                   '-out %(cd)s/%(d)s.req' % repl,
                   '-days %(CRT_DAYS)s' % cfg.map, '-config %s' % config_file.name]))
    print(openssl(['ca', '-batch', '-passin %(CAKEY_PASSPHRASE)s' % cfg.map,
                   '-policy policy_anything',
                   '-notext', '-days %(CRT_DAYS)s' % cfg.map,
                   '-out %(cd)s/%(d)s.crt' % repl,
                   '-infiles %(cd)s/%(d)s.req' % repl]))
    call('cat %(cd)s/%(d)s.key %(cd)s/%(d)s.crt > %(cd)s/%(d)s-fullchain.pem' %
         repl)
    # chmod go= $1.crt $1.key $1.req

    os.unlink(config_file.name)

    return domain_name

def parse_create_cert_args(cfg):
    """ Parse create_cert arguments."""

    parser = argparse.ArgumentParser(
        description='Create a new certificate for domain name.')
    parser.add_argument('create_cert')
    parser.add_argument('domain', help='Certificate domain.')
    parser.add_argument(
        '-f', '--force', help='Force creation by deleting previous certificate of same name.',
        action="store_true")

    args = parser.parse_args()
    create_cert(cfg, args.domain, force=args.force)
