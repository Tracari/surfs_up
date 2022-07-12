# import dependencies
import datetime as dt
from email.mime import base
import pandas as pd
import numpy as np
# import SQLalchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
# import Flask dependencies
from flask import Flask, jsonify

# Set up database engine for Flask application
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into existing classes
Base = automap_base()
# Reflect our table
Base.prepare(engine, reflect=True)

# Save references to each tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link from Python to the database
session = Session(engine)

# Set up Flask, create a Flask app
app = Flask(__name__)

# Create the Welcome Route --> Homepage
@app.route("/")
# Create additional routes
def welcome():
    return (
    """
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    """)
# Create the precipitation route
@app.route('/api/v1.0/precipitation')
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)
# Create the stations route
@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
# Create the temperature observation route
@app.route('/api/v1.0/tobs')
def temp_monthly():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
# Create the statistics route
@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return  jsonify(temps)
    
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(f'temps: {temps}')






