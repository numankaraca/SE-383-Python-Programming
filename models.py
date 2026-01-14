import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

@dataclass
class Student:
    name: str
    surname: str
    class_name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    grades: Dict[str, List[int]] = field(default_factory=dict)
    absence_count: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "class_name": self.class_name,
            "grades": self.grades,
            "absence_count": self.absence_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Student':
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            surname=data.get("surname"),
            class_name=data.get("class_name"),
            grades=data.get("grades", {}),
            absence_count=data.get("absence_count", 0),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )

    def update_timestamp(self):
        self.updated_at = datetime.now().isoformat()
