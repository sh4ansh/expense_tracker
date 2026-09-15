# auth.py

from database import get_connection


def register_user(name, email, password):
    connection = get_connection()
    cursor = connection.cursor()

    # Check if email already exists
    cursor.execute(
        "SELECT id FROM users WHERE email = %s",
        (email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        connection.close()
        return False

    # Insert new user
    query = """
        INSERT INTO users (name, email, password)
        VALUES (%s, %s, %s)
    """

    cursor.execute(query, (name, email, password))

    connection.commit()

    cursor.close()
    connection.close()

    return True


def login_user(email, password):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT id, name, email
        FROM users
        WHERE email = %s AND password = %s
    """

    cursor.execute(query, (email, password))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user