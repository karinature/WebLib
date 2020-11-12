import datetime

from flask_wtf import FlaskForm, RecaptchaField
from markupsafe import Markup
from wtforms import *
from wtforms.validators import *

# from wtforms import (StringField,
#                      TextAreaField,
#                      SubmitField,
#                      PasswordField,
#                      DateField,
#                      SelectField, validators)
# from wtforms.validators import (DataRequired,
#     # Note there is a distinction between this and DataRequired in that
#     # InputRequired looks that form-input data was provided, and DataRequired looks at the post-coercion data.
#                                 Email,
#                                 EqualTo,
#                                 Length,
#                                 URL, Optional)
from wtforms.widgets import html_params, TextInput

EMPTY_LABEL = ''


class SearchSubject(FlaskForm):
    subject_keyword_1 = StringField(
        EMPTY_LABEL,
        [DataRequired(message='Did you forget to insert a search keyword'),
         validators.Regexp('^\w+$', message="Field accepts one search word")],
        render_kw={'placeholder': 'Subject'})
    subject_keyword_2 = StringField(EMPTY_LABEL,
                                    [Optional(), validators.Regexp('^\w+$', message="Field accepts one search word")],
                                    render_kw={'placeholder': '(Optional) Subject'})
    submit_subject = SubmitField('Search',
                                 render_kw={'class': 'btn-primary', }
                                 #            # 'style': 'float: right',
                                 #            # 'onclick': "alert('Fetching Data...')"
                                 #            }
                                 )


centuries = [('Any', 'Any'),
             ('8 BCE', '8 BCE'),
             ('7 BCE', '7 BCE'),
             ('6 BCE', '6 BCE'),
             ('5 BCE', '5 BCE'),
             ('4 BCE', '4 BCE'),
             ('3 BCE', '3 BCE'),
             ('2 BCE', '2 BCE'),
             ('1 BCE', '1 BCE'),
             ('1 CE', '1 CE'),
             ('2 CE', '2 CE'),
             ('3 CE', '3 CE'),
             ('4 CE', '4 CE'),
             ('5 CE', '5 CE'),
             ('6 CE', '6 CE'),
             ('7 CE', '7 CE'),
             ('8 CE', '8 CE')]
languages = [
    ('Any', 'Any'),
    ('Aramaic', 'Aramaic'),
    ('Arabic', 'Arabic'),
    ('Greek', 'Greek'),
    ('Hebrew', 'Hebrew'),
    ('Latin', 'Latin'),
    ('Syriac', 'Syriac')
]


class ExpenseItem(Form):
    expense_name = StringField('Expense_Item', validators=[DataRequired()])
    cost = FloatField('Cost', validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d',
                         validators=[DataRequired()],
                         default=datetime.datetime.today().date())
    type = SelectField('Role', choices=[
        ('mutual', 'Mutual'),
        ('personal#1', 'Personal #1'),
        ('personal#2', 'Personal #2')
    ])


class ExpensesForm(FlaskForm):
    """A collection of expense items."""
    items = FieldList(FormField(ExpenseItem), min_entries=1)


class Include(FlaskForm):
    include = StringField(render_kw={'placeholder': 'Subject'})


class Exclude(FlaskForm):
    exclude = StringField(render_kw={'placeholder': 'Subject'})


