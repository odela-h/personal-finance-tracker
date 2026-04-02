from flask import Blueprint, request, jsonify
from database import db
from models import Transaction

transactions_bp = Blueprint("transactions", __name__)

# Add a transaction
@transactions_bp.route("/", methods=["POST"])
def add_transaction():
    data = request.get_json()
    t = Transaction(
        type=data["type"],
        amount=data["amount"],
        category=data["category"],
        description=data.get("description", "")
    )
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201

# Get all transactions
@transactions_bp.route("/", methods=["GET"])
def get_transactions():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    return jsonify([t.to_dict() for t in transactions])

# Delete a transaction
@transactions_bp.route("/<int:id>", methods=["DELETE"])
def delete_transaction(id):
    t = Transaction.query.get_or_404(id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"})