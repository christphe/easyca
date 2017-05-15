""" Check certificates validity. """
import glob
import argparse

import utils.certs

def check_certs(_, path):
    """ Check certificates in given path. """

    cert_list = []
    for pem in glob.glob(path + '/*.pem'):
        cert_list.append(utils.certs.get_cert_from_file(pem))
    return cert_list


def parse_check_certs_args(cfg):
    """ Parse check_certs arguments."""

    parser = argparse.ArgumentParser(
        description='Check certificates in given path.')
    parser.add_argument('check_certs')
    parser.add_argument('path', help='Path where certs are stored.')
    args = parser.parse_args()
    print(check_certs(cfg, args.path))
