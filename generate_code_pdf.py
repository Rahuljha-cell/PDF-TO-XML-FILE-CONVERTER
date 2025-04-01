import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT

def get_file_content(filepath):
    """Read the content of a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def generate_code_pdf(output_pdf="pdf_to_xml_converter_code.pdf"):
    """Generate a PDF with all code files from the project."""
    # Setup document
    doc = SimpleDocTemplate(output_pdf, pagesize=A4, 
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    
    # Create a code style
    code_style = ParagraphStyle(
        'CodeStyle',
        fontName='Courier',
        fontSize=8,
        leading=10,
        leftIndent=20,
        rightIndent=20,
        textColor=colors.black,
        alignment=TA_LEFT,
    )
    
    # Content to add to the PDF
    content = []
    
    # Add title
    content.append(Paragraph("PDF to XML Converter Application - Complete Source Code", title_style))
    content.append(Spacer(1, 0.25*inch))
    
    # Add project overview
    overview = """
    This document contains the complete source code for a PDF to XML Converter web application
    built with Flask, SQLAlchemy, and vanilla JavaScript. The application allows users to:
    
    • Register and login with authentication
    • Upload PDF documents
    • Convert PDFs to structured XML
    • View and download the XML output
    • Track conversion history
    """
    content.append(Paragraph(overview, styles['Normal']))
    content.append(Spacer(1, 0.5*inch))
    
    # Files to include in the PDF
    files_to_include = [
        ('app.py', 'Flask Application Configuration'),
        ('main.py', 'Application Entry Point'),
        ('models.py', 'Database Models'),
        ('forms.py', 'Web Form Definitions'),
        ('routes.py', 'Application Routes'),
        ('pdf_converter.py', 'PDF to XML Conversion Logic'),
        ('static/js/main.js', 'Main JavaScript'),
        ('static/js/pdf_viewer.js', 'PDF Viewer JavaScript'),
    ]
    
    # Additional template files if they exist
    template_files = [
        ('templates/base.html', 'Base HTML Template'),
        ('templates/index.html', 'Index Page Template'),
        ('templates/login.html', 'Login Page Template'),
        ('templates/register.html', 'Registration Page Template'),
        ('templates/dashboard.html', 'Dashboard Page Template'),
        ('templates/history.html', 'History Page Template'),
    ]
    
    # Add CSS file if it exists
    css_files = [
        ('static/css/style.css', 'CSS Stylesheet'),
    ]
    
    # Combine all files
    all_files = files_to_include + template_files + css_files
    
    # Add each file's content to the PDF
    for filepath, description in all_files:
        if os.path.exists(filepath):
            # Add file header
            content.append(Paragraph(f"{description}: {filepath}", subtitle_style))
            content.append(Spacer(1, 0.1*inch))
            
            # Add code with syntax highlighting if available
            code = get_file_content(filepath)
            pre_text = Preformatted(code, code_style)
            content.append(pre_text)
            
            # Add spacer
            content.append(Spacer(1, 0.3*inch))
    
    # Add timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content.append(Paragraph(f"Generated on: {timestamp}", styles['Normal']))
    
    # Build the PDF
    doc.build(content)
    
    return output_pdf

if __name__ == "__main__":
    pdf_path = generate_code_pdf()
    print(f"PDF generated successfully: {pdf_path}")