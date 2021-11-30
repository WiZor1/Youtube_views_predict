FROM python:3.9
COPY . /app
VOLUME /app/app/models
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8180
EXPOSE 8181
CMD python /app/app/back/run_server_back.py & python /app/app/front/run_server_front.py