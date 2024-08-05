from flask import Flask, jsonify, render_template, url_for
import sqlite3
import random

app = Flask(__name__, static_url_path='/static')

def get_db_connection():
    conn = sqlite3.connect('rc.db')
    conn.row_factory = sqlite3.Row
    return conn

# Image mapping for coasters
coaster_images = {
    'Coaster Name 1': 'coaster1.jpg',
    'Coaster Name 2': 'coaster2.jpg',
    'Coaster Name 3': 'coaster3.jpg',
    'Coaster Name 4': 'coaster4.jpg',
    'Coaster Name 5': 'coaster5.jpg',
    'Coaster Name 6': 'coaster6.jpg',
    'Coaster Name 7': 'coaster7.jpg',
    'Coaster Name 8': 'coaster8.jpg',
    'Coaster Name 9': 'coaster9.jpg',
    'Coaster Name 10': 'coaster10.jpg',
    'Coaster Name 11': 'coaster11.jpg',
    'Coaster Name 12': 'coaster12.jpg',
    'Coaster Name 13': 'coaster13.jpg',
    'Coaster Name 14': 'coaster14.jpg',
    'Coaster Name 15': 'coaster15.jpg',
    'Coaster Name 16': 'coaster16.jpg',
    'Coaster Name 17': 'coaster17.jpg',
    'Coaster Name 18': 'coaster18.jpg',
    'Coaster Name 19': 'coaster19.jpg',
    'Coaster Name 20': 'coaster20.jpg',
    'Coaster Name 21': 'coaster21.jpg',
    'Coaster Name 22': 'coaster22.jpg',
    'Coaster Name 23': 'coaster23.jpg',
    'Coaster Name 24': 'coaster24.jpg',
    'Coaster Name 25': 'coaster25.jpg',
    'Coaster Name 26': 'coaster26.jpg',
}

# Image mapping for parks
park_images = {
    'Alton Towers': 'alton_towers.jpg',
    'Thorpe Park': 'thorpe_park.jpg',
    'Chessington World of Adventures': 'chessington.jpg',
    'Blackpool Pleasure Beach': 'blackpool.jpg',
    # Add more mappings as needed
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/random')
def random_coaster():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Rollercoasters')
    rows = cursor.fetchall()
    conn.close()
    
    # Select a random coaster
    coaster = random.choice(rows)
    coaster = dict(coaster)
    
    # Assuming that the coaster name maps directly to the coaster image
    coaster['image'] = (coaster['Image Path'])

    return render_template('coaster_page.html', coaster=coaster)

@app.route('/coasters')
def coasters():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT "Coaster Name" FROM Rollercoasters')
    rows = cursor.fetchall()
    conn.close()
    coasters = [dict(ix) for ix in rows]
    return render_template('coasters.html', coasters=coasters)

@app.route('/parks')
def parks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT "Park Name" FROM Parks')
    rows = cursor.fetchall()
    conn.close()
    parks = [dict(ix) for ix in rows]
    return render_template('parks.html', parks=parks)


@app.route('/coaster/<name>')
def coaster_page(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Rollercoasters WHERE "Coaster Name" = ?', (name,))
    coaster = cursor.fetchone()
    conn.close()
    if coaster is None:
        return 'Coaster not found!', 404
    coaster = dict(coaster)
    coaster['image'] = (coaster['Image Path'])

    return render_template('coaster_page.html', coaster=coaster)

@app.route('/park/<name>')
def park_page(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Parks WHERE "Park Name" = ?', (name,))
    park = cursor.fetchone()
    conn.close()
    if park is None:
        return 'Park not found!', 404
    park = dict(park)
    park['image'] = park['Image Path']
    return render_template('park_page.html', park=park)

@app.route('/data')
def data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT "Coaster Name" FROM Rollercoasters')
    rows = cursor.fetchall()
    conn.close()
    data = [dict(ix) for ix in rows]
    return jsonify(data)

@app.route('/data_parks')
def data_parks():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT "Park Name" FROM Parks')
    rows = cursor.fetchall()
    conn.close()
    data = [dict(ix) for ix in rows]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
