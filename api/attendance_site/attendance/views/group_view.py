import pytz
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from attendance.models import Group, Lesson, Subject, Teacher
from attendance.serializers import GroupSerializer, LessonSerializer
from datetime import datetime, timedelta
from django.utils import timezone
import json

class GroupAPIView(ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# `GET api/v1/groups/35427/schedule/?date=2023-04-13`
class GroupScheduleView(APIView):
    def get_week_schedule(self, group_id: int, date):

        # проверка существования группы
        try:
            group = Group.objects.get(group_id=group_id)
        except Group.DoesNotExist:
            return Response({'error': f'Group with id {group_id} not found'}, status=400)
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
        start_date = tz.localize(datetime.combine(start_date,datetime.min.time()))
        end_date = tz.localize(datetime.combine(end_date,datetime.max.time()))

        lessons = Lesson.objects.filter(
            subject__group=group,
            lesson_start_time__gte=start_date,
            lesson_end_time__lte=end_date,
        )

        # группируем занятия по дням недели (индекс = день)
        days = []


        for i in range(7):
            day = {}
            day['weekday'] = i + 1
            day['date'] = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
            day['lessons'] = []
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

            teacher_data={
                'id' : teacher_by_subject.teacher_id,
                'full_name' : teacher_by_subject.teacher_name,
            }

            subject_data={
                'subject': subject_by_lesson.subject_name,
                'time_start': lesson_data.get('lesson_start_time')[11:16],#datetime.strptime(lesson_data.get('lesson_start_time')[11:16],'%H:%M'),
                'teacher' : teacher_data,
            }

            days[day_index]['lessons'].append(subject_data)


        response_data = {
            'week': {
                'date_start': start_date.strftime('%Y-%m-%d'),
                'date_end': end_date.strftime('%Y-%m-%d')
            },
            'days': days,
            'group': {
                'id': group.group_id,
                'name': group.groupname
            }
        }

        return Response(response_data,status=200)

    def get(self, request, group_id, format=None):
        try:
            group = Group.objects.get(group_id=group_id)
        except Group.DoesNotExist:
            return Response({'error': f'Group with id {group_id} not found'}, status=400)

        date = request.query_params.get('date', None)
        if not date:
            date = datetime.today().date()
        else:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        schedule = self.get_week_schedule(group.group_id, date)
        return schedule


class GroupItemView(APIView):
    def get(self, request, group_id, format=None):
        try:
            group = Group.objects.get(group_id=group_id)
        except Group.DoesNotExist:
            return Response({'error': f'Group with id {group_id} not found'}, status=400)

        serializer = GroupSerializer(group)
        return Response(serializer.data, status=200)
