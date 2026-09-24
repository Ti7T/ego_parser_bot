from dataclasses import dataclass

@dataclass
class ActivityRecord:
    map_name: str
    time: float
    rank: int
    points: int
    difficulty: str
    stars: int

    is_team: bool
    is_solo_team: bool
    is_refinish: bool

    finished_at: str