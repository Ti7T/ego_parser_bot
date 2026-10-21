from dataclasses import dataclass

@dataclass
class Clan:
    id: int | None
    name: str | None
    avatar_url: str | None = None