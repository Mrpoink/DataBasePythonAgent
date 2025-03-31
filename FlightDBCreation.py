import mysql.connector as db
from DataBaseLogInInfo import LogInfo as user
import pandas as pd

def connect_to_db():
    try:
        connection = db.connect(
            user = user.username,
            password = user.password,
            host = user.host)
        if connection.is_connected():
            print("Chosen successfully")
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS FLIGHTS")
        cursor.execute("Use FLIGHTS")
        cursor.execute(createAirPort())
        cursor.execute(createFlights())
        cursor.execute(createPassangers())
        result = cursor.fetchall()
        for item in result:
            print(str(item))
    except db.errors as e:
        print(e)


def createAirPort():
    creation_query = ("CREATE TABLE AirPort "
                      "(AirPortID Integer NOT NULL, "
                      "Location Varchar(120), "
                      "Name Varchar(120), "
                      "PRIMARY KEY (AirPortID))")
    return creation_query

def createFlights():
    creation_query = ("CREATE TABLE Flights "
                      "(FlightID INTEGER, "
                      "AirPortIDTo INTEGER, "
                      "AirPortIDFrom INTEGER, "
                      "BoardingTime TIME, "
                      "PlaneID INTEGER NOT NULL, "
                      "PRIMARY KEY(FlightID), "
                      "FOREIGN KEY(AirPortIDFrom) REFERENCES AirPort(AirPortID), "
                      "FOREIGN KEY(AirPortIDTo) REFERENCES AirPort(AirPortID))")
    return creation_query

def createPassangers():
    creation_query = ("CREATE TABLE Passangers "
                      "(ID Integer, FlightID Integer, "
                      "Name Varchar(60), PRIMARY KEY (ID), "
                      "FOREIGN KEY(FlightID) REFERENCES Flights(FlightID))")
    return creation_query

connect_to_db()