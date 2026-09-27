import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, Image as RLImage
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
        self.drawString(36, 592, "🌱 AGRISENSE AI — VISUAL STEP-BY-STEP FARMER OPERATING GUIDE & SLIDES")
        self.drawRightString(792 - 36, 592, "PRECISION AGRI-TECH PLATFORM")

        # Slide Footer
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.75)
        self.line(36, 32, 792 - 36, 32)
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(36, 20, "AgriSense AI Official Visual Help Center • Image-Driven Farmer Flow with Pointer Arrows")
        page_str = f"Slide {self._pageNumber} of {page_count}"
        self.drawRightString(792 - 36, 20, page_str)

        self.restoreState()


def generate_presentation():
    print("Generating AgriSense AI Farmer Guide Presentation Slides PDF with UI Mockup Images...")

    # Landscape 792 x 612
    doc = SimpleDocTemplate(
        PDF_PRESENTATION_PATH,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=38
    )

    styles = getSampleStyleSheet()

    PRIMARY = colors.HexColor("#14532d")
    SECONDARY = colors.HexColor("#16a34a")
    DARK_TEXT = colors.HexColor("#0f172a")
    BODY_TEXT = colors.HexColor("#334155")
    ACCENT_BG = colors.HexColor("#f0fdf4")
    BORDER_COLOR = colors.HexColor("#cbd5e1")
    ALERT_RED = colors.HexColor("#dc2626")

    slide_title = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=PRIMARY,
        spaceAfter=3
    )

    slide_subtitle = ParagraphStyle(
        'SlideSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=SECONDARY,
        spaceAfter=10
    )

    body_p = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=BODY_TEXT,
        spaceAfter=6
    )

    bullet_p = ParagraphStyle(
        'SlideBullet',
        parent=body_p,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=4
    )

    def make_visual_slide(step_num, title, subtitle, image_filename, tap_instructions, color_meanings, pro_tip):
        """Construct a high-impact slide pairing the marked UI mockup screenshot with structured farmer guidance."""
        elements = []
        elements.append(Paragraph(f"<b>STEP {step_num}: {title}</b>", slide_title))
        elements.append(Paragraph(subtitle, slide_subtitle))

        # Left Column: Image with UI Mockup & Arrows
        img_path = os.path.join("images", image_filename)
        if os.path.exists(img_path):
            img_flowable = RLImage(img_path, width=440, height=255)
        else:
            img_flowable = Paragraph(f"<b>[Image {image_filename} not found]</b>", body_p)

        # Right Column: Clean Action & Tap Guidance Card
        right_card_content = [
            Paragraph(f"<b>🎯 WHERE TO TAP & FOLLOW:</b>", ParagraphStyle('RT1', fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=ALERT_RED, spaceAfter=4)),
            Paragraph(tap_instructions, ParagraphStyle('RT2', fontName='Helvetica', fontSize=9.2, leading=13, textColor=DARK_TEXT, spaceAfter=8)),
            
            Paragraph(f"<b>🎨 COLOR & SYMBOL MEANING:</b>", ParagraphStyle('RT3', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=PRIMARY, spaceAfter=3)),
            Paragraph(color_meanings, ParagraphStyle('RT4', fontName='Helvetica', fontSize=8.8, leading=12.5, textColor=BODY_TEXT, spaceAfter=8)),

            Paragraph(f"<b>💡 FARMER PRO-TIP:</b><br/>{pro_tip}", ParagraphStyle('RT5', fontName='Helvetica', fontSize=8.8, leading=12.5, textColor=DARK_TEXT, backColor=ACCENT_BG, borderColor=colors.HexColor("#86efac"), borderWidth=0.5, borderPadding=5))
        ]

        right_tbl = Table([[right_card_content]], colWidths=[265])
        right_tbl.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))

        # Two-column grid table (445pt image + 270pt guidance card = 715pt)
        split_table = Table([[img_flowable, right_tbl]], colWidths=[445, 270])
        split_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))

        elements.append(split_table)
        return elements

    story = []

    # =========================================================================
    # SLIDE 1: COVER SLIDE
    # =========================================================================
    story.append(Spacer(1, 35))
    story.append(Paragraph("🌱 AGRISENSE AI", ParagraphStyle('CoverT', fontName='Helvetica-Bold', fontSize=32, leading=38, textColor=PRIMARY, alignment=1)))
    story.append(Paragraph("IMAGE-DRIVEN STEP-BY-STEP FARMER OPERATING FLOW", ParagraphStyle('CoverST', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=SECONDARY, alignment=1, spaceAfter=18)))
    story.append(HRFlowable(width="85%", thickness=2, color=PRIMARY, spaceBefore=0, spaceAfter=20))

    cover_meta = [
        [Paragraph("<b>Target Audience:</b> Indian Farmers, Extension Workers, KVK Scientists", body_p), Paragraph("<b>Visual Format:</b> Screenshot Cards + Pointer Arrows", body_p)],
        [Paragraph("<b>Supported Languages:</b> English, Telugu, Hindi, Tamil, Kannada, Marathi", body_p), Paragraph("<b>Platform Release:</b> AgriSense AI v2.0 Enterprise", body_p)],
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
    # SLIDE 2: 7-STEP VISUAL WORKFLOW OVERVIEW
    # =========================================================================
    story.append(Paragraph("🚜 7-Step Complete Agricultural Decision Flow", slide_title))
    story.append(Paragraph("Clear visual progression from login to soil readings, AI crop choice, irrigation, and medicine", slide_subtitle))

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
    story.append(Spacer(1, 14))
    story.append(Paragraph("• <b>Visual-First Design:</b> Every screen uses large color indicators (🔴 Red, 🟡 Yellow, 🟢 Green) and red pointer arrows.", bullet_p))
    story.append(Paragraph("• <b>Spoken Regional Audio:</b> Non-literate farmers can tap <i>'🔊 Listen to This Step'</i> in Telugu, Hindi, Tamil, Kannada, Marathi, or English.", bullet_p))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 3: STEP 1 - LOGIN & LANGUAGE
    # =========================================================================
    story.extend(make_visual_slide(
        "1",
        "Select Language & Farmer Login",
        "Personalized advisory configured to your mother tongue with simple mobile number authentication",
        "step1_login_ui.png",
        "<b>1.</b> Look at the top bar and tap your mother tongue chip (e.g. <b>తెలుగు / Hindi</b>).<br/>"
        "<b>2.</b> Type your 10-digit mobile number in the box.<br/>"
        "<b>3.</b> Tap the large green <b>[ 🚜 Enter Dashboard ]</b> button.",
        "• 🟢 <b>Green Chip:</b> Active language selected.<br/>"
        "• ⚪ <b>White Input:</b> Enter your 10-digit phone number.",
        "You can switch languages anytime from the top bar without losing any recorded data."
    ))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 4: STEP 2 - FARM DATA & ESP32
    # =========================================================================
    story.extend(make_visual_slide(
        "2",
        "Input Soil Data or Connect Live ESP32 Sensor",
        "Capturing soil Nitrogen (N), Phosphorus (P), Potassium (K), pH, and Moisture telemetry",
        "step2_farm_data_ui.png",
        "<b>1.</b> Open 'My Farm Data'. Standard soil readings (N:80, P:42, K:43) are pre-filled.<br/>"
        "<b>2.</b> Adjust any values to match your soil test and tap <b>[ 💾 Save Farm Data ]</b>.<br/>"
        "<b>3.</b> Or plug in the ESP32 sensor for live automatic reading sync.",
        "• 🟢 <b>Green Cards:</b> Nutrients in optimal balance.<br/>"
        "• 🟡 <b>Yellow Card:</b> Soil moisture needs attention.",
        "Insert the ESP32 sensor probe 10 cm deep into root-zone soil for maximum reading accuracy."
    ))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 5: STEP 3 - AI CROP RECOMMENDATION
    # =========================================================================
    story.extend(make_visual_slide(
        "3",
        "Get AI Crop Recommendation & Ranked Alternatives",
        "Machine learning model evaluates soil nutrients and climate to recommend the most profitable crop",
        "step3_crop_recommendation_ui.png",
        "<b>1.</b> Tap the green button <b>[ 🌾 Find Best Crop ]</b>.<br/>"
        "<b>2.</b> Look at the <b>#1 Recommended Crop Card</b> (e.g. Rice with 96% match).<br/>"
        "<b>3.</b> Tap <i>'Check Water Schedule'</i> or <i>'View Fertilizer Plan'</i> to proceed.",
        "• 🟢 <b>Green Card:</b> Top recommended crop for maximum yield.<br/>"
        "• ⚪ <b>Right Cards:</b> Top alternative crops ranked by match score.",
        "Check local market mandi prices for the top 2 alternatives before final sowing."
    ))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 6: STEP 4 - SMART IRRIGATION
    # =========================================================================
    story.extend(make_visual_slide(
        "4",
        "Smart Moisture-Driven Irrigation & Motor Timer",
        "Preventing crop water stress, saving groundwater, and calculating exact pumping hours",
        "step4_irrigation_advisor_ui.png",
        "<b>1.</b> Look at the top banner: 🔴 <b>RED</b> means water today; 🟢 <b>GREEN</b> means moist.<br/>"
        "<b>2.</b> Tap <b>[ 🔊 Play Voice Irrigation Advice ]</b> to hear the spoken plan.<br/>"
        "<b>3.</b> Read the box: <b>RUN MOTOR FOR 3.5 HOURS</b> for 1.0 acre on 5HP pump.",
        "• 🔴 <b>Red Gauge:</b> Soil is dry (&lt;25%) — Water immediately!<br/>"
        "• 🔵 <b>Blue Box:</b> Exact water liters (15,000 L) and pumping time.",
        "Irrigate in cool early mornings (6-9 AM) to prevent 30% solar evaporation loss."
    ))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 7: STEP 5 - FERTILIZER SCHEDULE
    # =========================================================================
    story.extend(make_visual_slide(
        "5",
        "Precision Fertilizer Plan & 4-Stage Split Schedule",
        "Eliminating fertilizer wastage, preventing soil acidity, and balancing N-P-K",
        "step5_fertilizer_advisor_ui.png",
        "<b>1.</b> Look at total bags needed: <b>Urea: 2 Bags • DAP: 1 Bag • Potash: 0.7 Bag</b>.<br/>"
        "<b>2.</b> Follow the 4-Stage Cards: Stage 1 (Basal Day 0), Stage 2 (Tillering Day 25), Stage 3 (Panicle Day 50), Stage 4 (Grain Day 75).",
        "• 🟢 <b>Stage 1:</b> Basal sowing dose.<br/>"
        "• 🔵 <b>Stage 2:</b> 1st Urea top-dressing.<br/>"
        "• 🟣 <b>Stage 3:</b> Panicle boost.<br/>"
        "• 🟡 <b>Stage 4:</b> Potash grain fill spray.",
        "Never dump all Urea at once; 3 split doses prevent nitrogen burning and root leaching."
    ))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 8: STEP 6 - LEAF DISEASE DOCTOR
    # =========================================================================
    story.extend(make_visual_slide(
        "6",
        "Plant Leaf Disease Doctor (Photo Diagnosis)",
        "Multimodal Computer Vision detecting leaf pathologies with organic and chemical cures",
        "step6_disease_doctor_ui.png",
        "<b>1.</b> Take a close-up photo of the affected leaf in clear daylight.<br/>"
        "<b>2.</b> Tap <b>[ 🤖 Analyze Leaf Disease ]</b>.<br/>"
        "<b>3.</b> Read the diagnosis report: Disease Name + Organic Remedy + Chemical Spray Dose.",
        "• 🔴 <b>Red Alert:</b> Disease detected (e.g. Rice Blast).<br/>"
        "• 🟢 <b>Green Box:</b> Organic cure (Neem oil 5ml/L).<br/>"
        "• ⚪ <b>White Box:</b> Chemical fungicide dose (Tricyclazole 0.6g/L).",
        "Take photos in bright natural daylight rather than in dark shade for highest AI accuracy."
    ))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 9: STEP 7 - VOICE AI & KISAN CALL
    # =========================================================================
    story.extend(make_visual_slide(
        "7",
        "Multilingual AI Voice Assistant & Toll-Free Helpline",
        "Conversational agronomy in your mother tongue with zero typing and 1-touch emergency helpline",
        "step7_voice_ai_ui.png",
        "<b>1.</b> Tap the green microphone button <b>[ 🎤 TAP TO SPEAK ]</b> and ask your question naturally in Telugu/Hindi/English.<br/>"
        "<b>2.</b> Listen to the instant spoken audio answer from AgriSense AI.<br/>"
        "<b>3.</b> Or tap <b>[ 📞 CALL 1551 ]</b> for free 24/7 Govt Kisan Helpline.",
        "• 🟢 <b>Green Mic:</b> Tap and speak directly in your voice.<br/>"
        "• 🔵 <b>Blue Button:</b> Toll-free call to Government 1551 Kisan Center.",
        "No typing is needed at all — farmers can operate the entire app purely through voice."
    ))
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 10: SUMMARY & ACCESS
    # =========================================================================
    story.append(Paragraph("🏆 Summary & In-App Help Center Access", slide_title))
    story.append(Paragraph("Empowering every Indian farmer with simple, image-driven precision agriculture", slide_subtitle))

    summary_content = [
        [Paragraph("<b>Unified Visual Guide:</b>", body_p), Paragraph("All 7 steps are visually guided inside the app. Farmers can open the <b>Help Center</b> anytime by selecting <i>'❓ Farmer Help Center & Guide'</i> from the top menu.", body_p)],
        [Paragraph("<b>Image & Voice First:</b>", body_p), Paragraph("Every screen is illustrated with high-contrast color cards, red pointer arrows, and 1-tap regional audio narration.", body_p)],
        [Paragraph("<b>Offline Support:</b>", body_p), Paragraph("Core crop prediction, soil health analysis, irrigation math, and fertilizer schedules run 100% offline via local SQLite.", body_p)],
    ]
    summary_table = Table(summary_content, colWidths=[180, 535])
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
