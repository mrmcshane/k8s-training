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
    some_variable = "put some database test string here and return the values"
    if some_variable:
        db_output = some_variable + "<br> because the database connection works!"
    else:
        db_output = "db connection broke"

    return db_output

if __name__ == "__main__":
    app.run()

