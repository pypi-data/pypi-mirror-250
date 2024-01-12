
import json
import os
import shutil
import unidiff
import logging
from pathlib import Path
from dev_assistant_client.utils import TERMINAL_CWD_FILE
        

# Setting up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FilesModule:
    def __init__(self, instruction):
        self.client_id = instruction.get("client_id")
        self.feedback = instruction.get("feedback")
        self.module = instruction.get("module")
        self.operation = instruction.get("operation")
        self.arguments = instruction.get("arguments")
        self.operations = {
            "create": self.create,
            "read": self.read,
            "update": self.update,
            "append": self.append,
            "delete": self.delete,
            "list": self.list_dir,
            "copy": self.copy,
            "move": self.move,
            "rename": self.rename,
            "apply_diff": self.apply_diff,
            "exists": self.exists,
            "is_file": self.is_file,
            "is_dir": self.is_dir,
            "get_size": self.get_size,
            "create_directory": self.create_directory,
            "set_permissions": self.set_permissions
        }
        
        self.cwd_file = TERMINAL_CWD_FILE
        self.current_dir = self._load_cwd()  # Load or default to current working directory
    
    def execute(self):
        operation_func = self.operations.get(self.operation, self.unknown_operation)
        try:
            execute_response = operation_func(*self.arguments)
            return json.dumps(execute_response)
        except TypeError as e:
            return json.dumps({'error': f'Invalid arguments for {self.operation}: {str(e)}'}, ensure_ascii=False)
        except FileNotFoundError as e:
            return json.dumps({'error': str(e)}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({'error': f'Error in {self.operation}: {str(e)}'}, ensure_ascii=False)

    def unknown_operation(self, *args):
        valid_operations = list(self.operations.keys())
        return json.dumps({'error': f'Unknown operation: {self.operation}', 'valid_operations': valid_operations})

    def _load_cwd(self):
        """Load the saved current working directory, or default to the system's CWD."""
        try:
            if Path(self.cwd_file).exists():
                with open(self.cwd_file, 'r') as file:
                    saved_dir = file.read().strip()
                    if Path(saved_dir).exists():
                        return saved_dir
        except Exception as e:
            logging.error(f"Error loading saved CWD: {e}")
        return os.getcwd()
    
    def path_exists(self, path):
        return os.path.exists(path)

    def create(self, path, content=None):
        absolute_path = Path(self.current_dir, path).resolve()
        directory = absolute_path.parent
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
        with open(absolute_path, "w", encoding="utf-8") as file:
            if content:
                file.write(content)
        return {"message": f"File created at {absolute_path}"}

    def read(self, path):
        absolute_path = Path(self.current_dir, path).resolve()
        if not self.path_exists(absolute_path):
            return {"error": f"Path does not exist: {absolute_path}"}
        if absolute_path.is_dir():
            return self.list_dir(absolute_path)
        with open(absolute_path, "r", encoding="utf-8") as file:
            content = file.read()
        return {"content": content}

    def update(self, arguments):
        path, content = arguments.split(',')
        if not os.path.exists(path):
            return {"error": f"File does not exist: {path}"}

        with open(path, "w", encoding="utf-8") as file:
            file.write(content)

        return {"message": f"File updated at {path}"}

    def append(self, path, content=""):
        absolute_path = Path(self.current_dir, path).resolve()
        if not self.path_exists(absolute_path):
            return {"error": f"File does not exist: {absolute_path}"}

        with open(absolute_path, "a", encoding="utf-8") as file:
            file.write(content)

        return {"message": f"Content appended to file at {absolute_path}"}
    
    def delete(self, path):
        absolute_path = Path(self.current_dir, path).resolve()
        if not self.path_exists(absolute_path):
            return {"error": f"File does not exist: {absolute_path}"}

        os.remove(absolute_path)
        return {"message": f"File deleted at {absolute_path}"}

    def list_dir(self, path):
        absolute_path = Path(self.current_dir, path).resolve()
        if not self.path_exists(absolute_path):
            return {"error": f"Directory does not exist: {absolute_path}"}

        try:
            files = os.listdir(absolute_path)
        except Exception as e:
            return {"error": f"Error listing directory: {e}"}
        
        return {"files": files}

    def copy(self, source, destination):
        try:
            absolute_source = Path(self.current_dir, source).resolve()
            absolute_destination = Path(self.current_dir, destination).resolve()
            if not self.path_exists(absolute_source):
                return {"error": f"File does not exist: {absolute_source}"}

            shutil.copy(absolute_source, absolute_destination)
            return {"message": f"File copied from {absolute_source} to {absolute_destination}"}
        except Exception as e:
            return {"error": f"Error copying file: {e}"}

    def move(self, source, destination):
        try:
            absolute_source = Path(self.current_dir, source).resolve()
            absolute_destination = Path(self.current_dir, destination).resolve()
            if not self.path_exists(absolute_source):
                return {"error": f"File does not exist: {absolute_source}"}

            shutil.move(absolute_source, absolute_destination)
            return {"message": f"File moved from {absolute_source} to {absolute_destination}"}
        except Exception as e:
            return {"error": f"Error moving file: {e}"}

    def rename(self, source, destination):
        try:
            absolute_source = Path(self.current_dir, source).resolve()
            absolute_destination = Path(self.current_dir, destination).resolve()
            if not self.path_exists(absolute_source):
                return {"error": f"File does not exist: {absolute_source}"}

            os.rename(absolute_source, absolute_destination)
            return {"message": f"File renamed from {absolute_source} to {absolute_destination}"}
        except Exception as e:
            return {"error": f"Error renaming file: {e}"}

    def apply_diff(self, arguments):
        try:
            path, diff_instructions = arguments.split(',')
        except ValueError:
            return {"error": "Invalid arguments. Expected format: 'path,diff_instructions'"}

        absolute_path = Path(self.current_dir, path).resolve()
        if not self.path_exists(absolute_path):
            return {"error": f"File does not exist: {absolute_path}"}

        with open(absolute_path, "r", encoding="utf-8") as file:
            original_content = file.read()

        # Apply diff instructions using unidiff
        patch_set = unidiff.PatchSet.from_string(diff_instructions)
        patched_content = original_content
        for patched_file in patch_set:
            for hunk in patched_file:
                patched_content = hunk.apply_to(patched_content)

        # Save the file after applying the diff
        with open(absolute_path, "w", encoding="utf-8") as file:
            file.write(patched_content)

        return {"message": f"Diff applied to file at {absolute_path}"}

    def exists(self, path):
        absolute_path = Path(self.current_dir, path).resolve()
        return {"exists": self.path_exists(absolute_path)}

    def is_file(self, path):
        absolute_path = Path(self.current_dir, path).resolve()
        return {"is_file": self.path_exists(absolute_path) and os.path.isfile(absolute_path)}

    def is_dir(self, path):
        absolute_path = Path(self.current_dir, path).resolve()
        return {"is_dir": self.path_exists(absolute_path) and os.path.isdir(absolute_path)}

    def get_size(self, path):
        absolute_path = Path(self.current_dir, path).resolve()
        if not self.path_exists(absolute_path):
            return {"error": f"File does not exist: {absolute_path}"}
        return {"size": os.path.getsize(absolute_path)}

    def create_directory(self, path):
        absolute_path = Path(self.current_dir, path).resolve()
        absolute_path.mkdir(parents=True, exist_ok=True)
        return {"message": f"Directory created at {absolute_path}"}

    def set_permissions(self, path, mode):
        absolute_path = Path(self.current_dir, path).resolve()
        if not self.path_exists(absolute_path):
            return {"error": f"File does not exist: {absolute_path}"}
        os.chmod(absolute_path, mode)
        return {"message": f"Permissions set for {absolute_path}"}

