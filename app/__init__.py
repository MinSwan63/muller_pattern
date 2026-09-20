import os
from pathlib import Path
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import config

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(config_name=None):
    app = Flask(__name__, instance_relative_config=True)

    env = config_name or os.environ.get("FLASK_ENV", "development")
    app.config.from_object(config.get(env, config["default"]))

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    Path(app.config["LOGO_PATH"]).parent.mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    csrf.init_app(app)

    from app.routes.main import main_bp
    from app.routes.patterns import patterns_bp
    from app.routes.clients import clients_bp
    from app.routes.settings import settings_bp
    from app.routes.pdf import pdf_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(patterns_bp, url_prefix="/patterns")
    app.register_blueprint(clients_bp, url_prefix="/clients")
    app.register_blueprint(settings_bp, url_prefix="/settings")
    app.register_blueprint(pdf_bp, url_prefix="/pdf")

    with app.app_context():
        from app import models  # noqa
        db.create_all()

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    return app
