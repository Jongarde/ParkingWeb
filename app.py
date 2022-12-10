import mysql.connector as con
from mysql.connector import errorcode


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

#TO-DO: Incomplete method for registration(more verifications and INSERT query with mySQL)
def registerEmployee(dni, name, mail, pw, pw_conf):
    db = mysqlConnexion()
    mycursor = db.cursor()
    registerable = True
    if(pw != pw_conf):
        registerable = False
    return 0

#TO-DO: Login method
def loginEmployee(dni, pw):
    return 0