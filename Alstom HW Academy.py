import streamlit as st
from PIL import Image
from supabase import create_client, Client


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
DEFAULTS = {
    "logged_in": False,
    "user_id": "",
    "user_name": "",
    "user_email": "",
    "stage1_completed": False,
    "stage2_completed": False,
    "selected_path": "",
    "current_page": "landing"
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------------------------------------------
# Supabase Connection
# ---------------------------------------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_ANON_KEY = st.secrets["SUPABASE_ANON_KEY"]
SUPABASE_SERVICE_ROLE_KEY = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]

supabase_auth: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


# ---------------------------------------------------
# Helper Functions
# ---------------------------------------------------
def go_to(page_name: str):
    st.session_state.current_page = page_name


def reset_session():
    for key, value in DEFAULTS.items():
        st.session_state[key] = value


def logout():
    reset_session()


def calculate_progress():
    progress = 0
    if st.session_state.stage1_completed:
        progress += 40
    if st.session_state.stage2_completed:
        progress += 40
    if st.session_state.selected_path:
        progress += 20
    return progress


def resize_image_to_height(image_path, target_height=320):
    img = Image.open(image_path)
    width, height = img.size
    new_width = int((target_height / height) * width)
    return img.resize((new_width, target_height))


def ensure_profile_exists(user_id, full_name, email):
    existing = supabase_admin.table("profiles").select("id").eq("id", user_id).execute()
    if not existing.data:
        supabase_admin.table("profiles").insert({
            "id": user_id,
            "full_name": full_name,
            "email": email
        }).execute()


def ensure_user_progress_exists(user_id):
    existing = supabase_admin.table("user_progress").select("user_id").eq("user_id", user_id).execute()
    if not existing.data:
        supabase_admin.table("user_progress").insert({
            "user_id": user_id,
            "stage1_completed": False,
            "stage2_completed": False,
            "selected_path": "",
            "progress_percent": 0
        }).execute()


def load_user_data(user):
    st.session_state.logged_in = True
    st.session_state.user_id = user.id
    st.session_state.user_email = user.email

    guessed_name = user.email.split("@")[0].replace(".", " ").title()
    ensure_profile_exists(user.id, guessed_name, user.email)
    ensure_user_progress_exists(user.id)

    profile_res = supabase_admin.table("profiles").select("*").eq("id", user.id).execute()
    if profile_res.data:
        profile = profile_res.data[0]
        st.session_state.user_name = profile.get("full_name", guessed_name)
    else:
        st.session_state.user_name = guessed_name

    progress_res = supabase_admin.table("user_progress").select("*").eq("user_id", user.id).execute()
    if progress_res.data:
        progress_data = progress_res.data[0]
        st.session_state.stage1_completed = progress_data.get("stage1_completed", False)
        st.session_state.stage2_completed = progress_data.get("stage2_completed", False)
        st.session_state.selected_path = progress_data.get("selected_path", "")
    else:
        st.session_state.stage1_completed = False
        st.session_state.stage2_completed = False
        st.session_state.selected_path = ""


def save_progress():
    progress = calculate_progress()
    supabase_admin.table("user_progress").upsert(
        {
            "user_id": st.session_state.user_id,
            "stage1_completed": st.session_state.stage1_completed,
            "stage2_completed": st.session_state.stage2_completed,
            "selected_path": st.session_state.selected_path,
            "progress_percent": progress
        },
        on_conflict="user_id"
    ).execute()


def show_logo():
    try:
        st.image("alstom_logo.png", width=180)
    except Exception:
        st.markdown("## **ALSTOM**")
    st.caption("Alstom Hardware Academy")


# ---------------------------------------------------
# Global Style
# ---------------------------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #F5F5F7;
}

.main {
    background-color: #F5F5F7;
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
    padding-top: 18px;
    font-size: 16px;
    color: #374151;
}

.footer-text {
    text-align:center;
    color:#6B7280;
    font-size:15px;
    padding-bottom:10px;
}

.top-navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 6px 18px 6px;
}

