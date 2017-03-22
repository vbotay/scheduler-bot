from datetime import time


def format_time_input(inp):
    """Check and format input string with time
    to the expected format for scheduler

    :param inp: str with time
    :return:
    """
    if not isinstance(inp, str):
        raise TypeError('Need a string, {} was passed'.format(type(inp)))

    if len(inp) > 5:
        print('Check input')
        return

    delimiters = [' ', ':', '-']
    delimiter = ''

    for d in delimiters:
        if d in inp:
            delimiter = d
            break

    if delimiter:
        res = inp.split(delimiter)
        if len(res[0]) == 1:
            res = ['0' + res[0], res[1]]

    elif len(inp) == 4:
        res = [inp[:2], inp[2:]]

    elif len(inp) == 3:
        res = ['0' + inp[0], inp[1:]]

    elif len(inp) == 2:
        res = [inp, '00']

    elif len(inp) == 1:
        res = ['0' + inp, '00']

    else:
        print('Check input')
        return

    if not all(map(lambda x: x.isdecimal(), res)):
        print('Check input, maybe literal in string')
        return

    if int(res[0]) not in range(0, 24):
        print('Check hours format, it should be between 00 and 24')
        return

    if int(res[1]) not in range(00, 60):
        print('Check minutes format, it should be between 00 and 59')
        return

    return time(int(res[0]), int(res[1]))


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x < end
    else:
        return start <= x or x < end