from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime


client = MongoClient()
db = client.lipstick
lipsticks = db.lipsticks


app = Flask(__name__)


# lipstick = [
#  { 'title': 'red', 'description': 'matte' },
#     { 'title': 'pink', 'description': 'gloss' }
# ]

#lipsticks.insert_many(lipstick)
# lipsticks.delete_many

#deleting from the document
#ipsticks.delete_many({'title':'red'})

@app.route('/')
def lipstick_index():
    """Show all lipsticks."""
    return render_template('lipsticks_index.html', lipsticks=lipsticks.find())

@app.route('/lipsticks/new')
def lipstick_new():
    """Create new lipsticks."""
    return render_template('lipstick_new.html')

@app.route('/lipsticks', methods=['POST'])
def lipsticks_submit():
    """Submit a new lipstick."""
    lipstick = {
        'type': request.form.get('type'),
        'color': request.form.get('color'),
        'brand': request.form.get('brand'),
        'image': request.form.get('image')
    }
    # print(request.form.to_dict())
    return redirect(url_for('lipstick_index'))


if __name__ == '__main__':
    app.run(debug=True)

