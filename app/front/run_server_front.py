import wtforms as wtforms
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

import urllib.request
import json


class ClientDataForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    channel_title = StringField('Channel Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    tags = StringField('Tags', validators=[DataRequired()])
    comments_disabled = BooleanField('Comments Disabled', validators=[DataRequired()])
    views = StringField('Views', validators=[DataRequired()])


app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)

clm_list = ['title', 'channel_title', 'tags', 'description', 'comments_disabled', 'views']


def get_prediction(title, channel_title, tags, description, comments_disabled, views=50000, ratings_disabled=False):
    body = {'title': title,
            'channel_title': channel_title,
            'tags': tags,
            'description': description,
            'comments_disabled': comments_disabled,
            'ratings_disabled': ratings_disabled,
            'views': views,
            }

    myurl = "http://127.0.0.1:8180/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)
    return json.loads(response.read())



@app.route('/predicted/<response>')
def predicted(response):
    response = json.loads(response.replace("'", '"'))
    print(response)
    return render_template('predicted.html', response=response)


@app.route('/', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    if request.method == 'POST':
        for clm in clm_list:
            data[clm] = request.form.get(clm)

        data['comments_disabled'] = data['comments_disabled'] == 'on'

        try:
            response = get_prediction(data['title'],
                                      data['channel_title'],
                                      data['tags'],
                                      data['description'],
                                      data['comments_disabled'],
                                      data['views']
                                      )
            print(response)
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        return redirect(url_for('predicted', response=response))
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)
