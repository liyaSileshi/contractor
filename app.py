from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime

app = Flask(__name__)


lipsticks = [
    { 'title': 'red', 'description': 'matte' },
    { 'title': 'pink', 'description': 'gloss' }
]

@app.route('/')
def lipstick_index():
    """Show all lipsticks."""
    return render_template('lipsticks_index.html', lipsticks=lipsticks)

if __name__ == '__main__':
    app.run(debug=True)

