from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import HttpOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import json
import pandas as pd
import boto3
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from io import StringIO




def kelvin_to_fahrenheit(k):
    return (k - 273.15) * 9/5 + 32


def transform_load_data(ti):
    data = ti.xcom_pull(task_ids="extract_weather_data")

    transformed = {
        "City": data["name"],
        "Description": data["weather"][0]["description"],
        "Temp_F": kelvin_to_fahrenheit(data["main"]["temp"]),
        "Feels_Like_F": kelvin_to_fahrenheit(data["main"]["feels_like"]),
        "Min_Temp_F": kelvin_to_fahrenheit(data["main"]["temp_min"]),
        "Max_Temp_F": kelvin_to_fahrenheit(data["main"]["temp_max"]),
        "Pressure": data["main"]["pressure"],
        "Humidity": data["main"]["humidity"],
        "Wind_Speed": data["wind"]["speed"],
        "Time": datetime.utcfromtimestamp(data["dt"])
    }

    df = pd.DataFrame([transformed])

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)


    s3_hook = S3Hook(aws_conn_id="aws_default")
    filename = f"weather_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    s3_hook.load_string(
        string_data=csv_buffer.getvalue(),
        key=f"weather/{filename}",
        bucket_name="weather-api-airflow-mhk",
        replace=True
    )


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    "weather_api_to_s3",
    default_args=default_args,
    schedule="@daily",
    catchup=False
) as dag:

    is_api_ready = HttpSensor(
        task_id="is_api_ready",
        http_conn_id="weathermap_api",
        endpoint="/data/2.5/weather?q=Portland&appid=c021055779afc65c1d55f3761e58af1a"
    )

    extract_weather_data =  HttpOperator(
        task_id="extract_weather_data",
        http_conn_id="weathermap_api",
        endpoint="/data/2.5/weather?q=Portland&appid=c021055779afc65c1d55f3761e58af1a",
        method="GET",
        response_filter=lambda r: json.loads(r.text),
        log_response=True,
    )

    transform_load = PythonOperator(
        task_id="transform_load",
        python_callable=transform_load_data,
    )

    is_api_ready >> extract_weather_data >> transform_load
