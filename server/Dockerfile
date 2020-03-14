FROM python:3

WORKDIR /home/server/

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app" ]