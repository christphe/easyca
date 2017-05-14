#!/usr/bin/env python3
"""" Easy CA scripts for local certificate authority. """
import sys
import subprocess
import re
import os
import glob
import shutil
import argparse
import config

CONFIG = config.load_config()
CA_TOP = "./demoCA"


def call(cmd, write=None):
    """ Call command and returns stdout as an utf-8 string. """

    popen = subprocess.Popen(cmd,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE)
    result = popen.stdout.read().decode("utf-8")
    if write != None:
        popen.stdin.write(write.encode('utf-8'))
    return result


def openssl(args, write=None):
    """ Call openssl with given arguments."""
    print("openssl " + ' '.join(args))
    return call("openssl " + ' '.join(args), write)


def get_cert_from_dn(domain_name):
    """ Get cert information from domain name. """

    return domain_name


def format_date(date):
    """ Formats date to iso-8601 using the date unix command. """

    return call("date --date='%s' --iso-8601" % date).rstrip()


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


def revoke(domain_name):
    """ Revoke existing certificate. """

    return domain_name


def init_ca():
    """ Create certificate authority. """
    return


def create_cert(domain_name, force=False):
    """ Create a new certificate for domain name. """

    repl = {"t" : CA_TOP, "d": domain_name}
    repl["cd"] = '%(t)s/certs/%(d)s' % repl

    if os.path.exists(repl["cd"]) and not force:
        print('%s already exists. Exiting.' % domain_name)
        return
    if os.path.exists(repl["cd"]) and force:
        shutil.rmtree(repl["cd"])
    os.mkdir(repl["cd"])

    config_file = config.create_config_file(CONFIG, domain_name)
    print(openssl(['req', '-new', '-nodes', '-keyout',
                   '%(cd)s/%(d)s.key' % repl,
                   '-out %(cd)s/%(d)s.req' % repl,
                   '-days %(CRT_DAYS)s' % CONFIG, '-config %s' % config_file.name]))
    print(openssl(['ca', '-batch', '-passin %(CAKEY_PASSPHRASE)s' % CONFIG,
                   '-policy policy_anything',
                   '-notext', '-days %(CRT_DAYS)s' % CONFIG,
                   '-out %(cd)s/%(d)s.crt' % repl,
                   '-infiles %(cd)s/%(d)s.req' % repl]))
    call('cat %(cd)s/%(d)s.key %(cd)s/%(d)s.crt > %(cd)s/%(d)s-fullchain.pem' %
         repl)
    # chmod go= $1.crt $1.key $1.req

    os.unlink(config_file.name)

    return domain_name


def write_to_file(path, text):
    """ Write something to a file and close it. """

    tmp_file = open(path, mode="w")
    tmp_file.write(text)
    tmp_file.close()


def create_ca(force=False):
    """ Create certificate authority. """

    ca_key = "cakey.pem"
    ca_req = "careq.pem"
    ca_cert = "cacert.pem"

    ssleay_config = os.getenv('SSLEAY_CONFIG', '')

    if os.path.exists(CA_TOP) and not force:
        print('%s already exists. Exiting.' % CA_TOP)
        return
    if os.path.exists(CA_TOP) and force:
        shutil.rmtree(CA_TOP)

    os.makedirs(CA_TOP)
    os.makedirs("%s/certs" % CA_TOP)
    os.makedirs("%s/crl" % CA_TOP)
    os.makedirs("%s/newcerts" % CA_TOP)
    os.makedirs("%s/private" % CA_TOP)
    write_to_file("%s/index.txt" % CA_TOP, "")
    write_to_file("%s/crlnumber" % CA_TOP, "01")

    config_file = config.create_config_file(CONFIG, CONFIG["CA_DOMAIN"])
    print(openssl(["req", ssleay_config,
                   "-new", "-keyout %s/private/%s" % (CA_TOP, ca_key),
                   "-out %s/%s" % (CA_TOP, ca_req),
                   "-passout %(CAKEY_PASSPHRASE)s" % CONFIG, '-config %s' % config_file.name]))
    print(openssl(["ca -batch", ssleay_config, "-create_serial",
                   "-passin %(CAKEY_PASSPHRASE)s" % CONFIG,
                   "-out %s/%s" % (CA_TOP, ca_cert),
                   "-days %(CA_DAYS)s" % CONFIG, "-batch", "-keyfile",
                   "%s/private/%s" % (CA_TOP, ca_key), "-selfsign", "-extensions v3_ca",
                   "-infiles %s/%s" % (CA_TOP, ca_req)]))

    return


def check_certs(path):
    """ Check certificates in given path. """

    cert_list = []
    for pem in glob.glob(path + '/*.pem'):
        cert_list.append(get_cert_from_file(pem))
    return cert_list


def parse_check_certs_args():
    """ Parse check_certs arguments."""

    parser = argparse.ArgumentParser(
        description='Check certificates in given path.')
    parser.add_argument('check_certs')
    parser.add_argument('path', help='Path where certs are stored.')
    args = parser.parse_args()
    print(check_certs(args.path))


def parse_create_cert_args():
    """ Parse create_cert arguments."""

    parser = argparse.ArgumentParser(
        description='Create a new certificate for domain name.')
    parser.add_argument('create_cert')
    parser.add_argument('domain', help='Certificate domain.')
    parser.add_argument(
        '-f', '--force', help='Force creation by deleting previous certificate of same name.',
        action="store_true")

    args = parser.parse_args()
    create_cert(args.domain, force=args.force)


def parse_create_ca_args():
    """ Parse create_ca arguments."""

    parser = argparse.ArgumentParser(
        description='Create a new certificate authority.')
    parser.add_argument('create_ca')
    parser.add_argument(
        '-f', '--force', help='Force creation by deleting previous certificate authority folder.',
        action="store_true")

    args = parser.parse_args()
    create_ca(force=args.force)
    return


def parse_args():
    """ Parse program arguments. """

    help_message = '%s [-h] action\n' % sys.argv[0] + \
        '\n' + \
        'Easy CA scripts for local certificate authority.\n' + \
        '\n' + \
        'action:\n' + \
        '  check_certs:      Check certificates in given path.\n' + \
        '  create_cert:      Create a new certificate for domain name.\n' + \
        '  create_ca:        Create a new certificate authority.\n' + \
        '\n' + \
        'optional arguments:\n' + \
        '  -h, --help  show this help message and exit\n' \

    parser = argparse.ArgumentParser(
        add_help=False,
        description='Easy CA scripts for local certificate authority.',
        usage=help_message)
    parser.add_argument('-h', '--help', action="store_true")
    parser.add_argument('action', help='Action.', choices=[
        'check_certs',
        'create_cert',
        'create_ca'
    ])

    (args, _) = parser.parse_known_args()
    if not args.action and args.help:
        parser.print_usage()
        return

    if args.action is not None:
        if args.action == 'check_certs':
            parse_check_certs_args()
        elif args.action == 'create_cert':
            parse_create_cert_args()
        elif args.action == 'create_ca':
            parse_create_ca_args()


parse_args()
