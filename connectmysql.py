#!/usr/bin/python
import MySQLdb

db = MySQLdb.connect(host="localhost",port =3306,user="root",db="inspiringquotes",charset='utf8')

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# Use all the SQL you like
cur.execute("SELECT * FROM list_link limit 20")

# print all the first cell of all the rows
for row in cur.fetchall():
    print row[1]


