import abc
from typing import Sequence

from dofacts.news.models import News
from dofacts.processor.models import NewsDraft


class NewsDuplicatesFinder(abc.ABC):
    @abc.abstractmethod
    def find_duplicates(self, news_draft: NewsDraft) -> Sequence[News]:
        pass


class DummyDuplicatesFinder(NewsDuplicatesFinder):
    def find_duplicates(self, news_draft: NewsDraft) -> Sequence[News]:
        return []
