# import dependencies

import datetime as dt
import numpy as np
import pandas as pd

# import sqlalchemy dependencies

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import Flask dependencies

from flask import Flask, jsonify

# access and query our SQLite database file

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database into our classes

Base = automap_base()

# reflect the database

Base.prepare(engine, reflect=True)

# save our references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database

session = Session(engine)

## define app for the Flask application

# create a Flask application

app = Flask(__name__) # __name__ = __main__ in this case

# create the welcome route

@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API! <br/>
    Available Routes: <br/>
    <a href="/api/v1.0/precipitation" target="_blank"> precipitation <br/>
    <a href="/api/v1.0/stations" target="_blank"> stations <br/>
    <a href="/api/v1.0/tobs" target="_blank"> tobs <br/>
    <a href="/api/v1.0/temp/start/end" target="_blank"> temp/start/end <br/>
    ''')
print("done")

# precipitation route

@app.route('/api/v1.0/precipitation')
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    # create a dictionary with the date as the key and the precipitation as the value
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# stations route

@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.station).all()
    # unraveling our results into a one-dimensional array
    # convert our unraveled results into a list
    stations = list(np.ravel(results))
    return jsonify(stations=stations) # formats list into JSON

# monthly temperature route

@app.route('/api/v1.0/tobs')
def temp_monthly():
    prev_year = dt.date(2017, 8, 27) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.date >= prev_year).\
        filter(Measurement.station == 'USC00519281').all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


# temp route




if __name__ == "__main__":
    app.run(debug=True) # track modifications in live