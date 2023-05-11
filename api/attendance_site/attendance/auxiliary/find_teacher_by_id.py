import requests

def get_teacher_by_id(teacher_id : int):
    response = requests.get(f'https://ruz.spbstu.ru/api/v1/ruz/teachers/{teacher_id}')
    r = response.json()
    return r

if __name__ == '__main__':
    # get Vostrov test
    print(get_teacher_by_id(3549))