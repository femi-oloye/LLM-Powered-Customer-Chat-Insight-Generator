import os
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# Set up OpenAI client with OpenRouter
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Load chat CSV
df = pd.read_csv("data/sample_chats.csv")

# Load summarization prompt template
with open("prompts/summarizer_prompt.txt", "r") as f:
    base_prompt = f.read()

# Function to combine prompt and message
def build_prompt(message):
    return f"{base_prompt}\n\nCustomer Message:\n{message}"

# Function to call OpenRouter's model
def get_response(prompt):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo",  # Change to another if preferred
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Generate insights
results = []
for idx, row in df.iterrows():
    customer = row["Customer"]
    message = row["Message"]
    prompt = build_prompt(message)
    ai_insight = get_response(prompt)

    results.append({
        "Customer": customer,
        "Message": message,
        "AI Insight": ai_insight
    })

# Save to output CSV
output_df = pd.DataFrame(results)
output_df.to_csv("data/chat_insights_output.csv", index=False)
print("✅ AI insights generated and saved to data/chat_insights_output.csv")
