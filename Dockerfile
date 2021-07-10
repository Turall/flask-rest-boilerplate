FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN pip install --upgrade pip
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80
