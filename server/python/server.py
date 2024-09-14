from typing import Final

from labirinth import Labirinth, Cell
from labirinth import PrintLabirinth

from flask import Flask, send_from_directory, jsonify
import os


site_dir_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'site', 'public')
print("Site folder:", site_dir_path)

app = Flask(__name__, static_folder=site_dir_path)

@app.route('/', methods=['GET'])
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_resource(filename):
    return send_from_directory(app.static_folder, filename)

width: Final = 5
height: Final = 5
labitinth_counter = 0

@app.route('/get-labirinth', methods=['GET'])
def get_data():
    labirinth = Labirinth.Generate(width, height)
    #labitinth_counter += 1

    data = {
        "id": f"{labitinth_counter}",
        "width": f"{width}",
        "height": f"{height}",
        "cells": list(labirinth.Cells()),
        "test": PrintLabirinth(labirinth, (0, 0)),
        "status": "success"
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
