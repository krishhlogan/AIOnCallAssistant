from celery import Celery
from modules.llm_infer import infer_issue
from modules.playbook_runner import execute_playbook
from modules.notifier import notify
from dotenv import load_dotenv

import os

load_dotenv()
# Celery config
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_BACKEND_URL = os.getenv("CELERY_BACKEND_URL", "redis://redis:6379/0")

celery_app = Celery("worker", broker=CELERY_BROKER_URL, backend=CELERY_BACKEND_URL)


@celery_app.task(name="process_email")
def process_email(subject, sender, body, llm_provider="openai"):
    try:
        # STEP 1: LLM inference
        inferred_data = infer_issue(subject, body, llm_provider)
        print("Inferred data",inferred_data,type(inferred_data))
        issue_type = inferred_data['issue_type']
        print(f"[Inference] Issue Type: {issue_type}")
        print(f"[Inference] Customer Name: {inferred_data['customer_name']}")
        print(f"[Inference] Policy Number: {inferred_data['policy_number']}")
        print(f"[Inference] Mobile Number: {inferred_data['mobile_number']}")
        print(f"[Inference] Main Ticket #: {inferred_data['sf_ticket_main']}")
        print(f"[Inference] Side Ticket #: {inferred_data['sf_ticket_secondary']}")
        print(f"[Inference] Member id #: {inferred_data['member_id']}")
        print(f"[Inference] Points to refund #: {inferred_data['points']}")

        # STEP 2: Execute actions based on YAML playbook
        context = {
            "subject": subject,
            "sender": sender,
            "body": body,
            "customer_name": inferred_data['customer_name'],
            "policy_number": inferred_data['policy_number'],
            "mobile_number": inferred_data['mobile_number'],
            "main_ticket_number": inferred_data['sf_ticket_main'],
            "side_ticket_number": inferred_data['sf_ticket_secondary'],
            "member_id": inferred_data['member_id'],
            "points": inferred_data['points']
        }

        if issue_type == 'unknown':
            notify(f"⚠️Unhandled Email 📧\n from: {sender}\nsubject: {subject}\nbody: {body}")
            return {
                "status": "success",
                "issue_type": issue_type,
                "result": "Cannot find issue type"
            }
        result = execute_playbook(issue_type, **context)
        print('[Execution] Result:', result)

        # STEP 3: Notify
        notify(f"Issue processed: {issue_type}\n\nResult:\n{result}")

        return {
            "status": "success",
            "issue_type": issue_type,
            "result": result,
        }

    except Exception as e:
        notify(f"Processing failed: {str(e)}")
        return {"status": "error", "message": str(e)}
