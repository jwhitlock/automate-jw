from ..tasks import OmnifocusTask


class RuleBase:
    def __init__(self, url: str):
        self.url = url

    def is_match(self) -> bool:
        return False

    def as_task(self) -> OmnifocusTask:
        return OmnifocusTask(action="New Task")
