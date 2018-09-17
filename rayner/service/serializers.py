from rest_framework.serializers import ModelSerializer

from rayner.service.models import ChangeEvent


class ChangeEventSerializer(ModelSerializer):

    class Meta:
        model = ChangeEvent
        fields = ('service_ip', 'client_ip', 'client_id', 'color', 'timestamp')
