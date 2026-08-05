from models import DifficultyCounter, Player, Clan, Teammate

class JSONConverter:

    @staticmethod
    def _to_difficulty_count(data: dict) -> DifficultyCounter:
        return DifficultyCounter(
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
    def to_player(data : dict) -> Player:
        return Player(
            nick=data["nick"],
            #clan=data.get("clan"),
            clan=JSONConverter._to_clan(data["clan"]) if data["clan"] else None,
            points=data["points"],
            total_finished_maps=data["total_finished_maps"],
            counts=JSONConverter._to_difficulty_count(data["counts"]),
            counts_total=JSONConverter._to_difficulty_count(data["counts_total"]),
            best_teammates=[
                Teammate(
                    nickname=t["nickname"],
                    count=t["count"],
                    avatar_url=t.get("avatar_url")
                )
                for t in data.get("best_teammates", [])
            ]
        )
