# Generated by Django 4.2 on 2023-04-19 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.IntegerField(unique=True)),
                ('groupname', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_login', models.CharField(max_length=255, unique=True)),
                ('user_password', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teacher_id', models.CharField(max_length=20, unique=True)),
                ('teacher_name', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='attendance.user', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Teachers',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_id', models.IntegerField(unique=True)),
                ('subject_name', models.CharField(max_length=255)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.group', verbose_name='Group')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.teacher', verbose_name='Teacher')),
            ],
            options={
                'verbose_name': 'Subject',
                'verbose_name_plural': 'Subjects',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('student_name', models.CharField(max_length=255)),
                ('is_foreign', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.group', verbose_name='Group')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_id', models.IntegerField(unique=True)),
                ('lesson_start_time', models.DateTimeField()),
                ('lesson_end_time', models.DateTimeField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.subject', verbose_name='Subject')),
            ],
            options={
                'verbose_name': 'Lesson',
                'verbose_name_plural': 'Lessons',
            },
        ),
        migrations.CreateModel(
            name='GroupLeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupleader_id', models.CharField(max_length=20)),
                ('groupleader_name', models.CharField(max_length=100)),
                ('groupleader_promote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.teacher', verbose_name='Teacher')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.user')),
            ],
            options={
                'verbose_name': 'GroupLeader',
                'verbose_name_plural': 'GroupLeaders',
            },
        ),
        migrations.AddField(
            model_name='group',
            name='groupleader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='attendance.groupleader', verbose_name='GroupLeader'),
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('attendance_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_attendend', models.BooleanField(default=False)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.lesson', verbose_name='Lesson')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.student', verbose_name='Student')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.user', verbose_name='User')),
            ],
            options={
                'verbose_name': 'Attendance',
                'verbose_name_plural': 'Attendances',
            },
        ),
    ]
