""" Date utility methods. """

from utils.shell import call

def format_date(date):
    """ Formats date to iso-8601 using the date unix command. """

    return call("date --date='%s' --iso-8601" % date).rstrip()
