FROM python:alpine3.7

COPY . /article_filter
WORKDIR /article_filter

RUN pip install -r requirements.txt

CMD [ "python", "./index.py" ]