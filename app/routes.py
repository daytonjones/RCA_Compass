import io
import json
import os
import pdfkit
from flask import render_template, request, redirect, url_for, flash, send_file, current_app
from app import create_app, db
from app.models import RCAReport

app = create_app()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Collect data from the form. The fields below match the sections of your attached template :contentReference[oaicite:0]{index=0}.
        report_data = {
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
        # Use the description as the title for simplicity
        title = report_data.get("description", "Untitled Report")
        report = RCAReport(title=title, report_data=json.dumps(report_data))
        db.session.add(report)
        db.session.commit()
        flash("Report created successfully.", "success")
        return redirect(url_for("list_reports"))
    return render_template("form.html")

@app.route('/reports')
def list_reports():
    reports = RCAReport.query.order_by(RCAReport.created_at.desc()).all()
    return render_template("list_reports.html", reports=reports)

@app.route('/reports/<int:report_id>')
def view_report(report_id):
    report = RCAReport.query.get_or_404(report_id)
    report_data = json.loads(report.report_data)
    return render_template("report.html", report=report, data=report_data)

@app.route('/reports/<int:report_id>/pdf')
def download_pdf(report_id):
    report = RCAReport.query.get_or_404(report_id)
    report_data = json.loads(report.report_data)
    # Render the report template as HTML for PDF conversion
    html = render_template("report.html", report=report, data=report_data, pdf=True)
    # wkhtmltopdf is installed in the container at /usr/bin/wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
    pdf = pdfkit.from_string(html, False, configuration=config)
    return send_file(io.BytesIO(pdf),
                     download_name=f"report_{report.id}.pdf",
                     as_attachment=True,
                     mimetype='application/pdf')

