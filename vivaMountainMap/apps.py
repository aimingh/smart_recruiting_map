from django.apps import AppConfig
import sys
from django.apps import AppConfig
from .views import get_info
class VivamountainmapConfig(AppConfig):
    name = 'vivaMountainMap'

    def ready(self):
            get_info()


