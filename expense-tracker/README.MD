# Expense Tracker

A Flask + MySQL web application for tracking personal expenses.

## Features

- User registration and secure login
- Add, view, and delete expenses
- Dashboard with total spending summary
- Category-based expense breakdown
- Monthly expense trends

---

## After Downloading (from ZIP)

1. **Extract** the ZIP file to a folder of your choice.

2. **Start MySQL Server** — ensure the service is running.

3. **Create a `.env` file** — copy `.env.example` and fill in your MySQL
   password:

   ```bash
   copy .env.example .env        # Windows
   # or
   cp .env.example .env           # macOS / Linux
   ```

   Then edit `.env` and set `DB_PASSWORD` to your actual MySQL root password.
   Leave it empty only if your MySQL root user has no password.

4. **Run the setup script:**

   ```bash
   python setup.py
   ```

   This will create a virtual environment, install dependencies, create the
   database, and start the Flask server automatically.

5. **Open** `http://127.0.0.1:5000` in your browser.

> **Note:** `setup.py` imports `mysql-connector-python` in the system Python.
> If you see `ModuleNotFoundError: No module named 'mysql.connector'`, run
> `pip install mysql-connector-python` and then re-run `python setup.py`.

---

## Prerequisites

Install the following before running the project:

| Requirement | Minimum Version | Download |
|---|---|---|
| Python | 3.8+ | https://python.org |
| MySQL Server | 8.0+ (or MariaDB 10.3+) | https://dev.mysql.com/downloads/ |

---

## Project Structure

```
expense-tracker/
├── app.py              # Main Flask application (routes & views)
├── auth.py             # User registration and login logic
├── expenses.py         # Expense CRUD operations
├── analytics.py        # Dashboard data queries
├── database.py         # MySQL connection helper
├── config.py           # Database configuration (environment variables)
├── setup.py            # Automated setup script (venv + DB + server)
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment variable file
├── database/
│   └── schema.sql      # Database schema (CREATE TABLE statements)
└── templates/
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── add_expense.html
    └── transactions.html
```

The `setup.py` script automates the entire setup:

1. Creates a Python virtual environment
2. Installs all dependencies from `requirements.txt`
3. Creates the MySQL database and tables
4. Starts the Flask development server

### Steps

1. **Start your MySQL server.**

2. **Create a `.env` file** with your MySQL credentials (see
   [Configuration](#configuration)).

3. **Run the setup script:**

   ```bash
   python setup.py
   ```

4. Open `http://127.0.0.1:5000` in your browser.

---

## Quick Start (Manual)

If you prefer to set things up manually:

1. **Install dependencies (optionally in a virtual environment):**

   ```bash
   python -m venv venv
   source venv/bin/activate     # macOS / Linux
   # OR
   venv\Scripts\activate          # Windows
   pip install -r requirements.txt
   ```

2. **Create a `.env` file** with your MySQL credentials (see
   [Configuration](#configuration)).

3. **Create the database and tables:**

   Start your MySQL client and run:

   ```sql
   CREATE DATABASE expense_tracker;
   USE expense_tracker;
   SOURCE database/schema.sql;
   ```

4. **Start the Flask server:**

   ```bash
   python app.py
   ```

5. Open `http://127.0.0.1:5000`.

---

## Configuration

The application reads database settings from a `.env` file in the project root
(via `config.py`) or from environment variables. No credentials are stored in
source code.

| Variable       | Default             | Description            |
|---|---|---|
| `DB_HOST`      | `localhost`         | MySQL server hostname  |
| `DB_USER`      | `root`              | MySQL username         |
| `DB_PASSWORD`  | _(empty)_           | MySQL password         |
| `DB_NAME`      | `expense_tracker`   | Database name          |

### Setting credentials

The easiest way is to create a `.env` file by copying the example:

```bash
copy .env.example .env        # Windows
cp .env.example .env           # macOS / Linux
```

Then edit `.env` and fill in your MySQL root password. The `config.py` script
loads `.env` automatically — no additional packages required.

**Alternatively**, set environment variables manually:

**Windows (PowerShell):**

```powershell
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="your_mysql_password"
$env:DB_NAME="expense_tracker"
```

**Windows (Command Prompt):**

```cmd
set DB_HOST=localhost
set DB_USER=root
set DB_PASSWORD=your_mysql_password
set DB_NAME=expense_tracker
```

**macOS / Linux:**

```bash
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=your_mysql_password
export DB_NAME=expense_tracker
```

> **Security:** Never commit the `.env` file to version control. The included
> `.gitignore` excludes it.


---

## Database Schema

### `users`

| Column     | Type         | Description            |
|------------|--------------|------------------------|
| id         | INT AI PK    | Unique user ID         |
| name       | VARCHAR(100) | User name              |
| email      | VARCHAR(100) | Unique email           |
| password   | VARCHAR(255) | User password          |
| created_at | TIMESTAMP    | Account creation time  |

### `expenses`

| Column       | Type          | Description                |
|--------------|---------------|----------------------------|
| id           | INT AI PK     | Unique expense ID          |
| user_id      | INT FK        | References `users.id`      |
| title        | VARCHAR(100)  | Expense title              |
| amount       | DECIMAL(10,2) | Expense amount             |
| category     | VARCHAR(50)   | Category                   |
| expense_date | DATE          | Date of expense            |
| description  | VARCHAR(255)  | Optional description       |

The full schema is in `database/schema.sql`.

---

## Running the Application

After initial setup, you can run the app directly:

**Windows:**

```powershell
venv\Scripts\Activate.ps1
python app.py
```

**macOS / Linux:**

```bash
source venv/bin/activate
python app.py
```

> If PowerShell blocks activation, run:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
> ```

The app runs in debug mode at `http://127.0.0.1:5000`. Press `Ctrl+C` to
stop the server.

---

## Troubleshooting

### "Can't connect to MySQL server"

- Ensure MySQL Server is running:
  - **Windows:** Check Services (`services.msc`) for `MySQL80`.
  - **macOS:** `brew services start mysql`
  - **Linux:** `sudo systemctl start mysql`
- Verify your credentials in `config.py` or environment variables.
- Confirm the host and port (default: `localhost:3306`).

### "Unknown database 'expense_tracker'"

Run `python setup.py` to create the database automatically, or run the
SQL commands in the [Manual Setup](#quick-start-manual) section.

### `ModuleNotFoundError: No module named 'mysql.connector'`

`setup.py` now auto-installs `mysql-connector-python` in the system Python if it
is missing. If the error persists, install manually:

```bash
pip install mysql-connector-python
```

### Flask port 5000 is already in use

Stop the conflicting process, or change the port in `app.py`:

```python
app.run(debug=True, port=5001)
```

### Virtual environment activation fails (PowerShell)

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
venv\Scripts\Activate.ps1
```

---

## Sharing This Project

When zipping and sharing this project with others:

1. **Exclude the `venv/` directory** — it is large and machine-specific.
   Recreate it with `python -m venv venv` on the destination machine.
2. **Exclude any `.env` file** — it may contain personal credentials.
3. **Verify no credentials in source** — `config.py` loads credentials from
   the `.env` file (not from source code). `setup.py` does not hardcode any
   passwords.
4. **Include** `requirements.txt`, `database/schema.sql`, `config.py`,
   `setup.py`, `app.py`, `auth.py`, `expenses.py`, `analytics.py`,
   `database.py`, `templates/`, and `.env.example`.
