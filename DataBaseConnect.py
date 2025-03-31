import mysql.connector as db
from DataBaseLogInInfo import LogInfo as user
from mysql.connector import errors

def connect(dbname):
    if dbname is not None:
        try:
            connection = db.connect(
                user = user.username,
                password = user.password,
                host = user.host,
                database = dbname)
            if connection.is_connected():
                print("Chosen successfully")
        except db.Error as err:
            print("Cannot connect due to: " + str(err))

        return connection
    try:
        connection = db.connect(
            user = user.username,
            password = user.password,
            host = user.host)
        if connection.is_connected():
            print("Connected successfully")
    except db.Error as err:
        print("Cannot connect due to: " + str(err))

    return connection

connection = connect(None)

def create_connection():
    new_cursor = connection.cursor()
    new_cursor.execute("SHOW DATABASES")
    i=0
    for x in new_cursor:
        i+=1
        print(i, ". ", x)
    i = i - 1
    connection.close()
    user_choice = input("Choose Database to use: ")
    new_connection = connect(user_choice)
    return new_connection

new_connection = create_connection()

def create_table(connection_to_db):
    cursor = connection_to_db.cursor()
    while True:
        query = input("Enter Query or 'exit': ")
        if query == "exit":
            cursor.close()
            break
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            for item in result:
                print(str(item))
            connection_to_db.commit()
        except db.Error as err:
            print("Cannot connect due to: " + str(err))
            cursor.fetchwarnings()


create_table(new_connection)




