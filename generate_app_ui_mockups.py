import os
from PIL import Image, ImageDraw, ImageFont

IMAGES_DIR = "images"
os.makedirs(IMAGES_DIR, exist_ok=True)
W, H = 1000, 630

def get_font(size, bold=False):
    path = "C:/Windows/Fonts/Nirmala.ttc"
    if os.path.exists(path):
        try:
            return ImageFont.truetype(path, size, index=1 if bold else 0)
        except Exception:
            pass
    return ImageFont.load_default()

def draw_rounded_rect(draw, bbox, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=int(width))

def draw_pointer_callout(draw, badge_xy, target_xy, step_num, text_indic, text_en=None, color="#dc2626"):
    """
    Draws a professional, high-visibility UI pointer annotation:
    - Glowing badge with step circle '(1)'
    - High-contrast text banner in Indic + English
    - Sharp connecting pointer line and arrow head pointing precisely to the target button/input.
    """
    bx, by = badge_xy
    tx, ty = target_xy
    
    font_bold = get_font(12, bold=True)
    font_sub = get_font(10.5, bold=False)
    
    full_text = f"({step_num}) {text_indic}"
    if text_en:
        full_text += f" • {text_en}"
        
    bbox = draw.textbbox((0, 0), full_text, font=font_bold)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    bw = tw + 26
    bh = th + 16
    
    # Auto-clamp badge coordinates safely within canvas boundaries
    bx = max(bw // 2 + 30, min(W - bw // 2 - 30, bx))
    by = max(bh // 2 + 30, min(H - bh // 2 - 30, by))
    
    # Calculate arrow starting point from nearest edge of badge
    if ty < by - bh//2:
        sx, sy = bx, by - bh//2
    elif ty > by + bh//2:
        sx, sy = bx, by + bh//2
    elif tx < bx - bw//2:
        sx, sy = bx - bw//2, by
    else:
        sx, sy = bx + bw//2, by
        
    # Draw line and arrow FIRST (behind the badge)
    draw.line([(sx, sy), (tx, ty)], fill="#ffffff", width=5)
    draw.line([(sx, sy), (tx, ty)], fill=color, width=3)
    
    # Arrow head pointing to (tx, ty)
    dx = tx - sx
    dy = ty - sy
    dist = max(1, (dx*dx + dy*dy)**0.5)
    ux, uy = dx/dist, dy/dist
    
    arrow_len = 12
    arrow_width = 7
    px, py = -uy, ux
    
    p1 = (tx, ty)
    p2 = (tx - ux*arrow_len + px*arrow_width, ty - uy*arrow_len + py*arrow_width)
    p3 = (tx - ux*arrow_len - px*arrow_width, ty - uy*arrow_len - py*arrow_width)
    draw.polygon([p1, p2, p3], fill=color, outline="#ffffff")
    
    # Draw drop shadow for badge ON TOP
    draw_rounded_rect(draw, (bx - bw//2 + 2, by - bh//2 + 2, bx + bw//2 + 2, by + bh//2 + 2), radius=8, fill="#0f172a")
    # Draw main colored badge
    draw_rounded_rect(draw, (bx - bw//2, by - bh//2, bx + bw//2, by + bh//2), radius=8, fill=color, outline="#ffffff", width=1.5)
    # Draw text inside badge
    draw.text((bx - tw//2, by - th//2 - 1), full_text, fill="#ffffff", font=font_bold)


# =============================================================================
# 1. STEP 1: LOGIN & LANGUAGE SELECTION UI
# =============================================================================
def make_step1_image():
    img = Image.new("RGB", (W, H), "#0f172a")
    draw = ImageDraw.Draw(img)

    draw_rounded_rect(draw, (20, 20, W-20, H-20), radius=16, fill="#ffffff", outline="#334155", width=2)
    draw_rounded_rect(draw, (20, 20, W-20, 75), radius=16, fill="#14532d")
    draw.rectangle((20, 55, W-20, 75), fill="#14532d")
    draw.text((40, 34), "AgriSense AI — Smart Agriculture Platform", fill="#ffffff", font=get_font(18, bold=True))

    # Top Language Selector Chips
    draw.text((40, 92), "Select Your Language / మీ భాషను ఎంచుకోండి:", fill="#1e293b", font=get_font(13, bold=True))
    langs = [("English", False), ("తెలుగు (Telugu)", True), ("हिन्दी (Hindi)", False), ("தமிழ் (Tamil)", False), ("ಕನ್ನಡ (Kannada)", False), ("मराठी (Marathi)", False)]
    lx = 40
    for ltext, active in langs:
        bg = "#16a34a" if active else "#f1f5f9"
        fg = "#ffffff" if active else "#334155"
        border = "#15803d" if active else "#cbd5e1"
        bbox = draw.textbbox((0, 0), ltext, font=get_font(11.5, bold=active))
        tw = bbox[2] - bbox[0] + 20
        draw_rounded_rect(draw, (lx, 118, lx + tw, 148), radius=8, fill=bg, outline=border, width=1.5 if active else 1)
        draw.text((lx + 10, 125), ltext, fill=fg, font=get_font(11.5, bold=active))
        lx += tw + 8

    # Login Form Box - Centered with comfortable side margins for callouts
    draw_rounded_rect(draw, (230, 170, 770, 510), radius=16, fill="#f8fafc", outline="#cbd5e1", width=2)
    draw.text((260, 190), "Farmer Profile Login / రైతు లాగిన్", fill="#0f172a", font=get_font(19, bold=True))
    draw.text((260, 218), "Enter your details to open your personalized farm dashboard", fill="#64748b", font=get_font(11.5))

    # Name Input
    draw.text((260, 252), "Farmer Name / రైతు పేరు:", fill="#334155", font=get_font(12.5, bold=True))
    draw_rounded_rect(draw, (260, 274, 740, 314), radius=8, fill="#ffffff", outline="#94a3b8", width=1)
    draw.text((275, 284), "Ramesh Kumar (రమేష్ కుమార్)", fill="#0f172a", font=get_font(13.5))

    # Mobile Input
    draw.text((260, 330), "Mobile Number / మొబైల్ నంబర్ (10 Digits):", fill="#334155", font=get_font(12.5, bold=True))
    draw_rounded_rect(draw, (260, 352, 740, 392), radius=8, fill="#ffffff", outline="#94a3b8", width=1)
    draw.text((275, 362), "98765 43210", fill="#0f172a", font=get_font(13.5, bold=True))

    # Big Green Login Button
    draw_rounded_rect(draw, (260, 420, 740, 475), radius=10, fill="#16a34a", outline="#15803d", width=2)
    draw.text((370, 435), "Enter Dashboard / లాగిన్ అవ్వండి", fill="#ffffff", font=get_font(15, bold=True))

    # Callout Annotations - Precision Positioned in Clean Side Margins
    draw_pointer_callout(draw, (360, 95), (170, 118), "1", "భాషను ఎంచుకోండి", "Select Telugu", color="#dc2626")
    draw_pointer_callout(draw, (865, 372), (740, 372), "2", "నంబర్ నమోదు చేయండి", "Enter Mobile", color="#0284c7")
    draw_pointer_callout(draw, (500, 565), (500, 475), "3", "ఇక్కడ నొక్కండి", "TAP TO ENTER", color="#16a34a")

    path = os.path.join(IMAGES_DIR, "step1_login_ui.png")
    img.save(path, quality=95)
    print(f"Generated: {path}")


# =============================================================================
# 2. STEP 2: FARM SOIL DATA & ESP32 IOT SYNC
# =============================================================================
def make_step2_image():
    img = Image.new("RGB", (W, H), "#0f172a")
    draw = ImageDraw.Draw(img)

    draw_rounded_rect(draw, (20, 20, W-20, H-20), radius=16, fill="#ffffff", outline="#334155", width=2)
    draw_rounded_rect(draw, (20, 20, W-20, 75), radius=16, fill="#14532d")
    draw.rectangle((20, 55, W-20, 75), fill="#14532d")
    draw.text((40, 34), "Step 2: My Farm Data & ESP32 IoT Soil Telemetry", fill="#ffffff", font=get_font(18, bold=True))

    # IoT Status Banner
    draw_rounded_rect(draw, (40, 90, W-40, 140), radius=10, fill="#dcfce7", outline="#86efac", width=1)
    draw.text((55, 102), "ESP32 7-in-1 Soil Sensor Status: CONNECTED & SYNCED (Real-time Telemetry)", fill="#166534", font=get_font(12.5, bold=True))
    draw.text((55, 122), "Hardware ID: ESP32-AGRI-01 • Last Sync: Just Now • Status: Online 100%", fill="#15803d", font=get_font(11))

    # Metric Cards Grid
    cards = [
        ("Nitrogen (N)", "80 kg/ha", "Optimal", "#22c55e", "#f0fdf4", "#86efac"),
        ("Phosphorus (P)", "42 kg/ha", "Good", "#22c55e", "#f0fdf4", "#86efac"),
        ("Potassium (K)", "43 kg/ha", "Good", "#22c55e", "#f0fdf4", "#86efac"),
        ("Soil pH", "7.2 pH", "Neutral", "#3b82f6", "#eff6ff", "#93c5fd"),
        ("Moisture", "35 %", "Moderate", "#eab308", "#fefce8", "#fde047")
    ]
    cx = 40
    cw = 172
    for title, val, status, col, bg, border in cards:
        draw_rounded_rect(draw, (cx, 155, cx + cw, 330), radius=12, fill=bg, outline=border, width=1)
        draw.text((cx + 14, 170), title, fill="#475569", font=get_font(12, bold=True))
        draw.text((cx + 14, 205), val, fill="#0f172a", font=get_font(20, bold=True))
        draw_rounded_rect(draw, (cx + 14, 275, cx + cw - 14, 305), radius=6, fill=col)
        draw.text((cx + 35, 283), status, fill="#ffffff", font=get_font(11, bold=True))
        cx += cw + 15

    # Bottom Actions
    draw_rounded_rect(draw, (40, 355, 480, 510), radius=12, fill="#f8fafc", outline="#cbd5e1", width=1)
    draw.text((60, 372), "Manual Data Entry Mode / నేల వివరాలు", fill="#0f172a", font=get_font(14, bold=True))
    draw.text((60, 396), "Pre-filled with standard regional soil test values.", fill="#64748b", font=get_font(11.5))
    draw_rounded_rect(draw, (60, 435, 460, 480), radius=8, fill="#16a34a")
    draw.text((180, 448), "Save Farm Data", fill="#ffffff", font=get_font(14, bold=True))

    draw_rounded_rect(draw, (520, 355, 960, 510), radius=12, fill="#f8fafc", outline="#cbd5e1", width=1)
    draw.text((540, 372), "Live IoT Simulation & Calibration / సెన్సార్", fill="#0f172a", font=get_font(14, bold=True))
    draw.text((540, 396), "Sync live RS485 NPK probe readings directly.", fill="#64748b", font=get_font(11.5))
    draw_rounded_rect(draw, (540, 435, 940, 480), radius=8, fill="#0284c7")
    draw.text((640, 448), "Simulate ESP32 Sensor Sync", fill="#ffffff", font=get_font(14, bold=True))

    # Pointers
    draw_pointer_callout(draw, (260, 565), (260, 480), "1", "నేల వివరాలు సేవ్ చేయండి", "Save Soil Data", color="#16a34a")
    draw_pointer_callout(draw, (740, 565), (740, 480), "2", "సెన్సార్ కలపండి", "Sync ESP32 Sensor", color="#0284c7")

    path = os.path.join(IMAGES_DIR, "step2_farm_data_ui.png")
    img.save(path, quality=95)
    print(f"Generated: {path}")


# =============================================================================
# 3. STEP 3: AI CROP RECOMMENDATION UI
# =============================================================================
def make_step3_image():
    img = Image.new("RGB", (W, H), "#0f172a")
    draw = ImageDraw.Draw(img)

    draw_rounded_rect(draw, (20, 20, W-20, H-20), radius=16, fill="#ffffff", outline="#334155", width=2)
    draw_rounded_rect(draw, (20, 20, W-20, 75), radius=16, fill="#14532d")
    draw.rectangle((20, 55, W-20, 75), fill="#14532d")
    draw.text((40, 34), "Step 3: Machine Learning AI Crop Recommendation", fill="#ffffff", font=get_font(18, bold=True))

    # Trigger Button Box
    draw_rounded_rect(draw, (40, 90, W-40, 150), radius=12, fill="#f0fdf4", outline="#86efac", width=1)
    draw_rounded_rect(draw, (60, 100, 450, 140), radius=8, fill="#16a34a")
    draw.text((80, 112), "Find Best Crop / మంచి పంటను తెలుసుకోండి", fill="#ffffff", font=get_font(13.5, bold=True))
    draw.text((470, 112), "AI Model evaluated 2,200 soil-climate records", fill="#166534", font=get_font(12.5, bold=True))

    # #1 Top Recommended Crop Card
    draw_rounded_rect(draw, (40, 165, 580, 510), radius=16, fill="#f0fdf4", outline="#16a34a", width=3)
    draw.text((65, 185), "#1 TOP RECOMMENDED CROP", fill="#15803d", font=get_font(12, bold=True))
    draw.text((65, 210), "RICE / వరి (Paddy)", fill="#0f172a", font=get_font(24, bold=True))
    draw.text((65, 252), "Confidence Match Score: 96.4% Highly Suitable", fill="#16a34a", font=get_font(13.5, bold=True))
    
    draw.text((65, 290), "• Season: Kharif / Rabi (Wetlands)", fill="#334155", font=get_font(12.5))
    draw.text((65, 318), "• Soil Suitability: Clay loam, High Nitrogen (80 kg/ha)", fill="#334155", font=get_font(12.5))
    draw.text((65, 346), "• Expected Yield: 24 - 28 Quintals / Acre", fill="#334155", font=get_font(12.5))
    draw.text((65, 374), "• Profit Potential: HIGH (Current Mandi Rs 2,200/Q)", fill="#334155", font=get_font(12.5))

    # Quick action chips
    draw_rounded_rect(draw, (65, 425, 295, 470), radius=8, fill="#0284c7")
    draw.text((85, 440), "Check Water Schedule", fill="#ffffff", font=get_font(12, bold=True))
    draw_rounded_rect(draw, (315, 425, 555, 470), radius=8, fill="#16a34a")
    draw.text((335, 440), "View Fertilizer Plan", fill="#ffffff", font=get_font(12, bold=True))

    # Alternative Crops Column
    draw_rounded_rect(draw, (610, 165, 960, 510), radius=16, fill="#f8fafc", outline="#cbd5e1", width=1)
    draw.text((630, 185), "Top Alternative Crop Options:", fill="#0f172a", font=get_font(14.5, bold=True))

    alts = [
        ("Maize (మొక్కజొన్న)", "88.2% Match", "Low water, high market demand", "#16a34a"),
        ("Jute (జనపనార)", "81.5% Match", "Ideal for high moisture clay soils", "#0284c7"),
        ("Cotton (పత్తి)", "74.0% Match", "High commercial value in black soil", "#d97706")
    ]
    ay = 220
    for aname, amatch, adesc, acol in alts:
        draw_rounded_rect(draw, (630, ay, 940, ay + 72), radius=10, fill="#ffffff", outline="#e2e8f0", width=1)
        draw.text((645, ay + 12), aname, fill="#0f172a", font=get_font(13.5, bold=True))
        draw.text((820, ay + 12), amatch, fill=acol, font=get_font(11.5, bold=True))
        draw.text((645, ay + 40), adesc, fill="#64748b", font=get_font(11))
        ay += 85

    # Pointer Arrows
    draw_pointer_callout(draw, (750, 115), (450, 115), "1", "బటన్ నొక్కండి", "Tap Find Best Crop", color="#dc2626")
    draw_pointer_callout(draw, (435, 565), (435, 470), "2", "ఎరువులు & నీటి వివరాలు", "View Plans", color="#16a34a")

    path = os.path.join(IMAGES_DIR, "step3_crop_recommendation_ui.png")
    img.save(path, quality=95)
    print(f"Generated: {path}")


# =============================================================================
# 4. STEP 4: SMART IRRIGATION ADVISOR UI
# =============================================================================
def make_step4_image():
    img = Image.new("RGB", (W, H), "#0f172a")
    draw = ImageDraw.Draw(img)

    draw_rounded_rect(draw, (20, 20, W-20, H-20), radius=16, fill="#ffffff", outline="#334155", width=2)
    draw_rounded_rect(draw, (20, 20, W-20, 75), radius=16, fill="#14532d")
    draw.rectangle((20, 55, W-20, 75), fill="#14532d")
    draw.text((40, 34), "Step 4: Smart Irrigation Advisor & Motor Pumping Timer", fill="#ffffff", font=get_font(18, bold=True))

    # Moisture Alert Verdict Banner (RED - URGENT)
    draw_rounded_rect(draw, (40, 90, W-40, 160), radius=12, fill="#fef2f2", outline="#ef4444", width=2)
    draw.text((60, 104), "LIVE AI WATER VERDICT: URGENT IRRIGATION NEEDED TODAY / ఈరోజే నీరు పెట్టండి!", fill="#dc2626", font=get_font(14, bold=True))
    draw.text((60, 130), "Soil Moisture is 22% (Below 30% Stress Threshold) • Evaporation Index: High • Avoid Midday Sun", fill="#991b1b", font=get_font(11.5))

    # Moisture Meter Visual Card
    draw_rounded_rect(draw, (40, 175, 480, 510), radius=14, fill="#f8fafc", outline="#cbd5e1", width=1)
    draw.text((60, 195), "Live Soil Moisture Meter / నేల తేమ", fill="#0f172a", font=get_font(14.5, bold=True))
    
    # Progress gauge bar
    draw_rounded_rect(draw, (60, 235, 460, 265), radius=8, fill="#e2e8f0")
    draw_rounded_rect(draw, (60, 235, 148, 265), radius=8, fill="#ef4444")
    draw.text((60, 275), "0% (Dry)", fill="#dc2626", font=get_font(11, bold=True))
    draw.text((130, 275), "22% (Live)", fill="#dc2626", font=get_font(11.5, bold=True))
    draw.text((220, 275), "40% (Warning)", fill="#d97706", font=get_font(11))
    draw.text((360, 275), "75% (Moist)", fill="#16a34a", font=get_font(11))

    draw.text((60, 325), "Voice Advice: 'రైతు సోదరులారా, నేలలో తేమ 22 శాతం మాత్రమే ఉంది. ఈరోజే నీరు పెట్టండి.'", fill="#334155", font=get_font(11))
    draw_rounded_rect(draw, (60, 430, 460, 475), radius=8, fill="#16a34a")
    draw.text((140, 442), "Play Voice Irrigation Advice", fill="#ffffff", font=get_font(13, bold=True))

    # Water Volume & Motor Run-Time Calculator
    draw_rounded_rect(draw, (510, 175, 960, 510), radius=14, fill="#f0f9ff", outline="#0284c7", width=1)
    draw.text((530, 195), "Farm Acreage & Motor Pump Run-Time", fill="#0369a1", font=get_font(14.5, bold=True))
    
    draw.text((530, 235), "• Farm Size: 1.0 Acre (ఎకరం)", fill="#0f172a", font=get_font(12.5, bold=True))
    draw.text((530, 265), "• Water Required: 15,000 Liters", fill="#0f172a", font=get_font(12.5, bold=True))
    draw.text((530, 295), "• Motor Pump: 5.0 HP Submersible (1,200 L/min)", fill="#0f172a", font=get_font(12.5, bold=True))
    
    draw_rounded_rect(draw, (530, 335, 940, 405), radius=10, fill="#ffffff", outline="#7dd3fc", width=2)
    draw.text((550, 350), "RUN MOTOR FOR: 3.5 HOURS", fill="#0284c7", font=get_font(17, bold=True))
    draw.text((550, 378), "Recommended Window: 6:00 AM - 9:30 AM (Cool Morning)", fill="#15803d", font=get_font(11.5, bold=True))

    draw_rounded_rect(draw, (530, 430, 940, 475), radius=8, fill="#0284c7")
    draw.text((640, 442), "Set Pumping Reminder", fill="#ffffff", font=get_font(13, bold=True))

    # Pointer Arrows
    draw_pointer_callout(draw, (260, 565), (260, 475), "1", "ఎరుపు రంగు చూసి నీరు పెట్టండి", "Red = Water Today", color="#dc2626")
    draw_pointer_callout(draw, (735, 565), (735, 475), "2", "మోటార్ సమయం పాటించండి", "Set 3.5 hrs Timer", color="#0284c7")

    path = os.path.join(IMAGES_DIR, "step4_irrigation_advisor_ui.png")
    img.save(path, quality=95)
    print(f"Generated: {path}")


# =============================================================================
# 5. STEP 5: FERTILIZER GUIDANCE & 4-STAGE DOSAGE UI
# =============================================================================
def make_step5_image():
    img = Image.new("RGB", (W, H), "#0f172a")
    draw = ImageDraw.Draw(img)

    draw_rounded_rect(draw, (20, 20, W-20, H-20), radius=16, fill="#ffffff", outline="#334155", width=2)
    draw_rounded_rect(draw, (20, 20, W-20, 75), radius=16, fill="#14532d")
    draw.rectangle((20, 55, W-20, 75), fill="#14532d")
    draw.text((40, 34), "Step 5: Precision Fertilizer Plan & 4-Stage Split Schedule", fill="#ffffff", font=get_font(18, bold=True))

    # Total Bags Summary Bar
    draw_rounded_rect(draw, (40, 90, W-40, 150), radius=12, fill="#f0fdf4", outline="#86efac", width=1)
    draw.text((60, 102), "Total Bags for 1 Acre Rice: Urea: 2.0 Bags (100 kg) • DAP: 1.0 Bag (50 kg) • Potash (MOP): 0.7 Bag (35 kg)", fill="#166534", font=get_font(12.5, bold=True))
    draw.text((60, 126), "Pro-Tip: Split Urea into 3 doses across crop stages to prevent 50% nitrogen loss and leaf burn.", fill="#15803d", font=get_font(11))

    # 4-Stage Timeline Cards
    stages = [
        ("STAGE 1: BASAL", "At Sowing / Day 0", "Full DAP (50 kg) + MOP (35 kg) + 1/3 Urea", "Soil incorporate at sowing.", "#16a34a", "#f0fdf4", "#86efac"),
        ("STAGE 2: TILLERING", "20-25 Days (DAS)", "1st Top-Dressing: Urea (35 kg)", "Broadcast in moist soil.", "#0284c7", "#f0f9ff", "#7dd3fc"),
        ("STAGE 3: PANICLE", "45-50 Days (DAS)", "2nd Top-Dressing: Urea (35 kg) + 19:19:19", "Boosts panicle length.", "#7c3aed", "#faf5ff", "#d8b4fe"),
        ("STAGE 4: GRAIN FILL", "70-75 Days (DAS)", "Foliar Spray: 0:0:50 Potash (1.5 kg/acre)", "Fills heavy grains.", "#d97706", "#fffbeb", "#fde68a")
    ]
    sx = 40
    sw = 217
    for stitle, sday, sprod, sdesc, scol, sbg, sborder in stages:
        draw_rounded_rect(draw, (sx, 165, sx + sw, 480), radius=12, fill=sbg, outline=sborder, width=2)
        draw.text((sx + 10, 180), stitle, fill=scol, font=get_font(11.5, bold=True))
        draw.text((sx + 10, 205), sday, fill="#0f172a", font=get_font(11, bold=True))
        
        draw_rounded_rect(draw, (sx + 8, 235, sx + sw - 8, 335), radius=8, fill="#ffffff", outline=sborder, width=1)
        draw.text((sx + 12, 245), "Products to Apply:", fill="#475569", font=get_font(10, bold=True))
        draw.text((sx + 12, 265), sprod[:28], fill="#0f172a", font=get_font(10.5, bold=True))
        if len(sprod) > 28:
            draw.text((sx + 12, 285), sprod[28:56], fill="#0f172a", font=get_font(10.5, bold=True))

        draw.text((sx + 10, 350), "Purpose / ఉద్దేశ్యం:", fill="#475569", font=get_font(10, bold=True))
        draw.text((sx + 10, 370), sdesc[:26], fill="#334155", font=get_font(10))
        
        draw_rounded_rect(draw, (sx + 10, 430, sx + sw - 10, 460), radius=6, fill=scol)
        draw.text((sx + 35, 439), "Follow Stage", fill="#ffffff", font=get_font(11, bold=True))

        sx += sw + 18

    # Pointer Arrows
    draw_pointer_callout(draw, (150, 565), (150, 460), "1", "విత్తే సమయం (Day 0)", "Stage 1 Basal", color="#16a34a")
    draw_pointer_callout(draw, (840, 565), (840, 460), "2", "గింజ బలం దశ (Day 75)", "Stage 4 Grain", color="#d97706")

    path = os.path.join(IMAGES_DIR, "step5_fertilizer_advisor_ui.png")
    img.save(path, quality=95)
    print(f"Generated: {path}")


# =============================================================================
# 6. STEP 6: PLANT LEAF DISEASE DOCTOR UI
# =============================================================================
def make_step6_image():
    img = Image.new("RGB", (W, H), "#0f172a")
    draw = ImageDraw.Draw(img)

    draw_rounded_rect(draw, (20, 20, W-20, H-20), radius=16, fill="#ffffff", outline="#334155", width=2)
    draw_rounded_rect(draw, (20, 20, W-20, 75), radius=16, fill="#14532d")
    draw.rectangle((20, 55, W-20, 75), fill="#14532d")
    draw.text((40, 34), "Step 6: Plant Leaf Disease Doctor (Photo Diagnosis)", fill="#ffffff", font=get_font(18, bold=True))

    # Left: Leaf Photo Upload Box
    draw_rounded_rect(draw, (40, 90, 450, 505), radius=14, fill="#f8fafc", outline="#cbd5e1", width=1)
    draw.text((60, 108), "Snap / Upload Leaf Photo / ఆకు ఫోటో", fill="#0f172a", font=get_font(14.5, bold=True))
    draw.text((60, 132), "Take a clear close-up photo in bright daylight.", fill="#64748b", font=get_font(11.5))

    # Leaf Photo Frame
    draw_rounded_rect(draw, (60, 165, 430, 420), radius=12, fill="#e2e8f0", outline="#94a3b8", width=1)
    draw.text((150, 250), "[ LEAF PHOTO / ఆకు ఫోటో ]", fill="#475569", font=get_font(15, bold=True))
    draw.text((110, 280), "Visible Brown Lesions & Spots (అగ్గితెగులు)", fill="#dc2626", font=get_font(12, bold=True))

    draw_rounded_rect(draw, (60, 440, 430, 485), radius=8, fill="#16a34a")
    draw.text((160, 453), "Analyze Leaf Disease", fill="#ffffff", font=get_font(14, bold=True))

    # Right: AI Diagnosis Results Box
    draw_rounded_rect(draw, (480, 90, 960, 505), radius=14, fill="#fef2f2", outline="#ef4444", width=2)
    draw.text((505, 108), "AI DIAGNOSIS REPORT: RICE BLAST DETECTED", fill="#dc2626", font=get_font(14.5, bold=True))
    draw.text((505, 132), "Pathogen: Magnaporthe oryzae (Fungal Infection) • Severity: Moderate (25%)", fill="#991b1b", font=get_font(11.5))

    # Organic Cure Box
    draw_rounded_rect(draw, (505, 165, 935, 292), radius=10, fill="#f0fdf4", outline="#86efac", width=1)
    draw.text((520, 178), "Biological / Organic Home Remedy:", fill="#166534", font=get_font(12.5, bold=True))
    draw.text((520, 202), "• Spray 5% Neem Seed Kernel Extract (NSKE) or Neem Oil @ 5ml/Liter.", fill="#15803d", font=get_font(11.5))
    draw.text((520, 226), "• Spray fermented sour buttermilk (1 Litre in 10 Litres water).", fill="#15803d", font=get_font(11.5))
    draw.text((520, 250), "• Apply Trichoderma viride bio-fungicide @ 2.5 kg/acre.", fill="#15803d", font=get_font(11.5))

    # Chemical Cure Box
    draw_rounded_rect(draw, (505, 308, 935, 440), radius=10, fill="#ffffff", outline="#cbd5e1", width=1)
    draw.text((520, 322), "Chemical Fungicide Prescription:", fill="#0f172a", font=get_font(12.5, bold=True))
    draw.text((520, 346), "• Tricyclazole 75% WP @ 0.6g / Liter water (120g / acre).", fill="#334155", font=get_font(11.5))
    draw.text((520, 370), "• Alternate with Isoprothiolane 40% EC @ 1.5ml / Liter water.", fill="#334155", font=get_font(11.5))
    draw.text((520, 394), "• Spray in early morning or evening; repeat after 10 days.", fill="#334155", font=get_font(11.5))

    draw_rounded_rect(draw, (505, 452, 935, 488), radius=6, fill="#0284c7")
    draw.text((640, 462), "Listen to Doctor Spoken Audio", fill="#ffffff", font=get_font(12, bold=True))

    # Pointer Arrows
    draw_pointer_callout(draw, (245, 565), (245, 485), "1", "ఫోటో తీసి పరిశీలించండి", "Upload Photo", color="#16a34a")
    draw_pointer_callout(draw, (720, 565), (720, 488), "2", "మందుల మోతాదు పాటించండి", "Follow Dosage", color="#dc2626")

    path = os.path.join(IMAGES_DIR, "step6_disease_doctor_ui.png")
    img.save(path, quality=95)
    print(f"Generated: {path}")


# =============================================================================
# 7. STEP 7: VOICE ASSISTANT & EMERGENCY TOLL-FREE CALL UI
# =============================================================================
def make_step7_image():
    img = Image.new("RGB", (W, H), "#0f172a")
    draw = ImageDraw.Draw(img)

    draw_rounded_rect(draw, (20, 20, W-20, H-20), radius=16, fill="#ffffff", outline="#334155", width=2)
    draw_rounded_rect(draw, (20, 20, W-20, 75), radius=16, fill="#14532d")
    draw.rectangle((20, 55, W-20, 75), fill="#14532d")
    draw.text((40, 34), "Step 7: Multilingual AI Voice Assistant & Toll-Free Helpline", fill="#ffffff", font=get_font(18, bold=True))

    # Left: Voice Conversation Box
    draw_rounded_rect(draw, (40, 90, 560, 505), radius=14, fill="#f8fafc", outline="#cbd5e1", width=1)
    draw.text((60, 108), "Live Spoken Conversation in Mother Tongue / వాయిస్", fill="#0f172a", font=get_font(13.5, bold=True))

    # Farmer Speech Bubble
    draw_rounded_rect(draw, (120, 150, 530, 210), radius=12, fill="#dcfce7", outline="#86efac", width=1)
    draw.text((135, 165), "Farmer: 'వరిలో అగ్గితెగులు వస్తే ఏ మందు కొట్టాలి?'", fill="#166534", font=get_font(11.5, bold=True))
    draw.text((135, 185), "(What medicine should I spray for Rice Blast disease?)", fill="#15803d", font=get_font(10.5))

    # AI Spoken Bubble
    draw_rounded_rect(draw, (60, 230, 480, 320), radius=12, fill="#ffffff", outline="#cbd5e1", width=1)
    draw.text((75, 245), "AgriSense AI (Voice):", fill="#0284c7", font=get_font(11.5, bold=True))
    draw.text((75, 265), "'రైతు సోదరా, లీటరు నీటికి 0.6 గ్రాముల ట్రైసైక్లాజోల్ కలిపి", fill="#0f172a", font=get_font(11.5, bold=True))
    draw.text((75, 285), "ఉదయం వేళ పిచికారీ చేయండి. వేప నూనె కూడా కలపవచ్చు.'", fill="#0f172a", font=get_font(11.5, bold=True))

    # Big Green Microphone Button
    draw_rounded_rect(draw, (60, 360, 530, 475), radius=14, fill="#16a34a", outline="#15803d", width=2)
    draw.text((120, 398), "TAP TO SPEAK / మాట్లాడండి (Telugu/Hindi/English)", fill="#ffffff", font=get_font(13, bold=True))
    draw.text((170, 424), "Zero typing required • Natural spoken answers", fill="#dcfce7", font=get_font(10.5))

    # Right: Emergency Toll-Free Govt Kisan Helpline
    draw_rounded_rect(draw, (590, 90, 960, 505), radius=14, fill="#f0f9ff", outline="#0284c7", width=2)
    draw.text((615, 108), "Emergency Govt Support & Live Call", fill="#0369a1", font=get_font(14.5, bold=True))

    draw_rounded_rect(draw, (615, 150, 935, 275), radius=12, fill="#0284c7")
    draw.text((660, 175), "CALL 1551", fill="#ffffff", font=get_font(24, bold=True))
    draw.text((640, 212), "Kisan Call Center (Toll-Free Helpline)", fill="#e0f2fe", font=get_font(12.5, bold=True))
    draw.text((645, 236), "Free 24/7 Expert Agricultural Support", fill="#bae6fd", font=get_font(10.5))

    draw_rounded_rect(draw, (615, 300, 935, 475), radius=12, fill="#ffffff", outline="#cbd5e1", width=1)
    draw.text((635, 320), "Gemini Live Audio Call Mode", fill="#7c3aed", font=get_font(13.5, bold=True))
    draw.text((635, 350), "• Real-time duplex voice streaming WebSocket", fill="#334155", font=get_font(11))
    draw.text((635, 375), "• Direct phone-like conversation with AI", fill="#334155", font=get_font(11))
    draw_rounded_rect(draw, (635, 415, 915, 455), radius=8, fill="#7c3aed")
    draw.text((700, 428), "Launch Live Call Mode", fill="#ffffff", font=get_font(11.5, bold=True))

    # Pointer Arrows
    draw_pointer_callout(draw, (295, 565), (295, 475), "1", "మైక్ నొక్కి మాట్లాడండి", "Tap to Speak", color="#16a34a")
    draw_pointer_callout(draw, (775, 565), (775, 455), "2", "ఉచిత కాల్ చేయండి", "Call 1551 Helpline", color="#0284c7")

    path = os.path.join(IMAGES_DIR, "step7_voice_ai_ui.png")
    img.save(path, quality=95)
    print(f"Generated: {path}")


def main():
    print("Generating 7 Step-by-Step App UI Mockup Images with Indic Font and Pointer Arrows...")
    make_step1_image()
    make_step2_image()
    make_step3_image()
    make_step4_image()
    make_step5_image()
    make_step6_image()
    make_step7_image()
    print("All 7 UI mockups successfully regenerated in images/ directory!")


if __name__ == "__main__":
    main()
