FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir ./logs/
RUN touch ./logs/bot.log
COPY ./src ./src
COPY ./conf ./conf

CMD ["python", "src/bot.py"]