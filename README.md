# ETL_project_Northwind_Traders

# 🛒 Northwind Traders ETL Pipeline & Advanced SQL Analytics

An end-to-end Data Engineering portfolio project implementing the **Medallion Architecture (Bronze -> Silver -> Gold)** using Python, Pandas, Google BigQuery, and advanced SQL.

---

## 🏗️ Project Architecture & Workflow

This project processes raw data through a structured 3-tier medallion pipeline:

1. **Bronze Layer (Ingestion):** Raw CSV/Relational data is ingested directly into Google BigQuery tables (`bronze_dataset_Northwind`) without transformations.
2. **Silver Layer (Cleaning & Transformation):** Python scripts (`pandas`) clean missing values, fix data types, standardize columns, and load the cleaned tables into `silver_dataset_Northwind`.
3. **Gold Layer (Analytics & Business Intelligence):** Advanced SQL queries utilizing CTEs, Window Functions (`RANK`, `DENSE_RANK`, `LAG`), and complex joins to generate actionable business insights.

---

## 🛠️ Tech Stack

* **Language:** Python (`pandas`, `pandas-gbq`)
* **Data Warehouse:** Google BigQuery
* **Query Language:** SQL (CTEs, Window Functions, Correlated Subqueries)
* **Version Control:** Git & GitHub

---

## 📁 Repository Structure

```text
ETL_project_Northwind_Traders/
│
├── bronze_ingestion.py        # Bronze layer extraction & loading script
├── silver_transformation.py   # Silver layer cleaning & validation script
├── gold_layer.sql             # Advanced SQL queries & analytical models
└── README.md                  # Project documentation