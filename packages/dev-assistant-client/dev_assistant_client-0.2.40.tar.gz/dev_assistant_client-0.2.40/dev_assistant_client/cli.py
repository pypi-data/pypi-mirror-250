import argparse
import os
from colorama import Fore, Style
from dotenv import load_dotenv
import logging
import requests
from packaging import version
from .utils import dd
import pkg_resources

from .dev_assistant_client import DevAssistant

load_dotenv()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
if os.getenv('DEBUG', 'False') != 'True':
    logging.disable()

def check_for_update():
    """
    Checks if there's an update available for the 'dev-assistant-client' package.
    Compares the current version with the latest version available on PyPI.
    Returns:
        bool: True if an update is available, False otherwise.
    """
    try:
        response = requests.get(f"https://pypi.org/pypi/dev-assistant-client/json")
        latest_version = response.json()["info"]["version"]
    except Exception as e:
        logging.error("Failed to check for updates: %s", e)
        return False

    current_version = pkg_resources.get_distribution("dev-assistant-client").version

    return version.parse(latest_version) > version.parse(current_version)


async def cli():
    """
    The main CLI entry point. Handles the command-line arguments, checks for updates,
    and runs the DevAssistant client.
    """        
    try:
        if check_for_update():
            print(Fore.LIGHTYELLOW_EX + "📦 New version available! "  + Style.RESET_ALL + "\nPlease run 'pip install --upgrade dev-assistant-client' to upgrade." )
    except Exception as e:
        logging.error("Failed to check for updates: %s", e)

    DEBUG = os.getenv('DEBUG', 'False') == 'True'

    # Setup CLI
    parser = argparse.ArgumentParser(description="Dev Assistant CLI.")
    parser.add_argument(
        "-d", "--debug", action="store_true", default=DEBUG, help="prints extra information"
    )
    parser.add_argument(
        "-v", "--version", action="store_true", help="show program's version number and exit"
    )
    
    try:
        args = parser.parse_args()
    except Exception as e:
        logging.error("Failed to parse arguments: %s", e)
        return

    if args.version:
        print("Dev Assistant", pkg_resources.get_distribution("dev-assistant-client").version)
        return
    if args.debug:
        logging.disable(0)

    try:
        dev_assistant = DevAssistant()
        await dev_assistant.run()

    except KeyboardInterrupt:
        print("\nInterrupção pelo usuário, encerrando...")
        # Close resources and cancel pending tasks
        await dev_assistant.close_resources()
        return  # Encerra a função CLI

    except Exception as e:
        logging.error("Falha ao executar DevAssistant: %s", e)
