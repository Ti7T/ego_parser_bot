from dataclasses import dataclass

@dataclass
class ProgressMetrics:
    points: int
    maps: int
    finishes: int
    rank: int