""" Shell utils. """
import subprocess


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
