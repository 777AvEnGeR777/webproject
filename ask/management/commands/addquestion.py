from django.core.management.base import BaseCommand, CommandError
from ask.models import Profile, Question, Tag
from optparse import make_option


class Command(BaseCommand):
    help = 'Creates new question'

    option_list = BaseCommand.option_list + (
        make_option('--title'),
        make_option('--text'),
        make_option('--tags'),
        make_option('--author_id'),
    )

    def handle(self, *args, **options):
        try:
            user = Profile.objects.get(user_id=options['author_id'])
        except Profile.DoesNotExist:
            raise CommandError("User %s doesn't exist" % options['author_id'])

        title = options['title']
        text = options['text']

        question = Question(title=title, text=text, author=user)
        question.save()

        for tag in options['tags'].split():
            try:
                question.tags.add(Tag.objects.get(name=tag))
            except Tag.DoesNotExist:
                raise CommandError('Tag "%s" does not exist' % tag)
        question.save()

