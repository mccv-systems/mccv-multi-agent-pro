import streamlit as st
from openai import OpenAI

# --- 1. PAGE CONFIGURATION & BRANDING ---
st.set_page_config(
    page_title="MCCV AI MULTI-AGENT PRO", 
    page_icon="🛡️", 
    layout="wide"
)

# --- 2. THE BRAIN (API KEY) ---
# This pulls your key safely from the Streamlit Cloud "Secrets" settings
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- 3. SIDEBAR BRANDING (The Company Profile) ---
with st.sidebar:
    # Your Company Logo (MCCV Strategic AI Solutions)
    st.image("https://i.postimg.cc/hvdqCRwF/LOGO_WITH_TAGLINE_3.png", use_container_width=True)
    
    st.divider()
    st.write("✨ **Your 24/7 Digital Partner**")
    st.write("📍 *Muntinlupa City, PH*")
    st.divider()
    st.caption("A Product of:")
    st.info("**MCCV Strategic AI Solutions**")
    st.write("---")
    st.write("💡 **Our Pillars:**")
    st.write("✅ Integrity")
    st.write("✅ Innovation")
    st.write("✅ Impact")
    st.divider()
    st.success("✅ System: Online")

# --- 4. THE SYSTEM INSTRUCTIONS (The AI's Identity) ---
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = (
        "You are 'MCCV AI MULTI-AGENT PRO,' a high-level digital assistant created and copyrighted by Melvyn C.C. Valenzuela "
        "of MCCV Strategic AI Solutions. You represent the highest standard of Filipino professional integrity. "
        "Speak in warm, professional, and helpful Taglish. Your goal is to provide expert guidance and "
        "capture interest for your user's services in Insurance, Security, Coaching, or Real Estate."
    )

# --- 5. SESSION STATE (The Memory) ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": st.session_state.system_prompt}
    ]

# --- 6. MAIN INTERFACE (The Product View) ---
# Your Product Logo (MCCV AI MULTI-AGENT PRO)
st.image("https://i.postimg.cc/tJxHrGfQ/BOT_LOGO_3.png", width=350)
st.subheader("Smart Tactics. Better Results.")
st.write("---")

# Display the chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# --- 7. THE CHAT LOGIC (The Interaction) ---
if prompt := st.chat_input("How can I help you grow your business today?"):
    # Save and show what the user typed
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Ask OpenAI for the answer
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        # "Stream" the text so it looks like the bot is typing
        response = st.write_stream(stream)
    
    # Save the bot's answer to its memory
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
