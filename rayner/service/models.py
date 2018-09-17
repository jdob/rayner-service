from django.db import models


class ChangeEvent(models.Model):

    service_ip = models.CharField(max_length=16)
    client_ip = models.CharField(max_length=16)
    client_id = models.CharField(max_length=128)
    color = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Client [%s] Color [%s]' % (self.client_id, self.color)

