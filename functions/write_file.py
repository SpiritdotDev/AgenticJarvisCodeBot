import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs,file_path))
    valid_targ_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    
    if not valid_targ_dir:
        return f"Error: Cannot write to {file_path} as it is outside the permitted working directory"

    if os.path.isdir(target_file):
        return f"Error: {file_path} is a directory"
    
    #makes sure all parent directories exist, does nothing if they already do.
    os.makedirs(os.path.dirname(target_file), exist_ok=True)

    try:
        with open(target_file, "w") as f:
            f.write(content)
    except:
        return f"Error: failed to write to file at {file_path}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes the given content to a file at the given file path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write contents to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file at the given file path",
            ),
        },
    ),
)