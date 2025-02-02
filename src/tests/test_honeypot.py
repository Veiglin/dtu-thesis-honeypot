import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from honeypot import Honeypot

class TestHoneypot(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.honeypot = Honeypot(self.app)
        self.client = self.app.test_client()

    @patch('honeypot.logging.info')
    def test_honeytokens_route(self, mock_logging_info):
        response = self.client.get('/honeytokens/secret_credentials.txt')
        self.assertEqual(response.status_code, 200)
        mock_logging_info.assert_called_with('Honeytoken accessed: secret_credentials.txt from 127.0.0.1')

    @patch('honeypot.logging.info')
    def test_index_route(self, mock_logging_info):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to our site!', response.data)

    @patch('honeypot.logging.info')
    def test_admin_route(self, mock_logging_info):
        response = self.client.get('/admin')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Panel', response.data)
        mock_logging_info.assert_called_with('Admin page accessed from 127.0.0.1')

    @patch('honeypot.logging.info')
    def test_log_alert(self, mock_logging_info):
        self.honeypot.log_alert('Test alert message')
        mock_logging_info.assert_called_with('Test alert message')

    @patch('honeypot.logging.info')
    def test_start(self, mock_logging_info):
        self.honeypot.start()
        mock_logging_info.assert_called_with('Honeypot started and ready to capture data.')

if __name__ == '__main__':
    unittest.main()