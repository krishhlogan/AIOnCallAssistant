import subprocess

def execute_actions(playbook, context):
    results = []
    for step in playbook.get("steps", []):
        action = step.get("action")
        if action == "run_shell":
            cmd = step["command"]
            try:
                output = subprocess.check_output(cmd, shell=True, text=True)
                results.append({"step": step["name"], "output": output})
            except Exception as e:
                results.append({"step": step["name"], "error": str(e)})
    return results
