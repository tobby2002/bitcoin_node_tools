from flask import Flask

app = Flask(__name__)

# This is actually a bit weird but if it was imported at the top
# it would create a circular import
from logreader import routes

# Enable the line below so the flask site is available across local network
# app.run(host='0.0.0.0')
