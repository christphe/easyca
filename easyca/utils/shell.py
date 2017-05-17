""" Shell utils. """
import subprocess


def call(cmd, write=None):
    """ Call command and returns stdout as an utf-8 string. """

    print(cmd)

    popen = subprocess.Popen(cmd,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE)
    if write is not None:
        write_bstring = write.encode('utf-8')
    else:
        write_bstring = None
    result = popen.communicate(write_bstring)[0].decode('utf-8')
    return result
