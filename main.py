import sys
import asyncio
import websockets

from unwrapper import Unwrapper
from wrapper import Wrapper

WS_BATCH_SIZE = 20
MAX_WS_CONNECTIONS = 400
RATE_LIMIT_SLEEP = 45
PROGRESS_SPOOF_INTERVAL = 14 # 0.056s * 250 ticks

token = ""

class WebSocketClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    async def connect(self):
        try:
            async with websockets.connect(self.endpoint) as websocket:
                print(f"WebSocket connection established for {self.endpoint}.")

                await self.handle_connection(websocket)

        except websockets.exceptions.ConnectionClosedError:
            print(f"WebSocket connection closed for {self.endpoint}.")
        except websockets.exceptions.WebSocketException as e:
            print(f"WebSocket error occurred for {self.endpoint}: {str(e)}")
        except TimeoutError:
            print(f"Timeout error occurred for {self.endpoint}.")

    async def handle_connection(self, websocket):
        # Convert hex string to binary
        message = Wrapper.socketInit()

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
        response = wrapper.getResponse(result, token)
        if not response:
            print("BUG")
            # Quit event loop
            return
        elif response == True:
            print(f"Logged in successfully for {self.endpoint}.")
            # Spoof progress
            message = Wrapper.spoofInitProgress()
            while True:
                await asyncio.sleep(PROGRESS_SPOOF_INTERVAL)
                await websocket.send(message)
        else:
            # Send wrapper results to server
            if not isinstance(response, list):
                response = [response]
            for res in response:
                await websocket.send(res)
                    
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
            print(f"Batch {i // WS_BATCH_SIZE + 1} of {MAX_WS_CONNECTIONS / WS_BATCH_SIZE} instantiated. Sleeping for {RATE_LIMIT_SLEEP} seconds.")
            tasks.append(task)

            # Wait for RATE_LIMIT_SLEEP seconds before creating the next batch so we avoid rate limiting
            await asyncio.sleep(RATE_LIMIT_SLEEP)

        # await all tasks
        for task in tasks:
            await task

    except asyncio.exceptions.CancelledError:
        print("Tasks were cancelled.")
    except KeyboardInterrupt:
        print("Exiting...")
        exit()

# Run the main function
if __name__ == "__main__":
    # Check if the token is set
    if not token:
        if len(sys.argv) > 1:
            token = sys.argv[1]
        else:
            token = input("Enter account token: ")
    asyncio.run(main())