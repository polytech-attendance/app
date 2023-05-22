import pytz
from django.db.models import Case, When, Value, IntegerField, OuterRef, Subquery, ExpressionWrapper, F, Q, Exists

from django.db.models.functions import Coalesce, Cast
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import BooleanField
from attendance.models import Group, Lesson, Subject, Teacher, Attendance, Student, User
from attendance.serializers import GroupSerializer, LessonSerializer, AttendanceSerializer
from datetime import datetime, timedelta
from django.utils import timezone
import requests
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
        start_date = tz.localize(datetime.combine(start_date, datetime.min.time()))
        end_date = tz.localize(datetime.combine(end_date, datetime.max.time()))

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

            teacher_data = {
                'id': teacher_by_subject.teacher_id,
                'full_name': teacher_by_subject.teacher_name,
            }

            subject_data = {
                'subject': subject_by_lesson.subject_name,
                'lesson_id': lesson.id,
                'time_start': lesson_data.get('lesson_start_time')[11:16],
                # datetime.strptime(lesson_data.get('lesson_start_time')[11:16],'%H:%M'),
                'teacher': teacher_data,
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

        return Response(response_data, status=200)

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


class GroupAttendanceListView(APIView):

    def get_queryset(self, group_id, lesson_id):
        group = Group.objects.get(group_id=group_id)
        students = Student.objects.filter(group_id=group.id)
        queryset = students.annotate(
            status=Case(
                When(
                    Exists(
                        Attendance.objects.filter(
                            student=OuterRef('student_id'),
                            lesson_id=lesson_id,
                            is_attendend=False,
                        )
                    ),
                    then=Value(False),
                ),
                default=Value(True),
                output_field=BooleanField(),
            )
        ).order_by('student_name')

        return queryset

    def get_student_list(self, group_id, lesson_id, request):
        group = Group.objects.get(group_id=group_id)
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return  {"error": f"This lesson doesnt exist!"}
        subject = lesson.subject

        #when subject_name and lesson_start time is equal

        print(group)


        try:
            lessons_tmp = Lesson.objects.get(
                subject__subject_name=subject.subject_name,
                lesson_start_time=lesson.lesson_start_time,
                subject__group=group,
            )
            subject=lessons_tmp.subject
        except:
            return {'error':'Unexcepted error'}


        print(group)
        #switch subject
        '''
        for l in lessons_tmp:
            print(l.subject.group)
            if l.subject.group == group:
                subject = l.subject
                print('find match!')
                break
        '''

        if subject.group != group:
            return {"error": f"This lesson isn't group {group.groupname} ({group_id})"}

        attendend_list = []
        # print(group.id)

        students = self.get_queryset(group_id, lesson_id)

        for student in students:
            # print(student.status)

            is_foreign_value = int(student.is_foreign)

            attendend_data = {
                'abbrev_name': student.student_name,
                'id': student.student_id,
                'is_foreign': is_foreign_value,
                'group_id': group_id,
                'status': int(student.status),
            }
            attendend_list.append(attendend_data)

        # attendend_list.sort(key=lambda x: x['abbrev_name'])
        return attendend_list

    def get(self, request, group_id, format=None):
        try:
            group = Group.objects.get(group_id=group_id)
        except Group.DoesNotExist:
            return Response({'error': f'Group with id {group_id} not found'}, status=400)

        lesson_id = request.query_params.get('lesson_id', None)
        if lesson_id is None:
            return Response({'error': 'You need to match ?lesson_id'}, status=400)

        response_data = self.get_student_list(group_id, lesson_id, request)

        if 'error' in response_data:
            return Response(response_data, status=400)

        return Response(response_data, status=200)


class GroupAttendanceSubjectView(APIView):
    def get_mark_list(self, group_id: int, lesson_id: int) -> []:
        attendend_list = []
        # print(group.id)
        group = Group.objects.get(group_id=group_id)
        students = Student.objects.filter(group_id=group.id)
        queryset = students.annotate(
            status=Case(
                When(attendance__lesson_id=lesson_id, attendance__is_attendend=False, then=False),
                default=Value(True),
                output_field=BooleanField(),
            )
        ).order_by('student_name')

        for student in queryset:
            # print(student.status)

            is_foreign_value = int(student.is_foreign)

            attendend_data = {
                'abbrev_name': student.student_name,
                'id': student.student_id,
                'is_foreign': is_foreign_value,
                'group_id': group_id,
                'status': int(student.status),
            }
            attendend_list.append(attendend_data)

        # attendend_list.sort(key=lambda x: x['abbrev_name'])
        return attendend_list

    def get_student_list(self, group_id: int, subject_id: int, date_start, date_end) -> dict:
        tz = pytz.timezone('Europe/Moscow')
        try:
            date_start = tz.localize(datetime.strptime(str(date_start), '%Y-%m-%d')).date()
            date_end = tz.localize(datetime.strptime(str(date_end), '%Y-%m-%d')).date()
        except ValueError:
            return {'error': f'Invalid date format: {date_start}    {date_end} (need to YYYY-MM-DD)'}
        group = Group.objects.get(group_id=group_id)
        subject = Subject.objects.get(id=subject_id)

        if subject.group != group:
            return {'error': f'Subject {subject.subject_name} ({subject_id}) not for group: {group.groupname} ({group})'}

        lessons = Lesson.objects.filter(
            subject__id=subject_id,
            lesson_start_time__gte=date_start,
            lesson_start_time__lte=date_end,
        )

        response_data = {
            'group': {
                'group_id': group.group_id,
                'groupname': group.groupname,
            },
            'subject': {
                'subject_name': subject.subject_name,
                'subject_id': subject_id,
                'teacher': {
                    'teacher_id': subject.teacher.teacher_id,
                    'teacher_name': subject.teacher.teacher_name,
                }
            },
            'lessons': []
        }

        for lesson in lessons:
            # r = requests.get(url=f'http://localhost:8000/api/v1/groups/{group_id}/attendance/?lesson_id={lesson.id}')
            r = self.get_mark_list(group_id, lesson.id)
            attendance_by_lesson = r

            lesson_start_date = lesson.lesson_start_time.astimezone(tz)
            lesson_data = {
                'lesson_id': lesson.id,
                'start_iso_time':lesson_start_date,
                #'lesson_start_date': lesson_start_date.date(),
                'attendance_list': attendance_by_lesson,
            }
            response_data['lessons'].append(lesson_data)

        return response_data

    def get(self, request, group_id, subject_id, format=None):
        try:
            group = Group.objects.get(group_id=group_id)
        except Group.DoesNotExist:
            return Response({'error': f'Group with id {group_id} not found'}, status=400)
        # проверка существования предмета и группы
        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return Response({'error': f'Subject with id {subject_id} not found'}, status=400)

        date_start = request.query_params.get('date_start', None)
        date_end = request.query_params.get('date_end', None)

        # Проверка валидности времени
        if not date_start:
            date_start = datetime(year=datetime.today().year, month=1, day=1).date()

        if not date_end:
            date_end = datetime(year=datetime.today().year, month=12, day=31).date()

        # получение данных для ответа
        response_data = self.get_student_list(group_id, subject_id, date_start, date_end)

        if 'error' in response_data:
            return Response(response_data, status=400)

        return Response(response_data, status=200)
