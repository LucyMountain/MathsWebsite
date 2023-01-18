import datetime
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MathsWebsite.settings")

import django
django.setup()
from django.core.management import call_command

from django.utils import timezone

from game.models import Question, Answer, Choice, Game

Choice.objects.all().delete()
Answer.objects.all().delete()
Question.objects.all().delete()
Game.objects.all().delete()

"""
=====================================Game 1=====================================
"""
game_1 = Game.objects.create(
    game_name="test"
)

question_1 = Question.objects.create(
    game=game_1,
    question_text="What is the answer to life the universe and everything?",
    number=1,
    pub_date=timezone.now(),
    error=""
)
Answer.objects.create(
    question=question_1,
    answer_text="42"
)
for option in ["42", "12", "49", "17"]:
    Choice.objects.create(
        question=question_1,
        choice_text=option
    )

question_2 = Question.objects.create(
    game=game_1,
    question_text="What is the answer.",
    number=2,
    pub_date=timezone.now() + datetime.timedelta(days=1),
    error=""
)
Answer.objects.create(
    question=question_2,
    answer_text="What"
)

question_3 = Question.objects.create(
    game=game_1,
    question_text="What is root 91?",
    number=3,
    pub_date=timezone.now() + datetime.timedelta(days=1),
    error=""
)
Answer.objects.create(
    question=question_3,
    answer_text="9"
)

"""
=====================================Game 2=====================================
"""
game_2 = Game.objects.create(
    game_name="test_2"
)
question_1 = Question.objects.create(
    game=game_2,
    question_text="Wrong one :((",
    number=1,
    pub_date=timezone.now(),
    error=""
)
Answer.objects.create(
    question=question_1,
    answer_text="Oops!"
)
