from datetime import date
from datetime import datetime
from datetime import timedelta

import six

import config
from utils.tools import DeletionError
from utils.tools import MembersError
from utils.tools import TimingError
from utils.tools import format_time_input


class SingletonMeta(type):
    """Metaclass for Singleton
    Main goals: not need to implement __new__ in singleton classes
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Scheduler(six.with_metaclass(SingletonMeta, object)):

    def __init__(self, schedule=None):
        self.schedule = schedule if schedule else {}
        self.playday = date.today()
        self.reserved_time = []
        self.play_time = timedelta(minutes=config.DEFAULT_DURATION)
        self.fmt = '%H:%M'

    def __len__(self):
        return len(self.schedule)

    def __clear_scheduler(self):
        self.schedule = {}
        self.reserved_time = []

    def __check_intervals(self, ptime):
        for start_time, end_time in self.reserved_time:
            if start_time <= ptime < end_time:
                return False
            ptime_end = datetime.combine(date.today(), ptime) + self.play_time
            ptime_end = ptime_end.time()
            if start_time < ptime_end < end_time:
                return False
        return True

    def add_to_schedule(self, input_time, participant):
        ptime = format_time_input(input_time)

        self.check_member(ptime, participant)
        self.check_time(ptime)

        self.schedule[ptime].append(participant)
        self.reserve_time(ptime)
        msg = "{} were added to game {}".format(participant,
                                                ptime.strftime(self.fmt))
        if len(self.schedule[ptime]) == config.MEMBERS_MAX:
            return msg + '>>>>>>>>>>>>>>> FULL HOUSE'
        else:
            return msg

    def reserve_time(self, ptime, duration=None):
        if not duration:
            duration = self.play_time
        else:
            duration = timedelta(minutes=int(duration))
        start_time = ptime
        end_time = datetime.combine(date.today(), ptime) + duration
        end_time = end_time.time()
        if (start_time, end_time) not in self.reserved_time:
            self.reserved_time.append((start_time, end_time))

    def print_team(self, input_time):
        if isinstance(input_time, str):
            ptime = format_time_input(input_time)
        else:
            ptime = input_time

        if not ptime:
            return 'No game was found for this time'
        team = self.schedule.get(ptime)
        if not team:
            return 'For {t}: No members for this time'.format(t=ptime.strftime(self.fmt))
        else:
            msg = 'For {t}: {m}'.format(t=ptime.strftime(self.fmt), m=team)
        print(msg)
        return msg

    def check_time(self, ptime):
        team = self.schedule.get(ptime)
        if team and len(team) == config.MEMBERS_MAX:
            raise MembersError('There are no places for this time')
        elif team is None:
            if not self.__check_intervals(ptime):
                msg = ('Busy time.\n'
                       'Your planed game starts or ends '
                       'at already scheduled time')
                raise TimingError(msg)
            self.schedule[ptime] = []

    def check_member(self, ptime, member):
        if member in self.schedule.get(ptime, []):
            raise MembersError('You has been already applied')

    def delete_from(self, input_time, member):
        ptime = format_time_input(input_time)
        game = self.schedule.get(ptime)
        if not game:
            raise DeletionError('Ups, no games for this time')
        if member not in game:
            raise DeletionError('Ups. not your game, bro')

        game.remove(member)
        return '{} was removed from {}'.format(member, ptime.strftime(self.fmt))

    def print_schedule(self):
        print(self.schedule)
        sch = []
        for t in self.schedule:
            sch.append(self.print_team(t))
        print(self.reserved_time)
        return '\n'.join(sch)

    def new_day_cleaner(self):
        if self.playday != date.today():
            self.__clear_scheduler()

    def my_games(self, member):
        result = []
        for ptime in self.schedule:
            if member in self.schedule[ptime]:
                result.append(self.print_team(ptime))
        if result:
            print(result)
            return 'Your games today:\n' + '\n'.join(result)
        else:
            return 'No games'
