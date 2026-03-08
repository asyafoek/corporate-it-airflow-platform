# Kies de Airflow + Python combi die je gebruikt in de chart
FROM apache/airflow:2.10.5-python3.11

# (Optioneel) kleine hygiene: pip updaten als 'airflow' user
USER airflow
RUN python -m pip install --no-cache-dir --upgrade pip

# Klaar: geen extra APT of pip packages,
# de entrypoint/CMD komen al uit de officiële base image.