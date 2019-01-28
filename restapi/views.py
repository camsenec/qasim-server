from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.decorators import list_route
from rest_framework import status
from .models import SpinGlassField
from .serializer import ManyItemsSerializer
from qa_simulator.solver import ColoringProblemSolver
from chainercv.datasets import voc_bbox_label_names
import subprocess


class SpinGlassFieldViewSet(viewsets.ModelViewSet):
    queryset = SpinGlassField.objects.all()
    serializer_class = ManyItemsSerializer

    #http://<host_name>/qa_simulator/solve
    @list_route(methods=["post"])
    def solve(self, request):
        subproc_result = subprocess.run(["rm", "data/SG.dat"])

        name = request.POST["name"]
        trotter_num = request.POST["trotter_num"]
        site_num = request.POST["site_num"]
        result = request.POST["result"]
        data = request.FILES["data"]

        # Delete the previous data ( for test )
        pre_vm = SpinGlassField.objects.all()
        pre_vm.delete()

        #nameの重複に対するエラー処理
        if SpinGlassField.objects.filter(name = name).count()!=0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        #register data to database
        spin_glass_field = SpinGlassField(name=name,trotter_num=trotter_num, site_num=site_num,result=result, data=data)
        spin_glass_field.save()

        #solve problem using qa_simulator
        simulator = ColoringProblemSolver(int(trotter_num),int(site_num))
        result = simulator.solve()

        #result update
        spin_glass_field = SpinGlassField.objects.get(name = name)
        spin_glass_field.result = result
        spin_glass_field.save()

        #make serializer
        serializer = ManyItemsSerializer(data={"name":name})

        #response
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
