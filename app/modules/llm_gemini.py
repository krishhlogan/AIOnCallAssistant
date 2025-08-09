import json
import os
import re

import google.generativeai as genai
from google.generativeai import GenerativeModel

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

VALID_ISSUE_TYPES = [
    "double_deduction",
    "sync_issue",
    "login_issue",
    "payment_failure"
]

def infer_issue_gemini(subject: str, email_text: str) -> dict:
    try:
        model = GenerativeModel("gemini-2.0-flash")

        prompt = f"""
You are an on-call AI assistant. From the email subject and body, infer:

1. Issue type (one of {VALID_ISSUE_TYPES} or "unknown")
2. Extract these values if present:
   - Policy Number
   - Mobile Number
   - Customer Name
   - SF Ticket Main (12-digit number in subject)
   - SF Ticket Secondary (from 'Ticket No: XYZ')
   - Member Id

Respond ONLY in this JSON format:
{{
  "issue_type": "<inferred type or 'unknown'>",
  "policy_number": "<string or null>",
  "mobile_number": "<string or null>",
  "customer_name": "<string or null>",
  "sf_ticket_main": "<string or null>",
  "sf_ticket_secondary": "<string or null>",
  "member_id": "<string or null>",
  "points" : "<number or null>"
}}

Subject: {subject}

Body:
{email_text}
"""

        response = model.generate_content(prompt)
        print("Response ",response)
        raw_text = response.text.strip()
        print("🔵 Raw Gemini Response:\n", raw_text)

        # Remove markdown-style wrapping like ```json\n ... \n```
        cleaned_json = re.sub(r"^```(?:json)?\n?|```$", "", raw_text.strip(), flags=re.MULTILINE)

        result = json.loads(cleaned_json)
        print('Result', result)
        if result.get("issue_type") not in VALID_ISSUE_TYPES:
            result["issue_type"] = "unknown"

        return result
    except json.JSONDecodeError as jde:
        return {"error": f"JSON parsing error: {str(jde)}", "raw_response": raw_text}
    except Exception as e:
        return {"error": f"gemini_error: {str(e)}"}
