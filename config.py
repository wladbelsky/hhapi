from os import getenv

DB_CONFIG = {
    'engine': getenv('DB_ENGINE', 'postgresql+asyncpg'),
    'user': getenv('DB_USER'),
    'password': getenv('DB_PASSWORD'),
    'host': getenv('DB_HOST'),
    'port': getenv('DB_PORT'),
    'database': getenv('DB_NAME'),
}

SPREADSHEET_ID = getenv('SPREADSHEET_ID')
