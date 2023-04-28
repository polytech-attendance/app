from django.db import models


# Create your models here.

class User(models.Model):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    user_id = models.AutoField(primary_key=True)
    user_login = models.CharField(max_length=255, unique=True)
    user_password = models.CharField(max_length=255)

    def __str__(self) -> models.CharField:
        return self.user_login


class Teacher(models.Model):
    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    user = models.OneToOneField(to=User, on_delete=models.CASCADE, verbose_name='User')
    teacher_id = models.CharField(max_length=20, unique=True)
    teacher_name = models.CharField(max_length=100)

    def __str__(self) -> models.CharField:
        return self.teacher_name


class GroupLeader(models.Model):
    class Meta:
        verbose_name = 'GroupLeader'
        verbose_name_plural = 'GroupLeaders'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    groupleader_id = models.CharField(max_length=20)
    groupleader_name = models.CharField(max_length=100)
    groupleader_promote = models.ForeignKey(to=Teacher, on_delete=models.CASCADE, verbose_name='Teacher')

    def __str__(self) -> models.CharField:
        return self.groupleader_name


class Group(models.Model):
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    group_id = models.IntegerField(unique=True)
    groupleader = models.ForeignKey(to=GroupLeader, on_delete=models.CASCADE, verbose_name='GroupLeader',null=True)
    groupname = models.CharField(max_length=50)

    def __str__(self) -> models.CharField:
        return self.groupname


class Student(models.Model):
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    student_id = models.AutoField(primary_key=True)
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, verbose_name='Group')
    student_name = models.CharField(max_length=255)
    is_foreign = models.BooleanField(default=False)

    def __str__(self):
        return self.student_name


class Subject(models.Model):
    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, verbose_name='Group')
    teacher = models.ForeignKey(to=Teacher, on_delete=models.CASCADE, verbose_name='Teacher')
    subject_name = models.CharField(max_length=255)

    def __str__(self) -> models.CharField:
        return self.subject_name


class Lesson(models.Model):
    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'

    lesson_id = models.IntegerField(unique=True)
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, verbose_name='Subject')
    lesson_start_time = models.DateTimeField()
    lesson_end_time = models.DateTimeField()


class Attendance(models.Model):
    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'

    attendance_id = models.AutoField(primary_key=True)
    lesson = models.ForeignKey(to=Lesson, on_delete=models.CASCADE, verbose_name='Lesson')
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE, verbose_name='Student')
    is_attendend = models.BooleanField(default=False)
    update_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(to=User, on_delete=models.CASCADE,verbose_name='User')
