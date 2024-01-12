from datetime import datetime
from typing import Any, List

from ..constants import SOURCE_NAMES
from ..dataformats import Event

class BellingcatExtractor():
    @staticmethod
    def extract_events(data: List[Any]) -> List[Event]:
        DATE_INPUT_FORMAT = '%m/%d/%Y'
        events = []
        # Convert JSON strings to datetime objects, set links
        for e in data:
            links = [s.get('path') for s in e.get('sources')]
            event = Event(
                id=e.get('id'),
                date=datetime.strptime(e.get('date'), DATE_INPUT_FORMAT),
                latitude=float(lat if (lat := e.get('latitude')) else 0),
                longitude=float(lng if (lng := e.get('longitude')) else 0),
                place_desc=e.get('place_desc'),
                title=e.get('title'),
                description=e.get('description'),
                source=SOURCE_NAMES.BELLINGCAT,
                links=links,
            )
            events.append(event)
        return events
