import mysql.connector as con
from mysql.connector import errorcode
import re

def mysqlConnexion():
    try:
        db = con.connect(host='localhost',
                         user='root',
                         passwd='deusto',
                         database='parkingadmins')
        mycursor = db.cursor()
        mycursor.execute("CREATE TABLE if not exists Employee (Employee_DNI VARCHAR(9) PRIMARY KEY, Employee_name VARCHAR(50), Employee_mail VARCHAR(50), Employee_pw VARCHAR(50))")
    except con.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            db = con.connect(host='localhost',
                             user='root',
                             passwd='deusto')
            db.cursor().execute("CREATE DATABASE parkingadmins")
            print("Database does not exist. We created the database for you, you must rerun the code.")
        else:
            print(err)

    return db

def registerEmployee(dni, name, mail, pw, pw_conf):
    try:
        # Variables used for register verification
        alphabet = "TRWAGMYFPDXBNJZSQVHLCKE"
        letter_idx = int(dni[:8])%23
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        registerable = True
        if(alphabet[letter_idx] != dni[8:]):
            registerable = False
            print("This DNI does not match with the pattern!")
        elif(re.fullmatch(regex, mail)==False):
            registerable = False
            print("This mail direction does not match with the pattern!")
        elif(pw != pw_conf):
            registerable = False
            print("The passwords were different!")
    
        if(registerable):
            db = mysqlConnexion()
            mycursor = db.cursor()

            mycursor.execute("INSERT INTO Employee (Employee_DNI, Employee_name, Employee_mail, Employee_pw) VALUES (%s,%s,%s,%s)", (dni, name, mail, pw))
            db.commit()

            db.close()
        else:
            print("The data that you entered could not be registered. Check the error above for further information!")
    except:
        print("""Registration process could not succeed, make sure that:
        \t-The length of the DNI is exactly 9 characters.
        \t-The length of the other inputs can't reach 50 characters.
        \t-You are not already registered.""")

def loginEmployee(dni, pw):
    db = mysqlConnexion()
    mycursor = db.cursor()

    mycursor.execute("SELECT Employee_pw FROM Employee WHERE Employee_DNI = %s", (dni, ))
    
    for e in mycursor:
        db_password = str(e)

    db.close()

    try:
        db_password = db_password[2:len(db_password)-3]
        if pw == db_password:
            return True
        else:
            return False
    except:
        print("No DNI matches with the input. Please make sure that you are registered.")

def checkDatabase():
    db = mysqlConnexion()
    mycursor = db.cursor()
    mycursor.execute("SELECT * FROM Employee")

    print("Employees registered in our database:")
    for e in mycursor:
        print(e)

    db.close()