from ..models import User

ADMIN_USER = User.objects.get(user_login='admin')