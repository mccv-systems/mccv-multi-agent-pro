import streamlit as st
from groq import Groq

# --- 1. PAGE CONFIGURATION & BRANDING ---
st.set_page_config(
    page_title="MCCV AI MULTI-AGENT PRO", 
    page_icon="🛡️", 
    layout="wide"
)

# --- 2. THE BRAIN (GROQ API) ---
# Ensure "GROQ_API_KEY" is in your Streamlit Secrets!
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 3. SIDEBAR: THE AGENT'S COMMAND CENTER ---
with st.sidebar:
    # Your Company Logo
    st.image("https://raw.githubusercontent.com/mccv-systems/mccv-multi-agent-pro/main/logo1.png", use_container_width=True)
    
    st.divider()
    
    # --- LEAD CAPTURE FORM ---
    st.subheader("📩 Request a Consultation")
    with st.form("lead_form"):
        name = st.text_input("Full Name")
        contact = st.text_input("Mobile / Email")
        service = st.selectbox("Financial Goal:", [
            "Life Protection (Income Replacement)", 
            "Health & Critical Illness (PruHealth Prime)", 
            "Investment & Savings (Elite Protector)", 
            "Education Fund (PruLink)",
            "Estate Planning"
        ])
        submit_button = st.form_submit_button("Book My 10-Min FNA")
        
        if submit_button:
            if name and contact:
                st.success(f"Salamat, {name}! Melvyn's team will contact you shortly regarding {service}.")
            else:
                st.error("Please provide your name and contact details.")

    st.divider()
    st.write("📍 *Muntinlupa City, PH*")
    st.info("**MCCV Strategic AI Solutions**")
    st.write("✅ Integrity | ✅ Innovation | ✅ Impact")
    st.success("✅ Engine: Active (Groq Llama 3)")

# --- 4. THE JUNIOR ASSOCIATE "FNA" INSTRUCTIONS ---
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = (
        "You are the 'Digital Junior Associate' for Melvyn C.C. Valenzuela, a Master Life Coach and Security Consultant. "
        "Your mission is to perform a warm, professional 10-minute Financial Needs Analysis (FNA) in Taglish. "
        "STRATEGY: Use the D.I.M.E. Method (Death/Protection, Income, Mortgage/Debt, Education). "
        "1. Greet the user warmly and ask for their Age and if they have dependents (kids). "
        "2. Ask about their monthly income range to qualify their budget. "
        "3. Identify gaps: Ask what would happen to the family if their income stopped today. "
        "4. RECOMMEND: Suggest 'PruHealth Prime' for health or 'Elite Protector' for high-value protection. "
        "5. CLOSE: Encourage them to use the 'Request a Consultation' form in the sidebar for a personalized proposal from Melvyn."
    )

# --- 5. CHAT MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": st.session_state.system_prompt}
    ]

# --- 6. MAIN INTERFACE ---
st.image("https://raw.githubusercontent.com/mccv-systems/mccv-multi-agent-pro/main/logo2.png", width=350)
st.subheader("Your AI-Powered Financial Needs Analyst")
st.write("---")

# Display conversation
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# --- 7. THE CHAT LOGIC ---
if prompt := st.chat_input("Start your 10-minute FNA here..."):
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

# --- 8. THE BRANDED FOOTER ---
st.write("") 
st.divider()
st.markdown(
    "<div style='text-align: center; color: grey; font-size: 0.8em;'>"
    "© 2026 MELVYN C C VALENZUELA | MCCV Strategic AI Solutions<br>"
    "A Digital Force Multiplier for Financial Advisors"
    "</div>", 
    unsafe_allow_html=True
)
