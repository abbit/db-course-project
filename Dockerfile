FROM python:3.10.4
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/app/
COPY requirements.txt /usr/app
RUN pip install -r requirements.txt
COPY . /usr/app/
