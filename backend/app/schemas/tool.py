from pydantic import BaseModel
from typing import Optional, List


class CustomQueryRequest(BaseModel):
    question: str
    region: Optional[str] = None


class CustomResponse(BaseModel):
    id: int
    title: str
    category: str
    content: str
    region: str


class EtiquetteQueryRequest(BaseModel):
    scenario: str
    category: Optional[str] = None


class EtiquetteResponse(BaseModel):
    id: int
    title: str
    category: str
    content: str


class GiftSuggestionRequest(BaseModel):
    target_group: str
    budget: Optional[str] = None
    occasion: str = "new_year"


class GiftSuggestionResponse(BaseModel):
    id: int
    target_group: str
    gift_name: str
    description: str
    price_range: str


class RedPacketRequest(BaseModel):
    amount_type: str
    relationship: Optional[str] = None
    meaning: Optional[str] = None


class RedPacketResponse(BaseModel):
    amount: str
    meaning: str
    cover_text: str
    message: str


class NewYearMenuRequest(BaseModel):
    people_count: int
    taste_preference: Optional[str] = None
    budget: Optional[str] = None


class NewYearMenuResponse(BaseModel):
    dishes: List[dict]
    meaning: str
    toast_speech: str


class ScheduleRequest(BaseModel):
    date: str
    region: Optional[str] = None
    activity_type: Optional[str] = None


class ScheduleResponse(BaseModel):
    activities: List[dict]
    tips: List[str]
