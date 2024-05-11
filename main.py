import sys
import os
import asyncio
import websockets
from dotenv import load_dotenv

from unwrapper import Unwrapper
from wrapper import Wrapper

token = ""
if os.path.exists(".env"):
    load_dotenv()
    token = os.getenv("TOKEN") or ""


WS_BATCH_SIZE = 30
MAX_WS_CONNECTIONS = 900
RATE_LIMIT_SLEEP = 65 # 5s buffer
PROGRESS_SPOOF_INTERVAL = 14 # 0.056s * 250 ticks

class WebSocketClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.state = "Connecting"

    async def connect(self):
        try:
            async with websockets.connect(self.endpoint) as websocket:
                self.state = "Established"
                await self.handle_connection(websocket)

        except websockets.exceptions.ConnectionClosedError:
            self.state = "Closed"
        except websockets.exceptions.WebSocketException as e:
            self.state = "Error"
        except TimeoutError:
            self.state = "Error"
        except OSError:
            self.state = "Error"

    async def handle_connection(self, websocket):
        # Convert hex string to binary
        message = Wrapper.socket_init()

        # Send binary message on open
        await websocket.send(message)

        while True:
            # Receive message from server
            received_message = await websocket.recv()

            # Create a new Unwrapper object
            unwrapper = Unwrapper(received_message)

            # Pass the received message to the unwrapper
            result = unwrapper.unwrap()

            # Respond to the server
            await self.respond(websocket, result)


    async def respond(self, websocket, result):
        wrapper = Wrapper()
        response = wrapper.get_response(result, token)
        if not response:
            self.state = "Bugged"
            # Quit event loop
            return
        elif response == True:
            self.state = "Active"
            # Spoof progress
            message = Wrapper.spoof_progress()
            while True:
                await asyncio.sleep(PROGRESS_SPOOF_INTERVAL)
                await websocket.send(message)
        else:
            # Send wrapper results to server
            if not isinstance(response, list):
                response = [response]
            for res in response:
                await websocket.send(res)


async def log_statistics(clients):
    await asyncio.sleep(RATE_LIMIT_SLEEP)

    counter_stats = {
        "Connecting": 0,
        "Established": 0,
        "Closed": 0,
        "Error": 0,
        "Active": 0,
        "Bugged": 0
    }
    for client in clients:
        counter_stats[client.state] += 1

    string = "Socket Statistics: "
    for key, value in counter_stats.items():
        string += f"\n{key}: {value}"
    print(string)

async def main():
    try:
        # Create a list to store all the WebSocket clients
        clients = []
        tasks = []

        # Create MAX_WS_CONNECTIONS instances of the WebSocketClient class in batches of WS_BATCH_SIZE
        for i in range(0, MAX_WS_CONNECTIONS, WS_BATCH_SIZE):
            batch = [WebSocketClient(f"wss://territorial.io/s52/{j}") for j in range(i, i + WS_BATCH_SIZE)]
            clients.extend(batch)

            # Run the WebSocket clients concurrently
            task = asyncio.gather(*(client.connect() for client in batch))
            tasks.append(task)

            batch_count = i // WS_BATCH_SIZE + 1
            max_batch_size = MAX_WS_CONNECTIONS // WS_BATCH_SIZE
            print("----------------------------------------")
            print(f"Batch {batch_count} of {max_batch_size} instantiated.")
            if batch_count < max_batch_size:
                print(f"Instantiating next batch in {RATE_LIMIT_SLEEP} seconds.")

            await log_statistics(clients)

        # await all tasks
        for task in tasks:
            await task

        # Log statistics every RATE_LIMIT_SLEEP seconds
        while True:
            await log_statistics(clients)

    except (KeyboardInterrupt, asyncio.exceptions.CancelledError) as e:
        print("Exiting...")
        os._exit(1 if isinstance(e, KeyboardInterrupt) else 0)

# Run the main function
if __name__ == "__main__":
    # Check if the token is set
    if not token:
        if len(sys.argv) > 1:
            token = sys.argv[1]
        else:
            token = input("Enter account token: ")
    asyncio.run(main())