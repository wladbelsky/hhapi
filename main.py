import asyncio

import gspread
from flask import Flask
from config import DB_CONFIG
from database.postgres import Database
from routes.parse import router as parse_router
from routes.vacancies import router as vacancies_router

app = Flask(__name__)
app.register_blueprint(parse_router)
app.register_blueprint(vacancies_router)

def prepare_db() -> None:
    db = Database(DB_CONFIG)
    db.prepare_tables()

prepare_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
