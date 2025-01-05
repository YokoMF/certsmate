import os
import yaml
import logging
import logging.config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import has_app_context, has_request_context, g
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
logger = logging.Logger("cm")

def create_app():
    app = Flask(__name__)
    configuration = os.environ.get("CONFIG_PATH", "conf/config.yaml")
    with open(configuration, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
        app.config.update(config)
        uri =(
            f"{config["sqlalchemy"]["db"]}+{config["sqlalchemy"]["engine"]}"
            f"://{config["sqlalchemy"]["user"]}:{os.environ.get("DB_PASSWORD")}"
            f"@{config["sqlalchemy"]["host"]}:{config["sqlalchemy"]["port"]}"
            f"/{config["sqlalchemy"]["schema"]}"
        )
        app.config["SQLALCHEMY_DATABASE_URI"] = uri
        app.config["SQLALCHEMY_ECHO"] = config["sqlalchemy"]["echo"]

    # Initialize the database
    db.init_app(app)

    # 加载 YAML 日志配置
    configuration = os.environ.get("LOG_PATH", "conf/logging.yaml")
    with open(configuration, 'r', encoding='utf-8') as file:
        log_config = yaml.safe_load(file)
        logging.config.dictConfig(log_config)

    # 关闭watchdog的debug信息
    logging.getLogger("watchdog").setLevel(logging.INFO)

    return app


class UUIDFilter (logging.Filter):
    def filter(self, record):
        # 使用固定的 UUID
        if has_request_context() or has_app_context():
            record.uuid = getattr(g, 'uuid', 'N/A')
        else:
            record.uuid = 'N/A'

        return True
