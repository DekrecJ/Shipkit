from __future__ import annotations
from dataclasses import dataclass, field, asdict

@dataclass
class CheckItem:
    name: str
    status: str  # pass, fail, warn, skip
    detail: str = ""
    blocker: bool = False

@dataclass
class CheckSection:
    name: str
    weight: int
    items: list[CheckItem] = field(default_factory=list)

    def ratio(self) -> float:
        scored = [i for i in self.items if i.status in {"pass", "fail"}]
        if not scored:
            return 1.0
        return sum(1 for i in scored if i.status == "pass") / len(scored)

    def score(self) -> int:
        return round(self.weight * self.ratio())

    def to_dict(self):
        return {"name": self.name, "weight": self.weight, "score": self.score(), "items": [asdict(i) for i in self.items]}
