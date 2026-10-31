import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    # Theme Colors
    NAVY = RGBColor(15, 23, 42)       # Slate 900
    BLUE = RGBColor(37, 99, 235)      # Royal Blue 600
    LIGHT_BLUE = RGBColor(239, 246, 255) # Blue 50
    TEXT_DARK = RGBColor(30, 41, 59)  # Slate 800
    TEXT_MUTED = RGBColor(100, 116, 139) # Slate 500
    WHITE = RGBColor(255, 255, 255)
    EMERALD = RGBColor(16, 185, 129)
    CARD_BG = RGBColor(248, 250, 252) # Slate 50
    BORDER_COLOR = RGBColor(226, 232, 240) # Slate 200

    def add_header(slide, title_text, category_text="CAMPUSFIND • BCA COLLEGE PROJECT"):
        # Category pill
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = BLUE

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = NAVY

    # =========================================================================
    # SLIDE 1: Title Slide (Cover)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_slide_layout)

    # Top dark gradient banner
    bg_shape = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg_shape.fill.solid()
    bg_shape.fill.fore_color.rgb = NAVY
    bg_shape.line.fill.background()

    # Blue Accent bar
    accent_bar = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.15), Inches(3.2))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = BLUE
    accent_bar.line.fill.background()

    # Title & Subtitle box
    tbox = slide1.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(11.0), Inches(3.4))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "CAMPUSFIND"
    p0.font.size = Pt(44)
    p0.font.bold = True
    p0.font.color.rgb = WHITE

    p1 = tf1.add_paragraph()
    p1.text = "College Lost and Found Portal Web Application"
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(147, 197, 253) # Light Blue 300
    p1.space_before = Pt(8)

    p2 = tf1.add_paragraph()
    p2.text = "A secure, responsive full-stack platform for campus item recovery, ownership verification, and safe handovers."
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(203, 213, 225) # Slate 300
    p2.space_before = Pt(14)

    # 3 Metadata Badges in Bottom Container
    badge_data = [
        ("PROJECT TYPE", "BCA Final Year Project", Inches(1.2)),
        ("TECH STACK", "React 19 • Tailwind CSS • Flask • SQLite", Inches(4.8)),
        ("TARGET ENVIRONMENT", "College Campus & Security Gate", Inches(8.9)),
    ]
    for label, val, left in badge_data:
        box = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(4.8), Inches(3.5), Inches(1.5))
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(30, 41, 59)
        box.line.color.rgb = RGBColor(51, 65, 85)
        btf = box.text_frame
        btf.word_wrap = True
        bp0 = btf.paragraphs[0]
        bp0.text = label
        bp0.font.size = Pt(10)
        bp0.font.bold = True
        bp0.font.color.rgb = RGBColor(96, 165, 250)
        bp1 = btf.add_paragraph()
        bp1.text = val
        bp1.font.size = Pt(13)
        bp1.font.bold = True
        bp1.font.color.rgb = WHITE
        bp1.space_before = Pt(4)

    slide1.notes_slide.notes_text_frame.text = (
        "Good morning respected examiners and faculty members. Today, I am presenting 'CampusFind', "
        "a full-stack web application developed for our BCA final year project. CampusFind replaces paper notice boards "
        "and unorganized social media groups with an automated, secure digital portal that reunites college students "
        "and staff with their lost belongings through a structured anti-fraud verification workflow."
    )

    # =========================================================================
    # SLIDE 2: Problem Statement & Project Objectives
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide2, "Problem Statement & Project Objectives")

    # Left Card: Traditional Challenges
    card1 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    card1.fill.solid()
    card1.fill.fore_color.rgb = CARD_BG
    card1.line.color.rgb = BORDER_COLOR
    ctf1 = card1.text_frame
    ctf1.word_wrap = True

    cp0 = ctf1.paragraphs[0]
    cp0.text = "🚨 Traditional Campus Challenges"
    cp0.font.size = Pt(17)
    cp0.font.bold = True
    cp0.font.color.rgb = RGBColor(225, 29, 72) # Rose 600

    challenges = [
        ("Chaotic Communication", "Lost items posted in WhatsApp/Telegram groups get buried within hours."),
        ("Physical Notice Inefficiency", "Paper posters tear off notice boards and cannot be searched or updated."),
        ("High Fraud & Theft Risk", "Anyone can claim valuable electronics without proof of rightful ownership."),
        ("Privacy Vulnerability", "Students publicly write personal phone numbers on posters, inviting spam."),
        ("Zero Administrative Records", "Campus security desks have no central register to track item return rates.")
    ]
    for title, desc in challenges:
        p = ctf1.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = NAVY
        p.space_before = Pt(8)
        # Add normal text
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED

    # Right Card: Project Objectives
    card2 = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    card2.fill.solid()
    card2.fill.fore_color.rgb = LIGHT_BLUE
    card2.line.color.rgb = RGBColor(191, 219, 254)
    ctf2 = card2.text_frame
    ctf2.word_wrap = True

    cp2 = ctf2.paragraphs[0]
    cp2.text = "🎯 Core Objectives of CampusFind"
    cp2.font.size = Pt(17)
    cp2.font.bold = True
    cp2.font.color.rgb = BLUE

    objectives = [
        ("Centralized Campus Hub", "Single responsive portal to browse and report lost and found items."),
        ("Landmark-Specific Tagging", "Pinpoint exact spots (Central Library, MCA Lab 1, Cafeteria, Sports Turf)."),
        ("Anti-Fraud Verification", "Require undisclosed distinctive marks and proof photos before approval."),
        ("Secure In-Portal Messaging", "Private chat between finder and claimant without exposing phone numbers."),
        ("Role-Based Oversight", "Admin console for security staff with live statistics and JSON data export.")
    ]
    for title, desc in objectives:
        p = ctf2.add_paragraph()
        p.text = f"✔ {title}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = BLUE
        p.space_before = Pt(8)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_DARK

    slide2.notes_slide.notes_text_frame.text = (
        "In Slide 2, we contrast the existing manual problem with our project's core objectives. "
        "On college campuses, hundreds of students misplace calculators, ID cards, laptop chargers, and wallets daily. "
        "Traditional notice boards and messaging groups fail because they are not searchable, expose students' personal phone numbers, "
        "and allow opportunistic false claims. CampusFind solves this by introducing mandatory ownership verification, "
        "specific campus landmark mapping, and an administrative moderation panel."
    )

    # =========================================================================
    # SLIDE 3: System Architecture & Technology Stack
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide3, "System Architecture & Full-Stack Technologies")

    # 4 Architecture Columns
    layers = [
        ("1. FRONTEND LAYER", "React 19 + Tailwind CSS", BLUE, [
            "Single Page Application (SPA)",
            "Vite 8.3 build tool & dev server",
            "Tailwind CSS v4 modern utility design",
            "Lucide React vector iconography",
            "Fully mobile-responsive layout"
        ]),
        ("2. BACKEND LAYER", "Python Flask 3.1", NAVY, [
            "RESTful API architecture",
            "Werkzeug WSGI server integration",
            "Modular blueprint routing (/auth, /items, /claims, /admin)",
            "Reverse proxy setup via Vite",
            "Secure static file upload handling"
        ]),
        ("3. DATABASE LAYER", "SQLite 3 + SQLAlchemy", RGBColor(13, 148, 136), [ # Teal
            "Zero-configuration embedded engine",
            "SQLAlchemy ORM with relational mapping",
            "Relational models: Users, Items, Claims, Messages, Alerts",
            "Cascade deletes and database indexing",
            "Automated realistic college seed script"
        ]),
        ("4. SECURITY LAYER", "JWT + Werkzeug RBAC", RGBColor(124, 58, 237), [ # Purple
            "JSON Web Tokens (7-day validity)",
            "Salted SHA-256 PBKDF2 password hashing",
            "@token_required & @admin_required",
            "Anti-tampering token verification",
            "File extension & size sanitization"
        ])
    ]

    col_width = Inches(2.78)
    col_gap = Inches(0.25)
    for idx, (head, sub, col_color, bullets) in enumerate(layers):
        left_pos = Inches(0.8) + idx * (col_width + col_gap)
        box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_pos, Inches(1.8), col_width, Inches(5.0))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = BORDER_COLOR
        btf = box.text_frame
        btf.word_wrap = True

        p0 = btf.paragraphs[0]
        p0.text = head
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = col_color

        p1 = btf.add_paragraph()
        p1.text = sub
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = NAVY
        p1.space_before = Pt(4)

        for b in bullets:
            bp = btf.add_paragraph()
            bp.text = f"• {b}"
            bp.font.size = Pt(11)
            bp.font.color.rgb = TEXT_DARK
            bp.space_before = Pt(10)

    slide3.notes_slide.notes_text_frame.text = (
        "Slide 3 illustrates the full-stack architecture of CampusFind. The client layer is built with React 19 and Tailwind CSS, "
        "delivering a responsive SPA. The server layer runs Python Flask 3.1 with RESTful endpoints. For persistence, "
        "we utilized SQLite 3 paired with SQLAlchemy ORM, ensuring an ACID-compliant, self-contained relational database. "
        "Security is handled using PyJWT for tokenized sessions and PBKDF2 password hashing to prevent unauthorized access."
    )

    # =========================================================================
    # SLIDE 4: Key Features & Verification Workflow
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide4, "Core Features & 3-Step Verification Workflow")

    # Left Box: Key Portal Modules
    mod_box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    mod_box.fill.solid()
    mod_box.fill.fore_color.rgb = CARD_BG
    mod_box.line.color.rgb = BORDER_COLOR
    mtf = mod_box.text_frame
    mtf.word_wrap = True

    mp0 = mtf.paragraphs[0]
    mp0.text = "⚙️ Core Application Modules"
    mp0.font.size = Pt(16)
    mp0.font.bold = True
    mp0.font.color.rgb = NAVY

    modules = [
        ("Universal Self-Registration", "Students, faculty, and visitors can register using any email; auto-generates Campus ID if left blank."),
        ("Search & Dynamic Filtering", "Search across titles, descriptions, categories (IDs, keys, laptops), and spots (Library, Lab 2)."),
        ("Student Personal Hub", "Manage reports, track submitted claims, inspect incoming inquiries, and view notifications."),
        ("Admin Control Center", "Monitor college recovery rate percentage, moderate listings, manage student accounts, and export data in JSON.")
    ]
    for title, desc in modules:
        p = mtf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = BLUE
        p.space_before = Pt(8)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_DARK

    # Right Box: Step-by-Step Handover Workflow
    flow_box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(5.0))
    flow_box.fill.solid()
    flow_box.fill.fore_color.rgb = LIGHT_BLUE
    flow_box.line.color.rgb = RGBColor(191, 219, 254)
    ftf = flow_box.text_frame
    ftf.word_wrap = True

    fp0 = ftf.paragraphs[0]
    fp0.text = "🛡️ 3-Step Anti-Fraud Verification Flow"
    fp0.font.size = Pt(16)
    fp0.font.bold = True
    fp0.font.color.rgb = BLUE

    steps = [
        ("Step 1: Item Discovery & Hidden Proofs", "Finder posts item with public photo, but keeps hidden identifiers (serial, engraved marks, scratches) confidential."),
        ("Step 2: Claim Submission & Secret Match", "Claimant submits a verification claim detailing secret marks, sticker colors, or uploading purchase bills."),
        ("Step 3: Safe Chat & Handover Checkpoint", "Both parties converse in an in-portal chat thread. Finder approves claim -> Item marks 'Reunited' -> Handover at Security Gate 1.")
    ]
    for title, desc in steps:
        p = ftf.add_paragraph()
        p.text = f"{title}\n"
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = NAVY
        p.space_before = Pt(10)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = TEXT_DARK

    slide4.notes_slide.notes_text_frame.text = (
        "Slide 4 highlights our unique anti-fraud ownership verification workflow. "
        "Unlike generic lost-and-found forums where anyone can say 'that item is mine', CampusFind enforces "
        "a verification protocol. Claimants must describe details not visible in the public photos—such as lockscreen wallpapers, "
        "scratches, or serial numbers. Finders can chat with claimants inside the portal before approving. Once approved, "
        "the status updates to 'Reunited', preventing duplicate claims."
    )

    # =========================================================================
    # SLIDE 5: Demonstration Results, Impact & Future Scope
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_slide_layout)
    add_header(slide5, "Results, Campus Impact & Future Scope")

    # 3 Summary Cards
    card_w = Inches(3.75)
    gap = Inches(0.24)

    # Card 1: Results
    c1 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), card_w, Inches(4.9))
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = BORDER_COLOR
    tf_c1 = c1.text_frame
    tf_c1.word_wrap = True
    p = tf_c1.paragraphs[0]
    p.text = "📊 Demonstration Results"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    r_items = [
        ("100% Fully Functional", "Complete working frontend, backend, database, and photo upload pipeline."),
        ("Automated Test Suite", "All unit and end-to-end integration tests passing with 0 errors."),
        ("1-Click Demo Profiles", "Instant quick-fill logins for Aarav, Priya, and Admin Prof. Verma.")
    ]
    for t, d in r_items:
        p = tf_c1.add_paragraph()
        p.text = f"✔ {t}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = EMERALD
        p.space_before = Pt(10)
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_DARK

    # Card 2: Campus Impact
    c2 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8) + card_w + gap, Inches(1.8), card_w, Inches(4.9))
    c2.fill.solid()
    c2.fill.fore_color.rgb = LIGHT_BLUE
    c2.line.color.rgb = RGBColor(191, 219, 254)
    tf_c2 = c2.text_frame
    tf_c2.word_wrap = True
    p = tf_c2.paragraphs[0]
    p.text = "🌟 Campus Impact & Benefits"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = BLUE

    impact_items = [
        ("Accelerated Recovery", "Reduces item return turnaround time from weeks to hours."),
        ("Zero Identity Leaks", "Protects student phone numbers and email addresses from public exposure."),
        ("Security Audit Trail", "Gives college security guards clear accountability and verified claim logs.")
    ]
    for t, d in impact_items:
        p = tf_c2.add_paragraph()
        p.text = f"★ {t}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = BLUE
        p.space_before = Pt(10)
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_DARK

    # Card 3: Future Enhancements
    c3 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8) + (card_w + gap) * 2, Inches(1.8), card_w, Inches(4.9))
    c3.fill.solid()
    c3.fill.fore_color.rgb = CARD_BG
    c3.line.color.rgb = BORDER_COLOR
    tf_c3 = c3.text_frame
    tf_c3.word_wrap = True
    p = tf_c3.paragraphs[0]
    p.text = "🔮 Future Enhancements"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = RGBColor(124, 58, 237)

    future_items = [
        ("AI Image Matching", "Automated computer vision comparison between newly found and lost items."),
        ("SMS & WhatsApp Alerts", "Instant SMS notifications via Twilio API when matching items are found."),
        ("QR Code Bag Tags", "College-branded QR luggage stickers for instant student contact.")
    ]
    for t, d in future_items:
        p = tf_c3.add_paragraph()
        p.text = f"🚀 {t}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = RGBColor(124, 58, 237)
        p.space_before = Pt(10)
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = TEXT_DARK

    slide5.notes_slide.notes_text_frame.text = (
        "To conclude, CampusFind has been thoroughly implemented, tested, and validated as a production-grade full-stack solution. "
        "It provides tangible benefits to students and security staff by speeding up recovery and preventing fraud. "
        "In future versions, we plan to incorporate AI image similarity matching and automated SMS notifications. "
        "Thank you for your time and guidance. I am now open to your questions."
    )

    # Save presentation file
    output_path = r"C:\Users\klemp\Desktop\project\CampusFind_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    create_presentation()
