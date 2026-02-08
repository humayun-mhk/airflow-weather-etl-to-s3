🌦️ Weather Data ETL Pipeline using Apache Airflow & AWS S3

This project demonstrates a production-style ETL (Extract, Transform, Load) pipeline built using Apache Airflow, where real-time weather data is fetched from a public API, transformed using Python, and stored in Amazon S3 as a CSV file.

The pipeline is containerized using Docker and showcases orchestration, scheduling, monitoring, and cloud storage integration.

🚀 Architecture Overview

Data Flow:

Weather API → Airflow (ETL DAG) → Data Transformation → AWS S3 (CSV)


Pipeline Stages:

API Availability Check

Weather Data Extraction

Data Transformation

Load into Amazon S3

🛠️ Tech Stack

Apache Airflow

Docker & Docker Compose

Python

AWS S3

Pandas

Boto3

OpenWeatherMap API

📂 Project Structure
.
├── dags/
│   └── weather_api_to_s3.py
├── docker-compose.yml
├── requirements.txt
├── README.md

⚙️ Airflow DAG Description

DAG Name: weather_api_to_s3
Schedule: Daily
Catchup: Disabled

🧩 Tasks Breakdown
1️⃣ is_api_ready (HttpSensor)

Checks if the Weather API is reachable before execution.

Prevents downstream failures.

2️⃣ extract_weather_data (HttpOperator)

Fetches live weather data from OpenWeatherMap.

Pushes the response to XCom.

3️⃣ transform_load (PythonOperator)

Converts temperature from Kelvin → Fahrenheit

Selects and structures meaningful fields

Stores the transformed data as a CSV file

Uploads the file to Amazon S3

🧠 Key Transformations

Temperature conversion (Kelvin → Fahrenheit)

Data normalization using Pandas

Timestamp conversion to UTC

CSV serialization using in-memory buffers

☁️ AWS S3 Output

Bucket: weather-api-airflow-mhk

Path: weather/

Filename format:

weather_YYYYMMDD_HHMMSS.csv


Example:

weather/weather_20260208_112645.csv

🧪 Sample Output Fields
Column	Description
City	City name
Description	Weather description
Temp_F	Temperature (°F)
Feels_Like_F	Feels-like temperature
Min_Temp_F	Minimum temperature
Max_Temp_F	Maximum temperature
Pressure	Atmospheric pressure
Humidity	Humidity percentage
Wind_Speed	Wind speed
Time	UTC timestamp
🐳 Running the Project Locally
1️⃣ Start Airflow
docker-compose up -d

2️⃣ Open Airflow UI
http://localhost:8080

3️⃣ Trigger the DAG

Enable weather_api_to_s3

Trigger manually or wait for schedule

📸 Screenshots
Airflow DAG Execution

✔ All tasks executed successfully
✔ ETL completed without errors

AWS S3 Storage

✔ CSV file stored in S3 bucket
✔ Timestamped file naming

(Screenshots included in repository)

🔐 Configuration Notes

Weather API credentials are configured using Airflow HTTP Connection

AWS credentials are managed using Airflow AWS Connection

No secrets are hard-coded

🎯 Learning Outcomes

Real-world ETL pipeline design

Apache Airflow orchestration

API data ingestion

Cloud storage integration

Dockerized data engineering workflow

📌 Future Enhancements

Add data validation checks

Partition data by date

Store data in Parquet format

Integrate AWS Glue / Athena

Add alerting using Airflow callbacks
