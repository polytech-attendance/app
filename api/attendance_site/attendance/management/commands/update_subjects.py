import json
from datetime import datetime, timedelta
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from attendance.models import Subject, Group, Teacher
from attendance.auxiliary.fill_subjects import get_subject_week
from attendance.auxiliary.find_teacher_by_id import get_teacher_by_id
from attendance.auxiliary.get_start_of_week_date import get_start_of_week_date
from .make_new_user import make_new_user


class Command(BaseCommand):
    created_count = 0
    updated_count = 0
    groups = Group.objects.all()

    def write_subject_by_date(self, date_arg: str):
        for group in self.groups:
            # Получить данные из стороннего API
            items = get_subject_week(group.group_id, date_arg)

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
                    self.created_count += 1
                else:
                    self.stdout.write(self.style.SUCCESS(f'Subject "{subject.subject_name}" updated'))
                    self.updated_count += 1

    def add_arguments(self, parser):
        parser.add_argument('start_date', type=str, help='Start date in YYYY-MM-DD format')

    def handle(self, *args, **options):
        start_date_str = get_start_of_week_date(options['start_date'])
        self.stdout.write(f"Start date: {start_date_str}")

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        delta = timedelta(days=7)
        index_date = start_date

        while index_date <= datetime.now():
            date_arg = index_date.strftime("%Y-%m-%d")

            self.stdout.write(f"\n\nStart date: {date_arg}\n\n")
            self.write_subject_by_date(date_arg)

            index_date += delta

        self.stdout.write(self.style.SUCCESS(f'Subjects updated {self.updated_count}'))
        self.stdout.write(self.style.SUCCESS(f'Subjects created {self.created_count}'))
