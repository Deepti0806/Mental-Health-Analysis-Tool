import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
    DEBUG = True

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    LOG_DIR = os.path.join(BASE_DIR, "logs")

    MODEL_DIR = os.path.join(BASE_DIR, "models", "mental_health")
