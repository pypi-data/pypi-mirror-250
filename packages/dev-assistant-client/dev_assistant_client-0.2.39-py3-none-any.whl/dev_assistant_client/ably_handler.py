import asyncio
import json
import pkg_resources
import requests
from ably import AblyRealtime
from colorama import Fore, Style
from dev_assistant_client.config import api_client
from dev_assistant_client.io import IOAssistant
from dev_assistant_client.utils import get_client_id, dd, now, read_token

class AblyHandler:
    def init_ably(self):
        token = None  # Initialize token
        try:
            # Read token and set authorization header
            api_client.token = read_token()
            api_client.headers["Authorization"] = f"Bearer {api_client.token}"

            # Get token request from server
            response = api_client.get(f"/auth/clients/{get_client_id()}/ably")
            if response is not None:
                token_request = json.loads(response.content)
                
                # Check if keyName is in token_request
                if "keyName" not in token_request:
                    print("An error occurred while initializing Ably: 'keyName' not found in token_request")
                    return None

                # Request token from Ably
                token_url = f'https://rest.ably.io/keys/{token_request["keyName"]}/requestToken'
                response = requests.post(token_url, json=token_request)
                
                # Check if response is not None
                if response is not None and response.json() is not None:
                    token = response.json().get("token")

            # Initialize Ably with the received token
            try:
                if token is not None:
                    realtime = AblyRealtime(token=token)
                else:
                    realtime = None
            except Exception as e:
                print(f"An error occurred while initializing Ably: {str(e)}")
                return None
        except Exception as e:
            print(f"An error occurred while initializing Ably: {str(e)}")
            return None

        return realtime

    async def establish_ably_connection(self):
        # Print the current time and a message about establishing a WebSocket connection
        print(now(), "Connecting WebSockets", sep="\t", end="\t")
        # Initialize Ably with the received token
        realtime = self.init_ably()
        # If the initialization fails, print an error message and return
        if realtime is None:
            print(Fore.LIGHTRED_EX + "Connection failed!" + Style.RESET_ALL)
            return
        
        # If the initialization is successful, print a success message
        print(Fore.LIGHTGREEN_EX + "Connected!" + Style.RESET_ALL)

        # Print the current time and a message about connecting to a private channel
        print(now(), "WS private channel...", sep="\t", end="\t")
        # Get the private channel
        privateChannel = realtime.channels.get(f"private:dev-assistant-{get_client_id()}")
        # If the connection to the private channel fails, print an error message and return
        if privateChannel is None:
            print(Fore.LIGHTRED_EX + "Connection failed!" + Style.RESET_ALL)
            return
        
        # If the connection to the private channel is successful, print a success message
        print(Fore.LIGHTGREEN_EX + "Connected!" + Style.RESET_ALL)

        # Subscribe to the private channel and handle incoming messages
        await privateChannel.subscribe(self.handle_ably_message)
        # Print the current time and a message about the connection being ready and listening for instructions
        print(now(), "Connection ready!", "Listening for instructions...", sep="\t")
              
        # Keep the connection alive
        while True:
            await asyncio.sleep(1)
        
    async def handle_ably_message(self, message):
               
        icon_path = pkg_resources.resource_filename('dev_assistant_client', 'icon.ico')
        
        from plyer import notification

        feedback = message.data.get("feedback")
        
        if feedback is not None:
            notification.notify(
                title='Dev Assistant', 
                message=feedback,
                app_name='Dev Assistant',
                app_icon=icon_path, 
                timeout=10, 
                ticker='Dev Assistant Notification', 
                toast=True, 
                hints={"x": 100, "y": 100}
            )

        # Process the received message
        await IOAssistant.process_message(message)