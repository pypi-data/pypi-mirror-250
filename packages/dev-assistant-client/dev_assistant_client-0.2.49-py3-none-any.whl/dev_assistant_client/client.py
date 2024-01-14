import logging
import os
import json
import asyncio
import socket
from colorama import Fore, Style
from .client_auth import ClientAuth
from .api_client import APIClient
from .ably_handler import AblyHandler
from .utils import (
    CERT_FILE,
    CLIENT_ID_FILE,
    KEY_FILE,
    TOKEN_FILE,
    CLIENT_ID,
    API_URL,
    dd,
    now,
    read_token,   
)

async def connect_client():
    """
    Tries to connect the client to the server. It starts by reading a token, creates
    a client payload and makes a POST call to the server. If the call is successful,
    the client is connected and the CLIENT ID is saved locally. Then, it tries to establish
    a WebSocket connection using the establish_ably_connection() function from auth.py.
    """
    print(now(), "Connecting...\t", sep="\t", end="\t")
    api_client = APIClient(f"{API_URL}")
    
    # -------------------
    
    payload = {
        "client_id": CLIENT_ID or "",
        "client_name": socket.gethostname(),
        "client_type": "cli",
    }    
    response = api_client.post(f"/auth/clients", data=payload)
    
    if response and response.status_code == 401:  # Unauthorized call
        auth_client = ClientAuth()
        await auth_client.authenticate()
        await connect_client()
        return
        
    # -------------------
    try:
        client_id = response.json().get("clientId") if response else None
        if response and response.status_code in [200, 201]:
            print(Fore.LIGHTGREEN_EX + "Connected!" + Style.RESET_ALL, sep="\t")
            
            with open(CLIENT_ID_FILE, "w") as f:
                f.write(str(client_id) if client_id else '')

            print(now(), "CLIENT ID: \t", Fore.LIGHTYELLOW_EX + (str(client_id) if client_id else '') + Style.RESET_ALL, sep="\t")
            await AblyHandler().establish_ably_connection()   
        else:
            print(Fore.LIGHTRED_EX + "Failed to connect!" + Style.RESET_ALL, sep="\t")
        
            print( Fore.LIGHTRED_EX + "Error: " + Style.RESET_ALL, response.json().get('error') if response else None, sep="\t")
            print( Fore.LIGHTRED_EX + "Please log in again." + Style.RESET_ALL, sep="\t")
            os.remove(TOKEN_FILE)
            
            # authenticate client again
            auth_client = ClientAuth()
            await auth_client.authenticate()
            await connect_client()
            
            # If a loop is already running, create a new task in the running loop
            if asyncio.get_event_loop().is_running():
                asyncio.create_task(connect_client())
            else:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(connect_client())                   
    except Exception as e:
        print("An error occurred:", e)