.top-navbar-left {
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.top-navbar-center {
    display: flex;
    align-items: center;
    gap: 34px;
    font-size: 17px;
    font-weight: 700;
    color: #1F2937;
}

.top-navbar-right {
    display: flex;
    gap: 14px;
    align-items: center;
}

.logo-subtitle {
    color: #6B7280;
    font-size: 15px;
    margin-top: 4px;
}

            .header-wrapper {
    background-color: white;
    padding: 18px 26px;
    border-radius: 0 0 18px 18px;
    margin: -1rem -1rem 28px -1rem;
    border-bottom: 1px solid #E5E7EB;
}

.footer-wrapper {
    background-color: white;
    padding: 24px 20px 14px 20px;
    margin: 30px -1rem -1rem -1rem;
    border-top: 1px solid #E5E7EB;
}
            
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# Landing Page
# ---------------------------------------------------
if st.session_state.current_page == "landing":
    st.markdown('<div class="top-header-area">', unsafe_allow_html=True)

    nav1, nav2, nav3 = st.columns([2.2, 3.2, 2])

    with nav1:
        try:
            st.image("alstom_logo.png", width=180)
        except:
            st.markdown("## **ALSTOM**")
        st.markdown('<div class="logo-subtitle">Alstom Hardware Academy</div>', unsafe_allow_html=True)

    with nav2:
        st.markdown("""
        <div class="top-navbar-center">
            <span>Explore</span>
            <span>Learning Journey</span>
            <span>Specializations</span>
            <span>About</span>
        </div>
        """, unsafe_allow_html=True)

    with nav3:
        btn1, btn2 = st.columns(2)
        with btn1:
            if st.button("Log in", use_container_width=True, key="landing_login"):
                go_to("auth")
                st.rerun()
        with btn2:
            if st.button("Join Now", use_container_width=True, key="landing_join"):
                go_to("auth")
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

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

    st.markdown("## Key Highlights")
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

    st.markdown("## Vision, Mission & Values")
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

    st.markdown("## Explore Learning Areas")
    st.write("Discover the main learning tracks included in Alstom Hardware Academy.")

    card1, card2 = st.columns(2)

    with card1:
        st.markdown('<div class="learning-card">', unsafe_allow_html=True)
        try:
            img1 = resize_image_to_height("railway_system.jpg", 320)
            st.image(img1, use_container_width=True)
        except:
            st.info("Add image: railway_system.jpg")

        st.markdown("""
        <div class="learning-card-body">
            <div class="learning-card-title">Railway System</div>
            <div class="learning-card-text">
                Build a high-level understanding of railway systems, infrastructure, rolling stock, power, telecom, and railway operations.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with card2:
        st.markdown('<div class="learning-card">', unsafe_allow_html=True)
        try:
            img2 = resize_image_to_height("specialized_paths.jpg", 320)
            st.image(img2, use_container_width=True)
        except:
            st.info("Add image: specialized_paths.jpg")

        st.markdown("""
        <div class="learning-card-body">
            <div class="learning-card-title">Specialized Paths</div>
            <div class="learning-card-text">
                Move into focused technical areas such as Pedals, OBC, Cable Chassis, and HVITC based on your role and learning goals.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    card3, card4 = st.columns(2)

    with card3:
        st.markdown('<div class="learning-card">', unsafe_allow_html=True)
        try:
            img3 = resize_image_to_height("signalling_hardware.jpg", 320)
            st.image(img3, use_container_width=True)
        except:
            st.info("Add image: signalling_hardware.jpg")

        st.markdown("""
        <div class="learning-card-body">
            <div class="learning-card-title">Signalling & Hardware Fundamentals</div>
            <div class="learning-card-text">
                Learn key hardware concepts, system interfaces, signalling basics, component understanding, and engineering principles.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with card4:
        st.markdown('<div class="learning-card">', unsafe_allow_html=True)
        try:
            img4 = resize_image_to_height("progress_tracking.jpg", 320)
            st.image(img4, use_container_width=True)
        except:
            st.info("Add image: progress_tracking.jpg")

        st.markdown("""
        <div class="footer-wrapper">
            <hr style="margin-top:0px; margin-bottom:12px;">
            <div class="footer-text">
                <strong>Alstom Hardware Academy Platform</strong><br>
                Built to support onboarding, technical learning, and knowledge development for hardware engineers at Alstom.
            </div>
        </div>
        """, unsafe_allow_html=True)

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
    show_logo()
    st.write("")

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
                            load_user_data(user)
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
                        auth_response = supabase_auth.auth.sign_up({
                            "email": signup_email,
                            "password": password
                        })

                        user = auth_response.user

                        if user is not None:
                            ensure_profile_exists(user.id, full_name, signup_email)
                            ensure_user_progress_exists(user.id)
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
            show_logo()

        with top3:
            if st.button("Logout", use_container_width=True, key="home_logout"):
                logout()
                st.rerun()

        st.title(f"Welcome, {st.session_state.user_name} 👋")

        progress = calculate_progress()
        st.write("## Your Progress")
        st.progress(progress / 100)
        st.write(f"Progress: **{progress}%**")

        st.write("---")

        col1, col2 = st.columns([1.4, 1])

        with col1:
            st.markdown("## About Alstom")
            st.write("""
Alstom is a global leader in smart and sustainable mobility.

Alstom Hardware Academy supports your onboarding journey through:
1. **Railway System**
2. **Signalling & Hardware Fundamentals**
3. **Specialized Technical Path**
""")

        with col2:
            st.markdown("## Next Step")
            if progress == 0:
                st.info("You have not started your learning journey yet.")
            elif progress < 100:
                st.info("Continue your learning journey.")
            else:
                st.success("You completed all stages!")

            if st.button("Go to Learning Journey", use_container_width=True, key="home_learning_journey"):
                go_to("learning")
                st.rerun()


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

        st.progress(progress / 100)