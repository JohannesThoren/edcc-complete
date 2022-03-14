# Copyright 2022 Johannes Thorén. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import json

import requests
from flask import blueprints, jsonify, request

import journal
import player
import settings
import LogHandler

api = blueprints.Blueprint("api_user", __name__)


@api.route('/api/', methods=['get'])
def ping():
    return "pong"


@api.route('/api/events/latest')
def get_latest_events():
    return jsonify(results=journal.journal.get_latest())


@api.route('/api/events/initial')
def get_initial_events():
    journal.journal.move_latest()
    return jsonify(results=journal.journal.get_journal(), length=len(journal.journal.get_journal()))


@api.route('/api/settings', methods=["get", "post"])
def get_settings():
    if request.method == "GET":
        return jsonify(results=settings.settings.get_settings())
    if request.method == "POST":
        request_data = request.json
        settings.settings.update_settings(request_data)

        # the following lines of code is only necessary if the current commander is changed.
        if request_data.get("current_commander"):
            journal.journal.reset_temp_lists()
            journal.journal.clear_journal()
            LogHandler.logHandler.load_old_logs()
            LogHandler.logHandler.load_initial_events()

        return request_data


@api.route('/api/system')
def get_current_system():
    if settings.settings.settings["platform_for_system_data"]["edsm"]:
        player.player.set_system_data(requests.get(f"https://www.edsm.net/api-v1/system?systemName={player.player.get_current_system()}&showId=1&showCoordinates=1&showPermit=1&showInformation=1&showPrimaryStar=1").content)
    return player.player.get_system_data()
