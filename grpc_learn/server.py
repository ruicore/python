import asyncio

from grpclib.server import Server
from grpclib.utils import graceful_exit
from helloworld_grpc import GreeterBase
from helloworld_pb2 import HelloReply


class Greeter(GreeterBase):
    async def SayHello(self, stream):
        request = await stream.recv_message()
        message = f"Hello,{request.name}"
        await stream.send_message(HelloReply(message=message))


async def main(*, host="192.168.50.226", port=50051):
    server = Server([Greeter()])
    with graceful_exit([server]):
        await server.start(host, port)
        print(f'Serving on {host}:{port}')
        await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())
