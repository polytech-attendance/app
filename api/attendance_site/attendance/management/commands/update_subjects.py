import json
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from attendance.models import Subject, Group
from attendance.managers import SubjectManager
from attendance.auxiliary.fill_subjects import get_subject_cur_week


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Получить данные из стороннего API
        group = Group.objects.get(groupname="3530201/10001")
        items = get_subject_cur_week(group.group_id)

        # Добавление предметов в базу данных
        subject_manager = Subject.objects
        for item in items:
            group = Group.objects.get(groupname="3530201/10001")
            subject, created = subject_manager.update_or_create(

                group=group,
                teacher_id=item['teacher_id'],
                subject_name=item['subject_name']
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Subject "{subject.subject_name}" created'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Subject "{subject.subject_name}" updated'))