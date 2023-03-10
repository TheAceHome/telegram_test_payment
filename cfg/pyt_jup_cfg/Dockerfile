FROM python:3.9

ENV POSTGRES_USER="root"
ENV POSTGRES_PASSWORD="root"
ENV POSTGRES_DB="customers_pays"
#VOLUME C:/Users/U_M1E6D/PycharmProjects/data-engineering-zoomcamp/week_1_basics_n_setup/HW_week_1_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data

RUN pip install pandas
RUN pip install jupyter

ENTRYPOINT [ "bash" ]