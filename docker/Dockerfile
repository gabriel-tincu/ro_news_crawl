FROM python:jessie
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
WORKDIR /app/news
CMD python main.py