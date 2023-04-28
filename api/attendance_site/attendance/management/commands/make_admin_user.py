import requests
import json
from django.core.management.base import BaseCommand
from attendance.models import GroupLeader, Teacher, User


class Command(BaseCommand):
    help = 'Create admin user and related models'

    def handle(self, *args, **kwargs):
        # Создаем пользователя
        user_data = {
            'user_login': 'admin',
            'user_password': 'admin',
        }
        response = requests.post('http://localhost:8000/api/v1/users/', data=user_data)

        if response.status_code != 201:
            self.stdout.write(self.style.ERROR('Failed to create user'))
            self.stdout.write(self.style.ERROR(response.text))
            return

        user = User.objects.get(user_login=user_data['user_login'])

        # Создаем объект Teacher
        teacher = Teacher.objects.create(
            user=user,
            teacher_id='admin',
            teacher_name='admin',
        )
        # Создаем объект GroupLeader
        groupleader = GroupLeader.objects.create(
            user=user,
            groupleader_id='ADMIN',
            groupleader_name='ADMIN',
            groupleader_promote=teacher
        )
        self.stdout.write(self.style.SUCCESS('Admin user and related models created successfully'))
