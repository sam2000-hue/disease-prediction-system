from os import name
import sqlite3
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()

#patient database section


def create_table():

    c.execute('CREATE TABLE IF NOT EXISTS Patientstable2(name TEXT,id TEXT NOT NULL PRIMARY KEY,diabetis TEXT,heart TEXT,parkinsons TEXT,Hospital TEXT,date DATE, county TEXT, UNIQUE(id,date))')


def add_data(name,id,diabetis,heart,parkinsons,Hospital,date,county):
    c.execute('INSERT INTO Patientstable2(name,id,diabetis,heart,parkinsons,Hospital,date,county) VALUES(?,?,?,?,?,?,?,?)',(name,id,diabetis,heart,parkinsons,Hospital,date,county))
    conn.commit()
    

def view_all_data():
    c.execute('SELECT * FROM Patientstable2')
    data = c.fetchall()
    return data

def view_unique_name():
    c.execute('SELECT DISTINCT id FROM Patientstable2')
    data = c.fetchall()
    return data

def get_name(id):
    c.execute('SELECT * FROM Patientstable2 WHERE  id="{}"'.format(id))
    data = c.fetchall()
    return data



def edit_patient_data(new_name,new_id,new_diabetis,new_heart,new_parkinsons,new_Hospital,new_date,name,id,diabetis,heart,parkinsons,Hospital,date):
    c.execute("UPDATE Patientstable2 SET name = ?,id=?,diabetis=?,heart=?,parkinsons=?,Hospital=?,date=? WHERE name = ? and id=? and diabetis=? and heart=? and parkinsons=? and Hospital=? and date=?",(new_name,new_id,new_diabetis,new_heart,new_parkinsons,new_Hospital,new_date,name,id,diabetis,heart,parkinsons,Hospital,date))
    conn.commit()
    data = c.fetchall()
    return data

def delete_data(name):
	c.execute('DELETE FROM Patientstable2 WHERE name="{}"'.format(name))
	conn.commit()


    #authentication section

def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS authtable(username TEXT,password TEXT,email TEXT NOT NULL PRIMARY KEY,regno TEXT, authstatus TEXT, UNIQUE(email,regno))')

def add_userdata(username,password,email,regno,authstatus):

    c.execute('INSERT INTO authstable(username,password,email,regno,authstatus ) VALUES(?,?,?,?,?)',(username,password,email,regno,authstatus))

    conn.commit()
def login_user(username,password,authstatus):
    c.execute('SELECT * FROM authstable WHERE username =? AND password =? AND authstatus=?',(username,password,authstatus))
    data = c.fetchall()
    return data
def view_allusers():
    c.execute('SELECT username,email,regno,authstatus FROM authstable')
    data = c.fetchall()
    return data
def view_user(username):
    c.execute('SELECT * FROM authstable WHERE username="{}"'.format(username))
    data = c.fetchall()
    return data
def edit_userprofile(update_user,update_email,username,email):
    c.execute('UPDATE authstable SET username=?,email=? WHERE username = ? and email = ?',(update_user,update_email,username,email))
    conn.commit()
    data = c.fetchall()
    return data
def edit_userpassword(updated_password,password):
    c.execute('UPDATE authstable SET password = ? WHERE password = ?',(updated_password,password))
    conn.commit()
    data = c.fetchall()
    return data

def view_unique_user():
    c.execute('SELECT DISTINCT email FROM authstable')
    data = c.fetchall()
    return data
def get_authname(email):
    c.execute('SELECT * FROM authstable WHERE email="{}"'.format(email))
    data = c.fetchall()
    return data
def edit_authstatus(updated_authstatus,updated_email,authstatus,email):
    c.execute('UPDATE authstable SET authstatus = ?,email =? WHERE authstatus = ? and email =?',(updated_authstatus,updated_email,authstatus,email))
    conn.commit()
    data = c.fetchall()
    return data
def delete_user(email):
	c.execute('DELETE FROM authstable WHERE email="{}"'.format(email))
	conn.commit()