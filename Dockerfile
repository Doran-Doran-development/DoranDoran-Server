FROM python:3.7

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/

RUN pip install -r requirements.txt

ADD . /code/

CMD ["python", "./dorandoran/manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000
