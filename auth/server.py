from concurrent import futures
import grpc
import user_pb2_grpc
import user_pb2


class User(user_pb2_grpc.UserService):
    def GetInfo(self, request, context):
        return user_pb2.UserInfoReply(pk=request.pk, name='John Doe', email='jd@example.com')


if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserService_to_server(User(), server)
    server.add_insecure_port('[::]:50055')
    server.start()
    server.wait_for_termination()
