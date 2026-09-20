import json
import firebase_admin
from firebase_admin import credentials, db
import requests
import streamlit as st

st.set_page_config(
    page_title="ClassIQ Registration",
    page_icon="📄",
    initial_sidebar_state="collapsed",
)

# Initialize Firebase Realtime Database using single secret json string
if not firebase_admin._apps:
  try:
    cred_dict = json.loads(st.secrets["FIREBASE_CREDENTIALS"])
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": (
                "https://smartiq-project-default-rtdb.asia-southeast1.firebasedatabase.app/"
            )
        },
    )
  except Exception as e:
    st.error(f"Firebase initialization error: {e}")

# Google Apps Script Web App URL
GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbwm26NlHOUfVQif2rJSUJN443k8SE7IPePBBTEgwEn7uA3rwyyuM3jstMd4jd-onK93/exec"

# Fully responsive mobile-friendly styling
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        .stApp {
            background-color: #ffffff !important;
            color: #111111 !important;
        }
        html, body, [class*="css"] {
            font-family: 'Jost', sans-serif !important;
            background-color: #ffffff !important;
            color: #111111 !important;
        }
        .main .block-container {
            max-width: 400px;
            width: 100%;
            padding-top: 2rem;
            padding-right: 1.2rem;
            padding-left: 1.2rem;
            margin: auto;
        }
        .brand-title {
            text-align: center;
            font-weight: 800;
            font-size: 32px;
            letter-spacing: -0.5px;
            color: #111111 !important;
            margin-bottom: 0px;
        }
        .brand-subtitle-container {
            text-align: center;
            margin-top: 2px;
            margin-bottom: 25px;
        }
        .sub-top {
            color: #71717a !important;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        .sub-bottom {
            font-weight: 800;
            font-size: 24px;
            color: #111111 !important;
            letter-spacing: -0.5px;
            margin-top: -3px;
        }
        .section-desc {
            color: #71717a !important;
            font-size: 13px;
            margin-bottom: 15px;
        }
        .input-label {
            font-size: 13px;
            font-weight: 600;
            color: #374151 !important;
            margin-bottom: 6px;
        }
        .helper-text {
            color: #9ca3af !important;
            font-size: 11px;
            margin-top: 6px;
            margin-bottom: 20px;
        }
        
        .stTextInput input {
            background-color: #ffffff !important;
            color: #111111 !important;
            border-radius: 12px !important;
            border: 1px solid #e2e8f0 !important;
            padding: 12px 14px !important;
            font-family: 'Jost', sans-serif !important;
            font-size: 14px !important;
            box-shadow: none !important;
            width: 100% !important;
        }
        .stTextInput input:focus, .stTextInput input:active {
            border-color: #111111 !important;
            box-shadow: none !important;
            outline: none !important;
        }
        div[data-baseweb="input"] {
            border-color: transparent !important;
            box-shadow: none !important;
        }

        label {
            color: #374151 !important;
        }
        
        .stButton button {
            width: 100% !important;
            background-color: #000000 !important;
            color: #ffffff !important;
            border-radius: 14px !important;
            padding: 14px !important;
            font-family: 'Jost', sans-serif !important;
            font-weight: 600 !important;
            border: none !important;
            font-size: 15px !important;
            margin-top: 15px !important;
            cursor: pointer !important;
            box-shadow: none !important;
        }
        .stButton button:hover {
            background-color: #1f2937 !important;
            color: #ffffff !important;
            border: none !important;
        }
        
        .success-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-top: 50px;
        }
        .black-circle {
            width: 75px;
            height: 75px;
            background-color: #000000;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
        }
        .checkmark {
            color: #ffffff;
            font-size: 38px;
            font-weight: bold;
            line-height: 1;
        }
        .success-text {
            font-weight: 800;
            font-size: 24px;
            color: #111111 !important;
            letter-spacing: -0.5px;
            text-align: center;
        }

        .footer {
            text-align: center;
            color: #a1a1aa !important;
            font-size: 11px;
            margin-top: 40px;
            letter-spacing: 0.5px;
        }
    </style>
