from dataclasses import dataclass
from DifficultyStats import DifficultyStats
from Clan import Clan

@dataclass
class PlayerStats:
    nick: str
    clan: Clan
    points: int
    total_finished_maps: int

    counts: DifficultyStats
    counts_total: DifficultyStats

    best_teammates: list[str]