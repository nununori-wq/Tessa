# =============================================================
# RUN THIS CELL AFTER RESTARTING THE KERNEL (see previous cell).
# It verifies the import works, then writes app.py to your
# Deepnote project folder so it's ready to launch.
# =============================================================

# --- Step 2: Verify the fix -----------------------------------
from google import genai
from google.genai import types
print("✅ google-genai imports correctly now!")

# --- Step 3: Set your API key -----------------------------------
# Get a free key at https://aistudio.google.com/
# Either paste it directly here for quick testing...
import os
os.environ["GEMINI_API_KEY"] = "enter your api key here"

# ...or, better for a real deployment, add it once as a Deepnote
# environment variable (Project settings -> Environment variables)
# named GEMINI_API_KEY, and skip the line above entirely.

# --- Step 4: Quick sanity check that the key + model work -------
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
test_chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a helpful assistant. Reply in one short sentence.",
        temperature=0.4,
    ),
)
test_response = test_chat.send_message("Say hello in one sentence.")
print("Model test response:", test_response.text)

# --- Step 5: Write the full Streamlit app to disk ----------------
app_code = r'''
import os
import streamlit as st
from google import genai
from google.genai import types

# -------------------------
# PAGE SETTINGS
# -------------------------
st.set_page_config(
    page_title="TESSA - IRD Grenada",
    page_icon="\U0001F1EC\U0001F1E9",
    layout="wide",
)

# -------------------------
# API KEY
# -------------------------
try:
    API_KEY = st.secrets.get("GEMINI_API_KEY", "")
except Exception:
    API_KEY = ""

if not API_KEY:
    API_KEY = os.environ.get("GEMINI_API_KEY", "")

if not API_KEY:
    st.error(
        "Missing API key. Set a GEMINI_API_KEY environment variable "
        "(Deepnote: Project settings -> Environment variables) or add "
        "a .streamlit/secrets.toml file with GEMINI_API_KEY."
    )
    st.stop()

client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-2.5-flash"

# -------------------------
# SYSTEM PROMPT
# -------------------------
SYSTEM_INSTRUCTION = """
You are TESSA (Taxpayer Electronic Support & Service Assistant).
You are the official AI assistant for the Inland Revenue Division (IRD) Grenada.

Your personality:
- Friendly
- Professional
- Patient
- Respectful
- Clear

Always explain things in simple language.

You help users with:
- TIN Registration
- Income Tax
- Property Tax
- VAT
- Business Taxes
- Filing Returns
- Payment Methods
- IRD Office Information
- Tax Deadlines

If you do not know something, politely recommend contacting the Inland Revenue Division.
Never invent laws or regulations.
"""

# -------------------------
# STYLING
# -------------------------
st.markdown(
    """
    <style>
    .stApp { background-color: #f7f8fa; }
    section[data-testid="stSidebar"] { background-color: #0b2e13; }
    section[data-testid="stSidebar"] * { color: #f5f5f5 !important; }
    .tessa-header {
        display: flex; align-items: center; gap: 14px;
        padding: 18px 22px;
        background: linear-gradient(90deg, #ce1126 0%, #f4d216 50%, #007a3d 100%);
        border-radius: 14px; margin-bottom: 18px;
    }
    .tessa-header h1 { color: #ffffff; margin: 0; font-size: 28px; text-shadow: 0 1px 3px rgba(0,0,0,0.35); }
    .tessa-header p { color: #ffffff; margin: 2px 0 0 0; font-size: 14px; text-shadow: 0 1px 2px rgba(0,0,0,0.3); }
    div.stButton > button {
        border-radius: 10px; border: 1px solid #007a3d;
        color: #0b2e13; background-color: #ffffff; font-weight: 500;
    }
    div.stButton > button:hover { background-color: #007a3d; color: #ffffff; border-color: #007a3d; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# SESSION STATE
# -------------------------
def new_chat_session():
    return client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.4,
        ),
    )

if "chat" not in st.session_state:
    st.session_state.chat = new_chat_session()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:
    st.markdown("## \U0001F1EC\U0001F1E9 IRD Grenada")
    st.markdown("### TESSA")
    st.write("Taxpayer Electronic Support & Service Assistant")
    st.markdown("---")
    st.write("### Quick Topics")
    st.write("- TIN Registration")
    st.write("- Income Tax")
    st.write("- VAT")
    st.write("- Property Tax")
    st.write("- Business Taxes")
    st.write("- Filing Returns")
    st.write("- Payment Methods")
    st.markdown("---")
    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.chat = new_chat_session()
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

# -------------------------
# HEADER
# -------------------------
st.markdown(
    """
    <div class="tessa-header">
        <div style="font-size: 40px;">\U0001F4AC</div>
        <div>
            <h1>TESSA</h1>
            <p>Official AI Assistant for the Inland Revenue Division, Grenada</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# QUICK QUESTIONS
# -------------------------
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Register for a TIN", use_container_width=True):
        st.session_state.pending_prompt = "How do I register for a TIN?"
with col2:
    if st.button("How do I pay my taxes?", use_container_width=True):
        st.session_state.pending_prompt = "How do I pay my taxes?"
with col3:
    if st.button("Business Taxes", use_container_width=True):
        st.session_state.pending_prompt = "What taxes do businesses pay in Grenada?"

# -------------------------
# CHAT HISTORY
# -------------------------
if not st.session_state.messages:
    st.info(
        "Hello! I'm TESSA, your virtual assistant for the Inland Revenue "
        "Division of Grenada. Ask me anything about TIN registration, "
        "Income Tax, VAT, Property Tax, and more, or use a quick topic above."
    )

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# CHAT INPUT
# -------------------------
typed_prompt = st.chat_input("Ask TESSA anything...")
prompt = st.session_state.pending_prompt or typed_prompt
st.session_state.pending_prompt = None

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("TESSA is typing..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                answer = response.text or (
                    "I'm sorry, I couldn't generate a response. Please try "
                    "rephrasing your question or contact the Inland Revenue "
                    "Division directly."
                )
            except Exception as e:
                answer = (
                    f"Sorry, I ran into a problem reaching the assistant "
                    f"service ({e}). Please try again in a moment, or "
                    "contact the Inland Revenue Division for assistance."
                )
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
'''

with open("app.py", "w") as f:
    f.write(app_code)

print("✅ app.py written to your Deepnote project folder.")
