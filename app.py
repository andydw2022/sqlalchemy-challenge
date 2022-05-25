import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
################################################
#
#  Home page
#
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date/<start_date><br/>"
        f"/api/v1.0/start_date_end_date/<date_range>"
    )

@app.route("/api/v1.0/stations")

  # Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

  # Return the JSON representation of your dictionary.

def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all stations
 
    results = session.query(Station.station, Station.name,Station.latitude,Station.longitude, Station.elevation).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/precipitation")

  # Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

  # Return the JSON representation of your dictionary.
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query rainfall and date
    results = session.query(Station.name, Measurement.date, Measurement.prcp).\
        filter(Station.station==Measurement.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)
    # # Create a dictionary from the row data and append to a list of all_passengers
    # all_rainfall = []
    # for name, age, sex in results:
    #     rainfall_dict = {}
    #     rainfall_dict["name"] = name
    #     rainfall_dict["age"] = age
    #     rainfall_dict["sex"] = sex
    #     all_rainfall.append(rainfall_dict)

    # return jsonify(all_rainfall)

@app.route("/api/v1.0/tobs")

  #  Query the dates and temperature observations of the most active station for the last year of data.
  
  #  Return a JSON list of temperature observations (TOBS) for the previous year.

def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query to retrieve most active stations
    #results = session.query(Measurement.station,Measurement.tobs).all()
    results = session.query(Station.name, Measurement.station, func.count(Measurement.tobs)).\
    filter(Station.station==Measurement.station).filter(Measurement.date >= "2016-08-23" , Measurement.date >= "2016-08-23").group_by(Measurement.station).\
    order_by(func.count(Measurement.tobs).desc()).all()

    # results = session.query(Measurement.station, func.count(Measurement.tobs)).\
    # group_by(Measurement.station).\
    # order_by(func.count(Measurement.tobs).desc()).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/start_date/<start_date>")

   # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

   # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

   # When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
def calc_temps(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    start_date = '"' + start_date + '"'
  
    # Query to retrieve most active stations
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >=start_date).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))
    #return(start_date)
    return jsonify(all_names)


@app.route("/api/v1.0/start_date_end_date/<date_range>/<end_date>")

   # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

   # When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

   # When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
def calc_temps_end_date(date_range,end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # date_range2=date_range.split('/')
    # start_date = '"'+ date_range2[0] + '"'
    # end_date = '"' + date_range2[1] + '"'

    # Query to retrieve most active stations
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= date_range).filter(Measurement.date <= end_date).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))
    #return(start_date + end_date)
    return jsonify(all_names)


if __name__ == '__main__':
    app.run(debug=True)
