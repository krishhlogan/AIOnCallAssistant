import yaml
import subprocess
import os

from jinja2 import Template


def load_playbook(playbook_path="playbooks/oncall_playbook.yaml"):
    if not os.path.exists(playbook_path):
        raise FileNotFoundError(f"Playbook not found at: {playbook_path}")

    with open(playbook_path, "r") as f:
        return yaml.safe_load(f)


def execute_shell(command: str) -> str:
    """Run a shell command and capture its output."""
    try:
        result = subprocess.run(
            command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
        return f"[ERROR] {e.stderr.decode().strip()}"


def render_template(template_string: str, context: dict) -> str:
    """Render a string with Jinja2-style {{ vars }} using context."""
    try:
        return Template(template_string).render(**context)
    except Exception as e:
        return f"[ERROR in templating] {e}"


def execute_playbook(issue_type: str, **context) -> str:
    """Executes steps from the playbook for the given issue type."""
    playbook = load_playbook()
    steps = playbook.get(issue_type)

    if not steps:
        return f"No playbook steps found for issue type: {issue_type}"

    results = []
    for idx, step in enumerate(steps):
        action_type = step.get("type")
        raw_command = step.get("command")
        description = step.get("description", f"Step {idx + 1}")

        results.append(f"➡️ {description}")

        # Render command with variables from context
        command = render_template(raw_command, context)

        if action_type == "shell":
            output = execute_shell(command)
            results.append(f"✅ Output: {output}")
        elif action_type == "http":
            results.append(f"🔗 HTTP call simulated: {command}")
        else:
            results.append(f"⚠️ Unknown action type: {action_type}")

    return "\n".join(results)
