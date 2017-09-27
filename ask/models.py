from django.db import models
from django.contrib.auth.models import User
import hashlib


def hash_filename(instance, filename):
    m = hashlib.md5()
    m.update(filename.encode('utf-8'))
    print m.hexdigest()
    return 'avatars/' + m.hexdigest()


class Profile(models.Model):
    avatar = models.ImageField(upload_to=hash_filename, default='avatars/no-avatar.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=25, unique=True)


class QuestionManager(models.Manager):
    def hot_questions(self):
        return self.order_by('-rating')

    def new_questions(self):
        return self.order_by('-created_at')

    def has_tag(self, tag):
        return self.filter(tags__name=tag)


class Question(models.Model):
    title = models.CharField(max_length=75)
    text = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    objects = QuestionManager()

    def count_answers(self):
        return Answer.objects.filter(question_id=self.pk).count()

    def get_url(self):
        return "/question/%d/" % self.pk

    def __unicode__(self):
        return u'{0} - {1}'.format(self.pk, self.title)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)


class Like(models.Model):
    value = models.IntegerField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)


class LikeAnswer(models.Model):
    value = models.IntegerField()
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)