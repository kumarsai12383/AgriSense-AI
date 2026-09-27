import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)

def build_pdf():
    pdf_filename = "AgriSense_AI_Project_Documentation.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#14532d")    # Dark Forest Green
    c_secondary = colors.HexColor("#15803d")  # Emerald Green
    c_accent = colors.HexColor("#16a34a")     # Light Leaf Green
    c_dark = colors.HexColor("#0f172a")       # Slate Black
    c_gray = colors.HexColor("#475569")       # Slate Gray
    c_bg_light = colors.HexColor("#f8fafc")   # Card BG

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=c_primary,
        alignment=0,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_secondary,
        alignment=0,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_dark,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_dark,
        leftIndent=12,
        spaceAfter=3
    )

    table_header_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    table_body_style = ParagraphStyle(
        'TB',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=c_dark
    )

    story = []

    # =========================================================
    # HEADER
    # =========================================================
    story.append(Paragraph("AgriSense AI — Project Architecture & Technical Guide", title_style))
    story.append(Paragraph("AI-Driven Precision Agriculture, Multilingual Voice Agronomist & IoT Decision Support System", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=c_primary, spaceAfter=12))

    # =========================================================
    # 1. EXECUTIVE SUMMARY & OBJECTIVE
    # =========================================================
    story.append(Paragraph("1. Project Executive Summary", h1_style))
    summary_text = (
        "<b>AgriSense AI</b> is a complete, modern agricultural decision-support platform designed to empower "
        "Indian farmers with data-driven precision farming. The system integrates Machine Learning for soil-specific "
        "crop recommendations, IoT hardware telemetry for real-time soil sensing, Multimodal Vision AI for plant disease detection, "
        "and a real-time conversational Multilingual Voice Assistant supporting 6 Indian languages (English, Telugu, Hindi, Tamil, Kannada, Marathi)."
    )
    story.append(Paragraph(summary_text, body_style))

    # =========================================================
    # 2. COMPLETE TECH STACK BREAKDOWN (FRONTEND & BACKEND)
    # =========================================================
    story.append(Paragraph("2. Complete Technical Stack Breakdown", h1_style))

    tech_table_data = [
        [Paragraph("Layer", table_header_style), Paragraph("Technology Used", table_header_style), Paragraph("Key Role & Functionality", table_header_style)],
        [
            Paragraph("<b>Frontend UI</b>", table_body_style),
            Paragraph("Streamlit, HTML5, Vanilla CSS3", table_body_style),
            Paragraph("Mobile-first presentation design, dynamic responsive cards, touch targets, and multilingual dashboard.", table_body_style)
        ],
        [
            Paragraph("<b>Voice & Audio</b>", table_body_style),
            Paragraph("Web Speech API, SpeechSynthesis & Recognition", table_body_style),
            Paragraph("Speech-to-Text input with 6 native regional Indian accents; Text-to-Speech audio reading for illiterate farmers.", table_body_style)
        ],
        [
            Paragraph("<b>Backend API</b>", table_body_style),
            Paragraph("FastAPI, Uvicorn (ASGI), WebSockets", table_body_style),
            Paragraph("High-performance REST API endpoints for IoT data ingestion (/sensor/data) and low-latency bidirectional audio streaming.", table_body_style)
        ],
        [
            Paragraph("<b>Machine Learning</b>", table_body_style),
            Paragraph("Scikit-Learn, Random Forest, Joblib", table_body_style),
            Paragraph("Trained on 7 soil & climate parameters (N, P, K, pH, Temp, Humidity, Rain) to predict the highest-yield crop.", table_body_style)
        ],
        [
            Paragraph("<b>Generative AI & Vision</b>", table_body_style),
            Paragraph("Google GenAI SDK (Gemini 3.7 / 3.1 Flash)", table_body_style),
            Paragraph("Leaf disease visual diagnosis, organic treatment remedies, and contextual farming agronomist chat.", table_body_style)
        ],
        [
            Paragraph("<b>IoT Hardware</b>", table_body_style),
            Paragraph("ESP32, RS485 Modbus, DHT22, Rain Sensor", table_body_style),
            Paragraph("7-in-1 soil probe measuring NPK, moisture & pH, transmitting telemetry via Wi-Fi HTTP POST.", table_body_style)
        ],
        [
            Paragraph("<b>Database Layer</b>", table_body_style),
            Paragraph("SQLite3 (Embedded Relational DB)", table_body_style),
            Paragraph("Stores farmer profiles, historical soil readings, ML predictions, and disease diagnostics with zero-config local fallback.", table_body_style)
        ],
        [
            Paragraph("<b>Cloud & Security</b>", table_body_style),
            Paragraph("Render Web Service, HTTPS, Private Git", table_body_style),
            Paragraph("Encrypted deployment on Render with SSL, private GitHub repo model protecting ML code and API keys.", table_body_style)
        ]
    ]

    t_tech = Table(tech_table_data, colWidths=[90, 150, 290])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 10))

    # =========================================================
    # 3. CORE APPLICATION MODULES (EXPLANATION FOR GUIDE)
    # =========================================================
    story.append(Paragraph("3. Functional Application Modules", h1_style))

    modules_info = [
        ("🌾 Crop Recommendation Module", "Accepts 7 soil nutrients (N, P, K, pH) and weather parameters (Temperature, Humidity, Rainfall). The pre-trained Random Forest model computes feature probabilities to recommend the most optimal crop with high precision."),
        ("🧪 Soil Health & NPK Diagnostics", "Evaluates macro-nutrients against agricultural benchmark standards. Classifies soil health (Deficient, Optimum, Excess) and suggests corrective organic/chemical conditioning."),
        ("💧 Smart Irrigation Advisor", "Analyzes soil moisture percentage, ambient temperature, and humidity to determine irrigation urgency, optimal watering volume, and schedules to prevent water waste."),
        ("🌿 Fertilizer Advisory System", "Calculates exact nutrient gaps for 22 Indian crops and recommends precise fertilizer dosages (Urea, DAP, MOP) and application stages (Basal, Vegetative, Flowering)."),
        ("🦠 Plant Disease Doctor (Vision AI)", "Farmers upload leaf photos. Gemini Vision AI inspects visual symptoms, diagnoses fungal/bacterial/viral diseases, and generates both organic and chemical treatment remedies."),
        ("🤖🎙️ Multilingual AI Agronomist & Voice", "Allows farmers to type or speak in English, Telugu, Hindi, Tamil, Kannada, or Marathi. AI translates agricultural science into conversational, practical advice and reads answers aloud.")
    ]

    for mod_title, mod_desc in modules_info:
        story.append(Paragraph(f"• <b>{mod_title}</b>: {mod_desc}", bullet_style))

    story.append(Spacer(1, 10))

    # =========================================================
    # 4. SYSTEM ARCHITECTURE & DATA FLOW
    # =========================================================
    story.append(Paragraph("4. System Data Flow & Architecture", h1_style))
    flow_text = (
        "<b>1. Data Ingestion</b>: Soil readings originate from either manual farmer entry in the web interface or automated ESP32 Modbus sensor telemetry.<br/>"
        "<b>2. Processing & Storage</b>: Data is validated and stored in SQLite tables. ML models evaluate soil parameters to predict ideal crop varieties.<br/>"
        "<b>3. AI Intelligence</b>: Generative AI combines live soil context, ML predictions, and farmer queries to provide contextual farming advisory in regional languages.<br/>"
        "<b>4. Output Delivery</b>: Results are presented via high-contrast UI cards, metrics, and crystal-clear browser voice synthesis."
    )
    story.append(Paragraph(flow_text, body_style))
    story.append(Spacer(1, 10))

    # =========================================================
    # 5. SECURITY & INTELLECTUAL PROPERTY PROTECTION
    # =========================================================
    story.append(Paragraph("5. Security, Privacy & Cloud Deployment", h1_style))
    sec_points = [
        ("Private Codebase", "Source code and trained ML model artifacts are maintained in a Private GitHub repository, preventing unauthorized cloning or plagiarism."),
        ("Encrypted Cloud Execution", "Deployed on Render over HTTPS/TLS. The backend runs inside an isolated container; users cannot access files or model weights."),
        ("Zero Secret Leaks", "API credentials (GEMINI_API_KEY) are injected as encrypted environment variables and strictly excluded from Git tracking via .gitignore."),
        ("Hybrid Local-First Resiliency", "The application operates seamlessly in offline SQLite mode even if external network servers are unreachable.")
    ]
    for sec_title, sec_desc in sec_points:
        story.append(Paragraph(f"• <b>{sec_title}</b>: {sec_desc}", bullet_style))

    story.append(Spacer(1, 14))
    story.append(HRFlowable(width="100%", thickness=1, color=c_secondary, spaceAfter=8))
    story.append(Paragraph("<i>AgriSense AI Project Documentation — Prepared for Academic Guide Evaluation & Presentation</i>", ParagraphStyle('Footer', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8, textColor=c_gray, alignment=1)))

    doc.build(story)
    print(f"✅ PDF successfully generated: {pdf_filename}")

if __name__ == "__main__":
    build_pdf()
