import streamlit as st
from groq import Groq

# --- 1. BRANDING & CONFIG ---
st.set_page_config(page_title="MCCV AI - Strategic Auditor", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. SIDEBAR ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/mccv-systems/mccv-multi-agent-pro/main/logo1.png", use_container_width=True)
    st.divider()
    st.subheader("📊 Audit Status")
    st.info("System: Professional HLV Audit")
    st.write("✅ **Tone:** Consultative & Trustworthy")
    st.write("✅ **Method:** 10x Income Rule")
    st.divider()
    st.caption("© 2026 MCCV Strategic AI Solutions")

# --- 3. THE "PROFESSIONAL AUDITOR" SYSTEM PROMPT ---
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = (
        "You are the 'MCCV Digital Auditor,' a professional Financial AI Assistant. Your tone is consultative and trustworthy. "
        "Your mission is to educate users on their protection gap. You never pressure; you audit. "
        "STRICT RULE: Ask only ONE question at a time. "
        "FLOW: "
        "1. Greet and ask: 'Ready na ba tayo para sa iyong 2-Minute Financial Health Audit?' "
        "2. Capture Data: Full Name (First, Middle, Family), then Birthdate (MM/DD/YYYY), then Phone/Email. "
        "3. Gather Financials: Dependents, Monthly Net Income, Current Savings/Insurance, and Monthly Expenses/Debts. "
        "4. CALCULATION: Use the '10x Income Rule' (Monthly Income x 12 months x 10 years) to find the Human Life Value (HLV). "
        "5. THE CLOSING (MANDATORY): Once data is gathered, say: "
        "'Analysis Complete. [Full Name], your family faces a [Protection Gap Amount] protection gap if your income stops today.' "
        "6. THE CTA: 'To receive a bridging plan, our senior advisor MELVYN will call you for a ZOOM or FACE-TO-FACE meeting to discuss your 1-page solution.'"
    )

# --- 4. CHAT MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": st.session_state.system_prompt}]
    initial_greeting = "Kumusta! Ako ang iyong MCCV Digital Auditor. Simulan natin ang iyong 2-Minute Strategic Financial Audit. Ready na ba tayo? (Yes/No)"
    st.session_state.messages.append({"role": "assistant", "content": initial_greeting})

# --- 5. MAIN INTERFACE ---
st.image("https://raw.githubusercontent.com/mccv-systems/mccv-multi-agent-pro/main/logo2.png", width=350)
st.subheader("🛡️ Strategic Financial Health Audit")
st.write("*Objective. Educational. Professional.*")

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# --- 6. CHAT LOGIC ---
if prompt := st.chat_input("I-type ang iyong sagot dito..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        chat_completion = client.chat.completions.create(
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            model="llama-3.3-70b-versatile",
            temperature=0.2
        )
        response = chat_completion.choices[0].message.content
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# --- 7. FOOTER ---
st.divider()
st.markdown("<div style='text-align: center; color: grey;'>MCCV AI MULTI-AGENT PRO | Powered by MCCV Strategic AI Solutions</div>", unsafe_allow_html=True)