class FilterForm(FlaskForm):
    """Sign up for a user account."""
    # email = StringField('Email', [
    #     Email(message='Not a valid email address.'),
    #     DataRequired()])

    # <!--sub-subject filtering options-->
    includes = FieldList(
        # 'Including ',  # fixme remove *all* [Optional()] ?
        FormField(Include), min_entries=1, label='Includes'
    )
    excludes = FieldList(
        # 'Including ',  # fixme remove *all* [Optional()] ?
        FormField(Exclude), min_entries=1, label='Excludes'
    )

    # <!--text and reference filtering options-->
    # Dont delete this: https://gist.github.com/Overdese/abebc48e878662377988
    from_century = SelectField('From ', id="from-century-dl",
                               choices=centuries,
                               )
    to_century = SelectField('To ', id="to-century-dl",
                             choices=centuries,
                             )
    language = SelectField('Language ', id="language-dl",
                           choices=languages,
                           # render_kw={'style': 'margin-left: 20px; float: right'},
                           )
    ancient_author = StringField('Ancient Author ',
                                 render_kw={'placeholder': ' (In English)'}
                                 )
    ancient_title = StringField('Ancient Work-Title ',
                                render_kw={'placeholder': ' (In English)'}
                                )
    reference = StringField('Reference ',
                            render_kw={
                                'placeholder': '(e.g., 1.1 for chapter 1 verse 1, or leave empty for whole work)'}
                            )
    fetch_full = BooleanField('Fetch full text', id='fetch_full_chkbox',
                              render_kw={'class': 'inline-radio', 'style': '',
                                         # 'onClick': 'displayWarningFetchAllChkbx()',
                                         'onClick':  # todo remove alert?
                                             "alert('Attention! Checking this box will attempt full text fetching, which can result in very highly loading times.')"}
                              )
    attention_label = Label(
        text='(Attention: Checking this box will attempt full text fetching,'
             '\nwhich can result in very highly loading times.)',
        field_id=fetch_full)
    fetch_results = SubmitField('Fetch Results',
                                render_kw={'class': 'btn btn-lg btn-primary',
                                           'style': 'margin-right: 5%; padding:1rem 4rem 1rem 4rem; position: sticky; float: right',
                                           # 'onclick': "alert('Fetching Data...')"
                                           }
                                )

    # clean_button = ('Clear all fields')


class SearchReference(FlaskForm):

    def any_fields_filled(self):
        return any([self.search_author.data, self.search_work.data, self.search_reference.data])

    def validate(self):
        return self.any_fields_filled()

    search_author = StringField(
        'Author\'s name',
        [Optional()],  # , validators.Regexp('^\w+$', message="Field accepts one search word")],
        render_kw={'placeholder': 'Author\'s name'})
    search_work = StringField(
        'Work',
        [Optional()],  # , validators.Regexp('^\w+$', message="Field accepts one search word")],
        render_kw={'placeholder': 'Work'})
    search_reference = StringField(
        'Reference',
        [Optional()],  # , validators.Regexp('^\w+$', message="Field accepts one search word")],
        render_kw={'placeholder': 'Reference'})
    submit_reference = SubmitField('Submit',
                                   # render_kw={'class': 'btn btn-lg btn-primary',
                                   #            # 'style': 'float: right',
                                   #            # 'onclick': "alert('Fetching Data...')"
                                   #            }
                                   )


class SearchTypeChoice(FlaskForm):
    r_field = RadioField(
        'Label',
        choices=[(1, 'Search by Subject'), (0, 'Search by Reference')],
        render_kw={'class': 'inline-radio', 'style': ''}
        # render_kw={'class': 'inline-radio',
        # 'style': 'font-size:1.5em; vertical-align: middle; horizontal-align: middle;text-align: center'}
    )

# class SignupForm(FlaskForm):
#     """Sign up for a user account."""
#     # email = StringField('Email', [
#     #     Email(message='Not a valid email address.'),
#     #     DataRequired()])
#     # background_color = ColorField() # from wtforms_components import If, ColorField
#     password = PasswordField('Password', [
#         DataRequired(message="Please enter a password."),
#     ])
#     confirmPassword = PasswordField('Repeat Password', [
#         EqualTo(password, message='Passwords must match.')
#     ])
#     title = SelectField('Title', [DataRequired()],
#                         choices=[('Farmer', 'farmer'),
#                                  ('Corrupt Politician', 'politician'),
#                                  ('No-nonsense City Cop', 'cop'),
#                                  ('Professional Rocket League Player', 'rocket'),
#                                  ('Lonely Guy At A Diner', 'lonely'),
#                                  ('Pokemon Trainer', 'pokemon')])
#     website = StringField('Website', validators=[URL()])
#     birthday = DateField('Your Birthday')
#     recaptcha = RecaptchaField()
#     body = StringField('Message',
#                        [DataRequired(),
#                         Length(min=4, message='Your message is too short.')])
#     submit = SubmitField('Submit')
#     # ,validators=[
#     # If(lambda form, field: form.user_id.data, Email())])
