from flask import Flask, request, g, render_template

DEBUG = True

app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.config.from_object(__name__)


# clear cache
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.

    :param response: flask response object
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.route('/predict-plot', methods=['POST'])
def hello():
    data = request.form 
    data = dict(data)
    review = data['review'][0]
    result = this_is_magic(review)
    for sentence in result['sentiment']:
        temp = sentence['predict'][0]
        sentence['predict'] = result['class'][temp.index(max(temp))]
    temp = result['overall'][0]
    result['overall'] = result['class'][temp.index(max(temp))]
    return render_template('home.html', result=result)

@app.route('/try-again', methods=['POST'])
def try_again():
    return render_template('home.html', result=None)

@app.route('/')
def main():
    return render_template('home.html', result=None)


def this_is_magic(plot):
    # TODO implement your function here : PAUL
    dummy = {
        "sentiment": [
            {
                "valid": True,
                "sentence": "i love you.",
                "predict": [
                    [
                        0.3040249357283957,
                        0.43088548910308844,
                        0.5788311780106976,
                        0.5354991246705849,
                        1,
                        0.14993613977722606,
                        0.22420728456749758
                    ]
                ]
            },
            {
                "valid": True,
                "sentence": "do you love me?",
                "predict": [
                    [
                        0.21856044480658934,
                        0.3747954272600018,
                        0.6596356936709812,
                        0.5497932681960965,
                        0.7454909465283363,
                        0.10636281471273593,
                        0.18044102482946542
                    ]
                ]
            },
            {
                "valid": True,
                "sentence": "no, we should be friend.",
                "predict": [
                    [
                        0.4031267249794135,
                        0.545241195629784,
                        0.6825621038534601,
                        0.5145061945373703,
                        0.5476750846732398,
                        0.2206336010794257,
                        0.28113322836978183
                    ]
                ]
            }
        ],
        "class": [
            "genre_action",
            "genre_adventure",
            "genre_comedy",
            "genre_drama",
            "genre_romance",
            "genre_sci-fi",
            "genre_thriller"
        ],
        "overall": [
            [
                0.054849286502729924,
                0.11592233039656072,
                0.6595044625658695,
                0.3791272927329301,
                0.5800935401948554,
                0.022056351625011576,
                0.043126898376971146
            ]
        ]
    }
    return dummy
    # return render_template('home.html', result='foo bar')


@app.route('/random')
def random_plot():
    # TODO random the plot : PAUL
    return 'this is a random plot'