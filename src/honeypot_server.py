from flask import Flask, request, render_template_string, redirect, url_for
from utils.logging import setup_logging
import random
import datetime

# Initialize Flask app
app = Flask(__name__)

# Setup logging
logger = setup_logging()

# Define breadcrumbs and honeytokens
#BREADCRUMBS = ['/admin', '/config', '/backup']
#HONEYTOKENS = ['/secret.txt', '/.env', '/credentials.json']

# Fake system data
fake_configs = {
    'database': 'mysql://user:password@localhost:3306/db',
    'cache': 'redis://localhost:6379/0',
    'api_key': 'ABC123-FAKE-KEY'
}

fake_backup_files = [
    'backup_2025_01_01.tar.gz',
    'backup_2025_01_02.tar.gz',
    'backup_2025_01_03.tar.gz'
]

# Helper to simulate fake system logs
def generate_fake_log():
    levels = ['INFO', 'WARNING', 'ERROR', 'DEBUG']
    messages = [
        "Service started successfully.",
        "User session established.",
        "Configuration file loaded.",
        "Unexpected input detected.",
        "Database connection established.",
        "Cache miss on key 'user:123'.",
        "Security module activated."
    ]
    level = random.choice(levels)
    message = random.choice(messages)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"{timestamp} [{level}] {message}"

@app.route('/')
def home():
    client_ip = request.remote_addr
    logger.info(f"Home page accessed from {client_ip}")
    # Return a fake login page to lure attackers into interacting with the system.
    login_page = """
    <html>
      <head><title>Login - Secure System</title></head>
      <body>
        <h2>Welcome to SecureCorp System</h2>
        <form action="/login" method="post">
          <label for="username">Username:</label><br>
          <input type="text" id="username" name="username"><br>
          <label for="password">Password:</label><br>
          <input type="password" id="password" name="password"><br><br>
          <input type="submit" value="Login">
        </form>
      </body>
    </html>
    """
    return render_template_string(login_page)

@app.route('/login', methods=['POST'])
def login():
    client_ip = request.remote_addr
    username = request.form.get('username', 'unknown')
    # Log the attempted login for further analysis
    logger.warning(f"Login attempt by {username} from {client_ip}")
    # Redirect to the admin page regardless of credentials to maintain deception
    return redirect(url_for('admin'))

@app.route('/admin', methods=['GET'])
def admin():
    client_ip = request.remote_addr
    logger.info(f"Admin dashboard accessed from {client_ip}")
    logger.warning(f"Breadcrumb accessed: {request.path} by {client_ip}")
    # Show a fake admin dashboard with system information and fake logs
    logs = "<br>".join(generate_fake_log() for _ in range(5))
    admin_page = f"""
    <html>
      <head><title>Admin Dashboard</title></head>
      <body>
        <h2>Admin Dashboard</h2>
        <p>Welcome, administrator!</p>
        <h3>System Logs:</h3>
        <div style='background-color:#f4f4f4; padding:10px;'>{logs}</div>
        <p><a href="/config">View System Configuration</a></p>
        <p><a href="/backup">View Backup Files</a></p>
      </body>
    </html>
    """
    return render_template_string(admin_page)

@app.route('/config', methods=['GET'])
def config():
    client_ip = request.remote_addr
    logger.info(f"Configuration page accessed from {client_ip}")
    logger.warning(f"Breadcrumb accessed: {request.path} by {client_ip}")

    config_content = "<br>".join([f"{key}: {value}" for key, value in fake_configs.items()])
    config_page = f"""
    <html>
      <head><title>System Configuration</title></head>
      <body>
        <h2>System Configuration</h2>
        <div style='background-color:#e8e8e8; padding:10px;'>{config_content}</div>
        <p><a href="/">Back to Home</a></p>
      </body>
    </html>
    """
    return render_template_string(config_page)

@app.route('/backup', methods=['GET'])
def backup():
    client_ip = request.remote_addr
    logger.info(f"Backup page accessed from {client_ip}")
    logger.warning(f"Breadcrumb accessed: {request.path} by {client_ip}")
    backup_content = "<br>".join(fake_backup_files)
    backup_page = f"""
    <html>
      <head><title>Backup Files</title></head>
      <body>
        <h2>Available Backup Files</h2>
        <div style='background-color:#e8e8e8; padding:10px;'>{backup_content}</div>
        <p><a href="/">Back to Home</a></p>
      </body>
    </html>
    """
    return render_template_string(backup_page)

# Honeytoken endpoints: if these are accessed, log at an error level to mark suspicious behavior
@app.route('/secret.txt', methods=['GET'])
@app.route('/.env', methods=['GET'])
@app.route('/credentials.json', methods=['GET'])
def honeytoken():
    client_ip = request.remote_addr
    logger.error(f"Honeytoken accessed: {request.path} by {client_ip}")
    return "Access denied!", 403

# Catch-all route for any additional paths that mimic file/directory browsing
@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    client_ip = request.remote_addr
    full_path = "/" + path
        
    # For all other paths, simulate a realistic directory or file response.
    logger.info(f"Unknown path accessed: {full_path} by {client_ip}")
    simulated_response = f"""
    <html>
      <head><title>File Not Found</title></head>
      <body>
        <h2>Error 404: Not Found</h2>
        <p>The requested resource {full_path} was not found on this server.</p>
        <p><em>{generate_fake_log()}</em></p>
        <p><a href="/">Return Home</a></p>
      </body>
    </html>
    """
    return render_template_string(simulated_response), 404

if __name__ == '__main__':
    # Run the Flask app in debug mode if needed (for development); in production, consider a proper WSGI server.
    app.run(host='127.0.0.1', port=5000)
