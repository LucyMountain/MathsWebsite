from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'sudoku/grid.html')


def solve(request):
    breakpoint()
    return HttpResponse("You're voting on question.")

