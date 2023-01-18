from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from game.models import Question, Choice, Game, Player, Answer


def index(request):
    game_list = Game.objects.all()
    context = {'game_list': game_list}
    return render(request, 'game/index.html', context)


def start(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    player = Player.objects.create(
        game=game,
        question_number=0,
        questions_correct=0
    )
    return HttpResponseRedirect(reverse('game:next_question', args=(game.id, player.id, None)))


def results(request, game_id, player_id):
    game = get_object_or_404(Question, pk=game_id)
    player = get_object_or_404(Player, pk=player_id)
    accuracy = (player.questions_correct // player.question_number) * 100
    context = {
        'game': game,
        'player': player,
        'accuracy': accuracy,
    }
    return render(request, 'game/results.html', context)


def detail(request, game_id, player_id, question_id):
    game = get_object_or_404(Game, pk=game_id)
    player = get_object_or_404(Player, pk=player_id)
    question = get_object_or_404(Player, pk=question_id)
    if player.question_number > 0:
        accuracy = (player.questions_correct // player.question_number) * 100
    else:
        accuracy = -1
    context = {
        'game': game,
        'player': player,
        'accuracy': accuracy,
        'question': question,
    }
    if len(question.error) > 0:
        context['error'] = question.error
    return render(request, 'game/detail.html', context)


def next_question(request, game_id, player_id):
    game = get_object_or_404(Game, pk=game_id)
    player = get_object_or_404(Player, pk=player_id)
    player.question_number += 1
    if player.question_number > Question.objects.filter(game=Game).count:
        return HttpResponseRedirect(reverse('game:results', args=(game.id, player.id)))
    else:
        question = get_object_or_404(Question, number=player.question_number, game=game)
    return HttpResponseRedirect(reverse('game:detail', args=(game_id, player_id, question.id)))


def answer(request, game_id, player_id, question_id):
    game = get_object_or_404(Game, pk=game_id)
    player = get_object_or_404(Player, pk=player_id)
    question = get_object_or_404(Question, pk=question_id)
    correct_answer = get_object_or_404(Answer, question=question)
    if Choice.objects.filter(question=question).count > 0:
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            question.error = "You didn't select an option."
            return HttpResponseRedirect(reverse('game:detail', args=(game.id, player.id, question.id)))
        else:
            input_answer = selected_choice.choice_text
    else:
        input_answer = request.POST["text_input"]
        input_answer = input_answer.lower()
        correct_answer = correct_answer.lower()
    if correct_answer == input_answer:
        player.questions_correct += 1
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
    return HttpResponseRedirect(reverse('game:next_question', args=(game.id, player.id)))


# todo: change progress bar to be quiz progress and add accuracy underneath
# todo: change quiz setup to be questions and then results at end
# todo: change quiz menu to show game and play etc.
