#!/usr/bin/env python

import MySQLdb
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/something")
def something():
    return "Were you looking for something?"

@app.route("/db")
def databasetest():

    db = MySQLdb.connect(host="mariadb-node-portdefault.svc.cluster.local",
                        user="test_user", 
                        passwd="test_pass",
                        db="test_db") 
    if db:
        db_output = "because the database connection works!"
    else:
        db_output = "db connection broke"

    return db_output

if __name__ == "__main__":
    app.run()

