FROM python:3.10.13

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /fastapi_app


RUN chmod a+x app.sh

# For deploying
#WORKDIR cd src
#
#CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
