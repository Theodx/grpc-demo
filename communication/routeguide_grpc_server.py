# -*- coding: UTF-8 -*-
"""
@Summary ：
@Author  ：Zhuguojun
@Time    ：2022-06-20 14:27
@log     ：
            author datetime(DESC) summary
"""

from concurrent import futures
import math
import time
import grpc
import routeguide_pb2
import routeguide_pb2_grpc
import routeguide_db


def get_feature(db, point):
    for feature in db:
        if feature.location == point:
            return feature
    return None


class RouteGuide(routeguide_pb2_grpc.RouteGuideServicer):
    def __init__(self):
        self.db = routeguide_db.read_routeguide_db()

    def GetFeature(self, request, context):
        feature = get_feature(self.db, request)
        if not feature:
            return routeguide_pb2.Feature(name='', location=request)
        return feature

    def ListFeature(self, request, context):
        """使用for-in yield进行多次返回"""
        left = min(request.lo.longitude, request.hi.longitude)
        right = max(request.lo.longitude, request.hi.longitude)
        top = max(request.lo.latitude, request.hi.latitude)
        bottom = min(request.lo.latitude, request.hi.latitude)
        for feature in self.db:
            if left <= feature.location.longitude <= right and bottom <= feature.location.latitude <= top:
                yield feature

    def RecordRoute(self, request_iterator, context):
        """通过for循环对传入数据进行判断"""
        point_count = 0
        feature_count = 1
        distance = 0.0

        start_time = time.time()
        for point in request_iterator:
            point_count += 1
            if get_feature(self.db, point):
                feature_count += 1
        elapsed_time = time.time() - start_time
        return routeguide_pb2.RouteSummary(
            point_count=point_count,
            feature_count=feature_count,
            distance=int(distance),
            elapsed_time=int(elapsed_time)
        )

    def RouteChat(self, request_iterator, context):
        prev_notes = []
        for new_note in request_iterator:
            for prev_note in prev_notes:
                if prev_note.location == new_note.location:
                    yield prev_note
            prev_notes.append(new_note)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    routeguide_pb2_grpc.add_RouteGuideServicer_to_server(RouteGuide(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(60*60*24) # one day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()