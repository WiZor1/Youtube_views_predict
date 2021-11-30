# Youtube_views_predict

Сервис по предсказанию потенциального количества просмотров,
лайков и дизлайков видео на YouTube исходя из их названия, описания, имени автора, тегов.

---------
## Запуск

Процесс развертки и запуска сервиса:

`docker build -t <img_name> .`<br>
`docker run -d -p 8180:8180 -p 8181:8181 -v "</path/to/model>":/app/app/models <img_name>`

Запущенный сервис находится на http://localhost:8181.

-------------
## Docker Hub

Для копирования готового образа можно воспользоваться:
`docker pull wizor1/youtube_preds`

Соответственно, образ находится <a href="https://hub.docker.com/repository/docker/wizor1/youtube_preds">здесь</a>.

-------------
## Модель

Для подготовки модели использовался датасет из открытого
источника на 
<a href="https://www.kaggle.com/datasnaek/youtube-new">Kaggle</a>.
Предварительно подготовлена предобученная модель `model.dill` на основе
`TfIdf` векторизации токенов и последующим обучением на основе
`Ridge` регрессии. Модель можно заменять на другую, удовлетворяющей требованиям:
* Иметь метод:
    * `predict(pd.DataFrame)` -> `list`*
      
        (`list` размерности 3 с `np.array` значениями отклонений от
    среднего для `[просмотров, лайков, дизлайков]`)
* Иметь переменные по средними значениями по обучающей выборке:
    * `views_mean`
    * `likes_mean`
    * `dislikes_mean`
* Принимать на вход `predict()` выборку, содержащую как минимум поля:
    * `title`: *text*
    * `channel_title`: *text*
    * `tags`: *text*
    * `description`: *text*
    * `comments_disabled`: *bool*
    

-------
## Стек

Backend:
* `numpy`
* `pandas`
* `flask`
* `docker`

Frontend:
* <a href="https://github.com/NetGeoOWild/Project-Oracle">NetGeoOWild</a>
-----
