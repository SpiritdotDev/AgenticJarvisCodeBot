import os
from google.genai import types

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs,file_path))
    valid_targ_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    
    if not valid_targ_dir:
        return f"Error: Cannot list '{file_path}' as it is outside the permitted working directory"
    
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_file, "r") as f:
            content = f.read(10000)

            if f.read(1):
                content += f'[...File "{file_path}" truncated at {10000} characters]'
    
    except:
        return f"Error: failed to open or read file at {target_file}"
    
    return content

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the contents of a given file and returns it as a string output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to pull contents from, relative to the working directory",
            ),
        },
    ),
)