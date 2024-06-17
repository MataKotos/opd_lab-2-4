from flask import Flask, render_template, request
import math

app = Flask(__name__)


def get_discriminant(a, b, c):
    d = b ** 2 - (4 * a * c)
    return d


def get_x1(a, b, d):
    if d >= 0:
        x1 = (-b + math.sqrt(d)) / (2 * a)
    else:
        x1 = "Нет решения"

    return x1


def get_x2(a, b, d):
    if d > 0:
        x2 = (-b - math.sqrt(d)) / (2 * a)
    else:
        x2 = "Нет решения"

    return x2


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/', methods=['post', 'get'])
def form():
    d = ''
    x1 = ''
    x2 = ''

    if request.method == 'POST':
        a = int(request.form.get('a'))
        b = int(request.form.get('b'))
        c = int(request.form.get('c'))

        d = get_discriminant(a, b, c)
        x1 = get_x1(a, b, d)
        x2 = get_x2(a, b, d)

    return render_template('index.html', d=d, x1=x1, x2=x2)


if __name__ == '__main__':
    app.run()