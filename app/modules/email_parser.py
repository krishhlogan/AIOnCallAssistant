def parse_email(email_data):
    return {
        "subject": email_data["subject"],
        "sender": email_data["sender"],
        "body": email_data["body"],
    }
