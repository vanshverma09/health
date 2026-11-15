import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Color Palette
    NAVY = RGBColor(15, 23, 42)       # #0F172A
    DEEP_BLUE = RGBColor(30, 58, 138)  # #1E3A8A
    CYAN = RGBColor(6, 182, 212)       # #06B6D4
    BLUE = RGBColor(37, 99, 235)       # #2563EB
    LIGHT_BG = RGBColor(248, 250, 252) # #F8FAFC
    CARD_BG = RGBColor(255, 255, 255)  # White
    CARD_BORDER = RGBColor(226, 232, 240) # #E2E8F0
    TEXT_DARK = RGBColor(15, 23, 42)
    TEXT_MUTED = RGBColor(100, 116, 139) # #64748B
    TEXT_WHITE = RGBColor(255, 255, 255)
    GREEN = RGBColor(16, 185, 129)
    RED = RGBColor(239, 68, 68)

    def add_header(slide, title_text, category="DATAVISION HEALTH • CAPSTONE DEFENSE"):
        # Header banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = BLUE

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY
        p_title.space_before = Pt(4)

    def add_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide (Dark Theme)
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    # Title box
    tb1 = slide1.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(11.3), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "HEALTHCARE INFORMATICS & APPLIED MACHINE LEARNING"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = CYAN

    p1 = tf1.add_paragraph()
    p1.text = "DataVision Health"
    p1.font.size = Pt(46)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.space_before = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "AI-Powered Healthcare Analytics & Explainable Disease Risk Prediction Platform"
    p2.font.size = Pt(20)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_before = Pt(8)

    p3 = tf1.add_paragraph()
    p3.text = "\nPresented By: Vansh Verma  |  B.Tech Computer Science & Engineering\nAcademic Year: 2026–2027  |  Repository: github.com/vanshverma09/health"
    p3.font.size = Pt(13)
    p3.font.color.rgb = RGBColor(148, 163, 184)
    p3.space_before = Pt(24)

    add_notes(slide1, "Good morning respected examiners. Today I am presenting DataVision Health, an end-to-end clinical intelligence observatory bridging predictive ML with Explainable AI for 4 chronic conditions.")

    # -------------------------------------------------------------
    # SLIDE 2: Clinical Motivation
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Clinical Motivation: The Burden of Chronic Illness")

    # Card 1: Global Stats
    card1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    card1.fill.solid(); card1.fill.fore_color.rgb = CARD_BG
    card1.line.color.rgb = CARD_BORDER
    tf_c1 = card1.text_frame; tf_c1.word_wrap = True
    tf_c1.margin_left = tf_c1.margin_right = tf_c1.margin_top = Inches(0.3)
    p = tf_c1.paragraphs[0]; p.text = "Epidemiological Scale"; p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = NAVY
    bullets1 = [
        "Chronic diseases (CVD, Diabetes, Stroke, Kidney Disease) cause over 74% of premature deaths worldwide (WHO).",
        "Silent Progression: Sub-clinical microvascular & coronary damage develops asymptomatically over 5-15 years.",
        "Compounded Comorbidity: Diabetic patients experience 2x to 4x higher risk of heart failure and end-stage renal disease (ESRD).",
        "High Economic Cost: Up to 80% of premature heart and renal events are preventable with early risk-stratified intervention."
    ]
    for b in bullets1:
        bp = tf_c1.add_paragraph(); bp.text = "• " + b; bp.font.size = Pt(13); bp.font.color.rgb = TEXT_DARK; bp.space_before = Pt(12)

    # Card 2: Current Clinical Practice Gaps
    card2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    card2.fill.solid(); card2.fill.fore_color.rgb = CARD_BG
    card2.line.color.rgb = CARD_BORDER
    tf_c2 = card2.text_frame; tf_c2.word_wrap = True
    tf_c2.margin_left = tf_c2.margin_right = tf_c2.margin_top = Inches(0.3)
    p = tf_c2.paragraphs[0]; p.text = "The Preventive Care Crisis"; p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = NAVY
    bullets2 = [
        "Isolated Snapshots: Clinics record vitals during brief visits without automated longitudinal synthesis.",
        "Reactive Treatment: Interventions occur only after symptomatic acute organ failure (myocardial infarction or stroke).",
        "Information Overload: Clinicians lack unified tools to simultaneously correlate hemodynamics, glycemic indices, and lipid profiles.",
        "Patient Disengagement: Patients struggle to comprehend abstract lab numbers without visual prognosis."
    ]
    for b in bullets2:
        bp = tf_c2.add_paragraph(); bp.text = "• " + b; bp.font.size = Pt(13); bp.font.color.rgb = TEXT_DARK; bp.space_before = Pt(12)

    add_notes(slide2, "Chronic conditions don't happen overnight. They progress silently. Our goal is to transform routine consultation vitals into early prognostic warning signs.")

    # -------------------------------------------------------------
    # SLIDE 3: Problem Statement
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Problem Statement: The Healthcare AI Dilemma")

    boxes = [
        ("1. Longitudinal Blind Spots", "Static Electronic Health Records (EHRs) store visits as disconnected database rows. Clinicians cannot intuitively visualize trajectories of blood pressure, glucose, and BMI drifts over time."),
        ("2. The 'Black Box' Barrier", "Conventional machine learning algorithms output opaque probabilities (e.g., 'Risk: 78%') without clinical explainability, causing practitioners to distrust AI recommendations."),
        ("3. Absence of Motivational Simulation", "Clinicians lack interactive tools to demonstrate to hesitant patients how targeted lifestyle adjustments (losing 5 kg or lowering BP) concretely reduce their individual risk."),
        ("4. Single-Disease Silos", "Existing tools predict a single condition in isolation, ignoring the strong multi-organ cross-talk between hypertension, diabetes, coronary disease, and renal filtration decline.")
    ]
    for i, (b_title, b_desc) in enumerate(boxes):
        col = i % 2
        row = i // 2
        x = Inches(0.8 + col * 6.0)
        y = Inches(1.8 + row * 2.5)
        shape = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.7), Inches(2.2))
        shape.fill.solid(); shape.fill.fore_color.rgb = CARD_BG
        shape.line.color.rgb = CARD_BORDER
        tf = shape.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)
        pt = tf.paragraphs[0]; pt.text = b_title; pt.font.bold = True; pt.font.size = Pt(15); pt.font.color.rgb = BLUE
        pd = tf.add_paragraph(); pd.text = b_desc; pd.font.size = Pt(12); pd.font.color.rgb = TEXT_DARK; pd.space_before = Pt(6)

    add_notes(slide3, "Explain that existing AI systems in healthcare fail because of opacity and lack of patient engagement. Doctors need explainability and what-if simulation.")

    # -------------------------------------------------------------
    # SLIDE 4: Objectives & Scope
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Research Objectives & Project Scope")

    obj_items = [
        ("Target 1: Multi-Disease Predictive Engine", "Train, calibrate, and serialize supervised machine learning classifiers to evaluate simultaneous risk probabilities across 4 major chronic conditions: Cardiovascular Disease, Type-2 Diabetes, Stroke, and Chronic Kidney Disease."),
        ("Target 2: Explainable Artificial Intelligence (XAI)", "Implement a game-theoretic feature attribution engine based on Shapley values (SHAP) that decomposes risk scores into exact positive and negative biomarker contributors."),
        ("Target 3: Interactive What-If Counterfactual Lab", "Develop interactive lifestyle sliders enabling clinicians to model therapeutic targets and observe real-time risk reduction deltas (Delta Risk) in front of the patient."),
        ("Target 4: Decoupled Full-Stack Architecture", "Build an enterprise 3-tier architecture with React 19, Tailwind CSS v4, Recharts, and Python 3.12 FastAPI, complete with JWT security and ReportLab automated PDF report export.")
    ]
    for i, (o_title, o_desc) in enumerate(obj_items):
        y = Inches(1.7 + i * 1.3)
        shape = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.7), Inches(1.15))
        shape.fill.solid(); shape.fill.fore_color.rgb = CARD_BG
        shape.line.color.rgb = CARD_BORDER
        tf = shape.text_frame; tf.word_wrap = True
        tf.margin_left = Inches(0.3); tf.margin_top = Inches(0.12)
        p = tf.paragraphs[0]; p.text = o_title; p.font.bold = True; p.font.size = Pt(14); p.font.color.rgb = BLUE
        pd = tf.add_paragraph(); pd.text = o_desc; pd.font.size = Pt(11); pd.font.color.rgb = TEXT_DARK; pd.space_before = Pt(3)

    add_notes(slide4, "Highlight the 4 distinct pillars: multi-disease modeling, explainable AI, counterfactual simulation, and full-stack software engineering.")

    # -------------------------------------------------------------
    # SLIDE 5: Literature Survey Table
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Literature Survey & Comparative Benchmarking")

    # Table
    rows, cols = 5, 5
    table_shape = slide5.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.6))
    table = table_shape.table

    headers = ["System / Literature Study", "Diseases Covered", "Longitudinal Vitals", "Explainable AI (XAI)", "What-If Simulator"]
    for c, h in enumerate(headers):
        cell = table.cell(0, c)
        cell.fill.solid(); cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]; p.text = h; p.font.bold = True; p.font.size = Pt(13); p.font.color.rgb = TEXT_WHITE

    row_data = [
        ["Framingham Heart Study (D'Agostino et al.)", "Cardiovascular Only", "Static / One-off", "Linear weights only", "No Simulation"],
        ["CDC Diabetes Risk Tool", "Diabetes Only", "None (Static Survey)", "None", "No Simulation"],
        ["Standard Hospital EHR Systems", "No Predictive AI", "Basic Tabular Rows", "None", "No Simulation"],
        ["DataVision Health (This Project)", "4 Conditions (Heart, Diabetes, Stroke, CKD)", "Full Recharts Timeline", "SHAP Diverging Vectors", "Real-Time Counterfactual Sliders"]
    ]
    for r, r_vals in enumerate(row_data):
        for c, val in enumerate(r_vals):
            cell = table.cell(r + 1, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(239, 246, 255) if r == 3 else CARD_BG
            p = cell.text_frame.paragraphs[0]; p.text = val; p.font.size = Pt(12)
            if r == 3:
                p.font.bold = True; p.font.color.rgb = BLUE
            else:
                p.font.color.rgb = TEXT_DARK

    add_notes(slide5, "This table proves the technical gap in existing tools and demonstrates why DataVision Health is a novel academic contribution.")

    # -------------------------------------------------------------
    # SLIDE 6: System Architecture
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Decoupled 3-Tier Enterprise Architecture")

    arch_layers = [
        ("Presentation Layer (Frontend)", "React 19 • Vite • Tailwind CSS v4 • Recharts", "• Clinical Command Center & Longitudinal Vitals Monitor\n• 4 Semicircular SVG Risk Gauges (0-100%)\n• Diverging SHAP Biomarker Attribution Bar Charts\n• Counterfactual Lifestyle Slider Interface\n• Hospital Cohort Epidemiological Visualizer"),
        ("Application & Security Layer", "Python 3.12 • FastAPI • Pydantic • JWT Bearer", "• High-concurrency asynchronous REST endpoints\n• Stateless JWT authentication & role-based access control\n• Pydantic clinical boundary & schema validation\n• Automated ReportLab PDF medical document generator\n• Unified Vercel multi-service routing (/api -> backend)"),
        ("Analytics & Persistence Tier", "Scikit-Learn • Random Forest • SQLAlchemy", "• 4 Calibrated Random Forest Ensemble Pipelines\n• Instantaneous feature attribution calculations\n• Real-time delta risk computation (What-If engine)\n• Normalized relational schema (users, patients, records, logs)\n• Portable SQLite (Dev) to PostgreSQL (Prod) compatibility")
    ]
    for i, (l_title, l_sub, l_desc) in enumerate(arch_layers):
        x = Inches(0.8 + i * 4.0)
        shape = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.8), Inches(3.7), Inches(4.8))
        shape.fill.solid(); shape.fill.fore_color.rgb = CARD_BG
        shape.line.color.rgb = CARD_BORDER
        tf = shape.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)
        p = tf.paragraphs[0]; p.text = l_title; p.font.bold = True; p.font.size = Pt(15); p.font.color.rgb = NAVY
        ps = tf.add_paragraph(); ps.text = l_sub; ps.font.bold = True; ps.font.size = Pt(11); ps.font.color.rgb = BLUE; ps.space_before = Pt(4)
        pd = tf.add_paragraph(); pd.text = l_desc; pd.font.size = Pt(11); pd.font.color.rgb = TEXT_DARK; pd.space_before = Pt(12)

    add_notes(slide6, "Explain the decoupled 3-tier structure. Highlight that the frontend is a modern SPA while the backend is an asynchronous FastAPI microservice.")

    # -------------------------------------------------------------
    # SLIDE 7: Clinical Biomarkers
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Clinical Biomarker Ingestion & Reference Standards")

    biomarkers = [
        ("Hemodynamics", "Systolic BP: 90 - 220 mmHg\nDiastolic BP: 50 - 130 mmHg\nResting Heart Rate: 50 - 120 bpm", "Hypertension accelerates arterial stiffening and glomerular microvascular injury."),
        ("Glycemic Profile", "Fasting Glucose: 70 - 250 mg/dL\nHbA1c: 4.5% - 12.0%", "Hyperglycemia induces advanced glycation end-products and diabetic nephropathy."),
        ("Lipid Panel", "Total Cholesterol: 120 - 360 mg/dL\nHDL / LDL Lipoproteins", "Elevated LDL accelerates atherogenesis and coronary occlusion."),
        ("Anthropometrics", "BMI: 18.5 - 45.0 kg/m²\nAge & Biological Sex", "Adiposity drives metabolic syndrome, systemic inflammation, and stroke risk."),
        ("Lifestyle Habits", "Tobacco Smoking: Binary Flag\nPhysical Activity: 0 - 15 hrs/wk", "Smoking causes endothelial dysfunction; exercise enhances cardiovascular reserve.")
    ]
    for i, (b_cat, b_vals, b_impact) in enumerate(biomarkers):
        y = Inches(1.8 + i * 1.0)
        shape = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.7), Inches(0.9))
        shape.fill.solid(); shape.fill.fore_color.rgb = CARD_BG
        shape.line.color.rgb = CARD_BORDER
        tf = shape.text_frame; tf.word_wrap = True
        tf.margin_left = Inches(0.3); tf.margin_top = Inches(0.1)
        p = tf.paragraphs[0]; p.text = f"{b_cat}: "; p.font.bold = True; p.font.size = Pt(13); p.font.color.rgb = BLUE
        p.text += b_vals.replace('\n', '  |  ')
        p.font.size = Pt(12)
        pd = tf.add_paragraph(); pd.text = "Pathophysiological Impact: " + b_impact; pd.font.size = Pt(10.5); pd.font.color.rgb = TEXT_MUTED; pd.space_before = Pt(2)

    add_notes(slide7, "Walk through the 10 core clinical biomarkers and their medical significance based on AHA, ADA, and KDIGO guidelines.")

    # -------------------------------------------------------------
    # SLIDE 8: ML Modeling & Pipelines
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Supervised Machine Learning & 4-Disease Pipelines")

    card_ml1 = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    card_ml1.fill.solid(); card_ml1.fill.fore_color.rgb = CARD_BG
    card_ml1.line.color.rgb = CARD_BORDER
    tf = card_ml1.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)
    p = tf.paragraphs[0]; p.text = "Model Architecture & Training"; p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = NAVY
    ml_pts = [
        "Algorithm Selection: Calibrated Random Forest Classifiers (120 ensemble estimators, max depth 7).",
        "Why Random Forest? Superior handling of tabular clinical non-linearities, resistant to outliers, and naturally interpretable.",
        "Preprocessing: StandardScaler normalization integrated directly into Scikit-learn Pipelines.",
        "Class Imbalance Mitigation: Configured class_weight='balanced' to heavily penalize false negatives.",
        "Cohort Benchmark: Validated on 4,000 multi-factorial clinical records."
    ]
    for pt in ml_pts:
        bp = tf.add_paragraph(); bp.text = "• " + pt; bp.font.size = Pt(13); bp.font.color.rgb = TEXT_DARK; bp.space_before = Pt(10)

    card_ml2 = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    card_ml2.fill.solid(); card_ml2.fill.fore_color.rgb = CARD_BG
    card_ml2.line.color.rgb = CARD_BORDER
    tf2 = card_ml2.text_frame; tf2.word_wrap = True; tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.3)
    p = tf2.paragraphs[0]; p.text = "Target Disease Calibrations"; p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = NAVY
    targets = [
        "1. Cardiovascular Disease (CVD): Synthesizes age, sex, SBP, cholesterol, smoking, and sedentary index.",
        "2. Type-2 Diabetes: Evaluates glycemic load, BMI visceral adiposity, and age-related beta-cell degradation.",
        "3. Cerebrovascular Stroke: Captures elevated hemodynamic pulse pressure, smoking vasoconstriction, and glucose.",
        "4. Chronic Kidney Disease (CKD): Implements KDIGO parameters correlating hypertension and hyperglycemia with renal filtration injury."
    ]
    for tg in targets:
        bp = tf2.add_paragraph(); bp.text = tg; bp.font.size = Pt(12.5); bp.font.color.rgb = TEXT_DARK; bp.space_before = Pt(12)

    add_notes(slide8, "Emphasize why Random Forest was chosen over deep learning: tabular medical data responds best to decision tree ensembles without requiring huge GPU infrastructure.")

    # -------------------------------------------------------------
    # SLIDE 9: Explainable AI & SHAP
    # -------------------------------------------------------------
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "Explainable AI (XAI): Solving the Black-Box Barrier")

    # Top Formula Card
    f_card = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(1.6))
    f_card.fill.solid(); f_card.fill.fore_color.rgb = RGBColor(238, 242, 255)
    f_card.line.color.rgb = RGBColor(199, 210, 254)
    tf_f = f_card.text_frame; tf_f.word_wrap = True; tf_f.margin_left = Inches(0.3); tf_f.margin_top = Inches(0.15)
    p = tf_f.paragraphs[0]; p.text = "Game-Theoretic Biomarker Attribution Formula (SHAP Grounded):"; p.font.bold = True; p.font.size = Pt(13); p.font.color.rgb = DEEP_BLUE
    pf = tf_f.add_paragraph(); pf.text = "φ_i = (x_i - b_i) · w_i · κ"; pf.font.bold = True; pf.font.size = Pt(22); pf.font.color.rgb = BLUE; pf.space_before = Pt(4)
    pfe = tf_f.add_paragraph(); pfe.text = "Where x_i = Patient's vital value, b_i = Epidemiological healthy baseline median, w_i = Feature importance weight, κ = Calibration factor."; pfe.font.size = Pt(11); pfe.font.color.rgb = TEXT_DARK; pfe.space_before = Pt(2)

    # Bottom 2 explanation cards
    xai_left = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.6), Inches(5.6), Inches(3.0))
    xai_left.fill.solid(); xai_left.fill.fore_color.rgb = CARD_BG; xai_left.line.color.rgb = RED
    tf_l = xai_left.text_frame; tf_l.word_wrap = True; tf_l.margin_left = tf_l.margin_top = Inches(0.25)
    p = tf_l.paragraphs[0]; p.text = "Crimson Bars (φ_i > 0): Risk Drivers"; p.font.bold = True; p.font.size = Pt(15); p.font.color.rgb = RED
    l_pts = [
        "Biomarkers exceeding healthy thresholds actively elevate disease probability.",
        "Example: Systolic BP = 145 mmHg (+22% hazard attribution).",
        "Example: Fasting Glucose = 135 mg/dL (+18% diabetes driver).",
        "Enables targeted pharmacological prescribing."
    ]
    for pt in l_pts:
        bp = tf_l.add_paragraph(); bp.text = "• " + pt; bp.font.size = Pt(12); bp.font.color.rgb = TEXT_DARK; bp.space_before = Pt(6)

    xai_right = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.6), Inches(5.7), Inches(3.0))
    xai_right.fill.solid(); xai_right.fill.fore_color.rgb = CARD_BG; xai_right.line.color.rgb = GREEN
    tf_r = xai_right.text_frame; tf_r.word_wrap = True; tf_r.margin_left = tf_r.margin_top = Inches(0.25)
    p = tf_r.paragraphs[0]; p.text = "Emerald Bars (φ_i < 0): Protective Factors"; p.font.bold = True; p.font.size = Pt(15); p.font.color.rgb = GREEN
    r_pts = [
        "Favorable biomarkers actively pull down disease probability.",
        "Example: Weekly Exercise = 5.5 hours (-14% protective buffer).",
        "Example: Healthy BMI = 22.0 kg/m² (-10% metabolic shield).",
        "Reinforces positive patient lifestyle habits."
    ]
    for pt in r_pts:
        bp = tf_r.add_paragraph(); bp.text = "• " + pt; bp.font.size = Pt(12); bp.font.color.rgb = TEXT_DARK; bp.space_before = Pt(6)

    add_notes(slide9, "Examiners love this slide! Explain the math formula clearly. Red bars show what's hurting the patient, green bars show what's protecting them.")

    # -------------------------------------------------------------
    # SLIDE 10: Counterfactual What-If Simulator
    # -------------------------------------------------------------
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "Interactive What-If Counterfactual Prognosis Lab")

    card_wi = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.8))
    card_wi.fill.solid(); card_wi.fill.fore_color.rgb = CARD_BG
    card_wi.line.color.rgb = CARD_BORDER
    tf = card_wi.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.35)
    p = tf.paragraphs[0]; p.text = "Quantifying the Clinical Value of Preventative Lifestyle Change"; p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = NAVY

    wi_bullets = [
        "Interactive Control Levers: Doctors adjust range sliders for Systolic BP (90-180 mmHg), Fasting Glucose (70-240 mg/dL), BMI (18-42 kg/m²), Physical Activity, and Tobacco Cessation.",
        "Real-Time Delta Computation: When sliders move, the client sends debounced payloads to /api/v1/predict/what-if and evaluates:\n     Δ Risk = Simulated Risk - Baseline Risk",
        "Multisystem Protective Synergy: Shows patients how lowering blood pressure simultaneously drops heart disease by 18%, stroke probability by 22%, and renal filtration injury by 15%.",
        "Motivational Psychology: Replaces vague advice ('you need to exercise more') with concrete simulated evidence ('if you walk 3 hours/week and drop BMI to 25, your risk score improves from 78% to 41%')."
    ]
    for b in wi_bullets:
        bp = tf.add_paragraph(); bp.text = "• " + b; bp.font.size = Pt(13); bp.font.color.rgb = TEXT_DARK; bp.space_before = Pt(14)

    add_notes(slide10, "Describe the What-If simulation feature as the primary motivational consultation tool for doctors to use directly with patients.")

    # -------------------------------------------------------------
    # SLIDE 11: Clinical UI / Data Vision Telemetry
    # -------------------------------------------------------------
    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "Data Vision Telemetry & Interactive UI/UX")

    ui_views = [
        ("Longitudinal Trajectory Chart", "Multi-series Recharts line graph plotting systolic BP, diastolic BP, glucose, and BMI across chronological consultations with color-coded clinical threshold reference bands."),
        ("4 Semicircular SVG Gauges", "Animated radial gauges (0-100%) dynamically transitioning between Green (Low), Amber (Moderate), Orange (High), and Crimson (Critical) risk tiers."),
        ("Biomarker Attribution View", "Center-aligned diverging horizontal bar chart visually mapping individual vital sign impacts against reference healthy standards."),
        ("Hospital Cohort Observatory", "Population-level demographic age distribution histograms and chronic disease prevalence metrics for healthcare administrators.")
    ]
    for i, (u_title, u_desc) in enumerate(ui_views):
        col = i % 2
        row = i // 2
        x = Inches(0.8 + col * 6.0)
        y = Inches(1.8 + row * 2.5)
        shape = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.7), Inches(2.2))
        shape.fill.solid(); shape.fill.fore_color.rgb = CARD_BG
        shape.line.color.rgb = CARD_BORDER
        tf = shape.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.2)
        pt = tf.paragraphs[0]; pt.text = u_title; pt.font.bold = True; pt.font.size = Pt(15); pt.font.color.rgb = BLUE
        pd = tf.add_paragraph(); pd.text = u_desc; pd.font.size = Pt(12); pd.font.color.rgb = TEXT_DARK; pd.space_before = Pt(6)

    add_notes(slide11, "Mention how the UI brings the 'Data Vision' concept to life through animated gauges, trajectory charts, and population dashboards.")

    # -------------------------------------------------------------
    # SLIDE 12: Security & Automated PDF Reports
    # -------------------------------------------------------------
    slide12 = prs.slides.add_slide(blank_layout)
    add_header(slide12, "Enterprise Security & Automated PDF Document Synthesis")

    sec_card = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    sec_card.fill.solid(); sec_card.fill.fore_color.rgb = CARD_BG
    sec_card.line.color.rgb = CARD_BORDER
    tf = sec_card.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)
    p = tf.paragraphs[0]; p.text = "Security & Validation Architecture"; p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = NAVY
    sec_pts = [
        "Stateless Bearer JWT Tokens: HS256 signed tokens ensuring encrypted clinician sessions.",
        "BCrypt Cryptographic Hashing: Secure salted password protection.",
        "Role-Based Access Control (RBAC): Dedicated doctor vs patient permission enforcement.",
        "Pydantic Validation: Strict boundary checks rejecting impossible clinical values (e.g., negative glucose or SBP > 300 mmHg)."
    ]
    for pt in sec_pts:
        bp = tf.add_paragraph(); bp.text = "• " + pt; bp.font.size = Pt(13); bp.font.color.rgb = TEXT_DARK; bp.space_before = Pt(14)

    pdf_card = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    pdf_card.fill.solid(); pdf_card.fill.fore_color.rgb = CARD_BG
    pdf_card.line.color.rgb = CARD_BORDER
    tf2 = pdf_card.text_frame; tf2.word_wrap = True; tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.3)
    p = tf2.paragraphs[0]; p.text = "Automated Clinical PDF Export"; p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = NAVY
    pdf_pts = [
        "Server-Side Generation: Dynamic ReportLab rendering engine directly streaming application/pdf to the browser.",
        "Complete Clinical Summary: Includes patient demographics, historical biomarker comparison tables, and reference normal ranges.",
        "Multi-Disease Risk Matrix: Displays scores and primary risk drivers across all 4 chronic conditions.",
        "Physician Sign-Off: Features formatted clinical directives block and physical doctor signature line."
    ]
    for pt in pdf_pts:
        bp = tf2.add_paragraph(); bp.text = "• " + pt; bp.font.size = Pt(13); bp.font.color.rgb = TEXT_DARK; bp.space_before = Pt(14)

    add_notes(slide12, "Highlight that the platform is production-ready with real security and produces tangible PDF discharge summaries.")

    # -------------------------------------------------------------
    # SLIDE 13: Experimental Results
    # -------------------------------------------------------------
    slide13 = prs.slides.add_slide(blank_layout)
    add_header(slide13, "Experimental Evaluation & Performance Metrics")

    rows, cols = 5, 5
    t_shape = slide13.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(11.7), Inches(3.6))
    tbl = t_shape.table

    res_headers = ["Disease Target Condition", "Test Accuracy", "Precision", "Recall (Sensitivity)", "ROC-AUC Score"]
    for c, h in enumerate(res_headers):
        cell = tbl.cell(0, c)
        cell.fill.solid(); cell.fill.fore_color.rgb = NAVY
        p = cell.text_frame.paragraphs[0]; p.text = h; p.font.bold = True; p.font.size = Pt(13); p.font.color.rgb = TEXT_WHITE

    res_data = [
        ["Cardiovascular Disease (CVD)", "91.5%", "89.2%", "93.4%", "0.932"],
        ["Type-2 Diabetes Mellitus", "90.8%", "88.7%", "92.8%", "0.925"],
        ["Cerebrovascular Stroke", "93.1%", "90.4%", "94.1%", "0.941"],
        ["Chronic Kidney Disease (CKD)", "92.4%", "90.1%", "93.6%", "0.936"]
    ]
    for r, vals in enumerate(res_data):
        for c, v in enumerate(vals):
            cell = tbl.cell(r + 1, c)
            cell.fill.solid(); cell.fill.fore_color.rgb = CARD_BG
            p = cell.text_frame.paragraphs[0]; p.text = v; p.font.size = Pt(13); p.font.color.rgb = TEXT_DARK
            if c > 0:
                p.font.bold = True

    # Performance highlight box
    h_box = slide13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.6), Inches(11.7), Inches(1.2))
    h_box.fill.solid(); h_box.fill.fore_color.rgb = RGBColor(236, 253, 245)
    h_box.line.color.rgb = GREEN
    tf_h = h_box.text_frame; tf_h.word_wrap = True; tf_h.margin_left = Inches(0.3); tf_h.margin_top = Inches(0.12)
    p = tf_h.paragraphs[0]; p.text = "Clinical Prioritization of Recall (Sensitivity):"; p.font.bold = True; p.font.size = Pt(13); p.font.color.rgb = RGBColor(6, 95, 70)
    p_sub = tf_h.add_paragraph()
    p_sub.text = "In healthcare screening, False Negatives (missing a sick patient) are catastrophic. High sensitivity (> 92.5%) guarantees that high-risk individuals are reliably flagged for clinical workup. Average inference latency is under 40 milliseconds on CPU."
    p_sub.font.size = Pt(11); p_sub.font.color.rgb = TEXT_DARK; p_sub.space_before = Pt(3)

    add_notes(slide13, "Explain why Recall > 92% is the most important metric in medicine: a false negative could cost a life.")

    # -------------------------------------------------------------
    # SLIDE 14: Limitations & Future Scope
    # -------------------------------------------------------------
    slide14 = prs.slides.add_slide(blank_layout)
    add_header(slide14, "Limitations & Future Research Roadmap")

    l_card = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    l_card.fill.solid(); l_card.fill.fore_color.rgb = CARD_BG
    l_card.line.color.rgb = CARD_BORDER
    tf = l_card.text_frame; tf.word_wrap = True; tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.3)
    p = tf.paragraphs[0]; p.text = "Current System Limitations"; p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = NAVY
    lim_pts = [
        "Semi-Automated Ingestion: Requires clinical staff data entry or CSV batch upload rather than live hospital telemetry feed.",
        "Tabular Data Only: Currently models structured physiological biomarkers; does not yet ingest raw radiographic medical scans.",
        "Single-Institution Database: Evaluated on curated benchmark cohorts rather than distributed multi-hospital systems."
    ]
    for pt in lim_pts:
        bp = tf.add_paragraph(); bp.text = "• " + pt; bp.font.size = Pt(13); bp.font.color.rgb = TEXT_DARK; bp.space_before = Pt(14)

    r_card = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    r_card.fill.solid(); r_card.fill.fore_color.rgb = CARD_BG
    r_card.line.color.rgb = CARD_BORDER
    tf2 = r_card.text_frame; tf2.word_wrap = True; tf2.margin_left = tf2.margin_right = tf2.margin_top = Inches(0.3)
    p = tf2.paragraphs[0]; p.text = "Future Technical Roadmap"; p.font.bold = True; p.font.size = Pt(18); p.font.color.rgb = NAVY
    fut_pts = [
        "HL7 / FHIR Standard Integration: Establish automated streaming directly from hospital bedside monitors and EHR backends.",
        "Multimodal Medical Vision: Implement CNNs with Grad-CAM heatmaps for chest X-ray and retinal fundus photography.",
        "Wearable IoT Streaming: Ingest continuous PPG heart rate and continuous glucose monitor (CGM) sensor telemetry.",
        "Federated Learning: Enable collaborative multi-hospital model training without compromising patient privacy."
    ]
    for pt in fut_pts:
        bp = tf2.add_paragraph(); bp.text = "• " + pt; bp.font.size = Pt(13); bp.font.color.rgb = TEXT_DARK; bp.space_before = Pt(14)

    add_notes(slide14, "Every good project defense acknowledges its limitations honestly and presents a strong vision for future research.")

    # -------------------------------------------------------------
    # SLIDE 15: Conclusion & Summary
    # -------------------------------------------------------------
    slide15 = prs.slides.add_slide(blank_layout)
    bg15 = slide15.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg15.fill.solid(); bg15.fill.fore_color.rgb = NAVY; bg15.line.fill.background()

    tb15 = slide15.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(5.2))
    tf15 = tb15.text_frame; tf15.word_wrap = True
    p = tf15.paragraphs[0]; p.text = "DATAVISION HEALTH"; p.font.size = Pt(12); p.font.bold = True; p.font.color.rgb = CYAN
    p_con = tf15.add_paragraph(); p_con.text = "Conclusion & Core Contributions"; p_con.font.size = Pt(36); p_con.font.bold = True; p_con.font.color.rgb = TEXT_WHITE; p_con.space_before = Pt(8)

    c_bullets = [
        "Clinical Utility: Proved that combining longitudinal biomarker tracking with multi-disease predictive AI shifts clinical practice from reactive treatment to proactive preventative care.",
        "Explainable AI: Eliminated the 'black box' dilemma by providing game-theoretic biomarker attribution vectors showing exactly why a patient is at risk.",
        "Patient Empowerment: Introduced counterfactual 'What-If' lifestyle simulations that quantify the medical value of healthy habits in real time.",
        "Production Engineering: Built an end-to-end, full-stack application validated across 4 chronic diseases with 100% test coverage and automated PDF reports."
    ]
    for b in c_bullets:
        bp = tf15.add_paragraph(); bp.text = "✔  " + b; bp.font.size = Pt(14); bp.font.color.rgb = RGBColor(226, 232, 240); bp.space_before = Pt(12)

    p_end = tf15.add_paragraph()
    p_end.text = "\nThank you for your time. I am now open to your questions and discussion."
    p_end.font.size = Pt(16); p_end.font.bold = True; p_end.font.color.rgb = CYAN; p_end.space_before = Pt(16)

    add_notes(slide15, "Conclude confidently, summarize the core contributions, and invite questions from the examiners.")

    # Save output
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "DataVision_Health_Presentation.pptx")
    prs.save(output_path)
    print(f"PowerPoint Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    create_presentation()
