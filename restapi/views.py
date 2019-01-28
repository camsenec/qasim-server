from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.decorators import list_route
from rest_framework import status
from .models import SpinGlassField
from .serializer import ManyItemsSerializer
from qa_simulator.solver import ColoringProblemSolver
from chainercv.datasets import voc_bbox_label_names


class SpinGlassFieldViewSet(viewsets.ModelViewSet):
    queryset = SpinGlassField.objects.all()
    serializer_class = ManyItemsSerializer

    #http://<host_name>/qa_simulator/solve
    @list_route(methods=["post"])
    def solve(self, request):
        name = request.POST["name"]
        trotter_num = request.POST["trotter_num"]
        site_num = request.POST["site_num"]
        result = request.POST["result"]
        data = request.FILES["data"]

        # Delete the previous data ( for test )
        pre_vm = SpinGlassField.objects.all()
        pre_vm.delete()


        if SpinGlassField.objects.filter(name = name).count()!=0:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        #register model
        spin_glass_field = SpinGlassField(name=name,trotter_num=trotter_num, site_num=site_num,result=result, data=data)
        spin_glass_field.save()

        #current_site = get_current_site(request)
        #domain = current_site.domain
        #download_url = download_url = '{0}://{1}{2}'.format(request.scheme,domain,photo.file.url,)

        serializer = ManyItemsSerializer(data={"name":name})

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
