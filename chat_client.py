import asyncio

async def read_message(reader: asyncio.StreamReader) -> None:
    """
    Read messages from the server.
    Args:
        reader (asyncio.StreamReader): asyncio class that reads data asynchronously from a stream
    """
    
    while True:
        data = await reader.readline() # Read from server
        print(data)
        if not data:
            print("Connection closed by the server.")
            break
        print(data.decode().strip())
    
async def send_message(writer: asyncio.StreamWriter, loop) -> None:
    """
    Send messages to the server.
    Args:
        writer (asyncio.StreamWriter): asyncio class that writes data asynchronously to a stream
    """
    while True:
        message = await loop.run_in_executor(None, input, 'You: ') # Get input from user
        writer.write((message + '\n').encode())  # Send message followed by newline
        await writer.drain()  # Ensure the message is sent
        
async def start_client(host='127.0.0.1', port='8888'):
    """
    Start the chat client, connect to the server, and send/receive messages.

    Args:
        host (str, optional): host of the chat server. Defaults to '127.0.0.1'.
        port (str, optional): port of the chat server. Defaults to '8887'.
    """
    
    reader, writer = await asyncio.open_connection(host, port)
    
    loop = asyncio.get_running_loop()
    
    await asyncio.gather(
        read_message(reader),
        send_message(writer, loop)
    )
    
if __name__ == "__main__":
    asyncio.run(start_client())