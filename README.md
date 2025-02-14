# RCA Compass

RCA Compass is a Dockerized Flask application that helps you:
- Collect Root Cause Analysis (RCA) information via a web form.
- Store RCAs in a persistent SQLite database for future reference.
- Generate PDF reports from a Jinja2-based template.
- Serve everything securely behind Nginx (HTTPS) with Gunicorn in production.

<br>

## Features

1. **Create RCA Reports**  
   A user-friendly form prompts you for all the fields typically needed for a root cause analysis.

2. **Persist Reports**  
   Each submitted RCA is stored in a SQLite database. A list of past reports is accessible through the app, with the ability to download PDFs of each.

3. **PDF Generation**  
   Using [WeasyPrint](https://weasyprint.org/), you can generate professional PDFs from your form data, matching your chosen layout/style.

4. **Uploads for Custom Logos**  
   Upload a new logo or image to personalize your reports. The upload directory is volume-mounted for persistence.

5. **Secure by Default**  
   By default, the Docker setup will generate a self-signed SSL certificate for HTTPS. If you have your own certificates, simply volume-mount them into the Nginx container at `/etc/nginx/certs`.

6. **Scalable Docker Architecture**  
   Uses a simple `docker-compose.yml` with two services:
   - `rca_compass_app`: a Python slim-based container running Flask + Gunicorn.
   - `nginx`: a stable-alpine-based container proxying requests over HTTPS to the Flask application.

<br>

## Project Structure

```bash
rca_compass/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── requirements.txt
│   ├── __init__.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── form.html
│   │   ├── list_reports.html
│   │   └── report.html
│   └── static/
│       └── uploads/
├── docker/
│   ├── Dockerfile.app
│   ├── Dockerfile.nginx
│   └── default.conf
├── docker-compose.yml
└── README.md
```

<br>

## Quick Start

1. **Clone the Repository** (or copy the files to your local system):
   ```bash
   git clone https://github.com/daytonjones/rca_compass.git
   cd rca_compass
   ```

2. **Build and Run with Docker Compose**:
   ```bash
   docker-compose build
   docker-compose up -d
   ```
   - This will:
     - Build the `rca_compass_app` image.
     - Build the `nginx` image from `nginx:stable-alpine`.
     - Launch the containers in detached mode.

3. **Access the Application**:
   - Visit `https://localhost` in your browser.
   - Because of the self-signed certificate, you might need to click through the browser’s “insecure” or “advanced” warning to proceed.

4. **View Logs (Optional)**:
   ```bash
   docker-compose logs -f
   ```

5. **Stopping the Containers**:
   ```bash
   docker-compose down
   ```

<br>

## Persistent Volumes

By default, three named volumes are defined in `docker-compose.yml`:

- **`db_data`**: Persists the SQLite database file, `rca_compass.db`.  
- **`uploads_data`**: Persists uploaded logos/images in `app/static/uploads/`.  
- **`certs_data`**: Holds SSL certificate files at `/etc/nginx/certs`. If you have a real SSL cert, mount it here under the names `server.crt` and `server.key`.

<br>

## Customizing SSL Certificates

If you want to use your own certificates instead of the self-signed ones:

1. Place `server.crt` and `server.key` into a directory on your host machine (e.g., `./mycerts`).
2. Update your `docker-compose.yml`:
   ```yaml
   volumes:
     - ./mycerts:/etc/nginx/certs
   ```
3. When you run Docker Compose, the Nginx container will pick up your certificate and key.

<br>

## Custom Logos and Images

You can upload a logo for your organization via the **Upload Logo** link in the navigation bar. The file will be saved into `app/static/uploads/`. The app will attempt to display a `logo.png` in the top portion of the PDF (and the HTML version). Rename your uploaded file to `logo.png` for it to appear automatically.

<br>

## Local Development

For local development (without Docker), you can still run the Flask app directly:

1. **Install Dependencies**:
   ```bash
   cd app
   pip install -r requirements.txt
   ```
2. **Run the Flask Development Server**:
   ```bash
   python main.py
   ```
3. Visit `http://localhost:5000` to see the application.

> **Note**: This bypasses Gunicorn and Nginx, so it’s recommended only for quick local testing.

<br>

## Production Notes

- In a production environment, ensure you set a strong `SECRET_KEY` for Flask.
- Confirm the SSL certificate is valid and recognized by your domain.
- Monitor logs and consider using production-grade logging solutions (e.g., shipping logs to a centralized system).

<br>

## Troubleshooting

- **Browser SSL Warnings**: This is normal if you’re using a self-signed certificate. Either trust the certificate or mount your own valid certificate to avoid warnings.
- **Permissions**: If you run into permissions issues with the SQLite DB or the uploads directory, ensure your Docker volumes are set with the proper user permissions. A non-root user was created inside the Dockerfiles, but you may adapt it if needed.

<br>

## License

You are free to use this example project as you see fit. Please note that usage of external libraries (Flask, WeasyPrint, etc.) is governed by their respective licenses.

<br>

---

**Happy RCA-ing with RCA Compass!**


