from django.core.management.base import BaseCommand
from ask.models import Profile
from django.contrib.auth.models import User
from optparse import make_option


class Command(BaseCommand):
    help = 'Creates new user'

    option_list = BaseCommand.option_list + (
        make_option('--login'),
        make_option('--email'),
        make_option('--nick'),
        make_option('--passwd'),
    )

    def handle(self, *args, **options):
        login = options['login']
        email = options['email']
        nick = options['nick']
        passwd = options['passwd']

        user = User.objects.create_user(login, email, passwd, first_name=nick)

        profile = Profile(user=user)
        profile.save()

