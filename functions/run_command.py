import subprocess
from google.genai import types

# Tool declaration / Schema for the model
schema_run_command = types.FunctionDeclaration(
    name="run_command",
    description="Runs a shell command (such as 'go run main.go', 'python3 test.py', or 'go test') inside the working directory and returns the output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "command": types.Schema(
                type=types.Type.STRING,
                description="The shell command to execute.",
            )
        },
        required=["command"],
    ),
)


def run_command(working_directory: str, command: str) -> str:
    try:
        result = subprocess.run(
            command,
            cwd=working_directory,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout
        if result.stderr:
            output += f"\nStderr:\n{result.stderr}"
        return output if output else "Command executed successfully with no output."
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds."
    except Exception as e:
        return f"Error executing command: {str(e)}"