from flask import Flask, request, g, render_template

DEBUG = True

app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.config.from_object(__name__)
# app.config.from_pyfile("config.py")
app.secret_key = "teacup-testing"


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


@app.route('/helloworld', methods=['POST'])
def hello():
    data = request.form 
    data = dict(data)
    review = data['foo'][0]
    result = this_is_magic(review)
    return result


@app.route('/')
def main():
    return render_template('main.html')

def this_is_magic(review):
    # TODO implement your function here
    return 'result: {}'.format(review)

# @app.errorhandler(401)
# def internal_server_error(e):
#     return render_template('errors/401.html'), 401


# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('errors/404.html'), 404


# @app.errorhandler(403)
# def forbidden(e):
#     return render_template('errors/403.html'), 403


# @app.errorhandler(500)
# def internal_server_error(e):
#     return render_template('errors/500.html'), 500