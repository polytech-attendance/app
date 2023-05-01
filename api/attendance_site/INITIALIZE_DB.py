import os

# Удаление файла db.sqlite3
os.remove('db.sqlite3')

# Список команд для выполнения
commands = [
    'python manage.py migrate --run-syncdb',
    'python manage.py runserver',
    'python manage.py make_admin_user',
    'python manage.py update_groups .\groups_data.csv',
    'python manage.py update_students .\students_data.csv',
    'python manage.py update_subjects',
    'python manage.py update_lessons'
]

# Выполнение команд по порядку
for cmd in commands:
    os.system(cmd)
