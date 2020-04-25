import abc
from typing import Sequence

from dook.news.models import News
from dook.processor.models import NewsDraft


class NewsDuplicatesFinder(abc.ABC):
    @abc.abstractmethod
    def find_duplicates(self, news_draft: NewsDraft) -> Sequence[News]:
        pass


class DummyDuplicatesFinder(NewsDuplicatesFinder):
    def find_duplicates(self, news_draft: NewsDraft) -> Sequence[News]:
        return []
