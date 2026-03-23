import streamlit as st
from groq import Groq

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="MCCV AI MULTI-AGENT PRO", page_icon="🛡️", layout="wide")

# --- 2. THE BRAIN ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 3. SIDEBAR BRANDING & LEAD CAPTURE ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/mccv-systems/mccv-multi-agent-pro/main/logo1.png", use_container_width=True)
    st.divider()
    
    # --- LEAD CAPTURE FORM ---
    st.subheader("📩 Request a Consultation")
    with st.form("lead_form"):
        name = st.text_input("Full Name")
        contact = st.text_input("Phone or Email")
        service = st.selectbox("Interested In:", ["Life Insurance", "Education Fund", "Retirement", "Estate Planning", "Security Consulting"])
        submit_button = st.form_submit_button("Book My Discovery Call")
        
        if submit_button:
            if name and contact:
                st.success(f"Thank you, {name}! Melvyn's team will contact you at {contact} regarding {service}.")
                # In the future, we can add code here to email this to you automatically!
            else:
                st.error("Please fill in your name and contact details.")

    st.divider()
    st.info("**MCCV Strategic AI Solutions**")
    st.write("✅ Integrity | ✅ Innovation | ✅ Impact")

# --- 4. SYSTEM INSTRUCTIONS (Warming up the Lead) ---
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = (
        "You are 'MCCV AI MULTI-AGENT PRO' created by Melvyn C.C. Valenzuela. "
        "Your goal is to warm up potential leads for Financial Advisors and Security Consultants. "
        "When people ask about insurance, explain that 'Insurance is Love made visible.' "
        "Encourage them to fill out the form in the sidebar to get a personalized 'Future You Formula' session. "
        "Always speak in helpful, professional Taglish."
    )

# --- 5. CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": st.session_state.system_prompt}]

st.image("https://raw.githubusercontent.com/mccv-systems/mccv-multi-agent-pro/main/logo2.png", width=350)
st.subheader("Smart Tactics. Better Results.")

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

if prompt := st.chat_input("How can I help you grow your business today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        chat_completion = client.chat.completions.create(
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            model="llama-3.3-70b-versatile",
        )
        response = chat_completion.choices[0].message.content
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# --- 6. FOOTER ---
st.divider()
st.markdown("<div style='text-align: center; color: grey;'>© 2026 MELVYN C C VALENZUELA</div>", unsafe_allow_html=True)
