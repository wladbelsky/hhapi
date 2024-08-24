import requests
from flask import Blueprint, request, jsonify
from database.postgres import Database
from database.models import Vacancy
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime, timedelta

router = Blueprint('parse', __name__)

@router.get('/parse')
async def parse():
    two_days_ago = datetime.now() - timedelta(days=2)
    params = {
        'date_from': two_days_ago.date().isoformat(),
        'per_page': 100,
        'page': 0,
    }
    current_page = 0
    max_pages = 1
    while True:
        params['page'] = current_page
        response = requests.get("https://api.hh.ru/vacancies", params=params)
        resp_json = response.json()
        if resp_json.get('pages'):
            max_pages = resp_json['pages']
        db = Database()
        with db.get_session() as session:
            for item in resp_json.get('items', {}):
                v = {
                    'id':int(item['id']),
                    'title':item['name'],
                    'url':item['alternate_url'],
                    'city':item['area']['name'],
                    'specialty':item['professional_roles'][0]['name'] if item['professional_roles'] else None,
                    'min_salary':item['salary']['from'] if item['salary'] and item['salary']['from'] else None,
                    'max_salary':item['salary']['to'] if item['salary'] and item['salary']['to'] else None
                }
                session.execute(insert(Vacancy).values(v).on_conflict_do_update(
                    index_elements=['id'],
                    set_=v
                ))
            session.commit()
        if current_page == max_pages:
            break
        current_page += 1
    return jsonify({'status': 'ok'})