""",
    unsafe_allow_html=True,
)

if "is_registered" not in st.session_state:
  st.session_state.is_registered = False

# Header Section
st.markdown('<div class="brand-title">ClassIQ</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="brand-subtitle-container">
        <div class="sub-top">NEW USER</div>
        <div class="sub-bottom">REGISTRATION</div>
    </div>
""",
    unsafe_allow_html=True,
)

if st.session_state.is_registered:
  st.markdown(
      """
        <div class="success-container">
            <div class="black-circle">
                <div class="checkmark">✓</div>
            </div>
            <div class="success-text">Registration Done</div>
        </div>
    """,
      unsafe_allow_html=True,
  )
else:
  st.markdown(
      '<div class="section-desc">Enter the OTP generated in the display</div>',
      unsafe_allow_html=True,
  )

  st.markdown(
      '<div class="input-label">Verification code</div>', unsafe_allow_html=True
  )

  otp_input_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Jost', sans-serif; margin: 0; background: transparent; }
            .otp-row { display: flex; gap: 10px; justify-content: space-between; width: 100%; box-sizing: border-box; }
            .otp-box {
                width: 100%; height: 50px;
                background-color: #f8fafc; color: #111111;
                border-radius: 12px; border: 1px solid #e2e8f0;
                text-align: center; font-family: 'Jost', sans-serif;
                font-size: 20px; font-weight: 600; outline: none;
            }
            .otp-box:focus { border-color: #111111; }
        </style>
    </head>
    <body>
        <div class="otp-row">
            <input type="tel" inputmode="numeric" pattern="[0-9]*" class="otp-box" maxlength="1" id="o1" oninput="move(this, 'o2')" onkeydown="back(event, null, 'o1')" />
            <input type="tel" inputmode="numeric" pattern="[0-9]*" class="otp-box" maxlength="1" id="o2" oninput="move(this, 'o3')" onkeydown="back(event, 'o1', 'o2')" />
            <input type="tel" inputmode="numeric" pattern="[0-9]*" class="otp-box" maxlength="1" id="o3" oninput="move(this, 'o4')" onkeydown="back(event, 'o2', 'o3')" />
            <input type="tel" inputmode="numeric" pattern="[0-9]*" class="otp-box" maxlength="1" id="o4" oninput="sendData()" onkeydown="back(event, 'o3', 'o4')" />
        </div>
        <script>
            function move(current, nextId) {
                if (current.value.length >= 1) {
                    document.getElementById(nextId).focus();
                }
                sendData();
            }
            function back(event, prevId, currId) {
                if (event.key === "Backspace" && document.getElementById(currId).value === "" && prevId) {
                    document.getElementById(prevId).focus();
                }
            }
            function sendData() {
                const otp = document.getElementById('o1').value + 
                            document.getElementById('o2').value + 
                            document.getElementById('o3').value + 
                            document.getElementById('o4').value;
                const targetUrl = window.parent.location.origin + window.parent.location.pathname + `?temp_otp=${otp}`;
                window.parent.history.replaceState(null, '', targetUrl);
            }
        </script>
    </body>
    </html>
    """
  st.components.v1.html(otp_input_html, height=58)

  st.markdown(
      '<div class="helper-text">Enter the 4-digit code displayed on the'
      " LCD.</div>",
      unsafe_allow_html=True,
  )

  query_params = st.query_params
  captured_otp = query_params.get("temp_otp", "")

  with st.form("ref_reg_form"):
    st.markdown(
        '<div class="input-label">Your name</div>', unsafe_allow_html=True
    )
    student_name = st.text_input(
        label="Your name", placeholder="", label_visibility="collapsed"
    )

    submit_btn = st.form_submit_button("Register")

    if submit_btn:
      if len(captured_otp) == 4 and student_name:
        try:
          ref = db.reference("registrations")
          ref.push({"otp": captured_otp, "student_name": student_name})

          payload = {"student_name": student_name, "otp": captured_otp}
          requests.post(GOOGLE_SHEET_URL, json=payload)

          st.session_state.is_registered = True
          st.rerun()
        except Exception as e:
          st.error(f"Database/Sheet write failed: {e}")
      else:
        st.warning("Please enter a valid 4-digit OTP and your name.")

st.markdown(
    '<div class="footer">Smart Attendance System</div>', unsafe_allow_html=True
)
