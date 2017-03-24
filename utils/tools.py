from datetime import time


class TimeFormatError(Exception):
    pass


class TimingError(Exception):
    pass

class DeletionError(Exception):
    pass


class MembersError(Exception):
    pass


def get_user_info(message):
    """Return info about Telegram user

    :param message: message from telebot api
    :return: message instance {'username': u'username', 'first_name': u'Ivan',
    'last_name': u'Ivanov', 'id': XXXXXXXXXX}
    """
    return message.from_user


def get_username(message):
    return '@' + get_user_info(message).username


def get_command_params(msg):
    return ' '.join(msg.text.split(' ')[1:])


def format_time_input(inp):
    """Check and format input string with time
    to the expected format for scheduler

    :param inp: str with time
    :return:
    """
    if not isinstance(inp, str):
        raise TypeError('Need a string, {} was passed'.format(type(inp)))

    if len(inp) > 5:
        raise TimeFormatError('Check input')

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
        raise TimeFormatError('Check input')

    if not all(map(lambda x: x.isdigit(), res)):
        raise TimeFormatError('Check input maybe literal in string')

    if int(res[0]) not in range(0, 24) or int(res[1]) not in range(00, 60):
        raise TimeFormatError('Minutes should be betwee 0 and 59.\n'
                              'Hours between 0 and 23')

    return time(int(res[0]), int(res[1]))


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start < x < end
    else:
        return start < x or x < end
