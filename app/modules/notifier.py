from .slack_notifier import send_slack_message


def notify(parsed):
    print(f"Notification for {parsed}")
    send_slack_message(parsed)
