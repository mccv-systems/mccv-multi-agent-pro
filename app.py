import streamlit as st
import requests
import json

# --- CONFIGURATION ---
# You can swap this with your local Ollama URL (http://localhost:11434/api/chat) 
# or a cloud API URL.
API_URL = "https://api.groq.com/openai/v1/chat/completions" # Change if using Groq/OpenAI
API_KEY = "YOUR_API_KEY_HERE" # Put your Groq/OpenAI key here or use st.secrets

st.set_page_config(page_title="MCCV Multi-Agent Pro", page_icon="🛡️")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stChatInput { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ MCCV Multi-Agent Pro")
st.caption("Digital Junior Associate for Pru Life UK Agents")

# --- INITIALIZE SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """
        You are the 'Digital Junior Associate' of Melvyn C.C. Valenzuela. 
        Your goal: Conduct a 10-minute Financial Needs Analysis (FNA) using the D.I.M.E. method.
        
        RULES:
        1. Speak in friendly, professional 'Taglish'.
        2. Ask ONE question at a time to avoid overwhelming the user.
        3. Sequence: 
           - Greet and ask for Name/Goal.
           - D (Death/Final Expenses): Ask about protection needs.
           - I (Income): Ask for monthly income to calculate the gap.
           - M (Mortgage/Debt): Ask about outstanding loans.
           - E (Education/Endowment): Ask about children's school needs.
        4. Calculate the gap and recommend PruLife Elite Protector or Health Prime.
        5. If the budget is below 2k/month, suggest a starter plan.
        6. End by saying you've forwarded the details to the Unit Manager.
        """}
    ]

# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- CHAT LOGIC ---
if prompt := st.chat_input("Type your answer here..."):
    # 1. Show User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate AI Response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # Prepare the data for the API
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": st.session_state.messages,
            "temperature": 0.7
        }
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            # Note: For free deployment, ensure you handle the API key securely!
            r = requests.post(API_URL, headers=headers, json=payload)
            r.raise_for_status()
            full_response = r.json()['choices'][0]['message']['content']
            response_placeholder.markdown(full_response)
            
            # 3. Save AI Message to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Associate is offline: {e}")

# --- SIDEBAR DASHBOARD ---
with st.sidebar:
    st.header("📊 Unit Dashboard")
    st.write("Target: **High-Value Leads**")
    if st.button("Reset Conversation"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()
    st.divider()
    st.info("This bot uses the 'D.I.M.E.' logic by Melvyn C.C. Valenzuela.")
