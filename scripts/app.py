import json
from flask import Flask, jsonify, send_file
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def inicio():
    return "O site está no ar!"


@app.route('/dados/')
def getdados():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, '../basestratadas/arrecadacao-estadov2.csv')
    return send_file(csv_path, as_attachment=True)

app.run(debug=True)