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
