from django.core.management.base import BaseCommand
from attendance.models import Subject, Group, Teacher, Lesson
from attendance.auxiliary.fill_lessons import get_lesson_by_group
from datetime import datetime
import pytz


class Command(BaseCommand):
    def handle(self, *args, **options):
        tz = pytz.timezone('Europe/Moscow')
        # Получить данные из стороннего API
        changes_count = 0
        groups = Group.objects.all()
        group = Group.objects.get(groupname='3530201/10001')
        items = get_lesson_by_group(group.group_id)

        # Добавление предметов в базу данных
        subject_manager = Subject.objects
        lesson_manager = Lesson.objects

        for item in items:
            subject = Subject.objects.get(subject_name=item['subject_name'], group=group)

            lesson_start_time = tz.localize(datetime.strptime(item['lesson_start_time'], '%Y-%m-%d %H:%M:%S'))
            lesson_end_time = tz.localize(datetime.strptime(item['lesson_end_time'], '%Y-%m-%d %H:%M:%S'))
            print(lesson_start_time)
            lesson, created = lesson_manager.update_or_create(
                subject=subject,
                lesson_start_time=lesson_start_time,
                lesson_end_time=lesson_end_time,
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Lesson "{lesson.subject.subject_name}" created'))
                changes_count += 1
            else:
                self.stdout.write(self.style.SUCCESS(f'Subject "{lesson.subject.subject_name}" updated'))
                changes_count += 1
        self.stdout.write(self.style.SUCCESS(f'Lessons({changes_count}) updated or created'))
