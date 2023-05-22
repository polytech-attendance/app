import json
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from attendance.models import Subject, Group, Teacher
from attendance.auxiliary.fill_subjects import get_subject_week
from attendance.auxiliary.find_teacher_by_id import get_teacher_by_id
#from attendance.auxiliary.get_start_of_week_date import get_start_of_week_date
from .make_new_user import make_new_user


class Command(BaseCommand):
    #def add_arguments(self, parser):
    #    parser.add_argument('start_date', type=str, help='Start date in YYYY-MM-DD format')
    def handle(self, *args, **options):
        #start_date_str = get_start_of_week_date(options['start_date'])
        #self.stdout.write(f"Start date: {start_date_str}")


        changes_count = 0
        groups = Group.objects.all()
        for group in groups:
            # Получить данные из стороннего API
            items = get_subject_week(group.group_id,)

            # Добавление предметов в базу данных
            subject_manager = Subject.objects

            for item in items:
                if (item['teacher_id'] is None):
                    self.stdout.write('Teacher\'s id is None. SKIP\n')
                    continue

                try:
                    teacher = Teacher.objects.get(teacher_id=item['teacher_id'])
                except Teacher.DoesNotExist:
                    teacher_data = get_teacher_by_id(item['teacher_id'])
                    teacher_user = make_new_user(teacher_data['first_name'])
                    Teacher.objects.update_or_create(
                        teacher_id=teacher_data['id'],
                        user=teacher_user,
                        teacher_name=teacher_data['full_name'],
                    )
                    self.stdout.write(self.style.SUCCESS(f'Teacher with name "{teacher_data["full_name"]}" created'))
                teacher = Teacher.objects.get(teacher_id=item['teacher_id'])
                subject, created = subject_manager.update_or_create(
                    group=group,
                    teacher=teacher,
                    subject_name=item['subject_name']
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Subject "{subject.subject_name}" created'))
                    changes_count+=1
                else:
                    self.stdout.write(self.style.SUCCESS(f'Subject "{subject.subject_name}" updated'))
                    changes_count+=1
        self.stdout.write(self.style.SUCCESS(f'Subjects({changes_count}) updated or created'))
