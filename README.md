A production-ready ETL pipeline that extracts real-time weather data from OpenWeatherMap API, transforms it using Python, and loads it into AWS S3. Built with Apache Airflow and containerized with Docker for seamless orchestration and deployment.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.0+-red.svg)
![AWS](https://img.shields.io/badge/AWS-S3-orange.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)

## 🚀 Architecture Overview
```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────────┐
│ Weather API │ -> │ Airflow DAG  │ -> │ Transform    │ -> │  AWS S3 │
│ (OpenWeather)│    │ Orchestration│    │ (Pandas)     │    │  (CSV)  │
└─────────────┘    └──────────────┘    └──────────────┘    └─────────┘
```

### Pipeline Stages
1. **Check** - Verify API availability
2. **Extract** - Fetch weather data from API
3. **Transform** - Process and structure data
4. **Load** - Upload to AWS S3

## 🛠️ Tech Stack

- **Orchestration**: Apache Airflow
- **Containerization**: Docker, Docker Compose
- **Data Processing**: Python, Pandas
- **Cloud Storage**: AWS S3 (Boto3)
- **Data Source**: OpenWeatherMap API

## 📂 Project Structure
```
weather-etl-pipeline/
├── dags/
│   └── weather_api_to_s3.py      # Main Airflow DAG
├── docker-compose.yml             # Docker services configuration
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
└── README.md
```

## ⚙️ DAG Configuration

| Property | Value |
|----------|-------|
| **DAG Name** | `weather_api_to_s3` |
| **Schedule** | Daily (`@daily`) |
| **Catchup** | Disabled |
| **Start Date** | 2024-01-01 |

### 🧩 Tasks

#### 1️⃣ `is_api_ready` (HttpSensor)
- Checks OpenWeatherMap API availability
- Prevents downstream failures
- Timeout: 120 seconds

#### 2️⃣ `extract_weather_data` (HttpOperator)
- Fetches real-time weather data
- Stores response in XCom for downstream tasks
- Error handling for API failures

#### 3️⃣ `transform_load` (PythonOperator)
- **Transform**:
  - Converts Kelvin → Fahrenheit
  - Normalizes data structure
  - Converts timestamps to UTC
- **Load**:
  - Serializes to CSV (in-memory)
  - Uploads to S3 with timestamped filename

## 🧠 Data Transformations
```python
# Temperature Conversion
temp_fahrenheit = (temp_kelvin - 273.15) * 9/5 + 32

# Data Structure
{
    "City": "Portland",
    "Description": "clear sky",
    "Temp_F": 72.5,
    "Feels_Like_F": 70.3,
    "Min_Temp_F": 68.0,
    "Max_Temp_F": 75.0,
    "Pressure": 1013,
    "Humidity": 65,
    "Wind_Speed": 5.2,
    "Time": "2024-02-08 11:26:45"
}
```

## ☁️ AWS S3 Output

**Bucket**: `weather-api-airflow-mhk`

**Path Structure**:
```
s3://weather-api-airflow-mhk/weather/weather_YYYYMMDD_HHMMSS.csv
```

**Example**:
```
weather/weather_20260208_112645.csv
```

### Output Schema

| Column | Description |
|--------|-------------|
| `City` | City name |
| `Description` | Weather description (e.g., "clear sky") |
| `Temp_F` | Temperature in Fahrenheit |
| `Feels_Like_F` | Feels-like temperature |
| `Min_Temp_F` | Minimum temperature |
| `Max_Temp_F` | Maximum temperature |
| `Pressure` | Atmospheric pressure (hPa) |
| `Humidity` | Humidity percentage |
| `Wind_Speed` | Wind speed (m/s) |
| `Time` | UTC timestamp |

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- AWS Account with S3 access
- OpenWeatherMap API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/weather-etl-pipeline.git
cd weather-etl-pipeline
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. **Start Airflow**
```bash
docker-compose up -d
```

4. **Access Airflow UI**
```
http://localhost:8080
```
Default credentials: `airflow` / `airflow`

### Configuration

#### Airflow Connections

**HTTP Connection (Weather API)**
```
Connection ID: weathermap_api
Connection Type: HTTP
Host: https://api.openweathermap.org
```

**AWS Connection (S3)**
```
Connection ID: aws_default
Connection Type: Amazon Web Services
AWS Access Key ID: <your-access-key>
AWS Secret Access Key: <your-secret-key>
Region: us-east-1
```

## 📊 Monitoring & Execution

1. Navigate to Airflow UI
2. Enable the `weather_api_to_s3` DAG
3. Trigger manually or wait for scheduled run
4. Monitor task execution in Graph/Tree view
5. Check S3 bucket for output files

## 🧪 Testing
```bash
# Run tests (if implemented)
pytest tests/

# Validate DAG
python dags/weather_api_to_s3.py
```

## 📸 Screenshots

### Airflow DAG Graph View
![DAG Graph](screenshots/dag_graph.png)

### AWS S3 Output
![S3 Bucket](screenshots/s3_output.png)

## 🎯 Learning Outcomes

✅ Real-world ETL pipeline design  
✅ Apache Airflow orchestration & scheduling  
✅ API integration & error handling  
✅ Cloud storage (AWS S3) integration  
✅ Dockerized data engineering workflow  
✅ Production-grade configuration management  

## 🔮 Future Enhancements

- [ ] Add data quality validation checks
- [ ] Implement data partitioning by date
- [ ] Convert CSV to Parquet format
- [ ] Integrate AWS Glue Catalog
- [ ] Add Athena query support
- [ ] Implement alerting via Airflow callbacks/SLAs
- [ ] Add unit & integration tests
- [ ] Create CI/CD pipeline
- [ ] Add historical data backfill capability

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
