FROM python:3.7
WORKDIR /code
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE config.settings.dev
CMD ["python", "dorandoran/manage.py", "runserver", "0.0.0.0:8000"]