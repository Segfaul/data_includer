from rest_framework import serializers
from table.models import *


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'file', 'user']
