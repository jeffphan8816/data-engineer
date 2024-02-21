FROM apache/airflow:2.8.1-python3.10
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends openjdk-17-jre-headless gcc python3-dev libkrb5-dev \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ADD requirements.txt .

USER airflow
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt