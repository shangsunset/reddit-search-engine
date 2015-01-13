from flask import Flask, url_for, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
Bootstrap(app)

class SearchForm(Form):
    user_query = StringField('user_query', validators=[DataRequired()])
    search_button = SubmitField('Search')

@app.route('/', methods=('GET', 'POST'))
def index():
    search_form = SearchForm(csrf_enabled=False)
    if search_form.validate_on_submit():
        return redirect(url_for('search_results', user_query=search_form.user_query.data))
    return render_template('index.html', form=search_form)

@app.route('/search_results/<user_query>')
def search_results(user_query):
    return render_template('search_results.html', query=user_query)

if __name__ == '__main__':
    app.run(debug=True)
