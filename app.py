from flask import Flask
from flask_cors import CORS
from database import db

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///finance.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

from routes.transactions import transactions_bp
from routes.analytics import analytics_bp

app.register_blueprint(transactions_bp, url_prefix="/api/transactions")
app.register_blueprint(analytics_bp, url_prefix="/api/analytics")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
