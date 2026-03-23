import streamlit as st
from groq import Groq

# --- 1. BRANDING ---
st.set_page_config(page_title="MCCV AI - Financial Auditor", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. SIDEBAR DASHBOARD ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/mccv-systems/mccv-multi-agent-pro/main/logo1.png", use_container_width=True)
    st.divider()
    st.subheader("📊 Audit Status")
    st.info("System: Human Life Value Calculator Active")
    st.write("✅ **Strategy:** HLV Audit")
    st.write("✅ **Goal:** Identify Protection Gaps")
    st.divider()
    st.caption("© 2026 MCCV Strategic AI Solutions")

# --- 3. THE "AUDITOR" SYSTEM PROMPT ---
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = (
        "You are the 'MCCV Digital Auditor.' Your goal is NOT to sell, but to Audit the user's Financial Health. "
        "Keep answers SHORT and TACTICAL. Do not use long paragraphs. "
        "INSTRUCTIONS: "
        "1. Conduct a '2-Minute Financial Health Check' by asking 7 quick questions (Age, Dependents, Income, Savings, Expenses, Debts). "
        "2. Once you have the income, calculate Human Life Value (Income x 10 years). "
        "3. CALCULATE THE GAP: (Human Life Value - Current Savings/Insurance). "
        "4. If the Gap is > ₱1M, say: 'URGENCY: CRITICAL.' "
        "5. Present the numbers clearly: 'Your family needs ₱X. You have ₱Y. The GAP is ₱Z.' "
        "6. CONVERT: Ask if they want a 1-page solution via WhatsApp, Email, or a Call from Melvyn."
    )

# --- 4. CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": st.session_state.system_prompt}]

st.image("https://raw.githubusercontent.com/mccv-systems/mccv-multi-agent-pro/main/logo2.png", width=350)
st.subheader("🛡️ 2-Minute Financial Health Audit")
st.write("*Objective Analysis. Professional Urgency.*")

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

if prompt := st.chat_input("Type 'Start Audit' to begin..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        chat_completion = client.chat.completions.create(
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            model="llama-3.3-70b-versatile",
            max_tokens=300 # Limits the length of the AI's response
        )
        response = chat_completion.choices[0].message.content
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# --- 5. FOOTER ---
st.divider()
st.markdown("<div style='text-align: center; color: grey;'>MCCV AI MULTI-AGENT PRO | Strategic Audit System</div>", unsafe_allow_html=True)
