import streamlit as st
from openai import OpenAI
import os

# You'll set your API key as a secret in Streamlit Cloud later
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Website Style Advisor", page_icon="🎨")

st.title("🎨 Website Style Advisor")
st.write(
    "Answer five quick questions and get a personalized style brief for your website."
)

questions = [
    "Do you prefer minimalist, modern, classic, or bold design styles?",
    "What colors feel most aligned with your brand or vision?",
    "Are there any websites you love the look of?",
    "What type of fonts appeal to you? (clean sans-serif, elegant serif, playful, etc.)",
    "What overall tone are you going for? (professional, friendly, luxurious, etc.)"
]

responses = []
with st.form(key="style_form"):
    for q in questions:
        responses.append(st.text_input(q))
    submitted = st.form_submit_button("Generate Style Brief")

if submitted:
    summary_prompt = f"""
    Based on these preferences, create a polished, professional website design style brief:

    1. Style: {responses[0]}
    2. Colors: {responses[1]}
    3. Inspirations: {responses[2]}
    4. Fonts: {responses[3]}
    5. Tone: {responses[4]}

    Structure the brief with the following sections:
    - Style Direction
    - Color Palette
    - Font Suggestions
    - Layout Ideas
    - Suggested Tone
    """
    with st.spinner("Generating..."):
        reply = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a branding and web design expert who writes clear, insightful, and practical creative briefs."
                },
                {
                    "role": "user",
                    "content": summary_prompt
                }
            ]
        )
        st.success("Done!")
        st.markdown("### Your Personalized Style Brief")
        st.write(reply.choices[0].message.content.strip())
