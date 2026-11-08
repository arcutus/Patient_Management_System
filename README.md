# Patient Management System

A learning project that provides a REST API for managing patient records. Built with Python and FastAPI, with database access through SQLAlchemy.

> **Educational use only.** This project is not intended for real patient data, clinical use, or production deployment. It does not claim to meet healthcare privacy, security, or regulatory requirements. Use only synthetic data.

## Features

- Create, view, update, and delete patient records
- Search records by patient name or ID
- Sort records by name, age, or gender
- Calculate BMI from height and weight
- Interactive API documentation provided by FastAPI

## Technology

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL (if this is the database configured by the project)

## Getting started

### Prerequisites

- Python [supported version]
- [PostgreSQL, if required by your configuration]

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/arcutus/Patient_Management_System.git
   cd Patient_Management_System
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   On Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   On macOS or Linux:

   ```bash
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database using the project’s environment-variable or configuration instructions: **[add the verified configuration steps here]**.

5. Start the API:

   ```bash
   uvicorn main:app --reload
   ```

6. Open the interactive API documentation at
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API overview

The API includes patient-management routes under `/patient_info` and `/data_patient`.
See the interactive documentation at `/docs` for the current routes, parameters,
and request examples.

## Sample data

Use synthetic records only. Do not add real patient information, database files,
backups, credentials, or other sensitive data to this repository.

## Limitations and security

This is a practice project, not a production-ready patient-record system. Before
considering any real-world use, it would need a thorough security and privacy
review, including authentication and authorization, input and access controls,
secure configuration, logging practices, backups, and applicable legal and
regulatory requirements.

## Contributing

Issues and pull requests are welcome. Please do not include personal or medical
information in issues, pull requests, test data, or screenshots.

## License

No license has been selected yet. Until a license is added, others generally do
not have permission to reuse, modify, or distribute this project. 

