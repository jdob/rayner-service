from django.conf import settings
import phue
from rest_framework.views import APIView
from rest_framework.response import Response


class LightAPI(APIView):

    def post(self, request):
        self.bridge().set_light(settings.BRIDGE_LIGHT, 'on', True)
        return Response()

    def delete(self, request):
        self.bridge().set_light(settings.BRIDGE_LIGHT, 'on', False)
        return Response()

    def put(self, request):
        hue = request.data['hue']
        self.bridge().set_light(settings.BRIDGE_LIGHT, 'hue', hue)
        return Response()

    @staticmethod
    def bridge():
        return phue.Bridge(ip=settings.BRIDGE_IP,
                           username=settings.BRIDGE_TOKEN)
