import asyncio

from grpclib.client import Channel
from helloworld_grpc import GreeterStub
from helloworld_pb2 import HelloReply, HelloRequest


async def main():
    channel = Channel("192.168.50.226", 50051)
    greeter = GreeterStub(channel)

    reply: HelloReply = await greeter.SayHello(HelloRequest(name="herui"))
    print(reply.message)

    channel.close()


if __name__ == '__main__':
    asyncio.run(main())
