from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime


client = MongoClient()
db = client.lipstick
lipsticks = db.lipsticks


app = Flask(__name__)


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
        'image': request.form.get('image'),
        'price': request.form.get('price')
    }
    lipstick_id = lipsticks.insert_one(lipstick).inserted_id
    #lipsticks.insert_one(lipstick)
    # print(request.form.to_dict())
    return redirect(url_for('lipstick_show', lipstick_id = lipstick_id))

@app.route('/lipsticks/<lipstick_id>')
def lipstick_show(lipstick_id):
    """Show a single lipstick."""
    lipstick = lipsticks.find_one({'_id' : ObjectId(lipstick_id)})
    return render_template('lipstick_show.html', lipstick= lipstick)

@app.route('/lipsticks/<lipstick_id>/edit')
def lipstick_edit(lipstick_id):
    """Show the edit form for a lipstick."""
    lipstick = lipsticks.find_one({'_id': ObjectId(lipstick_id)})
    return render_template('lipstick_edit.html', lipstick=lipstick)

@app.route('/lipsticks/<lipstick_id>', methods=['POST'])
def lipsticks_update(lipstick_id):
    """Submit an edited lipstick."""
    updated_lipstick = {
         'type': request.form.get('type'),
        'color': request.form.get('color'),
        'brand': request.form.get('brand'),
        'image': request.form.get('image'),
        'price': request.form.get('price')
    }
    lipsticks.update_one(
        {'_id': ObjectId(lipstick_id)},
        {'$set': updated_lipstick})
    return redirect(url_for('lipstick_show', lipstick_id=lipstick_id))

@app.route('/lipsticks/<lipstick_id>/delete', methods=['POST'])
def playlists_delete(lipstick_id):
    """Delete one lipstick."""
    lipsticks.delete_one({'_id': ObjectId(lipstick_id)})
    return redirect(url_for('lipstick_index'))


if __name__ == '__main__':
    app.run(debug=True)

