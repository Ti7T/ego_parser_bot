from dataclasses import dataclass
from .difficulty import DifficultyCounter
from .clan import Clan

@dataclass
class Player:
    nick: str
    clan: Clan | None
    points: int
    rank: int
    total_finished_maps: int

    avatar_url: str

    counts: DifficultyCounter
    counts_total: DifficultyCounter

    best_teammates: list[str]