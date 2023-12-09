from typing import Dict

from flask import Flask
from flask_cors import CORS

app = Flask('country-visualiser')
CORS(app)


@app.route('/')
def index() -> Dict:
    return {'hello': 'there!'}
