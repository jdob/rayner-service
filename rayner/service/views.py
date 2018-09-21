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

        hex_color = None
        result = {
            'hex': None,
            'on': None,
            'hue': None,
            'brightness': None,
            'saturation': None,
        }

        # See if we can get the current hue from the light itself
        if not settings.BRIDGE_MOCK:
            try:
                light = self.bridge().get_light(settings.BRIDGE_LIGHT)
                c = Converter()
                state = light['state']
                hex_color = c.xy_to_hex(*state['xy'])

                result['on'] = state['on']
                result['hue'] = state['hue']
                result['brightness'] = state['bri']
                result['saturation'] = state['sat']
            except phue.PhueRequestTimeout:
                print('Could not connect to bridge at %s' % settings.BRIDGE_IP)

        # If we can't, check the database
        if hex_color is None:
            qs = ChangeEvent.objects.order_by('-timestamp')[:1]
            if len(qs) > 0:
                hex_color = qs[0].color

        # Worst case, default to white
        if hex_color is None:
            hex_color = 'ffffff'

        result['hex'] = hex_color
        return Response(data=result)

    def post(self, request):
        if not settings.BRIDGE_MOCK:
            self.bridge().set_light(settings.BRIDGE_LIGHT, 'on', True)
        return Response()

    def delete(self, request):
        if not settings.BRIDGE_MOCK:
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

        # There should probably be a throttle in place, but I can control
        # that elsewhere in the demo
        if not settings.BRIDGE_MOCK:
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
