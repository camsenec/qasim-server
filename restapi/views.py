from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import status
from .models import SpinGlassField
from .serializer import SpinGlassFieldSerializer
from qa_simulator.solver import ColoringProblemSolver
from chainercv.datasets import voc_bbox_label_names
from django.shortcuts import render
import subprocess


def manual(request):
    context = {}
    return render(request, 'manual.html', context)


class SpinGlassFieldViewSet(viewsets.ModelViewSet):
    queryset = SpinGlassField.objects.all()
    serializer_class = SpinGlassFieldSerializer

    #http://<host_name>/qa_simulator/solve
    @list_route(methods=["post"])
    def solve(self, request):
        #delete preveous file(for test)
        subproc_result = subprocess.run(["rm", "data/SG.csv"])

        #read POST params
        name = request.POST["name"]
        trotter_num = request.POST["trotter_num"]
        site_num = request.POST["site_num"]
        result = request.POST["result"]
        data = request.FILES["data"]

        # Delete the previous data ( for test )
        pre = SpinGlassField.objects.all()
        pre.delete()

        #error exception for multiple name in model
        if SpinGlassField.objects.filter(name = name).count()!=0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        #register data to database
        spin_glass_field = SpinGlassField(name=name,trotter_num=trotter_num, site_num=site_num,result=result, data=data)
        spin_glass_field.save()

        #solve problem using qa_simulator
        simulator = ColoringProblemSolver(int(trotter_num),int(site_num))
        result = simulator.solve()

        #model update based on the result
        spin_glass_field = SpinGlassField.objects.get(name = name)
        spin_glass_field.result = result
        spin_glass_field.save()

        #create serializer
        spin_glass_field = SpinGlassField.objects.get(name = name)
        serializer = self.get_serializer(spin_glass_field)

        return Response(serializer.data, status=status.HTTP_200_OK)
