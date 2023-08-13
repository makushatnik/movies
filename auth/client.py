import grpc
import user_pb2_grpc
import user_pb2

if __name__ == '__main__':
    channel = grpc.insecure_channel('localhost:50055')
    stub = user_pb2_grpc.UserStub(channel)
    response = stub.GetInfo(user_pb2.UserInfoRequest(pk='77c08328-5867-4113-a5bf-59737664741d'))
    print(f"User Info: name: {response.name}")
