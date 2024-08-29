# syntax=docker/dockerfile:1
FROM python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/hp/backend
WORKDIR $APP_HOME

RUN apt-get update

# install dependencies
RUN apt-get install -yyq netcat-traditional
RUN apt-get install -y iputils-ping
RUN pip install --upgrade pip
RUN pip install gunicorn

# database Postgress dependencies
RUN pip install psycopg2-binary


# install requirments
COPY requirements.txt $APP_HOME/
RUN pip install --no-cache-dir -r requirements.txt


COPY . $APP_HOME/


COPY entrypoint.sh $APP_HOME/
RUN chmod +x  $APP_HOME/entrypoint.sh


ENTRYPOINT ["sh", "/hp/backend/entrypoint.sh"]