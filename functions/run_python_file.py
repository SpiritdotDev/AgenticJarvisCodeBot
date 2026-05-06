import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs,file_path))
    valid_targ_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    if not valid_targ_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    try:
        command = ["python", target_file]
        if args != None:
            command.extend(args)

        completed = subprocess.run(command,cwd=working_dir_abs,capture_output=True,text=True,timeout=30)

        output_string = ""
        if completed.returncode != 0:
            output_string += f"Process exited with code {completed.returncode}\n"
        if completed.stdout == None and completed.stderr == None:
            output_string += "No output produced\n"
        else:
            output_string += f"STDOUT: {completed.stdout}\n"
            output_string += f"STDERR: {completed.stderr}\n"
    except:
        return f"Error: executing Python file: {target_file}"

    return output_string


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="runs a Python file at a given file path with given args if any",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write contents to, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An array of possible arguments to be used by the file being called",
                items=types.Schema(
                    type=types.Type.STRING
                )
            ),
        },
    ),
)