from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect("portfolio.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stocks (
        symbol TEXT PRIMARY KEY,
        quantity INTEGER,
        price REAL
    )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stocks")
    portfolio = cursor.fetchall()
    conn.close()

    portfolio_data = []
    total_portfolio_value = 0

    for stock in portfolio:
        symbol, quantity, price = stock
        total_value = round(quantity * price, 2)
        total_portfolio_value += total_value
        portfolio_data.append({"symbol": symbol, "quantity": quantity, "price": price, "total_value": total_value})

    return render_template("index.html", portfolio=portfolio_data, total_portfolio_value=total_portfolio_value)

@app.route("/add", methods=["POST"])
def add_stock():
    symbol = request.form["symbol"].upper()
    quantity = int(request.form["quantity"])
    price = float(request.form["price"])  # User enters price manually

    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO stocks (symbol, quantity, price) VALUES (?, ?, ?)", (symbol, quantity, price))
    conn.commit()
    conn.close()
    
    return redirect("/")

@app.route("/remove", methods=["POST"])
def remove_stock():
    symbol = request.form["symbol"].upper()

    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM stocks WHERE symbol = ?", (symbol,))
    conn.commit()
    conn.close()
    
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
