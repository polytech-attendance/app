from datetime import datetime

import pytz
from django.db.models import When, Case, BooleanField, Value, Exists, OuterRef
from rest_framework.response import Response
from rest_framework.views import APIView

from attendance.models import Subject, Teacher, Group, Student, Lesson, Attendance
from attendance.serializers import SubjectSerializer, SubjectsResponseSerializer
from rest_framework import generics

'''
class SubjectAPIView(APIView):
    def get(self,request):
        subject_data = Subject.objects.all()
        return Response({'posts': SubjectAPIView(subject_data, many=True).data})
'''

class SubjectAPIView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectByTeacherAPIView(APIView):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(teacher_id=teacher_id)
        subjects = Subject.objects.filter(teacher__teacher_id=teacher_id)
        serializer = SubjectsResponseSerializer({'teacher': teacher, 'subjects': subjects})
        return Response(serializer.data)



class SubjectAttendanceView(APIView):
    def get_mark_list(self, group_id: int, lesson_id: int) -> list:
        attendend_list = []
        # print(group.id)
        group = Group.objects.get(group_id=group_id)
        students = Student.objects.filter(group_id=group.id)

        default_value = True  # Значение по умолчанию

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

        for student in queryset:
            # print(student.status)

            is_foreign_value = int(student.is_foreign)

            attendend_data = {
                #'abbrev_name': student.student_name,
                'id': student.student_id,
                #'is_foreign': is_foreign_value,
                #'group_id': group_id,
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
        ).order_by('lesson_start_time')

        student_list=[]
        # put students list into group->student_list
        # abbrev name
        # id
        # is foreign

        students_by_group = Student.objects.filter(group_id=group.id,).order_by('student_name')

        for student in students_by_group:
            student_data = {
                'abbrev_name':student.student_name,
                'id':student.student_id,
                'is_foreign':int(student.is_foreign),
            }
            student_list.append(student_data)



        response_data = {
            'group': {
                'id': group.group_id,
                'name': group.groupname,
                'students_list':student_list,
            },
            'subject': {
                'name': subject.subject_name,
                'id': subject_id,
                'teacher': {
                    'id': subject.teacher.teacher_id,
                    'name': subject.teacher.teacher_name,
                }
            },
            'lessons': []
        }





        for lesson in lessons:
            # r = requests.get(url=f'http://localhost:8000/api/v1/groups/{group_id}/attendance/?lesson_id={lesson.id}')
            r = self.get_mark_list(group_id, lesson.id)
            attendance_by_lesson = r


            tz = pytz.timezone('Europe/Moscow')
            lesson_start_date = lesson.lesson_start_time.astimezone(tz)
            lesson_data = {
                'id': lesson.id,
                'start_iso_time':lesson_start_date,
                #'start_date': lesson_start_date.date(),
                #'start_time': lesson_start_date.time(),
                'attendance_list': attendance_by_lesson,
            }
            response_data['lessons'].append(lesson_data)

        return response_data

    def get(self, request, subject_id, format=None):
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
        group = Group.objects.get(group_id=subject.group.group_id)
        response_data = self.get_student_list(group.group_id, subject_id, date_start, date_end)

        if 'error' in response_data:
            return Response(response_data, status=400)

        return Response(response_data, status=200)

class SubjectAttendanceStatistic(APIView):
    def statistic_for_student(self,student,subject):
        overall_lessons_count = Lesson.objects.filter(subject=subject).count()
        overall_lessons_positive = Attendance.objects.filter(lesson__subject=subject,student=student,is_attendend=Value(True)).count()

        return f'{overall_lessons_positive/overall_lessons_count}'

    def analys_group(self,subject):
        group = subject.group
        student_list=[]
        students = Student.objects.filter(group=subject.group).order_by('student_name')
        for student in students:
            student_data = {
                'abbrev_name':student.student_name,
                'id':student.student_id,
                'is_foreign':int(student.is_foreign),
                'stat':self.statistic_for_student(student,subject)
            }
            student_list.append(student_data)

        response_data = {
            'group': {
                'id': group.group_id,
                'name': group.groupname,
                'students_list': student_list,
            },
            'subject': {
                'name': subject.subject_name,
                'id': subject.id,
                'teacher': {
                    'id': subject.teacher.teacher_id,
                    'name': subject.teacher.teacher_name,
                }
            }
        }


        return response_data
    def get(self,request,subject_id):
        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return Response({'error': f'Subject with id {subject_id} not found'}, status=400)

        response_data = self.analys_group(subject)

        if 'error' in response_data:
            return Response(response_data, status=400)

        return Response(response_data, status=200)

