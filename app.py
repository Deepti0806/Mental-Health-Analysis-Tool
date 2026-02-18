import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from config import Config
from mental_health import mental_health


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ==============================
    # Security
    # ==============================
    app.secret_key = app.config.get("SECRET_KEY", "dev_secret_key")

    # ==============================
    # Logging Setup
    # ==============================
    log_dir = app.config.get("LOG_DIR", "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file_path = os.path.join(log_dir, "app.log")

    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=10240,      # 10KB per file
        backupCount=5       # Keep 5 old logs
    )

    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Avoid duplicate log handlers on reload
    if not app.logger.handlers:
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)

    app.logger.info("Application started successfully.")

    # ==============================
    # Register Blueprints
    # ==============================
    app.register_blueprint(mental_health, url_prefix="/mental_health")


    return app


if __name__ == "__main__":
    app = create_app()

    # Use config debug flag instead of hardcoding
    app.run(debug=app.config.get("DEBUG", False))
