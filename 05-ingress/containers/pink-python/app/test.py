#!/usr/bin/env python3

import MySQLdb
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def databasetest():

    db_pink = "OFFLINE"
    try:
        db = MySQLdb.connect(host="pink-mariadb-clusterip",
                            user="test_user", 
                            passwd="test_pass",
                            db="test_db") 
        if db:
            db_pink = "ONLINE"
    except:
        pass


    return render_template('index.html', pink=db_pink)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)