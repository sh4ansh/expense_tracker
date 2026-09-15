# app.py

from flask import Flask, render_template, request, redirect, url_for, session

from auth import register_user, login_user

from expenses import (
    add_expense,
    get_expenses,
    get_expense,
    update_expense,
    delete_expense
)

from analytics import (
    get_total_expense,
    get_category_expenses,
    get_monthly_expenses,
    get_transaction_count,
    get_current_month_expense,
    get_expense_statistics,
    get_recent_expenses
)


app = Flask(__name__)

app.secret_key = "expense_tracker_secret_key"


# ---------------- HOME ----------------

@app.route("/")
def home():

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        success = register_user(name, email, password)

        if success:
            return redirect(url_for("login"))

        return render_template(
            "register.html",
            error="Email already registered."
        )

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = login_user(email, password)

        if user:

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid email or password."
        )

    return render_template("login.html")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    total = get_total_expense(user_id)

    category_data = get_category_expenses(user_id)

    monthly_data = get_monthly_expenses(user_id)

    transaction_count = get_transaction_count(user_id)

    current_month = get_current_month_expense(user_id)

    statistics = get_expense_statistics(user_id)

    recent_expenses = get_recent_expenses(user_id)

    # Top category
    top_category = category_data[0] if category_data else None

    # Highest expense
    highest_expense = statistics["highest"]

    # Generate short report
    if total == 0:

        report = "You don't have any expenses yet. Add your first expense to start tracking your spending."

    elif top_category:

        percentage = (float(top_category["total"]) / float(total)) * 100

        report = (
            f"Your total spending is ₹{float(total):,.2f}. "
            f"Your highest spending category is {top_category['category']} "
            f"with ₹{float(top_category['total']):,.2f}, "
            f"which represents {percentage:.1f}% of your total expenses. "
            f"Your average transaction is ₹{float(statistics['average']):,.2f}."
        )

    else:

        report = "Keep tracking your expenses regularly to understand your spending habits."

    return render_template(
        "dashboard.html",
        total=total,
        category_data=category_data,
        monthly_data=monthly_data,
        transaction_count=transaction_count,
        current_month=current_month,
        statistics=statistics,
        recent_expenses=recent_expenses,
        top_category=top_category,
        report=report
    )


# ---------------- ADD EXPENSE ----------------

@app.route("/add-expense", methods=["GET", "POST"])
def add_expense_page():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        title = request.form["title"]
        amount = request.form["amount"]
        category = request.form["category"]
        expense_date = request.form["expense_date"]
        description = request.form["description"]

        add_expense(
            session["user_id"],
            title,
            amount,
            category,
            expense_date,
            description
        )

        return redirect(url_for("dashboard"))

    return render_template("add_expense.html")


# ---------------- TRANSACTIONS ----------------

@app.route("/transactions")
def transactions():

    if "user_id" not in session:
        return redirect(url_for("login"))

    selected_category = request.args.get("category", "All")

    expenses = get_expenses(session["user_id"])

    if selected_category != "All":

        expenses = [
            expense
            for expense in expenses
            if expense["category"] == selected_category
        ]

    return render_template(
        "transactions.html",
        expenses=expenses,
        selected_category=selected_category
    )


# ---------------- EDIT EXPENSE ----------------

@app.route("/edit-expense/<int:expense_id>", methods=["GET", "POST"])
def edit_expense_page(expense_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    expense = get_expense(expense_id, user_id)

    if not expense:
        return redirect(url_for("transactions"))

    if request.method == "POST":

        title = request.form["title"]
        amount = request.form["amount"]
        category = request.form["category"]
        expense_date = request.form["expense_date"]
        description = request.form["description"]

        update_expense(
            expense_id,
            user_id,
            title,
            amount,
            category,
            expense_date,
            description
        )

        return redirect(url_for("transactions"))

    return render_template(
        "edit_expense.html",
        expense=expense
    )


# ---------------- DELETE EXPENSE ----------------

@app.route("/delete-expense/<int:expense_id>")
def delete_expense_page(expense_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    delete_expense(
        expense_id,
        session["user_id"]
    )

    return redirect(url_for("transactions"))


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    app.run(debug=True)