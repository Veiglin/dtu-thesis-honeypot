import unittest
from flask import Flask
from breadcrumbs import setup_breadcrumbs

class TestBreadcrumbs(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.honeypot = HoneypotMock()
        setup_breadcrumbs(self.app, self.honeypot)
        self.client = self.app.test_client()

    def test_hidden_path(self):
        response = self.client.get('/hidden_path')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Nothing to see here!', response.data)
        self.assertTrue(self.honeypot.alert_logged)

    def test_robots_txt(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User-agent: *', response.data)
        self.assertIn(b'Disallow: /admin', response.data)
        self.assertIn(b'Disallow: /honeytokens/secret_credentials.txt', response.data)
        self.assertEqual(response.content_type, 'text/plain')
        self.assertTrue(self.honeypot.alert_logged)

class HoneypotMock:
    def __init__(self):
        self.alert_logged = False

    def log_alert(self, message):
        self.alert_logged = True

if __name__ == '__main__':
    unittest.main()