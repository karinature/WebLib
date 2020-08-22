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
        comment_contents = request.form["contents"] + " (from 1st field)"
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
def subject_list():
    return render_template('subject-list.html')
    # return render_template(url_for('subject_list')+'.html')


# example table module todo move to a different file (aux/migration/once_off)
class TextsSubjectsEntry(db.Model):
    __tablename__ = "texts_subjects"

    indexa = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(4096))
    C = db.Column(db.String(4096))
    # i


# @app.route('/#', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
# @app.route('/index', methods=['GET', 'POST'])
# @app.route('/index#', methods=['GET', 'POST'])
def home():
    if 'GET' == request.method:
        print('INDEX - GET')
        return render_template('index.html')

    print('INDEX - POST')
    # print(request.form.to_dict())
    # print(request.form)

    fields = [
        "search-subject",
        "second-keyword",
        "search-author",
        "search-work",
        "search-reference"
    ]
    print(request.form.get("search-subject"))
    for i in range(len(fields)):
        if fields[i] in request.form:
            print()
            # print("index() - field [", i, "]")
            # print(request.form.get(fields[i]))
        else:
            print()
            # print("whhhhhhtttttttt")

    # return redirect(url_for("search_results"), )

    # todo
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

    # change projection to include entire entry instead of indexa alone
    # add fuzzy (returns things *like* but not necessarily the same) / regex search on the query
    # clean data before:
    #   split creation of tables function in db-migration into multiple function
    #   appropriate normalization

    search_word = request.form[fields[0]]
    if search_word == "":
        pass

    # db = None

    dds = []
    if search_word:
        c2 = "'%" + search_word + "%'"
        # sql_for_df_sub = "SELECT * FROM texts_subjects WHERE subject like " + c2

        results = db.session.query(TextsSubjectsEntry).filter_by(subject=search_word)

        # texts_subjects2 = texts_subjects1[
        #     texts_subjects1["subject"].str.contains('\\b' + search_word + '\\b', case=False, na=False)]
        # # texts_subjects3 = texts_subjects1[
        #     # texts_subjects1["subject"].str.contains('\\b' + search_word + 's\\b', case=False, na=False)]
        # texts_subjects1 = pd.concat([texts_subjects2, texts_subjects3])
        # subjects = texts_subjects1['subject'].values.tolist()
        # # texts_subjects1["C"] = texts_subjects1["C"].apply(hyphenate)
        # cs = texts_subjects1['C'].values.tolist()
        # ccs = [item for sublist in cs for item in sublist]
        # lccs = len(ccs)
        # pd.set_option('display.max_colwidth', -1)
        # if option == "and":
        #     # d2 = "'%" + get_d_from_form + "%'"
        #     # sql_for_df_sub_d = "SELECT * FROM texts_subjects WHERE subject like " + d2
        #     d_texts_subjects = pd.read_sql_query(sql_for_df_sub_d, db)
        #     d_subjects = d_texts_subjects['subject'].values.tolist()
        #     d_texts_subjects["C"] = d_texts_subjects["C"].apply(hyphenate)
        #     ds = d_texts_subjects['C'].values.tolist()
        #     dds = [item for sublist in ds for item in sublist]

        print(results.all())

        return redirect(url_for("search_results"), )



@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('page_not_found.html'), 404)
    resp.headers['X-Something'] = 'A value'
    print(error)
    return resp
