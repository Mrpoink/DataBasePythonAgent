from DataBaseConnect import create_connection, connect, create_table
import mysql.connector as db


def insert_booking():
    #Enter a new row creation for new table

def view_booking():
    #Find row in table

def delete_booking():
    #Delete row in table

def user_choice():
    connect_to_db()
    connection = connect("FLIGHTS")
    cursor = connection.cursor()
    cursor.execute("")
    #Book, View Reservation, Cancel Reservation