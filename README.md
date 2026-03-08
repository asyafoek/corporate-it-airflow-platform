# corporate-it-airflow-platform

# This will add the repo locally
helm repo add apache-airflow https://airflow.apache.org
helm repo update

# This will create a subdir airflow in src/resources
helm pull apache-airflow/airflow --version 1.19.0 --untar --untardir src/resources


kubectl get namespace corporate-it-airflow || kubectl create namespace corporate-it-airflow

helm upgrade --install airflow src/resources/airflow --namespace corporate-it-airflow -f src/resources/airflow/values.yaml --atomic --wait