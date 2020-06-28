#flask file

#-------------------------
#import dependencies
import numpy as np
import pandas as pd
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify
import datetime as dt


#----------------------------------------------------------
#conection to database - first steps in ipynb file

hawaii_data_path = "./Resources/hawaii.sqlite"
engine = create_engine(f"sqlite:///{hawaii_data_path}")
conn = engine.connect()

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
    
    #starts the session connection
    session = Session(engine)
    #last year precipitation as in last file
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #calculate data that applies to this section
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year).all()
    
    #close session
    session.close()
    # save in dictionary
    precipitation_results = {date: prcp for date, prcp in precipitation}
    return jsonify(precipitation_results)


@app.route("/api/v1.0/stations")
def stations():
    """Here our stations"""
    #Start the session conection
    session = Session(engine)

    #Calculate the data that applies for this section
    list_stations = session.query(Station.station).all()

    #close the session conection
    session.close()

    # add data to the list
    stations_results = list(np.ravel(list_stations))
    return jsonify(stations_results)


@app.route("/api/v1.0/tobs")
def temp_obs():
    """Last year temperature observations (tobs)"""
    #start conection to session
    session = Session(engine)

    #calculate the data that applies to this section
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    tobs_results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= last_year).all()
    
    #close the connection to the session
    session.close()

    # list the results
    tobs_list = list(np.ravel(tobs_results))


    return jsonify(tobs_list)

#define 2 routes as per posibilities
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""
    
    #Start the connection to session
    session = Session(engine)
    
    #calculate data that belongs to this section
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        #add the resuts to a list, for results if only getting end point
        temps = list(np.ravel(results))
        return jsonify(temps)

    # calculate results if we are given start date and end date
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    session.close()
    #add the results to a list
    temps_list = list(np.ravel(results))
    return jsonify(temps_list)


#run the app
if __name__ == '__main__':
    app.run()



