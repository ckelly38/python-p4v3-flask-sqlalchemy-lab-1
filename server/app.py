# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def getEarthquakeById(id):
    eq = Earthquake.query.filter(Earthquake.id==id).first();
    body = None;
    status = -1;
    if (eq == None):
        body = {"message": "Earthquake " + str(id) + " not found."};
        status = 404;
    else:
        body = eq.to_dict();
        status = 200;
    return make_response(body, status);

@app.route('/earthquakes/magnitude/<float:magnitude>')
def getEarthquakesWithMagnitudeAtLeastAsBigAs(magnitude):
    eqs = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all();
    body = None;
    status = -1;
    if (eqs == None or len(eqs) < 1):
        body = {"count": 0, "quakes": []};
        status = 200;
    else:
        mlist = [eq.to_dict() for eq in eqs];
        body = {"count": len(eqs), "quakes": mlist};
        status = 200;
    return make_response(body, status);


if __name__ == '__main__':
    app.run(port=5555, debug=True)
