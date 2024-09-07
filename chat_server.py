import asyncio
from asyncio import StreamReader, StreamWriter
from typing import List

class ChatServer():
    def __init__(self):
        self.clients: List[StreamWriter] = []
    
    async def handle_client(self, reader: StreamReader, writer: StreamWriter) -> None:
        """
        Handle a client connection, read messages, and broadcast them to others.

        Args:
            reader (StreamReader): _asyncio class that reads data asynchronously from a stream
            writer (StreamWriter): asyncio class that writes data asynchronously to a stream
        """
        
        addr = writer.get_extra_info('peername')
        print(f"{addr} connected")
        
        # add this client to list
        
        self.clients.append(writer)
        try:
            while True:
                data = await reader.readline()  # Read until newline
                print(data)
                message = data.decode().strip()
                if not data:
                    break
                print(f"Received message from {addr}: {message}")
                await self.broadcast_message(f"{addr}: {message}\n", writer)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f'error {repr(e)}')
        finally:
            print(f"{addr} disconnected")
            self.clients.remove(writer)
            writer.close()
            await writer.wait_closed()

    async def broadcast_message(self, message: str, sender_writer: object):
        """
        Broadcast a message to all clients except the sender.
        Args:
            message (str): received message that needs to be broadcasted
            sender_writer (StreamWriter): asyncio class that writes data asynchronously to a stream
        """
        print(f'broadcasting {message}')
        for client in self.clients:
            if client != sender_writer:
                client.write(message.encode())
                await client.drain()
                print('ok')
    
    async def start_server(self, host: str='127.0.0.1', port: int=8888):
        """
        Start the chat server and accept client connections.
        Args:
            host (str, optional): _description_. Defaults to '127.0.0.1':str.
            port (int, optional): _description_. Defaults to 8888:int.
        """
        
        server = await asyncio.start_server(self.handle_client, host, port)
        
        async with server:
            await server.serve_forever()
        
if __name__ == '__main__':
    chat_server = ChatServer()
    asyncio.run(chat_server.start_server('localhost', '8888'))