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
    query_terms = user_query.split(" ")
    doc_ids = searcher.find_doc_AND(user_query.split(" "))
    print doc_ids
    urls = [searcher.get_doc_url(str(id)) for id in doc_ids]
    # docs_text = [searcher.generate_snippet(query_terms, str(id)) for id in doc_ids]
    docs_text = [" ".join(searcher.generate_snippet(query_terms, str(id))) for id in doc_ids]
    return render_template('search_results.html', query=user_query, urls_and_docs_text=zip(urls, docs_text))

if __name__ == '__main__':
    app.run(debug=True)
