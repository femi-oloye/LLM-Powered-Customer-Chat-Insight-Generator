import streamlit as st
import pandas as pd

st.set_page_config(page_title="Chat Insight Dashboard", page_icon="🧠", layout="wide")
st.title("🧠 AI-Powered Chat Insight Dashboard")

st.markdown("""
Welcome! This app analyzes customer messages using AI insights. Upload a CSV with:

- Customer  
- Message  
- AI Insight (includes Summary, Sentiment, Suggested Action)

Ideal for showcasing prompt engineering + AI workflows with minimal code.
""")

uploaded_file = st.file_uploader("📤 Upload your chat_insights_output.csv", type=["csv"])

if uploaded_file is not None:
    # Process uploaded file
    try:
        df = pd.read_csv(uploaded_file)

        expected_cols = {"Customer", "Message", "AI Insight"}
        if not expected_cols.issubset(df.columns):
            st.error("❌ CSV must contain: Customer, Message, and AI Insight columns.")
        else:
            def extract_sentiment(insight):
                try:
                    for line in insight.split("\n"):
                        if line.lower().startswith("sentiment:"):
                            return line.split(":")[1].strip().capitalize()
                except:
                    return "Unknown"

            df["Sentiment"] = df["AI Insight"].apply(extract_sentiment)

            # Keyword filter
            keyword = st.text_input("🔍 Search by Keyword (in Message or Insight)", "")
            if keyword:
                df = df[df["Message"].str.contains(keyword, case=False) | df["AI Insight"].str.contains(keyword, case=False)]

            # Sentiment filter
            sentiments = df["Sentiment"].unique().tolist()
            selected_sentiments = st.multiselect("🎯 Filter by Sentiment", sentiments, default=sentiments)
            df = df[df["Sentiment"].isin(selected_sentiments)]

            # Grouping
            group_by_customer = st.checkbox("👥 Group by Customer")
            if group_by_customer:
                grouped = df.groupby("Customer").agg({
                    "Message": lambda x: " | ".join(x),
                    "AI Insight": lambda x: " | ".join(x),
                    "Sentiment": lambda x: ", ".join(x)
                }).reset_index()
                st.subheader("📋 Grouped Chat Insights by Customer")
                st.dataframe(grouped, use_container_width=True)
                csv_to_download = grouped
            else:
                st.subheader("📋 Filtered Chat Insights")
                st.dataframe(df, use_container_width=True)
                csv_to_download = df

            # Sentiment Distribution
            st.subheader("📊 Sentiment Distribution")
            sentiment_count = df["Sentiment"].value_counts()
            st.bar_chart(sentiment_count)

            # Export filtered results
            csv = csv_to_download.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Filtered Results as CSV", csv, "filtered_chat_insights.csv", "text/csv")

    except Exception as e:
        st.error(f"⚠️ Error reading file: {e}")
else:
    # Load sample data if no file uploaded
    try:
        st.info("⬆️ No file uploaded. Loading sample data for demo.")
        sample_df = pd.read_csv("data/chat_insights_output.csv")

        expected_cols = {"Customer", "Message", "AI Insight"}
        if not expected_cols.issubset(sample_df.columns):
            st.error("❌ Sample CSV must contain: Customer, Message, and AI Insight columns.")
        else:
            def extract_sentiment(insight):
                try:
                    for line in insight.split("\n"):
                        if line.lower().startswith("sentiment:"):
                            return line.split(":")[1].strip().capitalize()
                except:
                    return "Unknown"

            sample_df["Sentiment"] = sample_df["AI Insight"].apply(extract_sentiment)

            # Keyword filter
            keyword = st.text_input("🔍 Search by Keyword (in Message or Insight)", "")
            if keyword:
                sample_df = sample_df[sample_df["Message"].str.contains(keyword, case=False) | sample_df["AI Insight"].str.contains(keyword, case=False)]

            # Sentiment filter
            sentiments = sample_df["Sentiment"].unique().tolist()
            selected_sentiments = st.multiselect("🎯 Filter by Sentiment", sentiments, default=sentiments)
            sample_df = sample_df[sample_df["Sentiment"].isin(selected_sentiments)]

            # Grouping
            group_by_customer = st.checkbox("👥 Group by Customer")
            if group_by_customer:
                grouped = sample_df.groupby("Customer").agg({
                    "Message": lambda x: " | ".join(x),
                    "AI Insight": lambda x: " | ".join(x),
                    "Sentiment": lambda x: ", ".join(x)
                }).reset_index()
                st.subheader("📋 Grouped Chat Insights by Customer")
                st.dataframe(grouped, use_container_width=True)
                csv_to_download = grouped
            else:
                st.subheader("📋 Filtered Chat Insights")
                st.dataframe(sample_df, use_container_width=True)
                csv_to_download = sample_df

            # Sentiment Distribution
            st.subheader("📊 Sentiment Distribution")
            sentiment_count = sample_df["Sentiment"].value_counts()
            st.bar_chart(sentiment_count)

            # Export filtered results
            csv = csv_to_download.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Filtered Results as CSV", csv, "filtered_chat_insights.csv", "text/csv")

    except Exception as e:
        st.error(f"⚠️ Error loading sample data: {e}")
