# Import dependencies
import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify

# Set up Flask
app = Flask(__name__)

# Create the connection engine to the sqlite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

# Establish Base for which classes will be constructed 
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Assign the stations class to a variable called `Station`
Station = Base.classes.station

# Assign the measurements class to a variable called `Measurement`
Measurement = Base.classes.measurement

# To query the server we use a Session object
session = Session(engine)

#Need to list all routes that are available 
# `/api/v1.0/precipitation`
#`/api/v1.0/stations`
#`/api/v1.0/tobs`
#`/api/v1.0/<start>`
#`/api/v1.0/<start>/<end>

@app.route("/")
def Home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start/<end>")

#Precipitation for dates of "2016-08-23" and "2017-08-23"
@app.route("/api/v1.0/precipitation")
def precipitation():

    prcp_year = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23")\
            .filter(Measurement.date <= "2017-08-23").order_by(Measurement.date).all()
    
    # Convert object to a list
    prcp_ls=[]
    for item in prcp_year:
        prcp_ls[item[0]]=item[1]
    
    # Return jsonified list
    return (jsonify(prcp_ls))

#Stations
@app.route("/api/v1.0/stations")
def stations():

    stations = session.query(Station.station).all()
    
    # Convert object to a list
    station_list=[]
    for locations in stations:
        for item in locations:
            station_list.append(item)
    
    # Return jsonified list
    return (jsonify(station_list))

#Tobs or Temperature "2016-08-23" and "2017-08-23"
@app.route("/api/v1.0/tobs")
def tobs():

    # Query database for stations
    tobs = session.query(Measurement.date, Measurement.tobs)\
            .filter(Measurement.date >= "2016-08-23")\
            .filter(Measurement.date <= "2017-08-23").order_by(Measurement.date).all()
    
    # Convert object to a list
    tobs_list=[]
    for temperature in tobs:
        for item in temperature:
            tobs_list.append(item)
    
    # Return jsonified list
    return (jsonify(tobs_list))

#Vacation Temperatures Start for "2016-12-15"  and end "2016-12-30"
@app.route("/api/v1.0/<start>/<end>")

def vacation_calcs(start_date, end_date):

    if end_date == 0:
        end_date = "2017-08-23"
    
    # Query database for tobs between start and end date
    vacation_calcs=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
   
    temperature_list = list(np.ravel(vacation_calcs))
    return jsonify(temperature_list)