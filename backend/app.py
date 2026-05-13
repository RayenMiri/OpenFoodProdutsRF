# backend/app.py
from flask import Flask
from sqlalchemy import text
from config import Config
from extensions import db, cors, limiter


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if config:
        app.config.update(config)

    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    limiter.init_app(app)

    from blueprints.health import health_bp
    from blueprints.products import products_bp
    app.register_blueprint(health_bp)
    app.register_blueprint(products_bp)

    from commands import register_commands
    register_commands(app)

    with app.app_context():
        db.create_all()
        try:
            _ensure_fts_index()
        except Exception:
            pass

    return app


def _ensure_fts_index():
    with db.engine.connect() as conn:
        conn.execute(text(
            "CREATE INDEX IF NOT EXISTS ix_products_fts ON products "
            "USING gin(to_tsvector('english', "
            "coalesce(product_name,'') || ' ' || coalesce(brands,'')))"
        ))
        conn.commit()


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
