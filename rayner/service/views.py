import socket

from django.conf import settings
import phue
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rgbxy import Converter

from rayner.service.models import ChangeEvent
from rayner.service.serializers import ChangeEventSerializer


class LightAPI(APIView):

    def get(self, request):

        # See if we can get the current hue from the light itself
        hex = None
        result = {
            'hex': None,
            'on': None,
            'hue': None,
            'brightness': None,
            'saturation': None,
        }

        if not settings.BRIDGE_SKIP_CHECK:
            try:
                light = self.bridge().get_light(settings.BRIDGE_LIGHT)
                c = Converter()
                hex = c.xy_to_hex(*light.xy)

                result['on'] = light.on
                result['hue'] = light.hue
                result['brightness'] = light.brightness
                result['saturation'] = light.saturation
            except phue.PhueRequestTimeout:
                print('Could not connect to bridge at %s' % settings.BRIDGE_IP)

        # If we can't, check the database
        if hex is None:
            qs = ChangeEvent.objects.order_by('-timestamp')[:1]
            if len(qs) > 0:
                hex = qs[0].color

        # Worst case, default to white
        if hex is None:
            hex = 'ffffff'

        result['hex'] = hex
        return Response(data=result)

    def post(self, request):
        self.bridge().set_light(settings.BRIDGE_LIGHT, 'on', True)
        return Response()

    def delete(self, request):
        self.bridge().set_light(settings.BRIDGE_LIGHT, 'on', False)
        return Response()

    def put(self, request):
        service_ip = socket.gethostbyname(socket.gethostname())
        client_ip = self.get_client_ip(request)
        client_id = request.data.get('client_id', 'Unknown')

        # Figure out how the color is specified
        c = Converter()
        if 'rgb' in request.data:
            r, g, b = request.data['rgb']
            xy = c.rgb_to_xy(r, g, b)
        elif 'hex' in request.data:
            xy = c.hex_to_xy(request.data['hex'])

        hex_color = c.xy_to_hex(*xy)

        # Log the request if a database is present
        if settings.DATABASE_FOUND:
            ce = ChangeEvent(service_ip=service_ip,
                             client_ip=client_ip,
                             client_id=client_id,
                             color=hex_color)
            ce.save()

        # Trigger the change; this will eventually need to be changed to
        # a throttled queue for the load balancing test
        self.bridge().set_light(settings.BRIDGE_LIGHT, 'xy', xy)

        return Response()

    @staticmethod
    def bridge():
        return phue.Bridge(ip=settings.BRIDGE_IP,
                           username=settings.BRIDGE_TOKEN)

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class ChangesAPI(ModelViewSet):

    queryset = ChangeEvent.objects.order_by('-timestamp')
    serializer_class = ChangeEventSerializer
