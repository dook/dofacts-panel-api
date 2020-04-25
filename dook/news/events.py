from dook.events.services import ModelEventService


class NewsEvents(ModelEventService):
    def new_verdict(self, *args, **kwargs):
        if not hasattr(self.obj, "_verdict"):
            raise AttributeError("_verdict attribute is missing. Call is_with_verdict()")

        self._send("news_new_verdict", *args, **kwargs)
