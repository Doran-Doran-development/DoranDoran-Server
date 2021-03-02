FROM python:3.7
WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
RUN python dorandoran/manage.py collectstatic

EXPOSE 8000
ENV DJANGO_SETTINGS_MODULE config.settings.dev
CMD ["gunicorn", "dorandoran.config.asgi:application", "--port", "8000"]