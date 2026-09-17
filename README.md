# JanSetu DataTrust

## AI-Assisted Public-Sector Data Quality & AI Readiness Platform

JanSetu DataTrust is an end-to-end data quality, governance, and analytics project designed around a public-sector data workflow.

The project uses a deliberately messy **synthetic public-service dataset** and processes it through ingestion, profiling, validation, cleaning, quality assessment, SQL analytics, statistical analysis, anomaly detection, metadata generation, data lineage tracking, and dashboard reporting.

The objective is to demonstrate how structured data-quality and governance practices can improve the reliability and readiness of datasets used for analytics and AI workflows.

> **Important:** The dataset used in this project is fully synthetic and does not represent real government data.

---

## Project Overview

Public-sector data workflows can involve datasets containing:

- Missing values
- Duplicate records
- Invalid values
- Inconsistent naming
- Invalid contact information
- Inconsistent date formats
- Incomplete metadata
- Unusual records requiring analyst review

JanSetu DataTrust provides a reproducible workflow for identifying, documenting, cleaning, assessing, and reporting these issues before the data is used for downstream analytics or AI workflows.

---

## Project Pipeline

```text
Synthetic Public-Service Dataset
              |
              v
        Data Ingestion
              |
              v
   Data Profiling & Validation
              |
              v
        Data Cleaning
              |
              v
    Data Quality Assessment
              |
              +---------> Data Lineage
              |
              v
      SQLite + SQL Analytics
              |
              v
      Statistical Analysis
              |
              v
 AI-Assisted Anomaly Detection
              |
              v
    AI Readiness Assessment
              |
              v
      Excel / Power BI Reporting