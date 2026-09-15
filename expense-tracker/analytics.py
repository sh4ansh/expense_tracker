# analytics.py

from database import get_connection


def get_total_expense(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = %s
    """

    cursor.execute(query, (user_id,))
    total = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return total


def get_category_expenses(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT category, SUM(amount) AS total
        FROM expenses
        WHERE user_id = %s
        GROUP BY category
        ORDER BY total DESC
    """

    cursor.execute(query, (user_id,))
    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data


def get_monthly_expenses(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            DATE_FORMAT(expense_date, '%Y-%m') AS month,
            SUM(amount) AS total
        FROM expenses
        WHERE user_id = %s
        GROUP BY DATE_FORMAT(expense_date, '%Y-%m')
        ORDER BY month
    """

    cursor.execute(query, (user_id,))
    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data


def get_transaction_count(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT COUNT(*)
        FROM expenses
        WHERE user_id = %s
    """

    cursor.execute(query, (user_id,))
    count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return count


def get_current_month_expense(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = %s
        AND MONTH(expense_date) = MONTH(CURDATE())
        AND YEAR(expense_date) = YEAR(CURDATE())
    """

    cursor.execute(query, (user_id,))
    total = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return total


def get_expense_statistics(user_id):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            COALESCE(AVG(amount), 0),
            COALESCE(MAX(amount), 0),
            COALESCE(MIN(amount), 0)
        FROM expenses
        WHERE user_id = %s
    """

    cursor.execute(query, (user_id,))
    average, highest, lowest = cursor.fetchone()

    cursor.close()
    connection.close()

    return {
        "average": average,
        "highest": highest,
        "lowest": lowest
    }


def get_recent_expenses(user_id, limit=5):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT *
        FROM expenses
        WHERE user_id = %s
        ORDER BY expense_date DESC, id DESC
        LIMIT %s
    """

    cursor.execute(query, (user_id, limit))
    data = cursor.fetchall()

    cursor.close()
    connection.close()

    return data