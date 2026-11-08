# Patient Management System

A demo project that provides a REST API for managing patient records. Built with Python and FastAPI, with database access through SQLAlchemy.

> **Project status: Demo.** This project is for learning and demonstration purposes only. It is not intended for real patient data, clinical use, or production deployment. It does not claim to meet healthcare privacy, security, or regulatory requirements. Use synthetic data only.

## Features

- Create, view, update, and delete patient records
- Search records by patient name or ID
- Sort records by name, age, or gender
- Calculate BMI from height and weight
- Interactive API documentation with Swagger UI and ReDoc

## Technology

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL

## Getting started

### Prerequisites

- Python
- PostgreSQL, configured for this application

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

4. Configure PostgreSQL for your local environment. Keep database credentials and other secrets out of source control.

5. Start the API:

   ```bash
   uvicorn main:app --reload
   ```

6. Open the API documentation:
   - [Swagger UI](http://127.0.0.1:8000/docs)
   - [ReDoc](http://127.0.0.1:8000/redoc)

These documentation links work when the API is running locally. Replace `127.0.0.1:8000` with your server address if running it elsewhere.

## Testing API endpoints

The API endpoints were tested using [Postman](https://www.postman.com/). Start the application and send requests to `http://127.0.0.1:8000` (or your server's base URL). Use `/docs` or `/redoc` to review the available endpoints and request schemas. No Postman collection is included in this repository.

## API overview

The API includes patient-management routes under `/patient_info` . See the interactive documentation at `/docs` or `/redoc` for the current routes, parameters, and request examples.

## Sample data

Use synthetic records only. Do not add real patient information, credentials, or other sensitive data to this repository.

## Limitations and security

This is a demo project, not a production-ready patient-record system. Before considering any real-world use, it would need a thorough security and privacy review, including authentication and authorization, input and access controls, secure configuration, logging practices, backups, and applicable legal and regulatory requirements.

## Contributing

Issues and pull requests are welcome. Please do not include personal or medical information in issues, pull requests, test data, or screenshots.

## License

This repository does not currently include a license. Without a license, others should not assume they have permission to reuse, modify, or distribute the code. Choose and add a license if you want to grant those permissions.
