FROM python:3.7

COPY ./requirements.txt /service/requirements.txt

COPY ./crawler /service/crawler

COPY ./configs /service/configs

WORKDIR /service

RUN pip install -r requirements.txt

RUN [ "python", "-c", "import nltk; nltk.download('stopwords')" ]

EXPOSE 8000

CMD python -m crawler
