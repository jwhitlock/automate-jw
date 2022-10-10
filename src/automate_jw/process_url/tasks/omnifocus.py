from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from json import dumps
from typing import Optional, Union


@dataclass
class OmnifocusTask:
    action: str
    flag: bool = False
    project: str = ""
    tags: list[str] = field(default_factory=list)
    note: str = ""
    start_date: Optional[Union[date, datetime]] = None
    due_date: Optional[Union[date, datetime]] = None
    estimate: str = ""

    def __str__(self) -> str:
        def escape_str(in_str: str) -> str:
            trouble_chars = "/#:!@$"
            out_str = in_str
            for c in trouble_chars:
                out_str = out_str.replace(c, f"\\{c}")
            return out_str

        sections: list[str] = []

        assert self.action
        safe_action = escape_str(self.action)
        task_bits: list[str] = [safe_action]
        if self.flag:
            task_bits.append("!")
        if self.project:
            task_bits.extend(("::", escape_str(self.project)))
        sections.append("".join(task_bits))

        start_date = self.start_date
        due_date = self.due_date
        if start_date and not due_date:
            due_date = start_date + timedelta(days=1)
        if start_date:
            sections.append(f"#{start_date.isoformat()}")
        if due_date:
            sections.append(f"#{due_date.isoformat()}")

        if self.estimate:
            sections.append(f"${escape_str(self.estimate)}")

        for tag in self.tags:
            sections.append(f"@{escape_str(tag)}")

        if self.note:
            safe_note = escape_str(self.note)
            sections.append(f"//{safe_note}")

        return " ".join(sections)

    def as_dict(self) -> dict[str, Union[bool, str, list[str]]]:
        ret: dict[str, Union[bool, str, list[str]]] = {"task": self.action}
        if self.flag:
            ret["flag"] = True
        if self.project:
            ret["project"] = self.project
        if self.tags:
            ret["tags"] = self.tags
        if self.start_date:
            ret["start_date"] = self.start_date.isoformat()
        if self.due_date:
            ret["due_date"] = self.due_date.isoformat()
        if self.estimate:
            ret["estimate"] = self.estimate
        if self.note:
            ret["note"] = self.note
        return ret

    def as_json(self) -> str:
        return dumps(self.as_dict())
