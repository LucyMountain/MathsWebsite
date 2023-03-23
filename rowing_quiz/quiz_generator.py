import os
import django
import matplotlib
import numpy as np
from PIL.ImageDraw import ImageDraw
from PIL.ImageFont import ImageFont
from matplotlib.cbook import get_sample_data
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

matplotlib.use('Agg')
from matplotlib import pyplot as plt
import base64
from io import BytesIO
from PIL import Image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MathsWebsite.settings')
django.setup()

from rowing_quiz.models import Round, Quiz


def create_quiz():
    rounds = []
    rounds.append('Rowing History')
    rounds.append('Film')
    rounds.append('Music')
    rounds.append('Guess the Blade')
    rounds.append('Rowing Technical')
    rounds.append('Sport')
    rounds.append('Maths and Science')
    rounds.append('Guess the Baby')

    Quiz.objects.all().delete()
    Round.objects.all().delete()
    quiz = Quiz.objects.create(
        quiz_name="boathouse_quiz"
    )
    for r in range(len(rounds)):
        Round.objects.create(
            quiz=quiz,
            round_name=rounds[r],
            round_number=r + 1,
        )
    return quiz


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0)
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def offset_image(x, y, ax):
    img = plt.imread(r'homepage/static/rowers.png')
    im = OffsetImage(img, zoom=0.03)
    im.image.axes = ax
    x_offset = -30
    ab = AnnotationBbox(im, (x, y), xybox=(x_offset, 0), frameon=False,
                        xycoords='data', boxcoords="offset points", pad=0)
    ax.add_artist(ab)


def generate_results_chart(results):
    fig, ax = plt.subplots()

    crews = [r[0] for r in results]
    values = np.array([r[1] for r in results])
    # labels = [f'{r[0]}\n{r[1]}' for r in results]
    labels = [f'{r[0]} - {r[1]}' for r in results]

    height = 0.9
    bar_h = plt.barh(y=crews, width=values, height=height, align='center', alpha=0, color="red")
    ax.bar_label(bar_h, labels=labels, color='white', fontsize=7)

    max_value = values.max()
    for i, (label, value) in enumerate(zip(crews, values)):
        offset_image(value, i, ax=plt.gca())
    plt.subplots_adjust(left=0.15)

    fig.set_facecolor('#5485b3')
    ax.set_facecolor('#5485b3')
    plt.axis('off')
    plt.tight_layout()
    fig.set_size_inches(10.5, 5.5)
    chart = get_graph()
    return chart


def generate_podium(results):
    img = Image.open(r'homepage/static/rowers.png')
    text = "Hello World!"
    font = ImageFont.truetype('Inconsolata-Light.ttf', 162)
    draw = ImageDraw.Draw(img)
    draw.text((1240, 1600), text, font=font, fill='white')
    podium = get_graph()
    return podium
