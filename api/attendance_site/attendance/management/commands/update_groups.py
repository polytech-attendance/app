import csv
from django.core.management.base import BaseCommand
from attendance.models import Group, GroupLeader, User


class Command(BaseCommand):
    help = 'Update groups with group leaders'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', help='Path to the CSV file')


    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        # Получаем пользователя
        user = User.objects.get(user_login='admin')

        # Читаем данные из CSV-файла и обновляем группы
        with open(csv_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                group_id = int(row['group_id'])
                groupname = str(row['group_name'])[:13]

                # Получаем GroupLeader или создаем новый, если его нет
                groupleader = GroupLeader.objects.get(user=User.objects.get(user_login='admin'))

                # Обновляем группу
                Group.objects.update_or_create(
                    group_id=group_id,
                    defaults={
                        'groupleader': groupleader,
                        'groupname': groupname,
                    }
                )

        self.stdout.write(self.style.SUCCESS('Groups updated successfully'))
