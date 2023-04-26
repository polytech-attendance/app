import json

import requests

group_id = 35426

r = requests.get(f'https://ruz.spbstu.ru/api/v1/ruz/scheduler/{group_id}')

j = r.json()

days = j['days']
log = ''
subject_set = set()
lst_sbj =[]
'''
for day in days:
    log += day['date'] + '\n'
    for lesson in day['lessons']:
        log += lesson['subject'] + ', '
        subject_set.add(lesson['subject'])
    log += '\n'
'''
for day in days:
    item = {
        'subject_name' : '',
        'group_id' : group_id,
        'teacher_id' : ''
    }
    for lesson in day['lessons']:
        item['subject_name'] = lesson['subject']
        if not ((lesson['teachers']) == None ):
            item['teacher_id'] = lesson['teachers'][0]['full_name']
        else:
            item['teacher_id'] = ''
        if not item['subject_name'] in subject_set:
            subject_set.add(item['subject_name'])
            lst_sbj.append(item)
        print(item)



print(log)
print(subject_set)
print(lst_sbj)