from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_contents import schema_get_file_content,get_file_content
from functions.write_file import schema_write_file,write_file
from functions.run_python_file import schema_run_python_file,run_python_file

available_functions = types.Tool(
    function_declarations=[schema_get_files_info,schema_get_file_content,schema_write_file,schema_run_python_file],
)

def call_function(function_call, verbose=False):
    
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_map = {
        "get_file_content": get_file_content,
        "write_file": write_file,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file
    }

    function_name = function_call.name or ""

    #if the function name isn't part of the available functions, returns a types.Content object to let the LLM and user know what went wrong
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    #creates a shallow copy of the args so that we can modify one argument to ensure working directory is set properly
    args = dict(function_call.args) if function_call.args else {}
    #overwrites the working directory to make sure the LLM doesn't escape into other directories
    args["working_directory"] = "./Playground"

    #time to call the function
    function_result = function_map[function_name](**args)

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)