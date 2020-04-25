from django.core.management.base import BaseCommand

from dofacts.processor.duplicates.aggregators import DummyAggregator
from dofacts.processor.duplicates.finders import DummyDuplicatesFinder
from dofacts.processor.processor import NewsDraftProcessor, StaleNewsProcessor


class Command(BaseCommand):
    help = "Processes a batch of news drafts and assigns fact checkers"

    def handle(self, *args, **options):
        drafts_processor = NewsDraftProcessor(
            finder=DummyDuplicatesFinder(), aggregator=DummyAggregator(),
        )
        stale_news_processor = StaleNewsProcessor()

        stale_news_processor.process_news()
        drafts_processor.process_batch()
