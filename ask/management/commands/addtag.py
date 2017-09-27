from django.core.management.base import BaseCommand
from ask.models import Tag
from optparse import make_option


class Command(BaseCommand):
    help = 'Creates new tag'

    option_list = BaseCommand.option_list + (
        make_option('--name'),
    )

    def handle(self, *args, **options):
        name = options['name']

        tag = Tag(name=name)
        tag.save()

