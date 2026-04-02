from flask import Blueprint, jsonify
from models import Transaction
import pandas as pd

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/summary", methods=["GET"])
def summary():
    transactions = Transaction.query.all()
    if not transactions:
        return jsonify({"message": "No data yet"})

    data = [t.to_dict() for t in transactions]
    df = pd.DataFrame(data)

    total_income = df[df["type"] == "income"]["amount"].sum()
    total_expense = df[df["type"] == "expense"]["amount"].sum()
    balance = total_income - total_expense

    expense_by_category = (
        df[df["type"] == "expense"]
        .groupby("category")["amount"]
        .sum()
        .to_dict()
    )

    return jsonify({
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "expense_by_category": expense_by_category
    })

@analytics_bp.route("/patterns", methods=["GET"])
def patterns():
    transactions = Transaction.query.all()
    if not transactions:
        return jsonify({"message": "No data yet"})

    data = [t.to_dict() for t in transactions]
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df["day_of_week"] = df["date"].dt.day_name()

    expenses = df[df["type"] == "expense"]
    if expenses.empty:
        return jsonify({"message": "No expense data yet"})

    grouped = expenses.groupby(["day_of_week", "category"])["amount"].sum()
    top = grouped.idxmax()
    insight = f"You spend the most on {top[1]} on {top[0]}s."

    return jsonify({"insight": insight})