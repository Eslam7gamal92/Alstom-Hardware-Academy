import streamlit as st
from PIL import Image
from supabase import create_client, Client
import streamlit as st
from PIL import Image

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(
    page_title="Alstom Hardware Academy",
    page_icon="🚆",
    layout="wide"
)

# ---------------------------------------------------
# Session State Initialization
# ---------------------------------------------------
defaults = {
    "logged_in": False,
    "user_id": "",
    "user_name": "",
    "user_email": "",
    "mandatory_completed": False,
    "mandatory_1_completed": False,
    "mandatory_2_completed": False,
    "mandatory_3_completed": False,
    "mandatory_4_completed": False,
    "mandatory_5_completed": False,
    "mandatory_6_completed": False,
    "mandatory_7_completed": False,
    "stage1_doc_completed": False,
    "stage1_quiz_completed": False,
    "stage1_current_item": 0,
    "stage1_completed": False,
    "stage2_completed": False,
    "selected_path": "",
    "current_page": "landing"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------------------------------------------
# Helper Functions
# ---------------------------------------------------
def go_to(page_name):
    st.session_state.current_page = page_name

def logout():
    st.session_state.logged_in = False
    st.session_state.user_id = ""
    st.session_state.user_name = ""
    st.session_state.user_email = ""
    st.session_state.mandatory_completed = False
    st.session_state.mandatory_1_completed = False
    st.session_state.mandatory_2_completed = False
    st.session_state.mandatory_3_completed = False
    st.session_state.mandatory_4_completed = False
    st.session_state.mandatory_5_completed = False
    st.session_state.mandatory_6_completed = False
    st.session_state.mandatory_7_completed = False
    st.session_state.stage1_doc_completed = False
    st.session_state.stage1_quiz_completed = False
    st.session_state.stage1_current_item = 0
    st.session_state.stage1_completed = False
    st.session_state.stage2_completed = False
    st.session_state.selected_path = ""
    st.session_state.current_page = "landing"

def calculate_progress():
    progress = 0
    if st.session_state.mandatory_completed:
        progress += 20
    if st.session_state.stage1_completed:
        progress += 30
    if st.session_state.stage2_completed:
        progress += 30
    if st.session_state.selected_path:
        progress += 20
    return progress

def update_mandatory_completion():
    st.session_state.mandatory_completed = all([
        st.session_state.mandatory_1_completed,
        st.session_state.mandatory_2_completed,
        st.session_state.mandatory_3_completed,
        st.session_state.mandatory_4_completed,
        st.session_state.mandatory_5_completed,
        st.session_state.mandatory_6_completed,
        st.session_state.mandatory_7_completed,
    ])

def resize_image_to_height(image_path, target_height=320):
    img = Image.open(image_path)
    width, height = img.size
    new_width = int((target_height / height) * width)
    resized_img = img.resize((new_width, target_height))
    return resized_img

def save_progress():
    progress = calculate_progress()

    supabase_admin.table("user_progress").upsert(
        {
            "user_id": st.session_state.user_id,
            "mandatory_completed": st.session_state.mandatory_completed,
            "mandatory_1_completed": st.session_state.mandatory_1_completed,
            "mandatory_2_completed": st.session_state.mandatory_2_completed,
            "mandatory_3_completed": st.session_state.mandatory_3_completed,
            "mandatory_4_completed": st.session_state.mandatory_4_completed,
            "mandatory_5_completed": st.session_state.mandatory_5_completed,
            "mandatory_6_completed": st.session_state.mandatory_6_completed,
            "mandatory_7_completed": st.session_state.mandatory_7_completed,
            "stage1_doc_completed": st.session_state.stage1_doc_completed,
            "stage1_quiz_completed": st.session_state.stage1_quiz_completed,
            "stage1_completed": st.session_state.stage1_completed,
            "stage2_completed": st.session_state.stage2_completed,
            "selected_path": st.session_state.selected_path,
            "progress_percent": progress
        },
        on_conflict="user_id"
    ).execute()

MANDATORY_COURSES = [
    {
        "key": "mandatory_1_completed",
        "title": "Alstom Railway Safety Induction",
        "duration": "45 minutes",
        "link": "https://alstomuniversity.eu.crossknowledge.com/site/path/53541?origin=lc_widget#tab/path/activity/219533",
        "image": "mandatory_1.jpg",
        "description": "Introduce the concept of Railway Safety and its implication within Alstom."
    },
    {
        "key": "mandatory_2_completed",
        "title": "Alstom Information Security Awareness",
        "duration": "15 minutes",
        "link": "https://alstomuniversity.eu.crossknowledge.com/site/path/7382?origin=lc_widget#tab/path/activity/49165",
        "image": "mandatory_2.png",
        "description": "Raise awareness on basic IT security good practices and information protection."
    },
    {
        "key": "mandatory_3_completed",
        "title": "Alstom Ethics and Compliance Alert Procedure",
        "duration": "3 minutes",
        "link": "https://alstomuniversity.eu.crossknowledge.com/site/path/7383?origin=lc_widget#tab/path/activity/49167",
        "image": "mandatory_3.png",
        "description": "Understand what the Alstom Alert Procedure is and what types of issues can be reported."
    },
     {
        "key": "mandatory_4_completed",
        "title": "Conflicts of Interest - Course 2024",
        "duration": "10 minutes",
        "link": "https://alstomuniversity.eu.crossknowledge.com/site/path/31252?origin=lc_widget#tab/path/activity/139730",
        "image": "mandatory_4.jpg",
        "description": "Identify situations of conflict of interest and understand how to handle them properly."
    },
    {
        "key": "mandatory_5_completed",
        "title": "e-ethics 2020 - Course 2024",
        "duration": "30 minutes",
        "link": "https://alstomuniversity.eu.crossknowledge.com/site/path/31269?origin=lc_widget#tab/path/activity/139766",
        "image": "mandatory_5.jpg",
        "description": "Increase awareness of ethics principles and expected professional conduct at Alstom."
    },
    {
        "key": "mandatory_6_completed",
        "title": "USB cybersecurity",
        "duration": "15 minutes",
        "link": "https://alstomuniversity.eu.crossknowledge.com/site/path/7402?origin=lc_widget#tab/path/activity/49425",
        "image": "mandatory_6.jpg",
        "description": "Learn about threats and risks related to USB devices and best practices to avoid them."
    },
    {
        "key": "mandatory_7_completed",
        "title": "Dawn Raids protocol",
        "duration": "5 minutes",
        "link": "https://alstomuniversity.eu.crossknowledge.com/site/path/52725?origin=lc_widget#tab/path/activity/216440",
        "image": "mandatory_7.jpg",
        "description": "Provide a general understanding of what constitutes a dawn raid and the right response."
    }
]

STAGE1_ITEMS = [
    {
        "key": "stage1_doc_completed",
        "title": "Railway System Document",
        "type": "PDF",
        "duration": "Self-paced",
        "description": "Download and study the railway system document before proceeding to the quiz.",
        "file": "stage1_railway_system.pdf"
    },
    {
        "key": "stage1_quiz_completed",
        "title": "Stage 1 Quiz",
        "type": "Quiz",
        "duration": "Short assessment",
        "description": "Complete the quiz based on the Stage 1 railway system document.",
        "file": ""
    }
]
# ---------------------------------------------------
# Supabase Connection
# ---------------------------------------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_ANON_KEY = st.secrets["SUPABASE_ANON_KEY"]
SUPABASE_SERVICE_ROLE_KEY = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]

