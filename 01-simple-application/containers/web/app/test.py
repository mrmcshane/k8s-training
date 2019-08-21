#!/usr/bin/env python3

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def databasetest():

    return render_template('index.html', variable='RUNNING')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)