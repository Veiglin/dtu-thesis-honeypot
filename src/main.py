import os
from flask import Flask
from honeypot_server import Honeypot
from breadcrumbs import setup_breadcrumbs

app = Flask(__name__)

# Initialize and start the honeypot
honeypot = Honeypot(app)
honeypot.start()

# Setup breadcrumbs leading to robots.txt as a honeytoken
setup_breadcrumbs(app, honeypot)

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    