import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a Python script with optional command-line arguments in a specified file path relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to desired Python script to execute, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the Python script.",
            ),
        },
        required=["file_path"]
    ),
)


def run_python_file(
    working_directory: str, 
    file_path: str, 
    args: list[str] | None = None,
) -> str:

    try:
        output_string = []

        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_dir]
        if args is not None:
            command.extend(args)

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            output_string.append(f"Process exited with code {result.returncode}")
        
        if not result.stdout and not result.stderr:
            output_string.append("No output produced")
        else:
            output_string.append(f"STDOUT: {result.stdout}")
            output_string.append(f"STDERR: {result.stderr}")
        
        return "\n".join(output_string)
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
        
