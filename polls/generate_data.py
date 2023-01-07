import datetime
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MathsWebsite.settings")

import django
django.setup()

from django.core.management import call_command

from django.utils import timezone

from polls.models import Question, Choice

Choice.objects.all().delete()
Question.objects.all().delete()

question_1 = Question.objects.create(
    question_text="Why?",
    pub_date=timezone.now()
)

question_2 = Question.objects.create(
    question_text="Who are you?",
    pub_date=timezone.now() + datetime.timedelta(days=1)
)

question_3 = Question.objects.create(
    question_text="What is your favourite colour?",
    pub_date=timezone.now() + datetime.timedelta(days=1)
)

for colour in ["red", "blue"]:
    Choice.objects.create(
        question=question_3,
        choice_text=colour
    )
