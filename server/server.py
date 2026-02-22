from typing import Final

from labyrinth import Labyrinth, Cell
from labyrinth import PrintLabyrinth

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
labytinth_counter = 0

@app.route('/get-labyrinth', methods=['GET'])
def get_labyrinth():
    labyrinth = Labyrinth.Generate(width, height)
    global labytinth_counter
    labytinth_counter += 1

    data = {
        "id": f"{labytinth_counter}",
        "width": f"{width}",
        "height": f"{height}",
        "cells": list(labyrinth.Cells()),
        "test": PrintLabyrinth(labyrinth, (0, 0)),
        "status": "success"
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    print("Labyrinth server started")
