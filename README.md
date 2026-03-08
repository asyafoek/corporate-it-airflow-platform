# corporate-it-airflow-platform

# This will add the repo locally
helm repo add apache-airflow https://airflow.apache.org
helm repo update

# This will create a subdir airflow in src/resources
helm pull apache-airflow/airflow --version 1.19.0 --untar --untardir src/resources


kubectl get namespace corporate-it-airflow || kubectl create namespace corporate-it-airflow

helm upgrade --install airflow src/resources/airflow --namespace corporate-it-airflow -f src/resources/airflow/values.yaml --debug


kubectl port-forward svc/airflow-api-server 8080:8080 --namespace corporate-it-airflow


python3 -c 'import secrets; print(secrets.token_hex(16))'

b08f9e08a0b9eae3dcb2cf629f9afdd6

values.yaml replace
apiSecretKeySecretName: my-api-secret


kubectl apply -f src/resources/secrets/my-api-secret.yaml

# Notes
Thank you for installing Apache Airflow 3.1.7!

Your release is named airflow.
You can now access your dashboard(s) by executing the following command(s) and visiting the corresponding port at localhost in your browser:
Airflow API Server:     kubectl port-forward svc/airflow-api-server 8080:8080 --namespace corporate-it-airflow
Default user (Airflow UI) Login credentials:
    username: admin
    password: admin
Default Postgres connection credentials:
    username: postgres
    password: postgres
    port: 5432

You can get Fernet Key value by running the following:

    echo Fernet Key: $(kubectl get secret --namespace corporate-it-airflow airflow-fernet-key -o jsonpath="{.data.fernet-key}" | base64 --decode)


#####################################################
#  WARNING: You should set a static API secret key  #
#####################################################

You are using a dynamically generated API secret key, which can lead to
unnecessary restarts of your Airflow components.

Information on how to set a static API secret key can be found here:
https://airflow.apache.org/docs/helm-chart/stable/production-guide.html#api-secret-key
[root@PDTWINCAM000014 corporate-it-airflow-platform]# helm list -n corporate-it-airlfow