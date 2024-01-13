import tracemalloc
tracemalloc.start()
import asyncio
import argparse
import time
import sys
from dotenv import load_dotenv
from colorama import Fore, Style
from .client import connect_client
from .client_auth import ClientAuth
from .utils import APP_URL, dd, read_token

import pkg_resources

load_dotenv()

class DevAssistant:
    
    def __init__(self):
        self.auth = ClientAuth()
        self.package_version = pkg_resources.get_distribution("dev_assistant-client").version
        self.print_header()

    def print_header(self):
        print(Fore.LIGHTGREEN_EX +
            '''
        ╭─────╮   Dev Assistant
        │ ''' + Fore.WHITE + '>_<' + Fore.LIGHTGREEN_EX + ''' │   ''' + Fore.LIGHTYELLOW_EX + 'v' + self.package_version + Fore.LIGHTGREEN_EX + ''' 
        ╰─────╯   ''' + Fore.LIGHTYELLOW_EX + APP_URL + Fore.LIGHTGREEN_EX + '''
        ''' + Style.RESET_ALL)

    async def cli(self):
        from .cli import cli
        await cli()

    async def run(self, args=None):
        token = read_token()
        
        if token is None:
            await self.auth.authenticate()
            
        # Parse command line arguments
        parser = argparse.ArgumentParser(prog='dev-assistant-client')
        subparsers = parser.add_subparsers()

        parser_logout = subparsers.add_parser('close')
        parser_logout.set_defaults(func=self.auth.deauthenticate)
                
        try:
            await connect_client()
        except KeyboardInterrupt:
            print("\nProcess interrupted by user. Exiting...")
            await self.close_resources()
            return  # Encerra a execução aqui
        # Removido o bloco finally para evitar chamar cli() após a interrupção
    
    async def close_resources(self):
        """
        This method is used to close any resources or connections.
        """
        # Cancel all tasks lingering
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        
        # Close WebSocket connections, files, database sessions, etc.
        if hasattr(self, 'ably_handler') and self.ably_handler is not None:
            await self.ably_handler.close()
        # Add the closing of other asynchronous resources here if necessary
            
if __name__ == "__main__":
    try:
        asyncio.run(DevAssistant().run())
    except KeyboardInterrupt:
        print("\nInterrupted by user, closing...")
        print("\nSee you soon 👋")
    # Não é necessário chamar loop.close() aqui