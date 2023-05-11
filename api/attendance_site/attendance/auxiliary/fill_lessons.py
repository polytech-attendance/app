import json
import requests
from datetime import datetime


def get_lesson_by_group(group_id: int, start_time=None):
    # https://ruz.spbstu.ru/api/v1/ruz/scheduler/35340?date=2023-04-28
    if start_time is None:
        cur_day = datetime.today()
        start_time = f"{cur_day.year}-{cur_day.month}-{cur_day.day}"

    response = requests.get(url=f'https://ruz.spbstu.ru/api/v1/ruz/scheduler/{group_id}?date={start_time}')
    j = response.json()

    days = j['days']
    lessons_list = []

    for day in days:
        date_for_day = datetime.strptime(day['date'], '%Y-%m-%d')
        lessons = day['lessons']
        for lesson in lessons:
            if (lesson['teachers']) is None:
                continue

            lesson_start_hour = datetime.strptime(lesson['time_start'], "%H:%M")
            lesson_end_hour = datetime.strptime(lesson['time_end'], "%H:%M")

            lesson_start_time = datetime.combine(date_for_day.date(), lesson_start_hour.time())
            lesson_end_time = datetime.combine(date_for_day.date(), lesson_end_hour.time())

            teacher_id = lesson['teachers'][0]['id']

            item = {'subject_name': lesson['subject'], 'group_id': group_id, 'lesson_start_time': str(lesson_start_time),
                    'lesson_end_time': str(lesson_end_time), 'teacher_id': teacher_id}

            lessons_list.append(item)
    return lessons_list


if __name__ == '__main__':
    # Debug part
    print(get_lesson_by_group(35340))
