FROM python:3
LABEL maintainer="olasodeadeyemi@gmail.com"
LABEL description="Activity service for saving and retrieving historical events"

WORKDIR /usr/src/service

COPY . /usr/src/service

RUN pip install -r requirements.txt

EXPOSE 5000

# Start processes
CMD ["./entrypoint.sh"]
