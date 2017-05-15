#!/usr/bin/env python3
"""" Easy CA scripts for local certificate authority. """
import sys
import argparse
import utils.config as config
import commands.create_ca
import commands.create_cert
import commands.check_certs

CFG = config.Config()
CFG.load()

def get_cert_from_dn(domain_name):
    """ Get cert information from domain name. """

    return domain_name


def revoke(domain_name):
    """ Revoke existing certificate. """

    return domain_name


def init_ca():
    """ Create certificate authority. """
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
            commands.check_certs.parse_check_certs_args(CFG)
        elif args.action == 'create_cert':
            commands.create_cert.parse_create_cert_args(CFG)
        elif args.action == 'create_ca':
            commands.create_ca.parse_create_ca_args(CFG)


parse_args()
