from flask import Flask, url_for, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from indexer import Searcher

app = Flask(__name__)
Bootstrap(app)
searcher = Searcher("indexes")

class SearchForm(Form):
    user_query = StringField('User Query', validators=[DataRequired()])
    search_button = SubmitField('Search')

@app.route('/', methods=('GET', 'POST'))
def index():
    search_form = SearchForm(csrf_enabled=False)
    if search_form.validate_on_submit():
        return redirect(url_for('search_results', user_query=search_form.user_query.data))
    return render_template('index.html', form=search_form)

@app.route('/search_results/<user_query>')
def search_results(user_query):
    pos_and_docId = searcher.find_doc(user_query.split(" "))
    urls = [searcher.get_doc_url(str(id)) for pos, id in pos_and_docId]
    return render_template('search_results.html', query=user_query, urls=urls)

if __name__ == '__main__':
    app.run(debug=True)
