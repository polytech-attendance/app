import csv
from django.core.management.base import BaseCommand
from attendance.models import Group, Student


class Command(BaseCommand):
    help = 'Update students list'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', help='Path to the CSV file')


    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        # Читаем данные из CSV-файла и обновляем группы
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                student_id = int(row['student_id'])
                student_name = str(row['student_name'])
                x = int((row['is_foreign']))

                if x == 1:
                    is_foreign = True
                else:
                    is_foreign = False

                groupname = str(row['group_name'])[:13]

                # Получаем Group
                group = Group.objects.get(groupname=groupname)

                # Обновляем студента
                Student.objects.update_or_create(
                   student_id=student_id,
                    defaults={
                        'is_foreign': is_foreign,
                        'student_name': student_name,
                        'group' : group,
                    }
                )

        self.stdout.write(self.style.SUCCESS('Students updated successfully'))
