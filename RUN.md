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