from datetime import datetime

import flask
from flask import Flask, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy

DB_USERNAME = 'postgres'
DB_PASSWORD = 'postgres'
DB_NETWORK = 'localhost'
DB_DATABASE = 'city'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_NETWORK}/{DB_DATABASE}'
db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String, nullable=False)
    visit_date = db.Column(db.Date, nullable=False)

    def __init__(self, city_name, visit_date):
        self.city_name = city_name
        self.visit_date = visit_date


@app.route('/', methods=['GET'])
def index():
    error = request.args.get('error', '')
    return flask.render_template('index.html', cities=City.query.all(), error=error)


@app.route('/city', methods=['POST'])
def add_new_city_visit():
    city_name = request.form['city_name']
    visit_date = request.form['visit_date']

    if city_name == '' or visit_date == '':
        return redirect(url_for('index', error='Пожалуйста, введите название города и дату посещения'))

    visit_date = datetime.strptime(visit_date, '%Y-%m-%d').date()

    if visit_date > datetime.now().date():
        return redirect(url_for('index', error='Дата посещения должна быть до сегодняшнего дня'))

    db.session.add(City(city_name, visit_date))
    db.session.commit()

    return redirect(url_for('index')) 


@app.route('/city', methods=['DELETE'])
def delete_all_comments():
    City.query.delete()
    db.session.commit()
    return "Success"


with app.app_context():
    db.create_all()

app.run()
