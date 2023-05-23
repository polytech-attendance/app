import os
import subprocess
import sys
from datetime import datetime
from attendance.auxiliary.get_start_of_week_date import get_start_of_week_date


def update_lessons(date:str):
    # Список команд для выполнения
    commands = [
        #f'python manage.py update_subjects {date}',
        f'python manage.py update_lessons {date}'
    ]

    # Выполнение команд по порядку
    for cmd in commands:
        subprocess.call(cmd, shell=True)
# Проверяем, есть ли аргументы командной строки
if len(sys.argv) > 1:
    # Если есть, используем значение из аргумента
    date_arg = sys.argv[1]
    date_arg = get_start_of_week_date(date_arg)
else:
    # Если нет, подставляем текущую дату
    date_arg = datetime.today().date().strftime("%Y-%m-%d")


update_lessons(date_arg)

