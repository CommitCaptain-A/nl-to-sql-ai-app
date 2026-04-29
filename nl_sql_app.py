import sqlite3
import requests

# 🔑 Replace with your OpenRouter API key
OPENROUTER_API_KEY = "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"


# =======================
# LLM → SQL (OpenRouter)
# =======================
def llm_to_sql(question):
    prompt = f"""
Convert the following natural language question into a SQL query.

Database:
Table: sales
Columns: product, category, region, revenue, quantity, year

Rules:
- Return ONLY SQL query
- No explanation

Examples:
total revenue in 2023 → SELECT SUM(revenue) FROM sales WHERE year = 2023;
sales in north region → SELECT * FROM sales WHERE region = 'North';

Question: {question}
"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )

        result = response.json()

        # DEBUG
        

        if "choices" not in result:
            return f"ERROR: {result}"

        sql = result["choices"][0]["message"]["content"].strip()
        sql = sql.replace("\n", " ")

        if not sql.lower().startswith("select"):
            return None

        return sql

    except Exception as e:
        return f"ERROR: {e}"


# =======================
# DATABASE SETUP
# =======================
def setup_database():
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY,
        product TEXT,
        category TEXT,
        region TEXT,
        revenue INTEGER,
        quantity INTEGER,
        year INTEGER
    )
    """)

    cursor.execute("DELETE FROM sales")

    data = [
        ("Laptop", "Electronics", "North", 50000, 5, 2023),
        ("Phone", "Electronics", "South", 30000, 10, 2023),
        ("Tablet", "Electronics", "West", 20000, 7, 2022),
        ("Laptop", "Electronics", "East", 70000, 8, 2022),
        ("Shoes", "Fashion", "North", 15000, 20, 2023),
        ("Shirt", "Fashion", "South", 12000, 25, 2022),
        ("Watch", "Accessories", "West", 25000, 6, 2023),
        ("Bag", "Accessories", "East", 18000, 12, 2022)
    ]

    cursor.executemany("""
    INSERT INTO sales (product, category, region, revenue, quantity, year)
    VALUES (?, ?, ?, ?, ?, ?)
    """, data)

    conn.commit()
    conn.close()


# =======================
# EXECUTE SQL
# =======================
def execute_sql(query):
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()

    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()
    return result


# =======================
# MAIN SYSTEM
# =======================
def ask_system(question):
    sql_query = llm_to_sql(question)

    if not sql_query:
        return "Could not generate valid SQL."

    if isinstance(sql_query, str) and sql_query.startswith("ERROR"):
        return sql_query

    try:
        result = execute_sql(sql_query)
        return f"\nSQL:\n{sql_query}\n\nResult:\n{result}\n"
    except Exception as e:
        return f"\nSQL:\n{sql_query}\n\nError: {e}\n"


# =======================
# RUN
# =======================
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    query = ""

    if request.method == "POST":
        user_input = request.form["question"]
        output = ask_system(user_input)

        query = user_input
        result = output

    return render_template("index.html", result=result, query=query)


if __name__ == "__main__":
    setup_database()
    app.run(debug=True)