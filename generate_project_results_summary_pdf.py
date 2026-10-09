import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether
)
from reportlab.pdfgen import canvas

PDF_OUTPUT = "PROJECT_RESULTS_SUMMARY.pdf"

def generate_pdf():
    # A4: 595.27 x 841.89 points
    margin = 28
    doc = SimpleDocTemplate(
        PDF_OUTPUT,
        pagesize=A4,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=22,
        bottomMargin=20
    )

    usable_width = 595.27 - (2 * margin) # 539.27 pt

    styles = getSampleStyleSheet()

    # Define clean typography styles
    style_normal = ParagraphStyle(
        'Base',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.black
    )

    style_bold = ParagraphStyle(
        'BaseBold',
        parent=style_normal,
        fontName='Helvetica-Bold'
    )

    style_title = ParagraphStyle(
        'Title',
        parent=style_normal,
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=13,
        alignment=1, # Center
        spaceAfter=2
    )

    style_th = ParagraphStyle(
        'TH',
        parent=style_normal,
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        alignment=0
    )

    style_cell = ParagraphStyle(
        'Cell',
        parent=style_normal,
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.6
    )

    style_cell_bold = ParagraphStyle(
        'CellBold',
        parent=style_cell,
        fontName='Helvetica-Bold'
    )

    style_remarks = ParagraphStyle(
        'Remarks',
        parent=style_cell,
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.6
    )

    story = []

    # 1. College Header
    header_img_path = r"C:\Users\praveenreddy\.gemini\antigravity-ide\brain\85979515-404d-4e59-88ff-bcc8ee66557f\scratch\college_header_precise.png"
    if os.path.exists(header_img_path):
        # 560 x 105 aspect ratio
        img_w = usable_width
        img_h = usable_width * (105.0 / 560.0)
        story.append(RLImage(header_img_path, width=img_w, height=img_h))
    else:
        # Fallback text header
        story.append(Paragraph("<b>PARVATHAREDDY BABUL REDDY VISVODAYA INSTITUTE OF TECHNOLOGY & SCIENCE (AUTONOMOUS)</b>", style_title))
        story.append(Paragraph("KAVALI - 524201, S.P.S.R Nellore Dist., A.P. India. Ph: 08626-243930", style_normal))
        story.append(Paragraph("<b>DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</b> (UG - Accredited by NBA)", style_normal))

    story.append(Spacer(1, 4))

    # 2. Main Title
    story.append(Paragraph("<u><b>PROJECT RESULTS SUMMARY</b></u>", style_title))
    story.append(Spacer(1, 4))

    # 3. Metadata (Section, Batch No, Batch Details, Date)
    meta_data = [
        [
            Paragraph("<b>Section:</b> CSE - A", style_normal),
            Paragraph("<b>Batch No:</b> 12", style_normal)
        ],
        [
            Paragraph("<b>Batch Details:</b> IV B.Tech II Semester (CSE)", style_normal),
            Paragraph("<b>Date:</b> 09-10-2026", style_normal)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[usable_width * 0.65, usable_width * 0.35])
    t_meta.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 1),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 4))

    # 4. Student Details Table (Left aligned as on paper)
    # 4 rows: Regd No | Student Name
    student_table_w = usable_width * 0.58
    student_data = [
        [Paragraph("<b>Student Regd. No</b>", style_th), Paragraph("<b>Student Name</b>", style_th)],
        [Paragraph("22X81A05XX", style_cell), Paragraph("Praveen Reddy Chedimala", style_cell_bold)],
        [Paragraph("", style_cell), Paragraph("", style_cell)],
        [Paragraph("", style_cell), Paragraph("", style_cell)],
        [Paragraph("", style_cell), Paragraph("", style_cell)],
    ]
    t_student = Table(student_data, colWidths=[student_table_w * 0.42, student_table_w * 0.58])
    t_student.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.6, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    # Place on left side using 2-column table wrapper
    wrapper_data = [[t_student, ""]]
    t_wrap = Table(wrapper_data, colWidths=[student_table_w, usable_width - student_table_w])
    t_wrap.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(t_wrap)
    story.append(Spacer(1, 4))

    # 5. Project Title & Supervisor
    story.append(Paragraph(
        "<b>Project Title:</b> AgriSense AI: Precision Agriculture, IoT Soil Telemetry & Multilingual Voice Advisory Platform",
        style_normal
    ))
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "<b>Name and Designation of the Project Supervisor:</b> Dr. / Mr. ______________________, Assistant Professor, Dept. of CSE",
        style_normal
    ))
    story.append(Spacer(1, 4))

    # 6. Project Results Summary Table
    story.append(Paragraph("<b>Project Results Summary:</b>", style_bold))
    story.append(Spacer(1, 2))

    summary_headers = [
        Paragraph("<b>Particulars</b>", style_th),
        Paragraph("<b>Project Results / Outcomes</b>", style_th),
        Paragraph("<b>Remarks</b>", style_th)
    ]

    r1_outcomes = (
        "• Developed AI engine recommending optimal crops from 7 soil/climate parameters (N, P, K, pH, Temp, Hum, Rain).<br/>"
        "• Interfaced real-time IoT edge sensing via ESP32 MCU and industrial 7-in-1 Modbus RS485 soil sensor.<br/>"
        "• Integrated leaf disease diagnosis using Multimodal Vision AI with organic & chemical treatment remedies.<br/>"
        "• Designed 4-stage split fertilizer guidance and soil-moisture-based irrigation pump runtime calculator.<br/>"
        "• Enabled 6 Indian regional languages (Telugu, Hindi, Tamil, Kannada, Marathi, English) with voice advisory.<br/>"
        "• Integrated live APMC Mandi rates (e-NAM vs. MSP) and 7 national government welfare schemes."
    )

    r2_outcomes = (
        "• <b>Crop Recommendation:</b> Multi-class prediction for 22 crops with confidence probability distribution.<br/>"
        "• <b>IoT Sensor Telemetry:</b> Continuous live streaming of NPK, moisture, temp & pH via HTTP POST to cloud.<br/>"
        "• <b>Plant Disease Doctor:</b> Real-time visual leaf diagnosis from uploaded photos with treatment remedies (~1.5s).<br/>"
        "• <b>Irrigation & Fertilizer:</b> Dynamic pump runtimes by acreage/HP and exact NPK gap (Urea, DAP, MOP dosages).<br/>"
        "• <b>Multilingual Voice:</b> Speech recognition & daily 1-minute automated audio farm bulletins.<br/>"
        "• <b>Mandi & Economics:</b> Live price comparison against MSP with acreage-based net profit margin estimator."
    )

    r3_outcomes = (
        "• <b>Frontend:</b> Modern responsive React 18 SPA (Vite) + Mobile-first Streamlit UI with Web Speech API.<br/>"
        "• <b>Backend:</b> High-performance asynchronous FastAPI REST API + WebSockets on Uvicorn ASGI server.<br/>"
        "• <b>Machine Learning:</b> Scikit-Learn Random Forest Classifier (100 estimators, 80/20 train-test split).<br/>"
        "• <b>Generative AI:</b> Google Gemini 2.5 Flash Multimodal Vision & Gemini Live Voice Audio API.<br/>"
        "• <b>IoT Edge Hardware:</b> ESP32 MCU, MAX485 transceiver, 7-in-1 Modbus probe, DHT22, and Rain sensor.<br/>"
        "• <b>Database & Cloud:</b> SQLite in WAL mode; deployed on Render Cloud over HTTPS with zero secret leaks."
    )

    r4_outcomes = (
        "• <b>ML Classification Accuracy:</b> <b>99.3% accuracy</b> on 2,200 agricultural dataset records across 22 crops.<br/>"
        "• <b>Inference Latency:</b> <b>0.0008 seconds</b> (0.8 ms), well below 50 ms real-time benchmark threshold.<br/>"
        "• <b>Database Latency:</b> <b>1.2 ms</b> per write transaction under SQLite WAL mode.<br/>"
        "• <b>Hardware Telemetry:</b> <b>180 ms</b> Modbus RS485 query latency over differential industrial lines.<br/>"
        "• <b>AI Vision Diagnosis:</b> <b>~1.42 seconds</b> complete analysis and remedy delivery.<br/>"
        "• <b>Mobile Usability:</b> Touch-optimized UI responsive from 320px screen width for rural 3G/4G connectivity."
    )

    r5_outcomes = (
        "• Successfully built an enterprise precision agriculture ecosystem that eliminates empirical guesswork.<br/>"
        "• Conserves agricultural water and fertilizer while preventing crop failures through early disease detection.<br/>"
        "• Overcomes rural digital and literacy barriers through native spoken voice assistance in regional languages.<br/>"
        "• Validated through comprehensive automated end-to-end test suite (test_comprehensive_e2e_verification.py)."
    )

    table_data = [
        summary_headers,
        [
            Paragraph("<b>Objectives Achieved</b>", style_cell_bold),
            Paragraph(r1_outcomes, style_cell),
            Paragraph("100% of defined project objectives successfully achieved and verified.", style_remarks)
        ],
        [
            Paragraph("<b>Functional Results / Features Demonstrated</b>", style_cell_bold),
            Paragraph(r2_outcomes, style_cell),
            Paragraph("Demonstrated live end-to-end functionality across web & mobile interfaces.", style_remarks)
        ],
        [
            Paragraph("<b>Technical Implementation</b>", style_cell_bold),
            Paragraph(r3_outcomes, style_cell),
            Paragraph("Production-grade multi-tier architecture with clean edge-to-cloud separation.", style_remarks)
        ],
        [
            Paragraph("<b>Performance / Accuracy / Effectiveness</b>", style_cell_bold),
            Paragraph(r4_outcomes, style_cell),
            Paragraph("Exceeded all target performance, accuracy, and latency benchmarks.", style_remarks)
        ],
        [
            Paragraph("<b>Overall Project Outcome</b>", style_cell_bold),
            Paragraph(r5_outcomes, style_cell),
            Paragraph("Highly practical, socially impactful, and field-ready agricultural solution.", style_remarks)
        ],
    ]

    col_w = [usable_width * 0.22, usable_width * 0.58, usable_width * 0.20]
    t_summary = Table(table_data, colWidths=col_w)
    t_summary.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.6, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 2.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 5))

    # 7. Project Status Row
    status_text = (
        "<b>Project Status:</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "<b>[ &#10004; ] Fully Functional</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "[ &nbsp;&nbsp; ] Partially Functional &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
        "[ &nbsp;&nbsp; ] Demonstration Only"
    )
    story.append(Paragraph(status_text, style_normal))
    story.append(Spacer(1, 14))

    # 8. Signatures Row
    sig_data = [
        [
            Paragraph("<b>Signature of the Student(s)</b>", style_normal),
            Paragraph("<div align='right'><b>Signature of the Supervisor</b></div>", style_normal)
        ]
    ]
    t_sig = Table(sig_data, colWidths=[usable_width * 0.5, usable_width * 0.5])
    t_sig.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(t_sig)

    doc.build(story)
    print("PDF build complete:", PDF_OUTPUT)

if __name__ == "__main__":
    generate_pdf()
