# Medical Telegram Warehouse - Interim Submission

**Course:** 10 Academy: Artificial Intelligence Mastery  
**Week:** 8  
**Challenge:** Shipping a Data Product: From Raw Telegram Data to an Analytical API  
**Interim Submission:** Tasks 1 & 2 (Data Scraping and dbt Modeling)

---

## 📂 Project Overview

This repository contains the interim work for the Week 8 Challenge, which focuses on building a **data platform for Ethiopian medical businesses** using raw Telegram data.  

The goal of the interim submission is to demonstrate:

1. **Task 1 – Data Scraping and Collection (Extract & Load)**  
   - Extract messages and images from public Telegram channels.  
   - Store raw data in a structured data lake (`data/raw/`).  
   - Log all scraping activity to `logs/`.  

2. **Task 2 – Data Modeling and Transformation with dbt (Transform)**  
   - Load raw data into PostgreSQL.  
   - Implement **staging models** to clean and standardize raw data.  
   - Implement **dimensional models** (star schema) in `models/marts/`.  
   - Run dbt tests to ensure data quality.  

---

## ⚙️ Folder Structure

medical-telegram-warehouse/
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── data/
│ └── raw/
│ ├── telegram_messages/
│ └── images/
├── logs/
├── src/
│ ├── init.py
│ ├── scraper.py
│ └── load_raw_to_db.py
├── medical_warehouse/
│ ├── dbt_project.yml
│ ├── profiles.yml
│ ├── models/
│ │ ├── staging/
│ │ └── marts/
│ └── tests/