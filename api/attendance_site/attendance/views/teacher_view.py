from datetime import datetime, timedelta
import pytz
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from attendance.models import Teacher, Lesson, Subject, Group
from attendance.models import User

from attendance.serializers import TeacherSerializer, LessonSerializer

import requests
import json


class TeacherAPIView(APIView):
    def get(self, request):
        user_data = Teacher.objects.all()
        return Response({'posts': TeacherSerializer(user_data, many=True).data})

    def post(self, request):
        # Find id of teacher at ruz.spbstu.ru/api/v1/teachers
        serializer = TeacherSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if Teacher.objects.filter(user_id=request.data.get('user_id')).exists():
            return Response({'error': f'Such a teacher with user_id {request.data.get("user_id")}' + ' already exists'},
                            status=400)

        if Teacher.objects.filter(teacher_name=request.data.get('teacher_name')).exists():
            return Response(
                {'error': f'Such a teacher with teacher_name {request.data.get("teacher_name")}' + ' already exists'},
                status=400)

        if not User.objects.filter(user_id=request.data.get('user_id')).exists():
            return Response({'error': f'Such a user with user_id {request.data.get("user_id")}' + ' doesnt exists'},
                            status=400)

        # find id by name
        teachers_req = requests.get('https://ruz.spbstu.ru/api/v1/ruz/teachers/')
        teachers_json = teachers_req.json()
        teachers_list = teachers_json['teachers']

        # new teacher id for our db
        teacher_id = None
        print(teachers_list)
        for teacher in teachers_list:
            if str(request.data.get('teacher_name')).lower() == str(teacher['full_name']).lower():
                teacher_id = teacher['id']
                print('Found')

        # check if teacher in ruz.spbstu/.../teachers
        if teacher_id is None:
            return Response(
                {'error': f'Such a teacher with name {request.data.get("teacher_name")}' + ' doesnt exists'},
                status=400)

        # if teacher was found
        request.data['teacher_id'] = str(teacher_id)
        serializer = TeacherSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # post data to database
        serializer.save()
        return Response({'post': serializer.data},
                        status=201)

class TeacherScheduleView(APIView):
    def get_week_schedule(self, teacher_id: int, date):

        # проверка существования группы
        try:
            teacher = Teacher.objects.get(teacher_id=teacher_id)
        except Teacher.DoesNotExist:
            return Response({'error': f'Teacher with id {teacher_id} not found'}, status=400)
        # проверка корректности даты
        tz = pytz.timezone('Europe/Moscow')
        try:
            date = tz.localize(datetime.strptime(str(date), '%Y-%m-%d')).date()
        except ValueError:
            return Response({'error': f'Invalid date format: {date}'}, status=400)

        # Определяем начальную и конечную даты недели

        weekday = date.weekday()
        start_date = (date - timedelta(days=weekday))
        end_date = (start_date + timedelta(days=6))

        # Подставялем нужный часовой пояс
        start_date = tz.localize(datetime.combine(start_date, datetime.min.time()))
        end_date = tz.localize(datetime.combine(end_date, datetime.max.time()))

        # получаем список предметов которые ведет преподаватель
        lessons = Lesson.objects.filter(
            subject__teacher=teacher,
            lesson_start_time__gte=start_date,
            lesson_end_time__lte=end_date,)

        lessons = Lesson.objects.filter(
            subject__teacher__isnull=False
        ).select_related('subject__teacher', 'subject__group')

        # группируем занятия по дням недели (индекс = день)
        days = []

        for i in range(7):
            day = {}
            day['weekday'] = i + 1
            day['date'] = (start_date.date() + timedelta(days=i)).strftime('%Y-%m-%d')
            day['lessons'] = []

            daily_lessons = lessons.filter(lesson_start_time__date=day['date']).order_by('lesson_start_time')

            for lesson in daily_lessons:
                groups = [{'id': g.id, 'name': g.name} for g in lesson.groups.all()]
                lesson_data = {
                    'subject': lesson.subject.subject_name,
                    'time_start': lesson.lesson_start_time.time(),
                    'teacher': {'id': teacher.teacher_id},
                    'groups': groups,
                }
                day['lessons'].append(lesson_data)

            days.append(day)

        for lesson in lessons:
            day_index = (lesson.lesson_start_time.date() - start_date.date()).days
            lesson_data = LessonSerializer(lesson).data
            subject_by_lesson = Subject.objects.get(
                id=lesson_data.get('subject')
            )
            teacher_by_subject = Teacher.objects.get(
                id=subject_by_lesson.teacher_id
            )

            response_data = {
                'week': {'date_start': start_date.date(), 'date_end': end_date.date()},
                'days': days,
                'teacher': {
                    'id': teacher.teacher_id,
                    'full_name': teacher.full_name,
                }
            }

        return Response(response_data,status=200)

    def get(self, request, teacher_id, format=None):
        try:
            teacher = Teacher.objects.get(teacher_id=teacher_id)
        except Teacher.DoesNotExist:
            return Response({'error': f'Teacher with id {teacher_id} not found'}, status=400)

        date = request.query_params.get('date', None)
        if not date:
            date = datetime.today().date()
        else:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        schedule = self.get_week_schedule(teacher.teacher_id, date)
        return schedule
