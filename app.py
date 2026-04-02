from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
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

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
