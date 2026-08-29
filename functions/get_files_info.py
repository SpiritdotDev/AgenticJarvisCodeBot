import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    import os
from pathlib import Path


def get_files_info(working_directory, directory="."):
    base_path = Path(working_directory).resolve()
    target_dir = (base_path / directory).resolve()

    if not target_dir.exists():
        return f"Error: Directory '{directory}' does not exist."

    entries = []
    # List items inside the directory, not the directory itself
    for entry in target_dir.iterdir():
        file_type = "directory" if entry.is_dir() else "file"
        size = entry.stat().st_size
        entries.append(f"{entry.name}: type={file_type}, size={size} bytes")

    if not entries:
        return "Directory is empty."

    return "\n".join(entries)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)