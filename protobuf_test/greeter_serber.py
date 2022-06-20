# -*- coding: UTF-8 -*-
"""
@Summary ：
@Author  ：Zhuguojun
@Time    ：2022-06-20 10:59
@log     ：
            author datetime(DESC) summary
"""
import grpc
from concurrent import futures
import time
import hello_pb2
import hello_pb2_grpc

class Greeter(hello_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return hello_pb2.HelloReply(message = f'hello {request.name}')

    def SayHelloAgain(self, request, context):
        return hello_pb2.HelloReply(message = f'hello {request.name}')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(),server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(60*60*24)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
