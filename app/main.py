# app/main.py
import os
from flask import render_template, request, redirect, url_for, send_file, flash
from io import BytesIO
from weasyprint import HTML
from app import create_app
from app.models import db, RCAReport

app = create_app()

@app.route('/')
def index():
    """Show the form to create a new Root Cause Analysis report."""
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Collect form data and create a new RCAReport record in the database."""
    try:
        # Grab all form fields (some might be optional)
        rca = RCAReport(
            issue_description=request.form.get('issue_description'),
            incident_date=request.form.get('incident_date'),
            incident_description=request.form.get('incident_description'),
            who_reported=request.form.get('who_reported'),
            who_affected=request.form.get('who_affected'),
            how_affected=request.form.get('how_affected'),
            how_often=request.form.get('how_often'),
            events_before=request.form.get('events_before'),
            events_during=request.form.get('events_during'),
            events_after=request.form.get('events_after'),
            staff_involved=request.form.get('staff_involved'),
            job_titles=request.form.get('job_titles'),
            data_collection_methods=request.form.get('data_collection_methods'),
            communication_plan=request.form.get('communication_plan'),
            root_cause=request.form.get('root_cause'),
            cause_occurrence=request.form.get('cause_occurrence'),
            supporting_data=request.form.get('supporting_data'),
            resolution_steps=request.form.get('resolution_steps'),
            date_resolved=request.form.get('date_resolved'),
            approved_by=request.form.get('approved_by'),
        )
        db.session.add(rca)
        db.session.commit()
        flash('RCA Report created successfully!', 'success')
        return redirect(url_for('view_report', report_id=rca.id))
    except Exception as e:
        print(e)
        flash('An error occurred while creating the RCA report.', 'danger')
        return redirect(url_for('index'))

@app.route('/reports')
def list_reports():
    """List all the RCA reports stored in the database."""
    reports = RCAReport.query.order_by(RCAReport.created_at.desc()).all()
    return render_template('list_reports.html', reports=reports)

@app.route('/report/<int:report_id>')
def view_report(report_id):
    """Show the RCA report detail."""
    rca = RCAReport.query.get_or_404(report_id)
    return render_template('report.html', rca=rca)

@app.route('/report/<int:report_id>/download')
def download_report(report_id):
    """Generate a PDF of the RCA report and return it as a download."""
    rca = RCAReport.query.get_or_404(report_id)
    html_out = render_template('report.html', rca=rca, pdf_mode=True)
    pdf = HTML(string=html_out).write_pdf()

    # Prepare PDF as a downloadable response
    return send_file(
        BytesIO(pdf),
        as_attachment=True,
        download_name=f"RCA_Report_{report_id}.pdf",
        mimetype='application/pdf'
    )

@app.route('/upload_logo', methods=['GET', 'POST'])
def upload_logo():
    """Endpoint to upload a custom logo or image to be used in the reports."""
    if request.method == 'POST':
        file = request.files.get('file')
        if file and file.filename:
            uploads_dir = os.path.join(app.root_path, 'static', 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            file.save(os.path.join(uploads_dir, file.filename))
            flash(f"File '{file.filename}' uploaded successfully!", 'success')
            return redirect(url_for('index'))
        else:
            flash('No file selected!', 'danger')
            return redirect(url_for('upload_logo'))
    return '''
    <h1>Upload Logo/Image</h1>
    <form method="POST" enctype="multipart/form-data">
      <input type="file" name="file"/>
      <input type="submit" value="Upload"/>
    </form>
    '''

if __name__ == '__main__':
    # For local debugging only
    # In production, we'll run with Gunicorn
    app.run(debug=True, host='0.0.0.0', port=5000)

