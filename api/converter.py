from models import DifficultyCounter, Player, Clan, Teammate, ActivityRecord

from urllib.parse import urlparse

def is_absolute(url):
    return bool(urlparse(url).scheme)

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
    def _to_clan(data: dict, api_url : str) -> Clan:
        return Clan(
            id=data["id"],
            name=data["name"],
            avatar_url=data["avatar_url"] if is_absolute(data["avatar_url"]) else api_url+data["avatar_url"]
        )

    @staticmethod
    def _to_activity_record(data: dict) -> ActivityRecord:
        return ActivityRecord(
            map_name=data["raw_map_name"],
            time=data["time"],
            rank=data["map_rank"],
            points=data["points_gained"],
            difficulty=data["difficulty"],
            stars=data["stars"],
            is_team=data["is_team_race"],
            is_solo_team=data["is_solo_team"],
            is_refinish=data["is_refinish"],
            finished_at=data["finished_at"],
        )

    @staticmethod
    def to_player(data : dict, api_url : str) -> Player:
        return Player(
            nick=data["nick"],
            #clan=data.get("clan"),
            clan=JSONConverter._to_clan(data["clan"], api_url) if data["clan"] else None,
            points=data["points"],
            rank=data["rank"],
            total_finished_maps=data["total_finished_maps"],
            avatar_url=data["avatar_url"] if is_absolute(data["avatar_url"]) else api_url+data["avatar_url"],
            counts=JSONConverter._to_difficulty_count(data["counts"]),
            counts_total=JSONConverter._to_difficulty_count(data["counts_total"]),
            best_teammates=[
                Teammate(
                    nickname=t["nickname"],
                    count=t["count"],
                    avatar_url=t["avatar_url"] if is_absolute(t["avatar_url"]) else api_url+t["avatar_url"]
                )
                for t in data.get("best_teammates", [])
            ],
            total_playtime=data["playtime"]["total_seconds"],
            activity_records=[
                JSONConverter._to_activity_record(record)
                for record in data.get("activity_records", [])
            ],
        )
