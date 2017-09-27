from django.core.management.base import BaseCommand, CommandError
from ask.models import Answer, Question, Profile
from optparse import make_option


class Command(BaseCommand):
    help = 'Creates new answer'

    option_list = BaseCommand.option_list + (
        make_option('--text'),
        make_option('--q_id'),
        make_option('--author_id')

    )

    def handle(self, *args, **options):
        text = options['text']

        try:
            question = Question.objects.get(pk=options['q_id'])
        except Question.DoesNotExist:
            raise CommandError("Question %d doesn't exist" % options['q_id'])

        try:
            user = Profile.objects.get(user_id=options['author_id'])
        except Profile.DoesNotExist:
            raise CommandError("User %d doesn't exist" % options['author_id'])

        answer = Answer(text=text, author=user, question=question)
        answer.save()