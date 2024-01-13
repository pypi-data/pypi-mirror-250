from enum import Enum
from typing import Any
from pydantic import BaseModel
from tradelink._src.models.Extended import Extended


class PortfolioModel(BaseModel):
    extended: Extended

    # Other
    createdAt: str
    startDate: str
    updatedAt: str
    views: int
    ctx: str
    disqualified: bool
    userId: str
    name: str
    keyId: str
    keyIds: list[str]
    public: bool
    inRating: bool
    unlisted: bool
    showPositions: bool
    jet: Any  # Optional[dict[str, list[Optional[dict[str, str]] | bool]]]
    description: str
    # marketDirection: None | str
    # speed: None | str
    # managementType: None | str
    # positionType: None | str
    # riskType: None | str
    portfolioId: str
    rank: int
    rankDelta: int
    stars: int


class TradeLinkStep(Enum):
    week = "week"
    day = "day"
    hour = "hour"
    

class ErrorModel(BaseModel):
    data: dict[Any, Any]
    error: str
    code: int
