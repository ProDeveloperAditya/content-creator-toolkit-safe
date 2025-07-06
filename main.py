from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    st.error("❌ API Key not loaded. Check your .env file and restart.")




import streamlit as st
import requests

st.set_page_config(page_title="Content Creator Toolkit", page_icon="🎥")
#API_KEY = "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" This one is expired API
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-7b-instruct"

# starting API calls
def get_ai_response(prompt):
    # print("Response status:", res.status_code)
    # print("Response body:", res.text)

    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for content creators."},
            {"role": "user", "content": prompt},
        ]
    }
    res=requests.post(API_URL, headers=headers, json=payload)
    if res.status_code == 200:
        return res.json()["choices"][0]["message"]["content"]
    return "❌ Error: Unable to fetch response."

# UI 
st.title("🎬 Content Creator Toolkit")
st.write("Boost your content creation with AI-generated titles, descriptions, and motivational messages.")

# rest of the project
st.header("1️⃣ YouTube Title & Description Generator")
video_topic = st.text_input("What is your video about?")

if st.button("Generate YT video Titles & Description"):
    if video_topic:
        with st.spinner("Generating..."):
            title_prompt = f"Generate 5 catchy YouTube video titles for a video about: {video_topic}"
            title_response = get_ai_response(title_prompt)

            desc_prompt = f"Write a short, engaging YouTube video description for a video about: {video_topic}"
            desc_response = get_ai_response(desc_prompt)

        st.markdown("### 🔖 Suggested Titles")
        st.markdown(
            f"""
            <div style="background-color:#e3f2fd;padding:15px;border-radius:10px;border-left:5px solid #2196f3;white-space:pre-wrap;word-wrap:break-word;color:#0d0d0d;">
            <p style="font-size:16px;">{title_response.strip()}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### 📄 Suggested Description")
        st.markdown(
            f"""
            <div style="background-color:#f1f8e9;padding:15px;border-radius:10px;border-left:5px solid #689f38;white-space:pre-wrap;word-wrap:break-word;color:#0d0d0d;">
            <p style="font-size:16px;">{desc_response.strip()}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("Please enter a video topic.")

# Additional Motivation Generator for creators 
st.markdown("---")
st.header("2️⃣ Daily Motivation Generator")
st.write("Select how you're feeling or type your own mood/situation.")

given_moods = [
    "Feeling anxious", "Lack of motivation", "Need focus",
    "Feeling low", "Procrastinating", "Feeling confident",
    "Need inspiration", "Stressed about results",
]

col1, col2 = st.columns(2)
with col1:
    initial=st.selectbox("Choose a common mood:", given_moods)
with col2:
    custom_selection=st.text_input("Or type your own mood (optional)")

final_selected= custom_selection.strip() if custom_selection else initial

if st.button("Generate Motivation 💬"):
    if final_selected:
        with st.spinner("Generating motivation..."):
            motivation_prompt = f"Give a short, powerful motivational message for someone who is {final_selected.lower()}."
            motivation_response = get_ai_response(motivation_prompt)

        st.markdown("### 💡 Your Motivation")
        st.markdown(
            f"""
            <div style="background-color:#fff3e0;padding:15px;border-radius:10px;border-left:5px solid #fb8c00;white-space:pre-wrap;word-wrap:break-word;color:#0d0d0d;">
            <p style="font-size:16px;">{motivation_response.strip()}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("Please select or type how you're feeling.")
