import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

VALID_ISSUE_TYPES = [
    "double_deduction",
    "sync_issue",
    "login_issue",
    "payment_failure"
]

def infer_issue_openai(subject: str, email_text: str) -> dict:
    try:
        prompt = f"""
You are an on-call AI assistant. Based on the email subject and body, do the following:

1. Infer the issue type (choose only from {VALID_ISSUE_TYPES} or respond "unknown").
2. Extract any of the following if present:
   - Policy Number
   - Mobile Number
   - Customer Name
   - SF Ticket Main (12-digit number in subject)
   - SF Ticket Secondary (from 'Ticket No: XYZ')

Return ONLY a valid JSON in this format:
{{
  "issue_type": "<inferred type or 'unknown'>",
  "policy_number": "<string or null>",
  "mobile_number": "<string or null>",
  "customer_name": "<string or null>",
  "sf_ticket_main": "<string or null>",
  "sf_ticket_secondary": "<string or null>"
}}

Subject: {subject}

Body:
{email_text}
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert support assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=500
        )

        content = response['choices'][0]['message']['content'].strip()

        # Ensure JSON-like response
        result = eval(content) if content.startswith("{") else {"error": "Malformed response"}
        if result.get("issue_type") not in VALID_ISSUE_TYPES:
            result["issue_type"] = "unknown"
        return result

    except Exception as e:
        return {"error": f"openai_error: {str(e)}"}
