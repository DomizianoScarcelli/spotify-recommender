FROM python:3.9

# Install Java
RUN apt-get update && apt-get install -y openjdk-11-jdk 

#Install Hadoop
# RUN wget https://archive.apache.org/dist/hadoop/core/hadoop-3.3.5/hadoop-3.3.5.tar.gz
# RUN tar hadoop-3.3.5.tar.gz
# RUN mv ./hadoop-3.3.5 /usr/lib/jvm/hadoop-3.3.5

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3004", "--reload"]
