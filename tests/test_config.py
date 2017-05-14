""" Basic test suite. """

import context
import config


def test_config_load():
    """ Test config load. """

    cfg = config.load_config('tests/resources/ca.cfg')
    cfg["CA_COUNTRY"] == 'FR'
