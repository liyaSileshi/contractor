from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

