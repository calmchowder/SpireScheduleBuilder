from flask import Flask, render_template, request, redirect
from subjects import subjects # list of subject names
from SpireBackEnd.Course import *
from SpireBackEnd.Discussion import *
from SpireBackEnd.Lecture import *
from SpireBackEnd.Scraper import *

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html', subjects=subjects)


@app.route('/submit', methods=['POST'])
def submit():
    subject = ''
    number = ''

    if 'subject' in request.form:
        subject = request.form['subject']
    if 'number' in request.form:
        number = request.form['number']
    if number == '':
        return render_template('index.html', subjects=subjects, number_exists=False)
    get_all_data(subject, int(number))
    return redirect('/')



if __name__ == '__main__':
    app.run()
