# **** Flask sample exercise code ****
# from flask import Flask
# app= Flask(__name__)
# @app.route('/')
# def hello_world():
#     return 'Hello World'
# *** End of sample code *****

# Module 9.5 - Import Flask app python dependencies
import datetime as dt 
import numpy as np 
import pandas as pd 

# import SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# import flask dependencies
from flask import Flask, jsonify

# Database setup
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into our classes
Base = automap_base()
Base.prepare(engine,reflect=True)

# create variables for each class so they can be referenced
Measurement = Base.classes.measurement
Station = Base.classes.station

# Now lets create a session link to invoke the SQL call
session = Session(engine)

# Now let set up the Flask
app = Flask(__name__)

# DEfining the welcome route
@app.route("/")

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Precipitation route
@app.route("/api/v1.0/precipitation")

def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Station route

@app.route("/api/v1.0/station")

def station():
   
   results = session.query(Station.station).all()
   # convert our results into a list and then will return as a JSON o/p
   stations = list(np.ravel(results))
   return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")

# Temperature route
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# statistics Route
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)