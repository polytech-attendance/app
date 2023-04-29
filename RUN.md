# Запуск Backend

1. Установить виртуальное окружение Python `python -m venv ./venv/` (выполняется в корне проекта — в папке `app`)
2. Выполнить `cd ./api && pip install -r requirements.txt`:
   подтянуть зависимости (команда `pip install` выполняется в папке `api`)
3. Положить файл `db.sqlite3` в папку `app/api/attendance_site`
4. Открыть консоль с виртуальным окружением:
  `venv\Scripts\activate.bat` для Windows, `source venv/bin/activate` для Linux.
5. В этой консоли выполнить `python manage.py runserver`

Если все успешно, будет выведено

```plain
Django version 4.2, using settings 'attendance_site.settings'
Starting development server at http://127.0.0.1:8000/
```

# Полезные команды если запустились впервые (выполнять по порядку!!!)
0. `python manage.py runserver` - запуск сервера АПИ
1.  `python manage.py make_admin_user ` - Создание user - admin с паролем admin. Teacher и GroupLeader с такими же параметрами. 
2.  `python manage.py update_groups <csv path>` - чтение из файла csv групп и заведения записей в БД
3.  `python manage.py update_students <csv path>` - чтение из файла csv студентов и заведения записей в БД
4.  `python manage.py update_subjects` - обновляет список предметов (исключая ФИЗРУ, Военную кафедру)

# Если снесли базу:
0. `python manage.py migrate --run-syncdb      `Пересоздать базу с 0 