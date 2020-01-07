#!/usr/bin/env python3

import MySQLdb
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def databasetest():

    db_output = "OFFLINE"
    try:
        db = MySQLdb.connect(host="mariadb-clusterip",
                            user="test_user", 
                            passwd="test_pass",
                            db="test_db") 
        if db:
            db_output = "ONLINE"
    except:
        pass

    return render_template('index.html', variable=db_output)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)