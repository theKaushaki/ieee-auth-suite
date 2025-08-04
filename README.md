# Authorship Certificate Automation

This project automatically generates PDF authorship certificates from a CSV file.

## Features
- Reads author and article names from a CSV.
- Generates a unique, human-readable ID (e.g., IEEE-RP-0001) for each certificate.
- Creates a PDF certificate with a QR code for validation.
- Stores all records in an SQLite database.
- Provides a simple Flask web app to validate certificates via the QR code.

## How to Run
1.  Install dependencies: `pip install -r requirements.txt`
2.  Initialize the database: `python main.py`
3.  Run the validation server: `flask --app app run`