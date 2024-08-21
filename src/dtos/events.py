from dataclasses import dataclass
from typing import Any


@dataclass
class Event():
    change_type: str
    changed_fields: list
    fields: dict[str, Any]