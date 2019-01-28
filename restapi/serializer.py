from rest_framework import serializers
from .models import SpinGlassField


class SpinGlassFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpinGlassField
        fields = ('name','trotter_num', 'site_num', 'result', 'data')

class ManyItemsSerializer(serializers.Serializer):

    """ All 'Item' Model serialize. """
    name = serializers.CharField()
    items = SpinGlassFieldSerializer(many=True, allow_null=True, default=SpinGlassField.objects.all())
