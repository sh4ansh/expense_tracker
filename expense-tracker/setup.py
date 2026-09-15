import os
import sys
import time
import urllib.request
import webbrowser
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
    import mysql.connector
except ImportError:
    print("\nInstalling mysql-connector-python for system Python...")
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "mysql-connector-python"
    ])
    import mysql.connector

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


# --------------------------------
# Create virtual environment
# --------------------------------

if not os.path.exists("venv"):
    print("\nCreating virtual environment...")

    subprocess.check_call([
        sys.executable,
        "-m",
        "venv",
        "venv"
    ])

    print("Virtual environment created.")


# --------------------------------
# Find virtual environment Python
# --------------------------------

if os.name == "nt":
    python_path = os.path.join(
        "venv",
        "Scripts",
        "python.exe"
    )
else:
    python_path = os.path.join(
        "venv",
        "bin",
        "python"
    )


# --------------------------------
# Install requirements
# --------------------------------

print("\nInstalling required libraries...")

subprocess.check_call([
    python_path,
    "-m",
    "pip",
    "install",
    "-r",
    "requirements.txt"
])

print("Libraries installed.")


# --------------------------------
# Connect to MySQL
# --------------------------------

print("\nConnecting to MySQL...")

try:

    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )

    cursor = connection.cursor()

    print("MySQL connection successful.")


except mysql.connector.Error as error:

    print("\nCould not connect to MySQL.")
    print("Make sure MySQL Server is running.")
    print("Error:", error)

    sys.exit(1)


# --------------------------------
# Create database
# --------------------------------

print("\nCreating database...")

cursor.execute(
    f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"
)

print(f"Database '{DB_NAME}' is ready.")


# --------------------------------
# Select database
# --------------------------------

cursor.execute(
    f"USE {DB_NAME}"
)


# --------------------------------
# Read schema.sql
# --------------------------------

print("\nCreating tables...")

with open(
    os.path.join("database", "schema.sql"),
    "r"
) as file:

    sql = file.read()


# Remove CREATE DATABASE and USE statements
# because database is already selected

statements = sql.split(";")

for statement in statements:

    statement = statement.strip()

    if not statement:
        continue

    if statement.upper().startswith("CREATE DATABASE"):
        continue

    if statement.upper().startswith("USE "):
        continue

    cursor.execute(statement)


connection.commit()

cursor.close()
connection.close()

print("Tables created successfully.")


# --------------------------------
# Start Flask
# --------------------------------

print("\nStarting Expense Tracker...")
print("Opening http://127.0.0.1:5000 in your browser...")
print("\nPress CTRL+C to stop the server.\n")

project_dir = os.path.dirname(os.path.abspath(__file__))
app_url = "http://127.0.0.1:5000"

app_process = subprocess.Popen(
    [python_path, "app.py"],
    cwd=project_dir
)

server_ready = False

for _ in range(30):
    if app_process.poll() is not None:
        print("Flask server stopped before it could start.")
        sys.exit(app_process.returncode)

    try:
        with urllib.request.urlopen(app_url, timeout=1) as response:
            if response.status == 200:
                server_ready = True
                break
    except Exception:
        time.sleep(1)

if not server_ready:
    print("The server did not start in time.")
    app_process.terminate()
    sys.exit(1)

webbrowser.open(app_url)

try:
    app_process.wait()
except KeyboardInterrupt:
    app_process.terminate()
    app_process.wait()
