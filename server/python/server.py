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

@app.route('/data', methods=['GET'])
def get_data():
    data = {
        'message': 'Hello, this is your JSON data!',
        'status': 'success'
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