supabase_auth: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# ---------------------------------------------------
# Global Style
# ---------------------------------------------------
st.markdown("""
<style>
.main {
    background-color: #FFFFFF;
}

.hero-box {
    background: linear-gradient(90deg, #0B3D91 0%, #123E8C 100%);
    padding: 42px 38px;
    border-radius: 20px;
    color: white;
    margin-top: 10px;
    margin-bottom: 20px;
}

.section-box {
    background-color: #F5F5F7;
    padding: 24px;
    border-radius: 16px;
    margin-bottom: 14px;
}

.white-box {
    background-color: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #E5E7EB;
    margin-bottom: 14px;
    min-height: 205px;
}

.stats-box {
    background-color: #F5F5F7;
    padding: 20px 18px;
    border-radius: 14px;
    text-align: center;
    border: 1px solid #E5E7EB;
    height: 185px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.card-box {
    background-color: white;
    padding: 16px;
    border-radius: 14px;
    border: 1px solid #D1D5DB;
    margin-bottom: 12px;
    min-height: 130px;
}

.small-title {
    color: #DCE7FF;
    font-weight: 600;
    font-size: 14px;
    letter-spacing: 0.4px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.main-title {
    font-size: 40px;
    font-weight: 700;
    color: white;
    line-height: 1.18;
    margin-bottom: 12px;
}

.hero-text {
    font-size: 17px;
    color: #E5E7EB;
    line-height: 1.65;
}

.section-title {
    font-size: 28px;
    font-weight: 700;
    color: #1F2937;
    margin-bottom: 6px;
}

.section-text {
    font-size: 16px;
    color: #374151;
    line-height: 1.65;
}

.nav-center {
    text-align: center;
    padding-top: 8px;
    font-size: 16px;
    font-weight: 700;
    color: #1F2937;
    white-space: nowrap;
}

.footer-text {
    text-align: center;
    color: #6B7280;
    font-size: 15px;
    padding-bottom: 10px;
}

.home-hero {
    background: linear-gradient(90deg, #0B3D91 0%, #123E8C 100%);
    padding: 44px 40px;
    border-radius: 20px;
    color: white;
    margin-bottom: 18px;
}

.home-hero-title {
    font-size: 44px;
    font-weight: 700;
    margin-bottom: 12px;
    color: white;
}

.home-hero-text {
    font-size: 18px;
    color: #E5E7EB;
    line-height: 1.8;
}

.stage-card {
    background-color: white;
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 22px;
    min-height: 250px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
    margin-bottom: 18px;
}

.stage-card-title {
    font-size: 20px;
    font-weight: 700;
    color: #1F3552;
    margin-bottom: 10px;
    line-height: 1.4;
}

.stage-card-text {
    font-size: 15px;
    color: #4B5563;
    line-height: 1.75;
    margin-bottom: 18px;
}

.stage-badge-completed {
    display: inline-block;
    background-color: #D1FAE5;
    color: #065F46;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 14px;
}

.stage-badge-current {
    display: inline-block;
    background-color: #DBEAFE;
    color: #1D4ED8;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 14px;
}

.stage-badge-locked {
    display: inline-block;
    background-color: #F3F4F6;
    color: #6B7280;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 14px;
}

.info-panel {
    background-color: white;
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 28px;
    min-height: 150px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
}
            
.mandatory-hero {
    background: linear-gradient(90deg, #0B3D91 0%, #123E8C 100%);
    padding: 36px 32px;
    border-radius: 20px;
    color: white;
    margin-bottom: 20px;
}

.mandatory-hero-title {
    font-size: 34px;
    font-weight: 700;
    margin-bottom: 10px;
    color: white;
}

.mandatory-hero-text {
    font-size: 17px;
    color: #E5E7EB;
    line-height: 1.75;
}

.mandatory-card {
    background-color: white;
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 18px;
    min-height: 420px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
    margin-bottom: 18px;
}

.mandatory-card-title {
    font-size: 20px;
    font-weight: 700;
    color: #1F3552;
    margin-top: 10px;
    margin-bottom: 8px;
    line-height: 1.4;
}

.mandatory-card-duration {
    font-size: 14px;
    color: #0B3D91;
    font-weight: 600;
    margin-bottom: 12px;
}

.mandatory-card-text {
    font-size: 15px;
    color: #4B5563;
    line-height: 1.7;
    margin-bottom: 16px;
}

.mandatory-status-done {
    display: inline-block;
    background-color: #D1FAE5;
    color: #065F46;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 12px;
}

.mandatory-status-pending {
    display: inline-block;
    background-color: #FEF3C7;
    color: #92400E;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 12px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Landing Page
# ---------------------------------------------------
if st.session_state.current_page == "landing":

    nav1, nav2, nav3 = st.columns([2.2, 3.6, 2.2])

    with nav1:
        try:
            st.image("alstom_logo.png", width=180)
            st.caption("Alstom Hardware Academy")
        except:
            st.markdown("## **ALSTOM**")
            st.caption("Alstom Hardware Academy")

    with nav2:
        st.markdown(
            """
            <div class="nav-center">
            Explore &nbsp;&nbsp;&nbsp; Learning Journey &nbsp;&nbsp;&nbsp; Specializations &nbsp;&nbsp;&nbsp; About
            </div>
            """,
            unsafe_allow_html=True
        )

    with nav3:
        b1, b2 = st.columns(2)
        with b1:
            if st.button("Log in", use_container_width=True, key="landing_login"):
                go_to("auth")
                st.rerun()
        with b2:
            if st.button("Join Now", use_container_width=True, key="landing_join"):
                go_to("auth")
                st.rerun()

    st.write("")

    # 1. Hero
    st.markdown("""
    <div class="hero-box">
        <div class="small-title">Structured Learning for New Joiners</div>
        <div class="main-title">A structured onboarding and learning journey for new hardware engineers</div>
        <div class="hero-text">
            Alstom Hardware Academy is designed to support newly joined engineers with a guided learning experience,
            starting from company introduction and railway system fundamentals, moving into signalling and hardware basics,
            and finally leading into specialized technical paths such as Pedals, OBC, HVITC, and Cable Chassis.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Key Highlights
    st.markdown('<h2 style="color:#1F3552; font-weight:700;">Key Highlights</h2>', unsafe_allow_html=True)
    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.markdown("""
        <div class="stats-box">
            <h2 style="color:#0B3D91; font-size:48px; margin-bottom:8px;">100%</h2>
            <p style="font-size:15px;">Structured onboarding flow</p>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div class="stats-box">
            <h2 style="color:#0B3D91; font-size:48px; margin-bottom:8px;">3</h2>
            <p style="font-size:15px;">Main learning stages</p>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown("""
        <div class="stats-box">
            <h2 style="color:#0B3D91; font-size:48px; margin-bottom:8px;">1</h2>
            <p style="font-size:15px;">Centralized learning platform</p>
        </div>
        """, unsafe_allow_html=True)

    with s4:
        st.markdown("""
        <div class="stats-box">
            <h2 style="color:#0B3D91; font-size:48px; margin-bottom:8px;">∞</h2>
            <p style="font-size:15px;">Continuous learning potential</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # 3 + 4. Platform Objectives / Why This Platform Matters
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="white-box">
            <div class="section-title">Platform Objectives</div>
            <div class="section-text">
                • Reduce onboarding time<br>
                • Standardize the learning journey<br>
                • Create one source of truth<br>
                • Improve knowledge retention<br>
                • Support continuous development
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="white-box">
            <div class="section-title">Why This Platform Matters</div>
            <div class="section-text">
                New engineers often face scattered resources and inconsistent onboarding. Alstom Hardware Academy gives each newcomer
                a guided learning flow, clear stages, and measurable progress toward technical readiness.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 5. About Alstom
    st.markdown("""
    <div class="section-box">
        <div class="section-title">About Alstom</div>
        <div class="section-text">
            Alstom is a global leader in smart and sustainable mobility, delivering integrated railway solutions across signaling,
            infrastructure, rolling stock, digital systems, and services. The company contributes to building safer, more efficient,
            and more sustainable transportation systems across the world.
            <br><br>
            In Egypt, Alstom plays an important role in mobility development and railway modernization. For a newcomer joining the
            hardware function, understanding the company context is essential — not only from a business perspective, but also from
            a technical and project integration perspective.
            <br><br>
            Alstom Hardware Academy was created to make that onboarding journey clearer, more structured, and more engaging.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 6. Vision / Mission / Values
    st.markdown('<h2 style="color:#1F3552; font-weight:700;">Vision, Mission & Values</h2>', unsafe_allow_html=True)

    vm1, vm2, vm3 = st.columns(3)

    with vm1:
        st.markdown("""
        <div class="white-box">
            <div class="section-title">Vision</div>
            <div class="section-text">
                Support smarter and more sustainable mobility by helping engineers understand the systems,
                technologies, and responsibilities that shape modern railway solutions.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with vm2:
        st.markdown("""
        <div class="white-box">
            <div class="section-title">Mission</div>
            <div class="section-text">
                Build a clear onboarding experience that transforms scattered information into a structured
                and practical learning journey for every new hardware engineer.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with vm3:
        st.markdown("""
        <div class="white-box">
            <div class="section-title">Core Values</div>
            <div class="section-text">
                Collaboration, safety, innovation, reliability, and continuous development are essential
                to both railway operations and engineering growth.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 7. Alstom and Global Mobility Impact
    st.markdown("""
    <div class="section-box">
        <div class="section-title">Alstom and Global Mobility Impact</div>
        <div class="section-text">
            Alstom contributes to the future of mobility through railway transportation solutions that combine
            engineering, digital systems, infrastructure, signaling, and services. Its role extends beyond delivering
            products — it also helps shape how cities and countries modernize transportation in a safer, smarter,
            and more sustainable way.
            <br><br>
            For engineers joining the organization, this means working in an environment where technical decisions are
            directly connected to operational reliability, passenger safety, system integration, and long-term project performance.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 8. Alstom in Egypt
    st.markdown("""
    <div class="section-box">
        <div class="section-title">Alstom in Egypt</div>
        <div class="section-text">
            In Egypt, Alstom is associated with major mobility and railway development ambitions, supporting the
            transformation of transportation systems and contributing to modern infrastructure initiatives. For local teams,
            this creates an environment where newcomers are not only joining a company, but also becoming part of long-term
            projects that carry technical, operational, and strategic impact.
            <br><br>
            Understanding this local context helps new engineers connect faster with the business purpose, the project
            environment, and the expectations of their technical role.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 9. Explore Learning Areas
    st.markdown('<h2 style="color:#1F3552; font-weight:700;">Explore Learning Areas</h2>', unsafe_allow_html=True)
    st.write("Discover the main learning tracks included in Alstom Hardware Academy.")

    card1, card2 = st.columns(2)

    with card1:
        try:
            img1 = resize_image_to_height("railway_system.jpg", 320)
            st.image(img1, use_container_width=True)
        except:
            st.info("Add image: railway_system.jpg")
        st.markdown("""
        <div style="padding:8px 10px 12px 6px;">
            <h3 style="color:#0B3D91; margin-top:0px; margin-bottom:6px;">Railway System</h3>
            <p style="font-size:16px; color:#374151; line-height:1.55;">
                Build a high-level understanding of railway systems, infrastructure, rolling stock, power, telecom, and railway operations.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with card2:
        try:
            img2 = resize_image_to_height("specialized_paths.jpg", 320)
            st.image(img2, use_container_width=True)
        except:
            st.info("Add image: specialized_paths.jpg")
        st.markdown("""
        <div style="padding:8px 10px 12px 6px;">
            <h3 style="color:#0B3D91; margin-top:0px; margin-bottom:6px;">Specialized Paths</h3>
            <p style="font-size:16px; color:#374151; line-height:1.55;">
                Move into focused technical areas such as Pedals, OBC, Cable Chassis, and HVITC based on your role and learning goals.
            </p>
        </div>
        """, unsafe_allow_html=True)

    card3, card4 = st.columns(2)

    with card3:
        try:
            img3 = Image.open("signalling_hardware.jpg")
            st.image(img3, width=760)
        except:
            st.info("Add image: signalling_hardware.jpg")
        st.markdown("""
        <div style="padding:8px 10px 12px 6px;">
            <h3 style="color:#0B3D91; margin-top:0px; margin-bottom:6px;">Signalling & Hardware Fundamentals</h3>
            <p style="font-size:16px; color:#374151; line-height:1.55;">
                Learn key hardware concepts, system interfaces, signalling basics, component understanding, and engineering principles.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with card4:
        try:
            img4 = resize_image_to_height("progress_tracking.jpg", 320)
            st.image(img4, use_container_width=True)
        except:
            st.info("Add image: progress_tracking.jpg")
        st.markdown("""
        <div style="padding:8px 10px 12px 6px;">
            <h3 style="color:#0B3D91; margin-top:0px; margin-bottom:6px;">Progress Tracking</h3>
            <p style="font-size:16px; color:#374151; line-height:1.55;">
                Track learning completion, unlock stages, validate understanding through quizzes, and monitor your progress step by step.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # 10. Why Alstom Hardware Academy?
    st.markdown("""
    <div class="section-box">
        <div class="section-title">Why Alstom Hardware Academy?</div>
        <div class="section-text">
            Alstom Hardware Academy is more than a content repository. It is a guided experience built to reduce confusion,
            improve onboarding quality, and create a shared technical language across newcomers, senior engineers, and managers.
            <br><br>
            Instead of relying only on scattered files or informal support, the platform provides a structured route:
            start with company awareness, continue through railway and hardware fundamentals, validate understanding
            through quizzes, and finally move into role-based specialization.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 11. Final CTA
    st.markdown("""
    <div class="hero-box" style="padding:30px 34px;">
        <div class="section-title" style="color:white;">Start your learning journey today</div>
        <div class="hero-text">
            Join Alstom Hardware Academy and begin a structured onboarding experience tailored for new hardware engineers.
        </div>
    </div>
    """, unsafe_allow_html=True)

    btn_left, btn1, btn2, btn_right = st.columns([1.5, 1, 1, 1.5])

    with btn1:
        if st.button("Create Account", use_container_width=True, key="landing_create_account"):
            go_to("auth")
            st.rerun()

    with btn2:
        if st.button("Access Platform", use_container_width=True, key="landing_access_platform"):
            go_to("auth")
            st.rerun()

    # 12. Footer
    st.markdown("""
    <hr style="margin-top:28px; margin-bottom:12px;">
    <div class="footer-text">
        <strong>Alstom Hardware Academy Platform</strong><br>
        Built to support onboarding, technical learning, and knowledge development for hardware engineers at Alstom.
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------
# Authentication Page
# ---------------------------------------------------
elif st.session_state.current_page == "auth":

    st.markdown("""
    <style>
    .auth-left-box {
        background: linear-gradient(180deg, #0B3D91 0%, #123E8C 100%);
        border-radius: 20px;
        padding: 35px 30px;
        color: white;
        margin-bottom: 25px;
    }
    .auth-left-title {
        font-size: 34px;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 15px;
        color: white;
    }
    .auth-left-text {
        font-size: 17px;
        line-height: 1.75;
        color: #E5E7EB;
        margin-bottom: 18px;
    }
    .auth-form-title {
        font-size: 30px;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 8px;
    }
    .auth-form-subtitle {
        font-size: 16px;
        color: #6B7280;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    top1, top2 = st.columns([1, 6])

    with top1:
        if st.button("← Home", key="auth_back_home"):
            go_to("landing")
            st.rerun()

    st.write("")

    # Logo aligned left
    try:
        st.image("alstom_logo.png", width=180)
    except:
        st.markdown("## **ALSTOM**")
    st.caption("Alstom Hardware Academy")

    st.write("")

    # Full width blue intro box
    st.markdown("""
    <div class="auth-left-box">
        <div class="auth-left-title">Start your onboarding journey with confidence</div>
        <div class="auth-left-text">
            Alstom Hardware Academy is designed to give new hardware engineers a clear and structured learning experience.
        </div>
        <div class="auth-left-text">
            Through this platform, you will explore:
            <br><br>
            • Railway System fundamentals<br>
            • Signalling & Hardware basics<br>
            • Role-based specialization paths<br>
            • Guided progress through each stage
        </div>
        <div class="auth-left-text">
            Create your account or log in to continue your learning journey.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Narrow centered form section
    form_left, form_center, form_right = st.columns([1.2, 2.6, 1.2])

    with form_center:
        st.markdown('<div class="auth-form-title">Login / Sign Up</div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-form-subtitle">Access your learning space and continue your technical onboarding journey.</div>', unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            st.subheader("Login")
            login_email = st.text_input("Email", key="login_email")
            login_password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login to Platform", use_container_width=True, key="auth_login_platform"):
                if login_email and login_password:
                    try:
                        auth_response = supabase_auth.auth.sign_in_with_password({
                            "email": login_email,
                            "password": login_password
                        })

                        user = auth_response.user

                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user_id = user.id
                            st.session_state.user_email = user.email

                            profile_res = supabase_admin.table("profiles").select("*").eq("id", user.id).execute()
                            if profile_res.data:
                                st.session_state.user_name = profile_res.data[0]["full_name"]
                            else:
                                st.session_state.user_name = user.email.split("@")[0].replace(".", " ").title()

                            progress_res = supabase_admin.table("user_progress").select("*").eq("user_id", user.id).execute()
                            if progress_res.data:
                                progress_data = progress_res.data[0]
                                st.session_state.mandatory_completed = progress_data.get("mandatory_completed", False)
                                st.session_state.mandatory_1_completed = progress_data.get("mandatory_1_completed", False)
                                st.session_state.mandatory_2_completed = progress_data.get("mandatory_2_completed", False)
                                st.session_state.mandatory_3_completed = progress_data.get("mandatory_3_completed", False)
                                st.session_state.mandatory_4_completed = progress_data.get("mandatory_4_completed", False)
                                st.session_state.mandatory_5_completed = progress_data.get("mandatory_5_completed", False)
                                st.session_state.mandatory_6_completed = progress_data.get("mandatory_6_completed", False)
                                st.session_state.mandatory_7_completed = progress_data.get("mandatory_7_completed", False)
                                st.session_state.stage1_doc_completed = progress_data.get("stage1_doc_completed", False)
                                st.session_state.stage1_quiz_completed = progress_data.get("stage1_quiz_completed", False)
                                st.session_state.stage1_completed = progress_data.get("stage1_completed", False)
                                st.session_state.stage2_completed = progress_data.get("stage2_completed", False)
                                st.session_state.selected_path = progress_data.get("selected_path", "")

                            go_to("home")
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Login failed. Please check your credentials.")

                    except Exception as e:
                        st.error(f"Login error: {e}")
                else:
                    st.error("Please enter both email and password.")

        with tab2:
            st.subheader("Create New Account")
            full_name = st.text_input("Full Name", key="signup_full_name")
            signup_email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")

            if st.button("Create Account", use_container_width=True, key="auth_create_account"):
                if not full_name or not signup_email or not password or not confirm_password:
                    st.error("Please complete all fields.")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    try:
                        # Create auth user
                        auth_response = supabase_auth.auth.sign_up({
                            "email": signup_email,
                            "password": password
                        })

                        user = auth_response.user

                        if user is not None:
                            # Insert into profiles table
                            supabase_admin.table("profiles").insert({
                                "id": user.id,
                                "full_name": full_name,
                                "email": signup_email
                            }).execute()

                            # Insert initial progress
                            supabase_admin.table("user_progress").insert({
                                "user_id": user.id,
                                "mandatory_completed": False,
                                "mandatory_1_completed": False,
                                "mandatory_2_completed": False,
                                "mandatory_3_completed": False,
                                "mandatory_4_completed": False,
                                "mandatory_5_completed": False,
                                "mandatory_6_completed": False,
                                "mandatory_7_completed": False,
                                "stage1_completed": False,
                                "stage2_completed": False,
                                "selected_path": "",
                                "progress_percent": 0
                            }).execute()

                            st.success("Account created successfully! You can now log in.")
                        else:
                            st.error("Sign up failed. Please try again.")

                    except Exception as e:
                        st.error(f"Sign up error: {e}")

# ---------------------------------------------------
# Home Page
# ---------------------------------------------------
elif st.session_state.current_page == "home":
    if not st.session_state.logged_in:
        st.warning("Please login first.")
        if st.button("Go to Login", key="home_go_to_login"):
            go_to("auth")
            st.rerun()
    else:
        top1, top2, top3 = st.columns([2, 4, 2])

        with top1:
            try:
                st.image("alstom_logo.png", width=180)
            except:
                st.markdown("## **ALSTOM**")
            st.caption("Alstom Hardware Academy")

        with top3:
            if st.button("Logout", use_container_width=True, key="home_logout"):
                logout()
                st.rerun()

        progress = calculate_progress()

        # Hero Welcome
        st.markdown(f"""
        <div class="home-hero">
            <div class="home-hero-title">Welcome, {st.session_state.user_name} 👋</div>
            <div class="home-hero-text">
                Your onboarding journey is organized into three guided stages: Railway System,
                Signalling & Hardware Fundamentals, and your final Specialization path.
                Follow them step by step to build your technical foundation and track your readiness.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Progress
        st.markdown(f'<h3 style="color:#1F3552; margin-bottom:12px;">Your Progress</h3>', unsafe_allow_html=True)
        st.progress(progress / 100)
        st.write(f"Progress: **{progress}%**")

        # About journey first
        st.markdown("""
        <div class="info-panel" style="margin-bottom:22px;">
            <h3 style="color:#1F3552; margin-bottom:12px;">About Your Journey</h3>
            <p style="font-size:16px; color:#374151; line-height:1.75; margin-bottom:0;">
                Alstom Hardware Academy is designed to make onboarding clearer, faster, and more structured.
                Instead of navigating scattered documents, you will move through a defined learning path,
                starting with the railway system, then hardware fundamentals, and finally your technical specialization.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Stage cards title
        st.markdown('<h2 style="color:#1F3552; font-weight:700;">Your Learning Journey</h2>', unsafe_allow_html=True)
        st.write("Explore the three stages of your journey and continue from your current step.")

        # Status logic
        if st.session_state.mandatory_completed:
            mandatory_badge = '<div class="stage-badge-completed">Completed</div>'
        else:
            mandatory_badge = '<div class="stage-badge-current">Required First</div>'

        if st.session_state.stage1_completed:
            stage1_badge = '<div class="stage-badge-completed">Completed</div>'
        elif st.session_state.mandatory_completed:
            stage1_badge = '<div class="stage-badge-current">Current Stage</div>'
        else:
            stage1_badge = '<div class="stage-badge-locked">Locked</div>'

        if st.session_state.stage2_completed:
            stage2_badge = '<div class="stage-badge-completed">Completed</div>'
        elif st.session_state.stage1_completed:
            stage2_badge = '<div class="stage-badge-current">Current Stage</div>'
        else:
            stage2_badge = '<div class="stage-badge-locked">Locked</div>'

        if st.session_state.selected_path:
            stage3_badge = '<div class="stage-badge-completed">Path Selected</div>'
        elif st.session_state.stage2_completed:
            stage3_badge = '<div class="stage-badge-current">Ready to Choose</div>'
        else:
            stage3_badge = '<div class="stage-badge-locked">Locked</div>'

        # Row 1
        c1, c2 = st.columns(2)

        with c1:
            st.markdown(f"""
            <div class="stage-card">
                {mandatory_badge}
                <div class="stage-card-title">Mandatory Trainings</div>
                <div class="stage-card-text">
                    Complete the required onboarding trainings before starting your technical learning journey.
                    These courses are mandatory for all new joiners.
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Enter Mandatory Trainings", use_container_width=True, key="open_mandatory"):
                go_to("mandatory_trainings")
                st.rerun()

        with c2:
            st.markdown(f"""
            <div class="stage-card">
                {stage1_badge}
                <div class="stage-card-title">Stage 1: Railway System</div>
                <div class="stage-card-text">
                    Start by building a high-level understanding of railway systems, infrastructure,
                    rolling stock, power systems, and the overall railway ecosystem.
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(
                "Enter Stage 1",
                use_container_width=True,
                key="open_stage1",
                disabled=not st.session_state.mandatory_completed
            ):
                go_to("stage1")
                st.rerun()

        # Row 2
        c3, c4 = st.columns(2)

        with c3:
            st.markdown(f"""
            <div class="stage-card">
                {stage2_badge}
                <div class="stage-card-title">Stage 2: Signalling & Hardware</div>
                <div class="stage-card-text">
                    Continue with signalling concepts, hardware fundamentals, interfaces,
                    system components, and core engineering principles used in the function.
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Enter Stage 2", use_container_width=True, key="open_stage2"):
                go_to("learning")
                st.rerun()

        with c4:
            st.markdown(f"""
            <div class="stage-card">
                {stage3_badge}
                <div class="stage-card-title">Stage 3: Specialization</div>
                <div class="stage-card-text">
                    Move into your role-based specialization path such as Pedals, OBC,
                    Cable Chassis, or HVITC based on your learning direction.
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Enter Stage 3", use_container_width=True, key="open_stage3"):
                go_to("learning")
                st.rerun()

# ---------------------------------------------------
# Mandatory Trainings Page
# ---------------------------------------------------
elif st.session_state.current_page == "mandatory_trainings":
    if not st.session_state.logged_in:
        st.warning("Please login first.")
        if st.button("Go to Login", key="mandatory_go_to_login"):
            go_to("auth")
            st.rerun()
    else:
        top1, top2, top3 = st.columns([2, 4, 2])

        with top1:
            if st.button("← Home", use_container_width=True, key="mandatory_home"):
                go_to("home")
                st.rerun()

        with top3:
            if st.button("Profile", use_container_width=True, key="mandatory_profile"):
                go_to("profile")
                st.rerun()

        st.markdown("""
        <div class="mandatory-hero">
            <div class="mandatory-hero-title">Mandatory Trainings</div>
            <div class="mandatory-hero-text">
                Before starting your technical learning journey, please complete the required onboarding trainings.
                These courses are mandatory for all new joiners and must be completed before progressing to Stage 1.
            </div>
        </div>
        """, unsafe_allow_html=True)

        progress = calculate_progress()
        st.markdown(f"### Progress: {progress}%")
        st.progress(progress / 100)

        if st.session_state.mandatory_completed:
            st.success("All mandatory trainings have been completed successfully ✅")
        else:
            st.info("Please complete all mandatory trainings before starting Stage 1.")

        st.write("")

        for i in range(0, len(MANDATORY_COURSES), 3):
            row_courses = MANDATORY_COURSES[i:i+3]

            if len(row_courses) == 1:
                left, center, right = st.columns([1, 1.2, 1])
                cols = [center]
            else:
                cols = st.columns(3)

            for col, course in zip(cols, row_courses):
                with col:
                    completed = st.session_state[course["key"]]

                    try:
                        course_img = resize_image_to_height(course["image"], 220)
                        st.image(course_img, use_container_width=True)
                    except:
                        st.info(f"Add image: {course['image']}")

                    if completed:
                        st.markdown('<div class="mandatory-status-done">Completed</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="mandatory-status-pending">Pending</div>', unsafe_allow_html=True)

                    st.markdown(f'<div class="mandatory-card-title">{course["title"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="mandatory-card-duration">{course["duration"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="mandatory-card-text">{course["description"]}</div>', unsafe_allow_html=True)

                    st.markdown(
                        f"""
                        <a href="{course['link']}" target="_blank" style="text-decoration:none;">
                            <div style="
                                background-color:#0B3D91;
                                color:white;
                                text-align:center;
                                padding:12px 14px;
                                border-radius:12px;
                                font-weight:700;
                                font-size:16px;
                                margin-top:6px;
                                margin-bottom:10px;
                            ">
                                Open Course
                            </div>
                        </a>
                        """,
                        unsafe_allow_html=True
                    )

                    if not completed:
                        if st.button("Mark as Completed", use_container_width=True, key=f'complete_{course["key"]}'):
                            st.session_state[course["key"]] = True
                            update_mandatory_completion()
                            save_progress()
                            st.rerun()
                    else:
                        st.button("Completed", use_container_width=True, key=f'done_{course["key"]}', disabled=True)

            st.write("")

# ---------------------------------------------------
# Stage 1 Page
# ---------------------------------------------------
elif st.session_state.current_page == "stage1":
    if not st.session_state.logged_in:
        st.warning("Please login first.")
        if st.button("Go to Login", key="stage1_go_to_login"):
            go_to("auth")
            st.rerun()
    else:
        top1, top2, top3 = st.columns([2, 4, 2])

        with top1:
            if st.button("← Home", use_container_width=True, key="stage1_home"):
                go_to("home")
                st.rerun()

        with top3:
            if st.button("Profile", use_container_width=True, key="stage1_profile"):
                go_to("profile")
                st.rerun()

        st.title("Stage 1: Railway System")

        progress = calculate_progress()
        st.progress(progress / 100)
        st.write(f"Overall Progress: **{progress}%**")

        st.write("---")

        if not st.session_state.mandatory_completed:
            st.info("This stage is locked. Complete Mandatory Trainings first.")
        else:
            # Set current item automatically
            if not st.session_state.stage1_doc_completed:
                st.session_state.stage1_current_item = 0
            elif not st.session_state.stage1_quiz_completed:
                st.session_state.stage1_current_item = 1
            else:
                st.session_state.stage1_current_item = 1

            left_col, right_col = st.columns([1.1, 2.2])

            # -----------------------------
            # Left Sidebar
            # -----------------------------
            with left_col:
                st.markdown("### Stage 1 Content")

                for idx, item in enumerate(STAGE1_ITEMS):
                    completed = st.session_state[item["key"]]
                    icon = "✅" if completed else "⬜"

                    label = f"{icon} {item['title']}"

                    if st.button(label, use_container_width=True, key=f"stage1_item_nav_{idx}"):
                        st.session_state.stage1_current_item = idx
                        st.rerun()

            # -----------------------------
            # Main Content Area
            # -----------------------------
            with right_col:
                current_index = st.session_state.stage1_current_item
                current_item = STAGE1_ITEMS[current_index]

                st.markdown(f"## {current_item['title']}")
                st.write(f"**Type:** {current_item['type']}")
                st.write(f"**Duration:** {current_item['duration']}")
                st.write(current_item["description"])
                st.write("")

                # -------------------------
                # Item 1: PDF Document
                # -------------------------
                if current_index == 0:
                    try:
                        with open(current_item["file"], "rb") as pdf_file:
                            st.download_button(
                                label="Download Document",
                                data=pdf_file,
                                file_name=current_item["file"],
                                mime="application/pdf",
                                use_container_width=True,
                                key="stage1_download_pdf"
                            )
                    except Exception:
                        st.error(f"PDF file not found: {current_item['file']}")

                    st.write("")

                    if not st.session_state.stage1_doc_completed:
                        if st.button("Mark Document as Completed", use_container_width=True, key="stage1_doc_complete"):
                            st.session_state.stage1_doc_completed = True
                            st.session_state.stage1_current_item = 1
                            save_progress()
                            st.rerun()
                    else:
                        st.success("Document completed ✅")

                    st.write("")

                    if st.button("Go to Next Item", use_container_width=True, key="stage1_next_from_doc"):
                        st.session_state.stage1_current_item = 1
                        st.rerun()

                # -------------------------
                # Item 2: Quiz
                # -------------------------
                elif current_index == 1:
                    if not st.session_state.stage1_doc_completed:
                        st.info("Please complete the document first before attempting the quiz.")
                    else:
                        if not st.session_state.stage1_quiz_completed:
                            st.subheader("Stage 1 Quiz")

                            q1 = st.radio(
                                "What is the main purpose of railway signalling?",
                                [
                                    "Entertainment",
                                    "Train safety and control",
                                    "Food service"
                                ],
                                key="stage1_q1_page"
                            )

                            if st.button("Submit Quiz", use_container_width=True, key="stage1_submit_quiz_page"):
                                if q1 == "Train safety and control":
                                    st.session_state.stage1_quiz_completed = True
                                    st.session_state.stage1_completed = True
                                    save_progress()
                                    st.success("Stage 1 completed successfully!")
                                    st.rerun()
                                else:
                                    st.error("Incorrect answer. Please try again.")
                        else:
                            st.success("Quiz completed ✅")
                            st.success("Stage 1 completed successfully ✅")

# ---------------------------------------------------
# Learning Journey Page
# ---------------------------------------------------
elif st.session_state.current_page == "learning":
    if not st.session_state.logged_in:
        st.warning("Please login first.")
        if st.button("Go to Login", key="learning_go_to_login"):
            go_to("auth")
            st.rerun()
    else:
        top1, top2, top3 = st.columns([2, 4, 2])

        with top1:
            if st.button("← Home", use_container_width=True, key="learning_home"):
                go_to("home")
                st.rerun()

        with top3:
            if st.button("Profile", use_container_width=True, key="learning_profile"):
                go_to("profile")
                st.rerun()

        st.title("Learning Journey")

        progress = calculate_progress()
        st.progress(progress / 100)
        st.write(f"Overall Progress: **{progress}%**")

        st.write("---")

        st.header("Stage 1: Railway System")

        if not st.session_state.mandatory_completed:
            st.info("This stage is locked. Complete Mandatory Trainings first.")
        else:
            st.write("""
        This stage introduces the learner to:
        - Railway ecosystem
        - Rolling stock
        - Infrastructure
        - Power systems
        - General railway understanding
        """)

            with st.expander("Open Stage 1 Content"):
                st.write("Here you can later add:")
                st.write("- Videos")
                st.write("- PDF files")
                st.write("- Technical articles")
                st.write("- Introductory presentations")

            if not st.session_state.stage1_completed:
                st.subheader("Stage 1 Quiz")
                q1 = st.radio(
                    "What is the main purpose of railway signalling?",
                    [
                        "Entertainment",
                        "Train safety and control",
                        "Food service"
                    ],
                    key="q1"
                )

                if st.button("Submit Stage 1 Quiz", use_container_width=True, key="submit_stage1"):
                    if q1 == "Train safety and control":
                        st.session_state.stage1_completed = True
                        save_progress()
                        st.success("Stage 1 completed successfully!")
                        st.rerun()
                    else:
                        st.error("Incorrect answer. Please try again.")
            else:
                st.success("Stage 1 completed ✅")

        st.write("---")

        st.header("Stage 2: Signalling & Hardware Fundamentals")

        if not st.session_state.stage1_completed:
            st.info("This stage is locked. Complete Stage 1 first.")
        else:
            st.write("""
This stage introduces:
- Signalling basics
- Hardware concepts
- Interfaces and system components
- General hardware application principles
""")

            with st.expander("Open Stage 2 Content"):
                st.write("Here you can later add:")
                st.write("- Hardware training files")
                st.write("- Fundamentals videos")
                st.write("- Engineering articles")
                st.write("- Department presentations")

            if not st.session_state.stage2_completed:
                st.subheader("Stage 2 Quiz")
                q2 = st.radio(
                    "What is the goal of hardware fundamentals training?",
                    [
                        "Understand technical system components",
                        "Learn graphic design",
                        "Manage cafeteria operations"
                    ],
                    key="q2"
                )

                if st.button("Submit Stage 2 Quiz", use_container_width=True, key="submit_stage2"):
                    if q2 == "Understand technical system components":
                        st.session_state.stage2_completed = True
                        save_progress()
                        st.success("Stage 2 completed successfully!")
                        st.rerun()
                    else:
                        st.error("Incorrect answer. Please try again.")
            else:
                st.success("Stage 2 completed ✅")

        st.write("---")

        st.header("Stage 3: Choose Your Specialization")

        if not st.session_state.stage2_completed:
            st.info("This stage is locked. Complete Stage 2 first.")
        else:
            st.write("Select the technical path you want to explore:")

            selected = st.selectbox(
                "Choose your path",
                ["", "Pedals", "OBC", "Cable Chassis", "HVITC"],
                index=0,
                key="specialization_select"
            )

            if st.button("Confirm Specialization", use_container_width=True, key="confirm_specialization"):
                if selected:
                    st.session_state.selected_path = selected
                    save_progress()
                    st.success(f"Specialization selected: {selected}")
                    st.rerun()
                else:
                    st.error("Please choose a specialization.")

            if st.session_state.selected_path:
                st.success(f"Selected Path: {st.session_state.selected_path} ✅")

# ---------------------------------------------------
# Profile Page
# ---------------------------------------------------
elif st.session_state.current_page == "profile":
    if not st.session_state.logged_in:
        st.warning("Please login first.")
        if st.button("Go to Login", key="profile_go_to_login"):
            go_to("auth")
            st.rerun()
    else:
        if st.button("← Back to Learning", key="profile_back_learning"):
            go_to("learning")
            st.rerun()

        st.title("My Profile")

        progress = calculate_progress()

        st.write(f"**Name:** {st.session_state.user_name}")
        st.write(f"**Email:** {st.session_state.user_email}")
        st.write(f"**Stage 1 Completed:** {'Yes' if st.session_state.stage1_completed else 'No'}")
        st.write(f"**Stage 2 Completed:** {'Yes' if st.session_state.stage2_completed else 'No'}")
        st.write(f"**Selected Path:** {st.session_state.selected_path if st.session_state.selected_path else 'Not selected'}")
        st.write(f"**Overall Progress:** {progress}%")

        st.write("---")
        st.subheader("Mandatory Trainings")

        st.write(f"**Mandatory Trainings Completed:** {'Yes' if st.session_state.mandatory_completed else 'No'}")

        for i, course in enumerate(MANDATORY_COURSES, start=1):
            status = "Yes" if st.session_state[course["key"]] else "No"
            st.write(f"**Course {i}: {course['title']}** — {status}")

        st.progress(progress / 100)