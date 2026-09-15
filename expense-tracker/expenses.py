# expenses.py

from database import get_connection


def add_expense(user_id, title, amount, category, expense_date, description):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO expenses
        (user_id, title, amount, category, expense_date, description)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (user_id, title, amount, category, expense_date, description)
    )

    connection.commit()

    cursor.close()
    connection.close()


def get_expenses(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT *
        FROM expenses
        WHERE user_id = %s
        ORDER BY expense_date DESC
    """

    cursor.execute(query, (user_id,))

    expenses = cursor.fetchall()

    cursor.close()
    connection.close()

    return expenses


def delete_expense(expense_id, user_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        DELETE FROM expenses
        WHERE id = %s AND user_id = %s
    """

    cursor.execute(query, (expense_id, user_id))

    connection.commit()

    cursor.close()
    connection.close()

def get_expense(expense_id, user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT *
        FROM expenses
        WHERE id = %s AND user_id = %s
    """

    cursor.execute(query, (expense_id, user_id))

    expense = cursor.fetchone()

    cursor.close()
    connection.close()

    return expense


def update_expense(
    expense_id,
    user_id,
    title,
    amount,
    category,
    expense_date,
    description
):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        UPDATE expenses
        SET title = %s,
            amount = %s,
            category = %s,
            expense_date = %s,
            description = %s
        WHERE id = %s AND user_id = %s
    """

    cursor.execute(
        query,
        (
            title,
            amount,
            category,
            expense_date,
            description,
            expense_id,
            user_id
        )
    )

    connection.commit()

    cursor.close()
    connection.close()