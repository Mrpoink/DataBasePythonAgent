import random
import sys
import pandas as pd
import mysql.connector as db
from DataBaseLogInInfo import LogInfo as user

connection = db.connect(
    user = user.username,
    password = user.password,
    host = user.host,
    database = "FLIGHTS")
if connection.is_connected():
    print("Chosen successfully")
cursor = connection.cursor()

def main():
    while True:
        userin = int(input("1.View flight information\n"
                           "2.View airport information\n"
                           "3.View Passenger information\n"
                           "4.Make new booking\n"
                           "5.Show bookings for user\n"
                           "6.Delete Booking\n"
                           "7.Exit\n"
                           "Enter:"))

        match userin:
            case 1:
                flight_info()
            case 2:
                airport_info()
            case 3:
                passenger_info()
            case 4:
                make_booking()
            case 5:
                get_booking()
            case 6:
                delete_booking()
            case 7:
                break


def flight_info():
    query = ("SELECT f.FlightID, "
             "ap_to.Name AS AirPortToName, "
             "ap_from.Name as AirPortFromName, "
             "f.BoardingTime, f.PlaneID"
             " FROM Flights as f INNER JOIN"
             " AirPort as ap_to ON"
             " f.AirPortIDTo = ap_to.AirPortID INNER JOIN"
             " AirPort AS ap_from ON"
             " f.AirPortIDFrom = ap_from.AirPortID")
    cursor.execute(query)
    result = cursor.fetchall()
    fid, to_name, from_name, time, pid = "FlightID", "To", "From", "Time", "PlaneID"
    print(f"{fid:<5}|{to_name:<25}|{from_name:<25}|{str(time):<10}|{pid:<10}")
    for item in result:
        fid, to_name, from_name, time, pid = item
        print(f"{fid:<5}|{to_name:<25}|{from_name:<25}|{str(time):<10}|{pid:<10}")


def airport_info():
    query = "SELECT * FROM AirPort"
    cursor.execute(query)
    result = cursor.fetchall()

    pid, ploc, pname = "ID", "Location", "Name"
    print(f"{pid:<5}|{ploc:<20}|{pname:<20}")

    for item in result:
        id, location, name = item
        print(f"{id:<5}|{location:<20}|{name:<20}")


def passenger_info():
    query = "SELECT * FROM Passangers"
    cursor.execute(query)
    result = cursor.fetchall()

    pid, fid, pname = "PID", "FID", "Name"
    print(f"{pid:<5}|{fid:<5}|{pname:<20}")

    for item in result:
        id, fid, name = item
        print(f"{id:<5}|{fid:<5}|{name:<20}")


def make_booking():
        name = input("Enter your name: ")

        location = location_request()
        air_info = ("SELECT AirPortID, Name FROM AirPort WHERE Location = '" + location + "'")
        cursor.execute(air_info)
        air_result = cursor.fetchall()
        for item in air_result:
            aid, aname = item

        plane_info = ("SELECT f.FlightID, "
                      "ap_to.Name AS AirPortToName, "
                      "ap_from.Name as AirPortFromName, "
                      "f.BoardingTime, f.PlaneID FROM "
                      "Flights as f INNER JOIN "
                      "AirPort as ap_to ON f.AirPortIDTo = ap_to.AirPortID INNER JOIN "
                      "AirPort as ap_from ON f.AirPortIDFrom = ap_from.AirPortID "
                      "WHERE f.AirPortIDFrom = '" + str(aid) + "'")
        cursor.execute(plane_info)
        plane_result = cursor.fetchall()
        if len(plane_result) == 0:
            print("Airport is closed for today please try again")
            sys.exit(0)
        plane_results = []
        for item in plane_result:
            fid, to_name, from_name, time, pid = item
            print(f"FlightID: {fid:<5}|PlaneID: {pid:<5}|From: {from_name:<25}|To: {to_name:<25}|At: {time}")
            plane_results.append(str(item)[1:-2])

        user_plane_info = input("Enter FlightID to book: ")

        user_plane_info_query = ("SELECT f.PlaneID, "
                           "ap_to.Name AS AirPortToName, "
                           "ap_from.Name as AirPortFromName, "
                           "f.BoardingTime FROM "
                           "Flights as f INNER JOIN "
                           "AirPort as ap_to ON "
                           "f.AirPortIDTo = ap_to.AirPortID INNER JOIN "
                           "AirPort as ap_from ON "
                           "f.AirPortIDFrom = ap_from.AirPortID WHERE f.FlightID = '" + user_plane_info + "'")
        cursor.execute(user_plane_info_query)
        user_plane_result = cursor.fetchall()
        for item in user_plane_result:
            id, to, fro, time = item
            print(f"FlightID: {user_plane_info:<5}|PlaneID: {id:<5}|From: {fro:<25}|To: {to:<25}|At: {str(time):<10}  Today")

        passenger_id = str(random.randint(1000, 9999))
        query = "INSERT INTO Passangers (ID, FlightID, Name) VALUES ('" + passenger_id + "', '" + str(user_plane_info) + "', '" + name + "')"
        print("Ticket Booked, Passenger ID: " + passenger_id)
        cursor.execute(query)
        connection.commit()



#IDK why I have to include this jsut for the return statement but
#clean code is clean
def location_request():
    data_file = pd.read_csv("Airports.csv")
    locations = []
    while True:
        for i in data_file["Location"]:
            locations.append(i)
        for i in locations:
            print(f"{i}")
        location = input("Where would you like to depart from?: ")
        if not (location in locations):
            print("Please try again")
        elif location in locations:
            return location


def get_booking():
    user_passenger_name = input("Enter your name: ")
    query = ("SELECT ap_to.Name as AirPortToName,"
             " ap_from.Name as AirPortFromName,"
             " f.BoardingTime, p.ID FROM Passangers as p INNER JOIN Flights as f"
             " ON p.FlightID = f.FlightID INNER JOIN AirPort as ap_to"
             " ON f.AirPortIDTo = ap_to.AirPortID INNER JOIN"
             " AirPort AS ap_from ON f.AirPortIDFrom = ap_from.AirPortID WHERE p.Name = '" + user_passenger_name + "'")
    cursor.execute(query)
    result = cursor.fetchall()
    for item in result:
        to, fro, time, id = item
        print(f"PassengerID: {id:<5}|From: {fro:<25}|To: {to:<25}|At:{time}")



def delete_booking():
    user_passenger_name = input("Enter your name: ")
    query = ("SELECT ap_to.Name as AirPortToName,"
             " ap_from.Name as AirPortFromName,"
             " f.BoardingTime, p.ID FROM Passangers as p INNER JOIN Flights as f"
             " ON p.FlightID = f.FlightID INNER JOIN AirPort as ap_to"
             " ON f.AirPortIDTo = ap_to.AirPortID INNER JOIN"
             " AirPort AS ap_from ON f.AirPortIDFrom = ap_from.AirPortID WHERE p.Name = '" + user_passenger_name + "'")
    cursor.execute(query)
    result = cursor.fetchall()
    for item in result:
        to, fro, time, id = item
        print(f"PassengerID: {id:<5}|From: {fro:<25}|To: {to:<25}|At:{time}")
    user_deleting = input("Enter PassengerID to delete: ")
    query = "DELETE FROM Passangers WHERE ID = '" + user_deleting + "'"
    cursor.execute(query)
    connection.commit()

main()