FROM apache/airflow:2.9.0

USER airflow

COPY requirements.txt /opt/airflow/requirements.txt

RUN pip install --no-cache-dir --force-reinstall "urllib3<2" && \
    pip install --no-cache-dir -r /opt/airflow/requirements.txt

ENV AIRFLOW__CORE__LOAD_EXAMPLES=False

WORKDIR /opt/airflow

