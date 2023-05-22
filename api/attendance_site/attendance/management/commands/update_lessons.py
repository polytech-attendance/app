from django.core.management.base import BaseCommand
from attendance.models import Subject, Group, Teacher, Lesson
from attendance.auxiliary.fill_lessons import get_lesson_by_group
from attendance.auxiliary.find_teacher_by_id import get_teacher_by_id

from datetime import datetime, timedelta
import pytz

from attendance.auxiliary.get_start_of_week_date import get_start_of_week_date
from .make_new_user import make_new_user


class Command(BaseCommand):
    created_count_lessons = 0
    updated_count_lessons = 0
    created_count_subjects = 0
    updated_count_subjects = 0
    created_count_teachers = 0
    updated_count_teachers = 0

    groups = Group.objects.all()
    tz = pytz.timezone('Europe/Moscow')
    def write_lesson_by_date(self,date_arg:str):
        for group in self.groups:
            # Получить данные из стороннего API
            items = get_lesson_by_group(group.group_id,date_arg)

            # Добавление предметов в базу данных
            lesson_manager = Lesson.objects
            subject_manager = Subject.objects

# найден баг с тем что если например есть лабы у разных лабщиков и это как две разные пары то не будет занесен препод поэтому тут я оставлю это сообщение чтобы это было
# я сделаю try excep чтобы прога не падала аминь
            for item in items:

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

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Teacher with name "{teacher_data["full_name"]}" created'))
                        self.created_count_teachers += 1
                    else:
                        self.stdout.write(
                            self.style.SUCCESS(f'Teacher with name "{teacher_data["full_name"]}" updated'))
                        self.updated_count_teachers += 1

                teacher = Teacher.objects.get(teacher_id=item['teacher_id'])
                try:
                    subject = Subject.objects.get(subject_name=item['subject_name'], group__group_id=group.group_id,
                                                teacher=teacher)
                except Subject.DoesNotExist:
                    subject, created = subject_manager.update_or_create(
                        group=group,
                        teacher=teacher,
                        subject_name=item['subject_name']
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Subject "{subject.subject_name}" created'))
                        self.created_count_subjects += 1
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Subject "{subject.subject_name}" updated'))
                        self.updated_count_subjects += 1

                subject = Subject.objects.get(subject_name=item['subject_name'], group__group_id=group.group_id,
                                              teacher=teacher)
                lesson_start_time = self.tz.localize(datetime.strptime(item['lesson_start_time'], '%Y-%m-%d %H:%M:%S'))
                lesson_end_time = self.tz.localize(datetime.strptime(item['lesson_end_time'], '%Y-%m-%d %H:%M:%S'))
                print(lesson_start_time)
                lesson, created = lesson_manager.update_or_create(
                    subject=subject,
                    lesson_start_time=lesson_start_time,
                    lesson_end_time=lesson_end_time,
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Lesson "{lesson.subject.subject_name}" created'))
                    self.created_count_lessons += 1
                else:
                    self.stdout.write(self.style.SUCCESS(f'Lesson "{lesson.subject.subject_name}" updated'))
                    self.updated_count_lessons += 1


    def add_arguments(self, parser):
        parser.add_argument('start_date', type=str, help='Start date in YYYY-MM-DD format')
    def handle(self, *args, **options):
        start_date_str = get_start_of_week_date(options['start_date'])
        self.stdout.write(f"Start date: {start_date_str}")

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        delta = timedelta(days=7)
        index_date = start_date

        groups = Group.objects.all()
        group = Group.objects.get(groupname='3530201/10001')
        while index_date <= datetime.now():
            date_arg = index_date.strftime("%Y-%m-%d")

            self.stdout.write(f"\n\nStart date: {date_arg}\n\n")
            self.write_lesson_by_date(date_arg)

            index_date += delta

        self.stdout.write(self.style.SUCCESS(f'Lessons updated {self.updated_count_lessons}'))
        self.stdout.write(self.style.SUCCESS(f'Lessons created {self.created_count_lessons}'))

        self.stdout.write(self.style.SUCCESS(f'Subjects updated {self.updated_count_subjects}'))
        self.stdout.write(self.style.SUCCESS(f'Subjects created {self.created_count_subjects}'))


        self.stdout.write(self.style.SUCCESS(f'Teachers updated {self.updated_count_teachers}'))
        self.stdout.write(self.style.SUCCESS(f'Teachers created {self.created_count_teachers}'))


