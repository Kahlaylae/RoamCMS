#!/usr/bin/env python3
"""
JSON Table Editor - Flask Server
View, edit, add, and delete rows in your JSON files through a web interface.
"""

import json
import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

DATA_DIR = os.path.dirname(os.path.abspath(__file__))


def get_json_files():
    """Return list of .json files in the data directory."""
    files = []
    for f in sorted(os.listdir(DATA_DIR)):
        if f.endswith('.json') and os.path.isfile(os.path.join(DATA_DIR, f)):
            files.append(f)
    return files


def load_json(filename):
    """Safely load a JSON file."""
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return None, "File not found"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data, None
    except json.JSONDecodeError as e:
        return None, f"Invalid JSON: {str(e)}"
    except Exception as e:
        return None, str(e)


def save_json(filename, data):
    """Save data to a JSON file with pretty formatting."""
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True, None
    except Exception as e:
        return False, str(e)


@app.route('/')
def index():
    """Serve the main editor page."""
    files = get_json_files()
    return render_template('index.html', files=files)


@app.route('/api/files')
def api_files():
    """Return list of JSON files."""
    return jsonify(get_json_files())


@app.route('/api/data/<filename>')
def api_get_data(filename):
    """Get data from a specific JSON file."""
    data, error = load_json(filename)
    if error:
        return jsonify({'error': error}), 404
    return jsonify(data)


@app.route('/api/data/<filename>', methods=['POST'])
def api_save_data(filename):
    """Save data to a specific JSON file."""
    new_data = request.get_json()
    if new_data is None:
        return jsonify({'error': 'Invalid JSON body'}), 400
    if not isinstance(new_data, list):
        return jsonify({'error': 'Data must be a JSON array'}), 400

    success, error = save_json(filename, new_data)
    if not success:
        return jsonify({'error': error}), 500
    return jsonify({'status': 'ok', 'count': len(new_data)})


if __name__ == '__main__':
    print("\n📊 JSON Table Editor")
    print("=" * 40)
    print(f"Data directory: {DATA_DIR}")
    print(f"JSON files found: {', '.join(get_json_files())}")
    print("\nOpen http://localhost:5050 in your browser\n")
    app.run(host='127.0.0.1', port=5050, debug=False)
