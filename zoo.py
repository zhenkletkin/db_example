'''
    My first experience on working with:
    1. Simple DP-API
    2. SQLAlcemy Driver
    3. SQLAlchemy Expression Language
    4. SQLAlchemy ORM
'''

#DB-API is a standart API in python for working with different databases
#main methods are connect, cursor, execute, executemany, fetchone, fetchmany, fetchall
#all next modules suit DB-API, but some of them have their own extensions or defference in details


#SQLlite holds databases in files. These files can be transfered to other systems, which makes SQLite a good decision for creating a simple database
import sqlite3
conn = sqlite3.connect('enterprise.db')
curs = conn.cursor()
curs.execute('''CREATE TABLE zoo(
    critter VARCHAR(20) PRIMARY KEY,
    count INT,
    damages FLOAT
)''')
curs.execute('INSERT INTO zoo VALUES("duck",5,0.0)')

#there's a more safe way for adding values
ins = 'INSERT INTO zoo VALUES(?,?,?)'
curs.execute(ins, ('bear',2,1000.0))
curs.execute(ins, ('weasel',1,2000))
result = curs.execute('SELECT critter FROM zoo')
critters = result.fetchall()
print('The following example has been created by DB_API')
print('In our zoo you can see:')
for num,critter_info in enumerate(critters,1):
    critter, = critter_info
    print('\t',num,critter)

#In the end we should close cursor and connection
curs.close()
conn.close()

#MySQL is a real server, so anyone can access it
#PostgreSQL is more advanced MySQL

#SQL is not the same in all databases. Each one has its own features
#Many libraries try to compensate the difference between databases and SQLAlchemy is the most popular one

#one can use SQLAlcheny on 3 level
#low level is similar to DB-API
#middle level - SQL Expression Language
#high level - ORM (Object-Relational Mapper)

#SQLAlchemy works with database drivers. We don't need to import driver. It will be defined in connection string
#   dialect + driver :// user : password @ host : port / dbname

#let's take a first look at the low level
#The following examples are about sqlite
#SQLlite let us leave driver, user, password, host and port fields.
#dbname tells Python which file to hold databases in
#if we leave dbname, Python will create database in memory

import sqlalchemy as sa
conn = sa.create_engine('sqlite://') #in memory
# 'sqlite://:memory:' will work as well
#here we don't need to create cursor
conn.execute('''CREATE TABLE zoo(
    critter VARCHAR(20) PRIMARY KEY,
    count INT,
    damages FLOAT
)''')
ins = 'INSERT INTO zoo VALUES(?,?,?)'
conn.execute(ins, ('duck', 5, 0.0)) #without brackets!
conn.execute(ins, ('bear',2,1000.0))
conn.execute(ins, ('weasel' ,1,2000))
rows = conn.execute('SELECT * FROM zoo ORDER BY damages DESC') #we don't need fetch.. anymore
print("")
print('This example has been created with low level syntax of SQLAlchemy library')
for critter, count, damages in rows:
    print('The damages on', critter, 'are', damages)
print('')

#low level SQLAlchemy syntax looks pretty similar to DB-API. The advantage of this method is that we don't need to import driver...
#SQLAlcemy itself defines driver from connecting string. And any change in connecting string lets us transfer this code to another database

#next level is SQL Expression Language (EL for short)
#EL can process more differences in dialects than low level can

#first we do all things we did before

import sqlalchemy as sa
conn = sa.create_engine('sqlite://')

#to define table zoo, instead of SQL we use Expression Language
meta = sa.MetaData()
zoo = sa.Table('zoo', meta,
    sa.Column('critter', sa.String, primary_key=True),
    sa.Column('count', sa.Integer),
    sa.Column('damages', sa.Float))
meta.create_all(conn)
#zoo presents a object, which connects the world of SQL databases with the world of Python structures

conn.execute(zoo.insert(('duck',5,0.0)))
conn.execute(zoo.insert(('bear', 2, 1000.0)))
conn.execute(zoo.insert(('weasel', 1, 2000.0)))
result = conn.execute(zoo.select())
rows = result.fetchall()
print("")
print('This example has been created with SQL Expression Language')
for critter,count,damages in rows:
    print('for {} we have {} inventory items'.format(critter, count))
print('')

#In previous example 'zoo' object was something between Python and SQL
#ORM (Object-Relational Mapper) also uses Expression Language but tries to make all database mechanisms invissible
#The main idea of ORM is that we can use objects and refer to them in code as we usually do in Python whilst using database
#we'll define class Zoo and bind it to ORM
#this time we use zoo.db to make sure ORM works

#import sqlalchemy as we've already done twice
from sqlalchemy.ext.declarative import declarative_base

#create a connection
conn = sa.create_engine('sqlite:///zoo.db')
Base = declarative_base()

#now we're creating a class Zoo (inherits from Base parent)
class Zoo(Base):
    __tablename__ = 'another_zoo'
    #this Class' attributes will be the collumns of our future table
    citter = sa.Column('critter', sa.String, primary_key = True)
    count = sa.Column('count', sa.Integer)
    damages = sa.Column('damages', sa.Float)
    def __init__(self, critter, count, damages):
        self.critter = critter
        self.count = count
        self.damages = damages
    def __str__(self):
        return "<Zoo({}, {}, {})>".format(self.critter, self.count, self.damages)
#this line of code will create our database and table
Base.metadata.create_all(conn)

#we can add new values to table by creating Python objects. ORM manages data
first = Zoo('duck', 3, 0.0)
second = Zoo('bear',2,1000.0)
third = Zoo('weasel', 1, 2000.0)
print('Just checking if __str__ method works', third)
print('')

#to start talking to database we need to create a session
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=conn)
session = Session()

#so to insert our objects into table we use add method for one object and add_all for some
session.add(first)
session.add_all([second,third])

#finally we need to close session
print('Wanna see if it works?')
print('type "sqlite3 zoo.db" in cmd (you need "sqlite3" installed )')
print('')
print('')

sqlite3_example='''
$ sqlite3 zoo.db
SQLite version 3.6.12
Enter ".help" for instructions
Enter SQL statements terminated with a ";"
sqlite> .tables
zoo
sqlite> select * from zoo;
duck|10|0.0
bear|2|1000.0
weasel|1|2000.0
'''

print('')
print(sqlite3_example)

#You should decide which of the above method/s to use
#Don't think that now you know everything about database and try to use simple SQL expressions
