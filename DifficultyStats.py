from dataclasses import dataclass

@dataclass
class DifficultyStats:
    easy: int
    main: int
    hard: int
    insane: int
    extreme: int
    jet: int
    solo: int
    mods: int