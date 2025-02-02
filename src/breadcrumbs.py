from flask import request

def setup_breadcrumbs(app, honeypot):
    @app.route('/hidden_path')
    def hidden_path():
        honeypot.log_alert(f'Breadcrumb path accessed from {request.remote_addr}')
        return "<h1>Nothing to see here!</h1><p>Check out our <a href='/robots.txt'>site rules</a>.</p>"

    @app.route('/robots.txt')
    def robots():
        honeypot.log_alert(f'robots.txt accessed from {request.remote_addr}')
        response = "User-agent: *\nDisallow: /admin\nDisallow: /honeytokens/secret_credentials.txt"
        return response, 200, {'Content-Type': 'text/plain'}
