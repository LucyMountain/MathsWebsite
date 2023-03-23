from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse

from rowing_quiz.enums import QuizState
from rowing_quiz.models import Crew, Round, Quiz
from rowing_quiz.quiz_generator import create_quiz, generate_results_chart

from numpy import random


def index(request):
    return render(request, 'rowing_quiz/index.html')


def quiz_engine(request):
    r_num = request.session['round_number']
    quiz = get_object_or_404(Quiz, id=request.session['quiz'])
    match QuizState(request.session['state']):
        case QuizState.ASSIGN_CREWS:
            Crew.objects.all().delete()
            response = None
            formset_class = modelformset_factory(
                model=Crew, fields=('crew_name', 'score', 'crew_number'), extra=0, can_delete=True)
            if request.method == 'POST':
                formset = formset_class(data=request.POST)
                if formset.is_valid():
                    formset.save()
                    request.session['crews'] = [crew.id for crew in Crew.objects.all()]
                    request.session['state'] = QuizState.NEXT_ROUND.value
                    response = HttpResponseRedirect(reverse('rowing_quiz:quiz_engine'))
            else:
                formset = formset_class()
            if response is None:
                response = render(
                    request, 'rowing_quiz/assign_crews.html', dict(formset=formset))
            return response
        case QuizState.DETAIL:
            if r_num > request.session['total_rounds']:
                request.session['state'] = QuizState.RESULTS.value
                return HttpResponseRedirect(reverse('rowing_quiz:quiz_engine'))
            else:
                current_round = get_object_or_404(Round, round_number=r_num, quiz=quiz)
            scores = []
            names = []
            numbers = {}
            for crew_id in request.session['crews']:
                crew = get_object_or_404(Crew, id=crew_id)
                s = crew.score
                if s - int(s) == 0:
                    s = int(s)
                scores.append([crew.crew_name, s])
                names.append(crew.crew_name)
                numbers[crew.crew_name] = (crew.crew_number)
            chart = generate_results_chart(scores)
            context = {
                'round': current_round,
                'chart': chart,
                'names': names,
                'numbers': numbers
            }
            if len(request.session['error']) > 0:
                context['error'] = request.session['error']
                request.session['error'] = ''
            request.session['state'] = QuizState.SUBMIT.value
            return render(request, 'rowing_quiz/detail.html', context)
        case QuizState.NEXT_ROUND:
            request.session['round_number'] += 1
            request.session['state'] = QuizState.DETAIL.value
            return HttpResponseRedirect(reverse('rowing_quiz:quiz_engine'))
        case QuizState.SUBMIT:
            for crew_id in request.session['crews']:
                crew = get_object_or_404(Crew, id=crew_id)
                if crew.crew_name in request.POST:
                    add_score = float(request.POST[crew.crew_name])
                    crew.score += add_score
                    crew.save()
                else:
                    request.session['error'] = "You didn't submit a value."
                    request.session['state'] = QuizState.NEXT_ROUND.value
                    return HttpResponseRedirect(reverse('rowing_quiz:quiz_engine'))
            request.session['state'] = QuizState.NEXT_ROUND.value
            return HttpResponseRedirect(reverse('rowing_quiz:quiz_engine'))
        case QuizState.RESULTS:
            crews = Crew.objects.all().order_by('-score')
            for c in crews:
                s = c.score
                if s - int(s) == 0:
                    c.score = int(s)
            scores = []
            for crew_id in request.session['crews']:
                crew = get_object_or_404(Crew, id=crew_id)
                s = crew.score
                if s - int(s) == 0:
                    s = int(s)
                scores.append([crew.crew_name, s])
            chart = generate_results_chart(scores)
            context = {
                'chart': chart,
                'crews': crews
            }
            return render(request, 'rowing_quiz/results.html', context)


def start(request):
    quiz = create_quiz()
    request.session['quiz'] = quiz.id
    request.session['round_number'] = 0
    request.session['total_rounds'] = Round.objects.all().filter(quiz=quiz).count()
    request.session['max_score'] = 100
    request.session['error'] = ""
    request.session['state'] = QuizState.ASSIGN_CREWS.value
    return HttpResponseRedirect(reverse('rowing_quiz:quiz_engine'))


"""
    request.session['state'] = QuizState.NEXT_ROUND.value
    Crew.objects.all().delete()
    for i in range(20):
        Crew.objects.create(
            crew_name=i,
            score=0
        )
    request.session['crews'] = [crew.id for crew in Crew.objects.all()]
    return HttpResponseRedirect(reverse('rowing_quiz:quiz_engine'))
"""


# todo: what was he doing while drinking the ice tea
