"""
данный файл можно удалить, поскольку функционал создания БД
выполняется модулем Миграций (flask_migrate / Alembic)
"""

from webapp import db, create_app

db.create_all(app=create_app())
