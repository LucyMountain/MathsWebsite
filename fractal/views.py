import pandas as pd
from django.shortcuts import render
from .dummy_chart import get_chart

# Create your views here.
from .sierpinksi_triangle import get_triangle


def index(request):
    d = {'transaction_id': [1, 2, 5, 6, 9], 'total_price': [3, 4, 1, 10, 5]}
    df = pd.DataFrame(data=d)
    chart = get_chart('#1', df, '#1')
    context = {
        'chart': chart,
    }
    return render(request, 'fractal/index.html', context)


def sierpinski(request):
    chart = get_triangle()
    context = {
        'chart': chart,
    }
    return render(request, 'fractal/index.html', context)