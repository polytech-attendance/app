import os

# Удаление файла db.sqlite3
os.remove('db.sqlite3')

# Список команд для выполнения
commands = [
    'python manage.py update_subjects',
    'python manage.py update_lessons'
]

# Выполнение команд по порядку
for cmd in commands:
    os.system(cmd)
