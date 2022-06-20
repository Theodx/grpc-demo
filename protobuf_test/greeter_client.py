# -*- coding: UTF-8 -*-
"""
@Summary ：
@Author  ：Zhuguojun
@Time    ：2022-06-20 14:01
@log     ：
            author datetime(DESC) summary
"""
import grpc
import hello_pb2_grpc
import hello_pb2

def run():
    # 链接rpc 服务器
    channerl = grpc.insecure_channel('localhost:50051')
    # 调用rpc服务
    stub = hello_pb2_grpc.GreeterStub(channerl)
    response = stub.SayHello(hello_pb2.HelloRequest(name='111'))
    print(response.message)
    response = stub.SayHelloAgain(hello_pb2.HelloRequest(name='222'))
    print(response.message)

if __name__ == '__main__':
    run()