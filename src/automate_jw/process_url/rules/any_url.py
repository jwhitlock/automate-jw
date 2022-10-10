from ..tasks import OmnifocusTask
from .base import RuleBase


class AnyURL(RuleBase):
    def is_match(self) -> bool:
        return True

    def as_task(self) -> OmnifocusTask:
        return OmnifocusTask(action=f"Read {self.url}", note=self.url, tags=["Laptop"])
