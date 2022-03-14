# Copyright 2022 Johannes Thorén. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import glob
import json
import os
import threading

import journal
import settings
import player


def check_commander(file):
    f = open(file, "r")
    print(file)
    lines = f.readlines()
    if len(lines) < 10:
        print("skipped file, the file is to small")
        return "file to small"
    for line in lines:
        if line is not None:
            event = json.loads(line)
            if event["event"] == "Commander":
                print("current commander is: " + settings.settings.settings["current_commander"])
                if event["Name"] == settings.settings.settings["current_commander"]:
                    print("correct commander, found: " + event["Name"])
                    return True
                else:
                    print("wrong commander, found: " + event["Name"])
                    return False
            else:
                continue
    print("could not find a commander, file is too small to contain any valuable information")
    return False


def load_events_from_file(file):
    isCorrectCommander = check_commander(file)
    if isCorrectCommander:
        f = open(file, "r")
        lines = f.readlines()
        events = []
        for line in lines:
            if line is not None:
                event = json.loads(line)
                player.player.system_change_check(event)
                events.append(event)

        journal.journal.add_events(events)
        f.close()


def load_events_to_journal_from_file(file):
    isCorrectCommander = check_commander(file)
    if isCorrectCommander != "file to small" and isCorrectCommander != False:
        f = open(file, "r")
        lines = f.readlines()
        for line in lines:
            if line is not None:
                event = json.loads(line)
                player.player.system_change_check(event)
                journal.journal.add_event_to_journal(event)
        f.close()


def get_latest_log_file():
    if settings.settings.settings["journal_location"] != "":
        list_of_files = glob.glob(settings.settings.settings["journal_location"] + '/Journal*.log')
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file
    else:
        return ""


class LogHandler:
    def __init__(self):
        self.latest_log_file_path = get_latest_log_file()
        self.latest_change_time = os.path.getmtime(self.latest_log_file_path)

        self.__file_change_thread_thread = threading.Thread(target=self.check_file_change)
        self.__file_change_thread_thread.start()

        self.__handle_log_path_change = threading.Thread(target=self.handle_latest_log_path_change)
        self.__handle_log_path_change.start()

    # TODO split this function into smaller functions
    def check_file_change(self):
        print("!!!starting new file change watcher thread!!!")
        print("latest log file path: " + self.latest_log_file_path)
        while True:
            comp_time = os.path.getmtime(self.latest_log_file_path)
            if comp_time != self.latest_change_time:
                if check_commander(self.latest_log_file_path):
                    self.latest_change_time = comp_time
                    load_events_from_file(self.latest_log_file_path)

        print("!!!killing file change watcher thread!!!")

    def handle_latest_log_path_change(self):
        while True:
            comp_file = get_latest_log_file()
            if comp_file != self.latest_log_file_path:
                print("new latest log path detected")
                journal.journal.move_to_journal_and_reset()
                self.latest_log_file_path = comp_file
                self.load_initial_events()

    def load_initial_events(self):
        if check_commander(self.latest_log_file_path):
            load_events_from_file(self.latest_log_file_path)

    def load_old_logs(self):
        list_of_files = glob.glob(settings.settings.settings["journal_location"] + '/Journal*.log')
        list_of_files.remove(self.latest_log_file_path)
        for file in list_of_files:
            if check_commander(file):
                load_events_to_journal_from_file(file)


logHandler = LogHandler()
logHandler.load_old_logs()
logHandler.load_initial_events()
