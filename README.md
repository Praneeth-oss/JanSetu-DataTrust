# JanSetu DataTrust

## AI-Assisted Public-Sector Data Quality & AI Readiness Platform

JanSetu DataTrust is a data-quality and governance project designed around a public-sector data workflow.

The project takes a deliberately messy synthetic public-service dataset and processes it through ingestion, validation, cleaning, quality assessment, SQL analytics, statistical analysis, anomaly detection, metadata generation, data lineage tracking, and dashboard reporting.

The goal is to demonstrate how structured data-quality practices can improve the reliability and readiness of datasets used for analytics and AI workflows.

> **Note:** The dataset used in this project is synthetic and does not represent real government data.

---

## What Problem Does It Solve?

Public-sector datasets can contain:

- Missing values
- Duplicate records
- Invalid values
- Inconsistent naming
- Invalid contact information
- Inconsistent date formats
- Incomplete metadata
- Unusual records requiring analyst review

Before data can reliably support analytics or AI systems, these issues need to be identified, documented, and addressed systematically.

JanSetu DataTrust provides an end-to-end workflow for doing that.

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
        +-------> Data Lineage
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
```

---

## Key Features

### 1. Data Profiling

The raw dataset is profiled before cleaning to identify:

- Dataset dimensions
- Missing values
- Duplicate records
- Invalid ages
- Invalid email addresses
- Invalid phone numbers
- Inconsistent state names
- Inconsistent department names
- Data-type characteristics

### 2. Data Cleaning

The cleaning pipeline:

- Removes duplicate records
- Standardizes inconsistent values
- Validates age ranges
- Validates email and phone fields
- Preserves genuinely missing information rather than inventing values
- Produces a cleaned dataset for downstream analysis

### 3. Data Quality Assessment

The project evaluates data using measurable quality dimensions:

- Completeness
- Validity
- Consistency
- Uniqueness
- Schema readiness

The project also generates a before-versus-after quality report to show how the cleaning process changes the dataset.

### 4. SQL Analytics

The cleaned data is analyzed using SQLite and SQL queries covering:

- Records by state
- Records by department
- Average income by state
- Service-request volume
- High service-request records
- Missing-value summaries

### 5. Statistical Analysis

Descriptive statistics are generated for important numerical fields, including:

- Mean
- Median
- Standard deviation
- Minimum
- Maximum
- Quartiles

### 6. AI-Assisted Anomaly Detection

An Isolation Forest model is used to identify unusual combinations of:

- Age
- Annual income
- Service requests

The output is intended for **analyst review of unusual records**, not as a fraud-detection system.

### 7. AI Readiness Assessment

JanSetu includes a transparent, project-defined AI readiness scoring framework based on data-quality and governance signals.

The current synthetic dataset produces an overall project score of:

**99.96 / 100**

This is a project-defined metric and is **not an industry certification or external AI-readiness standard**.

### 8. Data Lineage

The project records important processing events, including:

- Ingestion
- Cleaning
- Standardization
- Database loading

Each event records the transformation stage and affected record counts.

### 9. Automated Data Dictionary

The project generates metadata describing:

- Column names
- Data types
- Record counts
- Missing values
- Missing percentages
- Unique values
- Example values

---

## Results

The synthetic raw dataset contained:

- **1,003 records**
- **10 columns**
- **3 duplicate records**
- **8 initial missing cells**
- Invalid and inconsistent values across several fields

After the cleaning process:

- **1,000 records**
- **0 duplicate records**
- Invalid age values addressed
- Invalid email values addressed
- Invalid phone values addressed
- State inconsistencies addressed
- Department inconsistencies addressed
- Remaining missing values preserved and flagged

The cleaned dataset achieved:

| Metric | Result |
|---|---:|
| Records | 1,000 |
| Completeness | 99.88% |
| Data Validity | 100.00% |
| Project AI Readiness Score | 99.96 / 100 |
| Duplicate Records | 0 |

---

## Power BI Dashboard

The project includes a Power BI dashboard containing:

- Total Records KPI
- Data Completeness KPI
- Data Validity KPI
- AI Readiness KPI
- Before vs After Quality comparison
- State distribution
- Department distribution

The dashboard is designed to provide a quick overview of dataset quality and analytical characteristics.

---

## Technology Stack

- **Python**
- **Pandas**
- **NumPy**
- **Scikit-learn**
- **SQLite**
- **SQL**
- **Power BI**
- **Excel / CSV**
- **JSONL**

---

## Project Structure

```text
JanSetu-DataTrust/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── dashboard/
│
├── docs/
│   ├── data_dictionary.csv
│   └── data_lineage.jsonl
│
├── reports/
│
├── sql/
│   └── analytics.sql
│
├── src/
│   ├── config.py
│   ├── generate_data.py
│   ├── profile_data.py
│   ├── clean_data.py
│   ├── load_database.py
│   ├── run_sql.py
│   ├── statistics.py
│   ├── anomaly_detection.py
│   ├── readiness_score.py
│   ├── quality_report.py
│   ├── lineage.py
│   ├── data_dictionary.py
│   └── excel_report.py
│
├── SchemaSense/
│
├── JanSetu_DataTrust.pbix
└── README.md
```

---

## Data Governance Considerations

The project demonstrates several basic governance concepts relevant to data and AI workflows:

- Data quality measurement
- Metadata generation
- Data dictionary creation
- Data lineage
- Sensitive-field awareness
- Validation before analytics
- Preservation of missing information
- Documentation of transformations

The project uses synthetic data to avoid exposing personal or sensitive real-world information.

---

## Limitations

This project is a portfolio demonstration and should not be interpreted as a production government data platform.

Important limitations include:

- The dataset is synthetic.
- The AI readiness score is a project-defined framework.
- Anomaly detection identifies unusual records but does not establish the cause of an anomaly.
- The validation rules are designed for this demonstration dataset.
- Production deployments would require stronger security, access control, monitoring, governance policies, and domain-specific validation.

---

## Future Improvements

Potential future improvements include:

- Automated data-quality monitoring
- Additional anomaly-detection techniques
- Expanded metadata and governance rules
- Automated report generation
- API-based ingestion
- Role-based access control
- Data-quality trend monitoring
- Automated schema-change detection

---

## Author

**Praneeth Pentakota**

Computer Science Engineering — Information Security

Interested in:

- Data Analytics
- Data Quality
- Data Governance
- Artificial Intelligence
- Cybersecurity
- Information Security