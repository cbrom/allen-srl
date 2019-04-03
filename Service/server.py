import time
from concurrent import futures
import grpc

import srl_pb2
import srl_pb2_grpc

import allen_srl

class SRLServicer(srl_pb2_grpc.SRLServicer):
    def resolve(sel, request, context):
        if request.document is None:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("document is required!")
            return srl_pb2.Output()

        elif request.document == "":
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("document is empty!")
            return srl_pb2.Output()

        response = srl_pb2.Output()

        result = allen_srl.SRL.get_srl(request.document)

        # verbs
        verbs_list = []
        for verb_dic in result['verbs']:
            verbMessage = srl_pb2.Verb(
                verb=verb_dic['verb'], 
                description=verb_dic['description'],
                tags=verb_dic['tags'])
            verbs_list.append(verbMessage)

        response = srl_pb2.Output(
            verbs=verbs_list,
            words=result['words']
        )

        return response

def get_server(port="50051"):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    srl_pb2_grpc.add_SRLServicer_to_server(SRLServicer(), server)
    server.add_insecure_port('[::]:' + str(port))
    return server

if __name__ == "__main__":
    server = get_server()
    server.start()
    print("Server has started on port:", "50051")
    _ONE_DAY = 86400
    try:
        while True:
            time.sleep(_ONE_DAY)
    except KeyboardInterrupt:
        server.stop(1)
