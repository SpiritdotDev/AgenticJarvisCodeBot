import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs,directory))
    valid_targ_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    
    if not valid_targ_dir:
        return f"Error: Cannot list {directory} as it is outside the permitted working directory"
    
    if not os.path.isdir(target_dir):
        return f"Error: {directory} is not a directory"
    try:
        directory_list = os.listdir(target_dir)
    except:
       return "Error: os.listdir() did not resolve"
    pre_format_list= []

    for item in directory_list:
       try:
        pre_format_list.append(
           f"{item}: file_size={os.path.getsize(os.path.normpath(os.path.join(target_dir,item)))},is_dir={os.path.isdir(os.path.normpath(os.path.join(target_dir,item)))}"
           ) 
       except:
          return "Error: There was a problem listing the directory contents"
       
    formatted_report = "\n- ".join(pre_format_list)

    return formatted_report

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