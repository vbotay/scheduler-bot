from datetime import date
from datetime import datetime
from datetime import timedelta

import six

import config
from utils.tools import format_time_input
from utils.tools import time_in_range


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
            if time_in_range(start_time, end_time, ptime):
                print('Busy time.'
                      'There is game from {} to {}.\n'
                      'Your planed game ends in this time'.format(start_time,
                                                                    end_time))
                return False

            ptime_end = datetime.combine(date.today(), ptime) + self.play_time
            ptime_end = ptime_end.time()
            if time_in_range(start_time, end_time, ptime_end):
                print('Busy time.'
                      'There is game from {} to {}.\n'
                      'Your planed game ends in this time'.format(start_time,
                                                                  end_time))
                return False
        return True

    def add_to_schedule(self, input_time, participant):
        ptime = format_time_input(input_time)
        if not ptime:
            return
        if self.check_time(ptime) and self.check_member(ptime, participant):
            self.schedule[ptime].append(participant)
            self.reserve_time(ptime)

            if len(self.schedule[ptime]) == config.MEMBERS_MAX:
                print('>>>>>>>>>>>>>>> FULL HOUSE')

    def reserve_time(self, ptime):
        start_time = ptime
        end_time = datetime.combine(date.today(), ptime) + self.play_time
        end_time = end_time.time()
        if (start_time, end_time) not in self.reserved_time:
            self.reserved_time.append((start_time, end_time))

    def print_team(self, input_time):
        ptime = format_time_input(input_time)
        if not ptime:
            return
        team = self.schedule.get(ptime)
        if not team:
            print('No members for this time')
        else:
            msg = 'For {t}: {m}'.format(t=ptime.strftime(self.fmt), m=team)
            print(msg)

    def check_time(self, ptime):
        team = self.schedule.get(ptime)
        if team and len(team) == config.MEMBERS_MAX:
            print('There are no places for this time')
            return False
        elif team is None:
            # check time is free
            if not self.__check_intervals(ptime):
                return
            print('There are 4 places for this time')
            self.schedule[ptime] = []
        return True

    def check_member(self, ptime, member):
        if member in self.schedule[ptime]:
            print('You has been already applied')
            return False
        return True

    def delete_from(self, input_time, member):
        ptime = format_time_input(input_time)
        game = self.schedule.get(ptime)
        if not game:
            print('no game')
            return
        if member not in game:
            print('netu tut tebya')
            return
        game.remove(member)
        print('{} was removed'.format(member))

    def print_schedule(self):
        for t in self.schedule:
            self.print_team(t.strftime(self.fmt))
        # Todo delete next string
        print(self.reserved_time)

    def new_day_cleaner(self):
        if self.playday != date.today():
            self.__clear_scheduler()

    def my_games(self, member):
        result = {}
        for ptime in self.schedule:
            members = self.schedule[ptime]
            if member in members:
                result[ptime] = members
        print(result)
        return result
