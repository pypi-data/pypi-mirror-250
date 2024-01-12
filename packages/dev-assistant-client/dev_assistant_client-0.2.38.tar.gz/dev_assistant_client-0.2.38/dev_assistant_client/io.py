import json
import logging
import os
import pkg_resources
from time import sleep
from colorama import Fore, Style
from dev_assistant_client.api_client import APIClient
from dev_assistant_client.modules.files import FilesModule
from dev_assistant_client.modules.git import GitModule
from dev_assistant_client.modules.terminal import TerminalModule
from dev_assistant_client.client_auth import ClientAuth
from dev_assistant_client.utils import CALLBACK_URL, CERT_FILE, HEADERS, API_URL, CLIENT_ID, KEY_FILE, dd, now, read_token

class IOAssistant:
    MAX_RETRIES = 3

    @staticmethod
    def execute_request(instruction):
        print(
            now(),
            'Executing request ...',
            sep="\t",
            end="\t",
            flush=True
        )

        response = ""
        module = instruction.get("module").lower()
        operation = instruction.get("operation")
        arguments = instruction.get("arguments")
        if arguments is not None:
            arguments = arguments if isinstance(arguments, list) else [arguments]
        else:
            arguments = []

        for _ in range(IOAssistant.MAX_RETRIES):
            try:
                if module == "files":
                    response = FilesModule(instruction).execute()
                elif module == "terminal":
                    response = TerminalModule(instruction).execute()
                elif module == "git":
                    response = GitModule(instruction).execute()
                else:
                    response = "Invalid module or operation"                
                print(Fore.LIGHTGREEN_EX + "Done ✓" + Style.RESET_ALL)
            except Exception as e:
                logging.error("Error executing request", exc_info=True)
                response = json.dumps({'error': f'Error on the CLI: {str(e)}'}, ensure_ascii=False)
                print(Fore.LIGHTRED_EX + "Fail ✗" + Style.RESET_ALL)
                sleep(1)  # wait before retrying
        return response

    @staticmethod
    async def process_message(message):
        print(
            now(),
            "Receiving request ...",
            message.data.get("feedback") or "",
            sep="\t",
        )

        instruction = message.data

        try:
            await IOAssistant.set_as_processing(instruction)
        except Exception as e:
            logging.error(f"Error while processing message: {e}")
            response_data = json.dumps({'error': f"Error: {e}"}, ensure_ascii=False)
            HEADERS["Authorization"] = f'Bearer {read_token()}'
            instruction["status"] = "failed"
            IOAssistant.send_response(instruction, response_data)
            return

        try:
            response_data = json.loads(IOAssistant.execute_request(instruction))
        except Exception as e:
            logging.error(f"Error while processing message: {e}")
            response_data = json.dumps({'error': f'Error on the CLI: {str(e)}'}, ensure_ascii=False)
        
        HEADERS["Authorization"] = f'Bearer {read_token()}'

        error_response = response_data.get("error") if isinstance(response_data, dict) else None
        response_to_send = error_response if error_response else response_data
        
        instruction["status"] = "failed" if error_response else "completed"
            
        IOAssistant.send_response(instruction, response_to_send)

    @staticmethod
    async def set_as_processing(instruction):
        print(now(), "Setting status ...", sep="\t", end="\t")

        url = f'/io/{instruction.get("id")}'

        for _ in range(IOAssistant.MAX_RETRIES):
            try:
                api_client = APIClient(f"{API_URL}")
                response = api_client.put(url, data={"status": "processing"})

                if response.status_code == 401:
                    print(now(), "Invalid token. Reauthenticating...", sep="\t")
                    client_auth = ClientAuth()
                    await client_auth.authenticate()

                if response.status_code in [200, 201, 202, 204]:
                    output = json.loads(response.content.decode("utf-8"))
                    response = [output.get("response")] if output.get("response") is not None else []
                    print(Fore.LIGHTGREEN_EX + "Done ✓" + Style.RESET_ALL)
                    return response
                else:
                    print(now(), "Error: ", response.status_code, json.loads(response.content.decode("utf-8")))
            except Exception as e:
                print(now(), "Error: ", e)
                sleep(1)

        print(Fore.LIGHTRED_EX + "Failed after max retries" + Style.RESET_ALL)
        return None

    @staticmethod
    def send_response(instruction, data):
        print(
            now(),
            "Returning response ... ",
            sep="\t",
            end="\t",
        )

        url = f'/io/{instruction.get("id")}'

        for attempt in range(IOAssistant.MAX_RETRIES):
            try:
                api_client = APIClient(f"{CALLBACK_URL or API_URL}")

                return_data = {
                    "status": instruction.get("status"),
                    "response": [data]
                }

                response = api_client.put(url, data=return_data)
                if response.status_code == 200:
                    print(Fore.LIGHTGREEN_EX + "Done ✓ " + Style.RESET_ALL)
                    return json.loads(response.content.decode("utf-8"))
                else:
                    print(now(), "Error: ", response.status_code, json.loads(response.content.decode("utf-8")))
            except Exception as e:
                print(Fore.LIGHTRED_EX + "Error:" + Style.RESET_ALL, e)
                if attempt < IOAssistant.MAX_RETRIES - 1:
                    sleep(0.5)  # Espera antes de tentar novamente
                else:
                    print(Fore.LIGHTRED_EX + "Failed after max retries" + Style.RESET_ALL)
                    break  # Sai do loop após o número máximo de tentativas