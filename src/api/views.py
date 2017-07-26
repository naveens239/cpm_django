from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from cpm.models import Project, Schedule, Material, OrderStatus, Prototype, ScheduleComment, MaterialComment, VendorList
from api.serializer import ProjectSerializer, ScheduleSerializer, MaterialSerializer, VendorListSerializer
from api.serializer import StatusSerializer, PrototypeSerializer,ScheduleCommentSerializer, MaterialCommentSerializer

@api_view(['GET'])
def project_list(request, format=None):
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def schedule_list(request, format=None):
    if request.method == 'GET':
        qfilter = {}
        params = request.query_params
        if 'project_id' in params:
            qfilter['project_name'] = int(params['project_id'])

        schedules = Schedule.objects.filter(**qfilter)
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

@api_view(['GET','PUT'])
def schedule_details(request, pk):
    try:
        s = Schedule.objects.get(pk=pk)
    except Schedule.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ScheduleSerializer(s)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ScheduleSerializer(s,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def material_list(request, format=None):
    if request.method == 'GET':
        qfilter = {}
        params = request.query_params
        if 'project_id' in params:
            qfilter['project_name'] = int(params['project_id'])

        materials = Material.objects.filter(**qfilter).order_by('-added_on')
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)
    else:
        print 'method is ',request.method
@api_view(['GET','PUT'])
def material_details(request, pk):
    try:
        s = Material.objects.get(pk=pk)
    except Material.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MaterialSerializer(s)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = MaterialSerializer(s,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def status_list(request, format=None):
    if request.method == 'GET':
        status = OrderStatus.objects.all()
        serializer = StatusSerializer(status, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def prototype_list(request, format=None):
    if request.method == 'GET':
        qfilter = {}
        params = request.query_params
        if 'project_id' in params:
            qfilter['project_name'] = int(params['project_id'])

        prototypes = Prototype.objects.filter(**qfilter)
        serializer = PrototypeSerializer(prototypes, many=True)
        return Response(serializer.data)

@api_view(['GET','PUT'])
def prototype_details(request, pk):
    try:
        s = Prototype.objects.get(pk=pk)
    except Prototype.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PrototypeSerializer(s)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PrototypeSerializer(s,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def schedule_comment_list(request, format=None):
    print 'request is', request
    if request.method == 'GET':
        qfilter = {}
        params = request.query_params
        if 'schedule_id' in params:
            qfilter['schedule'] = int(params['schedule_id'])

        comments = ScheduleComment.objects.filter(**qfilter)
        print 'comments are', comments
        serializer = ScheduleCommentSerializer(comments, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def order_comment_list(request, format=None):
    print 'request is', request
    if request.method == 'GET':
        qfilter = {}
        params = request.query_params
        if 'order_id' in params:
            qfilter['material'] = int(params['order_id'])

        comments = MaterialComment.objects.filter(**qfilter)
        print 'comments are', comments
        serializer = MaterialCommentSerializer(comments, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def vendor_list(request, format=None):
     if request.method == 'GET':
        vendors = VendorList.objects.all()
        serializer = VendorListSerializer(vendors, many=True)
        return Response(serializer.data)

@api_view(['GET','PUT'])
def vendor_details(request, pk):
    try:
        s = VendorList.objects.get(pk=pk)
    except VendorList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VendorListSerializer(s)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = VendorListSerializer(s,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)