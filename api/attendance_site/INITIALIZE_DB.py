import os
import platform
import subprocess


def init_db():
    # Удаление файла db.sqlite3
    try:
        os.remove('db.sqlite3')
    except:
        pass

    # Список команд для выполнения
    run_server_command = None

    if platform.system() == 'Windows':
        run_server_command = 'start python manage.py runserver'
    elif platform.system() == 'Linux':
        run_server_command = 'nohup python manage.py runserver &'
    else:
        print('Unsupported system')
        return False

    commands = [
        'python manage.py migrate --run-syncdb',
        run_server_command,
        'python manage.py make_admin_user',
        'python manage.py update_groups .\groups_data.csv',
        'python manage.py update_students .\students_data.csv',
        'python manage.py update_subjects',
        'python manage.py update_lessons'
    ]

    # Выполнение команд по порядку
    for cmd in commands:
        subprocess.call(cmd, shell=True)

    return True


if __name__ == '__main__':
    print('Starting initialize DB')
    if init_db():
        print('DB succesfully initialize')
    else:
        print('DB initialize interrupted')
