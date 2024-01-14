import tracemalloc
tracemalloc.start()
import asyncio
import argparse
import time
import sys
from plyer import notification
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
        │ ''' + Fore.WHITE + '>_<' + Fore.LIGHTGREEN_EX + ''' │   ''' + Fore.LIGHTYELLOW_EX + 'Python CLI v' + self.package_version + Fore.LIGHTGREEN_EX + ''' 
        ╰─────╯   ''' + Fore.LIGHTYELLOW_EX + APP_URL + Fore.LIGHTGREEN_EX + '''
        ''' + Style.RESET_ALL)

    async def cli(self):
        from .cli import cli
        await cli()

    def show_ready_notification():
        notification.notify(
            title='Dev Assistant',
            message='Dev Assistant está pronto para te ajudar!',
            app_name='Dev Assistant',
            timeout=10
        )

    async def run(self, args=None):
        token = read_token()
        
        if token is None:
            await self.auth.authenticate()
        
        self.show_ready_notification()
            
        # Parse command line arguments
        parser = argparse.ArgumentParser(prog='dev-assistant-client')
        subparsers = parser.add_subparsers()

        parser_logout = subparsers.add_parser('close')
        parser_logout.set_defaults(func=self.auth.deauthenticate)
                    
        try:
            await connect_client()
        except KeyboardInterrupt:
            print("\nProcesso interrompido pelo usuário. Saindo...")
            await self.close_resources()
        except asyncio.CancelledError:
            print("\nTarefas do main_loop canceladas. Executando a limpeza...")
            await self.close_resources()
        return
    
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

async def main():    
    try:
        await asyncio.create_task(DevAssistant().run())
    except asyncio.CancelledError:
        print("Main loop cancelado do lado de fora.")
        
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Interrupção do teclado detectada. Encerrando o programa...")
        tasks = asyncio.all_tasks(loop)
        for t in tasks:
            t.cancel()
        loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
        loop.close()
        print("\nSee you soon 👋")
    # No need to call loop.close() here