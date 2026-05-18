from flask import Flask, render_template, request

app = Flask(__name__)

# Global storage (temporary demo data)
transactions = []

# 🏠 Home Page
@app.route("/")
def home():
    return render_template("index.html")


# 📊 Dashboard (MAIN LOGIC HERE 🔥)
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    result = ""
    balance = 10000

    if request.method == "POST":

        # Add transactions (multi-input)
        categories = ["Food", "Shopping", "Bills", "Transport"]

        for cat in categories:
            value = request.form.get(cat)

            if value and value.strip() != "":
                amount = int(value)
                transactions.append({"category": cat, "amount": amount})

        # Decision engine
        if "price" in request.form:
            price = int(request.form["price"])

            balance_value = request.form.get("balance")

            if balance_value and balance_value.strip() != "":
                balance = int(balance_value)
            else:
                balance = 10000

            if price < balance - 2000:
                result = "✅ Safe to buy"
            else:
                result = "❌ Not recommended"

    # Convert to summary
    category_sum = {}
    total_expense = 0

    for t in transactions:
        category_sum[t["category"]] = category_sum.get(t["category"], 0) + t["amount"]
        total_expense += t["amount"]

    # Behavior detection
    if category_sum.get("Shopping", 0) > 2000:
        behavior_msg = "⚠️ High shopping spending detected, you need to reduce"
    else:
        behavior_msg = "✅ Spending is under control"

    # Prediction
    predicted_balance = balance - total_expense

    if predicted_balance < 2000:
        prediction_msg = f"⚠️ Balance may drop to ₹{predicted_balance}"
    else:
        prediction_msg = f"✅ Expected balance: ₹{predicted_balance}"

    # Savings
    if balance < 3000:
        savings_msg = "💡 Reduce spending to improve savings"
    else:
        savings_msg = "✅ You are saving well"

    # FD Advisor
    if balance > 5000:
        fd_msg = "✅ You can safely invest ₹2000 in FD"
    else:
        fd_msg = "❌ FD not recommended"

    return render_template(
        "dashboard.html",
        result=result,
        balance=balance,
        data=category_sum,
        fd_msg=fd_msg,
        behavior_msg=behavior_msg,
        prediction_msg=prediction_msg,
        savings_msg=savings_msg
    )


# 📤 Upload Page
@app.route("/upload", methods=["GET", "POST"])
def upload():
    return render_template("upload.html")


# 📈 Insights Page
@app.route("/insights")
def insights():
    return render_template("insights.html")


# 🧑‍💻 About Page
@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)