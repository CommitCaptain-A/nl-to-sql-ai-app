# 🚀 NL-to-SQL AI Web App

An AI-powered web application that converts natural language queries into SQL and executes them on a structured database.

---

## 🧠 Overview

This project allows users to interact with a database using plain English.  
Instead of writing SQL queries manually, users can simply type questions like:

> "total revenue in 2023"

The system uses an LLM (via OpenRouter API) to generate SQL queries and executes them on a SQLite database, returning real results through a web interface.

---

## ✨ Features

- 🔹 Natural Language → SQL conversion using LLM
- 🔹 Real-time SQL execution on SQLite database
- 🔹 Flask-based interactive web UI
- 🔹 Handles filtering, aggregation, and multi-condition queries
- 🔹 Clean end-to-end pipeline (Input → LLM → SQL → Result)

---

## 🛠️ Tech Stack

- **Python**
- **Flask**
- **SQLite**
- **OpenRouter API (GPT-3.5)**
- **HTML/CSS**

---

## 🧪 Example Queries

Try these in the app:

- `total revenue in 2023`
- `sales in north region`
- `electronics products`
- `total revenue for electronics in 2023`

---

## ⚙️ How It Works

1. User enters a natural language query  
2. LLM converts it into a SQL query  
3. SQL query is executed on the database  
4. Results are displayed in the web UI  

---
