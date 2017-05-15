""" File utils. """


def write_to_file(path, text):
    """ Write something to a file and close it. """

    tmp_file = open(path, mode="w")
    tmp_file.write(text)
    tmp_file.close()
