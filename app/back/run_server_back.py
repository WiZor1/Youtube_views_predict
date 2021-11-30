import dill
import pandas as pd
import os
import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime
import re

app = flask.Flask(__name__)

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def load_model(model_path):
    with open(model_path, 'rb') as f:
        model = dill.load(f)
    return model


modelpath = "/app/app/models/model.dill"
model = load_model(modelpath)

num_clm_list = ['comments_disabled']

text_clm_list = {'title': 'текст',
                 'channel_title': 'текст',
                 'tags': 'текст',
                 'description': 'текст'
                 }

oth_clm_list = {'comments_disabled': False,
                'ratings_disabled': False,
                'video_error_or_removed': False
                }

label_list = ['views_mean', 'likes_mean', 'dislikes_mean']
df_dict = dict()


@app.route("/", methods=["GET"])
def general():
    return """Welcome to YouTube video popularity prediction process. Please use 'http://<address>/predict' to POST"""


@app.route("/predict", methods=["POST"])
def predict():
    data = dict()
    dt = strftime("[%Y-%b-%d %H:%M:%S]")
    if flask.request.method == "POST":

        request_json = flask.request.get_json()

        for clm in list(text_clm_list.keys()) + list(oth_clm_list.keys()):
            if request_json.get(clm) is not None and request_json.get(clm) != '':
                df_dict[clm] = [request_json[clm]]
            elif clm in list(text_clm_list.keys()):
                df_dict[clm] = [text_clm_list[clm]]
            else:
                df_dict[clm] = [oth_clm_list[clm]]

        if request_json.get('views', False):
            mean_views = int(request_json['views'])
        else:
            mean_views = 50000

        logger.info(f'{dt} Data: {df_dict}')
        print(df_dict, sep='\n')

        try:
            preds = model.predict(pd.DataFrame(df_dict))
        except AttributeError as e:
            logger.warning(f'{dt} Exception: {str(e)}')
            data['predictions'] = str(e)
            return flask.jsonify(data)

        data['pred_views'] = round((preds[0][0] - 1) * 100, 2)
        data['pred_likes'] = round((preds[1][0] - 1) * 100, 2)
        data['pred_dislikes'] = round((preds[2][0] - 1) * 100, 2)

        if data['pred_views'] > 10:
            v_comm = 'У тебя высокое количество просмотров! Так держать'
        elif data['pred_views'] < -10:
            v_comm = 'Просмотров достаточно мало'
        else:
            v_comm = 'Получается достаточно стабильный результат, тебя смотрят как и обычно'

        if data['pred_likes'] > 10:
            l_comm = ', а лайков-то сколько!'
        elif data['pred_likes'] < -10:
            l_comm = '.'
        else:
            l_comm = ', а лайков не много, но и не мало - твердая золотая середина.'

        if data['pred_likes'] / data['pred_dislikes'] > 10 and data['pred_likes'] > 50:
            both_comm = ' Дислайков за лайками не видать - даешь качественному названию качественный контент!'
        elif data['pred_likes'] / data['pred_dislikes'] < -10 and data['pred_likes'] > 50:
            both_comm = ' Ой закидали помидорами...'
        else:
            both_comm = ' Стабильный хороший результат.'

        data['pred_views_abs'] = int(mean_views * preds[0][0])
        data['pred_likes_abs'] = int(mean_views / model.views_mean * model.likes_mean * preds[1][0])
        data['pred_dislikes_abs'] = int(mean_views / model.views_mean * model.dislikes_mean * preds[2][0])
        data['comm'] = v_comm + l_comm + both_comm

    return flask.jsonify(data)


# if this is the main thread of execution first load the model and
# then start the server
if __name__ == '__main__':
    print(('* Loading the model and Flask starting server...'
           'please wait until server has fully started'))
    port = int(os.environ.get('PORT', 8180))
    app.run(host='0.0.0.0', debug=True, port=port)
