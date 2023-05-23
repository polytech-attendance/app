import datetime
from datetime import timedelta,datetime


def get_start_of_week_date(date_str:str)->str:
    date = datetime.strptime(date_str, '%Y-%m-%d')

    # Получаем день недели (0 - понедельник, 1 - вторник, и т.д.)
    weekday = date.weekday()

    # Вычисляем разницу дней для перемещения к началу недели (понедельник)
    days_to_start_of_week = (weekday) % 7

    # Вычитаем разницу дней из исходной даты, чтобы получить день начала недели
    start_of_week = date - timedelta(days=days_to_start_of_week)

    # Преобразуем день начала недели в строку в формате 'YYYY-MM-DD'
    start_of_week_str = start_of_week.strftime('%Y-%m-%d')
    return start_of_week_str