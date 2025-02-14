# RCA Compass - Root Cause Analysis Report Generator

## Overview
RCA Compass is a web application designed to facilitate the creation, storage, and management of Root Cause Analysis (RCA) reports. It allows users to input detailed incident data, generate structured reports, download them as PDFs, and review past reports.

The application is built using **Flask**, **SQLite**, and **pdfkit** for PDF generation, with a **Dockerized** deployment that includes **Nginx** and **Gunicorn** for production-ready performance. It also supports custom branding with a **persistent asset directory** for logos, images, and other customization needs.

---
## Features
- **Two-Column Layout:**
  - Left Panel: List of previously created reports.
  - Right Panel: RCA input form or selected report details.
- **PDF Generation:**
  - Professionally formatted reports with a company logo.
  - Auto-generated file names using the report title.
- **Persistent Storage:**
  - RCA reports are stored in an SQLite database for future reference.
- **Custom Branding Support:**
  - Logos and background images can be stored in a dedicated persistent directory (`custom_assets`).
- **Fully Dockerized:**
  - Runs using `python:3.12-slim`.
  - `Gunicorn` handles application requests.
  - `Nginx` serves as a reverse proxy with SSL support.

---
## Installation

### Prerequisites
Ensure you have the following installed:
- **Docker** & **Docker Compose**
- **wkhtmltopdf** (installed inside the container, required for PDF generation)

### Clone the Repository
```bash
git clone https://github.com/daytonjones/RCA_Compass.git
cd RCA_Compass
```

### Configure Custom Assets
- Place your **logo** (e.g., `compass_logo.png`) and **background image** (`compass_bg.svg`) inside the `custom_assets/` folder.

### Start the Application
```bash
docker-compose up --build -d
```
This will:
- Build and launch the Flask application using Gunicorn.
- Set up Nginx as a reverse proxy with SSL support.
- Persist database and asset storage.

---
## Usage

### Access the Application
Open a browser and go to:
```
https://localhost/
```

### Creating a New Report
1. Click **"New Report"** (if a report is currently being viewed).
2. Fill out the RCA form.
3. Click **"Create Report"**.
4. The report will be stored and available for future access.

### Viewing and Downloading Reports
- Click on any previous report in the left column to view it.
- Click **"Download Report"** to generate a professionally formatted PDF.
- PDFs are named using the format:
  ```
  ####_<NAME>-MMDDYYYY.pdf
  ```
  Example:
  ```
  0005_Production Web-02142025.pdf
  ```

---
## Project Structure
```
RCA_Compass/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── form.html
│   │   ├── index.html
│   │   ├── list_reports.html
│   │   ├── report.html
│   │   ├── report_pdf.html
├── custom_assets/         # persistent directory for custom files
│   ├── compass_bg.svg
│   └── compass_logo.png
├── data/                  # persistent SQLite database mount
├── docker/
│   ├── Dockerfile
│   └── nginx/
│       ├── compass.crt
│       └── compass.key
│       ├── nginx.conf
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---
## Configuration

### Environment Variables
- **FLASK_APP**: Entry point for Flask (`app` by default).
- **DATABASE_URL**: Path to SQLite database (`sqlite:///data/rca.db`).

### Nginx Configuration
- Uses SSL (`compass.crt` and `compass.key`).
- Redirects HTTP (`port 80`) to HTTPS (`port 443`).

---
## Customization

### Changing the Logo & Background
Replace files in `custom_assets/`:
- `compass_logo.png` → Company Logo
- `compass_bg.svg` → Background Image

### Modifying the PDF Format
Edit **`app/templates/report_pdf.html`** to customize styling and structure.

---
## Deployment
### Running in Production
Use:
```bash
docker-compose up -d
```
### Stopping the Application
```bash
docker-compose down
```

---
## Troubleshooting
### PDF Not Downloading or Broken Images
- Ensure `wkhtmltopdf` is installed and available inside the container.
- Verify `--enable-local-file-access` is passed in `pdfkit` options.

### SSL Certificate Errors
- Ensure valid SSL certs (`compass.crt` and `compass.key`) exist in `docker/nginx/`.
- Generate a self-signed certificate if necessary:
  ```bash
  openssl req -x509 -newkey rsa:2048 -keyout docker/nginx/compass.key -out docker/nginx/compass.crt -days 1095 -nodes
  ```

---
## Future Enhancements
- **User authentication for secured access**
- **Email notifications for RCA updates**
- **Graphical analytics dashboard for RCA trends**

---
## License
MIT License © 2025 Dayton Jones



