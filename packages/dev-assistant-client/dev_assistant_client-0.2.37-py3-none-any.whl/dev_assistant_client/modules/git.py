import json
import logging
import subprocess
from dev_assistant_client.utils import TERMINAL_CWD_FILE

class GitModule:
    def __init__(self, instruction):
        self.client_id = instruction.get("client_id")
        self.feedback = instruction.get("feedback")
        self.module = instruction.get("module")
        self.operation = instruction.get("operation")
        self.arguments = instruction.get("arguments")
        self.operations = {
            "clone": self.clone,
            "status": self.status,
            "checkout": self.checkout,
            "add": self.add,
            "commit": self.commit,
            "push": self.push,
            "pull": self.pull,
            "fetch": self.fetch,
            "merge": self.merge,
            "rebase": self.rebase,
            "reset": self.reset,
            "log": self.log
        }
        self.working_directory = TERMINAL_CWD_FILE
                    
    def execute(self):
        operation = self.operation
        arguments = self.arguments
        operation_func = self.operations.get(operation, self.unknown_operation)
        try:
            result = operation_func(arguments if arguments else [])
            logging.info(f"{operation} executed successfully")
            return result
        except subprocess.CalledProcessError as e:
            logging.error(f"Command failed: {e.cmd}")
            return json.dumps({'error': e.output.decode("utf-8")})
        except Exception as e:
            logging.exception("Unexpected error")
            return json.dumps({'error': str(e)})

    def unknown_operation(self, *args):
        valid_operations = list(self.operations.keys())
        return json.dumps({'error': f'Unknown operation: {self.operation}', 'valid_operations': valid_operations})

    def clone(self, arguments):
        if not arguments or len(arguments) < 1:
            raise ValueError("You must specify a repository to clone.")
        return self._run_git_command(["clone"] + arguments)

    def _run_git_command(self, command):
        full_command = ["git"] + command
        logging.info(f"Running command: {' '.join(full_command)}")
        print(f"Running command: {' '.join(full_command)}")
        response = subprocess.check_output(
            full_command, cwd=self.working_directory, stderr=subprocess.STDOUT
        )
        return json.dumps(response.decode("utf-8"))

    def checkout(self, arguments):
        if not arguments:
            raise ValueError("You must specify a branch or commit to checkout.")
        return self._run_git_command(["checkout"] + arguments)

    def add(self, arguments):
        if not arguments:
            raise ValueError("You must specify a file or pattern to add.")
        return self._run_git_command(["add"] + arguments)

    def commit(self, arguments):
        if not arguments or "--message" not in arguments:
            raise ValueError("You must specify a commit message using '--message'.")
        return self._run_git_command(["commit"] + arguments)

    def push(self, arguments):
        return self._run_git_command(["push"] + arguments)

    def pull(self, arguments):
        return self._run_git_command(["pull"] + arguments)

    def fetch(self, arguments):
        return self._run_git_command(["fetch"] + arguments)

    def merge(self, arguments):
        if not arguments:
            raise ValueError("You must specify a branch to merge.")
        return self._run_git_command(["merge"] + arguments)

    def rebase(self, arguments):
        if not arguments:
            raise ValueError("You must specify a branch to rebase onto.")
        return self._run_git_command(["rebase"] + arguments)

    def reset(self, arguments):
        return self._run_git_command(["reset"] + arguments)

    def log(self, arguments):
        return self._run_git_command(["log"] + arguments)

    def status(self, arguments):
        return self._run_git_command(["status"] + arguments)
        
