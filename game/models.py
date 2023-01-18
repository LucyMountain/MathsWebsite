import datetime
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MathsWebsite.settings")

from django.db import models

# Create your models here.
from django.utils import timezone


class Game(models.Model):
    game_name = models.CharField(max_length=200)

    def __str__(self):
        return self.game_name


class Player(models.Model):
    game = models.ForeignKey(Game, related_name="players", on_delete=models.CASCADE)
    question_number = models.IntegerField(default=0)
    questions_correct = models.IntegerField(default=0)

    def __str__(self):
        return self.player_id


class Question(models.Model):
    game = models.ForeignKey(Game, related_name="questions", on_delete=models.CASCADE)
    error = models.CharField(max_length=200)
    question_text = models.CharField(max_length=200)
    number = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)

    def __str__(self):
        return self.answer_text


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text
