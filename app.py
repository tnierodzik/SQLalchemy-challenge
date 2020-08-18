# Dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Create session
session = Session(engine)

#Setup Flask
app = Flask(__name__)

# Set Up Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return ("Welcome to the Surfs Up Weather-API!<br><br>"
    	f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/temperture<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitations():

	# Query for temperture measurements from last year
	precipitations = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date>="2016-08-23").\
    order_by(Measurement.date).all()

	# Close Session
	session.close()

	# Create a list of dictionaries
	precipitation_dict = {}
	for precipitation in precipitations:
		precipitation_dict[precipitation[0]] = precipitation[1]
	
	# Jsonify  List
	return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations():

	# Query stations list
	stations = session.query(Station.id,Station.station,Station.name).all()
	session.close()

	# Create a list of dictionaries
	stations_list = list(np.ravel(stations))

	# Jsonify  List
	return jsonify(stations_list)

@app.route("/api/v1.0/temperture")
def temperture():

	# Query for temperture measurements from last year
	tobs = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date>="2016-08-23").\
        filter(Measurement.station == 'USC00519281').\
        order_by(Measurement.date).all()
	session.close()

	# Create a list of Dictionaries	
	tobs_list = []
	for tob in tobs:
		tobs_dict = {}
		tobs_dict["station"] = tob.station
		tobs_dict["date"] = tob.date
		tobs_dict["tobs"] = tob.tobs
		tobs_list.append(tobs_dict)

	# Jsonify List
	return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start):

	# Query for temperture measurements base of start date
	start_result=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
		filter(Measurement.date >= start).all()
	session.close()

	# Create a list of dictionaries
	ptps = list(np.ravel(start_result))

	# Jsonify List
	return jsonify(ptps)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):

	# Query for temperture measurements base of start date & end date
	start_end_result=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
		filter(Measurement.date.between(start,end)).all()
	session.close()

	# Create a list of dictionaries
	ptps = list(np.ravel(start_end_result))

	# Jsonify List
	return jsonify(ptps)

if __name__ == "__main__":
    app.run(debug = True)