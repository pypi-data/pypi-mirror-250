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
        
        print('Starting Dev Assistant...')

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
        finally:
            time.sleep(1)
            await self.cli()  # Adicione 'await' aqui
            
if __name__ == "__main__":
    asyncio.run(DevAssistant().run())