FROM apache/airflow:2.9.0

USER root
RUN pip install --no-cache-dir locust
USER airflow

ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

WORKDIR /opt/airflow

