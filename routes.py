import os
import uuid
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, jsonify, send_file, session
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from io import BytesIO

from app import app, db
from models import User, Conversion
from forms import RegistrationForm, LoginForm, PDFUploadForm
from pdf_converter import convert_pdf_to_xml

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')
    
@app.route('/pdf-download')
def pdf_download_page():
    """Route to display a simple download page for the source code PDF."""
    return app.send_static_file('download_pdf.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = PDFUploadForm()
    if form.validate_on_submit():
        # Process the PDF file
        pdf_file = form.pdf_file.data
        original_filename = secure_filename(pdf_file.filename)
        
        # Generate unique filenames for both PDF and XML
        unique_id = str(uuid.uuid4())
        pdf_filename = f"{unique_id}_{original_filename}"
        xml_filename = f"{pdf_filename.rsplit('.', 1)[0]}.xml"
        
        # Convert PDF to XML
        try:
            pdf_content = pdf_file.read()
            file_size = len(pdf_content)
            xml_content = convert_pdf_to_xml(BytesIO(pdf_content))
            
            # Store conversion record in database
            conversion = Conversion(
                pdf_filename=original_filename,
                xml_filename=xml_filename,
                file_size=file_size,
                xml_content=xml_content,
                user_id=current_user.id
            )
            db.session.add(conversion)
            db.session.commit()
            
            # Store the XML content in session for preview
            session['current_conversion_id'] = conversion.id
            
            flash('PDF successfully converted to XML!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            flash(f'Error converting PDF: {str(e)}', 'error')
            app.logger.error(f"PDF conversion error: {str(e)}")
            
    # Get the most recent conversion for preview if available
    current_conversion = None
    if 'current_conversion_id' in session:
        current_conversion = Conversion.query.get(session['current_conversion_id'])
        
    return render_template('dashboard.html', form=form, conversion=current_conversion)

@app.route('/history')
@login_required
def history():
    conversions = Conversion.query.filter_by(user_id=current_user.id).order_by(Conversion.conversion_date.desc()).all()
    return render_template('history.html', conversions=conversions)

@app.route('/conversion/<int:conversion_id>')
@login_required
def view_conversion(conversion_id):
    conversion = Conversion.query.get_or_404(conversion_id)
    
    # Check that this conversion belongs to the current user
    if conversion.user_id != current_user.id:
        flash('You do not have permission to view this conversion.', 'error')
        return redirect(url_for('history'))
    
    session['current_conversion_id'] = conversion.id
    return redirect(url_for('dashboard'))

@app.route('/download/<int:conversion_id>')
@login_required
def download_xml(conversion_id):
    conversion = Conversion.query.get_or_404(conversion_id)
    
    # Check that this conversion belongs to the current user
    if conversion.user_id != current_user.id:
        flash('You do not have permission to download this file.', 'error')
        return redirect(url_for('history'))
    
    # Create BytesIO object with the XML content
    xml_data = BytesIO(conversion.xml_content.encode('utf-8'))
    
    # Generate a filename based on the original PDF name
    filename = f"{conversion.pdf_filename.rsplit('.', 1)[0]}.xml"
    
    return send_file(
        xml_data,
        mimetype='application/xml',
        as_attachment=True,
        download_name=filename
    )

@app.route('/api/conversion/<int:conversion_id>')
@login_required
def get_conversion_data(conversion_id):
    conversion = Conversion.query.get_or_404(conversion_id)
    
    # Check that this conversion belongs to the current user
    if conversion.user_id != current_user.id:
        return jsonify({'error': 'Not authorized'}), 403
    
    return jsonify({
        'id': conversion.id,
        'pdf_filename': conversion.pdf_filename,
        'xml_filename': conversion.xml_filename,
        'conversion_date': conversion.conversion_date.strftime('%Y-%m-%d %H:%M:%S'),
        'file_size': conversion.file_size,
        'xml_content': conversion.xml_content
    })

@app.route('/download/source-code')
def download_source_code():
    """Route to download the complete source code PDF."""
    try:
        pdf_path = "pdf_to_xml_converter_code.pdf"
        if os.path.exists(pdf_path):
            return send_file(
                pdf_path,
                mimetype='application/pdf',
                as_attachment=True,
                download_name="pdf_to_xml_converter_source_code.pdf"
            )
        else:
            flash('Source code PDF not found. Please generate it first.', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error downloading source code: {str(e)}', 'error')
        return redirect(url_for('index'))
