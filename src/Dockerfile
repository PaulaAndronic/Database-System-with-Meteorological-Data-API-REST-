FROM python:3.8-slim-buster
COPY ./src/requirements.txt requirements.txt
COPY ./src/server.py /app/server.py
RUN pip3 install -r requirements.txt
WORKDIR /app
CMD python server.py