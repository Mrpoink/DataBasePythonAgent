import random

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


def pull_csv():
    data_file = pd.read_csv("Airports.csv")
    names = []
    ids = []
    locations = []

    for i in data_file["Name"]:
        names.append(i)
    for i in data_file["ID"]:
        ids.append(i)
    for i in data_file["Location"]:
        locations.append(i)

    return names, ids, locations

names, ids, locations = pull_csv()

print(names)
print(ids)
print(locations)



def create_flight_table():

    for i in range(len(names)):
        query = "INSERT INTO AirPort (AirPortID, Location, Name) VALUES " + "(" + str(ids[i]) + ", " + "'" +  str(locations[i]) + "' " + ", " + "'" + str(names[i]) + "' " + ");"
        print(query)
        try:
            cursor.execute(query)
        except db.errors as e:
            print(e)


planeIDS = []
def create_flights_table():
    to = []
    fro = []
    for i in range(len(ids)):
        if i % 2 == 0:
            to.append(ids[i])
        else:
            fro.append(ids[i])

    for i in range(100):
        rand_to = random.randint(0, len(to)-1)
        rand_fro = random.randint(0, len(fro)-1)

        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        time = str(hour) + ":" + str(minute) + ":" + str(second)

        planeID = random.randint(1000, 9999)
        if planeID in planeIDS:
            planeID = i & ((1 << 10) -1)
            planeIDS.append(planeID)
        planeIDS.append(planeID)
        print(planeID)

        query = "INSERT INTO Flights (FlightID, AirPortIDTo, AirPortIDFrom, BoardingTime, PlaneID) VALUES " + "(" + str(i) + ", " + str(to[rand_to]) + ", " + str(fro[rand_fro]) + ", "+ "'" + str(time) + "'" + ", " + str(planeID) + ");"
        print(query)
        try:
            cursor.execute(query)
        except db.errors as e:
            print(e)



def create_passangers_table():
    first_names = ["Liam", "Noah", "Oliver", "Elijah", "James",
                   "William", "Henry", "Lucas", "Benjamin", "Theodore",
                   "Jack", "Levi", "Alexander", "Mateo", "Michael",
                    "Olivia", "Emma", "Charlotte", "Amelia", "Sophia",
                   "Isabella", "Ava", "Mia", "Evelyn", "Abigail",
                   "Luna", "Harper", "Emily", "Elizabeth", "Sofia"]


    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
        "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
        "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
        "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
        "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
        "Carter", "Roberts"]

    ids = []
    for i in range(100):
        rand_id = random.randint(1000, 9999)

        if rand_id in ids:
            rand_id = i & ((1 << 10) - 1)
            ids.append(rand_id)
        else:
            ids.append(rand_id)

        flightid = i

        if i < 29:
            rand_first = first_names[i]
            rand_last = last_names[i]

        else:
            random.shuffle(first_names)
            random.shuffle(last_names)

            rand_first = first_names[0]
            rand_last = last_names[0]

        query = "INSERT INTO Passangers (ID, FlightID, Name) VALUES " + "(" + str(rand_id) + ", " + str(flightid) + ", '" + rand_first + " " + rand_last + "')"
        print(query)
        try:
            cursor.execute(query)
        except db.errors as e:
            print(e)



create_flight_table()
create_flights_table()
create_passangers_table()
connection.commit()
