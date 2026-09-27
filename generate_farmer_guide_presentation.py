import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_PRESENTATION_PATH = "AgriSense_AI_Farmer_Guide_Slides.pdf"


class SlideCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_slide_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_slide_decorations(self, page_count):
        # Landscape 11 x 8.5 inches -> 792 x 612 pt
        self.saveState()
        
        # Slide Header Banner
        self.setFillColor(colors.HexColor("#14532d")) # Forest Green
        self.rect(0, 582, 792, 30, fill=True, stroke=False)
        self.setFont("Helvetica-Bold", 10)
        self.setFillColor(colors.white)
        self.drawString(36, 592, "🌱 AGRISENSE AI — STEP-BY-STEP FARMER OPERATING GUIDE & PRESENTATION")
        self.drawRightString(792 - 36, 592, "PRECISION AGRI-TECH PLATFORM")

        # Slide Footer
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.75)
        self.line(36, 35, 792 - 36, 35)
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(36, 22, "AgriSense AI Official Help Center Guide • Clean Step-by-Step Workflow")
        page_str = f"Slide {self._pageNumber} of {page_count}"
        self.drawRightString(792 - 36, 22, page_str)

        self.restoreState()


def generate_presentation():
    print("Generating AgriSense AI Farmer Guide Presentation Slides PDF...")

    # Landscape 792 x 612
    doc = SimpleDocTemplate(
        PDF_PRESENTATION_PATH,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=42,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    PRIMARY = colors.HexColor("#14532d")
    SECONDARY = colors.HexColor("#16a34a")
    DARK_TEXT = colors.HexColor("#0f172a")
    BODY_TEXT = colors.HexColor("#334155")
    ACCENT_BG = colors.HexColor("#f0fdf4")
    BORDER_COLOR = colors.HexColor("#e2e8f0")

    slide_title = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        spaceAfter=6
    )

    slide_subtitle = ParagraphStyle(
        'SlideSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=SECONDARY,
        spaceAfter=14
    )

    body_p = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=BODY_TEXT,
        spaceAfter=8
    )

    bullet_p = ParagraphStyle(
        'SlideBullet',
        parent=body_p,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=6
    )

    def make_slide_card(step_num, title, action_text, details, tips):
        card_content = [
            Paragraph(f"<b>STEP {step_num}: {title}</b>", ParagraphStyle('CT', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=PRIMARY, spaceAfter=4)),
            Paragraph(f"<b>🎯 Key Action:</b> {action_text}", ParagraphStyle('CA', fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=SECONDARY, spaceAfter=6)),
            Paragraph(f"<b>📋 How to Operate:</b> {details}", body_p),
            Spacer(1, 4),
            Paragraph(f"<b>💡 Pro-Tip for Farmers:</b> {tips}", ParagraphStyle('CP', fontName='Helvetica', fontSize=9.5, leading=13, textColor=DARK_TEXT, backColor=ACCENT_BG, borderColor=colors.HexColor("#86efac"), borderWidth=0.5, borderPadding=6))
        ]
        tbl = Table([[card_content]], colWidths=[720])
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('BOX', (0, 0), (-1, -1), 1.5, BORDER_COLOR),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 16),
            ('RIGHTPADDING', (0, 0), (-1, -1), 16),
        ]))
        return tbl

    story = []

    # =========================================================================
    # SLIDE 1: COVER SLIDE
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("🌱 AGRISENSE AI", ParagraphStyle('CoverT', fontName='Helvetica-Bold', fontSize=32, leading=38, textColor=PRIMARY, alignment=1)))
    story.append(Paragraph("FARMER OPERATING GUIDE & SYSTEM WORKFLOW PRESENTATION", ParagraphStyle('CoverST', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=SECONDARY, alignment=1, spaceAfter=20)))
    story.append(HRFlowable(width="80%", thickness=2, color=PRIMARY, spaceBefore=0, spaceAfter=25))

    cover_meta = [
        [Paragraph("<b>Target Audience:</b> Indian Farmers, Agricultural Officers, Extension Workers", body_p), Paragraph("<b>Platform Release:</b> AgriSense AI v2.0", body_p)],
        [Paragraph("<b>Supported Languages:</b> English, Telugu, Hindi, Tamil, Kannada, Marathi", body_p), Paragraph("<b>Core Features:</b> IoT + ML + Gemini Vision + Voice", body_p)],
    ]
    cover_table = Table(cover_meta, colWidths=[360, 360])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), ACCENT_BG),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#86efac")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(cover_table)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 2: 7-STEP WORKFLOW OVERVIEW
    # =========================================================================
    story.append(Paragraph("🚜 The 7-Step Complete Agricultural Decision Flow", slide_title))
    story.append(Paragraph("From initial login to automated voice advice, disease cure, and irrigation management", slide_subtitle))

    flow_steps = [
        [Paragraph("<b>Step 1</b><br/>🌐 Select Language & Login", body_p), Paragraph("<b>Step 2</b><br/>📡 Enter Soil Data / ESP32", body_p), Paragraph("<b>Step 3</b><br/>🌾 Get AI Crop Choice", body_p), Paragraph("<b>Step 4</b><br/>💧 Check Smart Irrigation", body_p)],
        [Paragraph("<b>Step 5</b><br/>🌿 4-Stage Fertilizer Plan", body_p), Paragraph("<b>Step 6</b><br/>🦠 Leaf Disease Doctor", body_p), Paragraph("<b>Step 7</b><br/>🎙️ Voice Assistant & Call", body_p), Paragraph("<b>Complete</b><br/>🏆 High Yield & Low Cost", body_p)],
    ]
    flow_table = Table(flow_steps, colWidths=[180, 180, 180, 180])
    flow_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1.5, PRIMARY),
        ('INNERGRID', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(flow_table)
    story.append(Spacer(1, 15))
    story.append(Paragraph("• <b>100% In-App:</b> No external tools required. Every step is executed directly inside the AgriSense AI interface.", bullet_p))
    story.append(Paragraph("• <b>Hands-Free Audio:</b> Every page contains a dedicated <i>'Play Audio Guide'</i> button for non-literate farmers.", bullet_p))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 3: STEP 1 - LANGUAGE & LOGIN
    # =========================================================================
    story.append(Paragraph("Step 1: Language Selection & Farmer Profile Login", slide_title))
    story.append(Paragraph("Personalized advisory configured to your regional mother tongue and farm identity", slide_subtitle))
    story.append(make_slide_card(
        "1",
        "Select Mother Tongue & Farmer Login",
        "Choose your language from the top selector dropdown and enter your 10-digit mobile number.",
        "1. Open the app. At the top right, tap <b>Language / భాష / भाषा</b> and choose from English, Telugu, Hindi, Tamil, Kannada, or Marathi.<br/>"
        "2. On the login screen, type your Name (e.g. Ramesh Kumar) and your 10-digit mobile number.<br/>"
        "3. Tap <b>'🚜 Enter Dashboard'</b>. The system automatically creates your secure local farmer profile.",
        "You can switch languages anytime from the top bar or home screen without losing any recorded data."
    ))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 4: STEP 2 - FARM DATA & IOT
    # =========================================================================
    story.append(Paragraph("Step 2: Farm Soil Data & IoT Sensor Ingestion", slide_title))
    story.append(Paragraph("Capturing exact soil Nitrogen, Phosphorus, Potassium, pH, and Moisture", slide_subtitle))
    story.append(make_slide_card(
        "2",
        "Input Soil & Climate Telemetry (Manual or Live ESP32)",
        "Open 'My Farm Data' and choose between Manual Entry mode or Live IoT Sensor mode.",
        "• <b>Manual Entry Mode:</b> Standard regional values (N:80, P:42, K:43, pH:7.2, Moisture:35%) are pre-filled. Adjust any values to match your recent soil test and tap <b>'💾 Save Farm Data'</b>.<br/>"
        "• <b>Live IoT Mode:</b> If you have the ESP32 soil probe, it automatically streams real-time telemetry every 30 seconds.<br/>"
        "• <b>Test Simulator:</b> Tap <i>'⚡ Simulate ESP32 Sensor Reading'</i> to test instant hardware sync without physical probes.",
        "Always ensure your soil probe is inserted at least 10 cm deep into root-zone soil for accurate moisture readings."
    ))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 5: STEP 3 - AI CROP RECOMMENDATION
    # =========================================================================
    story.append(Paragraph("Step 3: Machine Learning Crop Recommendation", slide_title))
    story.append(Paragraph("Scientific crop matching trained on 2,200 records across 22 major commercial crops", slide_subtitle))
    story.append(make_slide_card(
        "3",
        "Generate Top Recommended Crop & Probability Scores",
        "Navigate to 'AI Crop Recommendation' and tap 'Find Best Crop'.",
        "1. The Random Forest ML model evaluates your soil N-P-K, pH, temperature, humidity, and rainfall simultaneously.<br/>"
        "2. It highlights your <b>#1 Best Recommended Crop</b> with optimal season, soil suitability, and expected yield.<br/>"
        "3. Displays visual ranking cards for the top alternative crops with match percentages (e.g., Rice 92%, Maize 84%).<br/>"
        "4. Click <i>'Check Water Schedule'</i> or <i>'View Fertilizer Dosage'</i> to immediately proceed to next steps.",
        "Review the top 3 crop options to match current market mandi prices and local seed availability."
    ))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 6: STEP 4 - SMART IRRIGATION ADVISOR
    # =========================================================================
    story.append(Paragraph("Step 4: Smart Moisture-Driven Irrigation & Pump Timer", slide_title))
    story.append(Paragraph("Preventing crop water stress, saving groundwater, and calculating exact pumping hours", slide_subtitle))
    story.append(make_slide_card(
        "4",
        "Read Moisture Status & Calculate Water Volume Needed",
        "Open 'Smart Irrigation' to check live field moisture and pump run-time math.",
        "• <b>Live AI Water Verdict:</b> Check the top color banner (🔴 Urgent: Irrigate today | 🟡 Irrigate soon | 🟢 Moisture optimal).<br/>"
        "• <b>🔊 Audio Guide:</b> Tap <i>'Play Voice Advice'</i> to hear the spoken watering plan in Telugu/Hindi/English.<br/>"
        "• <b>Growth Stage Timeline:</b> Review critical watering stages (e.g. Rice Tillering & Panicle Initiation, Maize Tasseling).<br/>"
        "• <b>Volume Calculator:</b> Select your farm acres and motor HP (3 HP, 5 HP, Drip) to get exact pumping run-time in hours.",
        "Irrigate during early morning (6:00 - 9:00 AM) or evening (4:30 - 7:00 PM) to eliminate 30% solar evaporation loss."
    ))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 7: STEP 5 - FERTILIZER GUIDANCE & 4 STAGES
    # =========================================================================
    story.append(Paragraph("Step 5: Precision Fertilizer Plan & 4-Stage Split Doses", slide_title))
    story.append(Paragraph("Eliminating fertilizer wastage, preventing soil acidity, and balancing N-P-K", slide_subtitle))
    story.append(make_slide_card(
        "5",
        "Check Soil Nutrient Deficits & Follow 4-Stage Split Schedule",
        "Open 'Fertilizer Guidance' to see commercial bag requirements and application dates.",
        "1. <b>Soil NPK Balance:</b> Check whether Nitrogen, Phosphorus, and Potash are in Deficit, Normal, or Excess.<br/>"
        "2. <b>Bag Calculator:</b> View total bags needed per acre (e.g., Urea: 2.0 Bags • DAP: 1.0 Bag • Potash: 0.7 Bag).<br/>"
        "3. <b>4-Stage Split Schedule:</b> Follow the clear table:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <i>Stage 1 (Basal):</i> Full DAP + Potash + 1/3 Urea at sowing.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <i>Stage 2 (Vegetative 25-35 DAS):</i> 1st Urea top-dressing.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <i>Stage 3 (Flowering 50-60 DAS):</i> 2nd Urea + 19:19:19 foliar spray.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <i>Stage 4 (Grain Filling 75-90 DAS):</i> 0:0:50 Potash spray.",
        "Always split Nitrogen into 3 doses instead of applying all at once to prevent up to 50% nitrate leaching loss."
    ))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 8: STEP 6 - LEAF DISEASE DOCTOR
    # =========================================================================
    story.append(Paragraph("Step 6: Plant Leaf Disease Doctor (Photo Diagnosis)", slide_title))
    story.append(Paragraph("Multimodal Computer Vision detecting leaf pathologies with organic & chemical cures", slide_subtitle))
    story.append(make_slide_card(
        "6",
        "Snap or Upload Leaf Photo for Instant Pathology Diagnosis",
        "Open 'Plant Disease Doctor' and choose between 'Take Photo' or 'Upload Photo'.",
        "1. Aim your mobile camera at the diseased leaf under clear daylight and take a photo.<br/>"
        "2. Tap <b>'🤖 Analyze Plant'</b>. Google Gemini Vision scans leaf discoloration, spots, and fungal rust.<br/>"
        "3. Receive an instant diagnostic report detailing:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• Disease Name & Cause (Fungal, Bacterial, Viral, or Nutrient Deficiency).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• 🌿 <i>Biological / Organic Remedies:</i> (Neem oil spray 5ml/L, Trichoderma viride).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• 🧪 <i>Chemical Treatments:</i> (Specific fungicides like Mancozeb/Copper Oxychloride with safe dosage).",
        "Capture both the top and underside of affected leaves for maximum diagnostic accuracy."
    ))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 9: STEP 7 - VOICE ASSISTANT & LIVE CALL
    # =========================================================================
    story.append(Paragraph("Step 7: Multilingual AI Chat & Gemini Live Call", slide_title))
    story.append(Paragraph("Conversational agronomy assistant in your native language with zero typing required", slide_subtitle))
    story.append(make_slide_card(
        "7",
        "Talk to AgriSense AI Naturally via Microphone or Phone Call Mode",
        "Open 'AgriSense AI Chat & Voice' or 'Gemini Live Call Mode'.",
        "• <b>One-Tap Microphone:</b> Tap the green microphone button, speak your farming question in Telugu, Hindi, Tamil, Kannada, Marathi, or English, and receive an instant voice answer.<br/>"
        "• <b>Quick Prompt Chips:</b> Tap quick questions like <i>'What fertilizer for rice tillering?'</i> or <i>'How to control stem borers?'</i>.<br/>"
        "• <b>Live Phone Call Mode:</b> Connects to low-latency Gemini Live audio WebSocket for real-time natural conversation.",
        "Enable 'Auto-Speak Audio' in settings to have all AI answers read out loud automatically."
    ))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 10: SUMMARY & HELP CENTER ACCESS
    # =========================================================================
    story.append(Paragraph("🏆 Summary & In-App Help Center Access", slide_title))
    story.append(Paragraph("Empowering farmers with end-to-end data-driven agriculture", slide_subtitle))

    summary_content = [
        [Paragraph("<b>Feature Summary:</b>", body_p), Paragraph("All 7 steps are fully unified inside the app. Farmers can access the <b>Help Center</b> anytime by selecting <i>'❓ Farmer Help Center & Guide'</i> from the navigation menu or tapping <i>'📖 Open Guide'</i> on the dashboard home.", body_p)],
        [Paragraph("<b>Zero External Tools:</b>", body_p), Paragraph("Every screen, calculation, audio guide, and diagnosis operates self-contained inside AgriSense AI.", body_p)],
        [Paragraph("<b>Offline Support:</b>", body_p), Paragraph("Core crop prediction, soil health analysis, irrigation math, and fertilizer schedules run 100% offline via local SQLite.", body_p)],
    ]
    summary_table = Table(summary_content, colWidths=[180, 540])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1.5, PRIMARY),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(summary_table)

    doc.build(story, canvasmaker=SlideCanvas)
    print(f"Farmer Guide Presentation PDF generated: {PDF_PRESENTATION_PATH}")


if __name__ == "__main__":
    generate_presentation()
