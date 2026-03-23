import streamlit as st
from groq import Groq

# --- 1. PAGE CONFIGURATION & BRANDING ---
st.set_page_config(
    page_title="MCCV AI MULTI-AGENT PRO", 
    page_icon="🛡️", 
    layout="wide"
)

# --- 2. THE BRAIN (GROQ API KEY) ---
# Your specific Groq Key is now integrated
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- 3. SIDEBAR BRANDING (The Company Profile) ---
with st.sidebar:
    # Your Company Logo
    st.image("https://i.postimg.cc/hvdqCRwF/LOGO_WITH_TAGLINE_3.png", use_container_width=True)
    
    st.divider()
    st.write("✨ **Your 24/7 Digital Partner**")
    st.write("📍 *Muntinlupa City, PH*")
    st.divider()
    st.caption("A Product of:")
    st.info("**MCCV Strategic AI Solutions**")
    st.write("---")
    st.write("💡 **Our Pillars:**")
    st.write("✅ Integrity | ✅ Innovation | ✅ Impact")
    st.divider()
    st.success("✅ System: Online (FREE ENGINE)")

# --- 4. THE SYSTEM INSTRUCTIONS (The AI's Rules) ---
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = (
        "You are 'MCCV AI MULTI-AGENT PRO,' a high-level digital assistant created and copyrighted by Melvyn C.C. Valenzuela "
        "of MCCV Strategic AI Solutions. You represent the highest standard of Filipino professional integrity. "
        "You speak in a warm, professional, and helpful Taglish. Your goal is to provide expert guidance and "
        "capture interest for your user's services in Insurance, Security, Coaching, or Real Estate."
    )

# --- 5. SESSION STATE (The Memory) ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": st.session_state.system_prompt}
    ]

# --- 6. MAIN INTERFACE (The Product View) ---
# Your Product Logo
st.image("https://i.postimg.cc/tJxHrGfQ/BOT_LOGO_3.png", width=350)
st.subheader("Smart Tactics. Better Results.")
st.write("---")

# Display the chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# --- 7. THE CHAT LOGIC (Using the Llama 3 Model) ---
if prompt := st.chat_input("How can I help you grow your business today?"):
    # 1. Save and show what the user typed
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 2. Ask the Groq Engine for the answer
    with st.chat_message("assistant"):
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            model="llama-3.3-70b-versatile", # High-speed professional model
        )
        response = chat_completion.choices[0].message.content
        st.write(response)
    
    # 3. Save the bot's answer to its memory
    st.session_state.messages.append({"role": "assistant", "content": response})

# --- 8. THE BRANDED FOOTER WITH COPYRIGHT ---
st.write("") 
st.divider()
st.markdown(
    "<div style='text-align: center; color: grey; font-size: 0.8em;'>"
    "© 2026 MELVYN C C VALENZUELA | MCCV Strategic AI Solutions<br>"
    "Integrity • Innovation • Impact"
    "</div>", 
    unsafe_allow_html=True
)
