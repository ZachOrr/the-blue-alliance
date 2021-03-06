from typing import Dict, List, NewType

from backend.common.consts.api_version import ApiMajorVersion
from backend.common.models.team import Team
from backend.common.queries.dict_converters.converter_base import ConverterBase

TeamDict = NewType("TeamDict", Dict)


class TeamConverter(ConverterBase):
    SUBVERSIONS = {  # Increment every time a change to the dict is made
        ApiMajorVersion.API_V3: 4,
    }

    @classmethod
    def _convert_list(
        cls, model_list: List[Team], version: ApiMajorVersion
    ) -> List[TeamDict]:
        CONVERTERS = {
            ApiMajorVersion.API_V3: cls.teamsConverter_v3,
        }
        return CONVERTERS[version](model_list)

    @classmethod
    def teamsConverter_v3(cls, teams: List[Team]) -> List[TeamDict]:
        return list(map(cls.teamConverter_v3, teams))

    @classmethod
    def teamConverter_v3(cls, team: Team) -> TeamDict:
        default_name = "Team {}".format(team.team_number)
        team_dict = {
            "key": team.key.id(),
            "team_number": team.team_number,
            "nickname": team.nickname if team.nickname else default_name,
            "name": team.name if team.name else default_name,
            "website": team.website,
            "rookie_year": team.rookie_year,
            "motto": None,
            # "home_championship": team.championship_location,  # TODO: event not ported yet
            "school_name": team.school_name,
        }
        team_dict.update(cls.constructLocation_v3(team))
        return TeamDict(team_dict)

    @staticmethod
    def dictToModel_v3(data: Dict) -> Team:
        team = Team(id=data["key"])
        team.team_number = data["team_number"]
        team.nickname = data["nickname"]
        team.name = data["name"]
        team.website = data["website"]
        team.rookie_year = data["rookie_year"]
        team.motto = data["motto"]
        team.city = data["city"]
        team.state_prov = data["state_prov"]
        team.country = data["country"]
        team.school_name = data["school_name"]
        return team
