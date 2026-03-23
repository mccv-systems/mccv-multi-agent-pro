import streamlit as st
from groq import Groq

# --- 1. BRANDING & CONFIG ---
st.set_page_config(page_title="MCCV AI - Strategic Auditor", layout="wide")
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 2. SIDEBAR ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/mccv-systems/mccv-multi-agent-pro/main/logo1.png", use_container_width=True)
    st.divider()
    st.subheader("📊 Lead Capture Active")
    st.info("System: Personal Data & HLV Audit")
    st.write("✅ **Strategy:** KYC (Know Your Client) First")
    st.write("✅ **Goal:** Full Lead Identification")
    st.divider()
    st.caption("© 2026 MCCV Strategic AI Solutions")

# --- 3. THE "DATA-FIRST" SYSTEM PROMPT ---
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = (
        "You are the 'MCCV Digital Auditor.' Your goal is to capture Lead Data and conduct a Financial Health Check. "
        "STRICT RULE: Ask only ONE question at a time. Wait for the user to answer before moving to the next. "
        "FLOW: "
        "1. Greet the user and ask: 'Ready na ba tayo para sa iyong 2-Minute Financial Health Audit?' "
        "2. Question 1: What is your Complete Name? (First Name, Middle Name, and Family Name). "
        "3. Question 2: What is your Complete Birthdate? (Month/Day/Year). "
        "4. Question 3: What is your Phone Number and Email Address? "
        "5. Question 4: How many Dependents (umaasa sa inyo) do you have? "
        "6. Question 5: What is your Monthly Net Income? "
        "7. Question 6: Current Savings or Insurance coverage? "
        "8. Question 7: Monthly Expenses and Total Debts/Mortgages? "
        "9. FINAL STEP: Calculate Human Life Value (Income x 10 years). Show the GAP (HLV - Savings). "
        "If GAP > ₱1M, label as 'URGENCY: CRITICAL.' "
        "Be professional and emphasize that this data is for their official Audit Record."
    )

# --- 4. CHAT MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": st.session_state.system_prompt}]
    initial_greeting = "Kumusta! Ako ang iyong MCCV Digital Auditor. Simulan natin ang iyong 2-Minute Financial Health Audit. Ready na ba tayo? (Yes/No)"
    st.session_state.messages.append({"role": "assistant", "content": initial_greeting})

# --- 5. MAIN INTERFACE ---
st.image("https://raw.githubusercontent.com/mccv-systems/mccv-multi-agent-pro/main/logo2.png", width=350)
st.subheader("🛡️ Strategic Financial Health Audit")
st.write("*Securing your identity and your future, one step at a time.*")

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
            temperature=0.2 # Keeping it very focused on the data gathering
        )
        response = chat_completion.choices[0].message.content
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# --- 7. FOOTER ---
st.divider()
st.markdown("<div style='text-align: center; color: grey;'>MCCV AI MULTI-AGENT PRO | Strategic Audit System</div>", unsafe_allow_html=True)
