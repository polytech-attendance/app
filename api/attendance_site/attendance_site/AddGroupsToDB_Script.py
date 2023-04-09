import csv
import sqlite3

# Подключение к базе данных
db = sqlite3.connect('db.sqlite3')

# Открытие файла и чтение данных в формате CSV
with open('students23march2023telematics.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    # Итерация по строкам и загрузка данных в базу данных
    for row in reader:

        group_id_cursor = db.execute("SELECT group_id FROM attendance_group WHERE groupname = ?", (row['Группа'],))
        group_id = group_id_cursor.fetchone()
        if group_id:
            values = (row['ФИО'], row['Иностранец'], group_id[0])
            db.execute("INSERT INTO attendance_student (student_name, is_foreign, group_id) VALUES (?, ?, ?)", values)
        else:
            raise Exception("ERROR: No such group")

# Сохранение изменений в базе данных
db.commit()

# Закрытие соединения с базой данных
db.close()
