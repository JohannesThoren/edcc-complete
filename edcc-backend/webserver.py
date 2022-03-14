# Copyright 2022 Johannes Thorén. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import os

from flask import Flask, render_template
from flask_cors import CORS

import routes

template_dir = os.path.abspath('dist')


app = Flask(__name__, static_folder='dist', template_folder=template_dir)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

app.register_blueprint(routes.api)


@app.route("/")
def home_page():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3500, debug=False)
