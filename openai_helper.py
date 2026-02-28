from openai import OpenAI   
import json
import os
from dotenv import load_dotenv

# ---------------- LOAD ENV VARIABLES ----------------
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ---------------- EXTRACTION FUNCTION ----------------
def extract_financial_data(text):

    prompt = get_prompt_financial() + text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    default_data = {
        "Company Name": "None",
        "Stock Symbol": "None",
        "Revenue": "None",
        "Net Income": "None",
        "EPS": "None"
    }

    try:
        extracted = json.loads(content)

        for key in default_data:
            if key not in extracted or extracted[key] == "":
                extracted[key] = "None"

        return extracted

    except:
        return default_data
    
# ---------------- PROMPT ----------------
def get_prompt_financial():
    return """
Extract company name, revenue, net income, and earnings per share (EPS)
from the following news article.

If any value is missing return "".
Do NOT make assumptions.

Return ONLY valid JSON format:

{
    "Company Name": "",
    "Stock Symbol": "",
    "Revenue": "",
    "Net Income": "",
    "EPS": ""
}

News Article:
============
"""