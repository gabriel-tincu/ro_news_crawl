FROM python:jessie
ADD . /app
WORKDIR /app
RUN echo "deb http://ftp.us.debian.org/debian unstable main contrib non-free" > /etc/apt/sources.list.d/unstable.list
RUN pip install -r requirements.txt
WORKDIR /app/news
CMD python main.py