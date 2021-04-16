FROM python:3
LABEL maintainer="olasodeadeyemi@gmail.com"
LABEL description="Activity service for saving and retrieving historical events"

WORKDIR /

COPY . /

RUN pip install -r requirements.txt

EXPOSE 5000

# Start processes
CMD ["flask", "run", "--host=0.0.0.0"]