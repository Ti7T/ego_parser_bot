from DifficultyStats import DifficultyStats
from PlayerStats import PlayerStats
from Teammate import Teammate
from Clan import Clan

class JSONConverter:

    @staticmethod
    def _to_difficulty_stats(data: dict) -> DifficultyStats:
        return DifficultyStats(
            easy=data["Easy"],
            main=data["Main"],
            hard=data["Hard"],
            insane=data["Insane"],
            extreme=data["Extreme"],
            jet=data["Jet"],
            solo=data["Solo"],
            mods=data["Mods"],
        )

    @staticmethod
    def _to_clan(data: dict) -> Clan:
        return Clan(
            id=data["id"],
            name=data["name"],
            avatar_url=data["avatar_url"]
        )

    @staticmethod
    def to_player(data : dict) -> PlayerStats:
        return PlayerStats(
            nick=data["nick"],
            #clan=data.get("clan"),
            clan=JSONConverter._to_clan(data["clan"]),
            points=data["points"],
            total_finished_maps=data["total_finished_maps"],
            counts=JSONConverter._to_difficulty_stats(data["counts"]),
            counts_total=JSONConverter._to_difficulty_stats(data["counts_total"]),
            best_teammates=[
                Teammate(
                    nickname=t["nickname"],
                    count=t["count"],
                    avatar_url=t.get("avatar_url")
                )
                for t in data.get("best_teammates", [])
            ]
        )
