from django.db import models

# Create your models here.

class User(models.Model):
    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'

    user_id = models.AutoField(primary_key=True)
    user_password = models.CharField(max_length=255)
    user_login = models.CharField(max_length=255, unique=True)

    def __str__(self) -> models.CharField:
        return self.user_login

class Teacher(models.Model):
    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    user_id = models.ForeignKey(to=User, on_delete=models.CASCADE,verbose_name='User')
    teacher_id = models.CharField(max_length=20, unique=True)
    teacher_name = models.CharField(max_length=100)

    def __str__(self) -> models.TextField:
        return self.teacher_name

class GroupLeader(models.Model):
    class Meta:
        verbose_name = 'GroupLeader'
        verbose_name_plural = 'GroupLeaders'

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    groupleader_id = models.CharField(max_length=20)
    groupleader_name = models.CharField(max_length=100)
    groupleader_promote = models.ForeignKey(to=Teacher, on_delete=models.CASCADE,verbose_name='Teacher')

    def __str__(self) -> models.CharField:
        return self.groupleader_name

class Group(models.Model):
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'

    group_id = models.IntegerField(unique=True)
    groupleader_id = models.ForeignKey(to=GroupLeader, on_delete=models.CASCADE,verbose_name='GroupLeader')
    groupname = models.CharField(max_length=50)

    def __str__(self) -> models.CharField:
        return self.groupname
class Student(models.Model):
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    student_id = models.AutoField(primary_key=True)
    group_id = models.ForeignKey(to=Group, on_delete=models.CASCADE,verbose_name='Group')
    student_name = models.CharField(max_length=255)
    is_foreign = models.BooleanField(default=False)

    def __str__(self):
        return self.student_name

class Subject(models.Model):
    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    subject_id = models.IntegerField(unique=True)
    group_id = models.ForeignKey(to=Group,on_delete=models.CASCADE,verbose_name='Group')
    teacher_id = models.ForeignKey(to=Teacher,on_delete=models.CASCADE,verbose_name='Teacher')
    subject_name = models.CharField(max_length=255)

    def __str__(self) -> models.CharField:
        return self.subject_name


class Class(models.Model):
    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    class_id = models.IntegerField(unique=True)
    subject_id = models.ForeignKey(to=Subject, on_delete=models.CASCADE, verbose_name='Subject')
    class_start_time = models.DateTimeField()
    class_end_time = models.DateTimeField()

class Attendance(models.Model):
    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'

    attendance_id = models.AutoField(primary_key=True)
    class_id = models.ForeignKey(to=Class,on_delete=models.CASCADE,verbose_name='Class')
    student_id = models.ForeignKey(to=Student,on_delete=models.CASCADE,verbose_name='Student')
    is_attendend = models.BooleanField(default=False)