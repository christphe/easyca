""" OpenSSL client api """

from utils.shell import call

def openssl(args, write=None):
    """ Call openssl with given arguments."""

    return call("openssl " + ' '.join(args), write)
