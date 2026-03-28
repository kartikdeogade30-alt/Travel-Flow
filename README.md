# 🚀 TravelFlow: Micro-Batch Travel Data Pipeline

## 📌 Overview

TravelFlow is an end-to-end micro-batch data pipeline designed to process travel customer data using cloud-native tools. The pipeline follows an append-only ingestion strategy and supports scalable, production-style data engineering practices.

It integrates data ingestion, transformation, storage, and warehousing using AWS and Snowflake.

---

## 🏗️ Architecture

GitHub → S3 (Raw Layer) → AWS Glue (ETL) → S3 (Processed Layer) → Snowflake (Warehouse)

---

## ⚙️ Key Features

* ✅ Micro-batch ingestion (append-only raw data)
* ✅ Event-driven ETL using AWS Glue
* ✅ Data cleaning, validation, and feature engineering
* ✅ Partitioned Parquet storage in S3
* ✅ Star schema warehouse design in Snowflake
* ✅ Daily warehouse updates using scheduled tasks
* ✅ Idempotent pipeline execution using metadata tracking

---

## 📂 Data Lake Structure

### 🔹 Raw Layer (Immutable)

```
s3://travel-etl-project/raw/travel/
    year=YYYY/month=MM/day=DD/
        travel_YYYYMMDD_HHMM.csv
```

### 🔹 Processed Layer (Parquet)

```
s3://travel-etl-project/processed/travel_clean/
    year=YYYY/month=MM/day=DD/
        part-*.parquet
```

---

## 🔄 Pipeline Flow

1. New data file uploaded to S3 (append-only)
2. S3 event triggers AWS Lambda
3. Lambda triggers AWS Glue ETL job
4. Glue performs:

   * Data extraction
   * Transformation
   * Validation
   * Feature engineering
5. Processed data stored in partitioned Parquet format
6. Snowflake task runs daily:

   * Loads data into staging
   * Performs MERGE into fact and dimension tables

---

## 🧠 ETL Logic

### 🔹 Extract

Reads raw CSV files from S3

### 🔹 Transform

* Standardizes categorical values
* Handles missing values
* Creates derived features (e.g., TotalVisiting)

### 🔹 Validate

* Removes duplicates
* Filters invalid records

### 🔹 Load

Writes partitioned Parquet files to S3

---

## 🏢 Data Warehouse (Snowflake)

* Star Schema Design:

  * Fact: `fact_travel_sales`
  * Dimensions:

    * `dim_customer`
    * `dim_location`
    * `dim_product`

* Incremental loading using MERGE (upsert logic)

---

## ⏱ Scheduling Strategy

| Layer      | Trigger Type       |
| ---------- | ------------------ |
| Ingestion  | Event-driven       |
| Processing | Event-driven       |
| Warehouse  | Time-based (daily) |

---

## ⚠️ Current Limitations

* Initial version used full-load processing
* Overwrite-based storage in processed layer
* No row-level incremental filtering

---

## 🚀 Future Enhancements

* Implement true incremental loading using timestamps
* Add upsert logic using MERGE in Snowflake
* Introduce Airflow for orchestration
* Integrate streaming using Kafka
* Upgrade storage format to Delta Lake / Iceberg

---

## 🛠️ Tech Stack

* Python (Pandas)
* AWS S3
* AWS Glue (PySpark)
* AWS Lambda
* Snowflake
* GitHub Actions

---

## 🎯 Key Learning Outcomes

* Built a scalable micro-batch data pipeline
* Implemented data lake architecture (raw → processed)
* Designed star schema for analytical workloads
* Applied data engineering best practices (immutability, partitioning, idempotency)

---

## 📌 Author

Kartik Deogade
