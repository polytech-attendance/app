import requests
from attendance.models import User
def make_new_user(user_login : str):
    user_data = {
                'user_login': user_login,
                'user_password': 'admin',
            }
    response = requests.post('http://localhost:8000/api/v1/users/', data=user_data)

    if response.status_code != 201:
        print('Failed to create user')
        print((response.text))
        return
    print(f'Add new user with login:{user_login}')
    return User.objects.get(user_login=user_data['user_login'])