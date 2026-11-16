from dataclasses import dataclass

@dataclass
class FireStats:
    current: int
    best: int
    done_today: bool
    badge: bool