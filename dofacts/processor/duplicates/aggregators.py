import abc
from typing import Iterable

from dofacts.news.models import News
from dofacts.processor.models import NewsDraft


class NewsDuplicatesAggregator(abc.ABC):
    @abc.abstractmethod
    def group_duplicates(self, news_draft: NewsDraft, duplicates: Iterable[News]):
        pass


class DummyAggregator(NewsDuplicatesAggregator):
    def group_duplicates(self, news_draft: NewsDraft, duplicates: Iterable[News]):
        pass
