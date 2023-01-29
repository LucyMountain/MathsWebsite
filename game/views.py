import logging

from django.db.models import Count
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from game.enums import GameState
from game.models import Question, Choice, Game, Answer


def index(request):
    game_list = Game.objects.all()
    context = {'game_list': game_list}
    return render(request, 'game/index.html', context)


def game_engine(request):
    game = get_object_or_404(Game, pk=request.session['game'])
    q_num = request.session['question_number']
    match GameState(request.session['state']):
        case GameState.NEXT_QUESTION:
            request.session['question_number'] += 1
            request.session['state'] = GameState.DETAIL.value
            return HttpResponseRedirect(reverse('game:game_engine'))
        case GameState.DETAIL:
            if q_num > request.session['questions_total']:
                request.session['state'] = GameState.RESULTS.value
                return HttpResponseRedirect(reverse('game:game_engine'))
            else:
                question = get_object_or_404(Question, number=q_num, game=game)
            if q_num > 1:
                accuracy = int((request.session['questions_correct'] / (q_num - 1)) * 100)
            else:
                accuracy = -1
            choice_set = Choice.objects.filter(question=question)
            context = {
                'game': game,
                'accuracy': accuracy,
                'question': question,
                'choice_set': choice_set
            }
            if len(request.session['error']) > 0:
                context['error'] = request.session['error']
                request.session['error'] = ""
            request.session['state'] = GameState.ANSWER.value
            return render(request, 'game/detail.html', context)
        case GameState.ANSWER:
            question = get_object_or_404(Question, game=game, number=q_num)
            correct_answer = get_object_or_404(Answer, question=question).answer_text
            if Choice.objects.filter(question=question).count() > 0:
                try:
                    selected_choice = get_object_or_404(Choice, pk=request.POST['choice'])
                except (KeyError, Choice.DoesNotExist):
                    request.session['error'] = "You didn't select an option."
                    request.session['state'] = GameState.DETAIL.value
                    return HttpResponseRedirect(reverse('game:game_engine'))
                else:
                    input_answer = selected_choice.choice_text
            else:
                if "text_input" in request.POST:
                    input_answer = request.POST["text_input"]
                else:
                    request.session['error'] = "You didn't submit an answer."
                    request.session['state'] = GameState.DETAIL.value
                    return HttpResponseRedirect(reverse('game:game_engine'))
                input_answer = input_answer.lower()
                correct_answer = correct_answer.lower()
            if correct_answer == input_answer:
                request.session['questions_correct'] += 1
            request.session['state'] = GameState.NEXT_QUESTION.value
            return HttpResponseRedirect(reverse('game:game_engine'))
        case GameState.RESULTS:
            accuracy = int((request.session['questions_correct'] / (q_num - 1)) * 100)
            context = {
                'game': game,
                'accuracy': accuracy,
                'questions_count': request.session['questions_total'],
                'questions_correct': request.session['questions_correct']
            }
            return render(request, 'game/results.html', context)


def start(request, game_name):
    game = get_object_or_404(Game, game_name=game_name)
    request.session['game'] = game.id
    request.session['game_name'] = game.game_name
    request.session['question_number'] = 0
    request.session['questions_correct'] = 0
    request.session['questions_total'] = Question.objects.all().filter(game=game).count()
    request.session['state'] = GameState.NEXT_QUESTION.value
    request.session['error'] = ""
    return HttpResponseRedirect(reverse('game:game_engine'))


# todo: add concept of user and make player have a name
# todo: screen which displays if you are correct or not with next button
# todo: neaten detail, results css with nice choice buttons etc
# todo: neaten css file etc
# todo: what on earth happens when you full screen?
