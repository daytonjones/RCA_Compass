import io
import json
from datetime import datetime
import pdfkit
from flask import render_template, request, redirect, url_for, flash, send_file
from app import create_app, db
from app.models import RCAReport

app = create_app()

@app.route('/', methods=['GET', 'POST'])
def index():
    reports = RCAReport.query.order_by(RCAReport.created_at.desc()).all()
    selected_report = None

    if request.method == 'POST':
        # Collect form data including a new "report_name" field
        report_data = {
            "report_name": request.form.get("report_name"),
            "description": request.form.get("description"),
            "date_of_incident": request.form.get("date_of_incident"),
            "incident_description": request.form.get("incident_description"),
            "reported_by": request.form.get("reported_by"),
            "affected": request.form.get("affected"),
            "impact": request.form.get("impact"),
            "frequency": request.form.get("frequency"),
            "timeline": request.form.get("timeline"),
            "events_before": request.form.get("events_before"),
            "events_during": request.form.get("events_during"),
            "events_after": request.form.get("events_after"),
            "personnel": request.form.get("personnel"),
            "staff_investigating": request.form.get("staff_investigating"),
            "job_titles": request.form.get("job_titles"),
            "data_collection_methods": request.form.get("data_collection_methods"),
            "communication_plan": request.form.get("communication_plan"),
            "root_cause": request.form.get("root_cause"),
            "supporting_data": request.form.get("supporting_data"),
            "resolution_steps": request.form.get("resolution_steps"),
            "date_resolved": request.form.get("date_resolved"),
            "approved_by": request.form.get("approved_by")
        }
        # Ensure that the incident date is provided
        incident_date = request.form.get("date_of_incident")
        if not incident_date:
            flash("Date of Incident is required.", "error")
            return redirect(url_for("index"))
        dt = datetime.strptime(incident_date, "%Y-%m-%d")
        mmddyyyy = dt.strftime("%m%d%Y")
        # Calculate new report number (sequential, zero-padded to 4 digits)
        count = RCAReport.query.count() + 1
        report_number = f"{count:04d}"
        # Get the user-provided report name and build the full title in the format "####_<NAME>-MMDDYYYY"
        report_name_input = request.form.get("report_name").strip()
        full_report_title = f"{report_number}_{report_name_input}-{mmddyyyy}"
        # Save the report
        report = RCAReport(title=full_report_title, report_data=json.dumps(report_data))
        db.session.add(report)
        db.session.commit()
        flash("Report created successfully.", "success")
        return redirect(url_for("index", report_id=report.id))
    
    # GET request: check if a report is selected (via query parameter)
    report_id = request.args.get('report_id')
    if report_id:
        selected_report = RCAReport.query.get_or_404(report_id)
        selected_report.data = json.loads(selected_report.report_data)
        incident_date = selected_report.data.get("date_of_incident")
        if incident_date:
            dt = datetime.strptime(incident_date, "%Y-%m-%d")
            selected_report.data["header_date"] = dt.strftime("%m%d%y")
        else:
            selected_report.data["header_date"] = ""
    return render_template("index.html", reports=reports, selected_report=selected_report)

@app.route('/reports/<int:report_id>/pdf')
def download_pdf(report_id):
    report = RCAReport.query.get_or_404(report_id)
    data = json.loads(report.report_data)
    html = render_template("report_pdf.html", report=report, data=data)
    config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
    options = {"--enable-local-file-access": ""}
    pdf = pdfkit.from_string(html, False, configuration=config, options=options)
    # Use the report title as the download file name, appending .pdf.
    # (You might want to sanitize the title if necessary.)
    return send_file(
        io.BytesIO(pdf),
        download_name=f"{report.title}.pdf",
        as_attachment=True,
        mimetype='application/pdf'
    )

