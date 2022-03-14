# Copyright 2022 Johannes Thorén. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import player


class Journal:
    def __init__(self):
        self.__journal = []
        self.__events = []
        self.__latest = []

    def non_match(self, events):
        non_match = []
        events_len = len(events)
        journal_len = len(self.__events) + len(self.__latest)

        for index in range(journal_len, events_len):
            non_match.append(events[index])
        return non_match

    def add_events(self, events):
        '''adds events to the __latest list'''
        non_match = self.non_match(events)
        for event in non_match:
            self.__latest.append(event)

    def move_latest(self):
        '''This function, when called, will move all objects int __latest to __events'''
        for e in self.__latest:
            player.player.system_change_check(e)
            self.__events.append(e)
            self.__journal.append(e)

    def get_latest(self):
        tmp = self.__latest
        self.move_latest()
        self.__latest = []
        return tmp

    def get_events(self):
        return self.__events

    def get_journal(self):
        return self.__journal

    def add_event_to_journal(self, e):
        player.player.system_change_check(e)
        self.__journal.append(e)
        self.__journal = sorted(self.__journal, key=lambda k: k["timestamp"])

    def move_to_journal_and_reset(self):
        for e in self.__events:
            self.__journal.append(e)
        for e in self.__latest:
            self.__journal.append(e)
        self.reset_temp_lists()

    def reset_temp_lists(self):
        self.__latest = []
        self.__events = []

    def clear_journal(self):
        self.__journal = []


journal = Journal()
