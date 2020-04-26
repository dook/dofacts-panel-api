from pydoc import locate

from django.apps import AppConfig
from django.conf import settings


class EventsConfig(AppConfig):
    name = "dofacts.events"

    def ready(self):
        for subscribers in settings.EVENTS.values():
            for subscriber_path in subscribers:
                if not locate(subscriber_path):
                    raise ModuleNotFoundError(f"Event subscriber not found <{subscriber_path}>")
