import os
import subprocess


# Список команд для выполнения
commands = [
    'python manage.py update_subjects',
    'python manage.py update_lessons'
]

# Выполнение команд по порядку
for cmd in commands:
    subprocess.call(cmd, shell=True)