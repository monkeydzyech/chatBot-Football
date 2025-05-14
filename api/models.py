from pydantic import BaseModel, Field

class Player(BaseModel):
    player_name: str
    team_title: str
    league: str
    goals: int = Field(..., ge=0)
    assists: int = Field(..., ge=0)
    games: int = Field(..., ge=0)
