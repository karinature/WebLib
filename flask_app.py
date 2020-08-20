# A very simple Flask Hello World app for you to get started with...

from flask import Flask, jsonify
from flask import render_template, make_response, redirect, url_for, request
from flask_wtf import FlaskForm

import random  # todo remove

app = Flask(__name__)

# Also, just to help in case you’ve made a typo in the code somewhere, add this line just after the line that says
# app = Flask(__name__)
app.config["DEBUG"] = True  # todo fixme remove this in production!!!

from flask_sqlalchemy import SQLAlchemy

# SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{db_name}".format(
#     username="karinature",
#     password="dsmiUw2sn",
#     hostname="karinature.mysql.pythonanywhere-services.com",
#     db_name="karinature$tryout",
# )
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{db_name}".format(
    username="root",
    password="123",
    hostname="localhost",
    db_name="tryout",
)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# example table module todo move to a different file (aux/migration/once_off)
class ExampleEntry(db.Model):
    __tablename__ = "check"

    int_value_col = db.Column(db.Integer, primary_key=True)
    text_value_col = db.Column(db.String(4096))


# class Login(Form):
#     login_user = TextField('Username', [validators.Required()])
#     login_pass = PasswordField('Password', [validators.Required()])


# ++++++++++++  dbg page ++++++++++++
@app.route('/check', methods=['GET', 'POST'])
def check_check():
    if request.method == 'GET':
        return render_template('check.html', comments=ExampleEntry.query.all())
    print(request.form.get("contents"))
    print(request.form.get("contents2"))
    if "contents2" in request.form:
        comment_contents = request.form["contents2"] + " (from 2nd field)"
    else:
        comment_contents = request.form["contents"] + " (from 1nd field)"
    comment = ExampleEntry(text_value_col=comment_contents, int_value_col=random.randint(3, 9))
    db.session.add(comment)
    db.session.commit()
    return redirect('/check')


@app.route('/search-results', methods=['GET', 'POST'])
def search_results():
    return render_template('search-results.html')


@app.route('/book-indices')
def book_indices():
    return render_template('book-indices.html')


@app.route('/subject-list')
# @app.route('/subject-list.html')
def subject_list():
    return render_template('subject-list.html')
    # return render_template(url_for('subject_list')+'.html')


# @app.route('/#', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
# @app.route('/index', methods=['GET', 'POST'])
# @app.route('/index#', methods=['GET', 'POST'])
def home():
    if 'GET' == request.method:
        print('INDEX - GET')
        return render_template('index.html')

    print('INDEX - POST')
    print(request.form.to_dict())
    print(request.form)
    print(request.form.keys().__str__())
    print()

    fields = [
        "search-subject",
        "second-keyword",
        "search-author",
        "search-work",
        "search-reference"
    ]
    # print("fields: ", fields)
    print(request.form.get("search-subject"))
    if fields[0] in request.form:
        print('INDEX - fields[0]')
        print(request.form.get(fields[0]))
    else:
        print("whhhhhhtttttttt")
    if fields[1] in request.form:
        print('INDEX - fields[1]')
        print(request.form.get(fields[1]))
    if fields[2] in request.form:
        print('INDEX - fields[2]')
        print(request.form.get(fields[2]))
    #     print(request.form.to_dict())
    # print(url_for('search_results'))
    # print(url_for('home'))
    # collect fields
    # depending on which fields/form filled - choose a search function
    # next page should receive the results of the function as params
    # like so:         return render_template('check.html', comments=ExampleEntry.query.all())
    # but first try like this         redirect(url_for("search_results", comments=ExampleEntry.query.all()))

    # create a class for the forms?
    # you MUST make sure to be safe from SQL injection and other X

    # in the search-results do
    #   change get to render with params
    #   change html to create/fill new data ("you searched for...", "total #results..")
    #   consider running the functions in "search-result" and NOT "home"
    return redirect(url_for("search_results"))


@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('page_not_found.html'), 404)
    resp.headers['X-Something'] = 'A value'
    print(error)
    return resp
