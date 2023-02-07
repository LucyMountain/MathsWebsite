from django.db import models


# Create your models here.
class Crew(models.Model):
    crew_name = models.CharField(max_length=200)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.crew_name


class Quiz(models.Model):
    quiz_name = models.CharField(max_length=200)

    def __str__(self):
        return self.quiz_name


class Round(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="choices", on_delete=models.CASCADE)
    round_name = models.CharField(max_length=200)
    round_number = models.IntegerField(default=0)

    def __str__(self):
        return self.round_name
