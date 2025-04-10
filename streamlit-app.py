import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv
from collections import Counter
import plotly.express as px
import re
import tempfile
import speech_recognition as sr

# Load API key
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Load summarizer prompt
with open("prompts/summarizer_prompt.txt", "r") as f:
    base_prompt = f.read()

# Sentiment colors
sentiment_colors = {
    "Positive": "#d4edda",
    "Frustrated": "#fff3cd",
    "Angry": "#f8d7da",
    "Negative": "#f5c6cb",
    "Neutral": "#e2e3e5"
}

# Build prompt
def build_prompt(message, language="English"):
    return f"{base_prompt}\n\nCustomer Message:\n{message}\n\nRespond in: {language}"

# Get model response
def get_response(prompt, model):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Extract sentiment
def extract_sentiment(insight):
    match = re.search(r"Sentiment:\s*(.*)", insight)
    return match.group(1).strip() if match else "Unknown"

# Extract top keywords
def extract_keywords(text_list):
    words = " ".join(text_list).lower().split()
    common_words = [word.strip(".,!?") for word in words if len(word) > 3]
    return dict(Counter(common_words).most_common(10))

# Transcribe audio
def transcribe_audio(file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Error from Google API: {e}"

# Streamlit App UI
st.set_page_config(page_title="Customer Chat Insight Generator", layout="wide")
st.title("📊 LLM-Powered Customer Chat Insight Generator")

# File uploads
uploaded_file = st.file_uploader("📤 Upload CSV with `Customer` and `Message` columns", type="csv")
audio_file = st.file_uploader("🎙️ Upload Voice File (WAV format only)", type="wav")

# --- Track model selection to reset state ---
if "last_model_choice" not in st.session_state:
    st.session_state["last_model_choice"] = None

col1, col2 = st.columns(2)
with col1:
    model_choice = st.selectbox("🤖 Choose LLM", ["openai/gpt-3.5-turbo", "openrouter/mistral-7b", "anthropic/claude-3-haiku"])
with col2:
    language_choice = st.selectbox("🌍 Insight Language", ["English", "Spanish", "French", "German", "Arabic", "Chinese"])

# Reset insight data if model changes
if st.session_state["last_model_choice"] != model_choice:
    st.session_state["insight_data"] = None
    st.session_state["last_model_choice"] = model_choice

# Handle voice input
if audio_file is not None:
    st.subheader("🎧 Transcribed Voice Message")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_file.read())
        transcript = transcribe_audio(tmp.name)
        st.text_area("Transcribed Text", transcript)
        if st.button("Generate Insight from Voice"):
            with st.spinner("Analyzing..."):
                prompt = build_prompt(transcript, language_choice)
                insight = get_response(prompt, model_choice)
                st.markdown(f"**AI Insight:**\n\n{insight}")

# Handle CSV
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if "Customer" not in df.columns or "Message" not in df.columns:
        st.error("CSV must contain 'Customer' and 'Message' columns.")
    else:
        st.subheader("✅ File Preview")
        st.dataframe(df.head())

        if st.button("✨ Generate AI Insights"):
            with st.spinner("Thinking..."):
                results = []
                for _, row in df.iterrows():
                    prompt = build_prompt(row["Message"], language_choice)
                    insight = get_response(prompt, model_choice)
                    sentiment = extract_sentiment(insight)
                    results.append({
                        "Customer": row["Customer"],
                        "Message": row["Message"],
                        "AI Insight": insight,
                        "Sentiment": sentiment
                    })

                st.session_state["insight_data"] = pd.DataFrame(results)

# Display Insights
if st.session_state.get("insight_data") is not None:
    df = st.session_state["insight_data"]

    st.subheader("📈 Insight Summary Dashboard")

    # Top keywords
    top_keywords = extract_keywords(df["Message"])
    keywords_df = pd.DataFrame(top_keywords.items(), columns=["Keyword", "Count"])
    fig_keywords = px.bar(keywords_df, x="Keyword", y="Count", title="Top Keywords in Messages")
    st.plotly_chart(fig_keywords, use_container_width=True)

    # Sentiment distribution
    sentiment_counts = df["Sentiment"].value_counts(normalize=True) * 100
    sentiment_df = pd.DataFrame({
        "Sentiment": sentiment_counts.index,
        "Percentage": sentiment_counts.values
    })
    fig_sentiment = px.pie(sentiment_df, names="Sentiment", values="Percentage", title="Sentiment Distribution")
    st.plotly_chart(fig_sentiment, use_container_width=True)

    # Detailed insights
    st.subheader("📝 Detailed Insights")
    sentiment_filter = st.multiselect("🔍 Filter by Sentiment", df["Sentiment"].unique(), default=df["Sentiment"].unique())
    group_by_customer = st.checkbox("👥 Group by Customer")

    filtered_df = df[df["Sentiment"].isin(sentiment_filter)]

    if group_by_customer:
        for customer, group in filtered_df.groupby("Customer"):
            st.markdown(f"### 👤 {customer}")
            for _, row in group.iterrows():
                color = sentiment_colors.get(row["Sentiment"], "#ffffff")
                insight_html = row['AI Insight'].replace('\n', '<br>')
                with st.expander(f"💬 {row['Message']}"):
                    st.markdown(
                        f"""
                        <div style="background-color:{color}; padding:1rem; border-radius:10px;">
                            <b>AI Insight:</b><br>{insight_html}<br>
                            <b>Sentiment:</b> {row["Sentiment"]}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
    else:
        for _, row in filtered_df.iterrows():
            color = sentiment_colors.get(row["Sentiment"], "#ffffff")
            insight_html = row['AI Insight'].replace('\n', '<br>')
            with st.expander(f"👤 {row['Customer']} — 💬 {row['Message']}"):
                st.markdown(
                    f"""
                    <div style="background-color:{color}; padding:1rem; border-radius:10px;">
                        <b>AI Insight:</b><br>{insight_html}<br>
                        <b>Sentiment:</b> {row["Sentiment"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # Download CSV
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Insights CSV", csv, "customer_chat_insights.csv", "text/csv")
