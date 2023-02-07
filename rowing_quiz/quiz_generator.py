import os
import django
import matplotlib
import numpy as np
from matplotlib.cbook import get_sample_data
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

matplotlib.use('Agg')
from matplotlib import pyplot as plt
import base64
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MathsWebsite.settings')
django.setup()

from rowing_quiz.models import Round, Quiz


def create_quiz():
    rounds = []
    rounds.append('Sport')
    rounds.append('Food??')

    Quiz.objects.all().delete()
    Round.objects.all().delete()
    quiz = Quiz.objects.create(
        quiz_name="boathouse_quiz"
    )
    for r in range(len(rounds)):
        Round.objects.create(
            quiz=quiz,
            round_name=rounds[r],
            round_number=r+1,
        )
    return quiz


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def offset_image(x, y, ax):
    img = plt.imread(r'homepage/static/rowers.png')
    im = OffsetImage(img, zoom=0.1)
    im.image.axes = ax
    x_offset = -55
    ab = AnnotationBbox(im, (x, y), xybox=(x_offset, 0), frameon=False,
                        xycoords='data', boxcoords="offset points", pad=0)
    ax.add_artist(ab)


def generate_results_chart(results):
    fig, ax = plt.subplots()

    crews = [r[0] for r in results]
    values = np.array([r[1] for r in results])
    labels = [f'{r[0]}\n{r[1]}' for r in results]

    height = 0.9
    bar_h = plt.barh(y=crews, width=values, height=height, align='center', alpha=0)
    ax.bar_label(bar_h, labels=labels, color='white')

    max_value = values.max()
    for i, (label, value) in enumerate(zip(crews, values)):
        offset_image(value, i, ax=plt.gca())
    plt.subplots_adjust(left=0.15)

    fig.set_facecolor('blue')
    ax.set_facecolor("blue")
    plt.axis('off')
    plt.tight_layout()
    chart = get_graph()
    return chart
