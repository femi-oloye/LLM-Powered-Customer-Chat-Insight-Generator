# 🧠 AI-Powered Chat Insight Dashboard

This Streamlit app allows you to analyze customer messages enhanced with AI-generated insights. It’s designed to demonstrate prompt engineering, language model output handling, and no-code data exploration.

[Live Demo] https://llm-powered-customer-chat-insight-generatorgit-jegqhfuwed2gnv4.streamlit.app/

## 📂 Features

- ✅ Upload AI-generated chat CSVs  
- ✅ Filter by Sentiment (e.g. Positive, Angry, Frustrated)  
- ✅ Keyword search across messages and AI insights  
- ✅ Group chats by Customer  
- ✅ View sentiment distribution as a bar chart  
- ✅ Export filtered results  
- ✅ Try with sample data (no upload required)

## 📊 Sample Use Case

This app was built to simulate a customer service dashboard powered by LLM-generated insights. Great for use cases like:

- Customer complaint tracking
- Support conversation summarization
- CX trend analysis
- Prompt engineering showcases

## 📝 Sample Input Format

The app expects a CSV with these columns:

- **Customer**
- **Message**
- **AI Insight**

Example row from `chat_insights_output.csv`:

| Customer   | Message                                                     | AI Insight                                                                                      |
|------------|-------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| John Doe   | Hi, my internet hasn't worked for two days. I'm frustrated. | Customer Summary: Internet not working... Sentiment: Frustrated. Suggested Action: Troubleshoot. |

## 📦 Folder Structure
```bash
LLM-Powered-Customer-Chat-Insight-Generator/
│
├── data/
    └── chat_insights_output
    └── sample_chats.csv
├── prompts/
    └── summarizer_prompts.txt
├── app.py                        # main app that generates the chat_insights
├── streamlit-app.py              # streamlit app code
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation


## 🚀 How to Run Locally

Clone this repo & run:

```bash
pip install -r requirements.txt
streamlit run app.py

## 📡 Deployment

This app is deployed on Streamlit Cloud. You can fork and redeploy your own version easily by:

1. Forking the repo
2. Visiting [Streamlit Cloud](https://share.streamlit.io)
3. Connecting to your GitHub repo
4. Setting the main file as `app.py`

## 💡 How It Works

The **AI Insight** column contains LLM-generated responses with 3 parts:

- **Customer Summary**
- **Sentiment** (e.g. Angry, Positive, Frustrated)
- **Suggested Action**

The app parses the **Sentiment** and enables filtering, grouping, and visualization to make sense of high-volume customer feedback.

## 🎯 Skills Demonstrated

- 🧠 **Prompt Engineering**
- 🛠️ **LLM Output Parsing**
- 📊 **Streamlit UI/UX**
- 📁 **Project Packaging for Deployment**
- 🔁 **Workflow Automation**

