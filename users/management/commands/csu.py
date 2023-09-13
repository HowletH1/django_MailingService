from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Класс - команда для создания суперпользователя
    """

    def handle(self, *args, **options):
        user = User.objects.create(
            email='danila23482mailservice@yandex.ru',
            first_name='Danil',
            last_name='Bokov',
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

        user.set_password('123456')

        user.save()
