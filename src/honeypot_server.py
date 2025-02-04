import os
import logging
from flask import request, send_from_directory

class Honeypot:
    def __init__(self, app):
        self.app = app
        self.honeytokens_dir = 'honeytokens'
        self.setup_logging()
        self.create_honeytokens()
        self.setup_routes()

    def setup_logging(self):
        logging.basicConfig(filename='honeypot.log', level=logging.INFO, format='%(asctime)s %(message)s')

    def create_honeytokens(self):
        os.makedirs(self.honeytokens_dir, exist_ok=True)
        with open(os.path.join(self.honeytokens_dir, 'secret_credentials.txt'), 'w') as f:
            f.write('username: admin\npassword: 123456')

    def setup_routes(self):
        @self.app.route('/honeytokens/<path:filename>')
        def honeytokens(filename):
            logging.info(f'Honeytoken accessed: {filename} from {request.remote_addr}')
            return send_from_directory(self.honeytokens_dir, filename)

        @self.app.route('/')
        def index():
            return "<h1>Welcome to our site!</h1><p>Check our <a href='/admin'>admin panel</a>.</p>"

        @self.app.route('/admin')
        def admin():
            logging.info(f'Admin page accessed from {request.remote_addr}')
            return "<h1>Admin Panel</h1><p>Unauthorized access detected.</p>"

    def log_alert(self, message):
        logging.info(message)

    def start(self):
        logging.info('Honeypot started and ready to capture data.')