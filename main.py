from socket import socket
import mysql.connector  # importing the mysql - python connector
import csv  # import the csv lib
import os

cnx = mysql.connector.connect(user='root', password='root',
host ='127.0.0.1', buffered=True)  # connecting to mysql. Uing buffered=True to fix  error (xception has occurred: InternalError Unread result found)

DB_NAME = 'computer_parts'   # The database name

cursor = cnx.cursor()   # defining the mysql cursor

cursor.execute("SHOW DATABASES")    # registers the existing databases in the cursor

db_exists = False

for x in cursor:    # check if database exists
    if x == (DB_NAME,):
        db_exists = True
        cursor.execute("USE %s" % DB_NAME)
        print("Database", DB_NAME, "exists.")
        break

if db_exists == False:      # if database does not exist, we create it and it's tables as well as import the data.
    print("creating DATABASE %s" % DB_NAME)
    cursor.execute("CREATE DATABASE %s" % DB_NAME)
    cursor.execute("USE %s" % DB_NAME)

    cursor.execute("CREATE TABLE IF NOT EXISTS cpu (brand nvarchar(50), model varchar(50), speed nvarchar(50), cores nvarchar(50), threads nvarchar(50), socket nvarchar(50), primary key(model))")

    with open('cpu.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=',')    # reading the csv file cpu
        for line in reader:
            cursor.execute("INSERT INTO cpu (brand,model,speed,cores,threads,socket)" \
                            "VALUES('%s', '%s', '%s', '%s', '%s', '%s')" % (line['brand'], line['model'], line['speed'], line['cores'], line['threads'], line['socket']))
                            # inserting the values of the csv into the specified database table collumns for cpu.csv
    cnx.commit()    # commiting changest to the table and database

    cursor.execute("CREATE TABLE IF NOT EXISTS ram (name nvarchar(50), brand nvarchar(50), capacity nvarchar(50), speed nvarchar(50), ram_type nvarchar(50), primary key(name))")

    with open('ram.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=',')    # reading the csv file ram
        for line in reader:
            cursor.execute("INSERT INTO ram (name,brand,capacity,speed,ram_type)" \
                            "VALUES('%s', '%s', '%s', '%s', '%s')" % (line['name'], line['brand'], line['capacity'], line['speed'], line['ram_type']))
                            # inserting the values of the csv into the specified database table collumns for ram.csv
    cnx.commit()    # commiting changest to the table and database

    cursor.execute("CREATE TABLE IF NOT EXISTS motherboard (name varchar(50), chipset nvarchar(50), socket nvarchar(50), ram_type nvarchar(50), ram_speed nvarchar(50), ram_capacity nvarchar(50), ram_slots nvarchar(50), price nvarchar(50), primary key(name))")

    with open('motherboard.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=',')    # reading the csv file motherboard
        for line in reader:
            cursor.execute("INSERT INTO motherboard (name,chipset,socket,ram_type,ram_speed,ram_capacity,ram_slots,price)" \
                            "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (line['name'], line['chipset'], line['socket'], line['ram_type'], line['ram_speed'], line['ram_capacity'], line['ram_slots'], line['price']))
                            # inserting the values of the csv into the specified database table collumns for motherboard.csv
    cnx.commit()    # commiting changest to the table and database

    print("DATABASE created")

while True:
    print("-------------------------")
    print("1. available motherboards.")
    print("2. List the viable motherboards, ram combinations.")
    print("3. A view of processors using the intel 1200 socket.")
    print("4. List compatible ram and cpu according to type to a motherboard.")
    print("5. average price of motherboards in database.")
    print("Q. Quit.")
    print("-------------------------")
    action = input("Please choose one option:")

    if action == '1':
        cursor.execute("SELECT name FROM motherboard")  # return the names of the motherboars
        print("motherboards\n-------------------------")
        for x in cursor:
            print(str(x).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
        os.system('pause')
    elif action == '2':     # JOIN
        cursor.execute("SELECT motherboard.name, ram.name FROM motherboard INNER JOIN ram ON motherboard.ram_type = ram.ram_type;")      # select the motherboard and ram names as attributes and append their intersection where the ram_types correspond, into a new table of sorts.  
        print("compatible ram combinations for all motherboards\n---------------------------------")
        for x in cursor:
            print("motherboard:", str(x).replace("(", "").replace(")", "").replace("'", "").replace(",", ", ram:"))
        os.system('pause')
    elif action == '3':
        cursor.execute("DROP VIEW IF EXISTS computer_parts.socket")     # have to DROP the table since CREATE OR ALTER didn't work.
        cursor.execute("CREATE VIEW socket as select brand, model FROM cpu WHERE cpu.socket='Intel 1200'")      # Create a VIEW ie a table of the brand and model from the cpu where the socket is intel 1200
        cursor.execute("SELECT * FROM socket")
        for x in cursor: 
            print(str(x).replace("(", "").replace(")", "").replace("'", "")) 
        os.system('pause')
    elif action == '4':
        mobo = input("motherboard name: ")
        cursor.execute("SELECT socket, ram_type FROM motherboard WHERE name='%s'" % mobo)       # get the socket and ram type of motherboard
        info = cursor.fetchall()
        for x in info:
            socket = x[0]
            type = x[1]
        # print(socket, type)

        cursor.execute("SELECT cpu.model, ram.name FROM cpu, ram WHERE cpu.socket='%s' AND ram.ram_type='%s'" % (socket, type))     # get the compatible cpu models and ram.
        print("compatible cpu and ram combinations for '%s'\n---------------------------------" % mobo)
        for x in cursor:
            print(str(x).replace("(", "").replace(")", ""))
        os.system('pause')
    elif action == '5':
        cursor.execute("SELECT AVG(price) FROM motherboard")    # average price of motherboards in the databaase
        print(str(cursor.fetchall()).replace("(", "").replace(")", "").replace("'", "").replace(",", "").replace("'", "").replace("[", "").replace("]", ""), "kr")
        os.system('pause')
    elif action == 'Q' or 'q':
        quit()  # quit
    else:
        print("invalid input!")