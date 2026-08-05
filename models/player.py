from dataclasses import dataclass
from .difficulty import DifficultyCounter
from .clan import Clan

@dataclass
class Player:
    nick: str
    clan: Clan
    points: int
    total_finished_maps: int

    counts: DifficultyCounter
    counts_total: DifficultyCounter

    best_teammates: list[str]