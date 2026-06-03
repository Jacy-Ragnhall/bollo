import re
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def parse_resume_file(resume_file):
    """
    Extracts name and email dynamically from resume file content using simple regex logic.
    Ensures file seek is reset so Django can write the file cleanly afterwards.
    """
    parsed_name = ""
    parsed_email = ""
    
    try:
        content = resume_file.read(15000)
        # Attempt to decode as text, fallback to byte representation
        try:
            text = content.decode('utf-8', errors='ignore')
        except Exception:
            text = str(content)
            
        # Regex to locate standard email address format
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        if email_match:
            parsed_email = email_match.group(0)
            
        # Regex heuristic for Firstname Lastname
        name_match = re.search(r'\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b', text)
        if name_match:
            parsed_name = f"{name_match.group(1)} {name_match.group(2)}"
            
        # Crucial: Reset the seek pointer so Django can write the file cleanly
        resume_file.seek(0)
    except Exception as e:
        print(f"Error parsing resume: {e}")
        
    return parsed_name, parsed_email

def generate_resume_pdf(data):
    """
    Compiles input details into a highly polished, professional PDF document via ReportLab.
    """
    buffer = io.BytesIO()
    
    # Establish document margins
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        rightMargin=40, 
        leftMargin=40, 
        topMargin=40, 
        bottomMargin=40
    )
    story = []
    styles = getSampleStyleSheet()
    
    # Customized styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=26,
        textColor=colors.HexColor('#6366f1'), # Brand indigo color
        spaceAfter=4
    )
    contact_style = ParagraphStyle(
        'DocContact',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#64748b'), # Cool grey text
        spaceAfter=12
    )
    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=14,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )
    
    # Build sections
    story.append(Paragraph(data['full_name'], title_style))
    story.append(Paragraph(f"Email: {data['email']} | Phone: {data['phone']}", contact_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("Professional Summary", h2_style))
    story.append(Paragraph(data['summary'].replace('\n', '<br/>'), body_style))
    
    story.append(Paragraph("Work Experience", h2_style))
    story.append(Paragraph(data['experience'].replace('\n', '<br/>'), body_style))
    
    story.append(Paragraph("Education", h2_style))
    story.append(Paragraph(data['education'].replace('\n', '<br/>'), body_style))
    
    story.append(Paragraph("Skills", h2_style))
    story.append(Paragraph(data['skills'], body_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer
