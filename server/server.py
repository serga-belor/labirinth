from typing import Final

from labirinth import Labirinth, Cell
from labirinth import PrintLabirinth

from flask import Flask, send_from_directory, jsonify
import os


public_dir_path = os.path.join(os.path.dirname(__file__), 'public')
print("Public folder:", public_dir_path)

app = Flask(__name__, static_folder=public_dir_path)

@app.route('/test', methods=['GET'])
def test():
    data = {
        "test": "this is test",
    }
    return jsonify(data)

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
def get_labirinth():
    labirinth = Labirinth.Generate(width, height)
    global labitinth_counter
    labitinth_counter += 1

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
    app.run(host="0.0.0.0", port=5000, debug=True)
    print("Labirinth server started")
