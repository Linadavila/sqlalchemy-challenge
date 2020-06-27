#flask file

#-------------------------
#import dependencies
import numpy as np
import datetime as dt
import pandas as pd


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#----------------------------------------------------------
#conection to database - first steps in ipynb file
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

#-----------------------------------------------------
#FLASK

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Want all Hawaii's climate Analysis?<br/>"
        f"Check below paths:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """This is the precipitation for the last year"""
    
    session = Session(engine)
    #last year precipitation as in last file
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    precipitation = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= last_year).all()
    
    session.close()
    # save in dictionary
    precipitation_results = {date: prcp for date, prcp in precipitation}
    return jsonify(precipitation_results)


@app.route("/api/v1.0/stations")
def stations():
    """Here our stations"""
    session = Session(engine)
    list_stations = session.query(station.station).all()
    session.close()

    # Unravel results into a 1D array and convert to a list
    stations_results = list(np.ravel(list_stations))
    return jsonify(stations_results)




