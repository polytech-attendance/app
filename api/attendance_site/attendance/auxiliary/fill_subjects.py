from datetime import datetime
import json
import requests


def get_subject_week(group_id: int, start_time=None):

    if start_time is None:
        cur_day = datetime.today()
        start_time = f"{cur_day.year}-{cur_day.month}-{cur_day.day}"

    r = requests.get(url=f'https://ruz.spbstu.ru/api/v1/ruz/scheduler/{group_id}?date={start_time}')

    j = r.json()

    days = j['days']
    log = ''
    subject_set = set()
    lst_sbj = []

    for day in days:
        for lesson in day['lessons']:
            item = {'subject_name': lesson['subject'], 'group_id': group_id, 'teacher_id': ''}
            if not ((lesson['teachers']) == None):
                item['teacher_id'] = lesson['teachers'][0]['id']
            else:
                item['teacher_id'] = None
            if not item['subject_name'] in subject_set:
                subject_set.add(item['subject_name'])
                lst_sbj.append(item)
            # print(item)

    # print(log)
    # print(subject_set)
    # print(lst_sbj)
    return lst_sbj


'''
for day in days:
    log += day['date'] + '\n'
    for lesson in day['lessons']:
        log += lesson['subject'] + ', '
        subject_set.add(lesson['subject'])
    log += '\n'
'''

if __name__ == '__main__':
    group_id = 35426
    print(get_subject_week(group_id))
