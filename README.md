# Attendance manager
Приложение для контроля посещаемости студентов, разработанное для [Высшей школы искусственного интеллека](https://ai.spbstu.ru/)

## Backend configure

0. Убедитесь, что Python установлен: `python --version` должен выдавать `Python 3.11.3` или что-то похожее.
1. Установить виртуальное окружение Python `python -m venv ./venv/` (выполняется в корне проекта — в папке `app`)
2. Выполнить `cd ./api && pip install -r requirements.txt`:
   подтянуть зависимости (команда `pip install` выполняется в папке `api`)
3. ~~Положить файл `db.sqlite3` в папку `app/api/attendance_site`~~
4. Открыть консоль с виртуальным окружением:
  `venv\Scripts\activate.bat` для Windows, `source venv/bin/activate` для Linux.
5. В этой консоли выполнить `python manage.py runserver`
6. Теперь можно закрыть консоль и выполнить инициализацию БД
Если все успешно, будет выведено

```plain
Django version 4.2, using settings 'attendance_site.settings'
Starting development server at http://127.0.0.1:8000/
```

### Конфигурация базы данных если запустились
0. Добавляем в папку с файлом manage.py (api/attendance_site/) файлы с гугл диска (*.csv)
1. Далее запускаем терминал из этой директории и пишем `python INITIALIZE_DB.py`
Если все успешно то будет выводиться системная информация вида:
```plain
Admin user and related models created successfully
Groups updated successfully
Students updated successfully
...
Add new user with login:Курочкин
Teacher with name "Курочкин Михаил Александрович" created
Subject "Введение в профессиональную деятельность" created
...
Lesson "Программирование и алгоритмизация" created
2023-05-02 14:00:00+03:00
...
Lessons(54) updated or created
DB succesfully initialize
```

### Доступные команды
(либо запустите файл configurate_db)
0. `python manage.py runserver` - запуск сервера АПИ
1.  `python manage.py make_admin_user ` - Создание user - admin с паролем admin. Teacher и GroupLeader с такими же параметрами. 
2.  `python manage.py update_groups <csv path>` - чтение из файла csv групп и заведения записей в БД
3.  `python manage.py update_students <csv path>` - чтение из файла csv студентов и заведения записей в БД
4.  `python manage.py update_subjects` - обновляет список предметов (исключая ФИЗРУ, Военную кафедру)

### Если база удалена:
0. `python manage.py migrate --run-syncdb `     `Пересоздать базу с 0 

## Frontend configure
0. ```cd ./front```
1. Установить [`npm`](https://www.npmjs.com/). Для Windows стоит использовать [nvm-windows](https://github.com/coreybutler/nvm-windows#installation--upgrades) (по ссылке гайд по установке)
<!--
npm create svelte@latest .
-->

2. `nvm install 20.1.0`

3. `nvm use 20.1.0`

4. Выполнить `npm install` в этой папке (`front`) --- эта команда установит зависимости.

## Запуск

### Разработка

Чтобы запустить development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

При успешном запуске откроется страница <http://localhost:5173/> в браузере.

### Сборка

Чтобы создать production версию, нужно выполнить

```bash
npm run build
```

Можно запустить превью production сборки с помощью команды `npm run preview`.
