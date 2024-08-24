import gspread
from flask import Blueprint, request, jsonify

import config
from database.models import Vacancy
from database.postgres import Database
from spreadsheets import gc

router = Blueprint('vacancies', __name__)


@router.get('/vacancies')
def get_vacancies():
    db = Database()
    city = request.args.get('city')
    specialty = request.args.get('specialty')
    with db.get_session() as session:
        query = session.query(Vacancy)
        if city:
            query = query.filter(Vacancy.city == city)
        if specialty:
            query = query.filter(Vacancy.specialty == specialty)
        query = query.order_by(Vacancy.min_salary.asc())
        vacancies = query.all()
        return jsonify([v.to_dict() for v in vacancies])


@router.post('/report')
def report():
    db = Database()
    req = request.json
    city = req.get('city')
    specialty = req.get('specialty')
    with db.get_session() as session:
        query = session.query(Vacancy)
        if city:
            query = query.filter(Vacancy.city == city)
        if specialty:
            query = query.filter(Vacancy.specialty == specialty)
        query = query.order_by(Vacancy.min_salary.asc())
        vacancies = query.all()
    try:
        sheet = gc.open_by_key(config.SPREADSHEET_ID).sheet1
        sheet.clear()
    except (gspread.exceptions.GSpreadException, PermissionError) as e:
        return jsonify({'status': 'error', 'message': str(e)})
    sheet.append_row(['id', 'title', 'url', 'city', 'specialty', 'min_salary', 'max_salary'])
    for chunk in range(0, len(vacancies), 100):
        sheet.append_rows([[vacancy.id, vacancy.title, vacancy.url, vacancy.city, vacancy.specialty,
                              vacancy.min_salary, vacancy.max_salary] for vacancy in vacancies[chunk:chunk + 100]])

    return jsonify({'count': len(vacancies), 'status': 'ok', 'url': sheet.url})
