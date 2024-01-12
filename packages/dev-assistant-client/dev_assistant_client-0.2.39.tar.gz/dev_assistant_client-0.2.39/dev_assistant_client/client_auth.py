import os
from colorama import Fore, Style
from .config import api_client
from .utils import save_token, delete_token, get_client_id, APP_URL
import webbrowser
import getpass

class ClientAuth:
    """
    The ClientAuth class handles client-based authentication operations.
    This includes generating a token for the client after authenticating via a web browser.
    """
    
    async def authenticate(self):
        """
        Opens the authentication page in the browser for the client to be authenticated.
        Once authenticated, the user should be provided with a token that they'll enter here.
        """
        print("\nOpening authentication page in browser...")
        
        # Print the URL for the authentication page
        print(f"If not, please open URL in your browser: ", sep="\t", end="\t")
        print(Fore.LIGHTGREEN_EX + f"{APP_URL}/auth/clients/{get_client_id()}" + Style.RESET_ALL)
        
        # Determine the URL based on environment
        base_url = APP_URL
        
        # current client id
        client_id = get_client_id()
        
        webbrowser.open(f'{base_url}/auth/clients/{client_id}')
        token = getpass.getpass("Enter the token received after successful authentication: ")
        
        if token:
            save_token(token)
            print(Fore.LIGHTGREEN_EX + "Authenticated successfully!" + Style.RESET_ALL)
            
        else:
            print(Fore.LIGHTRED_EX + "Authentication failed. Please try again." + Style.RESET_ALL)
            return False

    def deauthenticate(self):
        """
        Deauthenticates the client by deleting the locally stored token.
        """
        try:
            delete_token()
            print("You was disconnected.")
        except FileNotFoundError:
            print("CLI not authenticated.")