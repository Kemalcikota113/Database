import mysql.connector  # importing the mysql - python connector
import csv  # import the csv lib
import os

cnx = mysql.connector.connect(user='root', password='seaweedZX02!',
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

    cursor.execute("CREATE TABLE IF NOT EXISTS ram (brand nvarchar(50), capacity nvarchar(50), speed nvarchar(50), ram_type nvarchar(50), artNR varchar(50), primary key(artNR))")

    with open('ram.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=',')    # reading the csv file ram
        for line in reader:
            cursor.execute("INSERT INTO ram (brand,capacity,speed,ram_type,artNR)" \
                            "VALUES('%s', '%s', '%s', '%s', '%s')" % (line['brand'], line['capacity'], line['speed'], line['ram_type'], line['artNR']))
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
    print("1. What motherboards support DDR4.")
    print("2. List the motherboards and corresponding chipset.")
    print("3. A view of processors using the AMD AM4 socket")
    print("4. List compatible cpu's to a motherboard.")
    print("5. ")
    print("Q. Quit")
    print("-------------------------")
    action = input("Please choose one option:")

    if action == '1':
        cursor.execute("SELECT name FROM motherboard WHERE ram_type='DDR4';")
        print("motherboards\n-------------------------")
        for x in cursor:
            print(str(x).replace("(", "").replace(")", "").replace(",", "").replace("'", ""))
        os.system('pause')
    elif action == '2':
        cursor.execute("SELECT name, chipset FROM motherboard;")
        for x in cursor:
            print(str(x).replace("(", "").replace(")", "").replace("'", ""))
        os.system('pause')
    elif action == '3':
        cursor.execute("DROP VIEW IF EXISTS computer_parts.socket")
        cursor.execute("CREATE VIEW socket as select brand, model FROM cpu WHERE cpu.socket='Intel 1200'");
        cursor.execute("SELECT * FROM socket");
        for x in cursor: 
            print(str(x).replace("(", "").replace(")", "").replace("'", "")) 
        os.system('pause')
    elif action == '4':
        mobo = input("motherboard name: ")
        cursor.execute("SELECT ")

        os.system('pause')
    elif action == '5':
        continue
    elif action == 'Q':
        quit()  # quit
    else:
        print("invalid input!")