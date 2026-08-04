from dataclasses import dataclass

@dataclass
class Teammate:
    nickname: str
    count: int
    avatar_url: str | None = None