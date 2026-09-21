import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st
from PIL import Image
from supabase import create_client, Client
import streamlit as st
from PIL import Image
import streamlit.components.v1 as components

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(
    page_title="Alstom Hardware & Installation Academy",
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
    "stage1_quiz_submitted": False,
    "stage1_submitted_answers": [],
    "stage1_quiz_score": 0,
    "stage1_quiz_completed": False,
    "stage1_current_item": 0,
    "stage1_completed": False,
    "stage2_doc1_completed": False,
    "stage2_doc2_completed": False,
    "stage2_quiz_submitted": False,
    "stage2_submitted_answers": [],
    "stage2_quiz_score": 0,
    "stage2_quiz_completed": False,
    "stage2_current_item": 0,
    "stage2_completed": False,
    "selected_path": "",
    "pedal_doc_completed": False,
    "pedal_quiz_submitted": False,
    "pedal_submitted_answers": [],
    "pedal_quiz_score": 0,
    "pedal_quiz_completed": False,
    "pedal_current_item": 0,
    "hvitc_doc_completed": False,
    "hvitc_quiz_submitted": False,
    "hvitc_submitted_answers": [],
    "hvitc_quiz_score": 0,
    "hvitc_quiz_completed": False,
    "hvitc_current_item": 0,
    "stage3_completed": False,
    "current_page": "landing",

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
    st.session_state.stage1_quiz_submitted = False
    st.session_state.stage1_quiz_score = 0
    st.session_state.stage1_quiz_completed = False
    st.session_state.stage1_submitted_answers = []
    st.session_state.stage1_current_item = 0
    st.session_state.stage1_completed = False
    st.session_state.stage2_doc1_completed = False
    st.session_state.stage2_doc2_completed = False
    st.session_state.stage2_quiz_submitted = False
    st.session_state.stage2_submitted_answers = []
    st.session_state.stage2_quiz_score = 0
    st.session_state.stage2_quiz_completed = False
    st.session_state.stage2_current_item = 0
    st.session_state.stage2_completed = False
    st.session_state.selected_path = ""
    st.session_state.pedal_doc_completed = False
    st.session_state.pedal_quiz_submitted = False
    st.session_state.pedal_submitted_answers = []
    st.session_state.pedal_quiz_score = 0
    st.session_state.pedal_quiz_completed = False
    st.session_state.pedal_current_item = 0
    st.session_state.hvitc_doc_completed = False
    st.session_state.hvitc_quiz_submitted = False
    st.session_state.hvitc_submitted_answers = []
    st.session_state.hvitc_quiz_score = 0
    st.session_state.hvitc_quiz_completed = False
    st.session_state.hvitc_current_item = 0
    st.session_state.stage3_completed = False
    st.session_state.current_page = "landing"

def calculate_progress():
    progress = 0
    if st.session_state.mandatory_completed:
        progress += 20
    if st.session_state.stage1_completed:
        progress += 30
    if st.session_state.stage2_completed:
        progress += 30
    if st.session_state.stage3_completed:
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
            "stage2_doc1_completed": st.session_state.stage2_doc1_completed,
            "stage2_doc2_completed": st.session_state.stage2_doc2_completed,
            "stage2_quiz_completed": st.session_state.stage2_quiz_completed,
            "stage2_completed": st.session_state.stage2_completed,
            "selected_path": st.session_state.selected_path,
            "pedal_doc_completed": st.session_state.pedal_doc_completed,
            "pedal_quiz_completed": st.session_state.pedal_quiz_completed,
            "hvitc_doc_completed": st.session_state.hvitc_doc_completed,
            "hvitc_quiz_completed": st.session_state.hvitc_quiz_completed,
            "stage3_completed": st.session_state.stage3_completed,
            "progress_percent": progress
        },
        on_conflict="user_id"
    ).execute()

def send_email_to_manager(manager_email, subject, body):
    sender_email = st.secrets["SENDER_EMAIL"]
    sender_password = st.secrets["SENDER_APP_PASSWORD"]

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = manager_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        return True
    except Exception as e:
        print("Email sending error:", e)
        return False

def get_email_flags(user_id):
    result = supabase_admin.table("user_progress").select(
        "mandatory_email_sent, stage1_email_sent, stage2_email_sent, full_completion_email_sent"
    ).eq("user_id", user_id).execute()

    if result.data:
        return result.data[0]

    return {
        "mandatory_email_sent": False,
        "stage1_email_sent": False,
        "stage2_email_sent": False,
        "full_completion_email_sent": False
    }

def mark_email_flag_as_sent(user_id, flag_name):
    supabase_admin.table("user_progress").update({
        flag_name: True
    }).eq("user_id", user_id).execute()

def check_and_send_milestone_emails():
    user_id = st.session_state.user_id

    if not user_id:
        return

    profile_res = supabase_admin.table("profiles").select("*").eq("id", user_id).execute()
    if not profile_res.data:
        return

    profile_data = profile_res.data[0]
    user_name = profile_data.get("full_name", "")
    manager_name = profile_data.get("manager_name", "")
    manager_email = profile_data.get("manager_email", "")

    if not manager_email:
        return

    email_flags = get_email_flags(user_id)

    # 1) Mandatory completed email
    if st.session_state.mandatory_completed and not email_flags.get("mandatory_email_sent", False):
        subject = "Mandatory Trainings Completion Notification"
        body = f"""
Hello {manager_name},

This is to inform you that {user_name} has successfully completed the Mandatory Trainings in the Alstom Hardware & Installation Academy journey.

Best regards,
Alstom Hardware & Installation Academy
"""
        sent = send_email_to_manager(manager_email, subject, body)
        if sent:
            mark_email_flag_as_sent(user_id, "mandatory_email_sent")

    # 2) Stage 1 completed email
    if st.session_state.stage1_completed and not email_flags.get("stage1_email_sent", False):
        subject = "Stage 1 Completion Notification"
        body = f"""
Hello {manager_name},

This is to inform you that {user_name} has successfully completed Stage 1: Railway System in the Alstom Hardware & Installation Academy journey.

Best regards,
Alstom Hardware & Installation Academy
"""
        sent = send_email_to_manager(manager_email, subject, body)
        if sent:
            mark_email_flag_as_sent(user_id, "stage1_email_sent")

    # 3) Stage 2 completed email
    if st.session_state.stage2_completed and not email_flags.get("stage2_email_sent", False):
        subject = "Stage 2 Completion Notification"
        body = f"""
Hello {manager_name},

This is to inform you that {user_name} has successfully completed Stage 2: Signalling & Hardware in the Alstom Hardware & Installation Academy journey.

Best regards,
Alstom Hardware & Installation Academy
"""
        sent = send_email_to_manager(manager_email, subject, body)
        if sent:
            mark_email_flag_as_sent(user_id, "stage2_email_sent")

    # 4) Full training completion email
    if is_training_fully_completed() and not email_flags.get("full_completion_email_sent", False):
        subject = "Full Training Completion Notification"
        body = f"""
Hello {manager_name},

This is to inform you that {user_name} has successfully completed the Alstom Hardware & Installation Academy training journey.

Best regards,
Alstom Hardware & Installation Academy
"""
        sent = send_email_to_manager(manager_email, subject, body)
        if sent:
            mark_email_flag_as_sent(user_id, "full_completion_email_sent")
   
def is_training_fully_completed():
    return (
        st.session_state.mandatory_completed
        and st.session_state.stage1_completed
        and st.session_state.stage2_completed
        and bool(st.session_state.selected_path)
    )

def resize_and_crop_image(image_path, target_width=320, target_height=180):
    img = Image.open(image_path)
    width, height = img.size

    target_ratio = target_width / target_height
    image_ratio = width / height

    if image_ratio > target_ratio:
        # Image is wider than target → crop sides
        new_height = target_height
        new_width = int(new_height * image_ratio)
    else:
        # Image is taller than target → crop top/bottom
        new_width = target_width
        new_height = int(new_width / image_ratio)

    img = img.resize((new_width, new_height))

    left = (new_width - target_width) / 2
    top = (new_height - target_height) / 2
    right = left + target_width
    bottom = top + target_height

    img = img.crop((left, top, right, bottom))
    return img

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
        "image": "mandatory_2.jpg",
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

