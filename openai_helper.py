import openai
import json
import os
from dotenv import load_dotenv

# ---------------- LOAD ENV VARIABLES ----------------
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


# ---------------- EXTRACTION FUNCTION ----------------
def extract_financial_data(text):

    prompt = get_prompt_financial() + text

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0]["message"]["content"]

    # Default response structure
    default_data = {
        "Company Name": "None",
        "Stock Symbol": "None",
        "Revenue": "None",
        "Net Income": "None",
        "EPS": "None"
    }

    try:
        extracted = json.loads(content)

        # Fill missing values
        for key in default_data:
            if key not in extracted or extracted[key] == "":
                extracted[key] = "None"

        return extracted

    except Exception:
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