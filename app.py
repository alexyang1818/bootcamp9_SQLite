# import the flask dependency

from flask import Flask

# create a new Flask app instance called 'app'

app = Flask(__name__) # magic methods

# creat Flask routes

## define starting point or root

@app.route('/')  # put data at the root of our routes
def hello_workd(): # create a function right below the route
    # return 'Hello World'
    return str(1+3)