MANAGERS = [
    {
        "name": "Yusuf BASEGMEZ",
        "email": "yusuf.basegmez@alstomgroup.com"
    },
    {
        "name": "Mohammed Ibrahim AbdelShafy",
        "email": "mohammed.abdelshafy@alstomgroup.com"
    },
    {
        "name": "Kubra Eker",
        "email": "kubra.eker@alstomgroup.com"
    },
    {
        "name": "Sirrican Karadogan",
        "email": "sirrican.karadogan@alstomgroup.com"
    },
    {
        "name": "Diaa Eldin Salah",
        "email": "diaa-eldin.salah@alstomgroup.com"
    },
    {
        "name": "Diaa ElDin Reda",
        "email": "diaa-eldin.reda@alstomgroup.com"
    },
    {
        "name": "Burak Bingol",
        "email": "burak.bingol@alstomgroup.com"
    },
    {
        "name": "Ahmet KILICARSLAN",
        "email": "ahmet.kilicarslan@alstomgroup.com"
    },
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

STAGE1_QUIZ_QUESTIONS = [
    {
        "question": "What is the most important rule regarding railway safety?",
        "options": [
            "Trains must follow the timetable exactly",
            "Trains must not exceed speed limits",
            "Two trains must not occupy the same position on the track at the same time",
            "Drivers must always operate manually"
        ],
        "answer": "Two trains must not occupy the same position on the track at the same time"
    },
    {
        "question": "Which of the following is NOT one of the five reasons for railway signalling mentioned in the training?",
        "options": [
            "Traffic management",
            "Rear-end collision prevention",
            "Head-on collision prevention",
            "Fuel consumption reduction"
        ],
        "answer": "Fuel consumption reduction"
    },
    {
        "question": "Before a route can be released for train movement, which condition must be ensured?",
        "options": [
            "The train schedule is approved",
            "The route is free and points are set, locked, and detected",
            "The station manager authorizes it manually",
            "The train speed is below 40 km/h"
        ],
        "answer": "The route is free and points are set, locked, and detected"
    },
    {
        "question": "What is the main limitation of axle counters highlighted in the presentation?",
        "options": [
            "They require insulated rail joints",
            "They consume high power",
            "They do not detect broken rails",
            "They cannot be used on bridges"
        ],
        "answer": "They do not detect broken rails"
    },
    {
        "question": "Which type of level crossing is described as the most widespread?",
        "options": [
            "SAL0",
            "SAL2",
            "SAL2B",
            "SAL4"
        ],
        "answer": "SAL2"
    },
    {
        "question": "The point equipment includes which three functions?",
        "options": [
            "Detection, communication, supervision",
            "Actuation, locking, detection",
            "Power supply, actuation, signalling",
            "Switching, routing, braking"
        ],
        "answer": "Actuation, locking, detection"
    },
    {
        "question": "What is the definition of headway?",
        "options": [
            "The distance between two stations",
            "The braking distance of a train",
            "The time interval between two following trains",
            "The distance between two signals"
        ],
        "answer": "The time interval between two following trains"
    },
    {
        "question": "Within Automatic Train Control (ATC), what is the primary role of ATP?",
        "options": [
            "Drives the train automatically",
            "Supervises train speed and applies protection",
            "Plans timetables",
            "Controls interlocking routes"
        ],
        "answer": "Supervises train speed and applies protection"
    },
    {
        "question": "What does ATS stand for?",
        "options": [
            "Automatic Train Safety",
            "Automatic Track Supervision",
            "Automatic Train Supervision",
            "Automatic Transit Signalling"
        ],
        "answer": "Automatic Train Supervision"
    },
    {
        "question": "According to the fail-safe principle, when a predictable signalling equipment failure occurs, the system should move to:",
        "options": [
            "A less restrictive condition",
            "A manual operating mode only",
            "A more restrictive safe condition",
            "A higher-performance mode"
        ],
        "answer": "A more restrictive safe condition"
    }
]

STAGE2_ITEMS = [
    {
        "title": "Railway Signalling Overview",
        "type": "External Course",
        "duration": "3 Hours",
        "description": "This course introduces the basics of railway signalling, including how signalling works, the main challenges involved, and the core technologies used in railway signalling systems.",
        "key": "stage2_doc1_completed"
    },
    {
        "title": "D&IS Technical Onboarding: Core Technology Introduction",
        "type": "External Course",
        "duration": "47 min",
        "description": "This course provides an introduction to Core Technology within Alstom, including organization, ways of working, technology systems, governance, and the main platforms and products used in railway signalling.",
        "key": "stage2_doc2_completed"
    },
    {
        "title": "Stage 2 Quiz",
        "type": "Assessment",
        "duration": "10–15 min",
        "description": "Complete the quiz after finishing both courses to validate your understanding and unlock the next stage.",
        "key": "stage2_quiz_completed"
    }
]

STAGE2_QUIZ_QUESTIONS = [
    {
        "question": "What is the main function of the BSI004 board?",
        "options": [
            "Power conversion",
            "Fuse protection",
            "Surge protection for detector cables",
            "Train speed monitoring"
        ],
        "answer": "Surge protection for detector cables"
    },
    {
        "question": "What does HVITC stand for?",
        "options": [
            "High Voltage Integrated Track Controller",
            "High Voltage Impulse Track Circuit",
            "High Velocity Impulse Track Circuit",
            "High Voltage Interlocking Track Circuit"
        ],
        "answer": "High Voltage Impulse Track Circuit"
    },
    {
        "question": "Which IMC063 configuration uses the Negative Detection Philosophy?",
        "options": [
            "DA/EP",
            "AxF/PA",
            "CCM-E",
            "SIC999"
        ],
        "answer": "AxF/PA"
    },
    {
        "question": "Which HVITC component generates high-voltage impulses and injects them into the rails?",
        "options": [
            "RUTA",
            "Impedance Bond",
            "EMZ",
            "CCM-E"
        ],
        "answer": "EMZ"
    },
    {
        "question": "Which cable type provides the 24VDC supply from SIC999 to IMC063?",
        "options": [
            "MAN0125300",
            "MAN0125600",
            "MAN0125700",
            "MAN0125800"
        ],
        "answer": "MAN0125700"
    },
    {
        "question": "The HVITC receiver (RUTA) checks:",
        "options": [
            "Pulse polarity, energy, and frequency",
            "Axle count only",
            "Train speed only",
            "Signal lamp status"
        ],
        "answer": "Pulse polarity, energy, and frequency"
    },
    {
        "question": "In the Pedal Cabinet layout, the BSI004 cards are installed at:",
        "options": [
            "+F2",
            "+F7",
            "+F9",
            "+F13"
        ],
        "answer": "+F13"
    },
    {
        "question": "What happens if an HVITC signal disappears or becomes distorted?",
        "options": [
            "The transmitter resets automatically",
            "The track relay drops",
            "The receiver increases sensitivity",
            "Nothing changes"
        ],
        "answer": "The track relay drops"
    },
    {
        "question": "How many IMC063 cards can one SIC Board protect?",
        "options": [
            "4",
            "6",
            "8",
            "10"
        ],
        "answer": "6"
    },
    {
        "question": "What is the maximum distance between the transmitter and the Impedance Bond when transmission and reception use different cables?",
        "options": [
            "1000 m",
            "1500 m",
            "2000 m",
            "2500 m"
        ],
        "answer": "2000 m"
    }
]

PEDAL_ITEMS = [
    {
        "key": "pedal_doc_completed",
        "title": "Pedal Presentation",
        "type": "PowerPoint",
        "duration": "Self-paced",
        "description": "Study the Pedal presentation before proceeding to the quiz.",
        "file": "pedal_presentation.pptx"
    },
    {
        "key": "pedal_quiz_completed",
        "title": "Pedal Quiz",
        "type": "Quiz",
        "duration": "Short assessment",
        "description": "Complete the quiz based on the Pedal presentation.",
        "file": ""
    }
]

PEDAL_QUIZ_QUESTIONS = [
    {
        "question": "What is the primary role of a Pedal Cabinet in a railway signaling system?",
        "options": [
            "Train propulsion control",
            "Passenger information management",
            "Interface between field detection devices and the signaling/control system",
            "Communication with the driver's cabin"
        ],
        "answer": "Interface between field detection devices and the signaling/control system"
    },
    {
        "question": "Which board sends different axle counter states to the CCM-E controller according to train detection status?",
        "options": [
            "SIC Board",
            "BSI004 Board",
            "IMC063 Evaluation Board",
            "Rectifier Unit"
        ],
        "answer": "IMC063 Evaluation Board"
    },
    {
        "question": "What is the main function of the BSI004 board?",
        "options": [
            "Power conversion from AC to DC",
            "Fuse protection",
            "Surge protection for detector cables",
            "Train direction calculation"
        ],
        "answer": "Surge protection for detector cables"
    },
    {
        "question": "In the Pedal Cabinet, which cable type is used for power distribution from the SIC999 Board to the IMC063 Evaluation Board?",
        "options": [
            "MAN0125300",
            "MAN0125600",
            "MAN0125700",
            "MAN0125800"
        ],
        "answer": "MAN0125700"
    },
    {
        "question": "Which detection philosophy is associated with the DA/EP configuration?",
        "options": [
            "Negative Detection Philosophy",
            "Positive Detection Philosophy",
            "Predictive Detection Philosophy",
            "Dynamic Detection Philosophy"
        ],
        "answer": "Positive Detection Philosophy"
    }
]

HVITC_ITEMS = [
    {
        "key": "hvitc_doc_completed",
        "title": "HVITC Presentation",
        "type": "PowerPoint",
        "duration": "Self-paced",
        "description": "Study the HVITC presentation before proceeding to the quiz.",
        "file": "hvitc_presentation.pptx"
    },
    {
        "key": "hvitc_quiz_completed",
        "title": "HVITC Quiz",
        "type": "Quiz",
        "duration": "Short assessment",
        "description": "Complete the quiz based on the HVITC presentation.",
        "file": ""
    }
]

HVITC_QUIZ_QUESTIONS = [
    {
        "question": "What does HVITC stand for?",
        "options": [
            "High Voltage Integrated Track Controller",
            "High Voltage Impulse Track Circuit",
            "High Voltage Internal Track Circuit",
            "Heavy Voltage Impulse Traction Circuit"
        ],
        "answer": "High Voltage Impulse Track Circuit"
    },
    {
        "question": "Which of the following is NOT a function of the HVITC system?",
        "options": [
            "Detect train occupancy",
            "Prove track vacancy",
            "Control train speed",
            "Detect broken rail conditions"
        ],
        "answer": "Control train speed"
    },
    {
        "question": "What are the three parameters checked by the RUTA receiver?",
        "options": [
            "Voltage, current, and resistance",
            "Pulse polarity, pulse energy, and pulse frequency",
            "Temperature, voltage, and frequency",
            "Track length, polarity, and speed"
        ],
        "answer": "Pulse polarity, pulse energy, and pulse frequency"
    },
    {
        "question": "What is the primary function of the Impedance Bond (CI/CIT 1000 CT3)?",
        "options": [
            "Generate track impulses",
            "Protect against lightning strikes",
            "Pass traction return current while allowing HVITC signaling pulses to pass",
            "Convert AC power to DC power"
        ],
        "answer": "Pass traction return current while allowing HVITC signaling pulses to pass"
    },
    {
        "question": "Why is return current continuity important in railway systems?",
        "options": [
            "It increases train speed.",
            "It closes the electrical traction circuit and ensures safe current return.",
            "It powers the station lighting system.",
            "It controls signal aspects."
        ],
        "answer": "It closes the electrical traction circuit and ensures safe current return."
    }
]

ALSTOM_TOOLS = [
    {
        "title": "Hydra",
        "description": "An internal Alstom platform that can support engineering and project-related workflows.",
        "image": "hydra_tool.jpg",
        "tool_link": "https://hydra.bt.bombardier.net/hydra/Client/",
        "learning_link": "https://example.com/hydra-learning"
    },
    {
        "title": "Orchestra",
        "description": "A useful internal platform that may help users navigate project and collaboration activities.",
        "image": "orchestra_tool.png",
        "tool_link": "https://datamanagement.alstom.com/ebx-ui/ui/custom/Public_Master_Data/action/378",
        "learning_link": "https://alstomgroup.sharepoint.com/sites/My_Data_Journey/SitePages/Your-very-first-steps-in-Orchestra.aspx"
    },
    {
        "title": "DOC4A",
        "description": "A document-related internal platform that can help users access technical references and documentation.",
        "image": "doc4a_tool.png",
        "tool_link": "https://alstomgroup.sharepoint.com/sites/DOC4A",
        "learning_link": "https://example.com/doc4a-learning"
    },
    {
        "title": "PLM",
        "description": "Access the PLM platform and related engineering resources.",
        "image": "plm.jpg",
        "tool_link": "https://plm.alstom.hub/enovia/common/emxNavigator.jsp",
        "learning_link": "https://example.com/doc4a-learning"
    },
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
    font-size: 36px;
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

.stage-page-hero {
    background: linear-gradient(90deg, #0B3D91 0%, #123E8C 100%);
    padding: 34px 32px;
    border-radius: 20px;
    color: white;
    margin-bottom: 22px;
}

.stage-page-hero-title {
    font-size: 34px;
    font-weight: 700;
    margin-bottom: 10px;
    color: white;
}

.stage-page-hero-text {
    font-size: 17px;
    color: #E5E7EB;
    line-height: 1.75;
}

.stage-sidebar-box {
    background-color: white;
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
    margin-bottom: 16px;
}

.stage-main-box {
    background-color: white;
    border: 1px solid #E5E7EB;
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
    margin-bottom: 18px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Landing Page
# ---------------------------------------------------
if st.session_state.current_page == "landing":

    nav1, nav2 = st.columns([1.4, 1])

    with nav1:
        try:
            st.image("alstom_logo.png", width=180)
            st.caption("Alstom Hardware & Installation Academy")
        except:
            st.markdown("## **ALSTOM**")
            st.caption("Alstom Hardware & Installation Academy")

    with nav2:
        space, b1, b2 = st.columns([1.2, 1, 1])
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
        <div class="main-title">A structured onboarding and learning journey for new hardware and installation engineers</div>
        <div class="hero-text">
            Alstom Hardware and Installation Academy is designed to support newly joined engineers with a guided learning experience,
            starting from company introduction and railway system fundamentals, moving into signalling and hardware basics,
            and finally leading into specialized technical paths and practical learning areas such as Pedals, OBC, HVITC, Cable Chassis, and other relevant engineering tools and references.
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
            <p style="font-size:15px; font-weight:700;">Structured onboarding flow</p>
        </div>
        """, unsafe_allow_html=True)

    with s2:
        st.markdown("""
        <div class="stats-box">
            <h2 style="color:#0B3D91; font-size:48px; margin-bottom:8px;">4</h2>
            <p style="font-size:15px; font-weight:700;">Core onboarding stages</p>
        </div>
        """, unsafe_allow_html=True)

    with s3:
        st.markdown("""
        <div class="stats-box">
            <h2 style="color:#0B3D91; font-size:48px; margin-bottom:8px;">1</h2>
            <p style="font-size:15px; font-weight:700;">Centralized learning platform</p>
        </div>
        """, unsafe_allow_html=True)

    with s4:
        st.markdown("""
        <div class="stats-box">
            <h2 style="color:#0B3D91; font-size:48px; margin-bottom:8px;">∞</h2>
            <p style="font-size:15px; font-weight:700;">Continuous learning potential</p>
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
                New engineers often face scattered resources and inconsistent onboarding. Alstom Hardware and Installation Academy gives each newcomer
                a guided learning flow, clear stages, and measurable progress toward technical readiness.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 5. About Alstom
    st.markdown("""
    <div class="section-box">
        <div class="section-title">About Alstom</div>
        <div class="section-text">
            Alstom is a global leader in smart and sustainable mobility, with a strong presence across the railway and transportation sector.
            The company designs, develops, and delivers a wide range of integrated solutions including signaling, infrastructure, rolling stock,
            digital systems, services, and maintenance support.
            <br><br>
            With operations and expertise spread across many countries, Alstom plays a major role in shaping the future of safer,
            smarter, and more sustainable transportation. Its long-standing industry experience, technical excellence, and innovation-driven
            approach make it one of the leading organizations in modern mobility worldwide.
            <br><br>
            For engineers, Alstom represents a professional environment where technology, collaboration, safety, and continuous improvement
            are deeply connected to real-world transportation impact.
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

    # 8. Explore Learning Areas
    st.markdown('<h2 style="color:#1F3552; font-weight:700;">Explore Learning Areas</h2>', unsafe_allow_html=True)
    st.write("Discover the main learning areas, specialization paths, and useful internal references included in Alstom Hardware and Installation Academy.")

    # Row 1
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
            img2 = Image.open("signalling_hardware.jpg")
            st.image(img2, use_container_width=True)
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

    # Row 2
    card3, card4 = st.columns(2)

    with card3:
        try:
            img3 = resize_image_to_height("specialized_paths.jpg", 320)
            st.image(img3, use_container_width=True)
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

    # Row 3 - centered
    left_tool, center_tool, right_tool = st.columns([1, 1.4, 1])

    with center_tool:
        try:
            img5 = resize_image_to_height("alstom_tools.jpg", 320)
            st.image(img5, use_container_width=True)
        except:
            st.info("Add image: alstom_tools.jpg")
        st.markdown("""
        <div style="padding:8px 10px 12px 6px;">
            <h3 style="color:#0B3D91; margin-top:0px; margin-bottom:6px;">Alstom Tools</h3>
            <p style="font-size:16px; color:#374151; line-height:1.55;">
                Discover useful internal tools and platforms such as Hydra, Orchestra, DOC4A, and other references that may support engineering and project activities.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # 9. Why Alstom Hardware and Installation Academy?
    st.markdown("""
    <div class="section-box">
        <div class="section-title">Why Alstom Hardware and Installation Academy?</div>
        <div class="section-text">
            Alstom Hardware and Installation Academy is more than a content repository. It is a guided experience built to reduce confusion,
            improve onboarding quality, and create a shared technical language across newcomers, senior engineers, and managers.
            <br><br>
            Instead of relying only on scattered files or informal support, the platform provides a structured route:
            start with company awareness, continue through railway and hardware fundamentals, validate understanding
            through quizzes, and finally move into role-based specialization.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 10. Final CTA
    st.markdown("""
    <div class="hero-box" style="padding:30px 34px;">
        <div class="section-title" style="color:white;">Start your learning journey today</div>
        <div class="hero-text">
            Join Alstom Hardware and Installation Academy and begin a structured onboarding experience tailored for new hardware and installation engineers.
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

    # 11. Footer
    st.markdown("""
    <hr style="margin-top:28px; margin-bottom:12px;">
    <div class="footer-text">
        <strong>Alstom Hardware and Installation Academy Platform</strong><br>
        Built to support onboarding, technical learning, and knowledge development for hardware and installation engineers at Alstom.
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
    st.caption("Alstom Hardware & Installation Academy")

    st.write("")

    # Full width blue intro box
    st.markdown("""
    <div class="auth-left-box">
        <div class="auth-left-title">Start your onboarding journey with clarity and confidence</div>
        <div class="auth-left-text">
            Alstom Hardware and Installation Academy is designed to give new hardware and installation engineers a clear and structured learning experience.
        </div>
        <div class="auth-left-text">
            Through this platform, you will explore:
            <br>
            • Mandatory Trainings<br>
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
                                st.session_state.stage2_doc1_completed = progress_data.get("stage2_doc1_completed", False)
                                st.session_state.stage2_doc2_completed = progress_data.get("stage2_doc2_completed", False)
                                st.session_state.stage2_quiz_completed = progress_data.get("stage2_quiz_completed", False)
                                st.session_state.stage2_current_item = 0
                                st.session_state.stage2_completed = progress_data.get("stage2_completed", False)
                                st.session_state.selected_path = progress_data.get("selected_path", "")
                                st.session_state.pedal_doc_completed = progress_data.get("pedal_doc_completed", False)
                                st.session_state.pedal_quiz_completed = progress_data.get("pedal_quiz_completed", False)
                                st.session_state.pedal_current_item = 0
                                st.session_state.hvitc_doc_completed = progress_data.get("hvitc_doc_completed", False)
                                st.session_state.hvitc_quiz_completed = progress_data.get("hvitc_quiz_completed", False)
                                st.session_state.hvitc_current_item = 0
                                st.session_state.stage3_completed = progress_data.get("stage3_completed", False)

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

            manager_names = [manager["name"] for manager in MANAGERS]
            selected_manager_name = st.selectbox(
                "Select Your Manager",
                [""] + manager_names,
                index=0,
                key="signup_manager"
            )

            if st.button("Create Account", use_container_width=True, key="auth_create_account"):
                if not full_name or not signup_email or not password or not confirm_password or not selected_manager_name:
                    st.error("Please complete all fields.")
                elif not signup_email.lower().endswith("@alstomgroup.com"):
                    st.error("Sorry, this platform is available for Alstom employees only.")
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
                            selected_manager = next(
                                (manager for manager in MANAGERS if manager["name"] == selected_manager_name),
                                None
                            )

                            manager_email = selected_manager["email"] if selected_manager else ""

                            supabase_admin.table("profiles").insert({
                                "id": user.id,
                                "full_name": full_name,
                                "email": signup_email,
                                "manager_name": selected_manager_name,
                                "manager_email": manager_email
                            }).execute()

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
                                "stage1_doc_completed": False,
                                "stage1_quiz_completed": False,
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
            st.caption("Alstom Hardware & Installation Academy")

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
                Your onboarding journey starts with Mandatory Trainings and continues through three guided technical stages:
                Railway System, Signalling & Hardware Fundamentals, and your final Specialization path.
                Follow the journey step by step to build your knowledge, track your progress, and complete your onboarding experience.
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
                Alstom Hardware and Installation Academy is designed to make onboarding clearer, faster, and more structured.
                Instead of navigating scattered documents, you will move through a defined learning path,
                starting with Mandatory Trainings, then continuing through railway system knowledge, hardware fundamentals, and finally your technical specialization.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Stage cards title
        st.markdown('<h2 style="color:#1F3552; font-weight:700;">Your Learning Journey</h2>', unsafe_allow_html=True)
        st.write("Start with the Mandatory Trainings, continue through the three technical stages, and explore optional Alstom Tools when needed.")

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

            if st.button(
                "Enter Stage 2",
                use_container_width=True,
                key="open_stage2",
                disabled=not st.session_state.stage1_completed
            ):
                go_to("stage2")
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

            if st.button(
                "Enter Stage 3",
                use_container_width=True,
                key="open_stage3",
                disabled=not st.session_state.stage2_completed
            ):
                go_to("stage3")
                st.rerun()

        # Row 3 - Alstom Tools
        left_tools, center_tools, right_tools = st.columns([1, 1.2, 1])

        with center_tools:
            st.markdown("""
            <div class="stage-card">
                <div class="stage-badge-current">Optional</div>
                <div class="stage-card-title">Alstom Tools</div>
                <div class="stage-card-text">
                    Explore useful Alstom tools and internal platforms such as Hydra, Orchestra, DOC4A,
                    and other helpful engineering references.
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Open Alstom Tools", use_container_width=True, key="open_alstom_tools"):
                go_to("alstom_tools")
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
                    except Exception:
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
                            check_and_send_milestone_emails()
                            st.rerun()
                    else:
                        st.button("Completed", use_container_width=True, key=f'done_{course["key"]}', disabled=True)

            st.write("")

        st.write("")

        if st.session_state.mandatory_completed:
            st.success("You can now proceed to Stage 1 ✅")

            if st.session_state.mandatory_completed:
                if st.button("Go to Stage 1", use_container_width=True, key="mandatory_go_stage1"):
                    go_to("stage1")
                    st.rerun()
            else:
                st.info("Complete all mandatory trainings to unlock Stage 1.")
                st.button("Go to Stage 1", use_container_width=True, key="mandatory_go_stage1_disabled", disabled=True)


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

        st.markdown("""
        <div class="stage-page-hero">
            <div class="stage-page-hero-title">Stage 1: Railway System</div>
            <div class="stage-page-hero-text">
                Build a foundational understanding of railway systems, infrastructure, rolling stock,
                power systems, and the wider railway ecosystem before moving forward in your technical journey.
            </div>
        </div>
        """, unsafe_allow_html=True)

        progress = calculate_progress()
        st.markdown(f"### Progress: {progress}%")
        st.progress(progress / 100)
        st.write("")

        if not st.session_state.mandatory_completed:
            st.info("This stage is locked. Complete Mandatory Trainings first.")
        else:
            if st.session_state.stage1_current_item not in [0, 1]:
                st.session_state.stage1_current_item = 0

            left_col, right_col = st.columns([0.9, 2.3])

            # -----------------------------
            # Left Sidebar (Display Only)
            # -----------------------------
            with left_col:
                st.markdown("### Stage 1 Content")

                for idx, item in enumerate(STAGE1_ITEMS):
                    completed = st.session_state[item["key"]]
                    is_current = st.session_state.stage1_current_item == idx

                    icon = "✅" if completed else "⬜"

                    if is_current:
                        st.markdown(
                            f"""
                            <div style="
                                background-color:#E8F0FE;
                                border:1px solid #BFDBFE;
                                border-radius:12px;
                                padding:10px 12px;
                                margin-bottom:10px;
                                font-weight:700;
                                color:#1F3552;
                            ">
                                {icon} {item['title']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"""
                            <div style="
                                background-color:white;
                                border:1px solid #E5E7EB;
                                border-radius:12px;
                                padding:10px 12px;
                                margin-bottom:10px;
                                font-weight:500;
                                color:#374151;
                            ">
                                {icon} {item['title']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

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
                                label="Download Railway System Document",
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
                        if st.button("Mark Document as Completed ✅", use_container_width=True, key="stage1_doc_complete"):
                            st.session_state.stage1_doc_completed = True
                            save_progress()
                            st.success("Document marked as completed.")
                            st.rerun()
                    else:
                        st.success("Document completed ✅")

                    st.write("")

                    next_col1, next_col2 = st.columns([1, 2.4])

                    with next_col1:
                        if st.button("Go to Next Item →", use_container_width=True, key="stage1_next_from_doc"):
                            st.session_state.stage1_current_item = 1
                            st.rerun()

                # -------------------------
                # Item 2: Quiz
                # -------------------------
                elif current_index == 1:
                    if not st.session_state.stage1_doc_completed:
                        st.info("Please complete the document first before attempting the quiz.")
                    else:
                        st.subheader("Stage 1 Quiz")

                        user_answers = []

                        for i, q in enumerate(STAGE1_QUIZ_QUESTIONS, start=1):
                            answer = st.radio(
                                f"Q{i}. {q['question']}",
                                q["options"],
                                key=f"stage1_quiz_q{i}"
                            )
                            user_answers.append(answer)

                            if st.session_state.stage1_quiz_submitted and len(st.session_state.stage1_submitted_answers) == len(STAGE1_QUIZ_QUESTIONS):
                                submitted_answer = st.session_state.stage1_submitted_answers[i - 1]

                                if submitted_answer == q["answer"]:
                                    st.success("✅ Correct")
                                else:
                                    st.error("❌ Wrong")

                        if st.button("Submit Quiz ✅", use_container_width=True, key="stage1_submit_quiz_page"):
                            correct_count = 0

                            # save submitted answers snapshot
                            st.session_state.stage1_submitted_answers = user_answers.copy()
                            st.session_state.stage1_quiz_submitted = True

                            for user_answer, q in zip(st.session_state.stage1_submitted_answers, STAGE1_QUIZ_QUESTIONS):
                                if user_answer == q["answer"]:
                                    correct_count += 1

                            total_questions = len(STAGE1_QUIZ_QUESTIONS)
                            required_score = int(total_questions * 0.8)

                            st.session_state.stage1_quiz_score = correct_count

                            if correct_count >= required_score:
                                st.session_state.stage1_quiz_completed = True
                                st.session_state.stage1_completed = True
                                save_progress()
                                check_and_send_milestone_emails()
                            else:
                                st.session_state.stage1_quiz_completed = False
                                st.session_state.stage1_completed = False

                            st.rerun()

                        if st.session_state.stage1_quiz_submitted:
                            total_questions = len(STAGE1_QUIZ_QUESTIONS)
                            required_score = int(total_questions * 0.8)

                            st.write(f"Your score: **{st.session_state.stage1_quiz_score}/{total_questions}**")

                            if st.session_state.stage1_quiz_score >= required_score:
                                st.success("You passed the quiz successfully ✅")
                                st.success("Stage 1 completed successfully ✅")

                                st.write("")
                                if st.button("Go to Stage 2", use_container_width=True, key="stage1_go_stage2"):
                                    go_to("stage2")
                                    st.rerun()
                            else:
                                st.error(f"You need at least {required_score}/{total_questions} correct answers to pass.")

                    st.write("")
                    back_col1, back_col2 = st.columns([1, 2.4])

                    with back_col1:
                        if st.button("← Back", use_container_width=True, key="stage1_back_to_doc"):
                            st.session_state.stage1_current_item = 0
                            st.rerun()

# ---------------------------------------------------
# Stage 2 Page
# ---------------------------------------------------
elif st.session_state.current_page == "stage2":
    if not st.session_state.logged_in:
        st.warning("Please login first.")
        if st.button("Go to Login", key="stage2_go_to_login"):
            go_to("auth")
            st.rerun()
    else:
        top1, top2, top3 = st.columns([2, 4, 2])

        with top1:
            if st.button("← Home", use_container_width=True, key="stage2_home"):
                go_to("home")
                st.rerun()

        with top3:
            if st.button("Profile", use_container_width=True, key="stage2_profile"):
                go_to("profile")
                st.rerun()

        st.markdown("""
        <div class="stage-page-hero">
            <div class="stage-page-hero-title">Stage 2: Signalling & Hardware</div>
            <div class="stage-page-hero-text">
                Continue your journey by exploring the recommended signalling and hardware learning resources,
                then complete the assessment to unlock the final specialization stage.
            </div>
        </div>
        """, unsafe_allow_html=True)

        progress = calculate_progress()
        st.markdown(f"### Progress: {progress}%")
        st.progress(progress / 100)
        st.write("")

        if not st.session_state.stage1_completed:
            st.info("This stage is locked. Complete Stage 1 first.")
        else:
            if st.session_state.stage2_current_item not in [0, 1, 2]:
                st.session_state.stage2_current_item = 0

            left_col, right_col = st.columns([0.9, 2.3])

            # -----------------------------
            # Left Sidebar (Display Only)
            # -----------------------------
            with left_col:
                st.markdown("### Stage 2 Content")

                for idx, item in enumerate(STAGE2_ITEMS):
                    completed = st.session_state[item["key"]]
                    is_current = st.session_state.stage2_current_item == idx

                    icon = "✅" if completed else "⬜"

                    if is_current:
                        st.markdown(
                            f"""
                            <div style="
                                background-color:#E8F0FE;
                                border:1px solid #BFDBFE;
                                border-radius:12px;
                                padding:10px 12px;
                                margin-bottom:10px;
                                font-weight:700;
                                color:#1F3552;
                            ">
                                {icon} {item['title']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"""
                            <div style="
                                background-color:white;
                                border:1px solid #E5E7EB;
                                border-radius:12px;
                                padding:10px 12px;
                                margin-bottom:10px;
                                font-weight:500;
                                color:#374151;
                            ">
                                {icon} {item['title']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            # -----------------------------
            # Main Content Area
            # -----------------------------
            with right_col:
                current_index = st.session_state.stage2_current_item
                current_item = STAGE2_ITEMS[current_index]

                st.markdown(f"## {current_item['title']}")
                st.write(f"**Type:** {current_item['type']}")
                st.write(f"**Duration:** {current_item['duration']}")
                st.write(current_item["description"])
                st.write("")

                # -------------------------
                # Item 1: Course 1
                # -------------------------
                if current_index == 0:
                    st.markdown(
                        """
                        <a href="https://alstomuniversity.eu.crossknowledge.com/site/m/public_training/573#/" target="_blank" style="text-decoration:none;">
                            <div style="
                                background-color:#0B3D91;
                                color:white;
                                text-align:center;
                                padding:12px 14px;
                                border-radius:12px;
                                font-weight:700;
                                font-size:16px;
                                margin-top:8px;
                                margin-bottom:10px;
                            ">
                                Open Course
                            </div>
                        </a>
                        """,
                        unsafe_allow_html=True
                    )

                    st.write("")

                    if not st.session_state.stage2_doc1_completed:
                        if st.button("Mark Course 1 as Completed ✅", use_container_width=True, key="stage2_doc1_complete"):
                            st.session_state.stage2_doc1_completed = True
                            save_progress()
                            st.success("Course 1 marked as completed.")
                            st.rerun()
                    else:
                        st.success("Course 1 completed ✅")

                    st.write("")

                    next_col1, next_col2 = st.columns([1, 2.4])
                    with next_col1:
                        if st.button("Go to Next Item →", use_container_width=True, key="stage2_next_from_doc1"):
                            st.session_state.stage2_current_item = 1
                            st.rerun()

                # -------------------------
                # Item 2: Course 2
                # -------------------------
                elif current_index == 1:
                    st.markdown(
                        """
                        <a href="https://alstomuniversity.eu.crossknowledge.com/site/m/public_training/10667#/" target="_blank" style="text-decoration:none;">
                            <div style="
                                background-color:#0B3D91;
                                color:white;
                                text-align:center;
                                padding:12px 14px;
                                border-radius:12px;
                                font-weight:700;
                                font-size:16px;
                                margin-top:8px;
                                margin-bottom:10px;
                            ">
                                Open Course
                            </div>
                        </a>
                        """,
                        unsafe_allow_html=True
                    )

                    st.write("")

                    if not st.session_state.stage2_doc2_completed:
                        if st.button("Mark Course 2 as Completed ✅", use_container_width=True, key="stage2_doc2_complete"):
                            st.session_state.stage2_doc2_completed = True
                            save_progress()
                            st.success("Course 2 marked as completed.")
                            st.rerun()
                    else:
                        st.success("Course 2 completed ✅")

                    st.write("")

                    nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 2])

                    with nav_col1:
                        if st.button("← Back", use_container_width=True, key="stage2_back_to_doc1"):
                            st.session_state.stage2_current_item = 0
                            st.rerun()

                    with nav_col2:
                        if st.button("Go to Next Item →", use_container_width=True, key="stage2_next_to_quiz"):
                            st.session_state.stage2_current_item = 2
                            st.rerun()

                # -------------------------
                # Item 3: Quiz
                # -------------------------
                elif current_index == 2:
                    if not st.session_state.stage2_doc1_completed or not st.session_state.stage2_doc2_completed:
                        st.info("Please complete both courses first before attempting the quiz.")
                    else:
                        st.subheader("Stage 2 Quiz")

                        user_answers = []

                        for i, q in enumerate(STAGE2_QUIZ_QUESTIONS, start=1):
                            answer = st.radio(
                                f"Q{i}. {q['question']}",
                                q["options"],
                                key=f"stage2_quiz_q{i}"
                            )
                            user_answers.append(answer)

                            if st.session_state.stage2_quiz_submitted and len(st.session_state.stage2_submitted_answers) == len(STAGE2_QUIZ_QUESTIONS):
                                submitted_answer = st.session_state.stage2_submitted_answers[i - 1]

                                if submitted_answer == q["answer"]:
                                    st.success("✅ Correct")
                                else:
                                    st.error("❌ Wrong")

                        if st.button("Submit Quiz ✅", use_container_width=True, key="stage2_submit_quiz_page"):
                            correct_count = 0

                            st.session_state.stage2_submitted_answers = user_answers.copy()
                            st.session_state.stage2_quiz_submitted = True

                            for user_answer, q in zip(st.session_state.stage2_submitted_answers, STAGE2_QUIZ_QUESTIONS):
                                if user_answer == q["answer"]:
                                    correct_count += 1

                            total_questions = len(STAGE2_QUIZ_QUESTIONS)
                            required_score = int(total_questions * 0.8)

                            st.session_state.stage2_quiz_score = correct_count

                            if correct_count >= required_score:
                                st.session_state.stage2_quiz_completed = True
                                st.session_state.stage2_completed = True
                                save_progress()
                                check_and_send_milestone_emails()
                            else:
                                st.session_state.stage2_quiz_completed = False
                                st.session_state.stage2_completed = False

                            st.rerun()

                        if st.session_state.stage2_quiz_submitted:
                            total_questions = len(STAGE2_QUIZ_QUESTIONS)
                            required_score = int(total_questions * 0.8)

                            st.write(f"Your score: **{st.session_state.stage2_quiz_score}/{total_questions}**")

                            if st.session_state.stage2_quiz_score >= required_score:
                                st.success("You passed the quiz successfully ✅")
                                st.success("Stage 2 completed successfully ✅")

                                st.write("")
                                if st.button("Go to Stage 3", use_container_width=True, key="stage2_go_stage3"):
                                    go_to("stage3")
                                    st.rerun()
                            else:
                                st.error(f"You need at least {required_score}/{total_questions} correct answers to pass.")

                    st.write("")
                    back_col1, back_col2 = st.columns([1, 2.4])

                    with back_col1:
                        if st.button("← Back", use_container_width=True, key="stage2_back_to_doc2"):
                            st.session_state.stage2_current_item = 1
                            st.rerun()

# ---------------------------------------------------
# Stage 3 Page
# ---------------------------------------------------
elif st.session_state.current_page == "stage3":
    if not st.session_state.logged_in:
        st.warning("Please login first.")
        if st.button("Go to Login", key="stage3_go_to_login"):
            go_to("auth")
            st.rerun()
    else:
        top1, top2, top3 = st.columns([2, 4, 2])

        with top1:
            if st.button("← Home", use_container_width=True, key="stage3_home"):
                go_to("home")
                st.rerun()

        with top3:
            if st.button("Profile", use_container_width=True, key="stage3_profile"):
                go_to("profile")
                st.rerun()

        st.markdown("""
        <div class="stage-page-hero">
            <div class="stage-page-hero-title">Stage 3: Specialization</div>
            <div class="stage-page-hero-text">
                In this final stage, you will choose your specialization path based on your team or technical focus.
                Once selected, you will continue to the dedicated learning page for that path and complete its final materials and quiz.
            </div>
        </div>
        """, unsafe_allow_html=True)

        progress = calculate_progress()
        st.markdown(f"### Progress: {progress}%")
        st.progress(progress / 100)
        st.write("")

        if not st.session_state.stage2_completed:
            st.info("This stage is locked. Complete Stage 2 first.")
        else:
            st.markdown("## Select Your Specialization Path")
            st.write("Choose the path that matches your team or technical learning direction.")

            select_col1, select_col2 = st.columns([1.3, 1.7])

            with select_col1:
                selected = st.selectbox(
                    "Select your specialization path",
                    ["", "Pedal", "HVITC", "OBC", "Cable Chassis"],
                    index=0,
                    key="stage3_path_select"
                )

            st.write("")

            button_col1, button_col2 = st.columns([1.3, 1.7])

            with button_col1:
                if st.button("Enter Selected Path", use_container_width=True, key="enter_selected_path"):
                    if not selected:
                        st.error("Please choose a specialization path first.")
                    else:
                        # Save selected_path only the first time
                        if not st.session_state.selected_path:
                            st.session_state.selected_path = selected
                            save_progress()

                        if selected == "Pedal":
                            go_to("stage3_pedal")
                        elif selected == "HVITC":
                            go_to("stage3_hvitc")
                        elif selected == "OBC":
                            go_to("stage3_obc")
                        elif selected == "Cable Chassis":
                            go_to("stage3_cable")

                        st.rerun()

# ---------------------------------------------------
# Stage 3 - Pedal Page
# ---------------------------------------------------
elif st.session_state.current_page == "stage3_pedal":
    if not st.session_state.logged_in:
        st.warning("Please login first.")
        if st.button("Go to Login", key="pedal_go_to_login"):
            go_to("auth")
            st.rerun()
    else:
        top1, top2, top3 = st.columns([2, 4, 2])

        with top1:
            if st.button("← Stage 3", use_container_width=True, key="pedal_back_stage3"):
                go_to("stage3")
                st.rerun()

        with top3:
            if st.button("Profile", use_container_width=True, key="pedal_profile"):
                go_to("profile")
                st.rerun()

        st.markdown("""
        <div class="stage-page-hero">
            <div class="stage-page-hero-title">Pedal Specialization</div>
            <div class="stage-page-hero-text">
                In this specialization path, you will explore the Pedal Cabinet and its main components,
                then complete the final quiz to validate your understanding.
            </div>
        </div>
        """, unsafe_allow_html=True)

        progress = calculate_progress()
        st.markdown(f"### Progress: {progress}%")
        st.progress(progress / 100)
        st.write("")

        if not st.session_state.stage2_completed:
            st.info("This path is locked. Complete Stage 2 first.")
        else:
            if st.session_state.pedal_current_item not in [0, 1]:
                st.session_state.pedal_current_item = 0

            left_col, right_col = st.columns([0.9, 2.3])

            # -----------------------------
            # Left Sidebar (Display Only)
            # -----------------------------
            with left_col:
                st.markdown("### Pedal Content")

                for idx, item in enumerate(PEDAL_ITEMS):
                    completed = st.session_state[item["key"]]
                    is_current = st.session_state.pedal_current_item == idx

                    icon = "✅" if completed else "⬜"

                    if is_current:
                        st.markdown(
                            f"""
                            <div style="
                                background-color:#E8F0FE;
                                border:1px solid #BFDBFE;
                                border-radius:12px;
                                padding:10px 12px;
                                margin-bottom:10px;
                                font-weight:700;
                                color:#1F3552;
                            ">
                                {icon} {item['title']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"""
                            <div style="
                                background-color:white;
                                border:1px solid #E5E7EB;
                                border-radius:12px;
                                padding:10px 12px;
                                margin-bottom:10px;
                                font-weight:500;
                                color:#374151;
                            ">
                                {icon} {item['title']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            # -----------------------------
            # Main Content Area
            # -----------------------------
            with right_col:
                current_index = st.session_state.pedal_current_item
                current_item = PEDAL_ITEMS[current_index]

                st.markdown(f"## {current_item['title']}")
                st.write(f"**Type:** {current_item['type']}")
                st.write(f"**Duration:** {current_item['duration']}")
                st.write(current_item["description"])
                st.write("")

                # -------------------------
                # Item 1: Presentation
                # -------------------------
                if current_index == 0:
                    try:
                        with open(current_item["file"], "rb") as doc_file:
                            st.download_button(
                                label="Download Pedal Presentation",
                                data=doc_file,
                                file_name=current_item["file"],
                                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                                use_container_width=True,
                                key="pedal_download_doc"
                            )
                    except Exception:
                        st.error(f"File not found: {current_item['file']}")

                    st.write("")

                    if not st.session_state.pedal_doc_completed:
                        if st.button("Mark Presentation as Completed ✅", use_container_width=True, key="pedal_doc_complete"):
                            st.session_state.pedal_doc_completed = True
                            save_progress()
                            st.success("Presentation marked as completed.")
                            st.rerun()
                    else:
                        st.success("Presentation completed ✅")

                    st.write("")

                    next_col1, next_col2 = st.columns([1, 2.4])

                    with next_col1:
                        if st.button("Go to Next Item →", use_container_width=True, key="pedal_next_to_quiz"):
                            st.session_state.pedal_current_item = 1
                            st.rerun()

                # -------------------------
                # Item 2: Quiz
                # -------------------------
                elif current_index == 1:
                    if not st.session_state.pedal_doc_completed:
                        st.info("Please complete the presentation first before attempting the quiz.")
                    else:
                        st.subheader("Pedal Quiz")

                        user_answers = []

                        for i, q in enumerate(PEDAL_QUIZ_QUESTIONS, start=1):
                            answer = st.radio(
                                f"Q{i}. {q['question']}",
                                q["options"],
                                key=f"pedal_quiz_q{i}"
                            )
                            user_answers.append(answer)

                            if st.session_state.pedal_quiz_submitted and len(st.session_state.pedal_submitted_answers) == len(PEDAL_QUIZ_QUESTIONS):
                                submitted_answer = st.session_state.pedal_submitted_answers[i - 1]

                                if submitted_answer == q["answer"]:
                                    st.success("✅ Correct")
                                else:
                                    st.error("❌ Wrong")

                        if st.button("Submit Quiz ✅", use_container_width=True, key="pedal_submit_quiz_page"):
                            correct_count = 0

                            st.session_state.pedal_submitted_answers = user_answers.copy()
                            st.session_state.pedal_quiz_submitted = True

                            for user_answer, q in zip(st.session_state.pedal_submitted_answers, PEDAL_QUIZ_QUESTIONS):
                                if user_answer == q["answer"]:
                                    correct_count += 1

                            total_questions = len(PEDAL_QUIZ_QUESTIONS)
                            required_score = int(total_questions * 0.8)

                            st.session_state.pedal_quiz_score = correct_count

                            if correct_count >= required_score:
                                st.session_state.pedal_quiz_completed = True
                                st.session_state.stage3_completed = True
                                save_progress()
                                check_and_send_milestone_emails()
                            else:
                                st.session_state.pedal_quiz_completed = False
                                st.session_state.stage3_completed = False

                            st.rerun()

                        if st.session_state.pedal_quiz_submitted:
                            total_questions = len(PEDAL_QUIZ_QUESTIONS)
                            required_score = int(total_questions * 0.8)

                            st.write(f"Your score: **{st.session_state.pedal_quiz_score}/{total_questions}**")

                            if st.session_state.pedal_quiz_score >= required_score:
                                st.success("You passed the quiz successfully ✅")
                                st.success("Pedal specialization completed successfully ✅")
                            else:
                                st.error(f"You need at least {required_score}/{total_questions} correct answers to pass.")

                    st.write("")
                    back_col1, back_col2 = st.columns([1, 2.4])

                    with back_col1:
                        if st.button("← Back", use_container_width=True, key="pedal_back_to_doc"):
                            st.session_state.pedal_current_item = 0
                            st.rerun()

# ---------------------------------------------------
# Stage 3 - HVITC Page
# ---------------------------------------------------
elif st.session_state.current_page == "stage3_hvitc":
    if not st.session_state.logged_in:
        st.warning("Please login first.")
        if st.button("Go to Login", key="hvitc_go_to_login"):
            go_to("auth")
            st.rerun()
    else:
        top1, top2, top3 = st.columns([2, 4, 2])

        with top1:
            if st.button("← Stage 3", use_container_width=True, key="hvitc_back_stage3"):
                go_to("stage3")
                st.rerun()

        with top3:
            if st.button("Profile", use_container_width=True, key="hvitc_profile"):
                go_to("profile")
                st.rerun()

        st.markdown("""
        <div class="stage-page-hero">
            <div class="stage-page-hero-title">HVITC Specialization</div>
            <div class="stage-page-hero-text">
                In this specialization path, you will explore HVITC concepts and components,
                then complete the final quiz to validate your understanding.
            </div>
        </div>
        """, unsafe_allow_html=True)

        progress = calculate_progress()
        st.markdown(f"### Progress: {progress}%")
        st.progress(progress / 100)
        st.write("")

        if not st.session_state.stage2_completed:
            st.info("This path is locked. Complete Stage 2 first.")
        else:
            if st.session_state.hvitc_current_item not in [0, 1]:
                st.session_state.hvitc_current_item = 0

            left_col, right_col = st.columns([0.9, 2.3])

            # -----------------------------
            # Left Sidebar (Display Only)
            # -----------------------------
            with left_col:
                st.markdown("### HVITC Content")

                for idx, item in enumerate(HVITC_ITEMS):
                    completed = st.session_state[item["key"]]
                    is_current = st.session_state.hvitc_current_item == idx

                    icon = "✅" if completed else "⬜"

                    if is_current:
                        st.markdown(
                            f"""
                            <div style="
                                background-color:#E8F0FE;
                                border:1px solid #BFDBFE;
                                border-radius:12px;
                                padding:10px 12px;
                                margin-bottom:10px;
                                font-weight:700;
                                color:#1F3552;
                            ">
                                {icon} {item['title']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"""
                            <div style="
                                background-color:white;
                                border:1px solid #E5E7EB;
                                border-radius:12px;
                                padding:10px 12px;
                                margin-bottom:10px;
                                font-weight:500;
                                color:#374151;
                            ">
                                {icon} {item['title']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            # -----------------------------
            # Main Content Area
            # -----------------------------
            with right_col:
                current_index = st.session_state.hvitc_current_item
                current_item = HVITC_ITEMS[current_index]

                st.markdown(f"## {current_item['title']}")
                st.write(f"**Type:** {current_item['type']}")
                st.write(f"**Duration:** {current_item['duration']}")
                st.write(current_item["description"])
                st.write("")

                # -------------------------
                # Item 1: Presentation
                # -------------------------
                if current_index == 0:
                    try:
                        with open(current_item["file"], "rb") as doc_file:
                            st.download_button(
                                label="Download HVITC Presentation",
                                data=doc_file,
                                file_name=current_item["file"],
                                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                                use_container_width=True,
                                key="hvitc_download_doc"
                            )
                    except Exception:
                        st.error(f"File not found: {current_item['file']}")

                    st.write("")

                    if not st.session_state.hvitc_doc_completed:
                        if st.button("Mark Presentation as Completed ✅", use_container_width=True, key="hvitc_doc_complete"):
                            st.session_state.hvitc_doc_completed = True
                            save_progress()
                            st.success("Presentation marked as completed.")
                            st.rerun()
                    else:
                        st.success("Presentation completed ✅")

                    st.write("")

                    next_col1, next_col2 = st.columns([1, 2.4])

                    with next_col1:
                        if st.button("Go to Next Item →", use_container_width=True, key="hvitc_next_to_quiz"):
                            st.session_state.hvitc_current_item = 1
                            st.rerun()

                # -------------------------
                # Item 2: Quiz
                # -------------------------
                elif current_index == 1:
                    if not st.session_state.hvitc_doc_completed:
                        st.info("Please complete the presentation first before attempting the quiz.")
                    else:
                        st.subheader("HVITC Quiz")

                        user_answers = []

                        for i, q in enumerate(HVITC_QUIZ_QUESTIONS, start=1):
                            answer = st.radio(
                                f"Q{i}. {q['question']}",
                                q["options"],
                                key=f"hvitc_quiz_q{i}"
                            )
                            user_answers.append(answer)

                            if st.session_state.hvitc_quiz_submitted and len(st.session_state.hvitc_submitted_answers) == len(HVITC_QUIZ_QUESTIONS):
                                submitted_answer = st.session_state.hvitc_submitted_answers[i - 1]

                                if submitted_answer == q["answer"]:
                                    st.success("✅ Correct")
                                else:
                                    st.error("❌ Wrong")

                        if st.button("Submit Quiz ✅", use_container_width=True, key="hvitc_submit_quiz_page"):
                            correct_count = 0

                            st.session_state.hvitc_submitted_answers = user_answers.copy()
                            st.session_state.hvitc_quiz_submitted = True

                            for user_answer, q in zip(st.session_state.hvitc_submitted_answers, HVITC_QUIZ_QUESTIONS):
                                if user_answer == q["answer"]:
                                    correct_count += 1

                            total_questions = len(HVITC_QUIZ_QUESTIONS)
                            required_score = int(total_questions * 0.8)

                            st.session_state.hvitc_quiz_score = correct_count

                            if correct_count >= required_score:
                                st.session_state.hvitc_quiz_completed = True
                                st.session_state.stage3_completed = True
                                save_progress()
                                check_and_send_milestone_emails()
                            else:
                                st.session_state.hvitc_quiz_completed = False
                                st.session_state.stage3_completed = False

                            st.rerun()

                        if st.session_state.hvitc_quiz_submitted:
                            total_questions = len(HVITC_QUIZ_QUESTIONS)
                            required_score = int(total_questions * 0.8)

                            st.write(f"Your score: **{st.session_state.hvitc_quiz_score}/{total_questions}**")

                            if st.session_state.hvitc_quiz_score >= required_score:
                                st.success("You passed the quiz successfully ✅")
                                st.success("HVITC specialization completed successfully ✅")
                            else:
                                st.error(f"You need at least {required_score}/{total_questions} correct answers to pass.")

                    st.write("")
                    back_col1, back_col2 = st.columns([1, 2.4])

                    with back_col1:
                        if st.button("← Back", use_container_width=True, key="hvitc_back_to_doc"):
                            st.session_state.hvitc_current_item = 0
                            st.rerun()

# ---------------------------------------------------
# Stage 3 - OBC Page
# ---------------------------------------------------
elif st.session_state.current_page == "stage3_obc":
    if not st.session_state.logged_in:
        st.warning("Please login first.")
        if st.button("Go to Login", key="obc_go_to_login"):
            go_to("auth")
            st.rerun()
    else:
        top1, top2, top3 = st.columns([2, 4, 2])

        with top1:
            if st.button("← Stage 3", use_container_width=True, key="obc_back_stage3"):
                go_to("stage3")
                st.rerun()

        with top3:
            if st.button("Profile", use_container_width=True, key="obc_profile"):
                go_to("profile")
                st.rerun()

        st.markdown("""
        <div class="stage-page-hero">
            <div class="stage-page-hero-title">OBC Specialization</div>
            <div class="stage-page-hero-text">
                This specialization path will provide focused learning content related to the OBC team and its technical scope.
            </div>
        </div>
        """, unsafe_allow_html=True)

        progress = calculate_progress()
        st.markdown(f"### Progress: {progress}%")
        st.progress(progress / 100)
        st.write("")

        st.info("This specialization path is currently under development. Content will be added soon.")

# ---------------------------------------------------
# Stage 3 - Cable Chassis Page
# ---------------------------------------------------
elif st.session_state.current_page == "stage3_cable":
    if not st.session_state.logged_in:
        st.warning("Please login first.")
        if st.button("Go to Login", key="cable_go_to_login"):
            go_to("auth")
            st.rerun()
    else:
        top1, top2, top3 = st.columns([2, 4, 2])

        with top1:
            if st.button("← Stage 3", use_container_width=True, key="cable_back_stage3"):
                go_to("stage3")
                st.rerun()

        with top3:
            if st.button("Profile", use_container_width=True, key="cable_profile"):
                go_to("profile")
                st.rerun()

        st.markdown("""
        <div class="stage-page-hero">
            <div class="stage-page-hero-title">Cable Chassis Specialization</div>
            <div class="stage-page-hero-text">
                This specialization path will provide focused learning content related to the Cable Chassis team and its technical scope.
            </div>
        </div>
        """, unsafe_allow_html=True)

        progress = calculate_progress()
        st.markdown(f"### Progress: {progress}%")
        st.progress(progress / 100)
        st.write("")

        st.info("This specialization path is currently under development. Content will be added soon.")

# ---------------------------------------------------
# Alstom Tools Page
# ---------------------------------------------------
elif st.session_state.current_page == "alstom_tools":
    if not st.session_state.logged_in:
        st.warning("Please login first.")
        if st.button("Go to Login", key="tools_go_to_login"):
            go_to("auth")
            st.rerun()
    else:
        top1, top2, top3 = st.columns([2, 4, 2])

        with top1:
            if st.button("← Home", use_container_width=True, key="tools_back_home"):
                go_to("home")
                st.rerun()

        with top3:
            if st.button("Profile", use_container_width=True, key="tools_profile"):
                go_to("profile")
                st.rerun()

        st.markdown("""
        <div class="mandatory-hero">
            <div class="mandatory-hero-title">Alstom Tools</div>
            <div class="mandatory-hero-text">
                Explore useful Alstom tools and internal platforms that may support your engineering work,
                project activities, and technical learning journey.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<h2 style="color:#1F3552; font-weight:700;">Available Tools</h2>', unsafe_allow_html=True)
        st.write("Discover useful internal platforms and their related learning materials.")

        for i in range(0, len(ALSTOM_TOOLS), 2):
            left_space, col1, col2, right_space = st.columns([0.3, 1, 1, 0.3])
            cols = [col1, col2]
            row_tools = ALSTOM_TOOLS[i:i+2]

            for col, tool in zip(cols, row_tools):
                with col:
                    try:
                        img_left, img_center, img_right = st.columns([1, 2, 1])
                        with img_center:
                            tool_img = resize_and_crop_image(tool["image"], 260, 170)
                            st.image(tool_img, width=260)
                    except:
                        st.info(f"Add image: {tool['image']}")

                    st.markdown(f'<div class="mandatory-card-title">{tool["title"]}</div>', unsafe_allow_html=True)
                    st.markdown(
                        f'''
                        <div class="mandatory-card-text" style="min-height: 50px;">
                            {tool["description"]}
                        </div>
                        ''',
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <a href="{tool['tool_link']}" target="_blank" style="text-decoration:none;">
                            <div style="
                                background-color:#0B3D91;
                                color:white;
                                text-align:center;
                                padding:10px 12px;
                                border-radius:12px;
                                font-weight:700;
                                font-size:14px;
                                margin-top:8px;
                                margin-bottom:10px;
                            ">
                                Open Tool
                            </div>
                        </a>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <a href="{tool['learning_link']}" target="_blank" style="text-decoration:none;">
                            <div style="
                                background-color:#F3F4F6;
                                color:#1F3552;
                                text-align:center;
                                padding:12px 14px;
                                border-radius:12px;
                                font-weight:700;
                                font-size:16px;
                                margin-top:6px;
                                margin-bottom:10px;
                                border:1px solid #D1D5DB;
                            ">
                                Open Learning Material
                            </div>
                        </a>
                        """,
                        unsafe_allow_html=True
                    )

                    st.write("")

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
        if st.button("← Back to Home", key="profile_back_home"):
            go_to("home")
            st.rerun()

        st.title("My Profile")

        progress = calculate_progress()

        # Top summary
        st.markdown(f"""
        <div class="info-panel" style="margin-bottom:18px;">
            <h2 style="color:#1F3552; margin-bottom:8px;">{st.session_state.user_name}</h2>
            <p style="font-size:16px; color:#4B5563; margin-bottom:6px;"><strong>Email:</strong> {st.session_state.user_email}</p>
            <p style="font-size:16px; color:#4B5563; margin-bottom:0;"><strong>Overall Progress:</strong> {progress}%</p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(progress / 100)
        st.write("")

        # Two compact cards
        c1, c2 = st.columns(2)

        with c1:
            st.markdown(f"""
            <div class="white-box" style="min-height: 220px;">
                <h3 style="color:#1F3552; font-size:20px; font-weight:700; margin-bottom:14px;">Profile Details</h3>
                <p style="font-size:16px; color:#374151; margin-bottom:10px;"><strong>Full Name:</strong> {st.session_state.user_name}</p>
                <p style="font-size:16px; color:#374151; margin-bottom:10px;"><strong>Email:</strong> {st.session_state.user_email}</p>
                <p style="font-size:16px; color:#374151; margin-bottom:0;"><strong>Selected Path:</strong> {st.session_state.selected_path if st.session_state.selected_path else 'Not selected'}</p>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="white-box" style="min-height: 220px;">
                <h3 style="color:#1F3552; font-size:20px; font-weight:700; margin-bottom:14px;">Journey Summary</h3>
                <p style="font-size:16px; color:#374151; margin-bottom:10px;"><strong>Mandatory Trainings:</strong> {'Completed' if st.session_state.mandatory_completed else 'Not completed'}</p>
                <p style="font-size:16px; color:#374151; margin-bottom:10px;"><strong>Stage 1:</strong> {'Completed' if st.session_state.stage1_completed else 'Not completed'}</p>
                <p style="font-size:16px; color:#374151; margin-bottom:10px;"><strong>Stage 2:</strong> {'Completed' if st.session_state.stage2_completed else 'Not completed'}</p>
                <p style="font-size:16px; color:#374151; margin-bottom:0;"><strong>Stage 3:</strong> {'Completed' if st.session_state.stage3_completed else 'Not completed'}</p>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        # Mandatory breakdown
        st.markdown("""
        <div class="white-box" style="min-height: auto;">
            <h3 style="color:#1F3552; font-size:20px; font-weight:700; margin-bottom:14px;">Mandatory Trainings Breakdown</h3>
        """, unsafe_allow_html=True)

        for i, course in enumerate(MANDATORY_COURSES, start=1):
            status = "✅ Completed" if st.session_state[course["key"]] else "⬜ Not completed"
            st.write(f"**Course {i}: {course['title']}** — {status}")

        st.markdown("</div>", unsafe_allow_html=True)
