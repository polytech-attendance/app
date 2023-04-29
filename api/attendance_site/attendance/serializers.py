from rest_framework import serializers
from .models import Group, Teacher, Lesson, User, Subject, Attendance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('group_id', 'groupname', 'groupleader_id')


class UserSerializer(serializers.Serializer):
    user_login = serializers.CharField(max_length=255)
    user_password = serializers.CharField(max_length=255)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

class TeacherSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    teacher_name = serializers.CharField(max_length=255)
    teacher_id = serializers.CharField(required=False)

    def create(self, validated_data):
        return Teacher.objects.create(**validated_data)

'''
class LessonSerializer(serializers.Serializer):
    lesson_id = serializers.IntegerField()
    subject_id = serializers.IntegerField()
    lesson_start_time = serializers.DateTimeField()
    lesson_end_time = serializers.DateTimeField()

    def create(self, validated_data):
        return Lesson.objects.create(**validated_data)
'''
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'group', 'teacher', 'subject_name')

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('subject', 'lesson_start_time', 'lesson_end_time')

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
