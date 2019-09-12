#!/usr/bin/env python3

import MySQLdb
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def databasetest():

    db_blue = "OFFLINE"
    try:
        db = MySQLdb.connect(host="mariadb-clusterip.blue",
                            user="test_user", 
                            passwd="test_pass",
                            db="test_db") 
        if db:
            db_blue = "ONLINE"
    except:
        pass

    db_green = "OFFLINE"
    try:
        db = MySQLdb.connect(host="mariadb-clusterip.green",
                            user="test_user", 
                            passwd="test_pass",
                            db="test_db") 
        if db:
            db_green = "ONLINE"
    except:
        pass

    return render_template('index.html', blue=db_blue, green=db_green)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)